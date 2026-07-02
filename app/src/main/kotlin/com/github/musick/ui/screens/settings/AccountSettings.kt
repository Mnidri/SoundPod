package com.github.musick.ui.screens.settings
import androidx.compose.ui.platform.LocalContext
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.GoogleAuthProvider
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.rememberCoroutineScope
import kotlinx.coroutines.launch
import androidx.compose.runtime.setValue
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf


import android.annotation.SuppressLint
import android.webkit.CookieManager
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Login
import androidx.compose.material.icons.automirrored.filled.Logout
import androidx.compose.material.icons.filled.AccountCircle
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import com.github.innertube.Innertube
import com.github.musick.R
import com.github.musick.service.YouTubeSessionManager
import com.github.musick.ui.common.IconSource
import com.github.musick.ui.components.isWebViewAvailable
import com.github.musick.ui.navigation.SettingsDestinations

@Composable
fun YouTubeSettingsContent(onOptionClick: (String) -> Unit) {
    val isLoggedIn = Innertube.isLoggedIn

    Column(modifier = Modifier.fillMaxSize()) {
        SettingsGroup(title = stringResource(R.string.youtube_account)) {
            if (!isLoggedIn) {
                SettingsColumn(
                    title = stringResource(R.string.sign_in),
                    description = stringResource(R.string.sign_in_description),
                    icon = IconSource.Vector(Icons.AutoMirrored.Filled.Login),
                    onClick = { onOptionClick(SettingsDestinations.LOGIN) },
                )
            } else {
                SettingsColumn(
                    title = stringResource(R.string.youtube_account),
                    description = stringResource(R.string.youtube_account_description),
                    icon = IconSource.Vector(Icons.Default.AccountCircle),
                )
                SettingsColumn(
                    title = stringResource(R.string.sign_out),
                    description = stringResource(R.string.sign_out_description),
                    icon = IconSource.Vector(Icons.AutoMirrored.Filled.Logout),
                    onClick = {
                        CookieManager.getInstance().removeAllCookies(null)
                        YouTubeSessionManager.updateSession(cookies = "")
                    }
                )
            }
        }

    }
}

@SuppressLint("SetJavaScriptEnabled")
@Composable
fun LoginSettingsContent(onBack: () -> Unit) {
    val context = androidx.compose.ui.platform.LocalContext.current
    if (!isWebViewAvailable(context)) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Text(
                text = "WebView is required for Login. Please install or enable Android System WebView.",
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.error,
                modifier = Modifier.padding(16.dp)
            )
        }
        return
    }

    var isLoading by remember { mutableStateOf(value = true) }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
    ) {
        AndroidView(
            factory = { context ->
                WebView(context).apply {
                    settings.apply {
                        javaScriptEnabled = true
                        domStorageEnabled = true
                        loadWithOverviewMode = true
                        useWideViewPort = true
                        setSupportZoom(true)
                        builtInZoomControls = true
                        mixedContentMode = android.webkit.WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                        userAgentString = "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"
                    }
                    
                    webChromeClient = android.webkit.WebChromeClient()
                    webViewClient = object : WebViewClient() {
                        override fun shouldInterceptRequest(view: WebView?, request: WebResourceRequest?): WebResourceResponse? {
                            val url = request?.url?.toString() ?: ""
                            if (url.contains("googlevideo.com") || url.contains("/videoplayback")) {
                                return WebResourceResponse("text/plain", "UTF-8", null)
                            }
                            return super.shouldInterceptRequest(view, request)
                        }

                        override fun onPageFinished(view: WebView?, url: String?) {
                            isLoading = false
                            view?.evaluateJavascript(
                                """
                                (function() {
                                    const media = document.querySelectorAll('video, audio');
                                    media.forEach(m => { m.muted = true; m.pause(); });
                                })();
                            """.trimIndent(),
                                null,
                            )

                            val cookies = CookieManager.getInstance().getCookie(url)
                            if ((cookies?.contains("__Secure-3PAPISID") == true) || (cookies?.contains("SAPISID") == true)) {
                                YouTubeSessionManager.updateSession(cookies = cookies)
                                if (url?.contains("music.youtube.com") == true && !url.contains("login")) {
                                    onBack()
                                }
                            }
                        }
                    }
                    loadUrl("https://music.youtube.com/")
                }
            },
            modifier = Modifier.fillMaxSize()
        )
        
        if (isLoading) {
            CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
        }
    }
}


@Composable
fun MusickAccountSection() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var firebaseUser by remember { mutableStateOf(FirebaseAuth.getInstance().currentUser) }
    androidx.compose.runtime.DisposableEffect(Unit) {
        val listener = com.google.firebase.auth.FirebaseAuth.AuthStateListener { auth ->
            firebaseUser = auth.currentUser
        }
        com.google.firebase.auth.FirebaseAuth.getInstance().addAuthStateListener(listener)
        onDispose { com.google.firebase.auth.FirebaseAuth.getInstance().removeAuthStateListener(listener) }
    }
    
    val gso = remember {
        GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestIdToken("1004660477819-oe8p4nmjbcq1ss1754nl6usu5re706i9.apps.googleusercontent.com")
            .requestEmail()
            .build()
    }
    val googleSignInClient = remember { GoogleSignIn.getClient(context, gso) }
    
    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartActivityForResult()
    ) { result ->
        val task = GoogleSignIn.getSignedInAccountFromIntent(result.data)
        try {
            val account = task.getResult(Exception::class.java)
            val credential = GoogleAuthProvider.getCredential(account.idToken, null)
            FirebaseAuth.getInstance().signInWithCredential(credential)
                .addOnCompleteListener { authResult ->
                    if (authResult.isSuccessful) {
                        firebaseUser = FirebaseAuth.getInstance().currentUser
                    }
                }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    SettingsGroup(title = "حساب کاربری Musick (امکانات ویژه)") {
        if (firebaseUser == null) {
            SettingsColumn(
                title = "ورود با حساب گوگل",
                description = "جهت فعال‌سازی پریموم، لیریک هوشمند و ترجمه خودکار هوش مصنوعی",
                icon = IconSource.Vector(Icons.AutoMirrored.Filled.Login),
                onClick = {
                    googleSignInClient.signOut().addOnCompleteListener {
                        launcher.launch(googleSignInClient.signInIntent)
                    }
                },
            )
        } else {
            SettingsColumn(
                title = "کاربر پریموم: ${firebaseUser?.displayName ?: "کاربر Musick"}",
                description = "ایمیل: ${firebaseUser?.email}\nوضعیت اشتراک: پریموم آزمایشی (Early-bird فعال)",
                icon = IconSource.Vector(Icons.Default.AccountCircle),
            )
            SettingsColumn(
                title = "خروج از حساب Musick",
                description = "غیرفعال‌سازی موقت دسترسی به ویژگی‌های هوش مصنوعی",
                icon = IconSource.Vector(Icons.AutoMirrored.Filled.Logout),
                onClick = {
                    FirebaseAuth.getInstance().signOut()
                    googleSignInClient.signOut()
                    firebaseUser = null
                }
            )
        }
    }
}
