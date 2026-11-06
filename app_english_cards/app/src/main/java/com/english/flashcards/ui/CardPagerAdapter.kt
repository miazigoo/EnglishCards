package com.english.flashcards.ui

import android.graphics.Color
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.RecyclerView
import com.english.flashcards.R
import com.english.flashcards.data.ProgressManager
import com.english.flashcards.databinding.ItemFlashcardBinding
import com.english.flashcards.fsrs.FSRSCard
import com.english.flashcards.fsrs.FSRSScheduler
import com.english.flashcards.fsrs.Rating
import com.english.flashcards.model.CardStatus
import com.english.flashcards.model.Flashcard

class CardPagerAdapter(
    private var cards: List<Flashcard>,
    private val progressManager: ProgressManager,
    private val fsrsScheduler: FSRSScheduler,
    private val onCardClick: (Flashcard) -> Unit,
    private val onExampleClick: (Flashcard) -> Unit,
    private val onPlayTerm: (Flashcard) -> Unit,
    private val onPlayExample: (Flashcard) -> Unit,
    private val onRatingSelected: (Flashcard, Rating) -> Unit,
    private val getPracticeState: (cardId: String) -> FSRSCard?
) : RecyclerView.Adapter<CardPagerAdapter.CardViewHolder>() {

    private val revealedCardIds = mutableSetOf<String>()
    private var defaultRevealed: Boolean = false

    inner class CardViewHolder(val binding: ItemFlashcardBinding) :
        RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CardViewHolder {
        val binding = ItemFlashcardBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return CardViewHolder(binding)
    }

    override fun onBindViewHolder(holder: CardViewHolder, position: Int) {
        val card = cards[position]
        val cardKey = card.cardId.ifEmpty { "legacy.${card.id}" }
        val isRevealed = defaultRevealed || revealedCardIds.contains(cardKey)

        with(holder.binding) {
            tvWord.text = card.word

            val cleanIpa = card.ipa.trim().takeIf { it.isNotEmpty() && !it.equals("null", ignoreCase = true) } ?: ""
            val cleanRuHint = card.transcriptionRu.trim().takeIf { it.isNotEmpty() && !it.equals("null", ignoreCase = true) } ?: ""

            tvIpa.text = cleanIpa
            tvIpa.visibility = if (cleanIpa.isNotEmpty()) View.VISIBLE else View.GONE

            tvRuHint.text = if (cleanRuHint.isNotEmpty()) "Примерно: $cleanRuHint" else ""
            tvRuHint.visibility = if (cleanRuHint.isNotEmpty()) View.VISIBLE else View.GONE

            tvTranslation.text = card.cleanTranslation
            tvCategoryBadge.text = card.category
            tvCardId.text = String.format("#%04d", card.id)

            // Name breakdown if available (e.g. for rsplit: right + split)
            if (!card.nameBreakdown.isNullOrBlank() && !card.nameBreakdown.equals("null", ignoreCase = true)) {
                tvBreakdown.visibility = View.VISIBLE
                tvBreakdown.text = card.nameBreakdown
            } else {
                tvBreakdown.visibility = View.GONE
            }

            // The restored Anki TSV contains word/translation pairs, not examples.
            val hasRealExample = card.example.isNotBlank() &&
                !card.example.equals("null", ignoreCase = true) &&
                !(card.example == card.word && card.primaryExampleRu == card.cleanTranslation)
            btnPlayExample.visibility = if (hasRealExample) View.VISIBLE else View.GONE
            btnShowExample.visibility = if (hasRealExample || !card.technicalCode.isNullOrBlank()) View.VISIBLE else View.GONE
            if (hasRealExample) {
                layoutExampleBox.visibility = View.VISIBLE
                tvExampleEn.text = card.example
                val exRu = (card.primaryExampleRu.takeIf { it.isNotBlank() && !it.equals("null", ignoreCase = true) }
                    ?: card.exampleNote.takeIf { it.isNotBlank() && !it.equals("null", ignoreCase = true) }
                    ?: "").trim()
                tvExampleRu.text = exRu
                tvExampleRu.visibility = if (exRu.isNotEmpty()) View.VISIBLE else View.GONE
            } else {
                layoutExampleBox.visibility = View.GONE
            }

            // Active Recall UI State
            if (isRevealed) {
                btnRevealAnswer.visibility = View.GONE
                layoutAnswerRevealed.visibility = View.VISIBLE
                layoutRatingButtons.visibility = View.GONE // Browsing never changes spaced-repetition progress.

                // Calculate FSRS interval previews
                val fsrsCard = getPracticeState(cardKey) ?: FSRSCard(
                    practiceId = "$cardKey.en_to_ru",
                    cardId = cardKey,
                    skill = "en_to_ru"
                )
                val previews = fsrsScheduler.preview(fsrsCard)
                tvIntervalAgain.text = previews[Rating.AGAIN]?.intervalText ?: "< 1м"
                tvIntervalHard.text = previews[Rating.HARD]?.intervalText ?: "5м"
                tvIntervalGood.text = previews[Rating.GOOD]?.intervalText ?: "10м"
                tvIntervalEasy.text = previews[Rating.EASY]?.intervalText ?: "3д"
            } else {
                btnRevealAnswer.visibility = View.VISIBLE
                layoutAnswerRevealed.visibility = View.GONE
                layoutRatingButtons.visibility = View.GONE
            }

            // Reveal button action
            btnRevealAnswer.setOnClickListener {
                revealedCardIds.add(cardKey)
                notifyItemChanged(position)
                onPlayTerm(card)
            }

            // Card body tap -> replay sound
            cardInnerLayout.setOnClickListener {
                onCardClick(card)
            }

            // Audio control buttons
            btnQuickAudio.setOnClickListener {
                onPlayTerm(card)
            }
            btnPlayTerm.setOnClickListener {
                onPlayTerm(card)
            }
            btnPlayExample.setOnClickListener {
                onPlayExample(card)
            }

            // Code details modal
            btnShowExample.setOnClickListener {
                onExampleClick(card)
            }

            // 4 FSRS Rating buttons
            btnAgain.setOnClickListener {
                onRatingSelected(card, Rating.AGAIN)
            }
            btnHard.setOnClickListener {
                onRatingSelected(card, Rating.HARD)
            }
            btnGood.setOnClickListener {
                onRatingSelected(card, Rating.GOOD)
            }
            btnEasy.setOnClickListener {
                onRatingSelected(card, Rating.EASY)
            }

            // Memory status badge
            updateStatusBadge(this, progressManager.getStatus(card.id))
        }
    }

    private fun updateStatusBadge(binding: ItemFlashcardBinding, status: CardStatus) {
        val ctx = binding.root.context
        when (status) {
            CardStatus.LEARNED -> {
                binding.tvStatusBadge.text = "🟢 Изучено"
                binding.tvStatusBadge.background = ContextCompat.getDrawable(ctx, R.drawable.bg_badge_learned)
                binding.tvStatusBadge.setTextColor(Color.parseColor("#34D399"))
            }
            CardStatus.HARD -> {
                binding.tvStatusBadge.text = "🟡 На повторении"
                binding.tvStatusBadge.background = ContextCompat.getDrawable(ctx, R.drawable.bg_badge_hard)
                binding.tvStatusBadge.setTextColor(Color.parseColor("#FBBF24"))
            }
            CardStatus.NEW -> {
                binding.tvStatusBadge.text = "⚪ Новое"
                binding.tvStatusBadge.background = ContextCompat.getDrawable(ctx, R.drawable.bg_badge_new)
                binding.tvStatusBadge.setTextColor(Color.parseColor("#94A3B8"))
            }
        }
    }

    override fun getItemCount(): Int = cards.size

    fun updateCards(newCards: List<Flashcard>) {
        cards = newCards
        notifyDataSetChanged()
    }

    fun getCard(position: Int): Flashcard? {
        return if (position in cards.indices) cards[position] else null
    }

    fun setDefaultRevealed(revealed: Boolean) {
        defaultRevealed = revealed
        if (revealed) {
            revealAll()
        } else {
            resetRevealed()
        }
    }

    fun revealAll() {
        for (c in cards) {
            revealedCardIds.add(c.cardId.ifEmpty { "legacy.${c.id}" })
        }
        notifyDataSetChanged()
    }

    fun resetRevealed() {
        revealedCardIds.clear()
        notifyDataSetChanged()
    }
}
