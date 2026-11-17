"""Single informed continuation audit: stdlib data reading; writes only own lane."""
from pathlib import Path
from datetime import datetime, timezone
from html import escape, unescape
from html.parser import HTMLParser
from xml.parsers import expat
import xml.etree.ElementTree as ET
import hashlib
import json
import re
import stat
import sys

BASE = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
LANE = BASE / 'verification/wreath-dyadic-stress-stage-audit-sol-20261116'
OUT = LANE / 'continuation-20261117'
STAGE = BASE / 'verification/wreath-dyadic-stress-stage-sol-20261116'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
M = Path('/Users/alec/Documents/Math')
AUTH = BASE / 'verification/root-wreath-dyadic-stress-editorial-adoption-20261116.json'
EXPECTED_M = 'ae8f9b87f02ac7799421280c9d4c354513f6242f'
PINS = {
    LANE / 'INITIAL_SEAL.json': 'e8097351d7f5444520b9b7181d34f7848b589288013296ec5393df9a0d94239a',
    AUTH: '4eb948c3cec10111bceac2170efe5922085f1f498fa37d8f8eaf805c6863ddf1',
    STAGE / 'FINAL.json': 'dad3a18d0493b8f5831e0e137e680a28690bacea0df7c3b97e8c1011b110e26d',
    STAGE / 'OWNED_MANIFEST.json': 'd245625d4f6b7131b3529110c45a6b9cd6691a56c946e784a0e9dd17d4875ca9',
    STAGE / 'PUBLIC_PAYLOADS.json': 'e09f4d6eb06ee9ba1135d77a8ce50e6591c0abfedc19a5c7e82bae9e40410dd6',
    STAGE / 'PREP_INPUT_SEAL.json': '39ded8fe882a58f85c5e61d39dfd2f6eb5aeac9ec4ac52b038d9259a42c5a4a1',
    STAGE / 'PREP_MANIFEST.json': '2044ccac276bd7b7b1edac9bb0752ae3583091847ad02c926f4de09cfe282503',
    STAGE / 'build_private_stage_v2.py': 'edbf6c1692633077f084a186426720289bebf7abbe846fd0ea7057154dfc0377',
}

def now():
    return datetime.now(timezone.utc).isoformat()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def json_text(text):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(text, object_pairs_hook=unique)

def load(path):
    return json_text(path.read_bytes().decode('utf-8'))

def mode(value):
    return value if type(value) is int else int(value, 8)

def pin(path):
    st = path.lstat()
    if not stat.S_ISREG(st.st_mode):
        raise ValueError('nonregular file: ' + str(path))
    data = path.read_bytes()
    return dict(bytes=len(data), SHA256=digest(data), mode=format(stat.S_IMODE(st.st_mode), '04o'))

def snapshot(root):
    st = root.lstat()
    if not stat.S_ISDIR(st.st_mode):
        raise ValueError('non-directory root: ' + str(root))
    files, directories = [], []
    for path in sorted(root.rglob('*')):
        st = path.lstat()
        rel = path.relative_to(root).as_posix()
        if stat.S_ISDIR(st.st_mode):
            directories.append(dict(path=rel, mode=format(stat.S_IMODE(st.st_mode), '04o')))
        elif stat.S_ISREG(st.st_mode):
            files.append(dict(path=rel, **pin(path)))
        else:
            raise ValueError('symlink/special object: ' + str(path))
    return dict(root=str(root), root_mode=format(stat.S_IMODE(root.stat().st_mode), '04o'),
                files=files, directories=directories, regular_files=len(files), child_directories=len(directories))

def write(name, value):
    with (OUT / name).open('x') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')

if (LANE / 'FINAL.json').exists() or (OUT / 'AUDIT_RESULT.json').exists():
    raise SystemExit('Existing terminal evidence: no replay permitted')
write('RUN_STARTED.json', dict(UTC=now(), own_data_audit_invocation=1, producer_or_native_execution=0))
CHECKS, EVIDENCE = [], {}

def check(name, passed, details=None):
    CHECKS.append(dict(check=name, PASS=bool(passed), details=details))

def task(name, function):
    try:
        function()
    except Exception as error:
        check(name + ': completed without parser/internal exception', False,
              dict(exception=type(error).__name__, message=str(error)))

def same_typed(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return set(a) == set(b) and all(same_typed(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same_typed(x, y) for x, y in zip(a, b))
    return a == b

def manifest_check(root, obj, snap, key, controls):
    actual = {r['path']: r for r in snap['files']}
    rows = obj[key]
    names = [r['path'] for r in rows]
    check(str(root) + ': manifest exact finite file set', len(names) == len(set(names)) and set(names) | controls == set(actual))
    bad = []
    for row in rows:
        rel = row['path']
        if rel not in actual or Path(rel).is_absolute() or '..' in Path(rel).parts:
            bad.append(rel + ': invalid/missing'); continue
        observed = actual[rel]
        if mode(row['mode']) != int(observed['mode'], 8):
            bad.append(rel + ': mode')
        if row.get('terminal_control'):
            if rel not in controls or 'SHA256' in row or 'bytes' in row:
                bad.append(rel + ': invalid terminal exclusion')
        elif (row['bytes'], row['SHA256']) != (observed['bytes'], observed['SHA256']):
            bad.append(rel + ': bytes/hash')
    check(str(root) + ': all manifest file bytes and modes', not bad, bad)
    expected_dirs = {r['path']: mode(r['mode']) for r in obj['directories'] if r['path'] != '.'}
    actual_dirs = {r['path']: int(r['mode'], 8) for r in snap['directories']}
    check(str(root) + ': exact directory set and modes', expected_dirs == actual_dirs)
    root_modes = [mode(obj['root_mode'])] if 'root_mode' in obj else [mode(r['mode']) for r in obj['directories'] if r['path'] == '.']
    check(str(root) + ': explicit root mode', root_modes == [int(snap['root_mode'], 8)])

def native(root):
    git = root / '.git'
    names = ['HEAD', 'index', 'config']
    if (git / 'packed-refs').exists():
        names.append('packed-refs')
    values = {name: pin(git / name) for name in names}
    head = (git / 'HEAD').read_text().strip()
    if not head.startswith('ref: refs/heads/'):
        raise ValueError('nonlocal-branch HEAD')
    ref = head[5:]
    loose = git / ref
    packed = {}
    if (git / 'packed-refs').exists():
        for line in (git / 'packed-refs').read_text().splitlines():
            parts = line.split()
            if len(parts) == 2 and parts[1].startswith('refs/heads/'):
                packed[parts[1]] = parts[0]
    oid = loose.read_text().strip() if loose.is_file() else packed[ref]
    branches = snapshot(git / 'refs/heads') if (git / 'refs/heads').is_dir() else None
    return dict(root=str(root), files=values, HEAD=head, branch=ref, OID=oid,
                local_heads=branches, packed_local_heads=packed,
                shared_indices={p.name: pin(p) for p in sorted(git.glob('sharedindex.*'))})

INITIAL_FILES = sorted(p.name for p in LANE.iterdir() if p.is_file())
INITIAL_BEFORE = {n: pin(LANE / n) for n in INITIAL_FILES}
NATIVE_BEFORE = [native(M), native(W)]

def initial_and_stage():
    for path, expected in PINS.items():
        check('external terminal/control pin: ' + str(path), pin(path)['SHA256'] == expected)
    seal = load(LANE / 'INITIAL_SEAL.json')
    check('INITIAL has exactly17 original flat files, all0644', len(INITIAL_FILES) == 17 and all(x['mode'] == '0644' for x in INITIAL_BEFORE.values()))
    check('INITIALrootmode0755preserved', stat.S_IMODE(LANE.lstat().st_mode) == 0o755)
    check('INITIAL manifest pin', pin(LANE / 'INITIAL_MANIFEST.sha256')['SHA256'] == seal['manifest']['SHA256'])
    for line in (LANE / 'INITIAL_MANIFEST.sha256').read_text().splitlines():
        sha, rel = line.split('  ', 1)
        check('INITIAL preserved payload: ' + rel, pin(LANE / rel)['SHA256'] == sha)
    snap = snapshot(STAGE); EVIDENCE['producer815'] = snap
    check('whole producer815files375dirs', (snap['regular_files'], snap['child_directories']) == (815, 375))
    manifest_check(STAGE, load(STAGE / 'OWNED_MANIFEST.json'), snap, 'files', {'OWNED_MANIFEST.json', 'FINAL.json'})
    obj = load(STAGE / 'OWNED_MANIFEST.json')
    expected = {str(STAGE / 'OWNED_MANIFEST.json'), str(STAGE / 'FINAL.json')}
    check('producer only two exact terminal hash exclusions', set(obj['exact_already_created_terminal_control_recursive_hash_exclusions']) == expected)
    check('producer17DSStorefiles', sum(Path(r['path']).name == '.DS_Store' for r in snap['files']) == 17)
    before, after = load(STAGE / 'BUILD_GUARDS_BEFORE.json'), load(STAGE / 'BUILD_GUARDS_AFTER.json')
    EVIDENCE['producer_build_guard_before'] = before
    check('producer whole before/after guards exact', same_typed(before, after))
    prep = load(STAGE / 'PREP_MANIFEST.json')
    prep_rows = before['preparation15']
    check('15originalPREPfiniteextent', len(prep['files']) == len(prep_rows) == 15 and {r['path'] for r in prep['files']} == {r['path'] for r in prep_rows})
    bad = []
    for row in prep_rows:
        if pin(STAGE / row['path']) != {k: row[k] for k in ('bytes', 'SHA256', 'mode')}:
            bad.append(row['path'])
    for row in prep['files']:
        if not row.get('terminal_control') and pin(STAGE / row['path']) != {k: row[k] for k in ('bytes', 'SHA256', 'mode')}:
            bad.append(row['path'])
    check('all15originalPREPbytesmodesunchanged', not bad, bad)

def adopted_and_sources():
    authority = load(AUTH)
    keys = [('MANIFEST.json', 'payload_files'), ('OWNED_MANIFEST.json', 'files'),
            ('OWNED_MANIFEST.json', 'files'), ('MANIFEST.json', 'files'),
            ('MANIFEST.json', 'payload_files'), ('OWNED_MANIFEST.json', 'files'), ('OWNED_MANIFEST.json', 'files')]
    guards = load(STAGE / 'BUILD_GUARDS_BEFORE.json')
    snaps = []
    for declared, (filename, key), prior in zip(authority['checks'], keys, guards['adopted_inputs']):
        root = Path(declared['root']); snap = snapshot(root); snaps.append(snap)
        check('adopted complete guard: ' + root.name, same_typed(snap, prior))
        check('adopted root control pins: ' + root.name,
              pin(root / filename)['SHA256'] == declared['manifest_SHA256'] and pin(root / 'FINAL.json')['SHA256'] == declared['FINAL_SHA256'])
        check('adopted exact declared extent: ' + root.name,
              (snap['regular_files'], snap['child_directories']) == (declared['files'], declared['child_directories']))
        manifest_check(root, load(root / filename), snap, key, {filename, 'FINAL.json'})
    check('all7adopted155files8dirs', len(snaps) == 7 and sum(s['regular_files'] for s in snaps) == 155 and sum(s['child_directories'] for s in snaps) == 8)
    EVIDENCE['adopted155'] = snaps
    sources = [snapshot(BASE / 'papers' / str(record) / 'sources') for record in (23203143, 23205181, 23331540)]
    check('all323sourcefiles44dirs', sum(s['regular_files'] for s in sources) == 323 and sum(s['child_directories'] for s in sources) == 44)
    check('all323sourcebuffersmodesandtopologyequalproduceroriginalguards', same_typed(sources, guards['original_sources']))
    EVIDENCE['source323'] = sources
    lines = (LANE / 'INPUT_TREES.sha256').read_text().splitlines()
    bad = []
    for line in lines:
        sha, name = line.split('  ', 1)
        if pin(Path(name))['SHA256'] != sha:
            bad.append(name)
    check('INITIAL391sourcewriterbuffersexact', len(lines) == 391 and not bad, bad)
    lines = (LANE / 'INPUT_TOPOLOGY_MODES.txt').read_text().splitlines()
    bad = []
    for line in lines:
        bits, name = line.split(' ', 1)
        if Path(name).lstat().st_mode != int(bits, 8):
            bad.append(name)
    check('INITIAL448sourcewriterfileroottopologymodenodesexact', len(lines) == 448 and not bad, bad)

def public_projection():
    baseline = snapshot(W / 'public'); candidate = snapshot(STAGE / 'candidate/public')
    EVIDENCE['current_W760'] = baseline; EVIDENCE['candidate772'] = candidate
    check('currentW760files368dirs', (baseline['regular_files'], baseline['child_directories']) == (760, 368))
    check('candidate772files373dirs', (candidate['regular_files'], candidate['child_directories']) == (772, 373))
    check('Wcompletecurrentguardmatchesproducerbefore', same_typed(baseline, load(STAGE / 'BUILD_GUARDS_BEFORE.json')['public']))
    check('candidatecompleteinventorymatchesactual', same_typed(candidate, load(STAGE / 'PROSPECTIVE_PUBLIC.json')))
    old = {r['path']: r for r in baseline['files']}; new = {r['path']: r for r in candidate['files']}
    deleted, added = sorted(set(old) - set(new)), sorted(set(new) - set(old))
    modified = sorted(k for k in set(old) & set(new) if old[k] != new[k])
    plan = load(STAGE / 'PUBLIC_PAYLOADS.json'); contract = load(LANE / 'TARGETS.json')
    wanted = {r['path'][7:]: r['status'] for r in contract['exact_public_target_leaves']}
    actual = {r['path'][7:]: r['action'] for r in plan['targets']}
    check('actual14targetplanmatchesINITIALexactpathsandactions', actual == wanted and len(plan['targets']) == 14)
    check('exact12A2Mprojectionnodeletions', not deleted and {k: 'A' for k in added} | {k: 'M' for k in modified} == wanted,
          dict(added=added, modified=modified, deleted=deleted))
    check('all758untargetedoldcandidatefileswholebytesmodes', sum(k not in modified for k in old) == 758 and all(new.get(k) == row for k, row in old.items() if k not in wanted))
    olddirs = {r['path']: r['mode'] for r in baseline['directories']}
    newdirs = {r['path']: r['mode'] for r in candidate['directories']}
    extra = sorted(set(newdirs) - set(olddirs))
    check('exact5newdirectories0755old368modeexact', extra == sorted(contract['exact_new_public_child_directories']) == plan['new_directories'] and all(newdirs[k] == v for k, v in olddirs.items()) and all(newdirs[k] == '0755' for k in extra))
    check('publicrootmodeandall17DSStorepreserved', candidate['root_mode'] == baseline['root_mode'] and sum(Path(k).name == '.DS_Store' for k in new) == 17 and all(new[k] == v for k, v in old.items() if Path(k).name == '.DS_Store'))
    bad = []
    for row in plan['targets']:
        rel = row['path'][7:]
        if pin(STAGE / 'candidate' / row['path']) != row['candidate'] or row['candidate']['mode'] != '0644':
            bad.append(rel + ': candidate')
        if row['action'] == 'M' and pin(W / row['path']) != row['baseline']:
            bad.append(rel + ': baseline')
        if row['action'] == 'A' and (row['baseline'] is not None or (W / row['path']).exists()):
            bad.append(rel + ': addition preexists')
    check('every14actualtargetpinandbaseline', not bad, bad)
    for filename, count in [('W_PUBLIC_BASELINE.sha256', 760), ('W_PUBLIC_TOPOLOGY_MODES.txt', 1129)]:
        lines = (LANE / filename).read_text().splitlines(); bad = []
        for line in lines:
            if filename.endswith('sha256'):
                sha, name = line.split('  ', 1)
                ok = pin(Path(name))['SHA256'] == sha
            else:
                bits, name = line.split(' ', 1)
                ok = Path(name).lstat().st_mode == int(bits, 8)
            if not ok: bad.append(name)
        check('INITIALwholepublicbaseline: ' + filename, len(lines) == count and not bad, bad)

class DOM(HTMLParser):
    VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text = text; self.nodes = []; self.stack = []; self.offsets = [0]
        for match in re.finditer('\n', text): self.offsets.append(match.end())
        self.feed(text); self.close()
        if self.stack: raise ValueError('unclosed HTML stack')
    def index(self):
        line, column = self.getpos(); return self.offsets[line-1] + column
    def handle_starttag(self, tag, attrs):
        start = self.index(); end = start + len(self.get_starttag_text())
        node = dict(tag=tag, attrs=dict(attrs), start=start, open_end=end,
                    parent=self.stack[-1] if self.stack else None, close_start=end, end=end)
        if len(dict(attrs)) != len(attrs): raise ValueError('duplicate HTML attribute')
        self.nodes.append(node)
        if tag not in self.VOID: self.stack.append(len(self.nodes)-1)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID: self.stack.pop()
    def handle_endtag(self, tag):
        if not self.stack or self.nodes[self.stack[-1]]['tag'] != tag:
            raise ValueError('unbalanced HTML closing tag: ' + tag)
        node = self.nodes[self.stack.pop()]; start = self.index()
        node['close_start'] = start; node['end'] = self.text.index('>', start) + 1
    def tags(self, tag):
        return [n for n in self.nodes if n['tag'] == tag]
    def raw(self, node):
        return self.text[node['start']:node['end']]
    def inner(self, node):
        return self.text[node['open_end']:node['close_start']]

def script_node(dom):
    nodes = [n for n in dom.tags('script') if n['attrs'].get('type') == 'application/ld+json']
    if len(nodes) != 1: raise ValueError('expected exactly1JSONschema')
    return nodes[0]

def schema_value(dom):
    return json_text(dom.inner(script_node(dom)))

def text_of(raw):
    return unescape(re.sub(r'<[^>]+>', '', raw))

def article_checks():
    receipts = []; items = []
    contract = load(LANE / 'TARGETS.json')
    for cfg in contract['article_source_contracts']:
        record = cfg['record']; root = BASE / cfg['writer']
        source = (root / cfg['article']).read_bytes()
        slug = cfg['canonical_candidate'].rstrip('/').split('/')[-1]
        candidate = (STAGE / 'candidate/public/research' / slug / 'index.html').read_bytes()
        old, new = source.decode(), candidate.decode(); olddom, newdom = DOM(old), DOM(new)
        oh, nh = olddom.tags('head'), newdom.tags('head')
        if len(oh) != 1 or len(nh) != 1: raise ValueError('article head count')
        oh, nh = oh[0], nh[0]
        check(str(record) + ': complete outsideHEADexact', old[:oh['start']].encode() == new[:nh['start']].encode() and old[oh['end']:].encode() == new[nh['end']:].encode())
        main = (root / cfg['MAIN']).read_bytes()
        check(str(record) + ': entireMAINincludingtrailingnewlineexact', candidate.count(main) == source.count(main) == 1 and digest(main) == cfg['MAIN_SHA256'] and len(main) == cfg['MAIN_bytes'])
        before, after = schema_value(olddom), schema_value(newdom)
        canonical = cfg['canonical_candidate']; rels = cfg['native_order']
        check(str(record) + ': activeexactcanonicalschemaidentity', after.get('url') == canonical and after.get('@id') == canonical + '#article' and same_typed(after.get('mainEntityOfPage'), {'@type':'WebPage','@id':canonical}))
        restored = json.loads(json.dumps(after))
        for key in ['url', '@id', 'mainEntityOfPage']: restored.pop(key, None)
        for original, current, rel in zip(before['encoding'], restored['encoding'], rels):
            check(str(record) + ': exactpublicencodingURL:' + rel, current['contentUrl'] == canonical + rel)
            current['contentUrl'] = original['contentUrl']
        check(str(record) + ': everyoriginalschemakeytypeandvalueexactafteridentitynormalization', same_typed(before, restored))
        def meta(dom):
            rows = [n['attrs'] for n in dom.tags('meta') if 'name' in n['attrs'] or 'property' in n['attrs']]
            names = [r.get('name', r.get('property')) for r in rows]
            if len(names) != len(set(names)): raise ValueError('duplicate article meta')
            return {r.get('name', r.get('property')): r.get('content') for r in rows}
        om, nm = meta(olddom), meta(newdom)
        wanted_meta = {k: v for k, v in om.items() if k not in ('robots','googlebot')}
        wanted_meta.update(citation_pdf_url=canonical + rels[0])
        wanted_meta.update({'og:url':canonical, 'og:site_name':'Alec Kriebel'})
        check(str(record) + ': exactmetafieldsandvaluesonlyauthorizedactivation', same_typed(wanted_meta, nm))
        links = [n['attrs'] for n in newdom.tags('link')]
        check(str(record) + ': exactcanonicalsharedstyleandnobase', links == [{'rel':'stylesheet','href':'/research/research.css'}, {'rel':'canonical','href':canonical}] and not newdom.tags('base'))
        def scrub(dom):
            edits = []; sn = script_node(dom)
            edits.append((sn['open_end'], sn['close_start'], 'SCHEMA_CONTENT'))
            for node in dom.tags('meta') + dom.tags('link'):
                a = node['attrs']; key = a.get('name', a.get('property'))
                if key in ('robots', 'googlebot', 'og:url', 'og:site_name') or a.get('rel') == 'canonical':
                    stop = node['end'] + (dom.text[node['end']:node['end']+1] == '\n')
                    edits.append((node['start'], stop, ''))
                elif key == 'citation_pdf_url' or a.get('rel') == 'stylesheet':
                    edits.append((node['start'], node['end'], 'ACTIVATED_FIELD'))
            result = dom.raw(dom.tags('head')[0]); offset = dom.tags('head')[0]['start']
            for start, end, value in sorted(edits, reverse=True):
                result = result[:start-offset] + value + result[end-offset:]
            return result.encode()
        check(str(record) + ': completeHEADrawnormalizationleavesnootherchange', scrub(olddom) == scrub(newdom))
        model = load(root / cfg['model'])
        abstract = model['complete_original_abstract'] if record == 23205181 else model['abstract']
        para = [n for n in newdom.tags('p') if n['attrs'].get('id') in ('abstract-text', 'original-abstract')]
        check(str(record) + ': wholevisibleDCschemamodelabstractexact', len(para) == 1 and text_of(newdom.inner(para[0])) == abstract == after['abstract'] == nm['DC.description'])
        check(str(record) + ': originaldateversionstatusandORCID', after['datePublished'] == model['publication_date'] == cfg['native_publication_date'] and after['version'] == model['native_version'] and after['author']['identifier'] == 'https://orcid.org/0009-0001-9320-500X')
        check(str(record) + ': Bibwholebytes', (STAGE / 'candidate/public/research' / slug / 'citation.bib').read_bytes() == (root / 'citation.bib').read_bytes())
        assets = []; model_assets = model['native_files_returned_order'] if record == 23205181 else model['native_asset_order']
        check(str(record) + ': nativePDFthenZIPorderandMIME', len(after['encoding']) == len(model_assets) == 2 and [e['encodingFormat'] for e in after['encoding']] == ['application/pdf', 'application/zip'])
        for rel, model_asset in zip(rels, model_assets):
            filename = Path(rel).name; sourcepath = BASE / 'papers' / str(record) / 'sources/assets' / filename
            writerpath = root / (str(Path(cfg['article']).parent / rel) if record == 23205181 else rel)
            stagepath = STAGE / 'candidate/public/research' / slug / rel
            data = stagepath.read_bytes(); md5 = hashlib.md5(data).hexdigest()
            native_md5 = model_asset['MD5'] if record == 23205181 else model_asset['native_checksum']
            check(str(record) + ': originalwriterstagedwholeassetandnativeMD5:' + rel,
                  data == sourcepath.read_bytes() == writerpath.read_bytes() and native_md5 == 'md5:' + md5 and len(data) == model_asset['bytes'])
            assets.append(dict(path=rel, **pin(stagepath), MD5=md5))
        check(str(record) + ': iframepathandfragmentexact', [n['attrs'] for n in olddom.tags('iframe')] == [n['attrs'] for n in newdom.tags('iframe')])
        if record == 23205181:
            check('dyadicoriginalnullaffiliationpreserved', 'affiliation' not in after['author'] and model['native_metadata']['creators'][0]['affiliation'] is None)
        else:
            check(str(record) + ': independentresearcheraffiliationpreserved', after['author']['affiliation']['name'] == 'Independent researcher')
        receipts.append(dict(record=record, source_article=pin(root / cfg['article']), candidate_article=pin(STAGE / 'candidate/public/research' / slug / 'index.html'), MAIN=pin(root / cfg['MAIN']), abstract_SHA256=digest(abstract.encode()), assets=assets))
        items.append(dict(record=record, canonical=canonical, site_path='/research/' + slug + '/',
                          title=model['title'], description=model['description'] if record == 23205181 else model['meta_description'],
                          date=model['publication_date'], status=after['creativeWorkStatus'], native_rels=rels))
    EVIDENCE['article_receipts'] = receipts; EVIDENCE['expected_new_items'] = items

def json_units(dom):
    node = script_node(dom); raw = dom.inner(node)
    schema = json_text(raw); markers = list(re.finditer(r'"itemListElement"\s*:\s*\[', raw))
    if len(markers) != 1: raise ValueError('ambiguous itemListElement')
    start = markers[0].end()-1; decoder = json.JSONDecoder()
    array, end = decoder.raw_decode(raw, start); spans = []; pos = start+1
    while True:
        while raw[pos].isspace(): pos += 1
        if raw[pos] == ']': break
        value, stop = decoder.raw_decode(raw, pos); spans.append((pos, stop, value)); pos = stop
        while raw[pos].isspace(): pos += 1
        if raw[pos] == ',': pos += 1
        elif raw[pos] != ']': raise ValueError('invalid JSON delimiter')
    if pos != end-1 or not same_typed(array, schema['mainEntity']['itemListElement']):
        raise ValueError('array structure mismatch')
    return node, raw, spans, end-1, schema

def xml_spans(raw):
    parser = expat.ParserCreate(namespace_separator='|'); spans = []; stack = []
    def start(name, attrs):
        if name.split('|')[-1] == 'url': stack.append(parser.CurrentByteIndex)
    def end(name):
        if name.split('|')[-1] == 'url':
            startpos = stack.pop(); stop = raw.index(b'>', parser.CurrentByteIndex) + 1
            spans.append((startpos, stop))
    parser.StartElementHandler = start; parser.EndElementHandler = end; parser.Parse(raw, True)
    return spans

def xml_typed(node):
    return (node.tag, dict(node.attrib), node.text, node.tail, [xml_typed(c) for c in node])

def aggregates():
    old = (LANE / 'BASELINE_index.html').read_bytes().decode('utf-8'); new = (STAGE / 'candidate/public/research/index.html').read_bytes().decode('utf-8')
    check('bothproducerandINITIALwholebaselineindexbuffersmatchW', old.encode() == (STAGE / 'BASELINE_INDEX.html').read_bytes() == (W / 'public/research/index.html').read_bytes())
    od, nd = DOM(old), DOM(new)
    on, os, ou, oc, ov = json_units(od); nn, ns, nu, nc, nv = json_units(nd)
    check('old123new126typedListItemnumericcount', len(ou) == 123 and len(nu) == 126 and ov['mainEntity']['numberOfItems'] == 123 and nv['mainEntity']['numberOfItems'] == 126 and type(nv['mainEntity']['numberOfItems']) is int and all(u[2]['@type'] == 'ListItem' for u in nu))
    check('allold123rawandtypedJSONorderedprefixexact', [os[a:b] for a,b,_ in ou] == [ns[a:b] for a,b,_ in nu[:123]] and same_typed([u[2] for u in ou], [u[2] for u in nu[:123]]))
    expected = [dict(**{'@type':'ListItem'}, position=124+i, url=v['canonical'], name=v['title']) for i,v in enumerate(EVIDENCE['expected_new_items'])]
    check('exact3newtypedJSONentriesorderidentityandnumericpositions', same_typed([u[2] for u in nu[123:]], expected))
    olduls, newuls = od.tags('ul'), nd.tags('ul')
    if len(olduls) != 1 or len(newuls) != 1: raise ValueError('index visible list count')
    olis = [n for n in od.tags('li') if n['start'] > olduls[0]['open_end'] and n['end'] <= olduls[0]['close_start']]
    nlis = [n for n in nd.tags('li') if n['start'] > newuls[0]['open_end'] and n['end'] <= newuls[0]['close_start']]
    check('allold123visibleunitsnew126exactorderedprefix', len(olis) == 123 and len(nlis) == 126 and [od.raw(n) for n in olis] == [nd.raw(n) for n in nlis[:123]])
    for item, node in zip(EVIDENCE['expected_new_items'], nlis[123:]):
        date = datetime.strptime(item['date'], '%Y-%m-%d'); human = str(date.day) + date.strftime(' %B %Y')
        expected_html = '<li><a href="' + item['site_path'] + '">' + escape(item['title']) + '</a><br><span class="entry-meta">' + human + ' · ' + escape(item['status']) + '</span><p>' + escape(item['description']) + '</p><p><a href="' + item['site_path'] + item['native_rels'][0] + '">PDF</a> · <a href="https://doi.org/10.5281/zenodo.' + str(item['record']) + '">Zenodo</a></p></li>'
        check(str(item['record']) + ': newvisibleentryexactadoptedcopydatePDFandDOI', nd.raw(node) == expected_html)
    insert_start = nu[123][0]-2
    check('JSONappendseamexactandoldtrailingbytespreserved', ns[insert_start:nu[123][0]] == ', ' and ns[nu[122][1]:insert_start] == os[ou[-1][1]:oc] and ns[nu[-1][1]:nc] == '' and all(ns[nu[i][1]:nu[i+1][0]] == ', ' for i in (123,124)))
    restored_schema = ns[:insert_start] + ns[nu[-1][1]:]
    restored_schema, count = re.subn(r'("numberOfItems"\s*:\s*)126(?!\d)', r'\g<1>123', restored_schema)
    check('wholeJSONschemareversiblecountand3unitremoval', count == 1 and restored_schema == os)
    restored = new[:nn['open_end']] + restored_schema + new[nn['close_start']:]
    rd = DOM(restored); rul = rd.tags('ul')[0]; rlis = [n for n in rd.tags('li') if n['start'] > rul['open_end'] and n['end'] <= rul['close_start']]
    seam = rlis[123]['start']-1
    check('visibleinsertionnewlineandtailseamexact', restored[seam:seam+1] == '\n' and restored[rlis[-1]['end']:rul['close_start']] == '\n')
    restored = restored[:seam] + restored[rul['close_start']:]
    check('WHOLEindexbytebufferreversibleexact', restored.encode() == old.encode(), dict(restored_SHA256=digest(restored.encode()), baseline_SHA256=digest(old.encode())))
    rawold = (LANE / 'BASELINE_sitemap.xml').read_bytes(); rawnew = (STAGE / 'candidate/public/research/sitemap.xml').read_bytes()
    check('bothproducerandINITIALwholesitemapbaselinebuffersmatchW', rawold == (STAGE / 'BASELINE_SITEMAP.xml').read_bytes() == (W / 'public/research/sitemap.xml').read_bytes())
    xo, xn = xml_spans(rawold), xml_spans(rawnew); to, tn = ET.fromstring(rawold), ET.fromstring(rawnew)
    check('old124new127XMLnodesrawtypednamespaceorderedprefixexact', len(xo) == len(to) == 124 and len(xn) == len(tn) == 127 and [rawold[a:b] for a,b in xo] == [rawnew[a:b] for a,b in xn[:124]] and [xml_typed(c) for c in to] == [xml_typed(c) for c in list(tn)[:124]] and to.tag == tn.tag and to.attrib == tn.attrib)
    builddate = load(STAGE / 'AGGREGATE_PRESERVATION.json')['sitemap_lastmod_is_private_build_date']
    check('declarednewlastmodbuilddate20261117', builddate == '2026-11-17')
    newnodes = list(tn)[124:]
    wanted_nodes = [('https://aleckriebel.com/research/' + item['site_path'].split('/')[2] + '/', builddate) for item in EVIDENCE['expected_new_items']]
    actual_nodes = [(node.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text, node.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod').text) for node in newnodes]
    check('exact3sitemapcanonicalnewnodesandlastmodsorder', actual_nodes == wanted_nodes and all(len(n) == 2 for n in newnodes))
    expected_raw_nodes = [('<url><loc>' + canonical + '</loc><lastmod>' + date + '</lastmod></url>').encode('utf-8') for canonical, date in wanted_nodes]
    check('exact3newXMLrawnodestagsattributesorderandtext', [rawnew[a:b] for a,b in xn[124:]] == expected_raw_nodes)
    check('XMLnewappendseamnewlineexact', rawnew[xn[-1][1]:xn[-1][1]+1] == b'\n')
    xmlrestored = rawnew[:xn[124][0]] + rawnew[xn[-1][1]+1:]
    check('WHOLEsitemapbytebufferreversibleexact', xmlrestored == rawold, dict(restored_SHA256=digest(xmlrestored), baseline_SHA256=digest(rawold)))
    receipt = load(STAGE / 'AGGREGATE_PRESERVATION.json')
    check('produceraggregateevidenceagreesactualoldandnewunits', receipt['old_visible_units'] == [od.raw(n) for n in olis] and same_typed(receipt['old_typed_JSON_units'], [u[2] for u in ou]) and receipt['old_raw_JSON_units'] == [os[a:b] for a,b,_ in ou] and receipt['old_raw_sitemap_nodes'] == [rawold[a:b].decode() for a,b in xo] and same_typed(receipt['new_typed_JSON_units'], expected) and receipt['new_raw_sitemap_nodes'] == [rawnew[a:b].decode() for a,b in xn[124:]])
    EVIDENCE['aggregate'] = dict(old_visible_raw=[od.raw(n) for n in olis], new_visible_raw=[nd.raw(n) for n in nlis[123:]], new_JSON=expected, new_XML=actual_nodes, index_whole_reversal_SHA256=digest(restored.encode()), sitemap_whole_reversal_SHA256=digest(xmlrestored))

def retained_history_and_native():
    history = load(STAGE / 'BUILD_HISTORY.json'); final = load(STAGE / 'FINAL.json')
    check('literalbuildhistory10andcollector11v3unexecutedretained', history['complete_build_exit_history'] == [1,0] and history['preparation_input_collector_history'] == [1,1] and history['preparation_v3_executed'] is False and final['complete_build_exit_history'] == [1,0])
    expected = [('BUILD_RUN_RECEIPT.json','BUILD.stdout.txt','BUILD.stderr.txt',1,0,1063),
                ('BUILD_v2_RUN_RECEIPT.json','BUILD_v2.stdout.txt','BUILD_v2.stderr.txt',0,160,0),
                ('INPUT_CUSTODY_RECEIPT.json','INPUT_CUSTODY.stdout.txt','INPUT_CUSTODY.stderr.txt',1,0,870),
                ('INPUT_CUSTODY_v2_RECEIPT.json','INPUT_CUSTODY_v2.stdout.txt','INPUT_CUSTODY_v2.stderr.txt',1,0,811)]
    for receipt, stdout, stderr, exitcode, outbytes, errbytes in expected:
        obj = load(STAGE / receipt)
        check('retainedliteralrun:' + receipt, obj['exit_code'] == exitcode and (STAGE / stdout).stat().st_size == outbytes and (STAGE / stderr).stat().st_size == errbytes)
    check('failedcollectorv3anderratumremainfinitepayloads', all((STAGE / n).is_file() for n in ['collect_input_custody.py','collect_input_custody_v2.py','collect_input_custody_v3.py','build_private_stage.py','SCHEMA_ERRATUM.md']))
    check('currentWnativeHEADindex58700records', NATIVE_BEFORE[1]['OID'] == 'b767102567ad89aff909f9f11c0e8b7d72b75c40' and NATIVE_BEFORE[1]['files']['index']['SHA256'] == '6e57311ffb524aabe230dec4962ebfa6983085674882606f5b8594aa1d4cee18' and (W / '.git/index').read_bytes()[:12] == b'DIRC\x00\x00\x00\x02\x00\x00\xe5L')
    check('currentMathauthorizedrootcheckpointmain', NATIVE_BEFORE[0]['branch'] == 'refs/heads/main' and NATIVE_BEFORE[0]['OID'] == EXPECTED_M, NATIVE_BEFORE[0]['OID'])
    bad = []; expected_math_drift = []
    for line in (LANE / 'NATIVE_GUARD_PINS.sha256').read_text().splitlines():
        sha, name = line.split('  ', 1); path = Path(name); observed = pin(path)['SHA256']
        if observed != sha:
            if path.is_relative_to(M / '.git') and path.name in ('index','packed-refs'):
                expected_math_drift.append(dict(path=name, INITIAL_SHA256=sha, current_SHA256=observed))
            else: bad.append(name)
    check('INITIALWandnonchangingMathnativeguardsCSSexact', not bad, bad)
    EVIDENCE['authorized_postINITIAL_Math_checkpoint_drift'] = expected_math_drift
    EVIDENCE['native_before_own_audit'] = NATIVE_BEFORE

for label, function in [('initial and complete producer', initial_and_stage), ('adopted and source custody', adopted_and_sources),
                        ('full public projection', public_projection), ('whole article fidelity', article_checks),
                        ('structural reversible aggregates', aggregates), ('literal history and native guards', retained_history_and_native)]:
    task(label, function)

def final_guard():
    check('original17INITIALfilesbyteandmodeexactthroughownaudit', {n: pin(LANE / n) for n in INITIAL_FILES} == INITIAL_BEFORE)
    check('producer815wholefrozenextentunchangedduringownaudit', same_typed(snapshot(STAGE), EVIDENCE['producer815']))
    check('currentW760wholepublicunchangedduringownaudit', same_typed(snapshot(W / 'public'), EVIDENCE['current_W760']))
    check('all155adoptedand323sourceguardsunchangedduringownaudit', all(same_typed(snapshot(Path(s['root'])), s) for s in EVIDENCE['adopted155'] + EVIDENCE['source323']))
    after = [native(M), native(W)]; EVIDENCE['native_after_own_audit'] = after
    check('rawcurrentMathandWnativeguardsunchangedduringownaudit', same_typed(NATIVE_BEFORE, after))

task('final preservation guards', final_guard)
failed = [r for r in CHECKS if not r['PASS']]
status = 'PASS_PRIVATE_STAGE_FIDELITY' if not failed else 'CORRECTIONS_REQUIRED'
result = dict(schema='independent-informed-stage-audit-data-result-v1', UTC=now(), status=status,
              role='informed continuation; implementation fidelity only', own_audit_invocations=1,
              checks=CHECKS, failed_checks=len(failed), evidence=EVIDENCE,
              producer_native_old_helper_or_Git_execution=0, network_browser_CUA_render_Sheet_deploy_contact=0,
              production_authority=False, reader_or_live_download_certificate=False, new_scientific_PASS=False, follow_up=None)
write('AUDIT_RESULT.json', result)
with (OUT / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- ' + now() + ' — One wholly read own data-only audit executed once. ' + status + '; ' + str(len(CHECKS)) + ' checks; ' + str(len(failed)) + ' failed. Complete original17 INITIAL and815 producer/155 adopted/323 source/760 W preservation rechecked. Completion100% of finite audit decision, whether PASS or precise correction. Production/reader authority remains false. Freeze after final seal.\n')
report = ('# Informed private integration audit\n\n**' + status + '**. Completion100% of this finite audit.\n\n'
          'This resumes the earlier sealed audit after interruption. It is an informed continuation, not a new blind family, scientific review, copy acceptance or production adoption. The17 INITIAL files remain exact.\n\n'
          'The audit read the corrected complete builder, actual root adoption, exact14-target plan, complete three candidate HTML pages and private heads/models/Bibs before one fresh own data-only validation. No producer/native/old helper/Git code was executed.\n\n'
          'The full815-file/375-directory stage includes the full772-file/373-directory candidate and17 DSStore files. The intended projection is12 additions/two aggregate modifications and five new directories. The checks cover all155 adopted private files,323 source files,15 PREP files,758 untargeted candidate files and760 unchanged current W files, including modes and ignored/empty objects.\n\n'
          'Article checks preserve all outside-HEAD bytes, complete MAIN including trailing newline, complete visible/DC/schema/model abstracts, all Bib bytes and six original assets with SHA256/MD5/order. Raw HEAD normalization and typed schema comparison admit only the authorized identity/citation/robots/shared-style fields. /research/research.css and og:site_name implement the later root-authorized shared-style/OG identity; no base is introduced.\n\n'
          'Structural parsers protect old123 visible/typed/raw ListItems and124 XML nodes as exact ordered prefixes. Removing the three additions and declared seams, and reversing only123→126, must reproduce both full original aggregate buffers byte-exact. New entries derive dates/status/descriptions/titles/PDF/DOI from adopted copies; sitemap lastmod2026-11-17 is the declared private build date.\n\n'
          'Literal retained histories are build[1,0], collectors[1,1], unexecuted v3 and schema erratum. The erroneous older dyadic root-mode attribution is not promoted into a clean first-pass claim. Math has the separately authorized later root checkpoint; current raw Math/W native states are preserved before/after this audit.\n\n'
          'AUDIT_RESULT.json records every check and complete current file inventories. Failed checks: ' + str(len(failed)) + '.\n')
if failed:
    report += '\n' + '\n'.join('- ' + r['check'] + ': ' + json.dumps(r['details'], ensure_ascii=False) for r in failed) + '\n'
report += ('\nA static fidelity result grants no installation/publication/Sheet/deployment/AA authority or browser/mobile/PDF-reader/live-download certificate. Existing stress/wreath iframe fragments remain accepted copy. No external contact or outreach occurred. No new scientific or priority claim is made. follow_up:null.\n')
with (OUT / 'REPORT.md').open('x') as f: f.write(report)
print(status + ': ' + str(len(CHECKS)) + ' checks, ' + str(len(failed)) + ' failed; original INITIAL preserved.', flush=True)

# Seal the finite complete lane after all ordinary payload and stdout writes.
controls = {'OWNED_MANIFEST.json', 'FINAL.json'}
for name in controls:
    with (LANE / name).open('x') as f: pass
snap = snapshot(LANE)
manifest_rows = [dict(path=r['path'], mode=r['mode'], terminal_control=True) if r['path'] in controls else r for r in snap['files']]
manifest = dict(schema='finite-complete-informed-stage-audit-manifest-v1', UTC=now(), owned_root=str(LANE),
                regular_files=snap['regular_files'], child_directories=snap['child_directories'], root_mode=snap['root_mode'],
                files=manifest_rows, directories=snap['directories'],
                exact_terminal_recursive_hash_exclusions=[str(LANE / n) for n in sorted(controls)],
                other_exclusions=[], no_future_subtree_or_basename_exclusions=True,
                all_ignored_hidden_empty_bytes_modes_and_topology_included=True, original17_INITIAL_payloads_preserved=True)
with (LANE / 'OWNED_MANIFEST.json').open('w') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False); f.write('\n')
final = dict(schema='independent-informed-stage-audit-FINAL-v1', UTC=now(), status=status,
             role='resumed existing informed audit; not a new blind scientific/copy family', completion_percent=100,
             owned_root=str(LANE), extent={k: snap[k] for k in ('regular_files','child_directories','root_mode')},
             manifest=dict(path='OWNED_MANIFEST.json', **pin(LANE / 'OWNED_MANIFEST.json')),
             result=dict(path='continuation-20261117/AUDIT_RESULT.json', **pin(OUT / 'AUDIT_RESULT.json')),
             report=dict(path='continuation-20261117/REPORT.md', **pin(OUT / 'REPORT.md')),
             original_INITIAL_SEAL=dict(path='INITIAL_SEAL.json', **pin(LANE / 'INITIAL_SEAL.json')),
             producer_FINAL=dict(path=str(STAGE / 'FINAL.json'), **pin(STAGE / 'FINAL.json')),
             root_adoption=dict(path=str(AUTH), **pin(AUTH)),
             checks=len(CHECKS), failed_checks=failed, own_data_audit_invocations=1,
             original17_INITIAL_files_preserved=True,
             finite_scope='815producer/375dirs;772candidate/373dirs;14targets12A2M/5dirs;155adopted;323sources;15PREP;760W;758untargeted',
             whole_aggregate_reversal_required=True, complete_build_history=[1,0], preparation_collector_history=[1,1], unexecuted_v3_retained=True,
             prior_read_limits='Prior INITIAL read limits preserved. First resumed combined builder/control display clipped; bounded full corrected-builder/FINAL/plan rereads completed. Old123individual catalogue semantics not personally rereviewed; exact whole bytes and raw/typed structure guarded.',
             production_authority=False, reader_live_download_certificate=False, new_scientific_PASS=False,
             native_producer_old_helper_Git_network_browser_CUA_Sheet_deploy_contact_actions=0,
             exact_terminal_control_hash_exclusions=[str(LANE / n) for n in sorted(controls)],
             other_exclusions=[], quiescent=True, postseal_writes_or_helper_executions_allowed=False, follow_up=None)
with (LANE / 'FINAL.json').open('w') as f:
    json.dump(final, f, indent=2, ensure_ascii=False); f.write('\n')
