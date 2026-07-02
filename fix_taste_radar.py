import os
import re

vm_path = "app/src/main/kotlin/com/github/soundpod/viewmodels/home/QuickPicksViewModel.kt"
if os.path.exists(vm_path):
    with open(vm_path, "r") as f: content = f.read()

    # جراحی کامل بخش نیو ریلیز و پیاده‌سازی منطق شکار آهنگ‌های جدید روز بر اساس دیتابیس کاربر
    old_block_pattern = r"val historySongs = runCatching \{ db\.lastPlayed\(50\)\.first\(\) \}\.getOrNull\(\).*?interleaved = fallbackRes\?\.items\?\.filterIsInstance<Innertube\.SongItem>\(\) \?: seedSongs\.shuffled\(\)\.take\(6\)\.filterIsInstance<Innertube\.SongItem>\(\)\n                    \}"
    
    # ساخت متنی که کاملاً با ساختار کاتلین و متغیرهای فایل شما همخوانی دارد
    replacement_logic = """val historySongs = runCatching { db.lastPlayed(100).first() }.getOrNull() ?: emptyList()
                        val historyArtists = historySongs.mapNotNull { it.artistsText }.flatMap { it.split(Regex(" & |, | x | • ")) }.map { it.trim().lowercase() }.filter { it.isNotBlank() }
                        val onboardedPref = appContext.getSharedPreferences("preferences", android.content.Context.MODE_PRIVATE).getString("onboardingSelectedArtists", "") ?: ""
                        val onboardedArtists = onboardedPref.split(",").map { it.trim().lowercase() }.filter { it.isNotBlank() }
                        
                        // ۱. ساخت پروفایل سلیقه کاربر از روی دیتابیس (سرچ‌ها و پخش‌های اخیر)
                        val myLovedArtists = (historyArtists + onboardedArtists).toSet()
                        
                        // ۲. دریافت لیست ۱۰۰ آهنگ جدید و رسمی روز دنیا از یوتیوب موزیک
                        val exploreRes = runCatching { Innertube.searchPage(query = "FEmusic_new_releases", params = "", fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull() }.getOrNull()
                        val globalNewReleases = exploreRes?.items?.filterIsInstance<Innertube.SongItem>() ?: emptyList()
                        
                        if (myLovedArtists.isNotEmpty() && globalNewReleases.isNotEmpty()) {
                            // ۳. تقاطع دادن: اگر آهنگ جدیدی مال خواننده‌های محبوب کاربر بود، گلچینش کن
                            val filteredSongs = globalNewReleases.filter { song ->
                                val songArtist = song.asMediaItem.mediaMetadata.artist?.toString()?.lowercase() ?: ""
                                myLovedArtists.any { beloved -> songArtist.contains(beloved) }
                            }
                            // اگر آهنگی مچ شد میاورد، در غیر این صورت برای خالی نماندن صفحه ۸ تا از جدیدترین‌های جهانی را نشان می‌دهد
                            interleaved = if (filteredSongs.isNotEmpty()) filteredSongs else globalNewReleases.take(8)
                        } else {
                            interleaved = globalNewReleases.take(8)
                        }
                    } catch (e: Exception) { e.printStackTrace() }"""

    # جایگزینی منطق جدید با متد منعطف regex برای جلوگیری از ارور کامپایلر
    content = re.sub(r"val historySongs = runCatching \{ db\.lastPlayed.*?.await\(\)\?\.let \{ Result\.success\(it\) \}", replacement_logic, content, flags=re.DOTALL)
    
    # اصلاح خط آخر ست کردن مقدار برای کامپایل بدون ارور
    content = content.replace("newReleasesResult = newReleasesDeferred.await()?.let { Result.success(it) }", "newReleasesResult = interleaved?.let { Result.success(it) }")

    with open(vm_path, "w") as f: f.write(content)

print("Taste Radar Logic Injected into ViewModel Successfully!")
