import argparse
import asyncio
import json
import os
import platform
import signal
import time
import requests
import progressbar
import zipfile
import subprocess
import shutil
import datetime
import random
import psutil

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

	def unzip(self, folder=None):
		if not self.force_unzip and os.path.exists(self.get_folder()):
			print(f'{self.name} already unzipped. Skipping unzip')
			return

		print(f'Unzipping {self.name}')
		zip_path = os.path.join(DATA_FOLDER, self.zip_name)
		to = os.path.join(DATA_FOLDER, folder) if folder else DATA_FOLDER
		with zipfile.ZipFile(zip_path, 'r') as zip_ref:
			zip_ref.extractall(to)

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

class GhosteryDownloader(ZipDownloader):
	def __init__(self):
		super().__init__("Ghostery Extension", DATA_FOLDER, 'ghostery-extension.zip')

	def get_folder(self):
		return os.path.abspath(os.path.join(DATA_FOLDER, 'ghostery.chromium'))

	def run(self):
		super().run()

		url = 'https://github.com/ghostery/ghostery-extension/releases/download/v10.4.25/ghostery-chromium-10.4.25.zip'
		self.download(url)
		self.unzip("ghostery.chromium")
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
	
	def get_executable(self):
		platform_name = platform.system()

		if platform_name == 'Windows':
			return os.path.join(self.get_folder(), 'chrome.exe')
		elif platform_name == 'Darwin':
			return os.path.join(self.get_folder(), 'Chromium.app', 'Contents', 'MacOS', 'Chromium')
		elif platform_name == 'Linux':
			return os.path.join(self.get_folder(), 'chrome')
		
		raise Exception('Platform not supported')
	
	def args(self, tab_url, extensions_folders=[], expect_extensions_loaded=False):
		extensions_folders = [folder for folder in extensions_folders if folder is not None]
		extension_folders_str = ','.join(extensions_folders) if extensions_folders is not None else ''
		arguments = [
			self.get_executable(), 
			'--disable-background-networking',
			'--disable-background-timer-throttling',
			f'--remote-debugging-port={self.remote_debugging_port}', 
			'--no-first-run', 
			'--disable-component-extensions-with-background-pages', 
			'--disable-default-apps',
			tab_url
		]
		if platform.system() == 'Windows':
			arguments.append(f'--user-data-dir={self.get_user_folder()}')
		if extensions_folders is None or len(extensions_folders) > 0:
			arguments.insert(1, f'--disable-extensions-except={extension_folders_str}')
			arguments.insert(1, f'--load-extension={extension_folders_str}')
		else:
			arguments.insert(1, '--disable-extensions')
		
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

class Step:
	def __init__(self, index: int, folder: str, chromium: Chromium, site_set_index: int, site_set: list[str] = [], extension_folder_index: int = 0, extension_folder: str|None=None):
		self.index = index
		self.chromium = chromium
		self.folder = folder
		self.site_set_index = site_set_index
		self.site_set = site_set
		self.extension_folder_index = extension_folder_index
		self.extension_folder = extension_folder

	async def run(self):
		start_time = time.time()
		output_file = os.path.join(self.folder, f'{self.index}_{self.site_set_index}_{self.extension_folder_index}.csv')
		args = [ENERGIBRIDGE, '-o', output_file, '--summary']
		args.extend(self.chromium.args('chrome://newtab', [self.extension_folder], False))
		print(f'> Starting Chromium through Energibridge -> {output_file}')
		proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		# Give time for Chromium to open
		await asyncio.sleep(5)

		for site in self.site_set:
			print(f'> Opening {site}')
			subprocess.run(self.chromium.args(site))
			# Give time for the tab to load
			await asyncio.sleep(5)
			
			last_tab_id = self.chromium.get_last_tab_id()
			self.chromium.close_tab(last_tab_id)

			# Give time for the tab to close
			await asyncio.sleep(1)

		# Close Chromium
		print('> Closing Chromium')
		proc.kill()
		await asyncio.sleep(1)
		stdout, stderr = proc.communicate()
		print("> EnergiBridge stderr:")
		print(stderr.decode('utf-8')) 
		self.chromium.close_all_tabs()
		await asyncio.sleep(5)
		end_time = time.time()
		print(f'=> Step took {end_time - start_time:.2f} seconds')

class StepSet:
	def __init__(self, index, n_sets, folder, site_sets, extension_folders):
		self.index = index
		self.n_sets = n_sets
		self.folder = folder
		self.chromium = Chromium()
		self.steps = []
		self.extension_folders = extension_folders
		self.site_sets = site_sets

		for i, site_set in enumerate(site_sets):
			for j, extension_folder in enumerate(extension_folders):
				self.steps.append(Step(index, folder, self.chromium, i, site_sets[site_set], j, extension_folder))
		
		random.seed(self.index)
		random.shuffle(self.steps)

		index_pairs = [f"({step.site_set_index}, {step.extension_folder_index})" for step in self.steps]
		print(f'Set {self.index + 1}/{n_sets} has {len(self.steps)} steps with ordering {", ".join(index_pairs)}')

	def update_preferences(self):
		print('> Updating Preferences file to turn on all extensions')
		preferences_file = os.path.join(self.chromium.get_user_folder(), 'Default', 'Preferences')

		with open(preferences_file, 'r') as file:
			try:
				data = json.loads(file.read())
			except:
				raise Exception('Could not parse Preferences file')
				
			if not 'extensions' in data or not 'settings' in data['extensions']:
				raise Exception('Could not update Preferences file')
			
			data['extensions']['ui'] = {
				'developer_mode': True
			}
			
			settings = data['extensions']['settings']

			for key in settings:
				settings[key]['state'] = 1

		with open(preferences_file, 'w') as file:
			json.dump(data, file, indent=4)

	async def reset_user_data(self):
		print('> Resetting user data by deleting old folder')
		self.chromium.create_user_folder()
		args = self.chromium.args('chrome://newtab', self.extension_folders)
		print(f'> Starting Chromium to generate user data')
		proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		await asyncio.sleep(15)

		print('> Closing Chromium gracefully to generate Preferences file')
		parent = psutil.Process(proc.pid)
		for child in parent.children(recursive=True):
			try:
				child.kill()
			except:
				break
		await asyncio.sleep(1)
		self.chromium.close_all_tabs()
		await asyncio.sleep(3)
		
		if platform.system() == 'Windows':
			self.update_preferences()

	async def run(self):
		start_time = time.time()
		await self.reset_user_data()

		for i, step in enumerate(self.steps):
			print(f'Step {i + 1}/{len(self.steps)} (of total {self.n_sets * len(self.steps)}) -> options: {step.site_set_index}, {step.extension_folder_index}')
			
			await self.reset_user_data()
			await step.run()

			# Give time for the system to cool down
			await asyncio.sleep(15)

		end_time = time.time()
		print(f'=> Set {self.index + 1}/{self.n_sets} took {end_time - start_time:.2f} seconds')

class Experiment:
	SITES = {
		"HIGH": [
			# "https://www.reuters.com/business/media-telecom/amazons-mgm-studios-take-creative-control-over-james-bond-franchise-2025-02-20/", # 35
			"https://www.msn.com/nl-nl", # 44
			"https://apnews.com/article/exercise-recovery-injury-workout-rest-2ffce1799725037b0142657db62d9e8d", # 72
			"https://www.npr.org/2025/02/15/nx-s1-5262600/movie-watch-six-spring-movies-to-get-excited-about", # 65
		],
		"MEDIUM": [
			"https://www.vice.com/en/article/pga-tour-2k25-is-a-proper-birdie-and-its-so-close-to-being-a-hole-in-one-review/", # 22
			"https://www.nytimes.com/2025/02/19/well/move/zone-2-exercise-benefits.html", # 17
			"https://time.com/7252972/american-murder-gabby-petito-true-story-netflix/", # 21
		],
		"LOW": [
			"https://www.nasa.gov/image-article/our-pale-blue-dot/", # 4
			"https://www.bellingcat.com/news/2024/12/18/ukraine-outraged-at-yemen-grain-shipment-from-occupied-crimea/", # 3
			"https://commission.europa.eu/topics/agriculture-and-rural-development/future-agriculture_en", # 0

			# "https://www.axios.com/2025/02/20/trump-tariffs-ceo-confidence", # 6
			# "https://www.propublica.org/article/trump-refugee-executive-order-afghan-allies", # 10
			# "https://www.vox.com/scotus/400323/supreme-court-trump-hampton-dellinger-unitary-executive", # 15
			# "https://arstechnica.com/gadgets/2025/02/what-i-do-to-clean-up-a-clean-install-of-windows-11-23h2-and-edge/", # 10
			# "https://www.technologyreview.com/2025/02/19/1112072/a-new-microsoft-chip-could-lead-to-more-stable-quantum-computers/", # 4
			# "https://www.theguardian.com/tv-and-radio/2025/feb/20/italy-estonia-offensive-eurovision-entry-tommy-cash", # 15
		],
	}

	def __init__(self, folder, n_sets, add_warmup=True, index=0):
		self.folder = folder
		self.n_sets = n_sets
		self.add_warmup = add_warmup
		self.index = index

	async def run(self):
		chromium_dl = ChromiumDownloader()
		extensions = [
			UBlockDownloader(),
		]

		chromium_dl.run()
		for extension in extensions:
			extension.run()

		if not os.path.exists(self.folder):
			os.makedirs(self.folder)

		time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
		folder = os.path.join(self.folder, time)

		if not os.path.exists(folder):
			os.makedirs(folder)

		if self.add_warmup:
			self.n_sets += 1

		extension_folders = [None] + [extension.get_folder() for extension in extensions]

		for i in range(self.n_sets - self.index):
			i = self.index + i
			print(f'Set {i + 1}/{self.n_sets}')
			step_set = StepSet(i, self.n_sets, folder, self.SITES, extension_folders)
			await step_set.run()

args_def = argparse.ArgumentParser(description='Run our experiment with the Energibridge tool')
args_def.add_argument('--temp-dir', type=str, help='Temporary folder', default='data')
args_def.add_argument('-o', '--output', type=str, help='Output folder', default='output')
args_def.add_argument('-n', '--n-sets', type=int, help='Number of sets', default=1)
args_def.add_argument('--add-warmup', action='store_true', help='Round one round as warmup', default=True)
args_def.add_argument('-e', '--energibridge', type=str, help='Path to Energibridge executable', default=r"C:\Users\20202571\Downloads\energibridge-v0.0.7-x86_64-pc-windows-msvc\energibridge")
args_def.add_argument('--index', type=int, help='Index of the experiment', default=0)
args = args_def.parse_args()

if __name__ == '__main__':
	DATA_FOLDER = args.temp_dir

	if not os.path.exists(DATA_FOLDER):
		os.makedirs(DATA_FOLDER)

	OUTPUT_FOLDER = args.output

	if not os.path.exists(OUTPUT_FOLDER):
		os.makedirs(OUTPUT_FOLDER)

	ENERGIBRIDGE = args.energibridge

	asyncio.run(Experiment(OUTPUT_FOLDER, args.n_sets, args.add_warmup, args.index).run())
