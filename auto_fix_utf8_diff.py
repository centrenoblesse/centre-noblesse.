import difflib

def fix_with_difflib(corrupted_path, pristine_path):
    print(f"Fixing {corrupted_path} using {pristine_path} with difflib...")
    
    with open(corrupted_path, 'r', encoding='utf-8') as f:
        corrupt_text = f.read()
        
    with open(pristine_path, 'r', encoding='utf-8') as f:
        pristine_text = f.read()

    # We want to match the files word by word or character by character.
    # difflib on full text char by char is slow, let's do it line by line?
    # No, the line numbers don't match exactly, and some lines are completely different.
    # But difflib can handle different line counts.
    
    corrupt_lines = corrupt_text.splitlines(keepends=True)
    pristine_lines = pristine_text.splitlines(keepends=True)
    
    sm = difflib.SequenceMatcher(None, pristine_lines, corrupt_lines)
    
    fixed_lines = []
    
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            fixed_lines.extend(corrupt_lines[j1:j2])
        elif tag == 'replace':
            # pristine_lines[i1:i2] was replaced by corrupt_lines[j1:j2]
            # Let's check if the corrupt_lines have \ufffd
            c_block = "".join(corrupt_lines[j1:j2])
            p_block = "".join(pristine_lines[i1:i2])
            
            if '\ufffd' in c_block:
                # We need to selectively replace \ufffd in c_block using p_block
                # Since the lines are mostly the same except for \ufffd vs real chars,
                # let's do a character-by-character diff of just this block!
                char_sm = difflib.SequenceMatcher(None, p_block, c_block)
                fixed_c_block = ""
                for c_tag, ci1, ci2, cj1, cj2 in char_sm.get_opcodes():
                    if c_tag == 'equal':
                        fixed_c_block += c_block[cj1:cj2]
                    elif c_tag == 'replace':
                        # c_block[cj1:cj2] replaced p_block[ci1:ci2]
                        # If c_block has \ufffd, use p_block!
                        sub_c = c_block[cj1:cj2]
                        sub_p = p_block[ci1:ci2]
                        if '\ufffd' in sub_c:
                            # Use pristine characters, but keep any Jinja tags if they exist?
                            # Usually Jinja tags don't contain \ufffd
                            fixed_c_block += sub_p
                        else:
                            fixed_c_block += sub_c
                    elif c_tag == 'insert':
                        fixed_c_block += c_block[cj1:cj2]
                    elif c_tag == 'delete':
                        pass
                fixed_lines.append(fixed_c_block)
            else:
                fixed_lines.extend(corrupt_lines[j1:j2])
        elif tag == 'insert':
            fixed_lines.extend(corrupt_lines[j1:j2])
        elif tag == 'delete':
            pass
            
    fixed_text = "".join(fixed_lines)
    
    with open(corrupted_path, 'w', encoding='utf-8') as f:
        f.write(fixed_text)
        
    print(f"  Done. Remaining \\ufffd: {fixed_text.count(chr(0xfffd))}")

fix_with_difflib('app/templates/public/index.html', 'index.html')
fix_with_difflib('app/templates/public/categories.html', 'categories.html')
