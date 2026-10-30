package com.english.flashcards

import android.animation.ValueAnimator
import android.os.Bundle
import android.view.View
import android.view.WindowManager
import android.view.animation.AccelerateDecelerateInterpolator
import android.widget.Toast
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity
import androidx.core.animation.doOnEnd
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.viewpager2.widget.ViewPager2
import com.english.flashcards.audio.AudioController
import com.english.flashcards.data.FlashcardRepository
import com.english.flashcards.data.ProgressManager
import com.english.flashcards.databinding.ActivityMainBinding
import com.english.flashcards.model.Flashcard
import com.english.flashcards.ui.CardPagerAdapter
import com.english.flashcards.ui.CategoryItem
import com.english.flashcards.ui.CategoryMenuAdapter
import android.content.ClipData
import android.content.ClipboardManager
import com.english.flashcards.databinding.DialogCardExampleBinding
import com.google.android.material.bottomsheet.BottomSheetDialog
import com.google.android.material.dialog.MaterialAlertDialogBuilder

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var repository: FlashcardRepository
    private lateinit var progressManager: ProgressManager
    private lateinit var cardAdapter: CardPagerAdapter
    private lateinit var audioController: AudioController
    private lateinit var menuAdapter: CategoryMenuAdapter

    private var currentCards: List<Flashcard> = emptyList()
    private var selectedCategory: String = "Все карточки"
    private var repeatCount: Int = 2
    private var isSplashActive: Boolean = true

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        repository = FlashcardRepository(this)
        progressManager = ProgressManager(this)

        setupAudioController()
        setupViewPager()
        setupMenu()
        setupPlayerControls()
        setupBackNavigation()
        startSplashAnimation()
    }

    private fun startSplashAnimation() {
        isSplashActive = true
        binding.layoutSplash.visibility = View.VISIBLE
        binding.layoutSplash.alpha = 1f
        binding.layoutMenu.visibility = View.GONE
        binding.layoutPlayer.visibility = View.GONE

        // Animated logo pulse
        binding.ivSplashLogo.scaleX = 0.85f
        binding.ivSplashLogo.scaleY = 0.85f
        binding.ivSplashLogo.animate()
            .scaleX(1.05f)
            .scaleY(1.05f)
            .setDuration(1200)
            .setInterpolator(AccelerateDecelerateInterpolator())
            .start()

        val animator = ValueAnimator.ofInt(0, 100)
        animator.duration = 1500
        animator.interpolator = AccelerateDecelerateInterpolator()

        animator.addUpdateListener { anim ->
            val progress = anim.animatedValue as Int
            binding.pbSplashLoading.progress = progress
            binding.tvSplashPercent.text = "$progress%"

            binding.tvSplashStatus.text = when {
                progress < 30 -> "Инициализация аудио-ядра..."
                progress < 70 -> "Загрузка IT словаря (1529 слов)..."
                progress < 95 -> "Синхронизация прогресса..."
                else -> "Все готово!"
            }
        }

        animator.doOnEnd {
            isSplashActive = false
            refreshMenuStats()

            // Smooth cross-fade into Main Menu
            binding.layoutMenu.alpha = 0f
            binding.layoutMenu.visibility = View.VISIBLE
            binding.layoutMenu.animate().alpha(1f).setDuration(400).start()

            binding.layoutSplash.animate()
                .alpha(0f)
                .setDuration(400)
                .withEndAction {
                    binding.layoutSplash.visibility = View.GONE
                }
                .start()
        }

        animator.start()
    }

    private fun setupMenu() {
        // Featured All Cards
        val allCatName = repository.getCategories().firstOrNull() ?: "Все карточки"
        binding.btnFeaturedAll.setOnClickListener {
            openPlayerWithCategory(allCatName)
        }
        binding.btnStartAll.setOnClickListener {
            openPlayerWithCategory(allCatName)
        }

        // Featured Hard / Needs Review Card
        val onHardClick = View.OnClickListener {
            openPlayerWithHardCards()
        }
        binding.btnFeaturedHard.setOnClickListener(onHardClick)
        binding.btnStartHard.setOnClickListener(onHardClick)

        // Menu repeat toggle
        binding.btnMenuRepeatCount.text = "${repeatCount}x (повтор)"
        binding.btnMenuRepeatCount.setOnClickListener {
            toggleRepeatCount()
            binding.btnMenuRepeatCount.text = "${repeatCount}x (повтор)"
        }

        // Build category items
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

        if (::menuAdapter.isInitialized) {
            menuAdapter.updateItems(buildCategoryItems())
        }
    }

    private fun getEmojiForCategory(cat: String): String {
        return when {
            cat.contains("IT") -> "💻"
            cat.contains("MES") -> "🏭"
            cat.contains("PLC") -> "⚙️"
            cat.contains("Быт") -> "✈️"
            cat.contains("Общение") -> "💬"
            cat.contains("глаголы") && !cat.contains("Фразовые") -> "🏃"
            cat.contains("Прилагательные") -> "✨"
            cat.contains("Работа") -> "💼"
            cat.contains("Фразовые") -> "🔄"
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
            onCardClick = { card ->
                audioController.playCard(card, restartRepetitions = true)
            },
            onExampleClick = { card ->
                showExampleBottomSheet(card)
            },
            onStatusChanged = { _, _ ->
                updateDeckStats()
                refreshMenuStats()
            }
        )

        binding.vpCards.adapter = cardAdapter
        binding.vpCards.registerOnPageChangeCallback(object : ViewPager2.OnPageChangeCallback() {
            override fun onPageSelected(position: Int) {
                super.onPageSelected(position)
                updateProgress(position)
                val card = cardAdapter.getCard(position)
                if (card != null && audioController.isAutoPlay()) {
                    audioController.playCard(card, restartRepetitions = true)
                }
            }
        })
    }

    private fun setupPlayerControls() {
        binding.btnBackToMenu.setOnClickListener {
            returnToMenu()
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

    private fun openPlayerWithCategory(categoryName: String) {
        selectedCategory = categoryName
        currentCards = repository.getCardsByCategory(selectedCategory)

        binding.btnPlayerCategory.text = if (selectedCategory.startsWith("Все")) "Все ▾" else "$selectedCategory ▾"
        binding.btnPlayerRepeatCount.text = "${repeatCount}x"

        cardAdapter.updateCards(currentCards)
        binding.vpCards.setCurrentItem(0, false)
        updateProgress(0)
        updateDeckStats()

        // Switch visible view
        binding.layoutMenu.visibility = View.GONE
        binding.layoutPlayer.visibility = View.VISIBLE

        // Start playback
        if (currentCards.isNotEmpty()) {
            audioController.setAutoPlay(true)
            binding.vpCards.post {
                audioController.playCard(currentCards[0], restartRepetitions = true)
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

        selectedCategory = "🔥 На повторение"
        currentCards = hardCards

        binding.btnPlayerCategory.text = "Повтор ▾"
        binding.btnPlayerRepeatCount.text = "${repeatCount}x"

        cardAdapter.updateCards(currentCards)
        binding.vpCards.setCurrentItem(0, false)
        updateProgress(0)
        updateDeckStats()

        // Switch visible view
        binding.layoutMenu.visibility = View.GONE
        binding.layoutPlayer.visibility = View.VISIBLE

        // Start playback
        if (currentCards.isNotEmpty()) {
            audioController.setAutoPlay(true)
            binding.vpCards.post {
                audioController.playCard(currentCards[0], restartRepetitions = true)
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
            .setTitle("Выберите тему карточек")
            .setSingleChoiceItems(displayItems, selectedIndex) { dialog, which ->
                val chosenCategory = categoryOptions[which].first
                if (chosenCategory == "🔥 На повторение") {
                    openPlayerWithHardCards()
                } else {
                    openPlayerWithCategory(chosenCategory)
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

        val codeSnippet = if (card.example.isNotBlank()) {
            card.example
        } else {
            "# Пример использования для ${card.word}\n# ${card.cleanTranslation}"
        }
        dialogBinding.tvExampleCode.text = codeSnippet

        val noteText = if (card.exampleNote.isNotBlank()) {
            card.exampleNote
        } else {
            card.translation
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
            .setTitle("🎉 Колода завершена!")
            .setMessage("Вы успешно прослушали и повторили все слова из раздела «$selectedCategory».")
            .setPositiveButton("Повторить сначала") { _, _ ->
                binding.vpCards.setCurrentItem(0, true)
                if (currentCards.isNotEmpty()) {
                    audioController.playCard(currentCards[0], restartRepetitions = true)
                }
            }
            .setNeutralButton("В меню тем") { _, _ ->
                returnToMenu()
            }
            .setCancelable(false)
            .show()
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
