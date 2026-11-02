package com.english.flashcards.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "user_entry_states")
data class UserEntryStateEntity(
    @PrimaryKey
    val cardId: String,
    val isPinned: Boolean = false,
    val isSuspended: Boolean = false,
    val customNote: String? = null,
    val lastRevealedAt: Long? = null
)
