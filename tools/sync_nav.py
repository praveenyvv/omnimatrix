import glob
import re

html_files = glob.glob('**/*.html', recursive=True)

for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        c = f.read()
    
    is_subpage = 'pages/' in hf.replace('\\', '/') or 'pages\\' in hf
    prefix = '' if is_subpage else 'pages/'
    
    # 1. Update dropdown menu
    new_dropdown = f'''<ul class="dropdown-menu">
                            <li><a href="{prefix}service1.html">Plastic Injection Moulds</a></li>
                            <li><a href="{prefix}service2.html">Press Tools &amp; Stamping</a></li>
                            <li><a href="{prefix}service3.html">Die Casting Dies</a></li>
                            <li><a href="{prefix}service4.html">Scientific Lab Plasticware</a></li>
                            <li><a href="{prefix}service5.html">Aerospace &amp; Drone Components</a></li>
                            <li><a href="{prefix}service6.html">Electronic Enclosures</a></li>
                        </ul>'''
    
    c = re.sub(r'<ul class="dropdown-menu">.*?</ul>', new_dropdown, c, flags=re.DOTALL)
    
    # 2. Update footer capabilities links
    new_footer_caps = f'''<h4>Capabilities &amp; Products</h4>
                    <div class="footer-links">
                        <a href="{prefix}service1.html">Plastic Injection Moulds</a>
                        <a href="{prefix}service2.html">Press Tools &amp; Stamping</a>
                        <a href="{prefix}service3.html">Die Casting Dies</a>
                        <a href="{prefix}service4.html">Scientific Lab Plasticware</a>
                        <a href="{prefix}service5.html">Aerospace &amp; Drone Components</a>
                        <a href="{prefix}service6.html">Electronic Enclosures</a>
                    </div>'''
    
    c = re.sub(r'<h4>(?:Core Capabilities|Capabilities &amp; Products)</h4>\s*<div class="footer-links">.*?</div>', new_footer_caps, c, flags=re.DOTALL)
    
    with open(hf, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'Synchronized {hf}')

print('All 10 HTML files synchronized successfully.')
