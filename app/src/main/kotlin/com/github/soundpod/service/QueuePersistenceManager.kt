package com.github.musick.service

import androidx.annotation.OptIn
import androidx.media3.common.C
import androidx.media3.common.Player
import androidx.media3.common.util.UnstableApi
import com.github.musick.db
import com.github.musick.models.QueuedMediaItem
import com.github.musick.query
import com.github.musick.utils.mediaItems
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class QueuePersistenceManager(
    private val player: Player,
    private val coroutineScope: CoroutineScope,
    private val onQueueRestored: () -> Unit
) {

    fun saveQueue(isEnabled: Boolean) {
        if (!isEnabled) return

        val mediaItems = player.currentTimeline.mediaItems
        val mediaItemIndex = player.currentMediaItemIndex
        val mediaItemPosition = player.currentPosition

        val queuedMediaItems = mediaItems.mapIndexed { index, mediaItem ->
            QueuedMediaItem(
                mediaItem = mediaItem,
                position = if (index == mediaItemIndex) mediaItemPosition else null
            )
        }

        query {
            db.clearQueue()
            db.insert(queuedMediaItems)
        }
    }

    @OptIn(UnstableApi::class)
    fun restoreQueue(isEnabled: Boolean) {
        if (!isEnabled) return

        query {
            val queuedSong = db.queue()
            db.clearQueue()

            if (queuedSong.isEmpty()) return@query

            val index = queuedSong.indexOfFirst { it.position != null }.coerceAtLeast(0)

            coroutineScope.launch(Dispatchers.Main) {
                player.setMediaItems(
                    queuedSong.map { mediaItem ->
                        mediaItem.mediaItem.buildUpon()
                            .setUri(mediaItem.mediaItem.mediaId)
                            .setCustomCacheKey(mediaItem.mediaItem.mediaId)
                            .build().apply {
                                mediaMetadata.extras?.putBoolean("isFromPersistentQueue", true)
                            }
                    },
                    index,
                    queuedSong[index].position ?: C.TIME_UNSET
                )
                player.prepare()
                onQueueRestored()
            }
        }
    }
}