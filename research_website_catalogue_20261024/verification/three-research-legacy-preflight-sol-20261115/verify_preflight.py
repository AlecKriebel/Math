#!/usr/bin/env python3
"""Finite offline read-only verification. No imports of other task programs.

Default requires all three exact terminal controls. --preseal requires none.
Both modes authenticate and rescan the same fixed corpus by reference. Neither
mode writes, uses Git/network, extracts PDFs, or interprets scientific claims.
"""
from pathlib import Path, PurePosixPath
from collections import Counter
import hashlib
import json
import stat
import sys
import unicodedata

A = Path(__file__).resolve().parent
P = A.parents[1]
DOCS = 'f5f5fb2fb18196b604d7b568e3e58ccc1bf127b3'
ROOT = 'dd84509773f131b7c059781361ac6b667f2f607f'
COMMIT = 'd767ab05bba4e63e75b8341ecb65d387e29a57bc'
LITERAL = 'NO GENUINE MATCHING LEGACY HTML IDENTIFIED IN THE ENUMERATED CURRENT DOCS CORPUS'
PAYLOADS = tuple(sorted('''
.gitignore
ADVERSARIAL_REVIEW.json
AUTHENTICATED_CORPUS_INTERFACE.json
COLLECT.stderr
COLLECT.stdout
COLLECT_EXECUTION.json
CORPUS_RECEIPT.json
EXCLUSIONS.json
INITIAL_EXPECTATIONS.json
INITIAL_LOG.md
INITIAL_MANIFEST.json
INITIAL_SEAL.json
INPUT_BINDINGS.json
PATHNAME_SEARCH_RESULTS.json
QUERY_DEFINITIONS.json
READ_LEDGER.json
REMOTE_BOUNDARY.json
REPORT.md
RESEARCH_LOG.md
RESUME_READ_LEDGER.json
SEARCH_RESULTS.json
TAKEOVER.json
TARGET_IDENTITIES.json
VERDICT.json
collect_identity_evidence.py
raw/close-branch.connector.json
raw/open-branch.connector.json
raw/open-root.connector.json
verify_preflight.py
'''.split()))
CONTROLS = ('CLOSURE_RECEIPT.json', 'FINAL_SEAL.json', 'OWNED_MANIFEST.json')
CHECKS = 0


def need(ok, why):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(why)


def canonical(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def equal(a, b, why):
    need(canonical(a) == canonical(b), why)


def whole(p):
    p = Path(p)
    need(p.is_absolute(), 'absolute read path: ' + str(p))
    for q in (p,) + tuple(p.parents):
        need(not q.is_symlink(), 'no symlink component: ' + str(q))
    need(stat.S_ISREG(p.stat().st_mode), 'ordinary file: ' + str(p))
    return p.read_bytes()


def load(p):
    def unique(items):
        d = {}
        for k, v in items:
            need(k not in d, 'duplicate JSON key: ' + k)
            d[k] = v
        return d
    return json.loads(whole(p), object_pairs_hook=unique)


def check(r):
    b = whole(r['path'])
    need(type(r['bytes']) is int and len(b) == r['bytes'], 'whole size: ' + r['path'])
    need(hashlib.sha256(b).hexdigest() == r.get('SHA256', r.get('sha256')), 'whole SHA256: ' + r['path'])
    return b


def pin(p, relative=False):
    b = whole(p)
    return {'path': p.relative_to(A).as_posix() if relative else str(p),
            'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest()}


def obj(kind, b):
    return hashlib.sha1(kind.encode() + b' ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def tree(entries):
    names = [e['path'] for e in entries]
    need(len(names) == len(set(names)), 'unique direct tree names')
    body = b''
    for e in sorted(entries, key=lambda e: (e['path'] + ('/' if e['type'] == 'tree' else '')).encode()):
        need('/' not in e['path'] and e['path'] not in ('', '.', '..'), 'direct safe tree name')
        need(e['type'] in ('tree', 'blob') and e['mode'] in ('040000', '100644', '100755'), 'tree mode/type')
        body += e['mode'].lstrip('0').encode() + b' ' + e['path'].encode() + b'\0' + bytes.fromhex(e['sha'])
    return obj('tree', body)


def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s).casefold() if c.isalnum())


def wrapper(name, url):
    o = load(A / name)
    need(o['actual_tool'] == 'mcp__codex_apps__github_fetch' and o['actual_URL'] == url, 'actual connector identity')
    w = o['whole_returned_wrapper']
    need(w['isError'] is False, 'connector not error')
    need(w['structuredContent']['url'] == url, 'connector returned URL')
    return json.loads(w['structuredContent']['content'])


def verify(final):
    files, dirs = [], []
    for p in sorted(A.rglob('*')):
        need(not p.is_symlink(), 'own namespace no symlinks')
        m = p.stat().st_mode
        if stat.S_ISREG(m):
            files.append(p.relative_to(A).as_posix())
        elif stat.S_ISDIR(m):
            dirs.append(p.relative_to(A).as_posix())
        else:
            need(False, 'own namespace no special files')
    equal(dirs, ['raw'], 'exact own directory extent')
    equal(files, sorted(PAYLOADS + (CONTROLS if final else ())), 'exact finite file extent; no future/basename exclusions')
    check({'path': str(A / 'INITIAL_SEAL.json'), 'bytes': 569,
           'SHA256': '29502e4979fb0959ee74e416c4558cf4e6fe370e7a18c7d9b6876faacdcec66f'})
    initial = load(A / 'INITIAL_SEAL.json')
    check(initial['manifest'])
    im = load(A / 'INITIAL_MANIFEST.json')
    equal(im['directories'], [], 'initial directory extent')
    need(im['initial_payloads_immutable'] is True and initial['no_correspondence_findings_yet'] is True, 'frozen independent INITIAL')
    for r in im['files']:
        need(Path(r['path']).parent == A, 'initial own path')
        check(r)
    for r in load(A / 'INPUT_BINDINGS.json'):
        check(r)
    targets = load(A / 'TARGET_IDENTITIES.json')
    expected = [('23418581', 132, 'simple-young-nonprojective-injectives'),
                ('23202966', 135, 'binary-relation-liveness'),
                ('23205305', 136, 'rational-point-undecidability')]
    equal([(t['record_id'], t['sheet_row'], t['slug_proposal']) for t in targets], expected, 'fixed targets only')
    for t in targets:
        source = json.loads(check(t['source_binding']))
        owner = json.loads(check(t['owner_config_binding']))
        root = json.loads(check(t['root_editorial_authority_binding']))
        equal(str(source['record_id']), t['record_id'], 'source record')
        for k, tk in [('title', 'title'), ('DOI', 'DOI'), ('publication_date', 'native_publication_date'),
                      ('version_field_present', 'native_version_field_present'), ('version', 'native_version')]:
            equal(source[k], t[tk], 'source selected identity: ' + k)
        equal(owner['title'], t['title'], 'owner title')
        equal(owner.get('slug', owner.get('promotion', {}).get('slug_proposal')), t['slug_proposal'], 'owner proposal')
        need(str(root['record_id']) == t['record_id'] and root['status'] == t['root_status_literal'], 'root authority identity/status')
        need(t['slug_is_future_proposal_not_current_canonical'] is True, 'proposal not live authority')
    base = 'https://api.github.com/repos/AlecKriebel/Math/'
    opened = wrapper('raw/open-branch.connector.json', base + 'branches/main')
    closed = wrapper('raw/close-branch.connector.json', base + 'branches/main')
    for b in (opened, closed):
        need(b['name'] == 'main' and b['commit']['sha'] == COMMIT and b['commit']['commit']['tree']['sha'] == ROOT, 'recorded remote boundary')
    root = wrapper('raw/open-root.connector.json', base + 'git/trees/' + ROOT)
    need(root['sha'] == ROOT and root['truncated'] is False and tree(root['tree']) == ROOT, 'complete actual root object')
    ds = [e for e in root['tree'] if e['path'] == 'docs']
    need(len(ds) == 1 and ds[0]['type'] == 'tree' and ds[0]['sha'] == DOCS, 'root docs entry')
    boundary = load(A / 'REMOTE_BOUNDARY.json')
    need(boundary['opening_commit'] == boundary['closing_commit'] == COMMIT, 'remote receipt commit')
    for call in boundary['actual_connector_calls_in_order']:
        check(call['binding'])
    check({'path': str(A / 'AUTHENTICATED_CORPUS_INTERFACE.json'), 'bytes': 327422,
           'SHA256': '4e3603f1683befb1c37a8ac5b0dc0fd37d277e618a96ba23d1fcd4cbdeb87f4f'})
    c = load(A / 'AUTHENTICATED_CORPUS_INTERFACE.json')
    need(c['current_docs_subtree'] == c['docs_tree_reconstructed'] == DOCS and c['root_tree'] == ROOT, 'corpus identities')
    refs = {Path(r['path']).name: r for r in c['reference_bindings']}
    need(len(c['reference_bindings']) == len(refs) == 5, 'exact five unique prior metadata references')
    equal(sorted(refs), sorted(['CURRENT_BLOB_BINDINGS.json', 'SEARCH_REPRESENTATIONS.json', 'docs-recursive.json', 'FINAL_SEAL.json', 'OWNED_MANIFEST.json']), 'finite old reference interface')
    for r in refs.values():
        check(r)
    equal(c['whole_blob_bindings'], json.loads(check(refs['CURRENT_BLOB_BINDINGS.json'])), 'entire original blob interface')
    equal(c['whole_text_representations'], json.loads(check(refs['SEARCH_REPRESENTATIONS.json'])), 'entire original text interface')
    rw = json.loads(check(refs['docs-recursive.json']))
    recursive = json.loads(rw['result']['structuredContent']['content'])
    need(recursive['sha'] == DOCS and recursive['truncated'] is False, 'complete recursive docs object')
    children = {}
    for e in recursive['tree']:
        p = PurePosixPath(e['path'])
        need(not p.is_absolute() and '..' not in p.parts, 'safe recursive path')
        parent = '' if str(p.parent) == '.' else str(p.parent)
        children.setdefault(parent, []).append({**e, 'path': p.name})
    reconstructed = []
    for e in recursive['tree']:
        if e['type'] == 'tree':
            h = tree(children[e['path']])
            need(h == e['sha'], 'reconstructed docs child')
            reconstructed.append({'path': e['path'], 'SHA1': h})
    need(tree(children['']) == DOCS and len(reconstructed) == 50, 'all51 docs objects including root')
    equal(reconstructed, c['recursive_tree_objects_reconstructed'], 'exact reconstructed tree interface')
    blobs = c['whole_blob_bindings']
    bypath = {r['path']: r for r in blobs}
    native = [e for e in recursive['tree'] if e['type'] == 'blob']
    need(len(blobs) == len(bypath) == len(native) == 254, 'exact254 unique blobs')
    equal(sorted(bypath), sorted('docs/' + e['path'] for e in native), 'whole blob/path coverage')
    for e in native:
        r = bypath['docs/' + e['path']]
        b = check(r['reused_complete_body'])
        need(r['blob'] == e['sha'] == obj('blob', b), 'whole immutable Git blob')
        need(r['mode'] == e['mode'] and r['bytes'] == len(b) and r['SHA256'] == hashlib.sha256(b).hexdigest(), 'whole blob mode/size/SHA256')
    reps = c['whole_text_representations']
    need(len(reps) == 260, 'exact260 text representations')
    equal(dict(Counter(r['kind'] for r in reps)), {'raw_UTF8': 137, 'decoded_HTML': 47, 'complete_PDF_text': 76}, 'representation types')
    textpaths = {r['public_path'] for r in reps}
    need(len(textpaths) == 213 and len(set(bypath) - textpaths) == 41, 'text coverage limits')
    htmlpaths = {p for p in bypath if p.casefold().endswith(('.html', '.htm'))}
    need(len(htmlpaths) == 47, 'exact47 HTML paths')
    for p in htmlpaths:
        equal(sorted(r['kind'] for r in reps if r['public_path'] == p), ['decoded_HTML', 'raw_UTF8'], 'every HTML has complete raw/decoded representations')
    aliases = {'23418581': ['miyachi', 'simple young', 'nonprojective injective', 'simple young nonprojective injectives'],
               '23202966': ['relation liveness', 'binary consequences', 'binary relation liveness'],
               '23205305': ['rational point undecidability', 'smooth projective', 'rational numbers']}
    queries = [{'record_id': t['record_id'], 'exact': [t['record_id'], t['DOI']],
                'compact': [t['title'], t['slug_proposal']] + aliases[t['record_id']]} for t in targets]
    equal(load(A / 'QUERY_DEFINITIONS.json'), queries, 'explicit finite identity queries')
    hits = []
    for r in reps:
        b = check(r['text_file'])
        text = b.decode('utf-8')
        need(r['public_path'] in bypath and r['blob'] == bypath[r['public_path']]['blob'], 'text belongs to current blob')
        if r['kind'] == 'raw_UTF8':
            need(obj('blob', b) == r['blob'], 'complete raw original representation')
        elif r['kind'] == 'complete_PDF_text':
            ex = r['original_whole_PDF_extract_binding']
            need(ex['pdf_blob'] == r['blob'] and ex['pdf_sha256'] == bypath[r['public_path']]['SHA256'], 'historical PDF extraction provenance')
            need(b == check(ex), 'whole historical PDF text bytes')
        n = norm(text)
        for q in queries:
            if any(s.casefold() in text.casefold() for s in q['exact']) or any(norm(s) in n for s in q['compact']):
                hits.append((q['record_id'], r['public_path'], r['kind']))
    pathhits = [(q['record_id'], p) for p in bypath for q in queries
                if any(norm(s) in norm(p) for s in q['exact'] + q['compact'])]
    equal(hits, [], 'no target text hits in bounded scan')
    equal(pathhits, [], 'no target pathname hits in bounded scan')
    equal(load(A / 'SEARCH_RESULTS.json'), [], 'literal saved text results')
    equal(load(A / 'PATHNAME_SEARCH_RESULTS.json'), [], 'literal saved pathname results')
    execution = load(A / 'COLLECT_EXECUTION.json')
    need(execution['exit'] == 0 and whole(A / 'COLLECT.stderr') == b'', 'actual prior collector exit0/empty stderr')
    need(hashlib.sha256(whole(A / 'collect_identity_evidence.py')).hexdigest() == execution['current_code_SHA256'], 'actual collector code pin')
    verdict = load(A / 'VERDICT.json')
    need(verdict['literal_verdict'] == LITERAL and verdict['docs_subtree'] == DOCS, 'literal bounded verdict')
    need(verdict['correspondence_only_no_scientific_verdict'] is True and verdict['root_independent_adoption_pending'] is True, 'scope and root adoption pending')
    equal(verdict['redirects_prepared_or_written'], [], 'no redirect work')
    for t, v in zip(targets, verdict['results']):
        need(v['record_id'] == t['record_id'] and v['genuine_matching_HTML'] is None, 'per-target negative')
        equal(v['redirect_candidate_paths'], [], 'no per-target redirect candidates')
    need(len(verdict['results']) == 3, 'three verdicts only')
    rows = [pin(A / name, True) for name in PAYLOADS]
    extent = {'files': rows, 'directories': ['raw']}
    digest = hashlib.sha256(canonical(extent).encode()).hexdigest()
    result = {'schema': 'strict-finite-read-only-legacy-preflight-v1', 'status': 'PASS',
              'final_seal_bound': False, 'payload_file_count': len(rows), 'directory_count': 1,
              'payload_bytes': sum(r['bytes'] for r in rows), 'payload_extent_SHA256': digest,
              'commit_as_observed': COMMIT, 'root_tree': ROOT, 'docs_subtree': DOCS,
              'whole_blob_paths': 254, 'text_representations': 260, 'HTML_paths_with_raw_and_decoded_text': 47,
              'text_hits': 0, 'pathname_hits': 0, 'literal_verdict': LITERAL,
              'network_Git_mutation_or_other_program_execution': False}
    if final:
        manifest = load(A / 'OWNED_MANIFEST.json')
        equal(manifest, {'schema': 'strict-finite-payload-manifest-v1', **extent,
                         'terminal_controls_exact_root_only': list(CONTROLS)}, 'entire finite own manifest')
        receipt = load(A / 'CLOSURE_RECEIPT.json')
        equal(receipt['result'], result, 'actual preseal result')
        need(receipt['exit_code'] == 0 and receipt['stderr'] == '' and receipt['full_current_helper_read_before_execution'] is True, 'actual successful read-only closure execution')
        seal = load(A / 'FINAL_SEAL.json')
        need(seal['status'] == 'SEALED_BOUNDED_LEGACY_CORRESPONDENCE_PREFLIGHT' and seal['completion_percent'] == 100, 'final bounded completion')
        equal(sorted(seal['bindings']), ['closure', 'manifest'], 'exact final bindings')
        for k, n in [('closure', 'CLOSURE_RECEIPT.json'), ('manifest', 'OWNED_MANIFEST.json')]:
            equal(seal['bindings'][k], pin(A / n), 'final terminal binding: ' + k)
        need(seal['root_independent_adoption_pending'] is True and seal['production_or_redirect_authority'] is False, 'final limited authority')
        result['final_seal_bound'] = True
    return result


if __name__ == '__main__':
    need(sys.argv[1:] in ([], ['--preseal']), 'only default or explicit --preseal accepted')
    print(json.dumps(verify(not sys.argv[1:]), ensure_ascii=False, sort_keys=True))
