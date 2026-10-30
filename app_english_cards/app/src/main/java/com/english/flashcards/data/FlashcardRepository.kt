package com.english.flashcards.data

import android.content.Context
import com.english.flashcards.model.Flashcard
import org.json.JSONArray
import java.io.BufferedReader
import java.io.InputStreamReader

class FlashcardRepository(private val context: Context) {

    private val allCards: MutableList<Flashcard> = mutableListOf()
    private val categories: MutableList<String> = mutableListOf()

    init {
        loadCards()
    }

    private fun loadCards() {
        try {
            val inputStream = context.assets.open("cards.json")
            val reader = BufferedReader(InputStreamReader(inputStream, "UTF-8"))
            val sb = StringBuilder()
            var line: String? = reader.readLine()
            while (line != null) {
                sb.append(line)
                line = reader.readLine()
            }
            reader.close()

            val jsonArray = JSONArray(sb.toString())
            val categorySet = mutableSetOf<String>()

            for (i in 0 until jsonArray.length()) {
                val obj = jsonArray.getJSONObject(i)
                val card = Flashcard(
                    id = obj.getInt("id"),
                    word = obj.getString("word"),
                    translation = obj.getString("translation"),
                    cleanTranslation = obj.optString("clean_translation", obj.getString("translation")),
                    ipa = obj.getString("ipa"),
                    transcriptionRu = obj.getString("transcription_ru"),
                    category = obj.getString("category"),
                    audio = obj.getString("audio"),
                    example = obj.optString("example", ""),
                    exampleNote = obj.optString("example_note", "")
                )
                allCards.add(card)
                categorySet.add(card.category)
            }

            categories.add("Все карточки (${allCards.size})")
            categories.addAll(categorySet.sorted())
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    fun getAllCards(): List<Flashcard> = allCards

    fun getCategories(): List<String> = categories

    fun getCardsByCategory(category: String): List<Flashcard> {
        return if (category.startsWith("Все")) {
            allCards
        } else {
            allCards.filter { it.category == category }
        }
    }
}
