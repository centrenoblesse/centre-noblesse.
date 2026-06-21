import re

def update_index():
    with open('app/templates/public/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the packs-grid section
    match = re.search(r'(<div class="packs-grid">)(.*?)(</section>)', content, re.DOTALL)
    if not match:
        print("Packs grid not found!")
        return

    jinja_loop = """
{% for service in services %}
          <article class="pack-card {% if loop.index == 2 %}pack-card--featured{% elif loop.index == 3 %}pack-card--blue{% endif %} reveal reveal-delay-{{ loop.index }}">
            <div class="pack-glow {% if loop.index == 2 %}pack-glow--red{% elif loop.index == 3 %}pack-glow--blue{% endif %}" aria-hidden="true"></div>
            <div class="pack-top">
              <div class="pack-badge {% if loop.index == 2 %}pack-badge--red{% elif loop.index == 3 %}pack-badge--blue{% endif %}">
                {% if service.category %}{{ service.category.name }}{% else %}Service{% endif %}
              </div>
              <h3 class="pack-name">{{ service.title }}</h3>
              <p class="pack-desc">{{ service.description }}</p>
            </div>
            
            <div class="pack-price-row">
              <div>
                <div class="pack-price">{{ service.price }}</div>
              </div>
              <button class="btn-pack {% if loop.index == 3 %}btn-pack--blue{% endif %}" data-open-modal="register" data-course="{{ service.title }}">
                S'inscrire
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                  <line x1="5" y1="12" x2="19" y2="12"/>
                  <polyline points="12 5 19 12 12 19"/>
                </svg>
              </button>
            </div>
          </article>
{% else %}
          <p style="color: white; text-align: center; width: 100%;">Aucun service disponible pour le moment.</p>
{% endfor %}
        </div>
      </div>
    """

    new_content = content[:match.start(2)] + jinja_loop + content[match.end(3)-10:]
    
    with open('app/templates/public/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Updated index.html services loop.")

if __name__ == '__main__':
    update_index()
