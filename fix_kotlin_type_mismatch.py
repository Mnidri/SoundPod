import os

fp_vm = "app/src/main/kotlin/com/github/soundpod/viewmodels/home/QuickPicksViewModel.kt"
if not os.path.exists(fp_vm): fp_vm = "app/src/main/kotlin/com/github/musick/viewmodels/home/QuickPicksViewModel.kt"

if os.path.exists(fp_vm):
    with open(fp_vm, "r") as f: code_vm = f.read()
    
    start_marker = "val newReleasesDeferred = async"
    end_marker = "val relatedDeferreds = seedSongs.map"
    
    start_idx = code_vm.find(start_marker)
    end_idx = code_vm.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        before = code_vm[:start_idx]
        after = code_vm[end_idx:]
        
        # تعریف صریح نوع خروجی با async<Result<List<Innertube.SongItem>>?> تا کامپایلر حق حدس زدن و ساخت جعبه تو در تو نداشته باشه
        new_block = """val newReleasesDeferred = async<Result<List<Innertube.SongItem>>?> {
                    try {
                        val historySongs = runCatching { db.lastPlayed(50).first() }.getOrNull() ?: emptyList()
                        val historyArtists = historySongs.mapNotNull { it.artistsText?.split(",")?.firstOrNull()?.trim() }.filter { it.isNotBlank() }
                        val onboardedPref = appContext.getSharedPreferences("preferences", android.content.Context.MODE_PRIVATE).getString("onboardingSelectedArtists", "") ?: ""
                        val onboardedArtists = onboardedPref.split(",").filter { it.isNotBlank() }
                        val activeArtists = (historyArtists + onboardedArtists).distinct().take(4)
                        
                        var interleaved = emptyList<Innertube.SongItem>()
                        
                        if (activeArtists.isNotEmpty()) {
                            val fetchedSongLists = mutableListOf<List<Innertube.SongItem>>()
                            for (artist in activeArtists) {
                                val res = runCatching { Innertube.searchPage(query = "$artist latest single releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull() }.getOrNull()
                                res?.items?.filterIsInstance<Innertube.SongItem>()?.let { fetchedSongLists.add(it.take(3)) }
                            }
                            
                            val tempInterleaved = mutableListOf<Innertube.SongItem>()
                            val maxLen = fetchedSongLists.maxOfOrNull { it.size } ?: 0
                            for (i in 0 until maxLen) {
                                for (list in fetchedSongLists) {
                                    if (i < list.size) tempInterleaved.add(list[i])
                                }
                            }
                            interleaved = tempInterleaved.distinctBy { it.key }
                        }
                        
                        if (interleaved.isEmpty()) {
                            val fallbackRes = runCatching { Innertube.searchPage(query = "New Music Releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull() }.getOrNull()
                            interleaved = fallbackRes?.items?.filterIsInstance<Innertube.SongItem>() ?: seedSongs.shuffled().take(6).filterIsInstance<Innertube.SongItem>()
                        }
                        
                        Result.success(interleaved)
                    } catch (e: Exception) {
                        e.printStackTrace()
                        Result.success(seedSongs.shuffled().take(6).filterIsInstance<Innertube.SongItem>())
                    }
                }
                
                """
        with open(fp_vm, "w") as f: f.write(before + new_block + after)

print("Kotlin compiler tamed! No more nested Results.")
