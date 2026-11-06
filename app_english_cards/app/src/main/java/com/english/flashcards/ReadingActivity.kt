package com.english.flashcards

import android.graphics.Color
import android.content.res.ColorStateList
import android.os.Bundle
import android.text.SpannableString
import android.text.Spanned
import android.text.method.LinkMovementMethod
import android.text.style.ClickableSpan
import android.view.View
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.english.flashcards.data.FlashcardRepository
import com.english.flashcards.model.Flashcard
import com.google.android.material.button.MaterialButton
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import org.json.JSONArray
import org.json.JSONObject

/** Offline guided reading: tap a word, save it for review, then check comprehension. */
class ReadingActivity : AppCompatActivity() {
    private lateinit var root: LinearLayout
    private lateinit var readings: JSONArray
    private lateinit var vocabulary: Map<String, Flashcard>
    private val progress by lazy { getSharedPreferences("reading_comprehension", MODE_PRIVATE) }
    private val unknown by lazy { getSharedPreferences("reading_unknown_words", MODE_PRIVATE) }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        readings = JSONArray(assets.open("readings.json").bufferedReader().use { it.readText() })
        vocabulary = FlashcardRepository(this).getAllCards()
            .filter { it.studyCollections.isNotEmpty() }
            .associateBy { it.word.lowercase() }
        val scroll = ScrollView(this)
        root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(22), dp(18), dp(22), dp(32))
            setBackgroundColor(getColor(R.color.bg_main))
        }
        scroll.addView(root)
        setContentView(scroll)
        showList()
    }

    private fun showList() {
        root.removeAllViews()
        button("← Меню") { finish() }
        label("Читаю документацию", 28, Color.WHITE)
        label("Читайте короткий текст. Нажмите на незнакомое слово, чтобы увидеть перевод и добавить его в повторение. Затем ответьте на вопросы.",
            16, getColor(R.color.text_secondary))
        for (i in 0 until readings.length()) {
            val item = readings.getJSONObject(i)
            val done = progress.getBoolean("${item.getString("id")}.done", false)
            button("${i + 1}. ${item.getString("title")}${if (done) " ✓" else ""}") { showReading(i) }
        }
    }

    private fun showReading(position: Int) {
        val item = readings.getJSONObject(position)
        val id = item.getString("id")
        root.removeAllViews()
        button("← К текстам") { showList() }
        label(item.getString("title"), 26, Color.WHITE)
        label("По мотивам: ${item.getString("source_url")}", 12, getColor(R.color.text_secondary))
        val passage = item.getString("passage")
        val spannable = SpannableString(passage)
        Regex("[A-Za-z][A-Za-z'-]*").findAll(passage).forEach { match ->
            val word = match.value
            spannable.setSpan(object : ClickableSpan() {
                override fun onClick(widget: View) = showWord(word)
                override fun updateDrawState(ds: android.text.TextPaint) {
                    ds.color = Color.WHITE
                    ds.isUnderlineText = false
                }
            }, match.range.first, match.range.last + 1, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE)
        }
        label("", 18, Color.WHITE).apply {
            text = spannable
            movementMethod = LinkMovementMethod.getInstance()
            highlightColor = getColor(R.color.accent_blue)
            setLineSpacing(dp(6).toFloat(), 1f)
        }
        label("Проверьте понимание", 22, getColor(R.color.accent_blue))
        val questions = item.getJSONArray("questions")
        for (q in 0 until questions.length()) {
            val question = questions.getJSONObject(q)
            val solved = progress.getBoolean("$id.question.$q", false)
            button("${q + 1}. ${question.getString("question_ru")}${if (solved) " ✓" else ""}") {
                askQuestion(item, q, position)
            }
        }
        if (progress.getBoolean("$id.done", false)) {
            label("Текст пройден: оба ответа верны.", 17, getColor(R.color.accent_green))
        }
    }

    private fun showWord(raw: String) {
        val value = raw.lowercase().trim('\'', '-')
        val variants = listOf(value, value.removeSuffix("s"), value.removeSuffix("ed"),
            value.removeSuffix("ing"), value.removeSuffix("ies") + "y")
        val card = variants.firstNotNullOfOrNull { vocabulary[it] }
        if (card == null) {
            MaterialAlertDialogBuilder(this).setTitle(raw)
                .setMessage("Этого слова пока нет в словарной колоде.")
                .setPositiveButton("Закрыть", null).show()
            return
        }
        val sentence = if (card.example.isNotBlank() && !card.example.equals(card.word, true))
            "\n\n${card.example}\n${card.primaryExampleRu}" else ""
        MaterialAlertDialogBuilder(this).setTitle(card.word)
            .setMessage(card.cleanTranslation + sentence)
            .setPositiveButton("Добавить в повторение") { _, _ ->
                val ids = unknown.getStringSet("card_ids", emptySet()).orEmpty().toMutableSet()
                ids.add(card.cardId)
                unknown.edit().putStringSet("card_ids", ids).apply()
            }
            .setNegativeButton("Закрыть", null).show()
    }

    private fun askQuestion(item: JSONObject, questionIndex: Int, readingIndex: Int) {
        val question = item.getJSONArray("questions").getJSONObject(questionIndex)
        val choices = question.getJSONArray("options_ru")
        val order = (0 until choices.length()).shuffled()
        val labels = Array(choices.length()) { choices.getString(order[it]) }
        MaterialAlertDialogBuilder(this).setTitle(question.getString("question_ru"))
            .setItems(labels) { _, selected ->
                val correct = order[selected] == question.getInt("correct")
                val message = (if (correct) "Верно. " else "Пока неверно. ") +
                    question.getString("explanation_ru")
                if (correct) {
                    val id = item.getString("id")
                    progress.edit().putBoolean("$id.question.$questionIndex", true).apply()
                    val allDone = (0 until item.getJSONArray("questions").length()).all {
                        progress.getBoolean("$id.question.$it", false)
                    }
                    if (allDone) progress.edit().putBoolean("$id.done", true).apply()
                }
                MaterialAlertDialogBuilder(this).setMessage(message)
                    .setPositiveButton("Продолжить") { _, _ -> showReading(readingIndex) }.show()
            }.show()
    }

    private fun label(text: String, size: Int, color: Int): TextView {
        val view = TextView(this).apply {
            this.text = text
            textSize = size.toFloat()
            setTextColor(color)
            setPadding(0, dp(12), 0, dp(12))
        }
        root.addView(view)
        return view
    }

    private fun button(text: String, click: () -> Unit) {
        root.addView(MaterialButton(this).apply {
            this.text = text
            textSize = 16f
            setTextColor(Color.WHITE)
            backgroundTintList = ColorStateList.valueOf(Color.rgb(30, 41, 59))
            setOnClickListener { click() }
        })
    }

    private fun dp(value: Int) = (value * resources.displayMetrics.density).toInt()
}
