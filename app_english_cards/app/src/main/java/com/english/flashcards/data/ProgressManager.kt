package com.english.flashcards.data

import android.content.Context
import android.content.SharedPreferences
import com.english.flashcards.model.CardStatus
import com.english.flashcards.model.Flashcard

class ProgressManager(context: Context) {
    private val prefs: SharedPreferences =
        context.getSharedPreferences("english_flashcards_progress", Context.MODE_PRIVATE)

    fun getStatus(cardId: Int): CardStatus {
        val str = prefs.getString("card_status_$cardId", CardStatus.NEW.name)
        return try {
            CardStatus.valueOf(str ?: CardStatus.NEW.name)
        } catch (e: Exception) {
            CardStatus.NEW
        }
    }

    fun setStatus(cardId: Int, status: CardStatus) {
        prefs.edit().putString("card_status_$cardId", status.name).apply()
    }

    fun getCounts(cards: List<Flashcard>): Triple<Int, Int, Int> {
        var learned = 0
        var hard = 0
        var newCards = 0
        for (c in cards) {
            when (getStatus(c.id)) {
                CardStatus.LEARNED -> learned++
                CardStatus.HARD -> hard++
                CardStatus.NEW -> newCards++
            }
        }
        return Triple(learned, hard, newCards)
    }

    fun getHardCards(allCards: List<Flashcard>): List<Flashcard> {
        return allCards.filter { getStatus(it.id) == CardStatus.HARD }
    }

    fun getLearnedCards(allCards: List<Flashcard>): List<Flashcard> {
        return allCards.filter { getStatus(it.id) == CardStatus.LEARNED }
    }

    fun resetProgress() {
        prefs.edit().clear().apply()
    }
}
