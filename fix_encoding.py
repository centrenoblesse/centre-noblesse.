# -*- coding: utf-8 -*-
"""
fix_encoding.py  —  Mojibake Reverser for Centre Noblesse
----------------------------------------------------------
Problem: HTML/Python files were saved with characters double-encoded.
         The original encoding was UTF-8, but VSCode/editor read them
         as Windows-1252 and re-saved as UTF-8, corrupting French accents
         and special characters (e.g.  â€" instead of —, rÃ© instead of ré).

Fix:     Read each file as UTF-8 bytes -> decode -> re-encode as windows-1252
         (reversing the mistake) -> decode final bytes as UTF-8 -> save clean UTF-8.
"""

import os

FILES_TO_FIX = [
    r"app\templates\public\index.html",
    r"app\templates\public\categories.html",
    r"app\templates\admin\base.html",
    r"app\templates\admin\login.html",
    r"app\templates\admin\dashboard.html",
    r"app\templates\admin\services.html",
    r"app\templates\admin\categories.html",
    r"app\templates\admin\settings.html",
    r"app\__init__.py",
    r"app\routes\public.py",
    r"app\routes\admin.py",
    r"app\routes\api.py",
    r"app\models.py",
    r"seed_db.py",
    r"run.py",
]


def fix_mojibake(text):
    """
    Reverse the double-encoding.
    Strategy: encode the corrupted utf-8 string back as windows-1252
    (which undoes the double-encode), then decode the resulting bytes as utf-8.
    Uses 'replace' error handler to skip any bytes that don't fit.
    """
    try:
        raw_bytes = text.encode('windows-1252', errors='replace')
        return raw_bytes.decode('utf-8', errors='replace')
    except Exception:
        return text


def fix_file(filepath):
    if not os.path.exists(filepath):
        print(f"  SKIP (not found):    {filepath}")
        return

    with open(filepath, 'rb') as f:
        raw = f.read()

    # Decode file content as UTF-8
    try:
        original_text = raw.decode('utf-8')
    except UnicodeDecodeError:
        print(f"  SKIP (not UTF-8):    {filepath}")
        return

    # Apply the Mojibake fix
    fixed_text = fix_mojibake(original_text)

    if fixed_text == original_text:
        print(f"  OK   (already clean): {filepath}")
        return

    # Save the fixed content back as clean UTF-8 with Unix line endings
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(fixed_text)
    print(f"  FIXED:               {filepath}")


if __name__ == '__main__':
    print("=" * 65)
    print("  Centre Noblesse - Encoding Fixer (Mojibake Reverser)")
    print("=" * 65)
    base = os.path.dirname(os.path.abspath(__file__))
    for rel_path in FILES_TO_FIX:
        full_path = os.path.join(base, rel_path)
        fix_file(full_path)
    print("=" * 65)
    print("  Done! Now upload all files to PythonAnywhere.")
    print("=" * 65)
