package com.example.textualize.data.room

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.example.textualize.data.entity.ItemEntity


@Database(entities = [ItemEntity::class], version = 1, exportSchema = false)
abstract class ItemDatabase : RoomDatabase() {
    abstract fun ItemDao(): ItemDao

    companion object {
        @Volatile
        private var instance: ItemDatabase? = null
        fun getInstance(context: Context): ItemDatabase {
            if (instance == null) {
                synchronized(ItemDatabase::class.java) {
                    instance = Room.databaseBuilder(
                        context.applicationContext,
                        ItemDatabase::class.java, "item_db"
                    )
                        .build()
                }
            }
            return instance as ItemDatabase
        }
    }

}