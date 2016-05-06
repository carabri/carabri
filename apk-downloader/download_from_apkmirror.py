#!/usr/bin/env python3

import os
import json
import re
import argparse
import subprocess
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = None


def main(args):
	global driver
	driver = webdriver.Chrome(args.driver)
	driver.get("http://www.apkmirror.com/uploads/?q="+args.app_id)
	
	apk_info_list = []
	apk_num = 1
	
	for apk_version_link in links_for_all_apk_version_pages():
		print("processing version:" + apk_version_link)
		driver.get(apk_version_link)
		variants = []
		for version_page in get_all_variants_of_version(apk_version_link):
			if apk_version_link != version_page:
				print("   processing sub-variant:" + version_page)
				driver.get(version_page)
			apk_info = download_apk_from_current_page(args.outdir, '%s_%d.apk' % (args.app_id,apk_num), args.app_id)
			apk_num+=1
			apk_info["app_id"] = args.app_id
			variants.append(apk_info)
# 			if apk_num>8: break
		apk_info_list.append({'app_id': args.app_id, 'version': variants[0]['version'], 'variants': variants})	
# 		if apk_num>8: break
	driver.close()

	apk_info_file = args.outdir + "/" + args.app_id + ".json"
	print("saving apk info list to %s" % apk_info_file)
	with open(apk_info_file, 'w') as out:
		out.write(json.dumps(apk_info_list, indent=4, sort_keys=True))
	


def links_for_all_apk_version_pages():
	all_apk_page_links = links_for_all_apk_versions_on_current_page()
	page = 1
	print('collecting versions from page %d' % page)
	page+=1
	
	while next_page_link():
		print('collecting versions from page %d' % page)
		page+=1
		driver.get(next_page_link())
		all_apk_page_links.extend(links_for_all_apk_versions_on_current_page())
	
	return all_apk_page_links


def links_for_all_apk_versions_on_current_page():
	wait_for_element_by_xpath("//div[contains(@class, 'widget_appmanager_recentpostswidget')]")
	apk_versions_on_current_page = driver.find_elements_by_xpath("//div[contains(@class, 'widget_appmanager_recentpostswidget')]//div[@class='appRow']//h5/a")
	return get_urls(apk_versions_on_current_page)


def next_page_link():
	link = driver.find_elements_by_xpath("//div[contains(@class, 'widget_appmanager_recentpostswidget')]//a[@class='nextpostslink']")
	if not link:
		return None
	return link[0].get_attribute('href')
	

def get_all_variants_of_version(current_page):
	multiple_variants = driver.find_elements_by_xpath("//div[@class='listWidget']/div[@class='widgetHeader' and .='Download']/..//div[contains(@class, 'variants-table')]//a")
	if not multiple_variants:
		return [current_page];
	return get_urls(multiple_variants)



def download_apk_from_current_page(dst_folder, dst_file_name, app_id):

	version_strings = locate_apk_spec_value_by_icon_class('file').split("\n")
	version = version_strings[0][8:].strip()
	architectures = ['any']
	if not version_strings[1].startswith("Package"): architectures = version_strings[1].strip().split(" + ")

	android_version_min = 'n/a'
	android_version_target = 'n/a'
	android_version_max = 'n/a'
	for android_version in locate_apk_spec_value_by_icon_class('sdk').split("\n"):
		if android_version.startswith('Min:'):
			android_version_min = android_version[4:].strip()
		if android_version.startswith('Target:'):
			android_version_target = android_version[7:].strip()
		if android_version.startswith('Max:'):
			android_version_max = android_version[4:].strip()

	screen_size = locate_apk_spec_value_by_icon_class('dpi').strip()
	upload_time = locate_apk_spec_value_by_icon_class('calendar').strip()[8:].split(" by")[0].strip()
	apk_download_ref=driver.find_element_by_xpath("//a[contains(@class,'downloadButton')]").get_attribute('href')
	downloaded_file_name=apk_download_ref.split('/')[-1]
	
	callAndDieIfNeeded('wget %s && mv ./%s ./%s' % (apk_download_ref, downloaded_file_name, dst_file_name), dst_folder)

	return {
	'app_id': app_id,
	'version': version, 
	'file_name': dst_file_name, 
	'architectures': architectures, 
	'screen_size': screen_size, 
	'android_version_min' : android_version_min,
	'android_version_target' : android_version_target,
	'android_version_max' : android_version_max,
	'upload_time':upload_time, 
	}


def locate_apk_spec_value_by_icon_class(icon_class):
	return driver.find_element_by_xpath("//*[contains(@class, 'apkm-icon-%s')]/ancestor::div[@class='appspec-row']/div[@class='appspec-value']" % icon_class).text



def get_urls(link_list):
	return list(map(lambda x : x.get_attribute('href'), link_list))


def wait_for_element_by_xpath(xpath):
	try:
		return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
	except:
		return None


def callAndDieIfNeeded(cmd, folder='.'):
    statusCode = subprocess.call(cmd, shell=True, cwd=folder)
    if (statusCode != 0):
        sys.exit(1)


if __name__ == '__main__':
    desc = """This script connects to Apk Mirror and downloads all the variants for the given app."""
    parser = argparse.ArgumentParser(description=desc)

    input_ = parser.add_argument_group('input')
    input_.add_argument('--app_id', help="app id in apk mirror; e.g.: google-play-movies if you want to download http://www.apkmirror.com/uploads/?q=google-play-movies")
    input_.add_argument('--driver', help='path to the chrome driver. eg: ./chrome_drivers/chromedriver-mac32-v2.20')

    output = parser.add_argument_group('output')
    output.add_argument('--outdir', help="path to the folder where all the apk and the metadata will be saved")

    optional = parser.add_argument_group('optional arguments')

    arguments = parser.parse_args()
    main(arguments)