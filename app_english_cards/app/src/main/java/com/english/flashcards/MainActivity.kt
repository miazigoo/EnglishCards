package com.english.flashcards

import android.content.ClipData
import android.content.ClipboardManager
import android.graphics.Color
import android.os.Bundle
import android.os.SystemClock
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.WindowManager
import android.widget.RadioButton
import android.widget.TextView
import android.widget.Toast
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity
import androidx.core.widget.doAfterTextChanged
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import androidx.viewpager2.widget.ViewPager2
import com.english.flashcards.audio.AudioController
import com.english.flashcards.data.AppDatabase
import com.english.flashcards.data.FlashcardRepository
import com.english.flashcards.data.PracticeStateEntity
import com.english.flashcards.data.ProgressManager
import com.english.flashcards.data.ReviewEventEntity
import com.english.flashcards.data.RoomMigrationHelper
import com.english.flashcards.databinding.ActivityMainBinding
import com.english.flashcards.databinding.DialogBackupBinding
import com.english.flashcards.databinding.DialogCardExampleBinding
import com.english.flashcards.databinding.DialogLessonDetailBinding
import com.english.flashcards.databinding.DialogLessonsBinding
import com.english.flashcards.databinding.DialogSearchBinding
import com.english.flashcards.databinding.DialogStatsBinding
import com.english.flashcards.databinding.ItemLessonBinding
import com.english.flashcards.databinding.ItemSearchResultBinding
import com.english.flashcards.fsrs.FSRSCard
import com.english.flashcards.fsrs.FSRSScheduler
import com.english.flashcards.fsrs.Rating
import com.english.flashcards.fsrs.State
import com.english.flashcards.model.CardStatus
import com.english.flashcards.model.Flashcard
import com.english.flashcards.ui.CardPagerAdapter
import com.english.flashcards.ui.CategoryItem
import com.english.flashcards.ui.CategoryMenuAdapter
import com.google.android.material.bottomsheet.BottomSheetDialog
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.io.InputStreamReader
import java.util.UUID
import java.util.concurrent.ConcurrentHashMap

class MainActivity : AppCompatActivity() {

    enum class StudyMode {
        TODAY,
        HARD,
        CATEGORY,
        LISTENING
    }

    private lateinit var binding: ActivityMainBinding
    private lateinit var repository: FlashcardRepository
    private lateinit var progressManager: ProgressManager
    private lateinit var cardAdapter: CardPagerAdapter
    private lateinit var audioController: AudioController
    private lateinit var menuAdapter: CategoryMenuAdapter
    private lateinit var db: AppDatabase

    private val fsrsScheduler = FSRSScheduler()
    private val practiceCache = ConcurrentHashMap<String, FSRSCard>()

    private var currentCards: List<Flashcard> = emptyList()
    private var selectedCategory: String = "Все карточки"
    private var repeatCount: Int = 2
    private var isSplashActive: Boolean = true
    private var currentMode: StudyMode = StudyMode.TODAY

    // Monotonic timer for measuring real active recall duration
    private var cardStartTimeMonotonic: Long = 0L

    // For Undo
    private var lastReviewAttemptId: String? = null
    private var lastReviewPosition: Int? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        repository = FlashcardRepository(this)
        progressManager = ProgressManager(this)
        db = AppDatabase.getInstance(this)

        setupAudioController()
        setupViewPager()
        setupMenu()
        setupPlayerControls()
        setupBackNavigation()
        startRealInitialization()
    }

    private fun startRealInitialization() {
        isSplashActive = true
        binding.layoutSplash.visibility = View.VISIBLE
        binding.layoutSplash.alpha = 1f
        binding.layoutMenu.visibility = View.GONE
        binding.layoutPlayer.visibility = View.GONE

        binding.pbSplashLoading.progress = 20
        binding.tvSplashPercent.text = "20%"
        binding.tvSplashStatus.text = "Миграция и проверка Room БД..."

        lifecycleScope.launch(Dispatchers.IO) {
            val allCards = repository.getAllCards()
            RoomMigrationHelper.checkAndMigrate(applicationContext, allCards)

            withContext(Dispatchers.Main) {
                binding.pbSplashLoading.progress = 60
                binding.tvSplashPercent.text = "60%"
                binding.tvSplashStatus.text = "Загрузка FSRS расписания..."
            }

            loadPracticeCache()

            withContext(Dispatchers.Main) {
                binding.pbSplashLoading.progress = 100
                binding.tvSplashPercent.text = "100%"
                binding.tvSplashStatus.text = "Все готово!"

                binding.layoutSplash.animate()
                    .alpha(0f)
                    .setDuration(300)
                    .withEndAction {
                        binding.layoutSplash.visibility = View.GONE
                        isSplashActive = false
                        refreshMenuStats()
                        binding.layoutMenu.alpha = 0f
                        binding.layoutMenu.visibility = View.VISIBLE
                        binding.layoutMenu.animate().alpha(1f).setDuration(300).start()
                    }
                    .start()
            }
        }
    }

    private suspend fun loadPracticeCache() {
        try {
            val practices = db.practiceDao().getAll()
            for (p in practices) {
                practiceCache[p.practiceId] = FSRSCard(
                    practiceId = p.practiceId,
                    cardId = p.cardId,
                    skill = p.skill,
                    due = p.due,
                    stability = p.stability,
                    difficulty = p.difficulty,
                    elapsedDays = p.elapsedDays,
                    scheduledDays = p.scheduledDays,
                    reps = p.reps,
                    lapses = p.lapses,
                    state = State.fromInt(p.state),
                    lastReview = p.lastReview
                )
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun setupMenu() {
        // Top Tools Row
        binding.btnMenuLessons.setOnClickListener {
            showLessonsDialog()
        }
        binding.btnMenuSearch.setOnClickListener {
            showSearchDialog()
        }
        binding.btnMenuStats.setOnClickListener {
            showStatsDialog()
        }
        binding.btnMenuBackup.setOnClickListener {
            showBackupDialog()
        }

        // 1. Featured TODAY (FSRS Due Queue)
        val onTodayClick = View.OnClickListener {
            openPlayerWithToday()
        }
        binding.btnFeaturedToday.setOnClickListener(onTodayClick)
        binding.btnStartToday.setOnClickListener(onTodayClick)

        // 2. Featured HARD
        val onHardClick = View.OnClickListener {
            openPlayerWithHardCards()
        }
        binding.btnFeaturedHard.setOnClickListener(onHardClick)
        binding.btnStartHard.setOnClickListener(onHardClick)

        // 3. Featured LISTENING
        val onListeningClick = View.OnClickListener {
            val allCatName = repository.getCategories().firstOrNull() ?: "Все карточки"
            openPlayerWithListening(allCatName)
        }
        binding.btnFeaturedListening.setOnClickListener(onListeningClick)
        binding.btnStartListening.setOnClickListener(onListeningClick)

        // 4. Featured ALL
        val allCatName = repository.getCategories().firstOrNull() ?: "Все карточки"
        val onAllClick = View.OnClickListener {
            openPlayerWithCategory(allCatName)
        }
        binding.btnFeaturedAll.setOnClickListener(onAllClick)
        binding.btnStartAll.setOnClickListener(onAllClick)

        // Repeat Switcher in Menu
        binding.btnMenuRepeatCount.text = "${repeatCount}x (повтор)"
        binding.btnMenuRepeatCount.setOnClickListener {
            toggleRepeatCount()
            binding.btnMenuRepeatCount.text = "${repeatCount}x (повтор)"
        }

        // Category Menu Adapter
        val categoryItems = buildCategoryItems()
        menuAdapter = CategoryMenuAdapter(categoryItems) { item ->
            openPlayerWithCategory(item.name)
        }
        binding.rvMenuCategories.layoutManager = LinearLayoutManager(this)
        binding.rvMenuCategories.adapter = menuAdapter

        refreshMenuStats()
    }

    private fun buildCategoryItems(): List<CategoryItem> {
        val allCats = repository.getCategories().filter { !it.startsWith("Все") }
        return allCats.map { cat ->
            val catCards = repository.getCardsByCategory(cat)
            val (learned, hard, newCards) = progressManager.getCounts(catCards)
            val emoji = getEmojiForCategory(cat)
            CategoryItem(
                name = cat,
                count = catCards.size,
                emoji = emoji,
                learnedCount = learned,
                hardCount = hard,
                newCount = newCards
            )
        }
    }

    private fun refreshMenuStats() {
        val allCards = repository.getAllCards()
        val (totalLearned, totalHard, totalNew) = progressManager.getCounts(allCards)
        val totalCount = allCards.size

        val totalPercent = if (totalCount > 0) ((totalLearned * 100f) / totalCount).toInt() else 0
        binding.tvTotalProgressPercent.text = "$totalPercent%"
        binding.pbTotalProgress.progress = totalPercent
        binding.tvTotalStatsSubtitle.text = "🟢 $totalLearned выучено  •  🟡 $totalHard повторить  •  ⚪ $totalNew новых"

        binding.tvHardSubtitle.text = if (totalHard > 0) {
            "$totalHard карточек требуют повторения"
        } else {
            "Нет карточек на повторение"
        }

        binding.tvAppSubtitle.text = "IT, Backend & Python • $totalCount карточек"
        binding.tvAllSubtitle.text = "Полная колода из $totalCount слов"

        if (::menuAdapter.isInitialized) {
            menuAdapter.updateItems(buildCategoryItems())
        }

        // Refresh Today queue stats from Room DB
        lifecycleScope.launch(Dispatchers.IO) {
            val now = System.currentTimeMillis()
            val dueCount = db.practiceDao().countDuePractices(now)
            val newCount = db.practiceDao().countNewPractices()
            withContext(Dispatchers.Main) {
                binding.tvTodaySubtitle.text = if (dueCount > 0 || newCount > 0) {
                    "$dueCount к повторению • ${minOf(10, newCount)} новых"
                } else {
                    "Все повторения на сегодня выполнены!"
                }
            }
        }
    }

    private fun getEmojiForCategory(cat: String): String {
        return when {
            cat.contains("Python", ignoreCase = true) -> "🐍"
            cat.contains("Django", ignoreCase = true) -> "🎸"
            cat.contains("FastAPI", ignoreCase = true) -> "⚡"
            cat.contains("SQL", ignoreCase = true) || cat.contains("баз", ignoreCase = true) -> "🗄️"
            cat.contains("Git", ignoreCase = true) || cat.contains("Docker", ignoreCase = true) -> "🐳"
            cat.contains("Celery", ignoreCase = true) || cat.contains("асинхрон", ignoreCase = true) -> "⏱️"
            cat.contains("Тестир", ignoreCase = true) -> "🧪"
            cat.contains("Workplace", ignoreCase = true) || cat.contains("Работа", ignoreCase = true) -> "💼"
            cat.contains("General", ignoreCase = true) || cat.contains("Общ", ignoreCase = true) -> "🌐"
            else -> "📖"
        }
    }

    private fun setupAudioController() {
        audioController = AudioController(
            context = this,
            onPlaybackStateChanged = { isPlaying ->
                binding.btnPlayPause.setImageResource(
                    if (isPlaying) R.drawable.ic_pause else R.drawable.ic_play_arrow
                )
                updateKeepScreenOn(isPlaying && binding.layoutPlayer.visibility == View.VISIBLE)
            },
            onRepetitionUpdate = { currentRep, maxRep ->
                binding.tvPlayerRepeatBadge.text = getString(R.string.repeat_badge_fmt, currentRep, maxRep)
            },
            onCardFinished = {
                val currentPos = binding.vpCards.currentItem
                if (currentPos < currentCards.size - 1) {
                    binding.vpCards.setCurrentItem(currentPos + 1, true)
                } else {
                    showDeckCompletionDialog()
                }
            }
        )
        audioController.setMaxRepetitions(repeatCount)
    }

    private fun setupViewPager() {
        cardAdapter = CardPagerAdapter(
            cards = currentCards,
            progressManager = progressManager,
            fsrsScheduler = fsrsScheduler,
            onCardClick = { card ->
                // Prompt stimulus only in Today (Active Recall) mode
                if (currentMode == StudyMode.TODAY) {
                    audioController.playPrompt(card, isEnToRu = true)
                } else {
                    audioController.playListening(card, restartRepetitions = true)
                }
            },
            onExampleClick = { card ->
                showExampleBottomSheet(card)
            },
            onPlayTerm = { card ->
                audioController.playTerm(card)
            },
            onPlayExample = { card ->
                audioController.playExample(card)
            },
            onRatingSelected = { card, rating ->
                handleRatingSelected(card, rating)
            },
            getPracticeState = { cardId ->
                practiceCache["$cardId.en_to_ru"]
            }
        )

        binding.vpCards.adapter = cardAdapter
        binding.vpCards.registerOnPageChangeCallback(object : ViewPager2.OnPageChangeCallback() {
            override fun onPageSelected(position: Int) {
                super.onPageSelected(position)
                updateProgress(position)
                cardStartTimeMonotonic = SystemClock.elapsedRealtime()

                val card = cardAdapter.getCard(position)
                if (card != null && audioController.isAutoPlay()) {
                    if (currentMode == StudyMode.TODAY) {
                        // In Active Recall, play ONLY prompt (NO spoilers!)
                        audioController.playPrompt(card, isEnToRu = true)
                    } else {
                        // In Player / Categories / Listening: play full audio and advance
                        audioController.playListening(card, restartRepetitions = true)
                    }
                }
            }
        })
    }

    private fun handleRatingSelected(card: Flashcard, rating: Rating) {
        val cardKey = card.cardId.ifEmpty { "legacy.${card.id}" }
        val practiceId = "$cardKey.en_to_ru"
        val now = System.currentTimeMillis()
        val duration = maxOf(200L, SystemClock.elapsedRealtime() - cardStartTimeMonotonic)
        val attemptId = UUID.randomUUID().toString()

        val currentFsrsCard = practiceCache[practiceId] ?: FSRSCard(
            practiceId = practiceId,
            cardId = cardKey,
            skill = "en_to_ru",
            due = now
        )

        val updatedCard = fsrsScheduler.review(currentFsrsCard, rating, now)
        practiceCache[practiceId] = updatedCard

        lastReviewAttemptId = attemptId
        lastReviewPosition = binding.vpCards.currentItem
        binding.btnUndoReview.visibility = View.VISIBLE

        // Atomic transaction to Room DB
        lifecycleScope.launch(Dispatchers.IO) {
            val entity = PracticeStateEntity(
                practiceId = updatedCard.practiceId,
                cardId = updatedCard.cardId,
                skill = updatedCard.skill,
                state = updatedCard.state.value,
                stability = updatedCard.stability,
                difficulty = updatedCard.difficulty,
                elapsedDays = updatedCard.elapsedDays,
                scheduledDays = updatedCard.scheduledDays,
                reps = updatedCard.reps,
                lapses = updatedCard.lapses,
                due = updatedCard.due,
                lastReview = updatedCard.lastReview
            )

            val event = ReviewEventEntity(
                attemptId = attemptId,
                practiceId = practiceId,
                cardId = cardKey,
                skill = "en_to_ru",
                rating = rating.value,
                reviewTime = now,
                durationMs = duration,
                stateBefore = currentFsrsCard.state.value,
                stateAfter = updatedCard.state.value,
                stabilityAfter = updatedCard.stability,
                difficultyAfter = updatedCard.difficulty,
                scheduledDaysAfter = updatedCard.scheduledDays
            )
            db.recordReviewTransaction(entity, event)
        }

        // Update legacy status for backward compatibility
        val newStatus = when (rating) {
            Rating.AGAIN, Rating.HARD -> CardStatus.HARD
            Rating.GOOD, Rating.EASY -> CardStatus.LEARNED
        }
        progressManager.setStatus(card.id, newStatus)
        updateDeckStats()
        refreshMenuStats()

        // Advance to next card
        val currentPos = binding.vpCards.currentItem
        if (currentPos < currentCards.size - 1) {
            binding.vpCards.setCurrentItem(currentPos + 1, true)
        } else {
            showDeckCompletionDialog()
        }
    }

    private fun handleUndoLastReview() {
        lifecycleScope.launch(Dispatchers.IO) {
            val success = db.undoLastReviewTransaction()
            loadPracticeCache()
            withContext(Dispatchers.Main) {
                if (success) {
                    Toast.makeText(this@MainActivity, "Оценка отменена ↩", Toast.LENGTH_SHORT).show()
                    binding.btnUndoReview.visibility = View.GONE
                    lastReviewPosition?.let { pos ->
                        if (pos in currentCards.indices) {
                            binding.vpCards.setCurrentItem(pos, true)
                        }
                    }
                    updateDeckStats()
                    refreshMenuStats()
                } else {
                    Toast.makeText(this@MainActivity, "Нечего отменять", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }

    private fun setupPlayerControls() {
        binding.btnBackToMenu.setOnClickListener {
            returnToMenu()
        }

        binding.btnUndoReview.setOnClickListener {
            handleUndoLastReview()
        }

        binding.btnPlayPause.setOnClickListener {
            audioController.togglePlayPause()
        }

        binding.btnNext.setOnClickListener {
            val nextPos = binding.vpCards.currentItem + 1
            if (nextPos < currentCards.size) {
                binding.vpCards.setCurrentItem(nextPos, true)
            } else {
                Toast.makeText(this, "Это последняя карточка в колоде", Toast.LENGTH_SHORT).show()
            }
        }

        binding.btnPrevious.setOnClickListener {
            val prevPos = binding.vpCards.currentItem - 1
            if (prevPos >= 0) {
                binding.vpCards.setCurrentItem(prevPos, true)
            } else {
                Toast.makeText(this, "Это первая карточка", Toast.LENGTH_SHORT).show()
            }
        }

        binding.btnReplay.setOnClickListener {
            audioController.replayCurrent()
        }

        binding.btnPlayerRepeatCount.setOnClickListener {
            toggleRepeatCount()
        }

        binding.btnPlayerCategory.setOnClickListener {
            showCategoryPicker()
        }
    }

    private fun setupBackNavigation() {
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (isSplashActive) {
                    return
                }
                if (binding.layoutPlayer.visibility == View.VISIBLE) {
                    returnToMenu()
                } else {
                    isEnabled = false
                    onBackPressedDispatcher.onBackPressed()
                }
            }
        })
    }

    private fun openPlayerWithToday() {
        lifecycleScope.launch(Dispatchers.IO) {
            val now = System.currentTimeMillis()
            val duePractices = db.practiceDao().getDuePractices(now)
            val newPractices = db.practiceDao().getNewPractices(10)
            val sessionPractices = (duePractices + newPractices).distinctBy { it.cardId }
            val cards = sessionPractices.mapNotNull { p ->
                repository.getCardById(p.cardId)
            }

            withContext(Dispatchers.Main) {
                if (cards.isEmpty()) {
                    Toast.makeText(this@MainActivity, "Все повторения на сегодня выполнены! 🎉", Toast.LENGTH_LONG).show()
                    return@withContext
                }
                currentMode = StudyMode.TODAY
                selectedCategory = "🎯 Сегодня"
                currentCards = cards

                binding.tvPlayerModeBadge.text = "🎯 Сегодня"
                binding.btnPlayerCategory.text = "Сегодня ▾"
                binding.btnPlayerRepeatCount.text = "${repeatCount}x"
                binding.btnUndoReview.visibility = View.GONE

                cardAdapter.setDefaultRevealed(false)
                cardAdapter.updateCards(currentCards)
                binding.vpCards.setCurrentItem(0, false)
                updateProgress(0)
                updateDeckStats()

                binding.layoutMenu.visibility = View.GONE
                binding.layoutPlayer.visibility = View.VISIBLE

                cardStartTimeMonotonic = SystemClock.elapsedRealtime()
                audioController.setAutoPlay(true)
                binding.vpCards.post {
                    audioController.playPrompt(currentCards[0], isEnToRu = true)
                }
            }
        }
    }

    private fun openPlayerWithCategory(categoryName: String) {
        currentMode = StudyMode.CATEGORY
        selectedCategory = categoryName
        currentCards = repository.getCardsByCategory(selectedCategory)

        binding.tvPlayerModeBadge.text = "🌟 Карточки"
        binding.btnPlayerCategory.text = if (selectedCategory.startsWith("Все")) "Все ▾" else "$selectedCategory ▾"
        binding.btnPlayerRepeatCount.text = "${repeatCount}x"
        binding.btnUndoReview.visibility = View.GONE

        cardAdapter.setDefaultRevealed(true)
        cardAdapter.updateCards(currentCards)
        binding.vpCards.setCurrentItem(0, false)
        updateProgress(0)
        updateDeckStats()

        binding.layoutMenu.visibility = View.GONE
        binding.layoutPlayer.visibility = View.VISIBLE

        if (currentCards.isNotEmpty()) {
            cardStartTimeMonotonic = SystemClock.elapsedRealtime()
            audioController.setAutoPlay(true)
            binding.vpCards.post {
                audioController.playListening(currentCards[0], restartRepetitions = true)
            }
        }
    }

    private fun openPlayerWithHardCards() {
        val allCards = repository.getAllCards()
        val hardCards = progressManager.getHardCards(allCards)
        if (hardCards.isEmpty()) {
            Toast.makeText(this, "Пока нет карточек со статусом «Повторить» (🟡)", Toast.LENGTH_SHORT).show()
            return
        }

        currentMode = StudyMode.HARD
        selectedCategory = "🔥 На повторение"
        currentCards = hardCards

        binding.tvPlayerModeBadge.text = "🔥 Повтор"
        binding.btnPlayerCategory.text = "Повтор ▾"
        binding.btnPlayerRepeatCount.text = "${repeatCount}x"
        binding.btnUndoReview.visibility = View.GONE

        cardAdapter.setDefaultRevealed(true)
        cardAdapter.updateCards(currentCards)
        binding.vpCards.setCurrentItem(0, false)
        updateProgress(0)
        updateDeckStats()

        binding.layoutMenu.visibility = View.GONE
        binding.layoutPlayer.visibility = View.VISIBLE

        if (currentCards.isNotEmpty()) {
            cardStartTimeMonotonic = SystemClock.elapsedRealtime()
            audioController.setAutoPlay(true)
            binding.vpCards.post {
                audioController.playListening(currentCards[0], restartRepetitions = true)
            }
        }
    }

    private fun openPlayerWithListening(categoryName: String) {
        currentMode = StudyMode.LISTENING
        selectedCategory = categoryName
        currentCards = repository.getCardsByCategory(selectedCategory)

        binding.tvPlayerModeBadge.text = "🎧 Слушание"
        binding.btnPlayerCategory.text = if (selectedCategory.startsWith("Все")) "Все ▾" else "$selectedCategory ▾"
        binding.btnPlayerRepeatCount.text = "${repeatCount}x"
        binding.btnUndoReview.visibility = View.GONE

        cardAdapter.setDefaultRevealed(true)
        cardAdapter.updateCards(currentCards)
        binding.vpCards.setCurrentItem(0, false)
        updateProgress(0)
        updateDeckStats()

        binding.layoutMenu.visibility = View.GONE
        binding.layoutPlayer.visibility = View.VISIBLE

        if (currentCards.isNotEmpty()) {
            audioController.setAutoPlay(true)
            binding.vpCards.post {
                audioController.playListening(currentCards[0], restartRepetitions = true)
            }
        }
    }

    private fun returnToMenu() {
        audioController.pause()
        updateKeepScreenOn(false)
        binding.layoutPlayer.visibility = View.GONE
        binding.layoutMenu.visibility = View.VISIBLE
        refreshMenuStats()
    }

    private fun toggleRepeatCount() {
        repeatCount = if (repeatCount == 2) 3 else 2
        binding.btnPlayerRepeatCount.text = "${repeatCount}x"
        binding.btnMenuRepeatCount.text = "${repeatCount}x (повтор)"
        audioController.setMaxRepetitions(repeatCount)
        Toast.makeText(this, "Режим повторения: ${repeatCount} раза", Toast.LENGTH_SHORT).show()
    }

    private fun showCategoryPicker() {
        val categories = repository.getCategories().toMutableList()
        val allCards = repository.getAllCards()
        val hardCount = progressManager.getHardCards(allCards).size

        val categoryOptions = mutableListOf<Pair<String, String>>()
        categoryOptions.add("🎯 Сегодня" to "🎯 Сегодня (FSRS очередь)")
        val allCatOption = repository.getCategories().firstOrNull() ?: "Все карточки"
        categoryOptions.add(allCatOption to "🌟 $allCatOption")
        if (hardCount > 0) {
            categoryOptions.add("🔥 На повторение" to "🔥 Сложные слова ($hardCount)")
        }

        for (cat in categories) {
            if (!cat.startsWith("Все")) {
                val count = repository.getCardsByCategory(cat).size
                val prefix = "${getEmojiForCategory(cat)} "
                categoryOptions.add(cat to "$prefix$cat ($count)")
            }
        }

        val displayItems = categoryOptions.map { it.second }.toTypedArray()
        val selectedIndex = categoryOptions.indexOfFirst { it.first == selectedCategory }.let {
            if (it >= 0) it else 0
        }

        MaterialAlertDialogBuilder(this)
            .setTitle("Выберите режим или тему")
            .setSingleChoiceItems(displayItems, selectedIndex) { dialog, which ->
                val chosenCategory = categoryOptions[which].first
                when (chosenCategory) {
                    "🎯 Сегодня" -> openPlayerWithToday()
                    "🔥 На повторение" -> openPlayerWithHardCards()
                    else -> openPlayerWithCategory(chosenCategory)
                }
                dialog.dismiss()
            }
            .setNegativeButton("Отмена", null)
            .show()
    }

    private fun showExampleBottomSheet(card: Flashcard) {
        val dialog = BottomSheetDialog(this)
        val dialogBinding = DialogCardExampleBinding.inflate(layoutInflater)
        dialog.setContentView(dialogBinding.root)

        dialogBinding.tvExampleWord.text = card.word
        dialogBinding.tvExampleTranslation.text = card.cleanTranslation
        dialogBinding.tvExampleCategory.text = card.category

        val codeSnippet = when {
            !card.technicalCode.isNullOrBlank() -> card.technicalCode
            card.example.isNotBlank() -> card.example
            else -> "# Использование ${card.word}:\n# ${card.cleanTranslation}"
        }
        dialogBinding.tvExampleCode.text = codeSnippet

        val noteText = when {
            !card.nameBreakdown.isNullOrBlank() -> "${card.nameBreakdown}\n\n${card.exampleNote}"
            card.exampleNote.isNotBlank() -> card.exampleNote
            else -> card.translation
        }
        dialogBinding.tvExampleNote.text = noteText

        dialogBinding.btnCopyCode.setOnClickListener {
            val clipboard = getSystemService(CLIPBOARD_SERVICE) as ClipboardManager
            val clip = ClipData.newPlainText("code_snippet", codeSnippet)
            clipboard.setPrimaryClip(clip)
            Toast.makeText(this, "Код скопирован в буфер", Toast.LENGTH_SHORT).show()
        }

        dialogBinding.btnCloseDialog.setOnClickListener {
            dialog.dismiss()
        }

        dialogBinding.btnDismissDialog.setOnClickListener {
            dialog.dismiss()
        }

        dialog.show()
    }

    private fun showDeckCompletionDialog() {
        updateKeepScreenOn(false)
        MaterialAlertDialogBuilder(this)
            .setTitle("🎉 Сессия завершена!")
            .setMessage("Вы успешно прошли карточки раздела «$selectedCategory».")
            .setPositiveButton("Повторить сначала") { _, _ ->
                binding.vpCards.setCurrentItem(0, true)
                if (currentCards.isNotEmpty()) {
                    if (currentMode == StudyMode.TODAY) {
                        audioController.playPrompt(currentCards[0], isEnToRu = true)
                    } else {
                        audioController.playListening(currentCards[0], restartRepetitions = true)
                    }
                }
            }
            .setNeutralButton("В меню") { _, _ ->
                returnToMenu()
            }
            .setCancelable(false)
            .show()
    }

    // =========================================================================
    // FEATURE 1: SEARCH & DICTIONARY
    // =========================================================================
    private fun showSearchDialog() {
        val dialog = BottomSheetDialog(this)
        val dialogBinding = DialogSearchBinding.inflate(layoutInflater)
        dialog.setContentView(dialogBinding.root)

        val allCards = repository.getAllCards()
        val resultsList = mutableListOf<Flashcard>()

        class SearchAdapter : RecyclerView.Adapter<SearchAdapter.ViewHolder>() {
            inner class ViewHolder(val b: ItemSearchResultBinding) : RecyclerView.ViewHolder(b.root)
            override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
                val b = ItemSearchResultBinding.inflate(LayoutInflater.from(parent.context), parent, false)
                return ViewHolder(b)
            }
            override fun onBindViewHolder(holder: ViewHolder, position: Int) {
                val card = resultsList[position]
                holder.b.tvSearchWord.text = card.word
                holder.b.tvSearchTranslation.text = card.cleanTranslation
                holder.b.tvSearchCategory.text = card.category
                holder.itemView.setOnClickListener {
                    dialog.dismiss()
                    showExampleBottomSheet(card)
                }
            }
            override fun getItemCount() = resultsList.size
        }

        val adapter = SearchAdapter()
        dialogBinding.rvSearchResults.layoutManager = LinearLayoutManager(this)
        dialogBinding.rvSearchResults.adapter = adapter

        dialogBinding.etSearchQuery.doAfterTextChanged { text ->
            val q = text?.toString()?.trim() ?: ""
            resultsList.clear()
            if (q.isNotEmpty()) {
                val matched = allCards.filter {
                    it.word.contains(q, ignoreCase = true) ||
                    it.cleanTranslation.contains(q, ignoreCase = true) ||
                    it.category.contains(q, ignoreCase = true) ||
                    (!it.technicalCode.isNullOrEmpty() && it.technicalCode.contains(q, ignoreCase = true)) ||
                    it.tags.any { tag -> tag.contains(q, ignoreCase = true) }
                }.take(100)
                resultsList.addAll(matched)
            }
            dialogBinding.tvSearchResultsCount.text = "Найдено карточек: ${resultsList.size}"
            adapter.notifyDataSetChanged()
        }

        dialogBinding.btnCloseSearch.setOnClickListener {
            dialog.dismiss()
        }

        dialog.show()
    }

    // =========================================================================
    // FEATURE 2: 12 MICRO-LESSONS
    // =========================================================================
    private fun showLessonsDialog() {
        val dialog = BottomSheetDialog(this)
        val dialogBinding = DialogLessonsBinding.inflate(layoutInflater)
        dialog.setContentView(dialogBinding.root)

        val lessons = loadLessonsFromAssets()

        class LessonsAdapter : RecyclerView.Adapter<LessonsAdapter.ViewHolder>() {
            inner class ViewHolder(val b: ItemLessonBinding) : RecyclerView.ViewHolder(b.root)
            override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
                val b = ItemLessonBinding.inflate(LayoutInflater.from(parent.context), parent, false)
                return ViewHolder(b)
            }
            override fun onBindViewHolder(holder: ViewHolder, position: Int) {
                val item = lessons[position]
                holder.b.tvLessonNumber.text = String.format("%02d", position + 1)
                holder.b.tvLessonTitle.text = item.optString("title_ru", "Урок")
                val dur = item.optInt("duration_minutes", 3)
                val exCount = item.optJSONArray("exercises")?.length() ?: 3
                holder.b.tvLessonDuration.text = "⏱ $dur мин • $exCount упражнения"

                holder.itemView.setOnClickListener {
                    dialog.dismiss()
                    showLessonDetailDialog(item)
                }
            }
            override fun getItemCount() = lessons.size
        }

        dialogBinding.rvLessonsList.layoutManager = LinearLayoutManager(this)
        dialogBinding.rvLessonsList.adapter = LessonsAdapter()

        dialogBinding.btnCloseLessons.setOnClickListener {
            dialog.dismiss()
        }

        dialog.show()
    }

    private fun loadLessonsFromAssets(): List<JSONObject> {
        val result = mutableListOf<JSONObject>()
        try {
            val list = assets.list("lessons") ?: emptyArray()
            val sortedFiles = list.filter { it.endsWith(".json") }.sorted()
            for (filename in sortedFiles) {
                val stream = assets.open("lessons/$filename")
                val content = InputStreamReader(stream).readText()
                result.add(JSONObject(content))
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return result
    }

    private fun showLessonDetailDialog(lessonObj: JSONObject) {
        val dialog = BottomSheetDialog(this)
        val dialogBinding = DialogLessonDetailBinding.inflate(layoutInflater)
        dialog.setContentView(dialogBinding.root)

        dialogBinding.tvLessonDetailTitle.text = lessonObj.optString("title_ru", "Микроурок")
        dialogBinding.tvLessonDetailTopic.text = "Тема: " + lessonObj.optString("topic", "IT English")
        dialogBinding.tvLessonDetailRule.text = lessonObj.optString("rule_ru", "")

        // Render examples
        val examplesArr = lessonObj.optJSONArray("examples")
        dialogBinding.layoutLessonExamples.removeAllViews()
        if (examplesArr != null) {
            for (i in 0 until examplesArr.length()) {
                val exObj = examplesArr.getJSONObject(i)
                val en = exObj.optString("en", "")
                val ru = exObj.optString("ru", "")
                val tv = TextView(this).apply {
                    text = "• $en\n  $ru"
                    setTextColor(Color.parseColor("#E2E8F0"))
                    textSize = 13f
                    setPadding(8, 6, 8, 6)
                }
                dialogBinding.layoutLessonExamples.addView(tv)
            }
        }

        // Exercises flow
        val exercisesArr = lessonObj.optJSONArray("exercises") ?: JSONArray()
        var currentExIndex = 0

        fun bindExercise(index: Int) {
            if (index >= exercisesArr.length()) {
                dialogBinding.tvExerciseHeader.text = "🎉 Урок завершен!"
                dialogBinding.tvExercisePrompt.text = "Вы успешно выполнили все упражнения этого урока."
                dialogBinding.rgExerciseOptions.removeAllViews()
                dialogBinding.tvExerciseFeedback.visibility = View.GONE
                dialogBinding.btnSubmitExercise.text = "Вернуться к списку уроков"
                dialogBinding.btnSubmitExercise.setOnClickListener {
                    dialog.dismiss()
                    showLessonsDialog()
                }
                return
            }

            val ex = exercisesArr.getJSONObject(index)
            dialogBinding.tvExerciseHeader.text = "УПРАЖНЕНИЕ ${index + 1} ИЗ ${exercisesArr.length()}"
            dialogBinding.tvExercisePrompt.text = ex.optString("prompt", "")
            dialogBinding.tvExerciseFeedback.visibility = View.GONE
            dialogBinding.btnSubmitExercise.text = "Проверить ответ"

            dialogBinding.rgExerciseOptions.removeAllViews()
            val optionsArr = ex.optJSONArray("options")
            if (optionsArr != null) {
                for (optIdx in 0 until optionsArr.length()) {
                    val optText = optionsArr.getString(optIdx)
                    val rb = RadioButton(this).apply {
                        text = optText
                        setTextColor(Color.WHITE)
                        textSize = 14f
                        id = View.generateViewId()
                    }
                    dialogBinding.rgExerciseOptions.addView(rb)
                }
            }

            dialogBinding.btnSubmitExercise.setOnClickListener {
                val selectedId = dialogBinding.rgExerciseOptions.checkedRadioButtonId
                if (selectedId == -1) {
                    Toast.makeText(this@MainActivity, "Выберите вариант ответа", Toast.LENGTH_SHORT).show()
                    return@setOnClickListener
                }

                val selectedRb = dialogBinding.rgExerciseOptions.findViewById<RadioButton>(selectedId)
                val chosenAnswer = selectedRb?.text?.toString() ?: ""
                val correctAnswer = ex.optString("answer", "")
                val explanation = ex.optString("explanation", "")

                dialogBinding.tvExerciseFeedback.visibility = View.VISIBLE
                if (chosenAnswer.trim() == correctAnswer.trim()) {
                    dialogBinding.tvExerciseFeedback.text = "✅ Верно!\n$explanation"
                    dialogBinding.tvExerciseFeedback.setTextColor(Color.parseColor("#34D399"))
                } else {
                    dialogBinding.tvExerciseFeedback.text = "❌ Неверно. Правильный ответ: '$correctAnswer'\n$explanation"
                    dialogBinding.tvExerciseFeedback.setTextColor(Color.parseColor("#F87171"))
                }

                dialogBinding.btnSubmitExercise.text = if (index + 1 < exercisesArr.length()) "Следующее упражнение" else "Завершить урок"
                dialogBinding.btnSubmitExercise.setOnClickListener {
                    currentExIndex++
                    bindExercise(currentExIndex)
                }
            }
        }

        bindExercise(0)

        dialogBinding.btnBackFromLesson.setOnClickListener {
            dialog.dismiss()
        }

        dialog.show()
    }

    // =========================================================================
    // FEATURE 3: STATISTICS DIALOG
    // =========================================================================
    private fun showStatsDialog() {
        val dialog = BottomSheetDialog(this)
        val dialogBinding = DialogStatsBinding.inflate(layoutInflater)
        dialog.setContentView(dialogBinding.root)

        val allCards = repository.getAllCards()
        val (learned, hard, _) = progressManager.getCounts(allCards)

        dialogBinding.tvStatsTotalCards.text = "Всего карточек в базе: ${allCards.size}"
        dialogBinding.tvStatsLearned.text = "🟢 Изучено: $learned"
        dialogBinding.tvStatsHard.text = "🟡 На повторении: $hard"

        lifecycleScope.launch(Dispatchers.IO) {
            val now = System.currentTimeMillis()
            val due = db.practiceDao().countDuePractices(now)
            val totalReviews = db.reviewEventDao().countTotalReviews()
            val successfulReviews = db.reviewEventDao().countSuccessfulReviews()
            val rate = if (totalReviews > 0) ((successfulReviews * 100f) / totalReviews).toInt() else 0

            withContext(Dispatchers.Main) {
                dialogBinding.tvStatsDueToday.text = "🎯 К повторению сегодня: $due"
                dialogBinding.tvStatsTotalReviews.text = "Всего ответов зафиксировано: $totalReviews"
                dialogBinding.tvStatsSuccessRate.text = "Успешных ответов (Good/Easy): $rate%"
            }
        }

        dialogBinding.btnCloseStats.setOnClickListener { dialog.dismiss() }
        dialogBinding.btnDismissStats.setOnClickListener { dialog.dismiss() }
        dialog.show()
    }

    // =========================================================================
    // FEATURE 4: BACKUP & RESTORE
    // =========================================================================
    private fun showBackupDialog() {
        val dialog = BottomSheetDialog(this)
        val dialogBinding = DialogBackupBinding.inflate(layoutInflater)
        dialog.setContentView(dialogBinding.root)

        dialogBinding.btnExportData.setOnClickListener {
            lifecycleScope.launch(Dispatchers.IO) {
                val practices = db.practiceDao().getAll()
                val events = db.reviewEventDao().getRecentEvents(1000)

                val root = JSONObject().apply {
                    put("version", 2)
                    put("timestamp", System.currentTimeMillis())
                    val pArr = JSONArray()
                    for (p in practices) {
                        pArr.put(JSONObject().apply {
                            put("practiceId", p.practiceId)
                            put("cardId", p.cardId)
                            put("skill", p.skill)
                            put("state", p.state)
                            put("stability", p.stability)
                            put("difficulty", p.difficulty)
                            put("elapsedDays", p.elapsedDays)
                            put("scheduledDays", p.scheduledDays)
                            put("reps", p.reps)
                            put("lapses", p.lapses)
                            put("due", p.due)
                            put("lastReview", p.lastReview)
                        })
                    }
                    put("practices", pArr)

                    val eArr = JSONArray()
                    for (e in events) {
                        eArr.put(JSONObject().apply {
                            put("attemptId", e.attemptId)
                            put("practiceId", e.practiceId)
                            put("cardId", e.cardId)
                            put("skill", e.skill)
                            put("rating", e.rating)
                            put("reviewTime", e.reviewTime)
                            put("durationMs", e.durationMs)
                        })
                    }
                    put("events", eArr)
                }

                val jsonStr = root.toString()
                withContext(Dispatchers.Main) {
                    val clipboard = getSystemService(CLIPBOARD_SERVICE) as ClipboardManager
                    clipboard.setPrimaryClip(ClipData.newPlainText("EnglishCardsBackup", jsonStr))
                    dialogBinding.tvExportStatus.visibility = View.VISIBLE
                    dialogBinding.tvExportStatus.text = "✅ Скопировано в буфер обмена! (${practices.size} карточек, ${events.size} ответов)"
                    Toast.makeText(this@MainActivity, "Бэкап скопирован в буфер", Toast.LENGTH_SHORT).show()
                }
            }
        }

        dialogBinding.btnImportData.setOnClickListener {
            val input = dialogBinding.etImportJson.text?.toString()?.trim() ?: ""
            if (input.isEmpty()) {
                Toast.makeText(this, "Вставьте JSON для восстановления", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            try {
                val root = JSONObject(input)
                val pArr = root.optJSONArray("practices") ?: JSONArray()
                lifecycleScope.launch(Dispatchers.IO) {
                    val pList = mutableListOf<PracticeStateEntity>()
                    for (i in 0 until pArr.length()) {
                        val obj = pArr.getJSONObject(i)
                        pList.add(
                            PracticeStateEntity(
                                practiceId = obj.getString("practiceId"),
                                cardId = obj.getString("cardId"),
                                skill = obj.optString("skill", "en_to_ru"),
                                state = obj.optInt("state", 0),
                                stability = obj.optDouble("stability", 0.0),
                                difficulty = obj.optDouble("difficulty", 0.0),
                                elapsedDays = obj.optLong("elapsedDays", 0),
                                scheduledDays = obj.optLong("scheduledDays", 0),
                                reps = obj.optInt("reps", 0),
                                lapses = obj.optInt("lapses", 0),
                                due = obj.optLong("due", System.currentTimeMillis()),
                                lastReview = obj.optLong("lastReview", 0)
                            )
                        )
                    }
                    db.practiceDao().upsertAll(pList)
                    loadPracticeCache()
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@MainActivity, "Успешно восстановлено ${pList.size} карточек!", Toast.LENGTH_LONG).show()
                        dialog.dismiss()
                        refreshMenuStats()
                    }
                }
            } catch (e: Exception) {
                Toast.makeText(this, "Ошибка разбора JSON: ${e.message}", Toast.LENGTH_LONG).show()
            }
        }

        dialogBinding.btnCloseBackup.setOnClickListener { dialog.dismiss() }
        dialog.show()
    }

    private fun updateProgress(position: Int) {
        val total = currentCards.size
        val current = if (total > 0) position + 1 else 0
        binding.tvPlayerCardProgress.text = getString(R.string.card_progress_fmt, current, total)
        binding.playerProgressBar.max = if (total > 0) total else 1
        binding.playerProgressBar.progress = current
    }

    private fun updateDeckStats() {
        val (learned, hard, _) = progressManager.getCounts(currentCards)
        binding.tvPlayerDeckStats.text = "• 🟢 $learned  🟡 $hard"
    }

    private fun updateKeepScreenOn(keepOn: Boolean) {
        if (keepOn) {
            window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        } else {
            window.clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        }
    }

    override fun onPause() {
        super.onPause()
        audioController.pause()
        updateKeepScreenOn(false)
    }

    override fun onDestroy() {
        super.onDestroy()
        audioController.destroy()
    }
}
