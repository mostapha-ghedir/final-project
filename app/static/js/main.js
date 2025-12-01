// Modern JavaScript for BookHub

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Add loading state to buttons
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
            submitBtn.disabled = true;
            
            // Re-enable after 3 seconds as fallback
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 3000);
        }
    });
});

// Add hover effects to cards
document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-2px)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});

// Auto-hide alerts after 5 seconds
document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
        alert.style.opacity = '0';
        setTimeout(() => {
            alert.remove();
        }, 300);
    }, 5000);
});

// Add search functionality enhancement
const searchInput = document.querySelector('input[name="query"]');
if (searchInput) {
    searchInput.addEventListener('input', function() {
        if (this.value.length > 2) {
            // Add search suggestions or live search here
            console.log('Searching for:', this.value);
        }
    });
}

// Favorite button animation
document.querySelectorAll('button[data-favorite]').forEach(btn => {
    btn.addEventListener('click', function() {
        const heart = this.querySelector('i');
        heart.classList.add('fa-beat');
        setTimeout(() => {
            heart.classList.remove('fa-beat');
        }, 1000);
    });
});

// Initialize tooltips if Bootstrap is available
if (typeof bootstrap !== 'undefined') {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Add intersection observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.card, .hero-section').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

console.log('BookHub JavaScript loaded successfully! 📚');