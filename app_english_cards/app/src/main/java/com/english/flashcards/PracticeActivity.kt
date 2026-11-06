package com.english.flashcards

import android.os.Bundle
import android.os.SystemClock
import android.view.View
import android.view.inputmethod.InputMethodManager
import android.content.Context
import android.graphics.Color
import android.content.res.ColorStateList
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.room.withTransaction
import androidx.lifecycle.lifecycleScope
import com.english.flashcards.audio.AudioController
import com.english.flashcards.data.AppDatabase
import com.english.flashcards.data.FlashcardRepository
import com.english.flashcards.data.PracticeStateEntity
import com.english.flashcards.data.ProgressManager
import com.english.flashcards.data.ReviewEventEntity
import com.english.flashcards.fsrs.FSRSCard
import com.english.flashcards.fsrs.FSRSScheduler
import com.english.flashcards.fsrs.Rating
import com.english.flashcards.fsrs.State
import com.english.flashcards.model.CardStatus
import com.english.flashcards.model.Flashcard
import com.google.android.material.button.MaterialButton
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.util.UUID

/** A review is a separate task for each skill. Browsing and passive audio never score it. */
class PracticeActivity : AppCompatActivity() {
    private lateinit var repo: FlashcardRepository
    private lateinit var db: AppDatabase
    private lateinit var audio: AudioController
    private lateinit var root: LinearLayout
    private val scheduler = FSRSScheduler()
    private val tasks = mutableListOf<PracticeTask>()
    private var index = 0
    private var startedAt = 0L
    private var mode = "today"
    private var saving = false
    private var lastUndo: UndoSnapshot? = null

    data class PracticeTask(val card: Flashcard, val skill: String, val existing: PracticeStateEntity?)
    data class UndoSnapshot(val position: Int, val old: PracticeStateEntity?,
                            val attemptId: String, val oldStatus: CardStatus)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        mode = intent.getStringExtra("mode") ?: "today"
        repo = FlashcardRepository(this)
        db = AppDatabase.getInstance(this)
        audio = AudioController(this, {}, { _, _ -> }, {})

        val scroll = ScrollView(this)
        root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(22), dp(20), dp(22), dp(36))
            setBackgroundColor(getColor(R.color.bg_main))
        }
        scroll.addView(root)
        setContentView(scroll)
        label("Загрузка заданий…", 21, Color.WHITE)

        lifecycleScope.launch(Dispatchers.IO) {
            val loaded = loadTasks()
            withContext(Dispatchers.Main) {
                tasks.addAll(loaded)
                showTask()
            }
        }
    }

    private suspend fun loadTasks(): List<PracticeTask> {
        val all = repo.getAllCards().associateBy { it.cardId }
        val vocab = repo.getAllCards().filter { it.studyCollections.isNotEmpty() }.associateBy { it.cardId }
        val dao = db.practiceDao()
        val now = System.currentTimeMillis()
        if (mode == "hard") {
            return ProgressManager(this).getHardCards(repo.getAllCards()).map { card ->
                PracticeTask(card, "en_to_ru", dao.getByPracticeId("${card.cardId}.en_to_ru"))
            }
        }
        if (mode == "today") {
            val unknown = getSharedPreferences("reading_unknown_words", MODE_PRIVATE)
                .getStringSet("card_ids", emptySet()).orEmpty()
            val marked = dao.getAll().filter {
                it.cardId in unknown && it.skill == "en_to_ru" && it.state != State.NEW.value
            }
            val due = (marked + dao.getDuePractices(now)).distinctBy { it.practiceId }
                .filter { it.skill == "en_to_ru" || it.skill == "ru_to_en" }
                .sortedWith(compareBy<PracticeStateEntity> { if (it.cardId in vocab) 0 else 1 }.thenBy { it.due })
            val dueIds = due.map { it.cardId }.toSet()
            val newRows = dao.getNewPractices(10000)
                .filter { it.cardId in vocab && it.cardId !in dueIds &&
                    (it.skill == "en_to_ru" || it.skill == "ru_to_en") }
            val newIds = newRows.map { it.cardId }.distinct()
                .sortedWith(compareBy<String> { if (it in unknown) 0 else 1 }
                    .thenBy { if (it.startsWith("anki.vocab.")) 0 else 1 }.thenBy { it })
                .take(10).toSet()
            val newTasks = newRows.filter { it.cardId in newIds }
                .sortedWith(compareBy<PracticeStateEntity> { if (it.skill == "en_to_ru") 0 else 1 }
                    .thenBy { it.cardId })
            return (due.filter { it.cardId in vocab } + newTasks + due.filter { it.cardId !in vocab })
                .mapNotNull { row ->
                all[row.cardId]?.let { PracticeTask(it, row.skill, row) }
            }
        }

        val selected = if (mode == "cloze") {
            vocab.values.filter { card -> clozeSentence(card) != null }
        } else {
            vocab.values.toList()
        }
        val skill = if (mode == "cloze") "cloze" else "listening"
        val existing = dao.getAll().filter { it.skill == skill }.associateBy { it.cardId }
        return selected.filter { card ->
            val previous = existing[card.cardId]
            previous == null || previous.state == State.NEW.value || previous.due <= now
        }.sortedWith(compareBy<Flashcard> { card ->
            val previous = existing[card.cardId]
            if (previous != null && previous.state != State.NEW.value) 0 else 1
        }.thenBy { if (it.cardId.startsWith("anki.vocab.")) 0 else 1 }.thenBy { it.cardId })
            .take(20).map { card -> PracticeTask(card, skill, existing[card.cardId]) }
    }

    private fun showTask() {
        audio.stop()
        root.removeAllViews()
        startedAt = SystemClock.elapsedRealtime()
        button("← Меню") { finish() }
        val undo = lastUndo
        if (undo != null && undo.position == index - 1) {
            button("↩ Отменить предыдущий ответ") { undoReview(undo) }
        }
        if (index >= tasks.size) {
            label("Занятие завершено", 28, Color.WHITE)
            label("Повторения сохранены. Возвращайтесь завтра за следующими словами.", 17, getColor(R.color.text_secondary))
            return
        }
        val task = tasks[index]
        val card = task.card
        val title = when (task.skill) {
            "ru_to_en" -> "Русский → английский"
            "listening" -> "Диктант на слух"
            "cloze" -> "Слово в предложении"
            else -> "Английский → русский"
        }
        label(title, 26, Color.WHITE)
        label("${index + 1} / ${tasks.size}  •  ${card.category}", 15, getColor(R.color.text_secondary))

        when (task.skill) {
            "en_to_ru" -> {
                label(card.word, 38, Color.WHITE)
                button("🔊 Слушать слово") { audio.playTerm(card) }
                button("Показать перевод") {
                    root.removeView(it)
                    label(card.cleanTranslation, 27, getColor(R.color.accent_green))
                    if (hasSentence(card)) {
                        label("${card.example}\n${card.primaryExampleRu}", 17, Color.WHITE)
                        button("🔊 Слушать фразу") { audio.playExample(card) }
                    }
                    ratingButtons(task)
                }
                audio.playTerm(card)
            }
            "ru_to_en" -> {
                label(card.cleanTranslation, 31, Color.WHITE)
                answerInput(task, "Напишите слово по-английски")
            }
            "listening" -> {
                label("Послушайте и напишите английское слово", 22, Color.WHITE)
                button("🔊 Воспроизвести") { audio.playTerm(card) }
                answerInput(task, "Что вы услышали?")
                audio.playTerm(card)
            }
            "cloze" -> {
                val (sentence, target) = clozeSentence(card) ?: return
                label(sentence.replace(Regex("\\b${Regex.escape(target)}\\b", RegexOption.IGNORE_CASE), "_____"), 24, Color.WHITE)
                label(card.primaryExampleRu, 16, getColor(R.color.text_secondary))
                answerInput(task, "Впишите пропущенное слово")
            }
        }
    }

    private fun answerInput(task: PracticeTask, hint: String) {
        val input = EditText(this).apply {
            this.hint = hint
            setTextColor(Color.WHITE)
            setHintTextColor(getColor(R.color.text_secondary))
            isSingleLine = true
            textSize = 20f
            inputType = android.text.InputType.TYPE_CLASS_TEXT or
                android.text.InputType.TYPE_TEXT_FLAG_NO_SUGGESTIONS
        }
        root.addView(input)
        button("Проверить ответ") { buttonView ->
            if (input.text.isNullOrBlank()) {
                input.error = "Введите ответ"
                return@button
            }
            buttonView.isEnabled = false
            input.isEnabled = false
            val expected = if (task.skill == "cloze") task.card.clozeTarget ?: task.card.word else task.card.word
            val answers = (task.card.acceptedAnswers + expected).distinct()
            val answer = normalize(input.text.toString())
            val exact = answers.any { normalize(it) == answer }
            val typo = !exact && answers.any { isMinorTypo(answer, normalize(it)) }
            val rating = when {
                exact -> Rating.GOOD
                typo -> Rating.HARD
                else -> Rating.AGAIN
            }
            val message = when {
                exact -> "Верно: $expected"
                typo -> "Почти верно: $expected (опечатка)"
                else -> "Нужно: $expected. ${task.card.cleanTranslation}"
            }
            label(message, 21, if (exact) getColor(R.color.accent_green) else Color.WHITE)
            if (hasSentence(task.card)) {
                label("${task.card.example}\n${task.card.primaryExampleRu}", 17, Color.WHITE)
                button("🔊 Слушать фразу") { audio.playExample(task.card) }
            }
            button("Продолжить") { saveAndAdvance(task, rating) }
            (getSystemService(Context.INPUT_METHOD_SERVICE) as InputMethodManager)
                .hideSoftInputFromWindow(input.windowToken, 0)
        }
    }

    private fun ratingButtons(task: PracticeTask) {
        label("Удалось вспомнить перевод?", 17, getColor(R.color.text_secondary))
        button("Не вспомнил") { saveAndAdvance(task, Rating.AGAIN) }
        button("С трудом") { saveAndAdvance(task, Rating.HARD) }
        button("Вспомнил") { saveAndAdvance(task, Rating.GOOD) }
        button("Очень легко") { saveAndAdvance(task, Rating.EASY) }
    }

    private fun saveAndAdvance(task: PracticeTask, rating: Rating) {
        if (saving) return
        saving = true
        val now = System.currentTimeMillis()
        val id = "${task.card.cardId}.${task.skill}"
        val attemptId = UUID.randomUUID().toString()
        val oldStatus = ProgressManager(this).getStatus(task.card.id)
        val old = task.existing?.let { FSRSCard(
            practiceId = it.practiceId, cardId = it.cardId, skill = it.skill,
            due = it.due, stability = it.stability, difficulty = it.difficulty,
            elapsedDays = it.elapsedDays, scheduledDays = it.scheduledDays,
            reps = it.reps, lapses = it.lapses, state = State.fromInt(it.state),
            lastReview = it.lastReview
        ) } ?: FSRSCard(practiceId = id, cardId = task.card.cardId, skill = task.skill, due = now)
        val updated = scheduler.review(old, rating, now)
        val entity = PracticeStateEntity(
            id, task.card.cardId, task.skill, updated.state.value,
            updated.stability, updated.difficulty, updated.elapsedDays,
            updated.scheduledDays, updated.reps, updated.lapses, updated.due, updated.lastReview
        )
        val event = ReviewEventEntity(
            attemptId = attemptId, practiceId = id,
            cardId = task.card.cardId, skill = task.skill, rating = rating.value,
            reviewTime = now, durationMs = maxOf(200L, SystemClock.elapsedRealtime() - startedAt),
            stateBefore = old.state.value, stateAfter = updated.state.value,
            stabilityAfter = updated.stability, difficultyAfter = updated.difficulty,
            scheduledDaysAfter = updated.scheduledDays,
            listensCount = if (task.skill == "listening") 1 else 0
        )
        lifecycleScope.launch(Dispatchers.IO) {
            db.recordReviewTransaction(entity, event)
            if (task.skill == "en_to_ru" || task.skill == "ru_to_en") {
                val both = db.practiceDao().getByCardId(task.card.cardId)
                    .filter { it.skill == "en_to_ru" || it.skill == "ru_to_en" }
                val status = when {
                    rating == Rating.AGAIN || rating == Rating.HARD -> CardStatus.HARD
                    both.size == 2 && both.all { it.state == State.REVIEW.value } -> CardStatus.LEARNED
                    else -> CardStatus.NEW
                }
                ProgressManager(this@PracticeActivity).setStatus(task.card.id, status)
            }
            val prefs = getSharedPreferences("reading_unknown_words", MODE_PRIVATE)
            val ids = prefs.getStringSet("card_ids", emptySet()).orEmpty().toMutableSet()
            if (ids.remove(task.card.cardId)) prefs.edit().putStringSet("card_ids", ids).apply()
            withContext(Dispatchers.Main) {
                saving = false
                lastUndo = UndoSnapshot(index, task.existing, attemptId, oldStatus)
                index++
                showTask()
            }
        }
    }

    private fun undoReview(snapshot: UndoSnapshot) {
        if (saving) return
        saving = true
        lifecycleScope.launch(Dispatchers.IO) {
            db.withTransaction {
                val practiceId = tasks[snapshot.position].let { "${it.card.cardId}.${it.skill}" }
                if (snapshot.old == null) db.practiceDao().deleteByPracticeId(practiceId)
                else db.practiceDao().upsert(snapshot.old)
                db.reviewEventDao().markUndone(snapshot.attemptId)
            }
            ProgressManager(this@PracticeActivity).setStatus(tasks[snapshot.position].card.id, snapshot.oldStatus)
            withContext(Dispatchers.Main) {
                index = snapshot.position
                lastUndo = null
                saving = false
                showTask()
            }
        }
    }

    private fun hasSentence(card: Flashcard): Boolean = card.example.isNotBlank() &&
        !card.example.equals(card.word, ignoreCase = true)

    private fun clozeSentence(card: Flashcard): Pair<String, String>? {
        if (!hasSentence(card)) return null
        val target = card.clozeTarget ?: card.word
        return if (Regex("\\b${Regex.escape(target)}\\b", RegexOption.IGNORE_CASE).containsMatchIn(card.example))
            card.example to target else null
    }

    private fun normalize(value: String): String = value.trim().lowercase()
        .replace('’', '\'').replace(Regex("[^a-z0-9' -]"), "")
        .replace(Regex("[ -]+"), " ")

    private fun isMinorTypo(actual: String, expected: String): Boolean {
        if (expected.length < 5 || kotlin.math.abs(actual.length - expected.length) > 1) return false
        var i = 0
        var j = 0
        var mistakes = 0
        while (i < actual.length && j < expected.length) {
            if (actual[i] == expected[j]) { i++; j++; continue }
            mistakes++
            if (mistakes > 1) return false
            if (actual.length > expected.length) i++
            else if (expected.length > actual.length) j++
            else { i++; j++ }
        }
        return mistakes + (actual.length - i) + (expected.length - j) <= 1
    }

    private fun label(value: String, size: Int, color: Int): TextView {
        val view = TextView(this).apply {
            text = value
            textSize = size.toFloat()
            setTextColor(color)
            setPadding(0, dp(13), 0, dp(13))
        }
        root.addView(view)
        return view
    }

    private fun button(value: String, click: (MaterialButton) -> Unit): MaterialButton {
        val view = MaterialButton(this).apply {
            text = value
            textSize = 17f
            setTextColor(Color.WHITE)
            backgroundTintList = ColorStateList.valueOf(Color.rgb(30, 41, 59))
            setOnClickListener { click(this) }
        }
        root.addView(view)
        return view
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density).toInt()

    override fun onDestroy() {
        audio.stop()
        super.onDestroy()
    }
}
