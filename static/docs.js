// Initialize syntax highlighting
document.addEventListener('DOMContentLoaded', function() {
    hljs.highlightAll();
    
    // Smooth scroll for sidebar links
    document.querySelectorAll('.sidebar-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // Active sidebar link on scroll
    const sections = document.querySelectorAll('.section');
    const sidebarLinks = document.querySelectorAll('.sidebar-link');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (window.pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });

        sidebarLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
});

// Copy code to clipboard
function copyCode(button) {
    const codeBlock = button.closest('.code-block');
    const code = codeBlock.querySelector('code').textContent;
    
    navigator.clipboard.writeText(code).then(() => {
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        button.style.background = '#10b981';
        
        setTimeout(() => {
            button.textContent = originalText;
            button.style.background = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        button.textContent = 'Failed';
        setTimeout(() => {
            button.textContent = 'Copy';
        }, 2000);
    });
}

// Try API functionality
async function tryAPI() {
    const uid = document.getElementById('tryUid').value.trim();
    const resultDiv = document.getElementById('tryResult');
    const tryBtn = document.getElementById('tryBtn');
    
    if (!uid) {
        resultDiv.textContent = 'Please enter a UID';
        resultDiv.style.color = '#ef4444';
        return;
    }
    
    // Show loading state
    tryBtn.disabled = true;
    tryBtn.textContent = 'Loading...';
    resultDiv.textContent = 'Fetching data...';
    resultDiv.style.color = '#94a3b8';
    
    try {
        const response = await fetch(`/bancheck?uid=${uid}`);
        const data = await response.json();
        
        if (response.ok) {
            resultDiv.textContent = JSON.stringify(data, null, 2);
            resultDiv.style.color = '#10b981';
        } else {
            resultDiv.textContent = JSON.stringify(data, null, 2);
            resultDiv.style.color = '#ef4444';
        }
    } catch (error) {
        resultDiv.textContent = `Error: ${error.message}`;
        resultDiv.style.color = '#ef4444';
    } finally {
        tryBtn.disabled = false;
        tryBtn.textContent = 'Try API';
    }
}

// Add Enter key support for Try API
document.addEventListener('DOMContentLoaded', function() {
    const tryUidInput = document.getElementById('tryUid');
    if (tryUidInput) {
        tryUidInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                tryAPI();
            }
        });
    }
});

// Add active class to sidebar links
document.addEventListener('DOMContentLoaded', function() {
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            sidebarLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
});
