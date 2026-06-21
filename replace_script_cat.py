import re

def update_categories_tabs():
    with open('app/templates/public/categories.html', 'r', encoding='utf-8') as f:
        content = f.read()

    start_marker = "<!-- CATEGORY TABS -->"
    end_marker = "</section>"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)
    
    if start_idx == -1 or end_idx == -1:
        print("Markers not found!")
        return

    jinja_html = """<!-- CATEGORY TABS -->
    <div class="cat-selector reveal reveal-delay-1" role="tablist" aria-label="Catégories de formations">
{% for category in categories %}
      <button class="cat-btn {% if loop.first %}active{% endif %}" role="tab" aria-selected="{% if loop.first %}true{% else %}false{% endif %}" aria-controls="cat-{{ category.id }}" id="tab-{{ category.id }}" data-target="cat-{{ category.id }}">
        <div class="cat-btn-icon" aria-hidden="true">💻</div>
        <div class="cat-btn-title">{{ category.name }}</div>
      </button>
{% endfor %}
    </div>

    <!-- PANELS -->
{% for category in categories %}
    <div class="cat-panel {% if loop.first %}active{% endif %}" id="cat-{{ category.id }}" role="tabpanel" aria-labelledby="tab-{{ category.id }}">
      <div class="panel-header">
        <div class="panel-icon">💻</div>
        <h2 class="panel-title">{{ category.name }}</h2>
      </div>
      <div class="courses-grid">
        {% for service in services %}
          {% if service.category_id == category.id %}
          <article class="course-card">
            <div class="cc-badge cc-badge--blue">{{ category.name }}</div>
            <h3 class="cc-title">{{ service.title }}</h3>
            <div class="cc-meta">
              <div class="meta-item"><span>Description</span> <span class="val" style="font-size:0.75rem">{{ service.description[:50] }}...</span></div>
              <div class="meta-item price"><span>Tarif</span> <span class="val">{{ service.price }}</span></div>
            </div>
            <div class="cc-footer">
              <button class="btn-course" data-open-modal="register" data-course="{{ service.title }}">S'inscrire</button>
            </div>
          </article>
          {% endif %}
        {% endfor %}
      </div>
    </div>
{% else %}
    <p style="text-align: center; width: 100%;">Aucune catégorie disponible pour le moment.</p>
{% endfor %}
    """
    
    content = content[:start_idx] + jinja_html + content[end_idx:]

    with open('app/templates/public/categories.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated categories.html tabs and panels.")

if __name__ == '__main__':
    update_categories_tabs()
