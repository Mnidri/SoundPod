import os

files_to_fix = [
    "app/src/main/kotlin/com/github/soundpod/ui/screens/artist/ArtistScreen.kt",
    "app/src/main/kotlin/com/github/soundpod/ui/components/HorizontalTabs.kt"
]

for fp in files_to_fix:
    if os.path.exists(fp):
        with open(fp, "r") as f:
            content = f.read()
        
        # جایگزینی کلمه کوتاه با آدرسِ کاملِ متریال ۳ تا نیازی به هیچ ایمپورتی نباشه
        content = content.replace("MaterialTheme.colorScheme.onBackground", 
                                  "androidx.compose.material3.MaterialTheme.colorScheme.onBackground")
        
        with open(fp, "w") as f:
            f.write(content)
        print(f"Absolute MaterialTheme path injected into: {os.path.basename(fp)}")

print("Done! Compiler has no excuses left.")
