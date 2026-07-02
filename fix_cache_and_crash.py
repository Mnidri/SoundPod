import os

# 1. دور زدن کش در ViewModel برای نمایش قطعی هیرو کارت و نیوریلیز
vm_path = "app/src/main/kotlin/com/github/soundpod/viewmodels/home/QuickPicksViewModel.kt"
if os.path.exists(vm_path):
    with open(vm_path, "r") as f: content = f.read()
    
    old_cache_logic = "if (!forceRefresh && cached != null && !ScreenCache.isExpired(PERSISTENT_CACHE_PREFIX + quickPicksSource.name, CACHE_EXPIRATION)) return"
    new_cache_logic = "// کش موقتاً برای تست ظاهر غیرفعال شد\n        // if (!forceRefresh && cached != null && !ScreenCache.isExpired(PERSISTENT_CACHE_PREFIX + quickPicksSource.name, CACHE_EXPIRATION)) return"
    
    if "// کش موقتاً" not in content:
        content = content.replace(old_cache_logic, new_cache_logic)
        with open(vm_path, "w") as f: f.write(content)

# 2. رفع کرش و منطق شیفت در QuickPicks
ui_path = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/QuickPicks.kt"
if os.path.exists(ui_path):
    with open(ui_path, "r") as f: content = f.read()
    
    # جایگزینی کل بلوک SpeedDial با یک منطق تمیز، بدون کرش و بدون دوگانگی
    old_speed_dial_block = """val speedDialItems = remember(recentHistory, related.songs, currentPlayingMediaItem) {
                val historyMocks = recentHistory.map { song -> FeedItemMock(id = song.id, title = song.title, subtitle = song.artistsText ?: "", thumbnailUrl = extractHighResUrlLocal(song.thumbnailUrl)) }
                val recommendedMocks = related.songs?.mapNotNull { song -> song.info?.endpoint?.videoId?.let { videoId -> FeedItemMock(id = videoId, title = song.info?.name.orEmpty(), subtitle = song.authors?.firstOrNull()?.name.orEmpty(), thumbnailUrl = extractHighResUrlLocal(song.thumbnail?.url)) } } ?: emptyList()
                val combined = (historyMocks + recommendedMocks).distinctBy { it.id }.toMutableList()
                
                // شیفت کردن هوشمند آهنگ در حال پخش به ایندکس ۰
                currentPlayingMediaItem?.let { currentItem ->
                     val playingId = currentItem.mediaId
                     val index = combined.indexOfFirst { it.id == playingId }
                     if (index != -1) {
                         val item = combined.removeAt(index)
                         combined.add(0, item)
                     } else {
                         val newItem = FeedItemMock(id = playingId, title = currentItem.mediaMetadata.title.toString(), subtitle = currentItem.mediaMetadata.artist.toString(), thumbnailUrl = extractHighResUrlLocal(currentItem.mediaMetadata.artworkUri?.toString()))
                         combined.add(0, newItem)
                     }
                }
                combined.take(24) // ریزش آهنگ ۲۵م
            }

            if (speedDialItems.isNotEmpty()) {
                SpeedDialGrid(
                    items = speedDialItems, 
                    onItemClick = { browseId -> 
                        val itemToPlay = speedDialItems.firstOrNull { it.id == browseId }
                        if (itemToPlay != null) {
                            val mediaItem = androidx.media3.common.MediaItem.Builder()
                                .setMediaId(itemToPlay.id)
                                .setMediaMetadata(androidx.media3.common.MediaMetadata.Builder().setTitle(itemToPlay.title).setArtist(itemToPlay.subtitle).setArtworkUri(android.net.Uri.parse(itemToPlay.thumbnailUrl)).build())
                                .build()
                            binder?.stopRadio()
                            binder?.player?.forcePlay(mediaItem)
                            binder?.setupRadio(NavigationEndpoint.Endpoint.Watch(videoId = mediaItem.mediaId))
                        }
                    }
                )
                Spacer(modifier = Modifier.height(16.dp))
            }"""
            
    new_speed_dial_block = """val speedDialItems = remember(recentHistory, related.songs, currentPlayingMediaItem) {
                val historyMocks = recentHistory.map { song -> FeedItemMock(id = song.id, title = song.title, subtitle = song.artistsText ?: "", thumbnailUrl = extractHighResUrlLocal(song.thumbnailUrl)) }
                val recommendedMocks = related.songs?.mapNotNull { song -> song.info?.endpoint?.videoId?.let { videoId -> FeedItemMock(id = videoId, title = song.info?.name.orEmpty(), subtitle = song.authors?.firstOrNull()?.name.orEmpty(), thumbnailUrl = extractHighResUrlLocal(song.thumbnail?.url)) } } ?: emptyList()
                val combined = (historyMocks + recommendedMocks).distinctBy { it.id }.toMutableList()
                
                // شیفت تمیز و بدون باگ با تکیه بر پلیر واقعی
                currentPlayingMediaItem?.let { currentItem ->
                     val playingId = currentItem.mediaId
                     val index = combined.indexOfFirst { it.id == playingId }
                     if (index != -1) {
                         val item = combined.removeAt(index)
                         combined.add(0, item)
                     }
                }
                combined.take(24)
            }

            if (speedDialItems.isNotEmpty()) {
                SpeedDialGrid(
                    items = speedDialItems, 
                    onItemClick = { browseId -> 
                        // جلوگیری از کرش: پیدا کردن دیتای کامل از دیتابیس یا سرور
                        val songFromDb = recentHistory.firstOrNull { it.id == browseId }
                        val songFromApi = related.songs?.firstOrNull { it.info?.endpoint?.videoId == browseId }
                        
                        val finalMediaItem = songFromApi?.asMediaItem ?: songFromDb?.asMediaItem
                        
                        if (finalMediaItem != null) {
                            binder?.stopRadio()
                            binder?.player?.forcePlay(finalMediaItem)
                            binder?.setupRadio(NavigationEndpoint.Endpoint.Watch(videoId = finalMediaItem.mediaId))
                        }
                    }
                )
                Spacer(modifier = Modifier.height(16.dp))
            }"""
            
    content = content.replace(old_speed_dial_block, new_speed_dial_block)
    with open(ui_path, "w") as f: f.write(content)

print("Cache bypassed & Speed Dial Crash Fixed!")
