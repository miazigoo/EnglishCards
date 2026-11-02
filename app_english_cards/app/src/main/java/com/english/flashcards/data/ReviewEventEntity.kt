package com.english.flashcards.data

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "review_events",
    indices = [
        Index(value = ["practiceId"]),
        Index(value = ["reviewTime"])
    ]
)
data class ReviewEventEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val practiceId: String,
    val cardId: String,
    val skill: String,
    val rating: Int, // 1=Again, 2=Hard, 3=Good, 4=Easy
    val reviewTime: Long,
    val durationMs: Long,
    val stateBefore: Int,
    val stateAfter: Int,
    val stabilityAfter: Double,
    val difficultyAfter: Double,
    val scheduledDaysAfter: Long
)
