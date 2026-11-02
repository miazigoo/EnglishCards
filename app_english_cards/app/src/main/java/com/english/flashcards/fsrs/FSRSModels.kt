package com.english.flashcards.fsrs

import java.util.Date

enum class State(val value: Int) {
    NEW(0),
    LEARNING(1),
    REVIEW(2),
    RELEARNING(3);

    companion object {
        fun fromInt(value: Int): State = entries.firstOrNull { it.value == value } ?: NEW
    }
}

enum class Rating(val value: Int) {
    AGAIN(1),
    HARD(2),
    GOOD(3),
    EASY(4);

    companion object {
        fun fromInt(value: Int): Rating = entries.firstOrNull { it.value == value } ?: AGAIN
    }
}

data class FSRSCard(
    val practiceId: String,
    val cardId: String,
    val skill: String, // en_to_ru, ru_to_en, listening, cloze, spelling
    val due: Long = System.currentTimeMillis(),
    val stability: Double = 0.0,
    val difficulty: Double = 0.0,
    val elapsedDays: Long = 0,
    val scheduledDays: Long = 0,
    val reps: Int = 0,
    val lapses: Int = 0,
    val state: State = State.NEW,
    val lastReview: Long = 0
)

data class SchedulingInfo(
    val card: FSRSCard,
    val rating: Rating,
    val intervalText: String
)

data class FSRSParameters(
    val requestRetention: Double = 0.90,
    val maximumInterval: Int = 36500,
    val w: DoubleArray = doubleArrayOf(
        0.40255, 1.18385, 3.173, 15.69105,
        7.1949, 0.5345, 1.4604, 0.0046,
        1.54575, 0.1192, 1.01925, 1.9395,
        0.11, 0.29605, 0.22695, 0.5698,
        2.85535, 0.4789, 0.2801
    )
) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (javaClass != other?.javaClass) return false
        other as FSRSParameters
        return requestRetention == other.requestRetention &&
                maximumInterval == other.maximumInterval &&
                w.contentEquals(other.w)
    }

    override fun hashCode(): Int {
        var result = requestRetention.hashCode()
        result = 31 * result + maximumInterval
        result = 31 * result + w.contentHashCode()
        return result
    }
}
