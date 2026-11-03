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
            val assetName = if (hasAsset("cards_v3.json")) "cards_v3.json" else "cards.json"
            val inputStream = context.assets.open(assetName)
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

                if (obj.has("schema_version") && obj.getInt("schema_version") == 3) {
                    val cid = obj.getString("card_id")
                    val legacyIds = obj.optJSONArray("legacy_ids")
                    val numericId = if (legacyIds != null && legacyIds.length() > 0) legacyIds.getInt(0) else (i + 1)
                    val term = obj.getString("display_term")
                    val meaningShort = obj.getString("meaning_ru_short")
                    val explanation = obj.optString("explanation_ru", "")

                    val pron = obj.optJSONObject("pronunciation")
                    val ipaStr = pron?.optString("ipa", "") ?: ""
                    val ruHint = pron?.optString("ru_hint", "") ?: ""

                    val examplesArr = obj.optJSONArray("examples")
                    val primaryEn = if (examplesArr != null && examplesArr.length() > 0) {
                        examplesArr.getJSONObject(0).optString("en", "")
                    } else ""
                    val primaryRu = if (examplesArr != null && examplesArr.length() > 0) {
                        examplesArr.getJSONObject(0).optString("ru", "")
                    } else ""

                    val secEn = if (examplesArr != null && examplesArr.length() > 1) {
                        val ex1 = examplesArr.getJSONObject(1)
                        if (ex1.has("en") && !ex1.isNull("en")) ex1.getString("en") else null
                    } else null

                    val secRu = if (examplesArr != null && examplesArr.length() > 1) {
                        val ex1 = examplesArr.getJSONObject(1)
                        if (ex1.has("ru") && !ex1.isNull("ru")) ex1.getString("ru") else null
                    } else null

                    val breakdownObj = obj.optJSONObject("name_breakdown")
                    val breakdownStr = if (breakdownObj != null && breakdownObj.has("explanation_ru") && !breakdownObj.isNull("explanation_ru")) {
                        breakdownObj.getString("explanation_ru")
                    } else null

                    val techObj = obj.optJSONObject("technical")
                    val techCode = if (techObj != null && techObj.has("code") && !techObj.isNull("code")) {
                        techObj.getString("code")
                    } else null

                    val techOut = if (techObj != null && techObj.has("expected_output") && !techObj.isNull("expected_output")) {
                        techObj.getString("expected_output")
                    } else null

                    val tagsArr = obj.optJSONArray("tags")
                    val tagList = mutableListOf<String>()
                    if (tagsArr != null) {
                        for (t in 0 until tagsArr.length()) {
                            tagList.add(tagsArr.getString(t))
                        }
                    }

                    val cat = if (tagList.isNotEmpty()) tagList[0].replaceFirstChar { it.uppercase() } else "Общее"

                    val card = Flashcard(
                        id = numericId,
                        word = term,
                        translation = meaningShort,
                        cleanTranslation = meaningShort,
                        ipa = ipaStr,
                        transcriptionRu = ruHint,
                        category = cat,
                        audio = "word_${String.format("%04d", numericId)}.mp3",
                        example = primaryEn,
                        primaryExampleRu = primaryRu,
                        exampleNote = explanation,
                        cardId = cid,
                        nameBreakdown = breakdownStr,
                        technicalCode = techCode,
                        expectedOutput = techOut,
                        secondaryExampleEn = secEn,
                        secondaryExampleRu = secRu,
                        tags = tagList
                    )
                    allCards.add(card)
                    categorySet.add(cat)
                } else {
                    // Legacy structure
                    val id = obj.getInt("id")
                    val word = obj.getString("word")
                    val translation = obj.getString("translation")
                    val cleanTr = obj.optString("clean_translation", translation)
                    val ipa = obj.optString("ipa", obj.optString("transcription_en", ""))
                    val transRu = obj.optString("transcription_ru", "")
                    val cat = obj.getString("category")
                    val audio = obj.optString("audio", "word_${String.format("%04d", id)}.mp3")
                    val ex = obj.optString("example", "")
                    val note = obj.optString("example_note", "")

                    val card = Flashcard(
                        id = id,
                        word = word,
                        translation = translation,
                        cleanTranslation = cleanTr,
                        ipa = ipa,
                        transcriptionRu = transRu,
                        category = cat,
                        audio = audio,
                        example = ex,
                        exampleNote = note,
                        cardId = obj.optString("card_id", "legacy.$id.${word.lowercase()}")
                    )
                    allCards.add(card)
                    categorySet.add(cat)
                }
            }

            categories.add("Все карточки (${allCards.size})")
            categories.addAll(categorySet.sorted())
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun hasAsset(name: String): Boolean {
        return try {
            val list = context.assets.list("") ?: return false
            list.contains(name)
        } catch (e: Exception) {
            false
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

    fun getCardById(cardId: String): Flashcard? {
        return allCards.firstOrNull { it.cardId == cardId }
    }
}
