package com.english.flashcards.data

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.withTransaction
import androidx.room.migration.Migration
import androidx.sqlite.db.SupportSQLiteDatabase

@Database(
    entities = [
        PracticeStateEntity::class,
        ReviewEventEntity::class,
        UserEntryStateEntity::class
    ],
    version = 2,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {

    abstract fun practiceDao(): PracticeDao
    abstract fun reviewEventDao(): ReviewEventDao
    abstract fun userEntryDao(): UserEntryDao

    suspend fun recordReviewTransaction(
        practice: PracticeStateEntity,
        event: ReviewEventEntity
    ) {
        withTransaction {
            practiceDao().upsert(practice)
            reviewEventDao().insert(event)
        }
    }

    suspend fun undoLastReviewTransaction(): Boolean {
        return withTransaction {
            val lastEvent = reviewEventDao().getLastReviewEvent() ?: return@withTransaction false
            reviewEventDao().markUndone(lastEvent.attemptId)
            val practice = practiceDao().getByPracticeId(lastEvent.practiceId) ?: return@withTransaction false
            val reverted = practice.copy(
                state = lastEvent.stateBefore,
                reps = maxOf(0, practice.reps - 1),
                due = System.currentTimeMillis()
            )
            practiceDao().upsert(reverted)
            true
        }
    }

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        val MIGRATION_1_2 = object : Migration(1, 2) {
            override fun migrate(db: SupportSQLiteDatabase) {
                db.execSQL("ALTER TABLE review_events ADD COLUMN attemptId TEXT NOT NULL DEFAULT ''")
                db.execSQL("ALTER TABLE review_events ADD COLUMN isAssisted INTEGER NOT NULL DEFAULT 0")
                db.execSQL("ALTER TABLE review_events ADD COLUMN hintsUsed INTEGER NOT NULL DEFAULT 0")
                db.execSQL("ALTER TABLE review_events ADD COLUMN listensCount INTEGER NOT NULL DEFAULT 0")
                db.execSQL("ALTER TABLE review_events ADD COLUMN isUndone INTEGER NOT NULL DEFAULT 0")
                db.execSQL("ALTER TABLE review_events ADD COLUMN contentRevision INTEGER NOT NULL DEFAULT 1")
                db.execSQL("ALTER TABLE review_events ADD COLUMN schedulerVersion TEXT NOT NULL DEFAULT 'FSRS-4.5'")
                db.execSQL("CREATE UNIQUE INDEX IF NOT EXISTS index_review_events_attemptId ON review_events (attemptId)")
            }
        }

        fun getInstance(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "english_cards.db"
                )
                    .addMigrations(MIGRATION_1_2)
                    .fallbackToDestructiveMigration()
                    .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
