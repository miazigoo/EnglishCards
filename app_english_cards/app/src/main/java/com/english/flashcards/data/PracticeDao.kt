package com.english.flashcards.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update

@Dao
interface PracticeDao {

    @Query("SELECT * FROM practice_states WHERE due <= :dueBefore ORDER BY due ASC")
    suspend fun getDuePractices(dueBefore: Long): List<PracticeStateEntity>

    @Query("SELECT * FROM practice_states WHERE state = 0 ORDER BY practiceId ASC LIMIT :limit")
    suspend fun getNewPractices(limit: Int): List<PracticeStateEntity>

    @Query("SELECT * FROM practice_states WHERE practiceId = :practiceId LIMIT 1")
    suspend fun getByPracticeId(practiceId: String): PracticeStateEntity?

    @Query("SELECT * FROM practice_states WHERE cardId = :cardId")
    suspend fun getByCardId(cardId: String): List<PracticeStateEntity>

    @Query("SELECT COUNT(*) FROM practice_states WHERE due <= :dueBefore AND state != 0")
    suspend fun countDuePractices(dueBefore: Long): Int

    @Query("SELECT COUNT(*) FROM practice_states WHERE state = 0")
    suspend fun countNewPractices(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(practice: PracticeStateEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertAll(practices: List<PracticeStateEntity>)

    @Query("SELECT * FROM practice_states")
    suspend fun getAll(): List<PracticeStateEntity>
}
