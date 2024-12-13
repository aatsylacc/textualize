# Textualize

Textualize is an Android-based application that leverages Machine Learning and Cloud Computing technologies to extract text from images, making it easy to edit, copy, and manage.

---

## Key Features

1. *Text Recognition from Images*: Uses ML Kit to recognize text from images.
2. *Image Processing*: Allows users to capture or select images from the gallery and crop them before analysis.
3. *Accessible Text Results*:
   - Editable text output.
   - Copy text to the clipboard for use in other applications.
4. *User-Friendly Interface*: A clean and intuitive design.
5. *Offline Mode*: Text processing is done entirely on-device.

---

## Technology Stack

### Android Stack
- *Programming Language*: Kotlin
- *Framework*: Android Jetpack (ViewModel, LiveData, RecyclerView)
- *Libraries*:
  - [Material Design](https://material.io/develop/android) for UI components.
  - [UCrop](https://github.com/Yalantis/uCrop) for image cropping.
  - [Glide](https://github.com/bumptech/glide) for image loading.

### Machine Learning Stack
- *ML Kit*: Google ML Kit for OCR-based Text Recognition.

### Cloud Computing Stack
- *Google Cloud Storage*: To store images (optional if needed).
- *Custom API* (if applicable): Hosting APIs for additional features such as text backup to the cloud.

---

## How the App Works

1. *Capture Image*:
   - Select an image from the gallery or capture one using the camera.
2. *Crop Image*:
   - Adjust the area of the image using the crop feature (UCrop).
3. *Process Text*:
   - The image is processed using ML Kit to detect text.
4. *Display and Save Results*:
   - The recognized text is displayed and can be copied to the clipboard or saved.

---

## Dependencies

Below is the list of libraries used in the app:

```gradle
dependencies {
    implementation "com.github.yalantis:ucrop:2.2.8" // UCrop for image cropping
    implementation "com.google.mlkit:text-recognition:16.0.0" // ML Kit for OCR
    implementation "com.github.bumptech.glide:glide:4.16.0" // Glide for image loading
    implementation "androidx.lifecycle:lifecycle-viewmodel-ktx:2.7.0" // ViewModel
    implementation "androidx.lifecycle:lifecycle-livedata-ktx:2.7.0" // LiveData
    implementation "org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3" // Coroutine
    implementation "com.google.android.material:material:1.11.0" // Material Design
}