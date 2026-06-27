import re
import os

def fix_corrupted_file(corrupted_path, pristine_path):
    print(f"Fixing {corrupted_path} using {pristine_path}...")
    
    with open(corrupted_path, 'r', encoding='utf-8', errors='replace') as f:
        corrupt_text = f.read()
        
    with open(pristine_path, 'r', encoding='utf-8') as f:
        pristine_text = f.read()

    # Find all occurrences of \ufffd
    pattern = re.compile(r'\ufffd')
    
    fixed_text = ""
    last_idx = 0
    
    success_count = 0
    fail_count = 0

    for match in pattern.finditer(corrupt_text):
        idx = match.start()
        
        # Grab context: 25 chars before and 25 chars after
        start_ctx = max(0, idx - 25)
        end_ctx = min(len(corrupt_text), idx + 26)
        
        prefix = corrupt_text[start_ctx:idx]
        suffix = corrupt_text[idx+1:end_ctx]
        
        # Escape for regex
        # We need to be careful if prefix or suffix contains \ufffd as well.
        # Let's clean up prefix/suffix by replacing \ufffd with wildcard .*?
        prefix_re = re.escape(prefix).replace(r'\ufffd', '.*?')
        suffix_re = re.escape(suffix).replace(r'\ufffd', '.*?')
        
        # Replace variable whitespaces just in case
        prefix_re = re.sub(r'\\s+', r'\\s*', prefix_re)
        suffix_re = re.sub(r'\\s+', r'\\s*', suffix_re)
        
        search_re = re.compile(prefix_re + r'(.{1,3})' + suffix_re, re.DOTALL)
        
        found = search_re.findall(pristine_text)
        
        fixed_text += corrupt_text[last_idx:idx]
        
        if len(found) == 1:
            replacement = found[0]
            fixed_text += replacement
            success_count += 1
        elif len(found) > 1:
            # If multiple matches, just take the first one assuming the context is identical
            replacement = found[0]
            fixed_text += replacement
            success_count += 1
        else:
            # Try a smaller context
            small_prefix = re.escape(prefix[-10:]).replace(r'\ufffd', '.*?')
            small_suffix = re.escape(suffix[:10]).replace(r'\ufffd', '.*?')
            small_re = re.compile(small_prefix + r'(.{1,3})' + small_suffix, re.DOTALL)
            small_found = small_re.findall(pristine_text)
            
            if len(small_found) > 0:
                fixed_text += small_found[0]
                success_count += 1
            else:
                fixed_text += '\ufffd'
                fail_count += 1
                
        last_idx = idx + 1
        
    fixed_text += corrupt_text[last_idx:]
    
    # Save the file
    with open(corrupted_path, 'w', encoding='utf-8') as f:
        f.write(fixed_text)
        
    print(f"  Fixed: {success_count}, Failed: {fail_count}")

# Fix index.html
fix_corrupted_file('app/templates/public/index.html', 'index.html')

# Fix categories.html
fix_corrupted_file('app/templates/public/categories.html', 'categories.html')
