#!/usr/bin/env python3
"""
Build script to compile YAML content into HTML using Mustache template.
"""

import yaml
import pystache
import sys
from pathlib import Path


def build_site():
    """Compile the website from YAML content and HTML template."""
    
    # Load content from YAML
    content_file = Path('content.yaml')
    template_file = Path('template.html')
    output_file = Path('dist/index.html')
    
    if not content_file.exists():
        print(f"❌ Error: {content_file} not found")
        sys.exit(1)
    
    if not template_file.exists():
        print(f"❌ Error: {template_file} not found")
        sys.exit(1)
    
    # Load YAML content
    with open(content_file, 'r', encoding='utf-8') as f:
        content = yaml.safe_load(f)
    
    # Load HTML template
    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Render template with content
    renderer = pystache.Renderer()
    html = renderer.render(template, content)
    
    # Ensure dist directory exists
    output_file.parent.mkdir(exist_ok=True)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Copy resume PDF to dist if it exists
    resume_file = Path('Shantara_Pintak_Resume.pdf')
    if resume_file.exists():
        import shutil
        dest = output_file.parent / resume_file.name
        shutil.copy(resume_file, dest)
        print(f"📄 Copied {resume_file} to dist/")
    
    print(f"✅ Successfully built site to {output_file}")
    return True


if __name__ == '__main__':
    build_site()
