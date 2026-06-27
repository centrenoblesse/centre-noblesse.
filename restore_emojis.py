import os

def restore_emojis(dest_path):
    with open(dest_path, 'r', encoding='utf-8') as f:
        dest = f.read()
    
    # Replace the replacement characters with the actual emojis
    replacements = {
        ' Cours Informatique': '💻 Cours Informatique',
        ' Formation de Formateurs': '🎤 Formation de Formateurs',
        ' Langues': '🌐 Langues',
        ' IA &amp; Cybersécurité': '🤖 IA &amp; Cybersécurité',
        ' IA & Cybersécurité': '🤖 IA & Cybersécurité',
        ' Kids Program': '🎯 Kids Program',
        '️ Formation Divers': '🛠️ Formation Divers',
        ' Formation Divers': '🛠️ Formation Divers',
        '<div class="stat-icon" aria-hidden="true"></div>': '<div class="stat-icon" aria-hidden="true">📜</div>',
        '<div class="stat-icon" aria-hidden="true">️</div>': '<div class="stat-icon" aria-hidden="true">👥</div>',
        '<div class="cat-btn-icon" aria-hidden="true"></div>': '<div class="cat-btn-icon" aria-hidden="true">✨</div>',
        '<div class="panel-icon"></div>': '<div class="panel-icon">✨</div>',
        'Catgories': 'Catégories',
        'Dconnexion': 'Déconnexion',
        'Paramtres': 'Paramètres'
    }
    
    for k, v in replacements.items():
        dest = dest.replace(k, v)
        
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(dest)
    print(f'Fixed emojis and chars in {dest_path}')

restore_emojis(r'app/templates/public/index.html')
restore_emojis(r'app/templates/public/categories.html')
restore_emojis(r'app/templates/admin/base.html')
