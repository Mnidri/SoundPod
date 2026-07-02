import os

# پیدا کردن مسیر درست پوشه‌ها
base_dir = "app/src/main/kotlin/com/github/soundpod"
if not os.path.exists(base_dir):
    base_dir = "app/src/main/kotlin/com/github/musick"

auth_dir = os.path.join(base_dir, "ui/screens/auth")
os.makedirs(auth_dir, exist_ok=True)
auth_file = os.path.join(auth_dir, "AuthScreen.kt")
home_file = os.path.join(base_dir, "ui/screens/home/HomeScreen.kt")

# پکیج‌نیم قطعی و ثابت (Musick)
pkg = "com.github.musick"

code_auth = f"""package {pkg}.ui.screens.auth

import android.widget.Toast
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.ArrowBack
import androidx.compose.material.icons.rounded.Email
import androidx.compose.material.icons.rounded.ImageSearch
import androidx.compose.material.icons.rounded.Lock
import androidx.compose.material.icons.rounded.Person
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AuthScreen(onBack: () -> Unit) {{
    val bgColor = MaterialTheme.colorScheme.background
    val textColor = MaterialTheme.colorScheme.onBackground
    val primaryColor = MaterialTheme.colorScheme.primary
    val context = LocalContext.current
    
    var isLoginMode by remember {{ mutableStateOf(true) }}
    var username by remember {{ mutableStateOf("") }}
    var email by remember {{ mutableStateOf("") }}
    var password by remember {{ mutableStateOf("") }}

    Scaffold(
        containerColor = bgColor,
        topBar = {{
            TopAppBar(
                title = {{ }},
                navigationIcon = {{
                    IconButton(onClick = onBack) {{
                        Icon(Icons.Rounded.ArrowBack, contentDescription = "Back", tint = textColor)
                    }}
                }},
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
        }}
    ) {{ paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(horizontal = 24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {{
            Spacer(modifier = Modifier.height(20.dp))
            
            Text(
                text = "Musick",
                fontSize = 48.sp,
                fontWeight = FontWeight.ExtraBold,
                fontFamily = FontFamily.Serif,
                letterSpacing = (-1.5).sp,
                color = textColor,
                style = TextStyle(shadow = androidx.compose.ui.graphics.Shadow(color = textColor.copy(alpha = 0.5f), blurRadius = 24f))
            )
            
            Spacer(modifier = Modifier.height(32.dp))
            
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(52.dp)
                    .clip(RoundedCornerShape(50))
                    .background(textColor.copy(alpha = 0.05f))
                    .padding(4.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {{
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxHeight()
                        .clip(RoundedCornerShape(50))
                        .background(if (isLoginMode) textColor.copy(alpha = 0.1f) else Color.Transparent)
                        .clickable {{ isLoginMode = true }},
                    contentAlignment = Alignment.Center
                ) {{
                    Text("Log In", fontWeight = FontWeight.Bold, color = if (isLoginMode) textColor else textColor.copy(alpha = 0.5f))
                }}
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxHeight()
                        .clip(RoundedCornerShape(50))
                        .background(if (!isLoginMode) textColor.copy(alpha = 0.1f) else Color.Transparent)
                        .clickable {{ isLoginMode = false }},
                    contentAlignment = Alignment.Center
                ) {{
                    Text("Sign Up", fontWeight = FontWeight.Bold, color = if (!isLoginMode) textColor else textColor.copy(alpha = 0.5f))
                }}
            }}
            
            Spacer(modifier = Modifier.height(32.dp))
            
            Column(modifier = Modifier.fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally) {{
                AnimatedVisibility(visible = !isLoginMode) {{
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {{
                        Box(
                            modifier = Modifier
                                .size(90.dp)
                                .clip(CircleShape)
                                .background(textColor.copy(alpha = 0.05f))
                                .border(1.dp, textColor.copy(alpha = 0.2f), CircleShape)
                                .clickable {{ Toast.makeText(context, "Gallery opened", Toast.LENGTH_SHORT).show() }},
                            contentAlignment = Alignment.Center
                        ) {{
                            Icon(Icons.Rounded.ImageSearch, contentDescription = null, tint = textColor.copy(alpha = 0.6f), modifier = Modifier.size(28.dp))
                        }}
                        Spacer(modifier = Modifier.height(24.dp))
                    }}
                }}
                
                AnimatedVisibility(visible = !isLoginMode) {{
                    Column {{
                        OutlinedTextField(
                            value = username,
                            onValueChange = {{ username = it }},
                            placeholder = {{ Text("Username") }},
                            leadingIcon = {{ Icon(Icons.Rounded.Person, contentDescription = null, tint = textColor.copy(alpha = 0.5f)) }},
                            modifier = Modifier.fillMaxWidth(),
                            singleLine = true,
                            shape = RoundedCornerShape(16.dp),
                            colors = OutlinedTextFieldDefaults.colors(unfocusedBorderColor = textColor.copy(alpha = 0.1f))
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                    }}
                }}
                
                OutlinedTextField(
                    value = email,
                    onValueChange = {{ email = it }},
                    placeholder = {{ Text("Email Address") }},
                    leadingIcon = {{ Icon(Icons.Rounded.Email, contentDescription = null, tint = textColor.copy(alpha = 0.5f)) }},
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    shape = RoundedCornerShape(16.dp),
                    colors = OutlinedTextFieldDefaults.colors(unfocusedBorderColor = textColor.copy(alpha = 0.1f))
                )
                
                Spacer(modifier = Modifier.height(16.dp))
                
                OutlinedTextField(
                    value = password,
                    onValueChange = {{ password = it }},
                    placeholder = {{ Text("Password") }},
                    leadingIcon = {{ Icon(Icons.Rounded.Lock, contentDescription = null, tint = textColor.copy(alpha = 0.5f)) }},
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    visualTransformation = PasswordVisualTransformation(),
                    shape = RoundedCornerShape(16.dp),
                    colors = OutlinedTextFieldDefaults.colors(unfocusedBorderColor = textColor.copy(alpha = 0.1f))
                )
                
                Spacer(modifier = Modifier.height(32.dp))
                
                Button(
                    onClick = {{ 
                        Toast.makeText(context, if (isLoginMode) "Logging in..." else "Creating account...", Toast.LENGTH_SHORT).show()
                        onBack()
                    }},
                    modifier = Modifier.fillMaxWidth().height(54.dp),
                    shape = RoundedCornerShape(50),
                    colors = ButtonDefaults.buttonColors(containerColor = primaryColor)
                ) {{
                    Text(if (isLoginMode) "Log In" else "Create Account", fontWeight = FontWeight.Bold, fontSize = 16.sp)
                }}
                
                Spacer(modifier = Modifier.height(32.dp))
                
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {{
                    Divider(modifier = Modifier.weight(1f), color = textColor.copy(alpha = 0.1f))
                    Text(" OR ", color = textColor.copy(alpha = 0.4f), fontSize = 12.sp, modifier = Modifier.padding(horizontal = 16.dp))
                    Divider(modifier = Modifier.weight(1f), color = textColor.copy(alpha = 0.1f))
                }}
                
                Spacer(modifier = Modifier.height(32.dp))
                
                Card(
                    modifier = Modifier.fillMaxWidth().height(54.dp).clickable {{ Toast.makeText(context, "Google Auth Started", Toast.LENGTH_SHORT).show() }},
                    shape = RoundedCornerShape(50),
                    colors = CardDefaults.cardColors(containerColor = Color.Transparent),
                    border = BorderStroke(1.dp, textColor.copy(alpha = 0.2f))
                ) {{
                    Row(modifier = Modifier.fillMaxSize(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.Center) {{
                        Text("G", fontWeight = FontWeight.ExtraBold, fontSize = 20.sp, color = textColor)
                        Spacer(modifier = Modifier.width(12.dp))
                        Text("Continue with Google", fontWeight = FontWeight.Bold, fontSize = 15.sp, color = textColor)
                    }}
                }}
            }}
        }}
    }}
}}
"""
with open(auth_file, "w") as f: f.write(code_auth)


code_home = f"""@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class, androidx.compose.animation.ExperimentalAnimationApi::class, androidx.compose.material3.ExperimentalMaterial3Api::class)
package {pkg}.ui.screens.home

import android.widget.Toast
import androidx.compose.animation.*
import androidx.compose.animation.core.tween
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.rounded.AccountCircle
import androidx.compose.material.icons.rounded.ChevronRight
import androidx.compose.material.icons.rounded.Person
import androidx.compose.material.icons.rounded.Settings
import androidx.compose.material.icons.rounded.Star
import androidx.compose.material.icons.rounded.Translate
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.TransformOrigin
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.lifecycle.viewmodel.compose.viewModel
import {pkg}.ui.components.HorizontalTabs
import {pkg}.enums.BuiltInPlaylist
import {pkg}.ui.navigation.Routes
import {pkg}.ui.screens.favorites.FavoritesScreen
import {pkg}.ui.screens.auth.AuthScreen
import {pkg}.viewmodels.home.HomeViewModel

@Composable
fun HomeScreen(navController: NavController, onSettingsClick: () -> Unit) {{
    val homeViewModel: HomeViewModel = viewModel()
    val pagerState = rememberPagerState(initialPage = 0) {{ homeViewModel.tabs.size }}
    val navigateToAlbum = {{ browseId: String -> navController.navigate(route = Routes.Album(id = browseId)) }}
    val navigateToArtist = {{ browseId: String -> navController.navigate(route = Routes.Artist(id = browseId)) }}
    
    val bgColor = MaterialTheme.colorScheme.background
    val textColor = MaterialTheme.colorScheme.onBackground
    val context = LocalContext.current
    
    var showProfileOverlay by remember {{ mutableStateOf(false) }}
    var showAuthScreen by remember {{ mutableStateOf(false) }}
    var expandedSection by remember {{ mutableStateOf<String?>(null) }}
    var aiTranslationEnabled by remember {{ mutableStateOf(false) }}
    var apiToken by remember {{ mutableStateOf("") }}

    AnimatedContent(targetState = showAuthScreen, transitionSpec = {{ fadeIn() with fadeOut() }}) {{ isAuth ->
        if (isAuth) {{
            AuthScreen(onBack = {{ showAuthScreen = false }})
        }} else {{
            Box(modifier = Modifier.fillMaxSize()) {{
                Scaffold(
                    containerColor = bgColor,
                    topBar = {{
                        TopAppBar(
                            title = {{
                                Text(
                                    text = "Musick",
                                    fontSize = 44.sp,
                                    fontWeight = FontWeight.ExtraBold,
                                    fontFamily = FontFamily.Serif,
                                    letterSpacing = (-1.5).sp,
                                    color = textColor,
                                    style = TextStyle(shadow = androidx.compose.ui.graphics.Shadow(color = textColor.copy(alpha = 0.4f), blurRadius = 20f))
                                )
                            }},
                            actions = {{
                                IconButton(onClick = {{ navController.navigate(route = Routes.Search) }}) {{
                                    Icon(imageVector = Icons.Default.Search, contentDescription = "Search", tint = textColor)
                                }}
                                Spacer(modifier = Modifier.width(4.dp))
                                OutlinedIconButton(onClick = {{ showProfileOverlay = true }}, border = BorderStroke(1.dp, textColor.copy(alpha = 0.15f))) {{
                                    Icon(imageVector = Icons.Rounded.Person, contentDescription = "Profile", tint = textColor)
                                }}
                            }},
                            colors = TopAppBarDefaults.topAppBarColors(containerColor = bgColor)
                        )
                    }}
                ) {{ paddingValues ->
                    Box(modifier = Modifier.fillMaxSize().padding(paddingValues)) {{
                        Column(modifier = Modifier.fillMaxSize()) {{
                            HorizontalTabs(pagerState = pagerState, tabs = homeViewModel.tabs)
                            HorizontalPager(state = pagerState, beyondViewportPageCount = 4, modifier = Modifier.weight(1f).background(Color.Transparent)) {{ page ->
                                when (page) {{
                                    0 -> QuickPicks(onAlbumClick = navigateToAlbum, onArtistClick = navigateToArtist, onPlaylistClick = {{ browseId -> navController.navigate(route = Routes.Playlist(id = browseId)) }}, onOfflinePlaylistClick = {{ navController.navigate(route = Routes.BuiltInPlaylist(index = 1)) }})
                                    1 -> FavoritesScreen(onFavoriteTracksClick = {{ navController.navigate(route = Routes.FavoriteTracks) }}, onGoToAlbum = navigateToAlbum, onGoToArtist = navigateToArtist, isEmbedded = true)
                                    2 -> HomeSongs(onGoToAlbum = navigateToAlbum, onGoToArtist = navigateToArtist)
                                    3 -> HomeArtistList(onArtistClick = {{ artist -> navigateToArtist(artist.id) }})
                                    4 -> HomeAlbums(onAlbumClick = {{ album -> navigateToAlbum(album.id) }})
                                    5 -> HomePlaylists(onBuiltInPlaylist = {{ playlistIndex -> if (playlistIndex == BuiltInPlaylist.Favorites.ordinal) navController.navigate(route = Routes.Favorites) else navController.navigate(route = Routes.BuiltInPlaylist(index = playlistIndex)) }}, onPlaylistClick = {{ playlist -> navController.navigate(route = Routes.LocalPlaylist(id = playlist.id)) }})
                                }}
                            }}
                        }}
                    }}
                }}
                
                AnimatedVisibility(
                    visible = showProfileOverlay,
                    enter = fadeIn(tween(300)) + scaleIn(tween(300), transformOrigin = TransformOrigin(0.9f, 0.05f)),
                    exit = fadeOut(tween(200)) + scaleOut(tween(200), transformOrigin = TransformOrigin(0.9f, 0.05f)),
                    modifier = Modifier.fillMaxSize()
                ) {{
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .background(Color.Transparent)
                            .clickable {{ showProfileOverlay = false }},
                        contentAlignment = Alignment.Center
                    ) {{
                        Card(
                            shape = RoundedCornerShape(28.dp),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.35f)),
                            border = BorderStroke(1.dp, textColor.copy(alpha = 0.2f)),
                            modifier = Modifier.fillMaxWidth(0.95f).clickable(enabled = false) {{}} 
                        ) {{
                            Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp, vertical = 32.dp), horizontalAlignment = Alignment.CenterHorizontally) {{
                                Card(
                                    modifier = Modifier.fillMaxWidth().clickable {{ showProfileOverlay = false; showAuthScreen = true }},
                                    shape = RoundedCornerShape(18.dp),
                                    colors = CardDefaults.cardColors(containerColor = textColor.copy(alpha = 0.04f)),
                                    border = BorderStroke(1.5.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.8f))
                                ) {{
                                    Row(modifier = Modifier.fillMaxWidth().padding(14.dp), verticalAlignment = Alignment.CenterVertically) {{
                                        Box(modifier = Modifier.size(46.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary.copy(alpha = 0.15f)), contentAlignment = Alignment.Center) {{
                                            Icon(Icons.Rounded.AccountCircle, contentDescription = null, modifier = Modifier.size(28.dp), tint = MaterialTheme.colorScheme.primary)
                                        }}
                                        Spacer(modifier = Modifier.width(14.dp))
                                        Column(modifier = Modifier.weight(1f)) {{
                                            Text("Sign in to Musick", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 16.sp), color = textColor)
                                            Text("Set up local sync profile", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 11.sp), color = textColor.copy(alpha = 0.6f))
                                        }}
                                        Icon(Icons.Rounded.ChevronRight, contentDescription = null, tint = textColor.copy(alpha = 0.5f))
                                    }}
                                }}
                                Spacer(modifier = Modifier.height(14.dp))
                                
                                Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(18.dp), colors = CardDefaults.cardColors(containerColor = textColor.copy(alpha = 0.04f)), border = BorderStroke(1.5.dp, Color(0xFFFFD700).copy(alpha = 0.8f))) {{
                                    Column(modifier = Modifier.fillMaxWidth().clickable {{ expandedSection = if (expandedSection == "premium") null else "premium" }}.padding(12.dp)) {{
                                        Row(verticalAlignment = Alignment.CenterVertically) {{
                                            Box(modifier = Modifier.size(42.dp).clip(CircleShape).background(Color(0xFFFFD700).copy(alpha = 0.15f)), contentAlignment = Alignment.Center) {{
                                                Icon(Icons.Rounded.Star, contentDescription = null, tint = Color(0xFFFFD700), modifier = Modifier.size(22.dp))
                                            }}
                                            Spacer(modifier = Modifier.width(14.dp))
                                            Column {{
                                                Text("Musick Premium", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 15.sp), color = textColor)
                                                Text("Exclusive layouts & quality", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 11.sp), color = textColor.copy(alpha = 0.6f))
                                            }}
                                        }}
                                        AnimatedVisibility(visible = expandedSection == "premium") {{
                                            Text("Unlock ad-free streaming, maximum audio bitrate, and elite adaptive designs.", style = TextStyle(fontSize = 13.sp, lineHeight = 18.sp), color = textColor.copy(alpha = 0.8f), modifier = Modifier.padding(top = 10.dp, start = 6.dp, end = 6.dp))
                                        }}
                                    }}
                                }}
                                Spacer(modifier = Modifier.height(14.dp))
                                
                                Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(18.dp), colors = CardDefaults.cardColors(containerColor = textColor.copy(alpha = 0.04f)), border = BorderStroke(1.2.dp, textColor.copy(alpha = 0.2f))) {{
                                    Column(modifier = Modifier.fillMaxWidth().clickable {{ expandedSection = if (expandedSection == "ai") null else "ai" }}.padding(12.dp)) {{
                                        Row(verticalAlignment = Alignment.CenterVertically) {{
                                            Box(modifier = Modifier.size(42.dp).clip(CircleShape).background(textColor.copy(alpha = 0.08f)), contentAlignment = Alignment.Center) {{
                                                Icon(Icons.Rounded.Translate, contentDescription = null, tint = textColor, modifier = Modifier.size(22.dp))
                                            }}
                                            Spacer(modifier = Modifier.width(14.dp))
                                            Column {{
                                                Text("AI Translation", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 15.sp), color = textColor)
                                                Text("Translate lyrics instantly", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 11.sp), color = textColor.copy(alpha = 0.6f))
                                            }}
                                        }}
                                        AnimatedVisibility(visible = expandedSection == "ai") {{
                                            Column(modifier = Modifier.fillMaxWidth().padding(top = 10.dp, start = 6.dp, end = 6.dp)) {{
                                                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {{
                                                    Text("Enable Smart Lyrics", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 13.sp), color = textColor.copy(alpha = 0.9f))
                                                    Switch(checked = aiTranslationEnabled, onCheckedChange = {{ if (apiToken.isBlank()) Toast.makeText(context, "Please enter your API token first", Toast.LENGTH_SHORT).show() else aiTranslationEnabled = it }})
                                                }}
                                                Spacer(modifier = Modifier.height(8.dp))
                                                OutlinedTextField(value = apiToken, onValueChange = {{ apiToken = it }}, label = {{ Text("API Token", fontSize = 12.sp) }}, placeholder = {{ Text("Enter token key") }}, modifier = Modifier.fillMaxWidth(), singleLine = true, shape = RoundedCornerShape(10.dp))
                                            }}
                                        }}
                                    }}
                                }}
                                Spacer(modifier = Modifier.height(14.dp))
                                
                                Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(18.dp), colors = CardDefaults.cardColors(containerColor = textColor.copy(alpha = 0.04f)), border = BorderStroke(1.2.dp, textColor.copy(alpha = 0.2f))) {{
                                    Row(modifier = Modifier.fillMaxWidth().clickable {{ showProfileOverlay = false; onSettingsClick() }}.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {{
                                        Box(modifier = Modifier.size(42.dp).clip(CircleShape).background(textColor.copy(alpha = 0.08f)), contentAlignment = Alignment.Center) {{
                                            Icon(Icons.Rounded.Settings, contentDescription = null, tint = textColor, modifier = Modifier.size(22.dp))
                                        }}
                                        Spacer(modifier = Modifier.width(14.dp))
                                        Text("Settings", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 15.sp), color = textColor)
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}
}}
"""
with open(home_file, "w") as f: f.write(code_home)
