import sys
import pandas as pd
import re
import undetected_chromedriver as uc
import subprocess
import shutil

from pathlib import Path
from time import time
from json import dumps
from selenium.common.exceptions import (
    InvalidArgumentException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver import Chrome, Edge, Ie, IeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.ie.service import Service as IeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
# from web_base.zones import disable_protected_mode


sys.path.insert(0, str(Path(__file__).parent.absolute().parent.absolute()))

def get_chrome_version_hidden():
    chrome_paths = [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
    ]

    for path in chrome_paths:
        if path.exists():
            try:
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # oculta a janela do console no Windows

                result = subprocess.run(
                    [str(path), '--version'],
                    capture_output=True,
                    text=True,
                    timeout=0,
                    startupinfo=si  # uso do startupinfo para esconder a janela
                )
                output = result.stdout.strip() or result.stderr.strip()
                match = re.search(r'\d+\.\d+\.\d+', output)
                if match:
                    return match.group(0)
            except subprocess.TimeoutExpired:
                continue
    return None



class ToolsWeb:
    def timeout(func):
        def inner(self, *args, **kwargs):
            delay = float(kwargs.pop("timeout", 10))
            check_instance = kwargs.pop("check_instance", False)
            instance = kwargs.pop("instance", pd.DataFrame)
            recursive = kwargs.pop("recursive", False)

            timeout_time = time() + delay
            result = None
            while True:
                if time() > timeout_time:
                    break
                try:
                    if recursive:
                        result, exit_flag = func(self, result, *args, **kwargs)
                    else:
                        result = func(self, *args, **kwargs)
                        exit_flag = result
                except Exception:
                    continue
                if check_instance and isinstance(result, instance):
                    break
                if not isinstance(exit_flag, bool):
                    continue
                elif exit_flag:
                    break
            return result
        return inner

    def loop_repet(func):
        def inner(self, *args, **kwargs):
            count = kwargs.get("count", 3)
            for _ in range(count):
                if func(self, *args, **kwargs):
                    return True
            return False
        return inner

    def print_time(func):
        def inner(self, *args, **kw):
            start = time()
            result = func(self, *args, **kw)
            return result
        return inner


class WebBaseConfig(ToolsWeb):
    def __init__(self, download_path='', anonimus=True, hidden=False, browser='Chrome', auto_update=True):
        self.browser = browser.capitalize()
        self.auto_update = auto_update

        temp_profile = Path.cwd() / "selenium_temp_profile"
        if temp_profile.exists():
            shutil.rmtree(temp_profile, ignore_errors=True)

        if self.browser == 'Chrome':
            self.options = uc.ChromeOptions()
            self.options.add_argument('--no-first-run')
            self.options.add_argument('--no-default-browser-check')
            self.options.add_argument('--disable-features=AutoClientProfileSelection,EnableProfilePickerOnStartup,PasswordImport')
            self.options.add_argument('--disable-popup-blocking')
            self.options.add_argument('--disable-extensions')
            self.options.add_argument('--disable-infobars')
            self.options.add_argument(f'--user-data-dir={str(temp_profile)}')
            self.options.add_argument('--profile-directory=Default')
            self.options.add_argument('--mute-audio')
            self.options.add_argument("--use-fake-ui-for-media-stream")


            self.driver_config = uc.Chrome
        
        if hidden:
            self.options.add_argument('--headless=new')

        if download_path:
            prefs = {
                "download.default_directory": download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
                "profile.default_content_setting_values.automatic_downloads": 1,
            }
            self.options.add_experimental_option('prefs', prefs)


        if anonimus:
            self.options.add_argument('--incognito')


class WebBase(WebBaseConfig):
    def start_driver(self):
        chrome_version = get_chrome_version_hidden()
        version_main = None
        if chrome_version:
            version_main = int(chrome_version.split('.')[0])

        if self.browser == 'Ie':
            self.driver = self.driver_config(service=self.service, options=self.options)
        elif self.auto_update:
            if version_main:
                self.driver = self.driver_config(options=self.options, version_main=version_main)
            else:
                self.driver = self.driver_config(options=self.options)
        else:
            self.driver = self.driver_config(
                options=self.options,
                driver_executable_path=self.driver_path,
                browser_executable_path=self.binary_location
            )
        self.status = True

    def validate_driver(self):
        try:
            return bool(self.driver.current_url)
        except:
            return False

    def navigate(self, url):
        try:
            self.driver.get(url)
            self.full_loading()
            return True
        except (TimeoutException, WebDriverException):
            return False

    def full_loading(self, delay=10):
        WebDriverWait(self.driver, delay).until(
            lambda _: self.driver.execute_script('return document.readyState') == 'complete'
        )

    def wait(self, by, element, present=True):
        try:
            WebDriverWait(self.driver, 0.5).until(
                EC.presence_of_element_located((by, element))
            )
            if present:
                return True
        except InvalidArgumentException:
            if not present:
                return True
        except TimeoutException:
            if present:
                return False
            return True
        return False

    def click_js(self, by, element):
        if not self.wait(by, element):
            return False
        self.driver.execute_script(
            'arguments[0].click();', self.driver.find_element(by, element)
        )
        return True
    
    def wait_blob(self, driver):
        return driver.execute_script("""
            const host = document.getElementById('waveform');
            if(!host) return false;
            const shadow = host.shadowRoot;
            if(!shadow) return false;
            const audio = shadow.querySelector('audio');
            if(!audio) return false;
            return !!audio.src && audio.src.startsWith('blob:') ? audio.src : false;
        """)

    
if __name__ == '__main__':

# ------------------------
# Função para detectar a versão do Chrome instalada
# ------------------------
    def get_chrome_version_hidden():
        chrome_paths = [
            Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
            Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
        ]

        for path in chrome_paths:
            if path.exists():
                try:
                    si = subprocess.STARTUPINFO()
                    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # oculta a janela do console no Windows

                    result = subprocess.run(
                        [str(path), '--version'],
                        capture_output=True,
                        text=True,
                        timeout=0,
                        startupinfo=si  # uso do startupinfo para esconder a janela
                    )
                    output = result.stdout.strip() or result.stderr.strip()
                    match = re.search(r'\d+\.\d+\.\d+', output)
                    if match:
                        return match.group(0)
                except subprocess.TimeoutExpired:
                    continue
        return None

    get_chrome_version_hidden()