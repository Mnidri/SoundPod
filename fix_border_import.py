import os

fp_home = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt"
if not os.path.exists(fp_home): fp_home = "app/src/main/kotlin/com/github/musick/ui/screens/home/HomeScreen.kt"

if os.path.exists(fp_home):
    with open(fp_home, "r") as f:
        code = f.read()
        
    if "import androidx.compose.foundation.border" not in code:
        code = code.replace("import androidx.compose.foundation.background", 
                            "import androidx.compose.foundation.background\nimport androidx.compose.foundation.border")
        
        with open(fp_home, "w") as f:
            f.write(code)
            print("Border import successfully added!")
