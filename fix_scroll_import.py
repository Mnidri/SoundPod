import os

auth_file = "app/src/main/kotlin/com/github/soundpod/ui/screens/auth/AuthScreen.kt"
if os.path.exists(auth_file):
    with open(auth_file, "r") as f: content = f.read()
    
    # تزریق ایمپورتِ اختصاصیِ اسکرول دقیقاً زیر بقیه ایمپورت‌های foundation
    if "import androidx.compose.foundation.verticalScroll" not in content:
        content = content.replace(
            "import androidx.compose.foundation.layout.*", 
            "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.verticalScroll"
        )
        with open(auth_file, "w") as f: f.write(content)
        print("verticalScroll imported perfectly!")
