import os
import threading

from web_base import WebBase
from selenium.webdriver.common.by import By
from time import sleep



def download(link: str, download: str, stop_callback=None):
    wb = WebBase(download_path=download, anonimus=False, hidden=True, browser='Chrome', auto_update=True)
    wb.start_driver()
    wb.navigate(link)
    wb.full_loading()

    # Espera botão "Entrar"
    wb.wait(By.XPATH, "//button[text()[contains(.,'Entrar')]]")

    tracks = wb.driver.find_elements(By.CSS_SELECTOR, '#tracklist [data-track-id]')

    if tracks:
        for index, track in enumerate(tracks):
            if stop_callback and stop_callback():
                print("Download interrompido.")
                wb.driver.quit()
                return

            if track.tag_name == 'div':
                name = track.text
                continue

            wb.driver.execute_script("arguments[0].click();", track)
            sleep(3)

            if stop_callback and stop_callback():
                print("Download interrompido.")
                wb.driver.quit()
                return

            wb.wait(By.ID, 'waveform')
            el = wb.driver.find_element(By.CSS_SELECTOR, '#waveform > div')
            shadow_root = el.shadow_root
            audio_el = shadow_root.find_element(By.CSS_SELECTOR, 'audio')
            blob_src = audio_el.get_attribute('src')

            js_code = f"""
            fetch('{blob_src}')
            .then(response => response.blob())
            .then(blob => {{
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = '{name}.wav';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            }})
            .catch(() => alert('Erro ao baixar o áudio'));
            """

            if not name:
                continue

            wb.driver.execute_script(js_code)
            sleep(3)

            for arquivo in os.listdir(download):
                caminho_arquivo = os.path.join(download, arquivo)
                if os.path.isfile(caminho_arquivo) and arquivo.lower().endswith(".m4a"):
                    os.remove(caminho_arquivo)
                    print(f"Removido: {caminho_arquivo}")
    wb.driver.quit()
