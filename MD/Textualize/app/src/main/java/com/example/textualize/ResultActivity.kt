package com.example.textualize

import android.net.Uri
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Toast
import androidx.activity.viewModels
import androidx.core.widget.doOnTextChanged
import com.bumptech.glide.Glide
import com.example.textualize.data.entity.ItemEntity

import com.example.textualize.databinding.ActivityResultBinding
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale


class ResultActivity : AppCompatActivity() {

    private lateinit var binding: ActivityResultBinding
    private lateinit var title: String
    private var isEdit = false
    private var currentImage: Uri? = null

    private val viewModel by viewModels<ItemViewModel> {
        ViewModelFactory.getInstance(application)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityResultBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val resultText = intent.getStringExtra(EXTRA_RESULT_TEXT) ?: ""
        val imageUri = intent.getStringExtra(EXTRA_IMAGE_URI)?.let { Uri.parse(it) }
        currentImage = imageUri

        binding.edDesc.setText(resultText)
        binding.previewImage.setImageURI(imageUri)

        setupView()

        val itemId = intent.getIntExtra(EXTRA_ID, 0)
        if (itemId != 0) {
            isEdit = true
            viewModel.getItem(itemId).observe(this) { item ->
                setItem(item)
            }
        }

        setupAction(itemId)
    }

    private fun setItem(item: ItemEntity) {
        with(binding) {
            edTitle.setText(item.title)
            edDesc.setText(item.descResult)
            currentImage = Uri.parse(item.imageResult)

            Glide.with(this@ResultActivity)
                .load(currentImage)
                .into(previewImage)
        }
    }

    private fun setupView() {
        binding.edTitle.apply {
            error = "Judul tidak boleh kosong"
            doOnTextChanged { text, _, _, _ ->
                if (text.isNullOrEmpty()) {
                    error = "Judul tidak boleh kosong"
                    binding.btnSave.isEnabled = false
                } else {
                    error = null
                    binding.btnSave.isEnabled = true
                }
            }
        }

        binding.edDesc.doOnTextChanged { text, _, _, _ ->
            if (text.isNullOrEmpty()) {
                binding.edTitle.error = "Deskripsi tidak boleh kosong"
                binding.btnSave.isEnabled = false
            } else {
                binding.edTitle.error = null
                binding.btnSave.isEnabled = true
            }
        }
    }

    private fun setupAction(itemId: Int) {
        binding.btnSave.setOnClickListener {
            title = binding.edTitle.text.toString()
            val date = getCurrentDate()

            if (isEdit) {
                val item = ItemEntity(
                    id = itemId,
                    title = title,
                    imageResult = currentImage.toString(),
                    descResult = binding.edDesc.text.toString(),
                    date = date
                )
                viewModel.update(item)
            } else {
                val item = ItemEntity(
                    id = 0,
                    title = title,
                    imageResult = currentImage.toString(),
                    descResult = binding.edDesc.text.toString(),
                    date = date
                )
                viewModel.insert(item)
            }

            showToast("Berhasil disimpan")
            finish()
        }
    }

    private fun getCurrentDate(): String {
        val dateFormat = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault())
        return dateFormat.format(Date())
    }

    private fun showToast(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }

    companion object {
        const val EXTRA_IMAGE_URI = "extra_image_uri"
        const val EXTRA_RESULT_TEXT = "extra_result_text"
        const val EXTRA_ID = "extra_id"
    }
}
