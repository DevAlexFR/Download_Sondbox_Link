import os

from selenium.webdriver.common.by import By
from time import sleep
from web_base import WebBase
from flask import Flask, request, jsonify, send_from_directory
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import re

def login(wb: WebBase, link, email_str, senha_str):
    wb.start_driver()
    wb.navigate(link)
    wb.full_loading()

    sleep(1)
    close_button = WebDriverWait(wb.driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH,
            "(//button[contains(@class, 'inline-flex') and contains(@class, 'items-center') and contains(@class, 'justify-center')])[1]"
        ))
    )

    close_button.click()
    sleep(3)

    wb.wait(By.XPATH, "//div[contains(@class, 'flex')]/button[contains(text(),'Entrar')]")
    enter = wb.driver.find_element(By.XPATH, "//div[contains(@class, 'flex')]/button[contains(text(),'Entrar')]")
    enter.click()

    wb.wait(By.ID, "email")
    email_input = wb.driver.find_element(By.ID, 'email')
    email_input.send_keys(email_str)

    wb.wait(By.ID, "password")
    password_input = wb.driver.find_element(By.ID, 'password')
    password_input.send_keys(senha_str)

    wb.wait(By.CSS_SELECTOR, "button.bg-gradient-primary")
    enter_login = wb.driver.find_element(By.CSS_SELECTOR, "button.bg-gradient-primary")
    try:
        enter_login.click()
    except:
        wb.driver.execute_script("arguments[0].click();", enter_login)


def download(email:str, senha:str, link: str, download: str, stop_callback=None):
    wb = WebBase(download_path=download, anonimus=True, hidden=True, browser='Chrome', auto_update=True)
    login(wb, link, email, senha)
    sleep(2)
    wb.full_loading()

    # Play na primeira musica
    download_btn = WebDriverWait(wb.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class, 'inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 hover:text-accent-foreground h-8 w-8 sm:h-10 sm:w-10 rounded-full bg-primary/10 hover:bg-primary/20 flex-shrink-0')])[1]"))
    )
    download_btn.click()

    # Maximizar
    wb.driver.execute_script("""
        const btn = document.querySelector("button .lucide-maximize2");
        if (btn) btn.closest("button").click();
    """)

    contador = 1
    while True:

        sleep(5)
        titulo = WebDriverWait(wb.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//h1[contains(@class, 'text-3xl') and contains(@class, 'font-bold') and contains(@class, 'mb-2')])[2]"))
        ).text.strip()
        safe_titulo = re.sub(r'[\\/:"*?<>|]+', '_', titulo)

        try:
            categoria = wb.driver.find_element(By.XPATH, "//h4[contains(@class, 'font-medium')]/following-sibling::p").text.strip()
            safe_categoria = re.sub(r'[\\/:"*?<>|]+', '_', categoria)
            filename = f"{safe_titulo} - {safe_categoria}.mp3"
        except:
            filename = f"{safe_titulo}.mp3"

        filepath = os.path.join(download, filename)

        try:
            audio_el = WebDriverWait(wb.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "audio"))
            )
            audio_url = audio_el.get_attribute("src")
            print(f"Baixando {contador}: {filename}")

            response = requests.get(audio_url)
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"✅ Salvo: {filename}")
        except Exception as e:
            print(f"❌ Falha ao baixar {filename}: {e}")

        try:
            next_button = wb.driver.find_element(By.XPATH, "//button[@title='Próxima faixa' and not(@disabled)]")
            next_button.click()
            print("➡️ Próxima faixa...")
        except:
            print("⏭️ Última faixa alcançada.")
            break

        sleep(5)
        contador += 1

    try:
        wb.driver.close()
    except:
        pass
    wb.driver.quit()
