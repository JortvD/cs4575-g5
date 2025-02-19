import asyncio
import os
import platform
import requests
import progressbar
import zipfile
import subprocess
import shutil
import datetime

DATA_FOLDER = 'data'

if not os.path.exists(DATA_FOLDER):
	os.makedirs(DATA_FOLDER)

OUTPUT_FOLDER = 'output'

if not os.path.exists(OUTPUT_FOLDER):
	os.makedirs(OUTPUT_FOLDER)

class ZipDownloader:
	def __init__(self, name, data_folder, zip_name, keep_zip=True, overwrite_zip=False, force_unzip=False):
		self.data_folder = data_folder
		self.name = name
		self.zip_name = zip_name
		self.keep_zip = keep_zip
		self.overwrite_zip = overwrite_zip
		self.force_unzip = force_unzip

	def check_if_zip_exists(self):
		return os.path.exists(os.path.join(DATA_FOLDER, self.zip_name))
	
	def download(self, url):
		if not self.overwrite_zip and self.check_if_zip_exists():
			print(f'{self.name} already exists. Skipping download')
			return

		response = requests.get(url, stream=True)
		download_path = os.path.join(DATA_FOLDER, self.zip_name)
		file = open(download_path, 'wb')
		total_length = int(response.headers.get('content-length'))
		total_length_mb = total_length / (1024 * 1024)

		print(f'Downloading {self.name} ({total_length_mb:.2f} MB)')

		widgets = [progressbar.Bar(), progressbar.Percentage(), " | ", progressbar.FileTransferSpeed(), " | ", progressbar.ETA()]
		bar = progressbar.ProgressBar(widgets=widgets, maxval=total_length).start()

		for chunk in response.iter_content(chunk_size=8192):
			file.write(chunk)
			bar.update(file.tell())

		file.close()
		bar.finish()

	def unzip(self):
		if not self.force_unzip and os.path.exists(self.get_folder()):
			print(f'{self.name} already unzipped. Skipping unzip')
			return

		print(f'Unzipping {self.name}')
		zip_path = os.path.join(DATA_FOLDER, self.zip_name)
		with zipfile.ZipFile(zip_path, 'r') as zip_ref:
			zip_ref.extractall(DATA_FOLDER)

	def clean_zip(self):
		if self.keep_zip:
			return

		print(f'Cleaning up {self.name} zip file')
		zip_path = os.path.join(DATA_FOLDER, self.zip_name)
		os.remove(zip_path)

	def run(self):
		pass

class ChromiumDownloader(ZipDownloader):
	def __init__(self):
		super().__init__('Chromium', DATA_FOLDER, 'chromium.zip')

	def get_platform(self):
		platform_name = platform.system()

		if platform_name == 'Windows':
			if platform.architecture()[0] == '32bit':
				return 'Win'
			else:
				return 'Win_x64'
		elif platform_name == 'Darwin':
			if platform.machine() == 'arm64':
				return 'Mac_Arm'
			else:
				return 'Mac'
		elif platform_name == 'Linux':
			if platform.architecture()[0] == '32bit':
				return 'Linux'
			else:
				return 'Linux_x64'
		
		raise Exception('Platform not supported')
	
	def get_folder(self):
		platform_name = platform.system()

		if platform_name == 'Windows':
			return os.path.join(DATA_FOLDER, 'chrome-win')
		elif platform_name == 'Darwin':
			return os.path.join(DATA_FOLDER, 'chrome-mac')
		elif platform_name == 'Linux':
			return os.path.join(DATA_FOLDER, 'chrome-linux')
		
		raise Exception('Platform not supported')

	def run(self):
		super().run()

		platform = self.get_platform()	
		url = f'https://download-chromium.appspot.com/dl/{platform}?type=snapshots'
		self.download(url)
		self.unzip()
		self.clean_zip()

class UBlockDownloader(ZipDownloader):
	def __init__(self):
		super().__init__("uBlock Extension", DATA_FOLDER, 'ublock-extension.zip')

	def get_folder(self):
		return os.path.abspath(os.path.join(DATA_FOLDER, 'uBlock0.chromium'))

	def run(self):
		super().run()

		url = 'https://github.com/gorhill/uBlock/releases/download/1.62.0/uBlock0_1.62.0.chromium.zip'
		self.download(url)
		self.unzip()
		self.clean_zip()

class AdNauseamDownloader(ZipDownloader):
	def __init__(self):
		super().__init__("AdNauseam Extension", DATA_FOLDER, 'adnauseam-extension.zip')

	def get_folder(self):
		return os.path.abspath(os.path.join(DATA_FOLDER, 'adnauseam.chromium'))

	def run(self):
		super().run()

		url = 'https://github.com/dhowe/AdNauseam/releases/download/v3.24.4/adnauseam-3.24.4.chromium.zip'
		self.download(url)
		self.unzip()
		self.clean_zip()

class Chromium:
	def __init__(self):
		self.user_folder_name = 'chromium-user-data'
		self.remote_debugging_port = 9222

	@property
	def devtools_url(self):
		return f'http://localhost:{self.remote_debugging_port}/json'

	def get_user_folder(self):
		return os.path.abspath(os.path.join(DATA_FOLDER, self.user_folder_name))

	def create_user_folder(self, force=True):
		folder = self.get_user_folder()
		if os.path.exists(folder):
			if force:
				shutil.rmtree(folder)
			
			return

		os.makedirs(folder)

	def get_folder(self):
		platform_name = platform.system()

		if platform_name == 'Windows':
			return os.path.join(DATA_FOLDER, 'chrome-win')
		elif platform_name == 'Darwin':
			return os.path.join(DATA_FOLDER, 'chrome-mac')
		elif platform_name == 'Linux':
			return os.path.join(DATA_FOLDER, 'chrome-linux')
		
		raise Exception('Platform not supported')
	
	def args(self, tab_url, extensions_folders=[], expect_extensions_loaded=False):
		extension_folders_str = ','.join(extensions_folders)
		arguments = [
			os.path.join(self.get_folder(), "chrome.exe"), 
			f'--user-data-dir={self.get_user_folder()}', 
			f'--remote-debugging-port={self.remote_debugging_port}', 
			'--no-first-run', 
			'--disable-component-extensions-with-background-pages', 
			'--disable-default-apps',
			tab_url
		]

		if expect_extensions_loaded:
			arguments.insert(1, f'--disable-extensions-except={extension_folders_str}')
		elif len(extensions_folders) > 0:
			arguments.insert(1, f'--load-extension={extension_folders_str}')

		
		return arguments
	
	def dev_data(self):
		res = requests.get(self.devtools_url)

		if res.status_code != 200:
			raise Exception('Could not connect to Chromium')
		
		return res.json()
	
	def get_last_tab_id(self):
		data = self.dev_data()
		return data[0]['id']
	
	def close_tab(self, tab_id):
		requests.get(f'{self.devtools_url}/close/{tab_id}')

	def close_all_tabs(self):
		try:
			data = self.dev_data()
		except:
			return

		for tab in data:
			try:
				self.close_tab(tab['id'])
			except:
				return

chromium_dl = ChromiumDownloader()
ublock_dl = UBlockDownloader()
adnauseam_dl = AdNauseamDownloader()
chromium = Chromium()

chromium_dl.run()
ublock_dl.run()
adnauseam_dl.run()
chromium.create_user_folder()

print("Chromium will now open. Please take the following steps:")
print("1. If you get a warning about developer mode, you can turn it on in the top right of the screen.")
print("2. Please enable AdNauseam.")
print("3. AdNauseam will open a new tab. Please select all the options and click on 'Let's go!'")
print("4. Close the window.")
subprocess.run(chromium.args('chrome://extensions/', [adnauseam_dl.get_folder(), ublock_dl.get_folder()]))

print("Did everything go successfully? (y/n)")

response = input()
if response.lower() != 'y':
	print("Please try again.")
	subprocess.run(chromium.args('chrome://extensions/', [adnauseam_dl.get_folder(), ublock_dl.get_folder()]))

SITES = [
	"https://google.com",
	"https://bing.com",
	"https://reddit.com",
	"https://youtube.com",
]

ENERGIBRIDGE = r"C:\Users\JortvD\Downloads\energibridge-v0.0.7-x86_64-pc-windows-msvc\energibridge"

async def test():
	time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	output_file = os.path.join(OUTPUT_FOLDER, f'{time}.txt')
	args = [ENERGIBRIDGE, '-o', output_file, '--summary', '--gpu']
	args.extend(chromium.args('chrome://newtab', [adnauseam_dl.get_folder()], True))

	proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	# Give time for Chromium to open
	await asyncio.sleep(5)

	for site in SITES:
		subprocess.run(chromium.args(site))
		last_tab_id = chromium.get_last_tab_id()
		print(f'Opened {site} (ID: {last_tab_id})')

		# Give time for the tab to load
		await asyncio.sleep(10)

		chromium.close_tab(last_tab_id)
		print(f'Closed {site} (ID: {last_tab_id})')

		# Give time for the tab to close
		await asyncio.sleep(2)

	# Give time for the tabs to close
	await asyncio.sleep(5)

	# Close Chromium
	proc.kill()
	await asyncio.sleep(2)
	chromium.close_all_tabs()

asyncio.run(test())
