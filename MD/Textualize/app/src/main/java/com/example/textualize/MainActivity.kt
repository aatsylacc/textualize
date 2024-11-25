package com.example.textualize

import android.Manifest
import android.content.ContentValues
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.view.View
import android.widget.Toast
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.core.content.ContextCompat
import androidx.core.content.FileProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.textualize.ResultActivity.Companion.EXTRA_IMAGE_URI
import com.example.textualize.ResultActivity.Companion.EXTRA_RESULT_TEXT
import com.example.textualize.data.entity.ItemEntity
import com.example.textualize.databinding.ActivityMainBinding
import com.google.android.material.bottomsheet.BottomSheetDialog
import com.google.mlkit.vision.common.InputImage
import com.google.mlkit.vision.text.TextRecognition
import com.google.mlkit.vision.text.latin.TextRecognizerOptions
import com.yalantis.ucrop.UCrop
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date

import java.util.Locale

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private var currentImageUri: Uri? = null
    private val viewModel by viewModels<ItemViewModel> { ViewModelFactory.getInstance(application) }
    private val timeStamp: String = SimpleDateFormat(FILENAME_FORMAT, Locale.US).format(Date())

    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        showToast(if (isGranted) "Izin diberikan" else "Izin ditolak")
    }

    private lateinit var adapter: ItemAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        if (!cameraPermissionsGranted()) requestPermissionLauncher.launch(REQUIRED_PERMISSION_CAMERA)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.rvItem.layoutManager = LinearLayoutManager(this)

        viewModel.getAllItem().observe(this) { item ->
            setItems(item)
            binding.tvEmpty.visibility = if (item.isEmpty()) View.VISIBLE else View.GONE
        }

        binding.addButton.setOnClickListener { showBottomSheet() }
    }

    private fun setItems(item: List<ItemEntity>) {
        adapter = ItemAdapter(viewModel, this@MainActivity)
        adapter.submitList(item.reversed())
        binding.rvItem.adapter = adapter
    }

    private fun showBottomSheet() {
        val dialogView = layoutInflater.inflate(R.layout.bottomsheet, null)
        val dialog = BottomSheetDialog(this).apply {
            setContentView(dialogView)
            show()
        }
        dialogView.findViewById<View>(R.id.galleryGroup).setOnClickListener {
            startGallery()
            dialog.dismiss()
        }
        dialogView.findViewById<View>(R.id.cameraGroup).setOnClickListener {
            startCamera()
            dialog.dismiss()
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        when {
            resultCode == RESULT_OK && requestCode == UCrop.REQUEST_CROP -> {
                currentImageUri = data?.let { UCrop.getOutput(it) }
                currentImageUri?.let { analyzeImage(it) }
            }
            resultCode == UCrop.RESULT_ERROR -> {
                val cropError = UCrop.getError(data!!)
                showToast(cropError.toString())
            }
        }
    }

    private fun openCropActivity(inputUri: Uri?) {
        val outputUri = getImageUri(this)
        val options = UCrop.Options().apply { setFreeStyleCropEnabled(true) }

        UCrop.of(inputUri!!, outputUri)
            .withMaxResultSize(1920, 1080)
            .withAspectRatio(1f, 1f)
            .withOptions(options)
            .start(this)
    }

    private fun cameraPermissionsGranted() =
        ContextCompat.checkSelfPermission(this, REQUIRED_PERMISSION_CAMERA) == PackageManager.PERMISSION_GRANTED

    private fun startGallery() {
        launcherGallery.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
    }

    private val launcherGallery = registerForActivityResult(
        ActivityResultContracts.PickVisualMedia()
    ) { uri ->
        if (uri != null) {
            currentImageUri = uri
            openCropActivity(currentImageUri)
        } else {
            showToast("Tidak ada gambar yang dipilih")
        }
    }

    private fun startCamera() {
        currentImageUri = getImageUri(this)
        currentImageUri?.let { launcherIntentCamera.launch(it) }
    }

    private val launcherIntentCamera = registerForActivityResult(
        ActivityResultContracts.TakePicture()
    ) { isSuccess ->
        if (isSuccess) openCropActivity(currentImageUri)
    }

    private fun analyzeImage(uri: Uri) {
        binding.progressIndicator.visibility = View.VISIBLE

        val textRecognizer = TextRecognition.getClient(TextRecognizerOptions.DEFAULT_OPTIONS)
        val inputImage = InputImage.fromFilePath(this, uri)
        textRecognizer.process(inputImage)
            .addOnSuccessListener { visionText ->
                binding.progressIndicator.visibility = View.GONE
                if (visionText.text.isNotBlank()) {
                    val intent = Intent(this, ResultActivity::class.java).apply {
                        putExtra(EXTRA_IMAGE_URI, currentImageUri.toString())
                        addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION)
                        putExtra(EXTRA_RESULT_TEXT, visionText.text)
                    }
                    startActivity(intent)
                } else {
                    showToast("Tidak ada teks terbaca")
                }
            }
            .addOnFailureListener {
                binding.progressIndicator.visibility = View.GONE
                showToast(it.message.toString())
            }
    }

    private fun getImageUri(context: Context): Uri {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            val timeStamp = SimpleDateFormat(FILENAME_FORMAT, Locale.US).format(Date())
            val contentValues = ContentValues().apply {
                put(MediaStore.MediaColumns.DISPLAY_NAME, "$timeStamp.jpg")
                put(MediaStore.MediaColumns.MIME_TYPE, "image/jpeg")
                put(MediaStore.MediaColumns.RELATIVE_PATH, "Pictures/MyCamera/")
            }
            context.contentResolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, contentValues)
                ?: getImageUriForPreQ(context)
        } else {
            getImageUriForPreQ(context)
        }
    }

    private fun getImageUriForPreQ(context: Context): Uri {
        val timeStamp = SimpleDateFormat(FILENAME_FORMAT, Locale.US).format(Date())
        val filesDir = context.getExternalFilesDir(Environment.DIRECTORY_PICTURES)
        val imageFile = File(filesDir, "/MyCamera/$timeStamp.jpg").apply {
            parentFile?.takeIf { !it.exists() }?.mkdirs()
        }
        return FileProvider.getUriForFile(context, "${BuildConfig.APPLICATION_ID}.provider", imageFile)
    }

    private fun showToast(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }

    companion object {
        private const val FILENAME_FORMAT = "yyyyMMdd_HHmmss"
        private const val REQUIRED_PERMISSION_CAMERA = Manifest.permission.CAMERA
    }
}
