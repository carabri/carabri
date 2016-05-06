# apk-downloader
tools and scripts to download apk files from various android app mirror sites

## Prerequisites

- python3 is installed
- wget installed and on the PATH
- pip install selenium (don't laugh! we really do this using selenium... :P )
- chrome installed

## usage

eg. download all facebook apps from apkMirror, using mac:  

```bash
mkdir ./facebook_apps
./download_from_apkmirror.py --app_id facebook --driver chrome-drivers/chromedriver-mac32-v2.20 --outdir ./facebook_apps
```
