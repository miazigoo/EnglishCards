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
    private var maxRepetitions = 2
    private var currentRepetition = 0
    private var isPlaying = false

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
        maxRepetitions = count
    }

    fun getMaxRepetitions(): Int = maxRepetitions

    /**
     * Plays only the English term (single segment).
     */
    fun playTerm(card: Flashcard) {
        stop()
        val path = getSegmentPath(card, "term_en")
        if (path != null) {
            playSingleFile(path)
        } else {
            playAudioFile(card.audio)
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
            playAudioFile(card.audio)
        }
    }

    /**
     * Plays the full pedagogical sequence for the card with repetitions.
     */
    fun playCard(card: Flashcard, restartRepetitions: Boolean = true) {
        stop()
        currentCard = card
        if (restartRepetitions) {
            currentRepetition = 1
        }
        onRepetitionUpdate(currentRepetition, maxRepetitions)

        val termPath = getSegmentPath(card, "term_en")
        val meaningPath = getSegmentPath(card, "meaning_ru")

        if (termPath != null && meaningPath != null) {
            playSequence(listOf(termPath, meaningPath))
        } else {
            playAudioFile(card.audio)
        }
    }

    private fun getSegmentPath(card: Flashcard, role: String): String? {
        val cid = card.cardId
        val segments = manifestMap[cid] ?: manifestMap["legacy.${card.id}.${card.word.lowercase()}"]
        return segments?.get(role)
    }

    private fun playSequence(paths: List<String>, index: Int = 0) {
        if (index >= paths.size) {
            handleSequenceFinished()
            return
        }

        val path = paths[index]
        playFile(path) {
            handler.postDelayed({
                playSequence(paths, index + 1)
            }, 500)
        }
    }

    private fun handleSequenceFinished() {
        if (currentRepetition < maxRepetitions) {
            currentRepetition++
            onRepetitionUpdate(currentRepetition, maxRepetitions)
            handler.postDelayed({
                currentCard?.let { playCard(it, restartRepetitions = false) }
            }, 800)
            return
        }

        onRepetitionUpdate(maxRepetitions, maxRepetitions)
        isPlaying = false
        if (isAutoPlayEnabled) {
            handler.postDelayed({
                onCardFinished()
            }, 1200)
        } else {
            onPlaybackStateChanged(false)
        }
    }

    private fun playSingleFile(assetPath: String) {
        playFile(assetPath) {
            isPlaying = false
            onPlaybackStateChanged(false)
        }
    }

    private fun playAudioFile(audioFileName: String) {
        val path = if (audioFileName.startsWith("audio/")) audioFileName else "audio/$audioFileName"
        playFile(path) {
            handleSequenceFinished()
        }
    }

    private fun playFile(assetPath: String, onCompletion: () -> Unit) {
        try {
            val afd = context.assets.openFd(assetPath)
            releasePlayer()
            mediaPlayer = MediaPlayer().apply {
                setDataSource(afd.fileDescriptor, afd.startOffset, afd.length)
                afd.close()
                prepare()
                setOnCompletionListener {
                    onCompletion()
                }
                setOnErrorListener { _, _, _ ->
                    stop()
                    true
                }
                start()
            }
            isPlaying = true
            onPlaybackStateChanged(true)
        } catch (e: Exception) {
            Log.w(TAG, "Failed to play asset $assetPath: ${e.message}")
            onCompletion()
        }
    }

    fun replayCurrent() {
        currentCard?.let { playCard(it, restartRepetitions = true) }
    }

    fun togglePlayPause() {
        if (isPlaying || isAutoPlayEnabled) {
            pause()
        } else {
            resume()
        }
    }

    fun pause() {
        handler.removeCallbacksAndMessages(null)
        mediaPlayer?.let {
            if (it.isPlaying) {
                it.pause()
            }
        }
        isPlaying = false
        isAutoPlayEnabled = false
        onPlaybackStateChanged(false)
    }

    fun resume() {
        isAutoPlayEnabled = true
        mediaPlayer?.let {
            it.start()
            isPlaying = true
            onPlaybackStateChanged(true)
            return
        }
        currentCard?.let { playCard(it, restartRepetitions = false) }
    }

    fun stop() {
        handler.removeCallbacksAndMessages(null)
        releasePlayer()
        isPlaying = false
        onPlaybackStateChanged(false)
    }

    private fun releasePlayer() {
        mediaPlayer?.let {
            try {
                if (it.isPlaying) it.stop()
                it.release()
            } catch (ignored: Exception) {}
        }
        mediaPlayer = null
    }

    fun destroy() {
        stop()
    }
}
