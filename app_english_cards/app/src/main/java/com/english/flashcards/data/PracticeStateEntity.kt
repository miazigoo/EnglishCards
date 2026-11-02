package com.english.flashcards.data

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "practice_states",
    indices = [
        Index(value = ["due"]),
        Index(value = ["cardId"]),
        Index(value = ["skill"])
    ]
)
data class PracticeStateEntity(
    @PrimaryKey
    val practiceId: String,
    val cardId: String,
    val skill: String, // en_to_ru, ru_to_en, listening, cloze, spelling
    val state: Int, // 0=new, 1=learning, 2=review, 3=relearning
    val stability: Double,
    val difficulty: Double,
    val elapsedDays: Long,
    val scheduledDays: Long,
    val reps: Int,
    val lapses: Int,
    val due: Long,
    val lastReview: Long
)
