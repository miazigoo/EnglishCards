package com.english.flashcards.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query

@Dao
interface ReviewEventDao {

    @Insert
    suspend fun insert(event: ReviewEventEntity): Long

    @Query("SELECT * FROM review_events WHERE reviewTime >= :since ORDER BY reviewTime DESC")
    suspend fun getEventsSince(since: Long): List<ReviewEventEntity>

    @Query("SELECT COUNT(*) FROM review_events WHERE reviewTime >= :startOfDay")
    suspend fun countTodayReviews(startOfDay: Long): Int

    @Query("SELECT COUNT(*) FROM review_events WHERE reviewTime >= :startOfDay AND rating >= 3")
    suspend fun countTodaySuccesses(startOfDay: Long): Int

    @Query("SELECT SUM(durationMs) FROM review_events WHERE reviewTime >= :startOfDay")
    suspend fun sumTodayDurationMs(startOfDay: Long): Long?

    @Query("SELECT COUNT(*) FROM review_events")
    suspend fun countTotalReviews(): Int

    @Query("SELECT * FROM review_events ORDER BY reviewTime DESC LIMIT :limit")
    suspend fun getRecentEvents(limit: Int): List<ReviewEventEntity>

    @Query("SELECT * FROM review_events")
    suspend fun getAll(): List<ReviewEventEntity>
}
