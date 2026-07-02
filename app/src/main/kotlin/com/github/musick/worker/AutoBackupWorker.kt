package com.github.musick.worker

import android.content.Context
import androidx.core.net.toUri
import androidx.documentfile.provider.DocumentFile
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.github.musick.db
import com.github.musick.query
import com.github.musick.utils.autoBackupUriPrefKey
import com.github.musick.utils.preferences
import java.io.FileInputStream
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.Locale

class AutoBackupWorker(
    private val context: Context,
    workerParams: WorkerParameters
) : CoroutineWorker(context, workerParams) {

    override suspend fun doWork(): Result {
        val sharedPrefs = context.preferences
        val savedUriString = sharedPrefs.getString(autoBackupUriPrefKey, null) ?: return Result.failure()

        val treeUri = savedUriString.toUri()

        return try {
            val formatter = DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss", Locale.US)
            val dateString = LocalDateTime.now().format(formatter)
            val fileName = "Musick_Auto_$dateString.db"

            val pickedDir = DocumentFile.fromTreeUri(context, treeUri)
            val newFile = pickedDir?.createFile("application/vnd.sqlite3", fileName)
                ?: return Result.failure()

            val dbFile = context.getDatabasePath("data.db")
            query { db.checkpoint() }

            context.contentResolver.openOutputStream(newFile.uri)?.use { outputStream ->
                FileInputStream(dbFile).use { inputStream ->
                    inputStream.copyTo(outputStream)
                }
            }

            pickedDir.listFiles()
                .filter { it.name?.startsWith("Musick_Auto_") == true }
                .sortedByDescending { it.name }
                .drop(5)
                .forEach { oldFile ->
                    oldFile.delete()
                }

            Result.success()
        } catch (e: Exception) {
            e.printStackTrace()
            Result.failure()
        }
    }
}