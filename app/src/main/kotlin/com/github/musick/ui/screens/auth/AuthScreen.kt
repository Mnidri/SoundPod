package com.github.musick.ui.screens.auth

import android.content.Context
import android.widget.Toast
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Shadow
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import android.util.Patterns
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.GoogleAuthProvider
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AuthScreen(onBack: () -> Unit) {
    val bgColor = MaterialTheme.colorScheme.background
    val textColor = MaterialTheme.colorScheme.onBackground
    val primaryColor = MaterialTheme.colorScheme.primary
    val context = LocalContext.current

    // گوش‌به‌زنگ زنده وضعیت فایربیس
    var firebaseUser by remember { mutableStateOf(FirebaseAuth.getInstance().currentUser) }
    
    DisposableEffect(Unit) {
        val listener = FirebaseAuth.AuthStateListener { auth ->
            firebaseUser = auth.currentUser
        }
        FirebaseAuth.getInstance().addAuthStateListener(listener)
        onDispose { FirebaseAuth.getInstance().removeAuthStateListener(listener) }
    }

    Scaffold(
        containerColor = bgColor,
        topBar = {
            TopAppBar(
                title = { },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Rounded.ArrowBack, contentDescription = "Back", tint = textColor)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
        }
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            if (firebaseUser == null) {
                // نمایش فرم لاگین در صورت عدم ورود
                LoginSignupForm(primaryColor, textColor, context)
            } else {
                // نمایش پروفایل مدیریتی و تنظیمات هوش مصنوعی
                ProfileManagementPanel(firebaseUser!!, textColor, context)
            }
        }
    }
}

@Composable
fun LoginSignupForm(primaryColor: Color, textColor: Color, context: Context) {
    var isLoginMode by remember { mutableStateOf(true) }
    var username by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    val auth = remember { FirebaseAuth.getInstance() }

    val gso = remember {
        GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestIdToken("1004660477819-oe8p4nmjbcq1ss1754nl6usu5re706i9.apps.googleusercontent.com")
            .requestEmail()
            .build()
    }
    val googleSignInClient = remember { GoogleSignIn.getClient(context, gso) }

    val googleLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartActivityForResult()
    ) { result ->
        isLoading = false
        val task = GoogleSignIn.getSignedInAccountFromIntent(result.data)
        try {
            val account = task.getResult(Exception::class.java)
            val credential = GoogleAuthProvider.getCredential(account.idToken, null)
            auth.signInWithCredential(credential)
                .addOnCompleteListener { authResult ->
                    if (authResult.isSuccessful) {
                        Toast.makeText(context, "Google Sign-In successful!", Toast.LENGTH_SHORT).show()
                    } else {
                        Toast.makeText(context, "Firebase Error: ${authResult.exception?.message}", Toast.LENGTH_LONG).show()
                    }
                }
        } catch (e: Exception) {
            Toast.makeText(context, "Google Auth Error: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(20.dp))
        Text(
            text = "Musick",
            fontSize = 48.sp,
            fontWeight = FontWeight.ExtraBold,
            fontFamily = FontFamily.Serif,
            letterSpacing = (-1.5).sp,
            color = textColor,
            style = TextStyle(shadow = Shadow(color = textColor.copy(alpha = 0.5f), blurRadius = 24f))
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
        ) {
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxHeight()
                    .clip(RoundedCornerShape(50))
                    .background(if (isLoginMode) textColor.copy(alpha = 0.1f) else Color.Transparent)
                    .clickable { isLoginMode = true },
                contentAlignment = Alignment.Center
            ) {
                Text("Log In", fontWeight = FontWeight.Bold, color = if (isLoginMode) textColor else textColor.copy(alpha = 0.5f))
            }
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxHeight()
                    .clip(RoundedCornerShape(50))
                    .background(if (!isLoginMode) textColor.copy(alpha = 0.1f) else Color.Transparent)
                    .clickable { isLoginMode = false },
                contentAlignment = Alignment.Center
            ) {
                Text("Sign Up", fontWeight = FontWeight.Bold, color = if (!isLoginMode) textColor else textColor.copy(alpha = 0.5f))
            }
        }
        Spacer(modifier = Modifier.height(32.dp))
        Column(modifier = Modifier.fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally) {
            AnimatedVisibility(visible = !isLoginMode) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Box(
                        modifier = Modifier
                            .size(90.dp)
                            .clip(CircleShape)
                            .background(textColor.copy(alpha = 0.05f))
                            .border(1.dp, textColor.copy(alpha = 0.2f), CircleShape)
                            .clickable { Toast.makeText(context, "Gallery opened", Toast.LENGTH_SHORT).show() },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Rounded.ImageSearch, contentDescription = null, tint = textColor.copy(alpha = 0.6f), modifier = Modifier.size(28.dp))
                    }
                    Spacer(modifier = Modifier.height(24.dp))
                }
            }
            AnimatedVisibility(visible = !isLoginMode) {
                Column {
                    OutlinedTextField(
                        value = username,
                        onValueChange = { username = it },
                        placeholder = { Text("Username") },
                        leadingIcon = { Icon(Icons.Rounded.Person, contentDescription = null, tint = textColor.copy(alpha = 0.5f)) },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true,
                        shape = RoundedCornerShape(16.dp),
                        colors = OutlinedTextFieldDefaults.colors(unfocusedBorderColor = textColor.copy(alpha = 0.1f))
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                }
            }
            OutlinedTextField(
                value = email,
                onValueChange = { email = it },
                placeholder = { Text("Email Address") },
                leadingIcon = { Icon(Icons.Rounded.Email, contentDescription = null, tint = textColor.copy(alpha = 0.5f)) },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                shape = RoundedCornerShape(16.dp),
                colors = OutlinedTextFieldDefaults.colors(unfocusedBorderColor = textColor.copy(alpha = 0.1f))
            )
            Spacer(modifier = Modifier.height(16.dp))
            OutlinedTextField(
                value = password,
                onValueChange = { password = it },
                placeholder = { Text("Password") },
                leadingIcon = { Icon(Icons.Rounded.Lock, contentDescription = null, tint = textColor.copy(alpha = 0.5f)) },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                visualTransformation = PasswordVisualTransformation(),
                shape = RoundedCornerShape(16.dp),
                colors = OutlinedTextFieldDefaults.colors(unfocusedBorderColor = textColor.copy(alpha = 0.1f))
            )
            Spacer(modifier = Modifier.height(32.dp))
            if (isLoading) {
                CircularProgressIndicator(color = primaryColor)
                Spacer(modifier = Modifier.height(16.dp))
            }
            Button(
                onClick = {
                    val trimmedEmail = email.trim()
                    val trimmedPassword = password.trim()
                    if (trimmedEmail.isEmpty() || trimmedPassword.isEmpty()) {
                        Toast.makeText(context, "Please fill in all fields", Toast.LENGTH_SHORT).show()
                        return@Button
                    }
                    if (!Patterns.EMAIL_ADDRESS.matcher(trimmedEmail).matches()) {
                        Toast.makeText(context, "Invalid email address format", Toast.LENGTH_SHORT).show()
                        return@Button
                    }
                    if (trimmedPassword.length < 6) {
                        Toast.makeText(context, "Password must be at least 6 characters", Toast.LENGTH_SHORT).show()
                        return@Button
                    }
                    isLoading = true
                    if (isLoginMode) {
                        auth.signInWithEmailAndPassword(trimmedEmail, trimmedPassword)
                            .addOnCompleteListener { task ->
                                isLoading = false
                                if (task.isSuccessful) {
                                    Toast.makeText(context, "Logged in successfully!", Toast.LENGTH_SHORT).show()
                                } else {
                                    Toast.makeText(context, "Login Error: ${task.exception?.localizedMessage}", Toast.LENGTH_LONG).show()
                                }
                            }
                    } else {
                        auth.createUserWithEmailAndPassword(trimmedEmail, trimmedPassword)
                            .addOnCompleteListener { task ->
                                isLoading = false
                                if (task.isSuccessful) {
                                    Toast.makeText(context, "Account created successfully!", Toast.LENGTH_SHORT).show()
                                } else {
                                    Toast.makeText(context, "Registration Error: ${task.exception?.localizedMessage}", Toast.LENGTH_LONG).show()
                                }
                            }
                    }
                },
                enabled = !isLoading,
                modifier = Modifier.fillMaxWidth().height(54.dp),
                shape = RoundedCornerShape(50),
                colors = ButtonDefaults.buttonColors(containerColor = primaryColor)
            ) {
                Text(if (isLoginMode) "Log In" else "Create Account", fontWeight = FontWeight.Bold, fontSize = 16.sp)
            }
            Spacer(modifier = Modifier.height(32.dp))
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                HorizontalDivider(modifier = Modifier.weight(1f), color = textColor.copy(alpha = 0.1f))
                Text(" OR ", color = textColor.copy(alpha = 0.4f), fontSize = 12.sp, modifier = Modifier.padding(horizontal = 16.dp))
                HorizontalDivider(modifier = Modifier.weight(1f), color = textColor.copy(alpha = 0.1f))
            }
            Spacer(modifier = Modifier.height(32.dp))
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(54.dp)
                    .clickable(enabled = !isLoading) {
                        isLoading = true
                        googleSignInClient.signOut().addOnCompleteListener {
                            googleLauncher.launch(googleSignInClient.signInIntent)
                        }
                    },
                shape = RoundedCornerShape(50),
                colors = CardDefaults.cardColors(containerColor = Color.Transparent),
                border = BorderStroke(1.dp, textColor.copy(alpha = 0.2f))
            ) {
                Row(modifier = Modifier.fillMaxSize(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.Center) {
                    Text("G", fontWeight = FontWeight.ExtraBold, fontSize = 20.sp, color = textColor)
                    Spacer(modifier = Modifier.width(12.dp))
                    Text("Continue with Google", fontWeight = FontWeight.Bold, fontSize = 15.sp, color = textColor)
                }
            }
            Spacer(modifier = Modifier.height(130.dp))
        }
    }
}

@Composable
fun ProfileManagementPanel(user: com.google.firebase.auth.FirebaseUser, textColor: Color, context: Context) {
    val sharedPreferences = context.getSharedPreferences("ai_settings", Context.MODE_PRIVATE)
    var apiKey by remember { mutableStateOf(sharedPreferences.getString("api_key", "") ?: "") }
    var isSaved by remember { mutableStateOf(false) }

    val neonGold = Color(0xFFFFD700)
    val neonRed = Color(0xFFFF3333)

    val gso = remember {
        GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestIdToken("1004660477819-oe8p4nmjbcq1ss1754nl6usu5re706i9.apps.googleusercontent.com")
            .requestEmail()
            .build()
    }
    val googleSignInClient = remember { GoogleSignIn.getClient(context, gso) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(16.dp))
        
        // Avatar / Profile Header
        Box(
            modifier = Modifier
                .size(90.dp)
                .clip(CircleShape)
                .background(textColor.copy(alpha = 0.05f))
                .border(1.dp, textColor.copy(alpha = 0.2f), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Rounded.Person, contentDescription = null, tint = textColor.copy(alpha = 0.7f), modifier = Modifier.size(40.dp))
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = user.displayName ?: "Musick User",
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold,
            color = textColor
        )
        Text(
            text = user.email ?: "",
            fontSize = 14.sp,
            color = textColor.copy(alpha = 0.5f)
        )

        Spacer(modifier = Modifier.height(32.dp))

        // Premium Status Card (Neon Gold Styling)
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .border(1.5.dp, neonGold, RoundedCornerShape(16.dp)),
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = Color.Black.copy(alpha = 0.4f))
        ) {
            Row(
                modifier = Modifier.padding(16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(Icons.Rounded.Star, contentDescription = "Premium", tint = neonGold, modifier = Modifier.size(28.dp))
                Spacer(modifier = Modifier.width(16.dp))
                Column {
                    Text(
                        text = "Premium Status",
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Bold,
                        color = neonGold,
                        style = TextStyle(shadow = Shadow(color = neonGold.copy(alpha = 0.6f), blurRadius = 12f))
                    )
                    Text(
                        text = "Early-bird Premium Active",
                        fontSize = 13.sp,
                        color = textColor
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // AI Translation Settings Box (Moved to Profile Panel)
        Card(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = textColor.copy(alpha = 0.03f)),
            border = BorderStroke(1.dp, textColor.copy(alpha = 0.1f))
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    text = "AI Translation Configuration",
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    color = textColor
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "Requests are processed automatically via Musick servers. Optionally, you can supply your personal Gemini API Key below.",
                    fontSize = 12.sp,
                    color = textColor.copy(alpha = 0.6f)
                )
                Spacer(modifier = Modifier.height(16.dp))
                OutlinedTextField(
                    value = apiKey,
                    onValueChange = {
                        apiKey = it
                        isSaved = false
                    },
                    placeholder = { Text("Enter personal Gemini API Key") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    shape = RoundedCornerShape(12.dp),
                    colors = OutlinedTextFieldDefaults.colors(unfocusedBorderColor = textColor.copy(alpha = 0.1f))
                )
                Spacer(modifier = Modifier.height(12.dp))
                Button(
                    onClick = {
                        sharedPreferences.edit().putString("api_key", apiKey).apply()
                        isSaved = true
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Text(if (isSaved) "Saved Successfully!" else "Save API Key")
                }
            }
        }

        Spacer(modifier = Modifier.height(32.dp))

        // Switch Account Button
        OutlinedButton(
            onClick = {
                FirebaseAuth.getInstance().signOut()
                googleSignInClient.signOut()
            },
            modifier = Modifier.fillMaxWidth().height(50.dp),
            shape = RoundedCornerShape(50),
            border = BorderStroke(1.dp, textColor.copy(alpha = 0.3f))
        ) {
            Icon(Icons.Rounded.SwitchAccount, contentDescription = null, tint = textColor)
            Spacer(modifier = Modifier.width(8.dp))
            Text("Switch Account", fontWeight = FontWeight.Bold, color = textColor)
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Log Out Button (Neon Red Styling)
        Button(
            onClick = {
                FirebaseAuth.getInstance().signOut()
                googleSignInClient.signOut()
            },
            modifier = Modifier
                .fillMaxWidth()
                .height(50.dp)
                .border(1.dp, neonRed, RoundedCornerShape(50)),
            shape = RoundedCornerShape(50),
            colors = ButtonDefaults.buttonColors(containerColor = Color.Black.copy(alpha = 0.2f))
        ) {
            Icon(Icons.Rounded.Logout, contentDescription = null, tint = neonRed)
            Spacer(modifier = Modifier.width(8.dp))
            Text(
                text = "Log Out",
                fontWeight = FontWeight.Bold,
                color = neonRed,
                style = TextStyle(shadow = Shadow(color = neonRed.copy(alpha = 0.6f), blurRadius = 12f))
            )
        }
        
        Spacer(modifier = Modifier.height(130.dp))
    }
}
