// Main JavaScript for Personal CRM

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Confirm delete actions
function confirmDelete(itemType, itemName) {
    return confirm(`Are you sure you want to delete this ${itemType}: "${itemName}"?\n\nThis action cannot be undone.`);
}

// Search functionality
function performSearch(query) {
    if (query.trim().length < 2) {
        alert('Please enter at least 2 characters to search');
        return false;
    }
    return true;
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return false;
    }
    return true;
}

// Dynamic field additions (for contacts, addresses, etc.)
function addContactField() {
    const container = document.getElementById('contact-fields');
    const newField = document.createElement('div');
    newField.className = 'row g-2 mb-2';
    newField.innerHTML = `
        <div class="col-md-4">
            <select class="form-select" name="contact_type[]">
                <option value="phone">Phone</option>
                <option value="email">Email</option>
                <option value="whatsapp">WhatsApp</option>
                <option value="telegram">Telegram</option>
            </select>
        </div>
        <div class="col-md-6">
            <input type="text" class="form-control" name="contact_value[]" placeholder="Value">
        </div>
        <div class="col-md-2">
            <button type="button" class="btn btn-danger" onclick="this.parentElement.parentElement.remove()">
                <i class="bi bi-trash"></i>
            </button>
        </div>
    `;
    container.appendChild(newField);
}

// Export data
function exportData(type) {
    // Placeholder for export functionality
    alert(`Exporting ${type} data... (Feature coming soon)`);
}

// Print functionality
function printPage() {
    window.print();
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        alert('Copied to clipboard!');
    }, function(err) {
        console.error('Could not copy text: ', err);
    });
}

// Date formatting
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Calculate age from DOB
function calculateAge(dob) {
    const birthDate = new Date(dob);
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    
    return age;
}

// Local storage helpers
function saveToLocalStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
        return true;
    } catch (e) {
        console.error('Error saving to localStorage:', e);
        return false;
    }
}

function getFromLocalStorage(key) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    } catch (e) {
        console.error('Error reading from localStorage:', e);
        return null;
    }
}

// Theme toggle (optional feature)
function toggleTheme() {
    const body = document.body;
    body.classList.toggle('dark-theme');
    const theme = body.classList.contains('dark-theme') ? 'dark' : 'light';
    saveToLocalStorage('theme', theme);
}

// Load saved theme
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = getFromLocalStorage('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
    }
});

// Map integration placeholder
function showOnMap(latitude, longitude, name) {
    const url = `https://www.google.com/maps/search/?api=1&query=${latitude},${longitude}`;
    window.open(url, '_blank');
}

// Statistics update
async function updateDashboardStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        document.getElementById('people-count').textContent = stats.people;
        document.getElementById('places-count').textContent = stats.places;
        document.getElementById('events-count').textContent = stats.events;
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
}

console.log('Personal CRM - JavaScript loaded successfully!');
