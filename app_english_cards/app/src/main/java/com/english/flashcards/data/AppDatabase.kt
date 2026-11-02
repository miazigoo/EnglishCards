package com.english.flashcards.data

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(
    entities = [
        PracticeStateEntity::class,
        ReviewEventEntity::class,
        UserEntryStateEntity::class
    ],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {

    abstract fun practiceDao(): PracticeDao
    abstract fun reviewEventDao(): ReviewEventDao
    abstract fun userEntryDao(): UserEntryDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getInstance(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "english_cards.db"
                ).build()
                INSTANCE = instance
                instance
            }
        }
    }
}
