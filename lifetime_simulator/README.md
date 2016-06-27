# Lifetime simulator
This script orchestrating the long simulations, executing multiple test scenarios and installing 
the application upgrades between the tests.


## Script prerequisites:

- python3 is installed (additional pip packages to install: python_dateutil, pytz)
- adb is installed / downloaded
- adb is added to the path in your favorite shell's rc or profile. (adb binary is in the _{android sdk}/platform-tools_ folder
- the target device is listed when running `adb devices` 
- the apks you have downloaded match the cpu architecture of the target device


## Prepare base image (AVD)
- display: 4" WVGA, 480x800, hdpi
- Android system image, 4.3, Jelly bean, API18 x86
- avd name: carabri (we will refer to this virtual device with it's name later)
- camera: emulated back camera
- network: full speed, no latency
- graphics emulation: auto (ADB will use hardware emulation if possible)
- RAM: 512 MB
- VM heap: 32 MB
- Internal storage: 800 MB
- SD card: 100 MB
- Keyboard: enable keyboard input


## starting the base image
- if you have the device specified above, you can start it with the "_{android sdk}/tools/emulator -avd carabri_" command
- to start the emulator in headless mode, use the "_-no-skin -no-audio -no-window_" options
- to verify Intel hardware vistualization support, you should look in the command line for the following output: "HAXM is working and emulator runs in fast virt mode"
- if the hardware virtalization is not working, then you shoud check the following page to fix it: https://developer.android.com/studio/run/emulator-commandline.html (see chapter: 'Configuring Virtual Machine Acceleration')
- you can not have hardware virtualization support if you execute the emulator from virtualbox or docker...
- to terminate the emaulator, you can use _kill_ in command line (for me sometime I had to use _kill -9_)

## Usage

```
lifetime_simulator [OPTIONS]
```

__Options:__
- `--config=<config file>`: specify the config json file will be used during execution (default=config.json)
- `--log_dir=<path>`: specify the log folder where the execution logs will be generated (default=./log/)

The install script loads a json config file that has the following fields:
- `emulator`: true if you are using an emulated device, false if using usb __(mandatory field)__
- `apk-database`: path to the folder contains the json files with the apk database __(mandatory field)__
- `api-version`: installing only apks compatible with the given API version (eg: 14, which refers to Android 4.0 (Ice Cream Sandwich)) __(mandatory field)__
- `apks`: \[ list of app ids (refering to the apk database) for the applications to be installed ] __(mandatory field)__
- `architecture`: installing only apks for the given architecture: arm, arm64, x86 (default: x86)
- `after`: only the apk released after this date (inclusive) will be installed (default: 2010-01-01)
- `before`: only the apk released before this date (inclusive) will be installed (default: 2099-12-31)
- `screen-size`: installing only apks compatible with the given screen size (eg: '240dpi', '480dpi') (default: 'nodpi' -> only the apks with no screen-size limitation will be installed)
- `tests`: \[ list of test json objects will be executed between each apk install ] __(mandatory field)__


Each test json object can contain the following fields: 
- `test-id`: id for test (used for logging, also forward to the test command)
- `command`: shell command will be executed to perform the given test
- `repeat`: number of repeats of the command (default=1)


## Test execution

The individual tests will be executed via shell. The following environment variables will be set for each command:
- `TEST_ID`: id specified for the test
- `SEQUENCE`: sequence of test execution (starting from 0, used to distinguish between different executions if `repeat`>1)
- `LOG_DIR`: path to the log dir
- `RELEASE_DATE`: the date of the release of the last upgraded app
- `APP_ID`: id of the last upgraded app (used in the apk database) 
- `APP_VERSION`: version of the last upgraded app


