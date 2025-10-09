// MODAL INTERAÇÃO
const loginBtn = document.getElementById('nav-login-btn');
const modalBackdrop = document.getElementById('login-modal-backdrop');
const loginModal = document.getElementById('login-modal');
const closeModal = document.getElementById('close-login-modal');
const loginForm = document.getElementById('login-form');
const modalMsg = document.getElementById('modal-msg');

function showModal() {
    modalBackdrop.classList.add('active');
    // Reinicia a animação
    loginModal.style.animation = 'none';
    void loginModal.offsetWidth;
    loginModal.style.animation = '';
}

function hideModal() {
    modalBackdrop.classList.remove('active');
    setTimeout(() => { modalMsg.textContent = ""; }, 350);
}

loginBtn.onclick = showModal;
closeModal.onclick = hideModal;
modalBackdrop.onclick = function(e) {
    if (e.target === modalBackdrop) hideModal();
};

document.addEventListener('keydown', function(e) {
    if (modalBackdrop.classList.contains('active') && e.key === "Escape") hideModal();
});

loginForm.onsubmit = function(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value.trim();
    const senha = document.getElementById('login-senha').value;

    if (email && senha) {
        localStorage.setItem('songbox_login', JSON.stringify({ email, senha }));
        modalMsg.style.color = "#b4ee99";
        modalMsg.textContent = "Login salvo!";
        setTimeout(hideModal, 950);
    } else {
        modalMsg.style.color = "#f77";
        modalMsg.textContent = "Preencha todos os campos.";
    }
};

// Recupera login salvo ao carregar a página
window.onload = function() {
    try {
        const loginData = JSON.parse(localStorage.getItem('songbox_login') || null);
        if (loginData) {
            document.getElementById('login-email').value = loginData.email;
            document.getElementById('login-senha').value = loginData.senha;
        }
    } catch (err) {
        console.warn("Erro ao carregar login salvo:", err);
    }
};

// --- Download form ---
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const status = document.getElementById('status');
let statusInterval = null;

document.getElementById('formulario').addEventListener('submit', function(e) {
    e.preventDefault();
    const link = document.getElementById('link').value;
    const download = document.getElementById('download').value;

    // Recupera email e senha do localStorage
    const loginData = JSON.parse(localStorage.getItem('songbox_login') || null);
    const email = loginData?.email || '';
    const senha = loginData?.senha || '';

    if (!email || !senha) {
        status.textContent = "Erro: Faça login primeiro!";
        return;
    }

    status.textContent = "Iniciando download...";
    startBtn.style.display = 'none';
    stopBtn.style.display = '';
    stopBtn.disabled = false;

    fetch('/api/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ link, download, email, senha })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            status.textContent = "Baixando...";
            statusInterval = setInterval(() => {
                fetch('/api/status')
                .then(r => r.json())
                .then(s => {
                    if (!s.running) {
                        status.textContent = "Download concluído!";
                        startBtn.style.display = '';
                        stopBtn.style.display = 'none';
                        clearInterval(statusInterval);
                    }
                });
            }, 1500);
        } else {
            status.textContent = "Erro: " + (data.error || "Verifique o backend.");
            startBtn.style.display = '';
            stopBtn.style.display = 'none';
        }
    })
    .catch(err => {
        status.textContent = "Erro ao comunicar com o backend!";
        startBtn.style.display = '';
        stopBtn.style.display = 'none';
    });
});

stopBtn.addEventListener('click', () => {
    status.textContent = "Parando download...";
    stopBtn.disabled = true;
    fetch('/api/stop', { method: 'POST' })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            status.textContent = "Download parado.";
        } else {
            status.textContent = "Erro: " + (data.error || "Verifique o backend.");
        }
        startBtn.style.display = '';
        stopBtn.style.display = 'none';
        clearInterval(statusInterval);
    })
    .catch(() => {
        status.textContent = "Erro ao comunicar com o backend!";
        startBtn.style.display = '';
        stopBtn.style.display = 'none';
        clearInterval(statusInterval);
    });
});
