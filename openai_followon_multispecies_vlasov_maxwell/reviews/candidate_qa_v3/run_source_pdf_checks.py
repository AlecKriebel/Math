#!/usr/bin/env python3
"""Reproduce mechanical source/PDF/certificate QA without changing the candidate.

Requires the existing bundled Python PDF libraries and Poppler/Tectonic paths.
Writes only in this v3 QA directory. Visual inspection is a separate recorded step.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import platform
import re
import shutil
import ssl
import subprocess
import sys
import tempfile
from pypdf import PdfReader
import pdfplumber
from PIL import Image, ImageChops

QA = Path(__file__).resolve().parent
PKG = QA.parent / 'package_v3'
SRC = PKG / 'source-and-verification'
PDF = PKG / 'upload-kit/paper.pdf'
TECTONIC = '/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic'
POPPLER = Path('/opt/homebrew/bin')

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def save(name, obj):
    (QA / name).write_text(json.dumps(obj, indent=2) + '\n')

def execute(command, logname, **kwargs):
    result = subprocess.run(command, capture_output=True, text=True, **kwargs)
    (QA / logname).write_text(result.stdout + result.stderr)
    result.check_returncode()
    return result

assert sha(PDF) == '20581b8b253c470d9fd775f88931002fc99729b7d7db21da5e6274482c5b990a'
assert sha(PKG/'upload-kit/source-and-verification.zip') == 'b14fa882d987ef6b168b9b821c86b1685f4e6abcd7540837e9f3afa9c0cff527'
execute([str(POPPLER/'pdfinfo'), str(PDF)], 'pdfinfo.txt')
execute([str(POPPLER/'pdffonts'), str(PDF)], 'pdffonts.txt')
execute([str(POPPLER/'pdftotext'), '-layout', str(PDF), '-'], 'paper_layout.txt')
work = QA / 'tmp/pdfs'
work.mkdir(parents=True, exist_ok=True)
subprocess.run([str(POPPLER/'pdftoppm'), '-r', '110', '-png', str(PDF), str(work/'candidate-page')], check=True)
build = Path(tempfile.mkdtemp(prefix='clean-source-build-', dir=work))
for name in ('main.tex', 'references.bib'):
    shutil.copyfile(SRC/name, build/name)
trust = ssl.get_default_verify_paths()
env = os.environ.copy()
if trust.cafile:
    env['SSL_CERT_FILE'] = trust.cafile
if trust.capath:
    env['SSL_CERT_DIR'] = trust.capath
command = [TECTONIC, '-X', 'compile', '--untrusted', '--only-cached', '--keep-logs', '--keep-intermediates', 'main.tex']
started = now()
execute(command, 'clean_build_console.log', cwd=build, env=env)
shutil.copyfile(build/'main.log', QA/'clean_build_main.log')
save('clean_build_receipt.json', {'timestamp_utc':started, 'completed_utc':now(), 'command':command, 'working_directory':str(build), 'runtime':'Tectonic 0.17.0 (existing bundled executable)', 'certificate_policy':'Python ssl.get_default_verify_paths(); no third-party cert bundle', 'standard_library_ssl_verify_paths':trust._asdict(), 'only_cached':True, 'returncode':0, 'input_main_tex_sha256':sha(build/'main.tex'), 'pdf_sha256':sha(build/'main.pdf')})
execute([str(POPPLER/'pdftotext'), '-layout', str(build/'main.pdf'), '-'], 'clean_build_layout.txt')
subprocess.run([str(POPPLER/'pdftoppm'), '-r', '110', '-png', str(build/'main.pdf'), str(build/'rebuilt-page')], check=True)
reader, rebuilt = PdfReader(PDF), PdfReader(build/'main.pdf')
assert len(reader.pages) == len(rebuilt.pages) == 11
pages, links = [], []
for number, (page, other) in enumerate(zip(reader.pages, rebuilt.pages), 1):
    original_png = work/f'candidate-page-{number:02}.png'
    rebuilt_png = build/f'rebuilt-page-{number:02}.png'
    left, right = Image.open(original_png), Image.open(rebuilt_png)
    difference = ImageChops.difference(left.convert('RGB'), right.convert('RGB'))
    annotations = page.get('/Annots', [])
    if hasattr(annotations, 'get_object'):
        annotations = annotations.get_object()
    for reference in annotations:
        annotation = reference.get_object()
        action = annotation.get('/A', {})
        if hasattr(action, 'get_object'):
            action = action.get_object()
        links.append({'page':number, 'subtype':str(annotation.get('/Subtype')), 'uri':str(action.get('/URI', '')), 'destination':str(annotation.get('/Dest', '')), 'rectangle':list(annotation.get('/Rect', []))})
    pages.append({'page':number, 'candidate_png_sha256':sha(original_png), 'rebuilt_png_sha256':sha(rebuilt_png), 'same_pixel_dimensions':left.size==right.size, 'pixel_identical':difference.getbbox() is None, 'extracted_text_identical':page.extract_text()==other.extract_text(), 'candidate_links':len(annotations), 'content_sha256':hashlib.sha256(page.get_contents().get_data()).hexdigest(), 'rebuilt_content_sha256':hashlib.sha256(other.get_contents().get_data()).hexdigest()})
save('pdf_reproduction_comparison.json', {'timestamp_utc':now(), 'candidate_pages':len(reader.pages), 'rebuilt_pages':len(rebuilt.pages), 'layout_text_identical':(QA/'paper_layout.txt').read_text()==(QA/'clean_build_layout.txt').read_text(), 'candidate_metadata':dict(reader.metadata), 'rebuilt_metadata':dict(rebuilt.metadata), 'pages':pages, 'links':links})
assert all(p['pixel_identical'] and p['extracted_text_identical'] and p['content_sha256']==p['rebuilt_content_sha256'] for p in pages)
raw = (SRC/'main.tex').read_text()
cited = [key for match in re.finditer(r'\\cite(?:\[[^\]]*\])*\{([^}]+)\}', raw) for key in match.group(1).split(',')]
bibkeys = re.findall(r'\\bibitem\{([^}]+)\}', raw)
labels = re.findall(r'\\label\{([^}]+)\}', raw)
refs = re.findall(r'\\(?:eqref|ref)\{([^}]+)\}', raw)
log = (QA/'clean_build_main.log').read_text()
warnings = ['Overfull \\hbox', 'Overfull \\vbox', 'Underfull \\hbox', 'Underfull \\vbox', 'LaTeX Warning:', 'Package hyperref Warning:', 'Undefined control sequence', 'Emergency stop', 'Fatal error']
geometry = []
with pdfplumber.open(PDF) as document:
    for number, page in enumerate(document.pages, 1):
        chars = page.chars
        geometry.append({'page':number, 'characters':len(chars), 'min_x0':min(c['x0'] for c in chars), 'max_x1':max(c['x1'] for c in chars), 'min_top':min(c['top'] for c in chars), 'max_bottom':max(c['bottom'] for c in chars), 'characters_outside_page':sum(c['x0']<0 or c['x1']>page.width or c['top']<0 or c['bottom']>page.height for c in chars), 'replacement_characters':sum(c['text']=='\ufffd' for c in chars)})
save('source_pdf_integrity.json', {'timestamp_utc':now(), 'cite_keys':sorted(set(cited)), 'bibitem_keys':bibkeys, 'missing_citations':sorted(set(cited)-set(bibkeys)), 'unused_bibitems':sorted(set(bibkeys)-set(cited)), 'label_count':len(labels), 'duplicate_labels':sorted(k for k in set(labels) if labels.count(k)>1), 'missing_source_reference_labels':sorted(set(refs)-set(labels)), 'tex_log_findings':{pattern:log.count(pattern) for pattern in warnings}, 'pdf_named_destination_count':len(reader.named_destinations), 'invalid_annotation_destinations':[link for link in links if link['destination'] and link['destination'] not in reader.named_destinations], 'pdf_uri_links':[link for link in links if link['uri']], 'page_geometry_checks':geometry, 'checks_scope':'Source/PDF correspondence and formatting only; no independent mathematical or external bibliographic validation.'})
certificate_dir = Path(tempfile.mkdtemp(prefix='certificates-', dir=work))
results = []
for name in ('exact_kernel_certificate.py', 'rational_selection_certificate.py', 'verify_pair_identity.py'):
    shutil.copyfile(SRC/name, certificate_dir/name)
    execute([sys.executable, '-I', str(certificate_dir/name)], name+'.log', cwd=certificate_dir)
    results.append({'script':name, 'script_sha256':sha(certificate_dir/name), 'exit_code':0, 'output_log':str(QA/(name+'.log'))})
save('certificate_receipt.json', {'timestamp_utc':now(), 'python_version':platform.python_version(), 'working_directory':str(certificate_dir), 'isolated_python':True, 'scope':'Algebra only. Certificate passes do not establish PDE existence, analytic transfer, priority, or formal theorem certification.', 'checks':results})
print(json.dumps({'status':'PASS', 'pages':11, 'all_pixels_text_and_content_streams_identical':True, 'certificate_checks':len(results), 'candidate_sha256':sha(PDF), 'rebuilt_sha256':sha(build/'main.pdf')}, indent=2))
