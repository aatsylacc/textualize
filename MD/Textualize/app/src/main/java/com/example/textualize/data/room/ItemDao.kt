package com.example.textualize.data.room

import androidx.lifecycle.LiveData
import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.example.textualize.data.entity.ItemEntity


@Dao
interface ItemDao {
    @Insert(onConflict = OnConflictStrategy.IGNORE)
    fun insert(item: ItemEntity)

    @Update
    fun update(item: ItemEntity)

    @Delete
    fun delete(item: ItemEntity)

    @Query("SELECT * FROM ItemEntity WHERE id = :id")
    fun getItem(id: Int): LiveData<ItemEntity>

    @Query("SELECT * from ItemEntity")
    fun getAllItem(): LiveData<List<ItemEntity>>
}