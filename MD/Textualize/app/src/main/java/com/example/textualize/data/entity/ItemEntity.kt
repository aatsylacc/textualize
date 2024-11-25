package com.example.textualize.data.entity

import android.os.Parcelable
import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey
import kotlinx.parcelize.Parcelize

@Entity
@Parcelize
data class ItemEntity(
    @PrimaryKey(autoGenerate = true)
    @ColumnInfo(name = "id")
    var id: Int = 0,

    @ColumnInfo(name = "title")
    var title: String,

    @ColumnInfo(name = "imageResult")
    var imageResult: String,

    @ColumnInfo(name = "descResult")
    var descResult: String,

    @ColumnInfo(name = "date")
    var date: String,

    ) : Parcelable