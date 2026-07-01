@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class, androidx.compose.animation.ExperimentalAnimationApi::class, androidx.compose.material3.ExperimentalMaterial3Api::class)
package com.github.musick.ui.screens.home

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Shadow
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.lifecycle.viewmodel.compose.viewModel
import com.github.musick.ui.components.HorizontalTabs
import com.github.musick.enums.BuiltInPlaylist
import com.github.musick.ui.navigation.Routes
import com.github.musick.ui.screens.favorites.FavoritesScreen
import com.github.musick.viewmodels.home.HomeViewModel

@Composable
fun HomeScreen(navController: NavController, onSettingsClick: () -> Unit) {
    val homeViewModel: HomeViewModel = viewModel()
    val pagerState = rememberPagerState(initialPage = 0) { homeViewModel.tabs.size }
    val navigateToAlbum = { browseId: String -> navController.navigate(route = Routes.Album(id = browseId)) }
    val navigateToArtist = { browseId: String -> navController.navigate(route = Routes.Artist(id = browseId)) }
    val bgColor = MaterialTheme.colorScheme.background
    val textColor = MaterialTheme.colorScheme.onBackground

    Scaffold(
        containerColor = bgColor,
        topBar = {
            TopAppBar(
                title = { 
                    Text(
                        text = "Musick", 
                        fontSize = 36.sp, 
                        fontWeight = FontWeight.Bold, 
                        fontFamily = FontFamily.Serif, 
                        letterSpacing = (-1).sp, 
                        color = textColor,
                        style = androidx.compose.ui.text.TextStyle(
                            shadow = androidx.compose.ui.graphics.Shadow(
                                color = textColor.copy(alpha = 0.5f), 
                                blurRadius = 24f
                            )
                        )
                    ) 
                },
                actions = {
                    IconButton(onClick = { navController.navigate(route = Routes.Search) }) {
                        Icon(imageVector = Icons.Default.Search, contentDescription = "Search", tint = textColor)
                    }
                    Spacer(modifier = Modifier.width(4.dp))
                    OutlinedIconButton(onClick = onSettingsClick, border = BorderStroke(1.dp, textColor.copy(alpha = 0.15f))) {
                        Icon(imageVector = Icons.Default.Settings, contentDescription = "Settings", tint = textColor)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = bgColor)
            )
        }
    ) { paddingValues ->
        Box(modifier = Modifier.fillMaxSize().padding(paddingValues)) {
            Column(modifier = Modifier.fillMaxSize()) {
                HorizontalTabs(pagerState = pagerState, tabs = homeViewModel.tabs)
                HorizontalPager(state = pagerState, beyondViewportPageCount = 4, modifier = Modifier.weight(1f).background(Color.Transparent)) { page ->
                    when (page) {
                        0 -> QuickPicks(onAlbumClick = navigateToAlbum, onArtistClick = navigateToArtist, onPlaylistClick = { browseId -> navController.navigate(route = Routes.Playlist(id = browseId)) }, onOfflinePlaylistClick = { navController.navigate(route = Routes.BuiltInPlaylist(index = 1)) })
                        1 -> FavoritesScreen(onFavoriteTracksClick = { navController.navigate(route = Routes.FavoriteTracks) }, onGoToAlbum = navigateToAlbum, onGoToArtist = navigateToArtist, isEmbedded = true)
                        2 -> HomeSongs(onGoToAlbum = navigateToAlbum, onGoToArtist = navigateToArtist)
                        3 -> HomeArtistList(onArtistClick = { artist -> navigateToArtist(artist.id) })
                        4 -> HomeAlbums(onAlbumClick = { album -> navigateToAlbum(album.id) })
                        5 -> HomePlaylists(onBuiltInPlaylist = { playlistIndex -> if (playlistIndex == BuiltInPlaylist.Favorites.ordinal) navController.navigate(route = Routes.Favorites) else navController.navigate(route = Routes.BuiltInPlaylist(index = playlistIndex)) }, onPlaylistClick = { playlist -> navController.navigate(route = Routes.LocalPlaylist(id = playlist.id)) })
                    }
                }
            }
        }
    }
}
