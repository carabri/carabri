# Lifetime simulator
This script orchestrating the long simulations, executing multiple test scenarios and installing 
the application upgrades between the tests.


## Script prerequisites:

- python3 is installed (additional pip packages to install: python_dateutil, pytz)
- adb is installed / downloaded
- adb is added to the path in your favorite shell's rc or profile.
- the target device is listed when running `adb devices` 
- the apks you have downloaded match the cpu architecture of the target device


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


