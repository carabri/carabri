import subprocess


subprocess.call("""
adb -d shell am start -n com.google.android.gm/com.google.android.gm.ComposeActivityGmail
-d email:test@email.com --es subject 'Test subject' --es body 'Test body'
& adb -d shell input keyevent 19 & adb -d shell input keyevent 19 & adb -d shell input keyevent 19
& adb -d shell input keyevent 19 & adb -d shell input keyevent 19 & adb -d shell input keyevent 22
& adb -d shell input keyevent 23
""")
