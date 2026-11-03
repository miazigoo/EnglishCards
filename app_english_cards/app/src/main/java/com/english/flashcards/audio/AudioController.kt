package com.english.flashcards.audio

import android.content.Context
import android.content.res.AssetFileDescriptor
import android.media.MediaPlayer
import android.os.Handler
import android.os.Looper
import android.util.Log
import com.english.flashcards.model.Flashcard
import org.json.JSONArray
import java.io.InputStreamReader

class AudioController(
    private val context: Context,
    private val onPlaybackStateChanged: (isPlaying: Boolean) -> Unit,
    private val onRepetitionUpdate: (currentRep: Int, maxRep: Int) -> Unit,
    private val onCardFinished: () -> Unit
) {
    private val TAG = "AudioController"
    private var mediaPlayer: MediaPlayer? = null
    private val handler = Handler(Looper.getMainLooper())
    private var currentCard: Flashcard? = null
    private var isAutoPlayEnabled = false
    private var maxRepetitions = 1
    private var currentRepetition = 0
    private var isPlaying = false
    private var sessionToken = 0L

    // Manifest: cardId -> (role -> relativeAssetPath)
    private val manifestMap = HashMap<String, MutableMap<String, String>>()

    init {
        loadManifest()
    }

    private fun loadManifest() {
        try {
            val stream = context.assets.open("audio_manifest.json")
            val text = InputStreamReader(stream).readText()
            val arr = JSONArray(text)
            for (i in 0 until arr.length()) {
                val item = arr.getJSONObject(i)
                val cid = item.optString("card_id")
                val role = item.optString("role")
                val path = item.optString("file_path")
                if (cid.isNotEmpty() && role.isNotEmpty() && path.isNotEmpty()) {
                    val map = manifestMap.getOrPut(cid) { HashMap() }
                    map[role] = path
                }
            }
            Log.d(TAG, "Loaded manifest with ${manifestMap.size} card mappings.")
        } catch (e: Exception) {
            Log.w(TAG, "Audio manifest not found or failed to load: ${e.message}")
        }
    }

    fun setAutoPlay(enabled: Boolean) {
        isAutoPlayEnabled = enabled
        onPlaybackStateChanged(isPlaying || isAutoPlayEnabled)
    }

    fun isAutoPlay(): Boolean = isAutoPlayEnabled

    fun setMaxRepetitions(count: Int) {
        maxRepetitions = maxOf(1, count)
    }

    fun getMaxRepetitions(): Int = maxRepetitions

    /**
     * Plays ONLY the prompt audio for Active Recall (NO SPOILERS).
     * In EN -> RU mode, plays only term_en. Never plays translation before reveal.
     */
    fun playPrompt(card: Flashcard, isEnToRu: Boolean = true) {
        stop()
        currentCard = card
        val role = if (isEnToRu) "term_en" else "meaning_ru"
        val path = getSegmentPath(card, role)
        if (path != null) {
            playSingleFile(path)
        } else {
            Log.d(TAG, "Single segment for prompt role '$role' not found for card ${card.cardId}")
        }
    }

    /**
     * Plays only the English term (single segment).
     */
    fun playTerm(card: Flashcard) {
        stop()
        val path = getSegmentPath(card, "term_en")
        if (path != null) {
            playSingleFile(path)
        } else {
            Log.d(TAG, "term_en not found in manifest for ${card.cardId}")
        }
    }

    /**
     * Plays only the English example phrase (single segment).
     */
    fun playExample(card: Flashcard) {
        stop()
        val path = getSegmentPath(card, "example_en")
        if (path != null) {
            playSingleFile(path)
        } else {
            Log.d(TAG, "example_en not found in manifest for ${card.cardId}")
        }
    }

    /**
     * Introduction mode: plays full sequence once:
     * term_en -> meaning_ru -> example_en -> example_ru
     */
    fun playIntroduction(card: Flashcard) {
        stop()
        currentCard = card
        currentRepetition = 1
        onRepetitionUpdate(1, 1)

        val paths = mutableListOf<String>()
        getSegmentPath(card, "term_en")?.let { paths.add(it) }
        getSegmentPath(card, "meaning_ru")?.let { paths.add(it) }
        getSegmentPath(card, "example_en")?.let { paths.add(it) }
        getSegmentPath(card, "example_ru")?.let { paths.add(it) }

        if (paths.isNotEmpty()) {
            playSequence(paths)
        } else {
            playLegacyFallback(card)
        }
    }

    /**
     * Listening mode with configured repetitions (1x, 2x, 3x).
     */
    fun playListening(card: Flashcard, restartRepetitions: Boolean = true) {
        stop()
        currentCard = card
        if (restartRepetitions) {
            currentRepetition = 1
        }
        onRepetitionUpdate(currentRepetition, maxRepetitions)

        val paths = mutableListOf<String>()
        getSegmentPath(card, "term_en")?.let { paths.add(it) }
        getSegmentPath(card, "meaning_ru")?.let { paths.add(it) }
        getSegmentPath(card, "example_en")?.let { paths.add(it) }
        getSegmentPath(card, "example_ru")?.let { paths.add(it) }

        if (paths.isNotEmpty()) {
            playSequence(paths)
        } else {
            playLegacyFallback(card)
        }
    }

    // Kept for backward compatibility
    fun playCard(card: Flashcard, restartRepetitions: Boolean = true) {
        playListening(card, restartRepetitions)
    }

    private fun getSegmentPath(card: Flashcard, role: String): String? {
        val cid = card.cardId
        val segments = manifestMap[cid] ?: manifestMap["legacy.${card.id}.${card.word.lowercase()}"]
        return segments?.get(role)
    }

    private fun playSequence(paths: List<String>, index: Int = 0) {
        val currentToken = sessionToken
        if (index >= paths.size) {
            handleSequenceFinished()
            return
        }

        val path = paths[index]
        playFile(path) {
            if (sessionToken != currentToken) return@playFile
            handler.postDelayed({
                if (sessionToken == currentToken) {
                    playSequence(paths, index + 1)
                }
            }, 400)
        }
    }

    private fun handleSequenceFinished() {
        val currentToken = sessionToken
        if (currentRepetition < maxRepetitions) {
            currentRepetition++
            onRepetitionUpdate(currentRepetition, maxRepetitions)
            handler.postDelayed({
                if (sessionToken == currentToken && currentCard != null) {
                    playListening(currentCard!!, restartRepetitions = false)
                }
            }, 800)
        } else {
            currentRepetition = 0
            isPlaying = false
            onPlaybackStateChanged(isAutoPlayEnabled)
            if (isAutoPlayEnabled) {
                handler.postDelayed({
                    if (sessionToken == currentToken) {
                        onCardFinished()
                    }
                }, 1000)
            }
        }
    }

    private fun playSingleFile(assetPath: String) {
        playFile(assetPath) {
            isPlaying = false
            onPlaybackStateChanged(isAutoPlayEnabled)
        }
    }

    private fun playLegacyFallback(card: Flashcard) {
        playFile("audio/word_${String.format("%04d", card.id)}.mp3") {
            handleSequenceFinished()
        }
    }

    private fun playFile(assetPath: String, onComplete: () -> Unit) {
        val currentToken = sessionToken
        try {
            val afd: AssetFileDescriptor = context.assets.openFd(assetPath)
            mediaPlayer?.release()
            mediaPlayer = MediaPlayer().apply {
                setDataSource(afd.fileDescriptor, afd.startOffset, afd.length)
                afd.close()
                prepare()
                setOnCompletionListener {
                    if (sessionToken == currentToken) {
                        onComplete()
                    }
                }
                setOnErrorListener { _, what, extra ->
                    Log.w(TAG, "MediaPlayer error: what=$what, extra=$extra for $assetPath")
                    if (sessionToken == currentToken) {
                        this@AudioController.isPlaying = false
                        onPlaybackStateChanged(isAutoPlayEnabled)
                    }
                    true
                }
                start()
            }
            isPlaying = true
            onPlaybackStateChanged(true)
        } catch (e: Exception) {
            Log.w(TAG, "Failed to play asset '$assetPath': ${e.message}")
            if (sessionToken == currentToken) {
                isPlaying = false
                onPlaybackStateChanged(isAutoPlayEnabled)
            }
        }
    }

    fun pause() {
        mediaPlayer?.let {
            if (it.isPlaying) {
                it.pause()
            }
        }
        isPlaying = false
        onPlaybackStateChanged(false)
    }

    fun resume() {
        mediaPlayer?.let {
            it.start()
            isPlaying = true
            onPlaybackStateChanged(true)
        } ?: run {
            currentCard?.let { playListening(it, restartRepetitions = false) }
        }
    }

    fun stop() {
        sessionToken++
        handler.removeCallbacksAndMessages(null)
        try {
            mediaPlayer?.stop()
            mediaPlayer?.release()
        } catch (e: Exception) {
            // Ignore
        }
        mediaPlayer = null
        isPlaying = false
        onPlaybackStateChanged(isAutoPlayEnabled)
    }

    fun togglePlayPause() {
        if (isPlaying) {
            pause()
        } else {
            resume()
        }
    }

    fun replayCurrent() {
        currentCard?.let {
            playListening(it, restartRepetitions = true)
        }
    }

    fun destroy() {
        release()
    }

    fun release() {
        stop()
    }
}
