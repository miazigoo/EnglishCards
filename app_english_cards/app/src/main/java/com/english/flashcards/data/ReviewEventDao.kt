package com.english.flashcards.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface ReviewEventDao {

    @Insert(onConflict = OnConflictStrategy.ABORT)
    suspend fun insert(event: ReviewEventEntity): Long

    @Query("SELECT * FROM review_events WHERE attemptId = :attemptId LIMIT 1")
    suspend fun getByAttemptId(attemptId: String): ReviewEventEntity?

    @Query("UPDATE review_events SET isUndone = 1 WHERE attemptId = :attemptId")
    suspend fun markUndone(attemptId: String)

    @Query("SELECT * FROM review_events WHERE isUndone = 0 ORDER BY reviewTime DESC LIMIT 1")
    suspend fun getLastReviewEvent(): ReviewEventEntity?

    @Query("SELECT * FROM review_events WHERE practiceId = :practiceId ORDER BY reviewTime ASC")
    suspend fun getEventsForPractice(practiceId: String): List<ReviewEventEntity>

    @Query("SELECT COUNT(*) FROM review_events WHERE isUndone = 0")
    suspend fun countTotalReviews(): Int

    @Query("SELECT COUNT(*) FROM review_events WHERE isUndone = 0 AND rating >= 3")
    suspend fun countSuccessfulReviews(): Int

    @Query("SELECT * FROM review_events WHERE isUndone = 0 ORDER BY reviewTime DESC LIMIT :limit")
    suspend fun getRecentEvents(limit: Int): List<ReviewEventEntity>
}
