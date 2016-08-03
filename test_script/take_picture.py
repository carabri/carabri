import subprocess


subprocess.call("""
adb -d shell am start -a android.media.action.IMAGE_CAPTURE
& adb -d shell input keyevent 27
""")
