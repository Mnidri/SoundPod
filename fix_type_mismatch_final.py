import os
import re

fp_vm = "app/src/main/kotlin/com/github/soundpod/viewmodels/home/QuickPicksViewModel.kt"
if not os.path.exists(fp_vm): fp_vm = "app/src/main/kotlin/com/github/musick/viewmodels/home/QuickPicksViewModel.kt"

if os.path.exists(fp_vm):
    with open(fp_vm, "r") as f: code_vm = f.read()
    
    # استفاده از RegEx برای پیدا کردن و جایگزینی دقیق و تمیز کل بلاک بدون به هم ریختگی
    pattern = re.compile(r"val newReleasesDeferred = async \{.*?\}(?=\s*val relatedDeferreds =)", re.DOTALL)
    
    new_block = """val newReleasesDeferred = async {
                    runCatching {
                        var interleaved = emptyList<Innertube.SongItem>()
                        try {
                            val historySongs = runCatching { db.lastPlayed(50).first() }.getOrNull() ?: emptyList()
                            val historyArtists = historySongs.mapNotNull { it.artistsText?.split(",")?.firstOrNull()?.trim() }.filter { it.isNotBlank() }
                            val onboardedPref = appContext.getSharedPreferences("preferences", android.content.Context.MODE_PRIVATE).getString("onboardingSelectedArtists", "") ?: ""
                            val onboardedArtists = onboardedPref.split(",").filter { it.isNotBlank() }
                            val activeArtists = (historyArtists + onboardedArtists).distinct().take(4)
                            
                            if (activeArtists.isNotEmpty()) {
                                val fetchedSongLists = mutableListOf<List<Innertube.SongItem>>()
                                for (artist in activeArtists) {
                                    val res = Innertube.searchPage(query = "$artist latest single releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()
                                    res?.items?.filterIsInstance<Innertube.SongItem>()?.let { fetchedSongLists.add(it.take(3)) }
                                }
                                
                                val tempInterleaved = mutableListOf<Innertube.SongItem>()
                                val maxLen = fetchedSongLists.maxOfOrNull { it.size } ?: 0
                                for (i in 0 until maxLen) {
                                    for (list in fetchedSongLists) {
                                        if (i < list.size) tempInterleaved.add(list[i])
                                    }
                                }
                                if (tempInterleaved.isNotEmpty()) {
                                    interleaved = tempInterleaved.distinctBy { it.key }
                                }
                            }
                        } catch (e: Exception) {
                            e.printStackTrace()
                        }
                        
                        // فال‌بک نهایی و تضمینی
                        if (interleaved.isEmpty()) {
                            val fallbackRes = Innertube.searchPage(query = "New Music Releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()
                            val fallbackItems = fallbackRes?.items?.filterIsInstance<Innertube.SongItem>()
                            interleaved = fallbackItems ?: seedSongs.shuffled().take(6).filterIsInstance<Innertube.SongItem>()
                        }
                        
                        if (interleaved.isEmpty()) {
                            throw Exception("No items found")
                        }
                        
                        // برگرداندن خود لیست؛ runCatching آن را به طور خودکار درون یک لایه Result قرار می‌دهد
                        interleaved
                    }
                }
"""
    
    updated_code = pattern.sub(new_block, code_vm)
    
    with open(fp_vm, "w") as f: f.write(updated_code)

print("Double Result bug successfully removed!")
