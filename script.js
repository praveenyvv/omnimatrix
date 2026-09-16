/**
 * OmniMatrix Technologies — Interactive Core Scripts
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Header scroll effect
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 30) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // 2. Video Autoplay Reliability Assurance
    const heroVideo = document.getElementById('heroVideo');
    if (heroVideo) {
        heroVideo.muted = true;
        const playPromise = heroVideo.play();
        if (playPromise !== undefined) {
            playPromise.catch(() => {
                // Autoplay was prevented, retry on first user interaction
                const enableVideoPlay = () => {
                    heroVideo.play();
                    document.removeEventListener('click', enableVideoPlay);
                    document.removeEventListener('touchstart', enableVideoPlay);
                    document.removeEventListener('scroll', enableVideoPlay);
                };
                document.addEventListener('click', enableVideoPlay, { once: true });
                document.addEventListener('touchstart', enableVideoPlay, { once: true });
                document.addEventListener('scroll', enableVideoPlay, { once: true });
            });
        }
    }

    // 3. Mobile Hamburger Menu Toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isOpen = navLinks.classList.toggle('active');
            mobileMenuBtn.classList.toggle('active', isOpen);
            document.body.style.overflow = isOpen ? 'hidden' : '';
        });

        // Dropdown toggle on mobile
        document.querySelectorAll('.nav-dropdown-trigger').forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    e.stopPropagation();
                    const parent = trigger.closest('.nav-dropdown-item');
                    if (parent) {
                        parent.classList.toggle('open');
                    }
                }
            });
        });

        // Close on link click
        navLinks.querySelectorAll('a:not(.nav-dropdown-trigger)').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
                document.body.style.overflow = '';
            });
        });

        // Close when clicking outside
        document.addEventListener('click', (e) => {
            if (!navLinks.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                navLinks.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }

    // 4. Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#' || targetId === '') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                const isMobile = window.innerWidth <= 768;
                const headerOffset = isMobile ? 70 : 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // 5. Active nav link on scroll
    const sections = document.querySelectorAll('section[id]');
    window.addEventListener('scroll', () => {
        const scrollY = window.pageYOffset + 120;
        sections.forEach(current => {
            const sectionHeight = current.offsetHeight;
            const sectionTop = current.offsetTop;
            const sectionId = current.getAttribute('id');
            const navLink = document.querySelector(`.nav-links a[href="#${sectionId}"]:not(.nav-cta)`);
            
            if (navLink) {
                if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                    navLink.classList.add('active');
                } else {
                    navLink.classList.remove('active');
                }
            }
        });
    });

    // 6. Stat Counter Animation
    const counters = document.querySelectorAll('.stat-number');
    let animated = false;

    const animateCounters = () => {
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target') || '0', 10);
            const duration = 1600; // ms
            const step = Math.ceil(target / (duration / 30));
            let current = 0;

            const timer = setInterval(() => {
                current += step;
                if (current >= target) {
                    counter.innerText = target + (counter.getAttribute('data-suffix') || '+');
                    clearInterval(timer);
                } else {
                    counter.innerText = current + (counter.getAttribute('data-suffix') || '+');
                }
            }, 30);
        });
    };

    const statsSection = document.querySelector('.hero-stats-grid');
    if (statsSection) {
        if ('IntersectionObserver' in window) {
            const statsObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !animated) {
                        animated = true;
                        animateCounters();
                    }
                });
            }, { threshold: 0.2 });
            statsObserver.observe(statsSection);
        } else {
            animateCounters();
        }
    }

    // 7. Lightbox Setup for Galleries
    setupLightbox();
});

// 7. Lightbox Setup for Galleries with Multi-Image Slider & Touch Support
function setupLightbox() {
    const galleryCards = document.querySelectorAll('.gallery-card');
    if (!galleryCards.length) return;

    let lightbox = document.querySelector('.lightbox-modal');
    if (!lightbox) {
        lightbox = document.createElement('div');
        lightbox.className = 'lightbox-modal';
        lightbox.innerHTML = `
            <button class="lightbox-close" aria-label="Close Lightbox">&times;</button>
            <button class="lightbox-prev" aria-label="Previous Image">&#10094;</button>
            <div class="lightbox-content-wrap">
                <img src="" alt="Expanded Tooling View" id="lightbox-img">
            </div>
            <button class="lightbox-next" aria-label="Next Image">&#10095;</button>
        `;
        document.body.appendChild(lightbox);
    }

    const lightboxImg = lightbox.querySelector('#lightbox-img');
    const closeBtn = lightbox.querySelector('.lightbox-close');
    const prevBtn = lightbox.querySelector('.lightbox-prev');
    const nextBtn = lightbox.querySelector('.lightbox-next');
    let currentIndex = 0;

    const cardsArray = Array.from(galleryCards);

    function showImage(index) {
        currentIndex = (index + cardsArray.length) % cardsArray.length;
        const targetImg = cardsArray[currentIndex].querySelector('img');
        if (targetImg) {
            lightboxImg.src = targetImg.src;
        }
    }

    cardsArray.forEach((card, idx) => {
        card.addEventListener('click', (e) => {
            e.preventDefault();
            showImage(idx);
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });

    const closeLightbox = () => {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
    };

    closeBtn.addEventListener('click', closeLightbox);
    prevBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        showImage(currentIndex - 1);
    });
    nextBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        showImage(currentIndex + 1);
    });

    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox || e.target.classList.contains('lightbox-content-wrap')) {
            closeLightbox();
        }
    });

    document.addEventListener('keydown', (e) => {
        if (!lightbox.classList.contains('active')) return;
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowLeft') showImage(currentIndex - 1);
        if (e.key === 'ArrowRight') showImage(currentIndex + 1);
    });

    // Touch Swipe Support for Mobile
    let touchStartX = 0;
    let touchEndX = 0;

    lightbox.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    lightbox.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        const diff = touchEndX - touchStartX;
        if (Math.abs(diff) > 45) {
            if (diff > 0) {
                showImage(currentIndex - 1); // Swiped right -> previous
            } else {
                showImage(currentIndex + 1); // Swiped left -> next
            }
        }
    }, { passive: true });
}
