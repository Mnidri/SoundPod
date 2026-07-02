package com.github.musick.ui.screens.auth
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
fun AuthScreen(onBack: () -> Unit) {
    val bgColor = MaterialTheme.colorScheme.background
    val textColor = MaterialTheme.colorScheme.onBackground
    val primaryColor = MaterialTheme.colorScheme.primary
    val context = LocalContext.current
    var isLoginMode by remember { mutableStateOf(true) }
    var username by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }

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
        // FIX: اضافه کردن اسکرول استاندارد بدون ایجاد فریز
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
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
                Button(
                    onClick = {
                        Toast.makeText(context, if (isLoginMode) "Logging in..." else "Creating account...", Toast.LENGTH_SHORT).show()
                        onBack()
                    },
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
                    modifier = Modifier.fillMaxWidth().height(54.dp).clickable { Toast.makeText(context, "Google Auth Started", Toast.LENGTH_SHORT).show() },
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
                // FIX: فضای خالی امن برای جلوگیری از افتادن زیر مینی‌پلیر
                Spacer(modifier = Modifier.height(130.dp))
            }
        }
    }
}
