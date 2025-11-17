#!/usr/bin/env python3
"""
Converting PDF map to PNG image.
"""
import sys
from pathlib import Path

# Checking if source PDF exists
pdf_path = Path('public/UCLA_MAP.png')
pdf_source = Path('public/UCLA_MAP.pdf')

if not pdf_source.exists():
    print(f"Source PDF not found: {pdf_source}")
    sys.exit(0)

# Attempting conversion using pdf2image
try:
    from pdf2image import convert_from_path
    print("Converting PDF to PNG using pdf2image...")
    images = convert_from_path(str(pdf_source), dpi=200)
    if images:
        images[0].save(str(pdf_path), 'PNG')
        print(f"WROTE: {pdf_path}")
        sys.exit(0)
    else:
        raise Exception("No images extracted from PDF")
except ImportError:
    # Falling back to ImageMagick convert
    print("pdf2image not available, trying ImageMagick convert...")
    try:
        import subprocess
        result = subprocess.run(
            ['convert', f'{pdf_source}[0]', str(pdf_path)],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"WROTE: {pdf_path}")
        sys.exit(0)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print("CONVERSION_FAILED — please provide public/UCLA_MAP.png manually")
        sys.exit(1)
except Exception as e:
    # Retrying with ImageMagick as fallback
    print(f"pdf2image conversion failed: {e}")
    print("Trying ImageMagick convert as fallback...")
    try:
        import subprocess
        result = subprocess.run(
            ['convert', f'{pdf_source}[0]', str(pdf_path)],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"WROTE: {pdf_path}")
        sys.exit(0)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print("CONVERSION_FAILED — please provide public/UCLA_MAP.png manually")
        sys.exit(1)
