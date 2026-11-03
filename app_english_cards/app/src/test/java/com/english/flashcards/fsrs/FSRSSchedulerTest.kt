package com.english.flashcards.fsrs

import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import java.util.concurrent.TimeUnit

class FSRSSchedulerTest {

    private lateinit var scheduler: FSRSScheduler

    @Before
    fun setUp() {
        scheduler = FSRSScheduler()
    }

    @Test
    fun testNewCardTransitions() {
        val now = 1700000000000L
        val card = FSRSCard(
            practiceId = "test.card.en_to_ru",
            cardId = "test.card",
            skill = "en_to_ru",
            due = now
        )

        // 1. Again on New
        val cardAgain = scheduler.review(card, Rating.AGAIN, now)
        assertEquals(State.LEARNING, cardAgain.state)
        assertEquals(1, cardAgain.reps)
        assertEquals(1, cardAgain.lapses)
        assertTrue(cardAgain.due > now)
        assertTrue(cardAgain.due <= now + TimeUnit.MINUTES.toMillis(2))

        // 2. Good on New
        val cardGood = scheduler.review(card, Rating.GOOD, now)
        assertEquals(State.LEARNING, cardGood.state)
        assertEquals(1, cardGood.reps)
        assertEquals(0, cardGood.lapses)
        assertTrue(cardGood.due >= now + TimeUnit.MINUTES.toMillis(9))

        // 3. Easy on New
        val cardEasy = scheduler.review(card, Rating.EASY, now)
        assertEquals(State.REVIEW, cardEasy.state)
        assertEquals(1, cardEasy.reps)
        assertTrue(cardEasy.scheduledDays >= 2)
        assertTrue(cardEasy.due >= now + TimeUnit.DAYS.toMillis(2))
    }

    @Test
    fun testGraduationToReviewAndIntervalGrowth() {
        val now = 1700000000000L
        val card = FSRSCard(
            practiceId = "test.card.en_to_ru",
            cardId = "test.card",
            skill = "en_to_ru",
            due = now
        )

        // New -> Good (Learning)
        val step1 = scheduler.review(card, Rating.GOOD, now)
        assertEquals(State.LEARNING, step1.state)

        // Learning -> Good (Graduates to Review)
        val step2Time = step1.due
        val step2 = scheduler.review(step1, Rating.GOOD, step2Time)
        assertEquals(State.REVIEW, step2.state)
        assertTrue(step2.scheduledDays >= 1)

        // Review -> Good (Interval expands)
        val step3Time = step2.due
        val step3 = scheduler.review(step2, Rating.GOOD, step3Time)
        assertEquals(State.REVIEW, step3.state)
        assertTrue(step3.scheduledDays > step2.scheduledDays)
    }

    @Test
    fun testLapseTransitionToRelearning() {
        val now = 1700000000000L
        val card = FSRSCard(
            practiceId = "test.card.en_to_ru",
            cardId = "test.card",
            skill = "en_to_ru",
            due = now,
            state = State.REVIEW,
            scheduledDays = 10,
            stability = 15.0,
            difficulty = 5.0,
            reps = 5,
            lapses = 0,
            lastReview = now - TimeUnit.DAYS.toMillis(10)
        )

        val lapsed = scheduler.review(card, Rating.AGAIN, now)
        assertEquals(State.RELEARNING, lapsed.state)
        assertEquals(1, lapsed.lapses)
        assertEquals(6, lapsed.reps)
        assertEquals(now + TimeUnit.MINUTES.toMillis(1), lapsed.due)
    }

    @Test
    fun testPreviewIntervals() {
        val now = 1700000000000L
        val card = FSRSCard(
            practiceId = "test.card.en_to_ru",
            cardId = "test.card",
            skill = "en_to_ru",
            due = now
        )

        val previews = scheduler.preview(card, now)
        assertEquals(4, previews.size)
        assertTrue(previews.containsKey(Rating.AGAIN))
        assertTrue(previews.containsKey(Rating.HARD))
        assertTrue(previews.containsKey(Rating.GOOD))
        assertTrue(previews.containsKey(Rating.EASY))

        assertEquals("< 1м", previews[Rating.AGAIN]?.intervalText)
        assertEquals("5м", previews[Rating.HARD]?.intervalText)
        assertEquals("10м", previews[Rating.GOOD]?.intervalText)
        assertTrue(previews[Rating.EASY]?.intervalText?.endsWith("д") == true)
    }

    @Test
    fun testHardRatingRetentionResponsivenessAndMaxInterval() {
        val now = 1700000000000L
        val card = FSRSCard(
            practiceId = "test.review.hard",
            cardId = "test.review",
            skill = "en_to_ru",
            due = now,
            state = State.REVIEW,
            scheduledDays = 10,
            stability = 15.0,
            difficulty = 5.0,
            reps = 3,
            lastReview = now - TimeUnit.DAYS.toMillis(10)
        )

        // 1. With retention 0.80: interval is large (~67 days)
        val scheduler80 = FSRSScheduler(FSRSParameters(requestRetention = 0.80))
        val hard80 = scheduler80.review(card, Rating.HARD, now)
        assertEquals(State.REVIEW, hard80.state)
        assertTrue("Hard at 0.80 retention should have larger interval than 10, got ${hard80.scheduledDays}", hard80.scheduledDays > 25)

        // 2. With retention 0.97: interval is small (~7 days)
        val scheduler97 = FSRSScheduler(FSRSParameters(requestRetention = 0.97))
        val hard97 = scheduler97.review(card, Rating.HARD, now)
        assertEquals(State.REVIEW, hard97.state)
        assertTrue("Hard at 0.97 retention should be shorter (~7d), got ${hard97.scheduledDays}", hard97.scheduledDays in 6..9)

        // 3. With maximumInterval = 10: MUST NEVER exceed 10 days!
        val schedulerMax10 = FSRSScheduler(FSRSParameters(requestRetention = 0.80, maximumInterval = 10))
        val hardMax10 = schedulerMax10.review(card, Rating.HARD, now)
        assertEquals(State.REVIEW, hardMax10.state)
        assertEquals("Hard must strictly observe maximumInterval=10", 10L, hardMax10.scheduledDays)
        assertEquals(now + TimeUnit.DAYS.toMillis(10), hardMax10.due)
    }
}
