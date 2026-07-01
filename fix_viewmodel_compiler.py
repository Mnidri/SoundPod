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
        
        new_block = """val newReleasesDeferred = async {
                    val historySongs = runCatching { db.lastPlayed(50).first() }.getOrNull() ?: emptyList()
                    val historyArtists = historySongs.mapNotNull { it.artistsText?.split(",")?.firstOrNull()?.trim() }.filter { it.isNotBlank() }
                    
                    val onboardedPref = appContext.getSharedPreferences("preferences", android.content.Context.MODE_PRIVATE).getString("onboardingSelectedArtists", "") ?: ""
                    val onboardedArtists = onboardedPref.split(",").filter { it.isNotBlank() }
                    
                    val activeArtists = (historyArtists + onboardedArtists).distinct().take(6)
                    
                    if (activeArtists.isNotEmpty()) {
                        val fetchedSongLists = mutableListOf<List<Innertube.SongItem>>()
                        // استفاده از سرچ ایمن و تضمین‌شده
                        for (artist in activeArtists) {
                            val res = runCatching {
                                Innertube.searchPage(query = "$artist latest single releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()
                            }.getOrNull()
                            res?.items?.filterIsInstance<Innertube.SongItem>()?.let { fetchedSongLists.add(it.take(3)) }
                        }
                        
                        // ادغام دستی و امن لیست‌ها (یکی در میان) بدون نیاز به توابع جانبی
                        val interleaved = mutableListOf<Innertube.SongItem>()
                        val maxLen = fetchedSongLists.maxOfOrNull { it.size } ?: 0
                        for (i in 0 until maxLen) {
                            for (list in fetchedSongLists) {
                                if (i < list.size) interleaved.add(list[i])
                            }
                        }
                        
                        if (interleaved.isNotEmpty()) {
                            interleaved.distinctBy { it.key }
                        } else {
                            runCatching {
                                val searchResult = Innertube.searchPage(query = "New Music Releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()
                                searchResult?.items?.filterIsInstance<Innertube.SongItem>()
                            }.getOrNull()
                        }
                    } else {
                        runCatching {
                            val searchResult = Innertube.searchPage(query = "New Music Releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()
                            searchResult?.items?.filterIsInstance<Innertube.SongItem>()
                        }.getOrNull()
                    }
                }
                """
        with open(fp_vm, "w") as f: f.write(before + new_block + after)

print("ViewModel syntax patched securely!")
