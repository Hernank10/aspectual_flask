// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Función para actualizar estadísticas
function updateStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            document.querySelectorAll('[data-stat="total"]').forEach(el => {
                el.textContent = data.total_attempts;
            });
            document.querySelectorAll('[data-stat="correct"]').forEach(el => {
                el.textContent = data.correct_answers;
            });
            document.querySelectorAll('[data-stat="percentage"]').forEach(el => {
                el.textContent = data.percentage + '%';
            });
        });
}

// Validación de formularios
document.addEventListener('DOMContentLoaded', function() {
    // Validar respuestas en tiempo real
    const inputs = document.querySelectorAll('input[type="text"]');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value.length > 0) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
            }
        });
    });
    
    // Smooth scroll para enlaces internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
    
    // Cargar estadísticas iniciales
    updateStats();
});

// Guardar progreso en localStorage
function saveProgress(exerciseId, correct) {
    let progress = JSON.parse(localStorage.getItem('aspectual_progress') || '{}');
    progress[exerciseId] = {
        completed: true,
        correct: correct,
        timestamp: new Date().toISOString()
    };
    localStorage.setItem('aspectual_progress', JSON.stringify(progress));
}

// Cargar progreso guardado
function loadProgress() {
    return JSON.parse(localStorage.getItem('aspectual_progress') || '{}');
}

// Mostrar progreso
function showProgress() {
    const progress = loadProgress();
    const total = Object.keys(progress).length;
    const correct = Object.values(progress).filter(p => p.correct).length;
    
    if (total > 0) {
        const progressBar = document.getElementById('progress-bar');
        if (progressBar) {
            const percentage = (correct / total) * 100;
            progressBar.style.width = percentage + '%';
            progressBar.textContent = Math.round(percentage) + '%';
        }
    }
}

// Exportar funciones para uso global
window.showNotification = showNotification;
window.updateStats = updateStats;
window.saveProgress = saveProgress;
window.loadProgress = loadProgress;
window.showProgress = showProgress;
