import re
import glob

def update_ui():
    logo_html = """<div class="logo-icon" aria-hidden="true" style="background: transparent; border: none; box-shadow: none;">
            <img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo Centre Noblesse" style="height: 48px; width: auto; display: block; object-fit: contain;">
          </div>"""
          
    # 1. Update logo in index.html and categories.html
    for file in ['app/templates/public/index.html', 'app/templates/public/categories.html']:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Regex to find logo-icon
        pattern = r'<div class="logo-icon".*?>\s*<svg.*?</svg>\s*</div>'
        content = re.sub(pattern, logo_html, content, flags=re.DOTALL)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

    # 2. Update categories.html animations
    cat_file = 'app/templates/public/categories.html'
    with open(cat_file, 'r', encoding='utf-8') as f:
        cat_content = f.read()

    old_anim_pattern = r'\.cat-panel\.active\s*\{\s*display:block;\s*animation:fadeScale \.5s var\(--spring\) forwards;\s*\}\s*@keyframes fadeScale\s*\{\s*to\s*\{\s*opacity:1;\s*transform:translateY\(0\) scale\(1\);\s*\}\s*\}'
    
    new_anim_css = """
    .cat-panel {
      display:none; opacity:0;
      transform:translateY(30px) scale(0.95);
      transform-origin:center;
    }
    .cat-panel.active {
      display:block;
      animation:panelEnter .6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    }
    @keyframes panelEnter {
      0% { opacity:0; transform:translateY(40px) scale(0.95) rotateX(8deg); }
      100% { opacity:1; transform:translateY(0) scale(1) rotateX(0deg); }
    }
    
    .cat-panel.active .course-card {
      opacity: 0;
      animation: cardEnter 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    }
    .cat-panel.active .course-card:nth-child(1) { animation-delay: 0.08s; }
    .cat-panel.active .course-card:nth-child(2) { animation-delay: 0.16s; }
    .cat-panel.active .course-card:nth-child(3) { animation-delay: 0.24s; }
    .cat-panel.active .course-card:nth-child(4) { animation-delay: 0.32s; }
    .cat-panel.active .course-card:nth-child(5) { animation-delay: 0.40s; }
    .cat-panel.active .course-card:nth-child(n+6) { animation-delay: 0.48s; }

    @keyframes cardEnter {
      0% { opacity: 0; transform: translateY(30px) scale(0.9); }
      100% { opacity: 1; transform: translateY(0) scale(1); }
    }

    @media (prefers-reduced-motion: reduce) {
      .cat-panel.active, .cat-panel.active .course-card {
        animation: none !important;
        opacity: 1 !important;
        transform: none !important;
      }
      .cat-panel {
        transform: none !important;
        transition: none !important;
      }
    }
    """
    
    # We also need to replace the .cat-panel selector because we added the active logic
    # Find .cat-panel { ... } .cat-panel.active { ... } @keyframes fadeScale { ... }
    full_pattern = r'\.cat-panel\s*\{[^}]*\}\s*\.cat-panel\.active\s*\{[^}]*\}\s*@keyframes fadeScale\s*\{[^}]*\}'
    cat_content = re.sub(full_pattern, new_anim_css.strip(), cat_content, flags=re.DOTALL)
    
    with open(cat_file, 'w', encoding='utf-8') as f:
        f.write(cat_content)

    print("UI updated.")

if __name__ == '__main__':
    update_ui()
