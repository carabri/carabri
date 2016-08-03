import subprocess


subprocess.call("""
adb -d shell am start -n com.android.gallery/com.android.camera.GalleryPicker
""")
