package com.english.flashcards.data

import android.content.Context
import android.util.Log
import com.english.flashcards.fsrs.State
import com.english.flashcards.model.Card
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.InputStreamReader

object RoomMigrationHelper {

    private const val TAG = "RoomMigrationHelper"
    private const val PREFS_PROGRESS = "english_flashcards_progress"
    private const val PREFS_LEGACY_V3 = "EnglishCardsPrefs"
    private const val KEY_MIGRATION_COMPLETED = "room_migration_completed_v4"

    suspend fun checkAndMigrate(context: Context, cards: List<Card>) = withContext(Dispatchers.IO) {
        val prefsProgress = context.getSharedPreferences(PREFS_PROGRESS, Context.MODE_PRIVATE)
        val prefsV3 = context.getSharedPreferences(PREFS_LEGACY_V3, Context.MODE_PRIVATE)

        val db = AppDatabase.getInstance(context)
        val practiceDao = db.practiceDao()
        val userEntryDao = db.userEntryDao()

        val isMigratedV4 = prefsProgress.getBoolean(KEY_MIGRATION_COMPLETED, false)

        val totalExisting = practiceDao.countNewPractices() + practiceDao.countDuePractices(Long.MAX_VALUE)
        if (isMigratedV4 && totalExisting >= cards.size * 2) {
            Log.d(TAG, "Migration v4 already completed and all $totalExisting practices present.")
            return@withContext
        }

        Log.d(TAG, "Starting robust migration and seeding for ${cards.size} cards...")
        val now = System.currentTimeMillis()
        val practiceEntities = ArrayList<PracticeStateEntity>(cards.size * 2)
        val userEntries = ArrayList<UserEntryStateEntity>(cards.size)

        val legacyIdMap = loadLegacyIdMap(context)

        for (card in cards) {
            val cardId = card.cardId.ifEmpty { "legacy.${card.id}.${card.word.lowercase()}" }
            val legacyId = card.id

            // Check if practice already exists in DB (to prevent overwriting real user answers)
            val existingEn = practiceDao.getByPracticeId("$cardId.en_to_ru")
            val existingRu = practiceDao.getByPracticeId("$cardId.ru_to_en")

            // Read legacy status from english_flashcards_progress or fallback
            val rawStatus = prefsProgress.getString("card_status_$legacyId", null)
                ?: prefsV3.getString("card_status_$legacyId", null)
            val legacyStatus = rawStatus?.uppercase()?.trim()

            val isFavorite = prefsProgress.getBoolean("card_favorite_$legacyId", false)
                || prefsV3.getBoolean("card_favorite_$legacyId", false)

            if (isFavorite) {
                userEntries.add(UserEntryStateEntity(cardId = cardId, isPinned = true))
            }

            // EN -> RU skill
            if (existingEn == null) {
                val (stateEn, stabilityEn, diffEn) = when (legacyStatus) {
                    "HARD" -> Triple(State.LEARNING.value, 1.0, 8.0)
                    "LEARNED" -> Triple(State.LEARNING.value, 2.0, 5.0)
                    else -> Triple(State.NEW.value, 0.0, 5.0)
                }

                practiceEntities.add(
                    PracticeStateEntity(
                        practiceId = "$cardId.en_to_ru",
                        cardId = cardId,
                        skill = "en_to_ru",
                        state = stateEn,
                        stability = stabilityEn,
                        difficulty = diffEn,
                        elapsedDays = 0,
                        scheduledDays = 0,
                        reps = 0,
                        lapses = 0,
                        due = now,
                        lastReview = 0L
                    )
                )
            }

            // RU -> EN skill (production starts as NEW to ensure honest testing)
            if (existingRu == null) {
                practiceEntities.add(
                    PracticeStateEntity(
                        practiceId = "$cardId.ru_to_en",
                        cardId = cardId,
                        skill = "ru_to_en",
                        state = State.NEW.value,
                        stability = 0.0,
                        difficulty = 5.0,
                        elapsedDays = 0,
                        scheduledDays = 0,
                        reps = 0,
                        lapses = 0,
                        due = now,
                        lastReview = 0L
                    )
                )
            }
        }

        if (practiceEntities.isNotEmpty()) {
            practiceDao.upsertAll(practiceEntities)
            Log.d(TAG, "Seeded ${practiceEntities.size} missing practice states.")
        }

        if (userEntries.isNotEmpty()) {
            userEntryDao.upsertAll(userEntries)
            Log.d(TAG, "Seeded ${userEntries.size} user entry states.")
        }

        prefsProgress.edit().putBoolean(KEY_MIGRATION_COMPLETED, true).apply()
        Log.d(TAG, "Migration v4 completed successfully.")
    }

    private fun loadLegacyIdMap(context: Context): Map<String, List<String>> {
        val result = HashMap<String, List<String>>()
        try {
            context.assets.open("legacy_id_map.json").use { stream ->
                InputStreamReader(stream, Charsets.UTF_8).use { reader ->
                    val json = JSONObject(reader.readText())
                    val keys = json.keys()
                    while (keys.hasNext()) {
                        val k = keys.next()
                        val arr = json.optJSONArray(k)
                        if (arr != null) {
                            val list = ArrayList<String>(arr.length())
                            for (i in 0 until arr.length()) {
                                list.add(arr.getString(i))
                            }
                            result[k] = list
                        }
                    }
                }
            }
        } catch (e: Exception) {
            Log.w(TAG, "legacy_id_map.json not found in assets, skipping map indexing.")
        }
        return result
    }
}
