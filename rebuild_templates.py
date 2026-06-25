# -*- coding: utf-8 -*-
"""
rebuild_templates.py
====================
Takes the CLEAN root index.html and categories.html files (which have zero
encoding corruption) and converts them into Flask/Jinja templates by applying
all necessary replacements:
  - Static paths → url_for()
  - Hardcoded links → Flask route links
  - Add CSRF token, cache-busting, admin login form
"""
import re

def convert_index():
    """Convert clean root index.html → app/templates/public/index.html"""
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # ── 1. Static asset paths ──────────────────────────────────────────
    # CSS animations link
    html = html.replace(
        "app/static/css/animations.css",
        "{{ url_for('static', filename='css/animations.css') }}"
    )
    # Add cache-busting to animations CSS
    html = re.sub(
        r"(url_for\('static', filename='css/animations\.css'\)\s*\}\})\"\s*>",
        r"""\1?v={{ config.ASSET_VERSION }}">""",
        html
    )
    # If animations.css is referenced differently
    html = html.replace(
        'href="app/static/css/animations.css"',
        """href="{{ url_for('static', filename='css/animations.css') }}?v={{ config.ASSET_VERSION }}" """
    )

    # Hero background image in inline CSS
    html = html.replace(
        "url('/static/images/hero-bg.jpg')",
        """url("{{ url_for('static', filename='images/hero-bg.jpg') }}")"""
    )
    html = html.replace(
        "url('app/static/images/hero-bg.jpg')",
        """url("{{ url_for('static', filename='images/hero-bg.jpg') }}")"""
    )

    # Logo image
    html = html.replace(
        'src="app/static/images/logo.png"',
        """src="{{ url_for('static', filename='images/logo.png') }}" """
    )

    # Footer logo
    html = html.replace(
        'src="app/static/images/logo.png"',
        """src="{{ url_for('static', filename='images/logo.png') }}" """
    )

    # Animations JS
    html = html.replace(
        'src="app/static/js/animations.js"',
        """src="{{ url_for('static', filename='js/animations.js') }}?v={{ config.ASSET_VERSION }}" """
    )

    # ── 2. Navigation links ───────────────────────────────────────────
    html = html.replace('href="index.html"', """href="{{ url_for('public.index') }}" """)
    html = html.replace('href="categories.html"', """href="{{ url_for('public.categories') }}" """)

    # ── 3. Replace the EmailJS admin form with Flask admin login ───────
    # Find the admin modal form and replace the action with Flask route
    html = html.replace(
        'action="#" method="POST"',
        """action="{{ url_for('admin.login') }}" method="POST" """
    )

    # Add CSRF token after the admin form opening tag
    html = html.replace(
        '<form id="admin-login-form"',
        '<form id="admin-login-form"'
    )
    # Insert csrf_token hidden field after the form tag
    html = re.sub(
        r'(<form id="admin-login-form"[^>]*>)',
        r"""\1\n          <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">""",
        html
    )

    # ── 4. Dynamic Pack cards from CMS ────────────────────────────────
    # Find the hardcoded pack cards section and replace with Jinja loop
    # Look for the pack-grid div with hardcoded cards
    pack_pattern = re.compile(
        r'(<div class="pack-grid"[^>]*>)\s*'
        r'(.*?)'
        r'(</div>\s*</div>\s*</div>\s*</section>)',
        re.DOTALL
    )

    pack_match = pack_pattern.search(html)
    if pack_match:
        jinja_pack_cards = """
{% for srv in services %}
          <article class="pack-card reveal" style="--accent: {{ ['var(--red)', 'var(--blue)', '#D97706', '#16A34A', '#8B5CF6', '#EC4899'][loop.index0 % 6] }}">
            <div class="pack-badge">{{ srv.category.name if srv.category else 'Formation' }}</div>
            <h3 class="pack-title">{{ srv.title }}</h3>
            <p class="pack-desc">{{ srv.description }}</p>
            <div class="pack-price">{{ srv.price }}</div>
            <a href="#register" data-open-modal="register" class="pack-cta">S'inscrire →</a>
          </article>
{% endfor %}
"""
        html = pack_pattern.sub(
            r'\1' + jinja_pack_cards + r'\3',
            html
        )

    # ── 5. Remove EmailJS script (backend handles emails now) ─────────
    # Keep the emailjs init but it's fine to leave it

    # ── 6. Write the final template ───────────────────────────────────
    with open('app/templates/public/index.html', 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print('[OK] Built: app/templates/public/index.html')


def convert_categories():
    """Convert clean root categories.html → app/templates/public/categories.html"""
    with open('categories.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # ── 1. Static asset paths ──────────────────────────────────────────
    html = html.replace(
        'href="app/static/css/animations.css"',
        """href="{{ url_for('static', filename='css/animations.css') }}?v={{ config.ASSET_VERSION }}" """
    )
    html = html.replace(
        'src="app/static/images/logo.png"',
        """src="{{ url_for('static', filename='images/logo.png') }}" """
    )
    html = html.replace(
        'src="app/static/js/animations.js"',
        """src="{{ url_for('static', filename='js/animations.js') }}?v={{ config.ASSET_VERSION }}" """
    )

    # ── 2. Navigation links ───────────────────────────────────────────
    html = html.replace('href="index.html"', """href="{{ url_for('public.index') }}" """)
    html = html.replace('href="categories.html"', """href="{{ url_for('public.categories') }}" """)

    # ── 3. Admin form ─────────────────────────────────────────────────
    html = html.replace(
        'action="#" method="POST"',
        """action="{{ url_for('admin.login') }}" method="POST" """
    )
    html = re.sub(
        r'(<form id="admin-login-form"[^>]*>)',
        r"""\1\n          <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">""",
        html
    )

    # ── 4. Make category tabs dynamic with Jinja ──────────────────────
    # Find the static category buttons block and replace with Jinja loop
    cat_btn_pattern = re.compile(
        r'(<!-- CATEGORY TABS -->.*?<div class="cat-selector[^"]*"[^>]*>)\s*'
        r'(.*?)'
        r'(</div>\s*<!-- PANELS -->)',
        re.DOTALL
    )
    cat_match = cat_btn_pattern.search(html)
    if cat_match:
        jinja_cat_tabs = """
{% for category in categories %}
      <button class="cat-btn {% if loop.first %}active{% endif %}" role="tab" aria-selected="{% if loop.first %}true{% else %}false{% endif %}" aria-controls="cat-{{ category.id }}" id="tab-{{ category.id }}" data-target="cat-{{ category.id }}">
        <div class="cat-btn-icon" aria-hidden="true">{{ ['💻','🎤','📈','🌐','🎯','🛠️'][loop.index0 % 6] }}</div>
        <div class="cat-btn-title">{{ category.name }}</div>
      </button>
{% endfor %}
"""
        html = cat_btn_pattern.sub(
            r'\1' + jinja_cat_tabs + r'\3',
            html
        )

    # Find the static panels block and replace with Jinja loop
    panel_pattern = re.compile(
        r'(<!-- PANELS -->)\s*'
        r'(.*?)'
        r'(<!-- REGISTRATION MODAL)',
        re.DOTALL
    )
    panel_match = panel_pattern.search(html)
    if panel_match:
        jinja_panels = """
{% for category in categories %}
    <div class="cat-panel {% if loop.first %}active{% endif %}" id="cat-{{ category.id }}" role="tabpanel" aria-labelledby="tab-{{ category.id }}">
      <div class="panel-header">
        <div class="panel-icon">{{ ['💻','🎤','📈','🌐','🎯','🛠️'][loop.index0 % 6] }}</div>
        <div>
          <h2 class="panel-title">{{ category.name }}</h2>
          <p class="panel-subtitle">{{ category.description or 'Découvrez nos formations' }}</p>
        </div>
      </div>
      <div class="services-grid">
        {% for srv in services if srv.category_id == category.id %}
        <article class="srv-card">
          <h3 class="srv-title">{{ srv.title }}</h3>
          <p class="srv-desc">{{ srv.description }}</p>
          <div class="srv-footer">
            <span class="srv-price">{{ srv.price }}</span>
            <button class="srv-cta" data-open-modal="register">S'inscrire</button>
          </div>
        </article>
        {% endfor %}
      </div>
    </div>
{% endfor %}

    """
        html = panel_pattern.sub(
            r'\1' + jinja_panels + r'\3',
            html
        )

    with open('app/templates/public/categories.html', 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print('[OK] Built: app/templates/public/categories.html')


if __name__ == '__main__':
    print('=' * 60)
    print('  Centre Noblesse — Template Rebuilder')
    print('=' * 60)
    convert_index()
    convert_categories()
    print('=' * 60)
    print('  Done! Templates rebuilt from clean source files.')
    print('=' * 60)
