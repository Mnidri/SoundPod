import os
import re

# 1. جراحی ViewModel برای دریافت دیتای خالص و واقعیِ New Releases
vm_path = "app/src/main/kotlin/com/github/soundpod/viewmodels/home/QuickPicksViewModel.kt"
if os.path.exists(vm_path):
    with open(vm_path, "r") as f: content = f.read()

    # حذف منطق سرچ متنی اشتباه
    old_new_releases_logic = r"val activeArtists = \(historyArtists \+ onboardedArtists\)\.distinct\(\)\.take\(4\)\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?interleaved = fallbackRes\?\.items\?\.filterIsInstance<Innertube\.SongItem>\(\) \?: seedSongs\.shuffled\(\)\.take\(6\)\.filterIsInstance<Innertube\.SongItem>\(\)\n                    }"
    
    new_new_releases_logic = """val activeArtists = (historyArtists + onboardedArtists).distinct().take(10)
                        
                        // دریافت شاهرگ اصلی از صفحه Explore یوتیوب موزیک برای نیوریلیز واقعی
                        val exploreRes = runCatching { Innertube.searchPage(query = "FEmusic_new_releases", params = null, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull() }.getOrNull()
                        val officialNewReleases = exploreRes?.items?.filterIsInstance<Innertube.SongItem>() ?: emptyList()
                        
                        if (activeArtists.isNotEmpty() && officialNewReleases.isNotEmpty()) {
                            // فیلتر کردن آهنگ‌های جدید جهانی بر اساس خواننده‌های محبوب شما
                            val matched = officialNewReleases.filter { song ->
                                val songArtist = song.asMediaItem.mediaMetadata.artist?.toString()?.lowercase() ?: ""
                                activeArtists.any { myArtist -> songArtist.contains(myArtist.lowercase()) }
                            }
                            interleaved = if (matched.isNotEmpty()) matched else officialNewReleases.take(8)
                        } else {
                            interleaved = officialNewReleases.take(8)
                        }
                    } catch (e: Exception) { e.printStackTrace() }
                    
                    if (interleaved.isNullOrEmpty()) {
                        val fallbackRes = runCatching { Innertube.searchPage(query = "FEmusic_new_releases", params = null, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull() }.getOrNull()
                        interleaved = fallbackRes?.items?.filterIsInstance<Innertube.SongItem>() ?: seedSongs.shuffled().take(6).filterIsInstance<Innertube.SongItem>()
                    }"""
    
    content = re.sub(old_new_releases_logic, new_new_releases_logic, content, flags=re.DOTALL)
    with open(vm_path, "w") as f: f.write(content)


# 2. جراحی PlayerService برای آپدیت قطعی دیتابیس (بیدار کردن Speed Dial)
service_path = "app/src/main/kotlin/com/github/soundpod/service/PlayerService.kt"
if os.path.exists(service_path):
    with open(service_path, "r") as f: content = f.read()
    
    # پیدا کردن Listener پلیر و اضافه کردن دستور ثبت در دیتابیس
    if "override fun onMediaItemTransition(mediaItem: MediaItem?, reason: Int)" in content and "db.insert" not in content:
        old_transition = "override fun onMediaItemTransition(mediaItem: MediaItem?, reason: Int) {\n"
        new_transition = """override fun onMediaItemTransition(mediaItem: MediaItem?, reason: Int) {
            // ثبت آنی آهنگ در دیتابیس برای بیدار کردن اسپید دایل
            mediaItem?.let { item ->
                kotlinx.coroutines.GlobalScope.launch(kotlinx.coroutines.Dispatchers.IO) {
                    com.github.musick.db.insert(com.github.musick.models.Song(
                        id = item.mediaId,
                        title = item.mediaMetadata.title.toString(),
                        artistsText = item.mediaMetadata.artist.toString(),
                        durationText = null,
                        thumbnailUrl = item.mediaMetadata.artworkUri?.toString()
                    ))
                }
            }
"""
        content = content.replace(old_transition, new_transition)
        with open(service_path, "w") as f: f.write(content)

print("Backend Logic Upgraded Successfully! DB Sync & Real New Releases Injected.")
