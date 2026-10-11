"""Read-only source inventory and trust-token audit of pinned family-113 sources.

This is a lexical/source-inspection receipt, not a Lean kernel certificate.
"""
from pathlib import Path
import datetime, hashlib, json, re, subprocess

ROOT = Path('/Users/alec/Desktop/math')
OUT = Path(__file__).resolve().parent
PIN = 'adc7f1241b42e322a6451854ab7e4b4c146bf78a'
PREFIX = 'OAI.Combinatorics.MatchingCount'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def uncomment(text):
    # Preserve offsets/newlines, including Lean's nested block comments.
    out = list(text)
    i = 0
    depth = 0
    string = False
    while i < len(text):
        if depth:
            if text[i:i+2] == '/-':
                out[i:i+2] = '  '
                depth += 1
                i += 2
            elif text[i:i+2] == '-/':
                out[i:i+2] = '  '
                depth -= 1
                i += 2
            else:
                if text[i] != '\n': out[i] = ' '
                i += 1
        elif string:
            if text[i] == '\\':
                i += 2
            elif text[i] == '"':
                string = False
                i += 1
            else:
                i += 1
        elif text[i:i+2] == '--':
            j = text.find('\n', i)
            if j < 0: j = len(text)
            out[i:j] = ' ' * (j-i)
            i = j
        elif text[i:i+2] == '/-':
            out[i:i+2] = '  '
            depth = 1
            i += 2
        elif text[i] == '"':
            string = True
            i += 1
        else:
            i += 1
    return ''.join(out)

def module_path(module):
    return ROOT / 'lean' / (module.replace('.', '/') + '.lean')

files = sorted((ROOT / 'lean/OAI/Combinatorics/MatchingCount').rglob('*.lean'))
items = {}
hits = []
missing = []
trust = re.compile(r'\b(sorry|admit|axiom|unsafe|native_decide|implemented_by|extern)\b|debug\.skipKernelTC|Elab\.unsafe|ofReduceBool')
for p in files:
    raw = p.read_bytes()
    rel = str(p.relative_to(ROOT))
    clean = uncomment(raw.decode())
    imports = [m for line in re.findall(r'^\s*import\s+([^\n]+)', clean, re.M)
               for m in line.split()]
    blob = subprocess.run(['git', '-C', str(ROOT), 'show', PIN+':'+rel],
                          capture_output=True, check=True).stdout
    module = str(p.relative_to(ROOT / 'lean')).removesuffix('.lean').replace('/', '.')
    items[module] = {'path':rel, 'sha256':sha(raw), 'bytes':len(raw),
                     'lines':raw.count(b'\n'), 'pinned_git_blob_equal':raw == blob,
                     'imports':imports}
    for m in trust.finditer(clean):
        hits.append({'path':rel, 'line':clean.count('\n',0,m.start())+1,
                     'token':m.group(0)})
    for imp in imports:
        if imp.startswith('OAI.') and not module_path(imp).exists():
            missing.append({'importer':rel, 'missing_import':imp})

closure = set()
externals = set()
todo = [PREFIX+'.Main']
while todo:
    m = todo.pop()
    if m in closure: continue
    if m not in items:
        externals.add(m)
        continue
    closure.add(m)
    todo.extend(items[m]['imports'])

primary = []
for subdir in ['A-Fully-Polynomial-Randomized-Approximation-Scheme-for-Perfect-Matchings-in-General-Graphs-September-23-2026',
               'Entropy-and-Face-Dimension-of-the-Perfect-Matching-Polytope-September-23-2026']:
    for p in sorted((ROOT/'preprints'/subdir).rglob('*')):
        if not p.is_file(): continue
        rel = str(p.relative_to(ROOT))
        raw = p.read_bytes()
        blob = subprocess.run(['git','-C',str(ROOT),'show',PIN+':'+rel],capture_output=True,check=True).stdout
        snap = Path('/Users/alec/Documents/Math/openai_followon_weighted_hafnian/sources') / rel
        primary.append({'path':rel,'sha256':sha(raw),'bytes':len(raw),
                        'pinned_git_blob_equal':raw==blob,
                        'snapshot_exists':snap.exists(),
                        'snapshot_equal':snap.exists() and snap.read_bytes()==raw})

data = {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'pinned_commit':PIN,
        'observed_head':subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),
        'scope':'Lexical scan and primary source hashes only; no semantic elaboration or kernel result.',
        'matching_source_files':len(files),'matching_source_lines':sum(x['lines'] for x in items.values()),
        'all_primary_sources_pinned_equal':all(x['pinned_git_blob_equal'] for x in primary),
        'all_matching_sources_pinned_equal':all(x['pinned_git_blob_equal'] for x in items.values()),
        'main_matching_import_closure_count':len(closure),
        'main_external_imports':sorted(externals),
        'missing_OAI_imports':missing,'trust_token_hits':hits,
        'main_import_closure':sorted(closure),'primary_sources':primary,'matching_sources':items}
(OUT/'STATIC_PRIMARY_RECEIPT.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({k:v for k,v in data.items() if k not in ['primary_sources','matching_sources','main_import_closure']},indent=2))
