# CARABRI
Tools and scripts to simulate the aging of software ecosystems.
Check the sub directories for the description of the given tools/scripts.

## Quick-start guide
1. pull the git repo
2. install all the prerequisites and initialize the android image (see the [Lifetime simulator page](https://github.com/carabri/carabri/tree/master/lifetime_simulator))
3. download and extract the sample application DB [from HERE](https://gumicsizma.netbiol.org/apk_db_sample.tgz) (~350MB)
4. create a config json file for the lifetime simulator based on the `config_example.json`. Make sure you set the following parameters:
    - `"apk-database": "../../apk_db_sample/"`: the absolute or relative path to the extracted `apk_db_sample` folder
    - `"apks": ["chrome", "gmail"]`: the sample apk db contains a few chrome and gmail apks
    - `"after": "2015-03-01"`and `"before": "2015-04-30"`: these the sample apks were released in these two months
5. start the lifetime simulator: `./lifetime_simulator.py --config=<path to your config file> --log_dir=<path to an empty folder>`