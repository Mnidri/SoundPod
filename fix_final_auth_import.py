import os

home_file = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt"
auth_file = "app/src/main/kotlin/com/github/soundpod/ui/screens/auth/AuthScreen.kt"

if os.path.exists(home_file):
    with open(home_file, "r") as f:
        content = f.read()
    
    # تشخیص پکیج واقعی فایل AuthScreen
    detected_auth_import = "import com.github.musick.ui.screens.auth.AuthScreen"
    if os.path.exists(auth_file):
        with open(auth_file, "r") as f:
            auth_content = f.read()
            for line in auth_content.splitlines():
                if line.startswith("package "):
                    pkg = line.replace("package ", "").strip()
                    detected_auth_import = f"import {pkg}.AuthScreen"
                    break
    
    # اصلاح ایمپورت خراب قبلی در HomeScreen
    content = content.replace("import com.github.musick.ui.screens.auth.*", detected_auth_import)
    
    with open(home_file, "w") as f:
        f.write(content)
    print(f"HomeScreen patched with dynamic import: {detected_auth_import}")
