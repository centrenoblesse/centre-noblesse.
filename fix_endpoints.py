import glob

for filename in glob.glob('app/templates/public/*.html'):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content.replace('http://localhost:8000/api/register', '/api/register')
    new_content = new_content.replace('http://localhost:8000/api/appointment', '/api/appointment')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Updated API endpoints.")
