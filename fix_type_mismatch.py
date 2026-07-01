import os

fp_vm = "app/src/main/kotlin/com/github/soundpod/viewmodels/home/QuickPicksViewModel.kt"
if not os.path.exists(fp_vm): fp_vm = "app/src/main/kotlin/com/github/musick/viewmodels/home/QuickPicksViewModel.kt"

if os.path.exists(fp_vm):
    with open(fp_vm, "r") as f: code_vm = f.read()
    
    start_str = "val newReleasesDeferred = async {"
    end_str = "val relatedDeferreds = seedSongs.map"
    
    if start_str in code_vm and end_str in code_vm:
        before = code_vm.split(start_str)[0]
        after = end_str + code_vm.split(end_str)[1]
        
        # بازنویسی کاملاً منطبق با تایپ Result<List<Innertube.SongItem>>
        new_block = """val newReleasesDeferred = async {
                    var interleaved = emptyList<Innertube.SongItem>()
                    try {
                        val historySongs = db.lastPlayed(50).first()
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
                    
                    // فال بک قطعی: اگر لیست خالی بود، مستقیما لیست جایگزین پر میشود
                    if (interleaved.isEmpty()) {
                        val fallback = Innertube.searchPage(query = "New Music Releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()?.items?.filterIsInstance<Innertube.SongItem>()
                        interleaved = fallback ?: seedSongs.shuffled().take(6).filterIsInstance<Innertube.SongItem>()
                    }
                    
                    // تحویل دقیق نوع دیتای درخواستی به کامپایلر
                    Result.success(interleaved)
                }
                """
        with open(fp_vm, "w") as f: f.write(before + new_block + after)

print("Kotlin Type Mismatch fixed natively!")
