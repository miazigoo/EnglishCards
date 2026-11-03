package com.english.flashcards.data

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "review_events",
    indices = [
        Index(value = ["attemptId"], unique = true),
        Index(value = ["practiceId"]),
        Index(value = ["reviewTime"])
    ]
)
data class ReviewEventEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val attemptId: String, // Unique UUID per review attempt
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
    val scheduledDaysAfter: Long,
    val isAssisted: Boolean = false,
    val hintsUsed: Int = 0,
    val listensCount: Int = 0,
    val isUndone: Boolean = false,
    val contentRevision: Int = 1,
    val schedulerVersion: String = "FSRS-4.5"
)
