// Elementos DOM
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const fileName = document.getElementById('fileName');
const textInput = document.getElementById('textInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const loading = document.getElementById('loading');
const categoryBadge = document.getElementById('categoryBadge');
const confidence = document.getElementById('confidence');
const responseContent = document.getElementById('responseContent');
const previewBox = document.getElementById('previewBox');
const copyBtn = document.getElementById('copyBtn');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');
const historyList = document.getElementById('historyList');
const toast = document.getElementById('toast');

// Tabs
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

// Histórico
let history = JSON.parse(localStorage.getItem('emailHistory')) || [];

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    setupTabs();
    setupUpload();
    setupTextInput();
    loadHistory();
    checkInputs();
});

// Configurar tabs
function setupTabs() {
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            
            // Atualizar botões
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Atualizar conteúdo
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === `${tabName}-tab`) {
                    content.classList.add('active');
                }
            });
            
            checkInputs();
        });
    });
}

// Configurar upload
function setupUpload() {
    uploadArea.addEventListener('click', () => fileInput.click());
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
}

function handleFileSelect(file) {
    if (!file.name.match(/\.(txt|pdf)$/i)) {
        showToast('Formato não suportado. Use .txt ou .pdf', 'error');
        return;
    }
    
    if (file.size > 5 * 1024 * 1024) {
        showToast('Arquivo muito grande. Máximo: 5MB', 'error');
        return;
    }
    
    fileName.textContent = `📄 ${file.name}`;
    fileName.classList.add('show');
    checkInputs();
}

// Configurar input de texto
function setupTextInput() {
    textInput.addEventListener('input', checkInputs);
}

function checkInputs() {
    const activeTab = document.querySelector('.tab-btn.active').dataset.tab;
    let hasInput = false;
    
    if (activeTab === 'upload') {
        hasInput = fileInput.files.length > 0;
    } else {
        hasInput = textInput.value.trim().length > 0;
    }
    
    analyzeBtn.disabled = !hasInput;
}

// Analisar email
analyzeBtn.addEventListener('click', async () => {
    const activeTab = document.querySelector('.tab-btn.active').dataset.tab;
    let formData = new FormData();
    
    if (activeTab === 'upload') {
        if (fileInput.files.length === 0) {
            showToast('Selecione um arquivo', 'error');
            return;
        }
        formData.append('file', fileInput.files[0]);
    } else {
        const text = textInput.value.trim();
        if (!text) {
            showToast('Digite ou cole o texto do email', 'error');
            return;
        }
        formData.append('text', text);
    }
    
    // Mostrar loading
    loading.style.display = 'block';
    resultsSection.style.display = 'none';
    analyzeBtn.disabled = true;
    
    try {
        let response;
        if (activeTab === 'upload') {
            response = await fetch('/api/classify', {
                method: 'POST',
                body: formData
            });
        } else {
            response = await fetch('/api/classify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: textInput.value.trim() })
            });
        }
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Erro ao processar');
        }
        
        // Exibir resultados
        displayResults(data);
        
        // Salvar no histórico
        addToHistory(data);
        
        showToast('Análise concluída com sucesso!', 'success');
        
    } catch (error) {
        showToast(`Erro: ${error.message}`, 'error');
        console.error('Erro:', error);
    } finally {
        loading.style.display = 'none';
        analyzeBtn.disabled = false;
    }
});

// Exibir resultados
function displayResults(data) {
    // Categoria
    const category = data.category.toLowerCase();
    categoryBadge.textContent = data.category;
    categoryBadge.className = `category-badge ${category}`;
    
    // Confiança
    confidence.textContent = `Confiança: ${data.confidence}%`;
    
    // Resposta
    responseContent.textContent = data.response;
    
    // Preview
    previewBox.textContent = data.original_text;
    
    // Mostrar seção de resultados
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Copiar resposta
copyBtn.addEventListener('click', () => {
    const text = responseContent.textContent;
    navigator.clipboard.writeText(text).then(() => {
        showToast('Resposta copiada!', 'success');
        copyBtn.innerHTML = '<i class="fas fa-check"></i>';
        setTimeout(() => {
            copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
        }, 2000);
    });
});

// Nova análise
newAnalysisBtn.addEventListener('click', () => {
    resultsSection.style.display = 'none';
    fileInput.value = '';
    fileName.textContent = '';
    fileName.classList.remove('show');
    textInput.value = '';
    checkInputs();
    
    // Voltar para o topo
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Histórico
function addToHistory(data) {
    const historyItem = {
        id: Date.now(),
        category: data.category,
        confidence: data.confidence,
        preview: data.original_text,
        response: data.response,
        date: new Date().toLocaleString('pt-BR')
    };
    
    history.unshift(historyItem);
    
    // Manter apenas os últimos 10
    if (history.length > 10) {
        history = history.slice(0, 10);
    }
    
    localStorage.setItem('emailHistory', JSON.stringify(history));
    loadHistory();
}

function loadHistory() {
    if (history.length === 0) {
        historyList.innerHTML = '<p class="empty-history">Nenhuma análise realizada ainda</p>';
        return;
    }
    
    historyList.innerHTML = history.map(item => `
        <div class="history-item" onclick="loadHistoryItem(${item.id})">
            <div class="history-item-header">
                <span class="history-category category-badge ${item.category.toLowerCase()}">
                    ${item.category}
                </span>
                <span class="history-date">${item.date}</span>
            </div>
            <div class="history-preview">${item.preview}</div>
        </div>
    `).join('');
}

function loadHistoryItem(id) {
    const item = history.find(h => h.id === id);
    if (!item) return;
    
    displayResults({
        category: item.category,
        confidence: item.confidence,
        response: item.response,
        original_text: item.preview
    });
    
    showToast('Item do histórico carregado', 'success');
}

// Toast
function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
