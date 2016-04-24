# carabri
tools and scripts to simulate the aging of software ecosystems

## Installer script

Prerequisites:

- python3 is installed
- adb is installed / downloaded
- adb is added to the path in your favorite shell's rc or profile.
- the target device is listed when running `adb devices` 
- the apks you have downloaded match the cpu architecture of the target device

The install script loads a config.json that has the following fields:

`emulator`: true if you are using an emulated device, false if using usb
`apks`: \[ list of paths to the apks to be installed ]
`uninstall`: \[ list of packages to be removed. convenient if you have to restart the test ]
`tests`: _TODO to be added later_

The easiest way to figure out the package name of a given apk is:
`aapt list -a $PATH_TO_YOUR_APK | sed -n "/^Package Group[^s]/s/.*name=//p"`

aapt can be found in `android-sdk-$PLATFORM_NAME/build-tools/$VERSION_NUMBER/`

__The script looks for the config file next to itself, so it should by started from its containing directory!__