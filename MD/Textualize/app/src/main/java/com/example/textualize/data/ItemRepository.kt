package com.example.textualize.data

import android.app.Application
import androidx.lifecycle.LiveData
import com.example.textualize.data.entity.ItemEntity
import com.example.textualize.data.room.ItemDao
import com.example.textualize.data.room.ItemDatabase
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

class ItemRepository(application: Application) {
    private val mItemDao: ItemDao
    private val executorService: ExecutorService = Executors.newSingleThreadExecutor()

    init {
        val db = ItemDatabase.getInstance(application)
        mItemDao = db.ItemDao()
    }

    fun insert(item: ItemEntity) {
        executorService.execute { mItemDao.insert(item) }
    }

    fun delete(item: ItemEntity) {
        executorService.execute { mItemDao.delete(item) }
    }

    fun update(item: ItemEntity) {
        executorService.execute { mItemDao.update(item) }
    }

    fun getItem(id: Int):
            LiveData<ItemEntity> = mItemDao.getItem(id)

    fun getAllItem(): LiveData<List<ItemEntity>> = mItemDao.getAllItem()

}