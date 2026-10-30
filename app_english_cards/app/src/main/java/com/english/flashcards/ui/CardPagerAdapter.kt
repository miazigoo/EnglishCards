package com.english.flashcards.ui

import android.graphics.Color
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.RecyclerView
import com.english.flashcards.R
import com.english.flashcards.data.ProgressManager
import com.english.flashcards.databinding.ItemFlashcardBinding
import com.english.flashcards.model.CardStatus
import com.english.flashcards.model.Flashcard

class CardPagerAdapter(
    private var cards: List<Flashcard>,
    private val progressManager: ProgressManager,
    private val onCardClick: (Flashcard) -> Unit,
    private val onExampleClick: (Flashcard) -> Unit,
    private val onStatusChanged: (Flashcard, CardStatus) -> Unit
) : RecyclerView.Adapter<CardPagerAdapter.CardViewHolder>() {

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
        with(holder.binding) {
            tvWord.text = card.word
            tvIpa.text = card.ipa
            tvRuHint.text = "Примерно: ${card.transcriptionRu}"
            tvTranslation.text = card.cleanTranslation
            tvCategoryBadge.text = card.category
            tvCardId.text = String.format("#%04d", card.id)

            if (card.translation.isNotBlank() && card.translation != card.cleanTranslation) {
                tvCodeHint.visibility = android.view.View.VISIBLE
                tvCodeHint.text = card.translation
            } else {
                tvCodeHint.visibility = android.view.View.GONE
            }

            // Current status
            updateStatusBadge(this, progressManager.getStatus(card.id))

            // Replay tap
            cardInnerLayout.setOnClickListener {
                onCardClick(card)
            }

            // Show Code Example Modal
            btnShowExample.setOnClickListener {
                onExampleClick(card)
            }

            // Mark as Learned
            btnMarkLearned.setOnClickListener {
                val current = progressManager.getStatus(card.id)
                val newStatus = if (current == CardStatus.LEARNED) CardStatus.NEW else CardStatus.LEARNED
                progressManager.setStatus(card.id, newStatus)
                updateStatusBadge(this, newStatus)
                animateBadge(tvStatusBadge)
                onStatusChanged(card, newStatus)
            }

            // Mark as Hard / Needs review
            btnMarkHard.setOnClickListener {
                val current = progressManager.getStatus(card.id)
                val newStatus = if (current == CardStatus.HARD) CardStatus.NEW else CardStatus.HARD
                progressManager.setStatus(card.id, newStatus)
                updateStatusBadge(this, newStatus)
                animateBadge(tvStatusBadge)
                onStatusChanged(card, newStatus)
            }
        }
    }

    private fun updateStatusBadge(binding: ItemFlashcardBinding, status: CardStatus) {
        val ctx = binding.root.context
        when (status) {
            CardStatus.LEARNED -> {
                binding.tvStatusBadge.text = "🟢 Запомнил"
                binding.tvStatusBadge.background = ContextCompat.getDrawable(ctx, R.drawable.bg_badge_learned)
                binding.tvStatusBadge.setTextColor(Color.parseColor("#34D399"))
            }
            CardStatus.HARD -> {
                binding.tvStatusBadge.text = "🟡 Повторить"
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

    private fun animateBadge(view: android.view.View) {
        view.scaleX = 0.8f
        view.scaleY = 0.8f
        view.animate().scaleX(1.15f).scaleY(1.15f).setDuration(120).withEndAction {
            view.animate().scaleX(1.0f).scaleY(1.0f).setDuration(100).start()
        }.start()
    }

    override fun getItemCount(): Int = cards.size

    fun updateCards(newCards: List<Flashcard>) {
        cards = newCards
        notifyDataSetChanged()
    }

    fun getCard(position: Int): Flashcard? {
        return if (position in cards.indices) cards[position] else null
    }
}
