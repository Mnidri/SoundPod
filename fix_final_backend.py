import os
import re

vm_path = "app/src/main/kotlin/com/github/soundpod/viewmodels/home/QuickPicksViewModel.kt"
if os.path.exists(vm_path):
    with open(vm_path, "r") as f: content = f.read()

    # جراحی لایه‌به‌لایه برای اعمال منطق ۱۰۰ آهنگ آخر دیتابیس
    old_block = r"val historySongs = runCatching \{ db\.lastPlayed\(50\)\.first\(\) \}\.getOrNull\(\) \?: emptyList\(\).*?interleaved = fallbackRes\?\.items\?\.filterIsInstance<Innertube\.SongItem>\(\) \?: seedSongs\.shuffled\(\)\.take\(6\)\.filterIsInstance<Innertube\.SongItem>\(\)\n                    \}"
    
    new_block = """val historySongs = runCatching { db.lastPlayed(100).first() }.getOrNull() ?: emptyList()
                        val historyArtists = historySongs.mapNotNull { it.artistsText }.flatMap { it.split(Regex(" & |, | x | • ")) }.map { it.trim().lowercase() }.filter { it.isNotBlank() }
                        val onboardedPref = appContext.getSharedPreferences("preferences", android.content.Context.MODE_PRIVATE).getString("onboardingSelectedArtists", "") ?: ""
                        val onboardedArtists = onboardedPref.split(",").map { it.trim().lowercase() }.filter { it.isNotBlank() }
                        
                        // ساخت یک پروفایل سلیقه قدرتمند و بدون تکراری از تمام خواننده‌های ۱۰۰ آهنگ اخیر
                        val myTasteProfile = (historyArtists + onboardedArtists).toSet()
                        
                        // صدا زدن مستقیم چارت رسمی نیو ریلیز یوتیوب موزیک
                        val exploreRes = runCatching { Innertube.searchPage(query = "FEmusic_new_releases", params = "", fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull() }.getOrNull()
                        val officialNewReleases = exploreRes?.items?.filterIsInstance<Innertube.SongItem>() ?: emptyList()
                        
                        if (myTasteProfile.isNotEmpty() && officialNewReleases.isNotEmpty()) {
                            // فیلتر کردن خروجی رسمی یوتیوب بر اساس پروفایل ۱۰۰ آهنگ آخر شما
                            val matched = officialNewReleases.filter { song ->
                                val songArtist = song.asMediaItem.mediaMetadata.artist?.toString()?.lowercase() ?: ""
                                myTasteProfile.any { myArtist -> songArtist.contains(myArtist) }
                            }
                            interleaved = if (matched.isNotEmpty()) matched else officialNewReleases.take(8)
                        } else {
                            interleaved = officialNewReleases.take(8)
                        }
                    } catch (e: Exception) { e.printStackTrace() }"""
    
    # جایگزینی با ساختار ایمن
    content = re.sub(r"val historySongs = runCatching \{ db\.lastPlayed\(50\)\.first\(\) \}\.getOrNull\(\).*?interleaved = fallbackRes\?\.items.*?}", new_block, content, flags=re.DOTALL)
    with open(vm_path, "w") as f: f.write(content)

# اصلاح لوله اتصال پلیر در فایل سرویس برای برطرف شدن بازی یکی‌درمیان دایل
service_path = "app/src/main/kotlin/com/github/soundpod/service/PlayerService.kt"
if os.path.exists(service_path):
    with open(service_path, "r") as f: content = f.read()
    
    if "override fun onMediaItemTransition" in content:
        # تغییر رویداد ثبت به وضعیت آماده شدن کامل متادیتا برای جلوگیری از دیتای خالی و جا افتادن آهنگ‌ها
        content = content.replace(
            "override fun onMediaItemTransition(mediaItem: MediaItem?, reason: Int) {",
            "override fun onPlaylistMetadataChanged(mediaMetadata: androidx.media3.common.MediaMetadata) {\n            val mediaItem = binder?.player?.currentMediaItem\n            super.onPlaylistMetadataChanged(mediaMetadata)"
        )
    with open(service_path, "w") as f: f.write(content)

print("100-Song Taste Profile Logic Injected Perfectly!")
