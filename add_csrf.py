import glob
import re

for filename in glob.glob('app/templates/admin/*.html'):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace <form ...> with <form ...><input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
    # Be careful not to replace it multiple times if it's already there
    if 'name="csrf_token"' not in content:
        content = re.sub(
            r'(<form[^>]*>)',
            r'\1\n        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>',
            content
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added CSRF token to {filename}")

print("CSRF tokens added to admin templates.")
