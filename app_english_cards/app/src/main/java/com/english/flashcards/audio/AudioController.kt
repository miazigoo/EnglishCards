package com.english.flashcards.audio

import android.content.Context
import android.media.MediaPlayer
import android.os.Handler
import android.os.Looper
import com.english.flashcards.model.Flashcard

class AudioController(
    private val context: Context,
    private val onPlaybackStateChanged: (isPlaying: Boolean) -> Unit,
    private val onRepetitionUpdate: (currentRep: Int, maxRep: Int) -> Unit,
    private val onCardFinished: () -> Unit
) {
    private var mediaPlayer: MediaPlayer? = null
    private val handler = Handler(Looper.getMainLooper())
    private var currentCard: Flashcard? = null
    private var isAutoPlayEnabled = true
    private var maxRepetitions = 2
    private var currentRepetition = 0
    private var isPlaying = false

    fun setAutoPlay(enabled: Boolean) {
        isAutoPlayEnabled = enabled
        onPlaybackStateChanged(isPlaying)
    }

    fun isAutoPlay(): Boolean = isAutoPlayEnabled

    fun setMaxRepetitions(count: Int) {
        maxRepetitions = count
    }

    fun getMaxRepetitions(): Int = maxRepetitions

    fun playCard(card: Flashcard, restartRepetitions: Boolean = true) {
        stop()
        currentCard = card
        if (restartRepetitions) {
            currentRepetition = 1
        }
        onRepetitionUpdate(currentRepetition, maxRepetitions)
        playAudioFile(card.audio)
    }

    private fun playAudioFile(audioFileName: String) {
        try {
            val afd = context.assets.openFd("audio/$audioFileName")
            mediaPlayer = MediaPlayer().apply {
                setDataSource(afd.fileDescriptor, afd.startOffset, afd.length)
                afd.close()
                prepare()
                setOnCompletionListener {
                    handleTrackCompletion()
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
            e.printStackTrace()
            // If asset loading error, proceed to next after delay if autoPlay is on
            if (isAutoPlayEnabled) {
                handler.postDelayed({ onCardFinished() }, 2000)
            }
        }
    }

    private fun handleTrackCompletion() {
        releasePlayer()
        isPlaying = false
        onPlaybackStateChanged(false)

        if (maxRepetitions > 2 && currentRepetition < maxRepetitions) {
            currentRepetition++
            onRepetitionUpdate(currentRepetition, maxRepetitions)
            handler.postDelayed({
                currentCard?.let { playAudioFile(it.audio) }
            }, 600)
            return
        }

        onRepetitionUpdate(maxRepetitions, maxRepetitions)
        if (isAutoPlayEnabled) {
            handler.postDelayed({
                onCardFinished()
            }, 1000)
        }
    }

    fun replayCurrent() {
        currentCard?.let {
            playCard(it, restartRepetitions = true)
        }
    }

    fun togglePlayPause() {
        if (isPlaying) {
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
