package com.english.flashcards.data

import android.content.Context
import android.util.Log
import com.english.flashcards.fsrs.State
import com.english.flashcards.model.Card
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONArray
import java.io.InputStreamReader
import java.util.concurrent.TimeUnit

object RoomMigrationHelper {

    private const val TAG = "RoomMigrationHelper"
    private const val PREFS_NAME = "EnglishCardsPrefs"
    private const val KEY_MIGRATION_COMPLETED = "room_migration_completed_v3"

    suspend fun checkAndMigrate(context: Context, cards: List<Card>) = withContext(Dispatchers.IO) {
        val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        val isMigrated = prefs.getBoolean(KEY_MIGRATION_COMPLETED, false)

        val db = AppDatabase.getInstance(context)
        val practiceDao = db.practiceDao()
        val userEntryDao = db.userEntryDao()

        // If practice states are already initialized, no need to re-seed
        val totalNew = practiceDao.countNewPractices()
        val totalDue = practiceDao.countDuePractices(Long.MAX_VALUE)
        if (isMigrated && (totalNew > 0 || totalDue > 0)) {
            Log.d(TAG, "Migration already completed, active practices: ${totalNew + totalDue}")
            return@withContext
        }

        Log.d(TAG, "Starting migration and practice state seeding for ${cards.size} cards...")
        val now = System.currentTimeMillis()
        val practiceEntities = ArrayList<PracticeStateEntity>(cards.size * 2)
        val userEntries = ArrayList<UserEntryStateEntity>(cards.size)

        // Read legacy legacy_id_map from assets if present
        val legacyIdMap = loadLegacyIdMap(context)

        for (card in cards) {
            val cardId = card.cardId.ifEmpty { "legacy.${card.id}.${card.word.lowercase()}" }
            val legacyId = card.id

            // Check SharedPreferences for legacy status
            val legacyStatus = prefs.getString("card_status_$legacyId", null)
            val isFavorite = prefs.getBoolean("card_favorite_$legacyId", false)

            if (isFavorite) {
                userEntries.add(UserEntryStateEntity(cardId = cardId, isPinned = true))
            }

            val (initialState, stability, scheduledDays, dueTime) = when (legacyStatus) {
                "learned" -> Tuple4(
                    State.REVIEW.value,
                    10.0,
                    5L,
                    now + TimeUnit.DAYS.toMillis(5)
                )
                "in_progress" -> Tuple4(
                    State.LEARNING.value,
                    2.0,
                    0L,
                    now
                )
                else -> Tuple4(
                    State.NEW.value,
                    0.0,
                    0L,
                    now
                )
            }

            // Skill 1: EN -> RU (Recognition)
            practiceEntities.add(
                PracticeStateEntity(
                    practiceId = "$cardId.en_to_ru",
                    cardId = cardId,
                    skill = "en_to_ru",
                    state = initialState,
                    stability = stability,
                    difficulty = 5.0,
                    elapsedDays = 0,
                    scheduledDays = scheduledDays,
                    reps = if (initialState == State.REVIEW.value) 3 else 0,
                    lapses = 0,
                    due = dueTime,
                    lastReview = if (initialState == State.REVIEW.value) now - TimeUnit.DAYS.toMillis(1) else 0L
                )
            )

            // Skill 2: RU -> EN (Production)
            practiceEntities.add(
                PracticeStateEntity(
                    practiceId = "$cardId.ru_to_en",
                    cardId = cardId,
                    skill = "ru_to_en",
                    state = initialState,
                    stability = stability,
                    difficulty = 5.5,
                    elapsedDays = 0,
                    scheduledDays = scheduledDays,
                    reps = if (initialState == State.REVIEW.value) 3 else 0,
                    lapses = 0,
                    due = dueTime,
                    lastReview = if (initialState == State.REVIEW.value) now - TimeUnit.DAYS.toMillis(1) else 0L
                )
            )
        }

        // Upsert all batch
        practiceDao.upsertAll(practiceEntities)
        for (ue in userEntries) {
            userEntryDao.upsert(ue)
        }

        prefs.edit().putBoolean(KEY_MIGRATION_COMPLETED, true).apply()
        Log.d(TAG, "Seeded ${practiceEntities.size} practice items into Room database.")
    }

    private fun loadLegacyIdMap(context: Context): Map<Int, List<String>> {
        return try {
            val stream = context.assets.open("legacy_id_map.json")
            val text = InputStreamReader(stream).readText()
            val json = org.json.JSONObject(text)
            val result = HashMap<Int, List<String>>()
            val keys = json.keys()
            while (keys.hasNext()) {
                val k = keys.next()
                val arr = json.getJSONArray(k)
                val list = ArrayList<String>()
                for (i in 0 until arr.length()) {
                    list.add(arr.getString(i))
                }
                result[k.toInt()] = list
            }
            result
        } catch (e: Exception) {
            emptyMap()
        }
    }

    private data class Tuple4<A, B, C, D>(val a: A, val b: B, val c: C, val d: D)
}
