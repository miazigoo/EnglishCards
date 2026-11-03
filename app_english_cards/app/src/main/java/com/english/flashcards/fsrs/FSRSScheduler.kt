package com.english.flashcards.fsrs

import java.util.concurrent.TimeUnit
import kotlin.math.exp
import kotlin.math.ln
import kotlin.math.max
import kotlin.math.min
import kotlin.math.pow
import kotlin.math.roundToInt
import kotlin.math.roundToLong

class FSRSScheduler(
    val params: FSRSParameters = FSRSParameters()
) {
    private val decay: Double = -0.5
    private val factor: Double = (19.0 / 81.0)

    fun preview(card: FSRSCard, now: Long = System.currentTimeMillis()): Map<Rating, SchedulingInfo> {
        return Rating.entries.associateWith { rating ->
            val nextCard = review(card, rating, now)
            val diffMs = nextCard.due - now
            val text = formatInterval(diffMs)
            SchedulingInfo(nextCard, rating, text)
        }
    }

    fun review(card: FSRSCard, rating: Rating, now: Long = System.currentTimeMillis()): FSRSCard {
        val elapsedDays = if (card.lastReview > 0) {
            max(0L, TimeUnit.MILLISECONDS.toDays(now - card.lastReview))
        } else {
            0L
        }

        return when (card.state) {
            State.NEW -> stepNew(card, rating, now)
            State.LEARNING, State.RELEARNING -> stepLearning(card, rating, now, elapsedDays)
            State.REVIEW -> stepReview(card, rating, now, elapsedDays)
        }
    }

    private fun stepNew(card: FSRSCard, rating: Rating, now: Long): FSRSCard {
        val s = initStability(rating)
        val d = initDifficulty(rating)
        val newReps = card.reps + 1

        return when (rating) {
            Rating.AGAIN -> card.copy(
                due = now + TimeUnit.MINUTES.toMillis(1),
                stability = s,
                difficulty = d,
                elapsedDays = 0,
                scheduledDays = 0,
                reps = newReps,
                lapses = card.lapses + 1,
                state = State.LEARNING,
                lastReview = now
            )
            Rating.HARD -> card.copy(
                due = now + TimeUnit.MINUTES.toMillis(5),
                stability = s,
                difficulty = d,
                elapsedDays = 0,
                scheduledDays = 0,
                reps = newReps,
                state = State.LEARNING,
                lastReview = now
            )
            Rating.GOOD -> card.copy(
                due = now + TimeUnit.MINUTES.toMillis(10),
                stability = s,
                difficulty = d,
                elapsedDays = 0,
                scheduledDays = 0,
                reps = newReps,
                state = State.LEARNING,
                lastReview = now
            )
            Rating.EASY -> {
                val intervalDays = nextInterval(s).roundToLong()
                val days = clamp(max(2L, intervalDays), 1L, params.maximumInterval.toLong())
                card.copy(
                    due = now + TimeUnit.DAYS.toMillis(days),
                    stability = s,
                    difficulty = d,
                    elapsedDays = 0,
                    scheduledDays = days,
                    reps = newReps,
                    state = State.REVIEW,
                    lastReview = now
                )
            }
        }
    }

    private fun stepLearning(card: FSRSCard, rating: Rating, now: Long, elapsedDays: Long): FSRSCard {
        val newReps = card.reps + 1
        return when (rating) {
            Rating.AGAIN -> card.copy(
                due = now + TimeUnit.MINUTES.toMillis(1),
                reps = newReps,
                lapses = card.lapses + 1,
                state = State.RELEARNING,
                lastReview = now
            )
            Rating.HARD -> card.copy(
                due = now + TimeUnit.MINUTES.toMillis(5),
                reps = newReps,
                lastReview = now
            )
            Rating.GOOD -> {
                val intervalDays = clamp(max(1L, nextInterval(card.stability).roundToLong()), 1L, params.maximumInterval.toLong())
                card.copy(
                    due = now + TimeUnit.DAYS.toMillis(intervalDays),
                    scheduledDays = intervalDays,
                    reps = newReps,
                    state = State.REVIEW,
                    lastReview = now
                )
            }
            Rating.EASY -> {
                val intervalDays = clamp(max(2L, (nextInterval(card.stability) * 1.3).roundToLong()), 1L, params.maximumInterval.toLong())
                card.copy(
                    due = now + TimeUnit.DAYS.toMillis(intervalDays),
                    scheduledDays = intervalDays,
                    reps = newReps,
                    state = State.REVIEW,
                    lastReview = now
                )
            }
        }
    }

    private fun stepReview(card: FSRSCard, rating: Rating, now: Long, elapsedDays: Long): FSRSCard {
        val newReps = card.reps + 1
        val r = retrievability(elapsedDays, card.stability)
        val d = nextDifficulty(card.difficulty, rating)

        return when (rating) {
            Rating.AGAIN -> {
                val s = nextForgetStability(card.difficulty, card.stability, r)
                card.copy(
                    due = now + TimeUnit.MINUTES.toMillis(1),
                    stability = s,
                    difficulty = d,
                    elapsedDays = elapsedDays,
                    scheduledDays = 0,
                    reps = newReps,
                    lapses = card.lapses + 1,
                    state = State.RELEARNING,
                    lastReview = now
                )
            }
            Rating.HARD -> {
                val s = nextRecallStability(card.difficulty, card.stability, r, rating)
                val rawDays = nextInterval(s).roundToLong()
                val days = clamp(rawDays, 1L, params.maximumInterval.toLong())
                card.copy(
                    due = now + TimeUnit.DAYS.toMillis(days),
                    stability = s,
                    difficulty = d,
                    elapsedDays = elapsedDays,
                    scheduledDays = days,
                    reps = newReps,
                    state = State.REVIEW,
                    lastReview = now
                )
            }
            Rating.GOOD -> {
                val s = nextRecallStability(card.difficulty, card.stability, r, rating)
                val rawDays = nextInterval(s).roundToLong()
                val days = clamp(max(card.scheduledDays + 1, rawDays), 1L, params.maximumInterval.toLong())
                card.copy(
                    due = now + TimeUnit.DAYS.toMillis(days),
                    stability = s,
                    difficulty = d,
                    elapsedDays = elapsedDays,
                    scheduledDays = days,
                    reps = newReps,
                    state = State.REVIEW,
                    lastReview = now
                )
            }
            Rating.EASY -> {
                val s = nextRecallStability(card.difficulty, card.stability, r, rating)
                val rawDays = (nextInterval(s) * 1.3).roundToLong()
                val days = clamp(max(card.scheduledDays + 2, rawDays), 1L, params.maximumInterval.toLong())
                card.copy(
                    due = now + TimeUnit.DAYS.toMillis(days),
                    stability = s,
                    difficulty = d,
                    elapsedDays = elapsedDays,
                    scheduledDays = days,
                    reps = newReps,
                    state = State.REVIEW,
                    lastReview = now
                )
            }
        }
    }

    private fun initStability(rating: Rating): Double {
        return max(0.1, params.w[rating.value - 1])
    }

    private fun initDifficulty(rating: Rating): Double {
        val d = params.w[4] - exp(params.w[5] * (rating.value - 1)) + 1.0
        return clamp(d, 1.0, 10.0)
    }

    private fun nextDifficulty(d: Double, rating: Rating): Double {
        val nextD = params.w[7] * initDifficulty(Rating.GOOD) + (1.0 - params.w[7]) * (d - params.w[6] * (rating.value - 3))
        return clamp(nextD, 1.0, 10.0)
    }

    fun retrievability(elapsedDays: Long, stability: Double): Double {
        if (stability <= 0.0) return 0.0
        return (1.0 + factor * (elapsedDays.toDouble() / stability)).pow(decay)
    }

    fun nextRecallStability(d: Double, s: Double, r: Double, rating: Rating): Double {
        val hardPenalty = if (rating == Rating.HARD) params.w[15] else 1.0
        val easyBonus = if (rating == Rating.EASY) params.w[16] else 1.0
        val nextS = s * (1.0 + exp(params.w[8]) *
                (11.0 - d) *
                s.pow(-params.w[9]) *
                (exp((1.0 - r) * params.w[10]) - 1.0) *
                hardPenalty *
                easyBonus)
        return max(0.1, nextS)
    }

    fun nextForgetStability(d: Double, s: Double, r: Double): Double {
        val nextS = params.w[11] *
                d.pow(-params.w[12]) *
                ((s + 1.0).pow(params.w[13]) - 1.0) *
                exp((1.0 - r) * params.w[14])
        return min(s, max(0.1, nextS))
    }

    fun nextInterval(stability: Double): Double {
        val interval = (stability / factor) * ((params.requestRetention.pow(1.0 / decay)) - 1.0)
        return clamp(interval, 1.0, params.maximumInterval.toDouble())
    }

    private fun clamp(v: Double, minVal: Double, maxVal: Double): Double {
        return min(maxVal, max(minVal, v))
    }

    private fun clamp(v: Long, minVal: Long, maxVal: Long): Long {
        return min(maxVal, max(minVal, v))
    }

    private fun formatInterval(ms: Long): String {
        if (ms <= TimeUnit.MINUTES.toMillis(1)) return "< 1м"
        if (ms < TimeUnit.HOURS.toMillis(1)) {
            val mins = TimeUnit.MILLISECONDS.toMinutes(ms)
            return "${mins}м"
        }
        if (ms < TimeUnit.DAYS.toMillis(1)) {
            val hrs = TimeUnit.MILLISECONDS.toHours(ms)
            return "${hrs}ч"
        }
        val days = TimeUnit.MILLISECONDS.toDays(ms)
        return if (days < 30) "${days}д" else "${days / 30}мес"
    }
}
