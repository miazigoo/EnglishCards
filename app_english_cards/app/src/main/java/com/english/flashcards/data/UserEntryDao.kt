package com.english.flashcards.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface UserEntryDao {

    @Query("SELECT * FROM user_entry_states WHERE cardId = :cardId LIMIT 1")
    suspend fun getByCardId(cardId: String): UserEntryStateEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(entry: UserEntryStateEntity)

    @Query("SELECT * FROM user_entry_states WHERE isPinned = 1")
    suspend fun getPinnedCards(): List<UserEntryStateEntity>

    @Query("SELECT * FROM user_entry_states")
    suspend fun getAll(): List<UserEntryStateEntity>
}
