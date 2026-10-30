package com.english.flashcards.ui

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.english.flashcards.databinding.ItemMenuCategoryBinding

data class CategoryItem(
    val name: String,
    val count: Int,
    val emoji: String,
    val learnedCount: Int = 0,
    val hardCount: Int = 0,
    val newCount: Int = 0
) {
    val percent: Int
        get() = if (count > 0) ((learnedCount * 100f) / count).toInt() else 0
}

class CategoryMenuAdapter(
    private var items: List<CategoryItem>,
    private val onCategoryClick: (CategoryItem) -> Unit
) : RecyclerView.Adapter<CategoryMenuAdapter.ViewHolder>() {

    inner class ViewHolder(val binding: ItemMenuCategoryBinding) :
        RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = ItemMenuCategoryBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return ViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val item = items[position]
        with(holder.binding) {
            tvCategoryEmoji.text = item.emoji
            tvCategoryTitle.text = item.name
            tvCategoryWordCount.text = "${item.count} слов • 🟢 ${item.learnedCount}  🟡 ${item.hardCount}  ⚪ ${item.newCount}"
            tvCategoryPercent.text = "${item.percent}%"
            pbCategoryProgress.progress = item.percent

            categoryItemContainer.setOnClickListener {
                onCategoryClick(item)
            }
        }
    }

    override fun getItemCount(): Int = items.size

    fun updateItems(newItems: List<CategoryItem>) {
        items = newItems
        notifyDataSetChanged()
    }
}
