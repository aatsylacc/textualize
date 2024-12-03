package com.example.textualize

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.util.Log
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.appcompat.app.AlertDialog
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.textualize.ResultActivity.Companion.EXTRA_ID
import com.example.textualize.data.entity.ItemEntity
import com.example.textualize.databinding.ItemsBinding

class ItemAdapter(private val viewModel: ItemViewModel, private val context: Context) :  ListAdapter<ItemEntity, ItemAdapter.MyViewHolder>(DIFF_CALLBACK) {
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MyViewHolder {
        val binding = ItemsBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return MyViewHolder(binding, viewModel, context )
    }

    override fun onBindViewHolder(holder: MyViewHolder, position: Int) {
        val item = getItem(position)
        holder.bind(item)
    }

    class MyViewHolder
        (private val binding: ItemsBinding,
         private val viewModel: ItemViewModel,
         private val context: Context)
        : RecyclerView.ViewHolder(binding.root) {
        fun bind(item: ItemEntity) {
            binding.tvItemName.text =  item.title
            binding.tvItemDesc.text = item.descResult
            binding.tvItemTime.text = item.date
            val imageUri = Uri.parse(item.imageResult)
            Log.d("myviewholder", "bind: ${item.imageResult}")
            Glide.with(itemView.context)
                .load(imageUri)
                .into(binding.ivPhoto)

            binding.btnDelete.setOnClickListener {
                val alertDialogBuilder = AlertDialog.Builder(context)
                alertDialogBuilder.apply {
                    setTitle("Peringatan!")
                    setMessage("Apakah anda yakin ingin menghapus ini?")
                    setPositiveButton("Ya") { dialog, _ ->
                        viewModel.delete(item)
                        dialog.dismiss()
                    }
                    setNegativeButton("Tidak"){ dialog,_ ->
                        dialog.dismiss()
                    }
                    create()
                    show()
                }
            }

            itemView.setOnClickListener{
                val intent = Intent(itemView.context, ResultActivity::class.java)
                intent.putExtra(EXTRA_ID,item.id)
                itemView.context.startActivity(intent)
            }
        }
    }

    companion object {
        val DIFF_CALLBACK = object : DiffUtil.ItemCallback<ItemEntity>() {
            override fun areItemsTheSame(oldItem: ItemEntity, newItem: ItemEntity): Boolean {
                return oldItem.id == newItem.id
            }

            override fun areContentsTheSame(oldItem: ItemEntity, newItem: ItemEntity): Boolean {
                return oldItem.id == newItem.id
            }
        }
    }

}