package com.english.flashcards.model

data class Flashcard(
    val id: Int,
    val word: String,
    val translation: String,
    val cleanTranslation: String,
    val ipa: String,
    val transcriptionRu: String,
    val category: String,
    val audio: String,
    val example: String = "",
    val exampleNote: String = ""
)

enum class CardStatus {
    NEW,
    HARD,
    LEARNED
}
