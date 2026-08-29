#!/usr/bin/env python3
"""
Build script to compile YAML content into HTML using Mustache template.
"""

import yaml
import pystache
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

# Static files live in assets/ and are copied to dist/assets/ verbatim.
ASSETS_DIR_NAME = 'assets'
WORK_SAMPLES_DIR_NAME = 'work-samples'


def asset_url(*parts):
    """Build a URL-safe href for a file inside assets/."""
    return '/'.join([ASSETS_DIR_NAME, *(quote(p) for p in parts)])


def missing_asset(assets_dir, *parts):
    """Return a description of the problem if the asset is missing, else None.

    Matches the file name against the real directory listing rather than using
    exists(), so a case mismatch is caught on macOS too — it would still 404 on
    the case-sensitive filesystem GitHub Pages is built on.
    """
    path = assets_dir.joinpath(*parts)
    rel = '/'.join([ASSETS_DIR_NAME, *parts])
    if not path.parent.is_dir():
        return f"{rel} (directory {path.parent.name}/ does not exist)"
    siblings = [p.name for p in path.parent.iterdir()]
    if path.name in siblings:
        return None
    case_match = next((s for s in siblings if s.lower() == path.name.lower()), None)
    if case_match:
        return f"{rel} (name differs by case — the file on disk is '{case_match}')"
    return rel


def resolve_asset_urls(content, assets_dir):
    """Turn asset file names from content.yaml into URLs the template can use.

    Keeps content.yaml free of paths and URL escaping — an editor only needs to
    name the file. Returns a list of problems for assets that would 404.
    """
    problems = []

    profile_image = content.setdefault('hero', {}).get('image', 'shantara.jpg')
    content['hero']['image_url'] = asset_url(profile_image)
    if problem := missing_asset(assets_dir, profile_image):
        problems.append(f"Profile image not found: {problem}")

    resume_file = content.setdefault('cta', {}).get('resume_file')
    if resume_file:
        content['cta']['resume_url'] = asset_url(resume_file)
        if problem := missing_asset(assets_dir, resume_file):
            problems.append(f"Résumé not found: {problem}")

    samples = (content.get('work_samples') or {}).get('items') or []
    for sample in samples:
        sample['url'] = asset_url(WORK_SAMPLES_DIR_NAME, sample['file'])
        if problem := missing_asset(assets_dir, WORK_SAMPLES_DIR_NAME, sample['file']):
            problems.append(f"Work sample not found: {problem}")

    return problems


def build_site(strict=False):
    """Compile the website from YAML content and HTML template.

    With strict=True, a missing asset fails the build instead of warning. Used by
    CI so a broken download link never reaches production.
    """

    # Load content from YAML
    project_root = Path(__file__).parent.parent
    content_file = Path(__file__).parent / 'content.yaml'
    template_file = Path(__file__).parent / 'template.html'
    output_file = project_root / 'dist/index.html'
    assets_dir = project_root / ASSETS_DIR_NAME

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

    problems = resolve_asset_urls(content, assets_dir)
    if not assets_dir.is_dir():
        problems.insert(0, f"No {ASSETS_DIR_NAME}/ directory found — images and PDFs will 404")

    for problem in problems:
        print(f"{'❌' if strict else '⚠️ '} {problem}")
    if problems and strict:
        print(f"❌ Build failed: {len(problems)} missing asset(s)")
        sys.exit(1)

    # Render template with content
    renderer = pystache.Renderer()
    html = renderer.render(template, content)
    
    # Ensure dist directory exists
    output_file.parent.mkdir(exist_ok=True)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Copy assets (profile image, résumé, work samples) to dist/assets/
    if assets_dir.is_dir():
        dest_assets = output_file.parent / ASSETS_DIR_NAME
        shutil.rmtree(dest_assets, ignore_errors=True)
        shutil.copytree(assets_dir, dest_assets)
        file_count = sum(1 for p in dest_assets.rglob('*') if p.is_file())
        print(f"📦 Copied {file_count} file(s) from {ASSETS_DIR_NAME}/ to dist/{ASSETS_DIR_NAME}/")

    print(f"✅ Successfully built site to {output_file}")
    return True


if __name__ == '__main__':
    build_site(strict='--strict' in sys.argv)
