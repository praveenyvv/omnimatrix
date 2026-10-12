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

    // 8. Contact & RFQ Form Handler (WhatsApp Integration)
    setupContactForm();

    // 9. Floating WhatsApp Quick-Chat Widget
    setupFloatingWhatsApp();
});

function setupContactForm() {
    const form = document.getElementById('enquiryForm');
    if (!form) return;

    const statusMsg = document.getElementById('formStatusMsg');
    const submitBtn = document.getElementById('submitBtn');

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // 1. Extract values
        const nameInput = form.querySelector('[name="name"]');
        const companyInput = form.querySelector('[name="company"]');
        const emailInput = form.querySelector('[name="email"]');
        const serviceSelect = form.querySelector('[name="service"]');
        const messageInput = form.querySelector('[name="message"]');

        const name = nameInput ? nameInput.value.trim() : '';
        const company = companyInput ? companyInput.value.trim() : '';
        const email = emailInput ? emailInput.value.trim() : '';
        const service = serviceSelect && serviceSelect.selectedIndex >= 0 ? serviceSelect.options[serviceSelect.selectedIndex].text : 'General Technical Consultation';
        const message = messageInput ? messageInput.value.trim() : '';

        // 2. Format WhatsApp RFQ Message
        let waText = `*New Technical RFQ / Enquiry - OmniMatrix Technologies*\n\n`;
        waText += `👤 *Name:* ${name}\n`;
        if (company) waText += `🏢 *Company:* ${company}\n`;
        waText += `✉️ *Email:* ${email}\n`;
        waText += `⚙️ *Requirement:* ${service}\n`;
        if (message) {
            waText += `📝 *Specifications:* ${message}\n`;
        }
        waText += `\n_Submitted via omnimatrixs.com_`;

        const waUrl = `https://wa.me/919177017779?text=${encodeURIComponent(waText)}`;

        // 3. Optional background email backup (silent, non-blocking)
        try {
            const formData = new FormData(form);
            fetch('send_mail.php', { method: 'POST', body: formData }).catch(() => {});
        } catch (_) {}

        // 4. In-page confirmation status
        if (statusMsg) {
            statusMsg.style.display = 'block';
            statusMsg.style.backgroundColor = '#ecfdf5';
            statusMsg.style.color = '#065f46';
            statusMsg.style.border = '1px solid #a7f3d0';
            statusMsg.innerHTML = `✅ <strong>Opening WhatsApp chat with OmniMatrix Engineering specialist (+91 9177017779)...</strong><br>If WhatsApp does not open automatically, <a href="${waUrl}" target="_blank" style="color: #047857; text-decoration: underline; font-weight: 700;">click here to start chat now</a>.`;
        }

        // 5. Open WhatsApp in new tab / app
        window.open(waUrl, '_blank');

        // Reset form
        form.reset();
    });
}

function setupFloatingWhatsApp() {
    if (document.querySelector('.whatsapp-float-btn')) return;

    const waBtn = document.createElement('a');
    waBtn.className = 'whatsapp-float-btn';
    waBtn.href = 'https://wa.me/919177017779?text=Hello%20OmniMatrix%20Technologies%2C%20I%20would%20like%20to%20enquire%20about%20tooling%20and%20manufacturing%20solutions.';
    waBtn.target = '_blank';
    waBtn.rel = 'noopener noreferrer';
    waBtn.setAttribute('aria-label', 'Chat with OmniMatrix on WhatsApp');
    waBtn.innerHTML = `
        <svg viewBox="0 0 24 24">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
        </svg>
        <span class="whatsapp-float-label">Chat on WhatsApp</span>
    `;

    document.body.appendChild(waBtn);
}



// 7. Lightbox Setup for Galleries with Multi-Image Slider & Touch Support
let lightboxInitialized = false;
let activeGalleryCards = [];
let currentIndex = 0;

function setupLightbox() {
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

    // Auto-skip if an image in the lightbox fails to load
    lightboxImg.onerror = function() {
        if (activeGalleryCards.length > 1) {
            // Remove the broken card reference from active array
            activeGalleryCards.splice(currentIndex, 1);
            if (activeGalleryCards.length > 0) {
                currentIndex = currentIndex % activeGalleryCards.length;
                showImage(currentIndex);
            } else {
                closeLightbox();
            }
        } else {
            closeLightbox();
        }
    };

    function showImage(index) {
        if (!activeGalleryCards.length) {
            closeLightbox();
            return;
        }
        currentIndex = (index + activeGalleryCards.length) % activeGalleryCards.length;
        const targetImg = activeGalleryCards[currentIndex].querySelector('img');
        if (targetImg && targetImg.src) {
            lightboxImg.src = targetImg.src;
        }
    }

    const closeLightbox = () => {
        lightbox.classList.remove('active');
        lightboxImg.src = '';
        document.body.style.overflow = '';
    };

    // Attach click listeners to cards (only once per card)
    document.querySelectorAll('.gallery-card').forEach(card => {
        if (card.dataset.lightboxBound) return;
        card.dataset.lightboxBound = 'true';

        card.addEventListener('click', (e) => {
            e.preventDefault();
            // Collect all currently valid cards across the entire page in sequence
            activeGalleryCards = Array.from(document.querySelectorAll('.gallery-card')).filter(c => {
                const img = c.querySelector('img');
                return img && img.naturalWidth !== 0 && c.isConnected;
            });

            if (!activeGalleryCards.length) {
                activeGalleryCards = Array.from(document.querySelectorAll('.gallery-card'));
            }

            const currentIdx = activeGalleryCards.indexOf(card);
            showImage(currentIdx >= 0 ? currentIdx : 0);
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });

    if (!lightboxInitialized) {
        lightboxInitialized = true;

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
}



