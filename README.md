# 🎵 Download Songbox Link (Songbox Web Scraper)

Aplicação em **Python + Flask + Selenium** para realizar **web scraping** e baixar músicas da plataforma **Songbox**.

A interface web permite informar o link de download e a pasta onde os arquivos serão salvos, com suporte para **iniciar e parar downloads**.

***
## 📂 Estrutura do Projeto
.
├── server.py # Backend Flask com API para iniciar/parar downloads
├── bll.py # Lógica de scraping e download (Selenium)
├── web_base.py # Classe utilitária para interação com Selenium
├── static/
│ ├── index.html # Interface web do app
│ ├── logo.png # Logo exibida na interface
└── README.md # Documentação do projeto
***

## 🚀 Tecnologias Utilizadas

- **Python 3.10+**
- **Flask** (backend e API REST)
- **Flask-CORS**
- **Selenium WebDriver**
- **HTML/CSS/JavaScript** (frontend)
- **Threading** para execução assíncrona dos downloads

***
## 📌 Pré-requisitos

Antes de iniciar, você precisa ter instalado:

- [Python](https://www.python.org/)
- [Google Chrome](https://www.google.com/chrome/) (ou outro navegador compatível)
- [ChromeDriver](https://chromedriver.chromium.org/) ou WebDriver equivalente  
- Pip instalado no Python
***

## 🔧 Instalação

1. **Clone este repositório**
    ```
    git clone https://github.com/DevAlexFR/Download_Sondbox_Link.git
    ```

2. **Crie um ambiente virtual (opcional, mas recomendado)**
    ```
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```

3. **Instale as dependências**
    ```
    pip install -r requirements-dev.txt
    ```

***
## ▶️ Execução

1. **No terminal, execute:**
    ```
    python project/server.py
    ```

2. **O servidor Flask iniciará por padrão em:**
    ```
    http://127.0.0.1:5000
    ```

***
## ⚠️ Aviso Importante!
- Este projeto é apenas para fins educacionais!!!
***

## ✨ Autor
**Desenvolvido por:** @DevAlexFR 
📅 **Ano:** 2025  
🚀 **Licença:** MIT
