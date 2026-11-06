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
    val primaryExampleRu: String = "",
    val exampleNote: String = "",
    val cardId: String = "",
    val nameBreakdown: String? = null,
    val technicalCode: String? = null,
    val expectedOutput: String? = null,
    val secondaryExampleEn: String? = null,
    val secondaryExampleRu: String? = null,
    val tags: List<String> = emptyList(),
    val studyCollections: List<String> = emptyList(),
    val acceptedAnswers: List<String> = emptyList(),
    val clozeTarget: String? = null
)

typealias Card = Flashcard

enum class CardStatus {
    NEW,
    HARD,
    LEARNED
}
