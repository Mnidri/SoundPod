import os

# ۱. اصلاح دیالوگ شیشه‌ای در HomeScreen
home_file = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt"
if os.path.exists(home_file):
    with open(home_file, "r") as f: content = f.read()
    
    # رفع مشکل کامپایلِ دارک‌مود با آدرس‌دهی کامل
    content = content.replace("val isDark = isSystemInDarkTheme()", "val isDark = androidx.compose.foundation.isSystemInDarkTheme()")
    
    # خالص‌تر کردنِ شیشه‌ی سفید در لایت‌مود تا کاملاً روشن و لوکس بشه
    content = content.replace("Color.White.copy(alpha = 0.85f)", "Color.White.copy(alpha = 0.98f)")
    
    with open(home_file, "w") as f: f.write(content)
    print("HomeScreen successfully patched!")

# ۲. اصلاح اسکرول و دکمه گوگل در AuthScreen
auth_file = "app/src/main/kotlin/com/github/soundpod/ui/screens/auth/AuthScreen.kt"
if os.path.exists(auth_file):
    with open(auth_file, "r") as f: content = f.read()

    old_col = """Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(horizontal = 24.dp),"""
    new_col = """Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(horizontal = 24.dp)
                .verticalScroll(androidx.compose.foundation.rememberScrollState()),"""
    content = content.replace(old_col, new_col)

    old_end = """Text("Continue with Google", fontWeight = FontWeight.Bold, fontSize = 15.sp, color = textColor)
                    }
                }
            }
        }
    }
}"""
    new_end = """Text("Continue with Google", fontWeight = FontWeight.Bold, fontSize = 15.sp, color = textColor)
                    }
                }
                Spacer(modifier = Modifier.height(110.dp))
            }
        }
    }
}"""
    content = content.replace(old_end, new_end)
    with open(auth_file, "w") as f: f.write(content)
    print("AuthScreen successfully patched!")

# ۳. اصلاح تب‌های ArtistScreen در لایت‌مود
artist_file = "app/src/main/kotlin/com/github/soundpod/ui/screens/artist/ArtistScreen.kt"
if os.path.exists(artist_file):
    with open(artist_file, "r") as f: content = f.read()

    old_tab = """Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(50))
                                .background(if (selected) if (androidx.compose.foundation.isSystemInDarkTheme()) Color.White else Color.Black else Color.White.copy(alpha = 0.1f))
                                .clickable { coroutineScope.launch { pagerState.animateScrollToPage(index) } }
                                .padding(horizontal = 20.dp, vertical = 10.dp)
                        ) {
                            Text(text = stringResource(titleRes), style = typography.titleSmall.copy(fontWeight = FontWeight.Bold), color = if (selected) if (androidx.compose.foundation.isSystemInDarkTheme()) Color.Black else Color.Black.copy(alpha = 0.06f) else if (androidx.compose.foundation.isSystemInDarkTheme()) Color.White else Color.Black)
                        }"""
    
    new_tab = """val isDark = androidx.compose.foundation.isSystemInDarkTheme()
                        val tabBg = if (selected) {
                            if (isDark) Color.White else Color.Black
                        } else {
                            if (isDark) Color.White.copy(alpha = 0.1f) else Color.Black.copy(alpha = 0.05f)
                        }
                        val tabTextColor = if (selected) {
                            if (isDark) Color.Black else Color.White
                        } else {
                            if (isDark) Color.White else Color.Black.copy(alpha = 0.7f)
                        }
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(50))
                                .background(tabBg)
                                .clickable { coroutineScope.launch { pagerState.animateScrollToPage(index) } }
                                .padding(horizontal = 20.dp, vertical = 10.dp)
                        ) {
                            Text(text = stringResource(titleRes), style = typography.titleSmall.copy(fontWeight = FontWeight.Bold), color = tabTextColor)
                        }"""
    
    content = content.replace(old_tab, new_tab)
    with open(artist_file, "w") as f: f.write(content)
    print("ArtistScreen successfully patched!")
