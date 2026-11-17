"""Single closed literal private-copy edit; passive guards, no project execution."""
from pathlib import Path
import datetime, hashlib, json, shutil, stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
L = P / 'verification/thompson-cstar-editorial-corrected-sol-20261117'
W = P / 'verification/thompson-cstar-editorial-sol-20261117'
F = P / 'verification/thompson-cstar-editorial-fact-sol-20261117'
S = P / 'papers/23204212/sources'
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
specific_pins = {
    S / 'SOURCE_FINAL.json': 'b68fbb425b7d910a2508c46ff311491a1c797568dcf39d3c7deb0a0545e1afd5',
    S / 'SOURCE_MANIFEST.json': 'afa64c126da0aabc4a44ec242553e5b2354540eb1b0b60e55ab7b1a9855a09be',
    W / 'FINAL.json': '36c84f224773aa954a4e59a3152b2089e60c95710e88a12231931c646b1e8557',
    W / 'MANIFEST.json': '4c5cb453d5fec1544e0b6556b5d858c059657f24dd547b161358f40e14314a55',
    W / 'SEAL.json': 'eee46ef4f3c64b6f428538d38b64af343404fad31a152912ca926e1d7bba92d9',
    F / 'FINAL.json': '2c4723092ac4d6e7c7a1a7fae7842090fa91bdfbb857b2d3e613dd697b748ead',
    F / 'FINAL_MANIFEST.json': '056a582ec4ca0525882a8a95f1db67f267050932b50febd44d409fa8e8637afa',
    F / 'FINAL_SEAL.json': 'eb51f8476628f017a55f0855ec80de3a34c65e3d66ac79014a881575f0a71817',
    F / 'FACT_REPORT.md': '06796566a85580cfaa67bdf671ba24eb848c0acee1e18f0460d2bc2abad9f36c',
    P / 'verification/root-clearance-23204212-20261117.json': 'cf26226d4c236473c5cb75ede27c50f77e486761df16a624d39cf26abdbb797c',
    P / 'papers/23204212/reviews/root-continuation-20261117/ROOT_REVIEW.md': '71136fd6de5610566ccffa7142a2ecabac093e33bad245e06eb7a3d456d85501',
}

def row(p, relative):
    st = p.lstat()
    r = {'path': relative, 'mode_octal': oct(stat.S_IMODE(st.st_mode)), 'mtime_ns': st.st_mtime_ns, 'ctime_ns': st.st_ctime_ns, 'hidden_component': any(t.startswith('.') for t in Path(relative).parts if t != '.')}
    if stat.S_ISDIR(st.st_mode):
        r.update(kind='directory', empty=not any(p.iterdir()))
    else:
        assert stat.S_ISREG(st.st_mode), ('unexpected protected node', str(p))
        b = p.read_bytes()
        r.update(kind='file', bytes=len(b), empty=not b, sha256=sha(b), md5=hashlib.md5(b).hexdigest())
    return r

def tree(root, files, childdirs):
    entries = [row(p, '.' if p == root else p.relative_to(root).as_posix()) for p in [root] + sorted(root.rglob('*'), key=lambda p: p.relative_to(root).as_posix())]
    assert sum(r['kind'] == 'file' for r in entries) == files, str(root)
    assert sum(r['kind'] == 'directory' for r in entries) - 1 == childdirs, str(root)
    return {'root': str(root), 'file_count': files, 'child_directory_count': childdirs, 'entries': entries}

def validate_finite(root, snapshot, manifest_name, excluded):
    manifest = json.loads((root / manifest_name).read_text())
    current = {r['path']: r for r in snapshot['entries'] if r['path'] not in excluded}
    declared = manifest['entries']
    assert set(current) == {r['path'] for r in declared}, ('manifest topology', str(root))
    for d in declared:
        actual = current[d['path']]
        for key, value in d.items():
            if key == 'mode_octal':
                assert int(actual[key], 8) == int(value, 8), ('manifest mode', str(root), d['path'])
            elif key in actual:
                assert actual[key] == value, ('manifest field', str(root), d['path'], key)

def custody():
    snapshots = {'source': tree(S, 55, 14), 'original_writer': tree(W, 27, 1), 'independent_fact': tree(F, 14, 0)}
    specific = []
    for p, expected in specific_pins.items():
        r = row(p, str(p))
        assert r['sha256'] == expected, ('protected pin', str(p), r['sha256'])
        specific.append(r)
    validate_finite(S, snapshots['source'], 'SOURCE_MANIFEST.json', ['SOURCE_FINAL.json', 'SOURCE_MANIFEST.json'])
    validate_finite(W, snapshots['original_writer'], 'MANIFEST.json', [])
    validate_finite(F, snapshots['independent_fact'], 'FINAL_MANIFEST.json', [])
    return {'UTC': utc(), 'snapshots': snapshots, 'specific_inputs': specific, 'all_three_original_finite_manifests_match': True, 'excluded_scope': ['actual website W', 'Git/native/index/refs', 'network', 'Sheet/stage/deploy', 'other source or review packets']}

assert not (L / 'private-page').exists() and not (L / 'MODEL.json').exists()
assert not (L / 'CUSTODY_BEFORE.json').exists() and not (L / 'CUSTODY_AFTER.json').exists()
before = custody()
(L / 'CUSTODY_BEFORE.json').write_text(json.dumps(before, indent=2) + '\n')
original = (W / 'private-page/index.html').read_bytes()
assert sha(original) == 'e5a368d2f5c82e10b048c21fe9e3137e503b62fa17be962e04f71bfca60eaee4'
old_clause = b'then takes their operator-norm closure.'
new_clause = b'then takes the operator-norm closure of their complex linear span.'
old_paragraph = b'<p>A reduced group C*-algebra represents a discrete group by translation operators on square-summable functions on the group, then takes their operator-norm closure. Calling this algebra <em>simple</em> means that it has no nonzero proper closed two-sided ideals. Its canonical trace reads the coefficient of the identity element; a unique tracial state means that every normalized positive trace agrees with it.</p>'
assert original.count(old_paragraph) == 1 and original.count(old_clause) == 1
assert original.count(new_clause) == 0 and old_paragraph.count(old_clause) == 1
new_paragraph = old_paragraph.replace(old_clause, new_clause, 1)
prefix, matched, suffix = original.partition(old_paragraph)
assert matched == old_paragraph
corrected = prefix + new_paragraph + suffix
assert corrected == original.replace(old_clause, new_clause, 1)
assert corrected.replace(new_clause, old_clause, 1) == original
assert corrected.partition(new_paragraph) == (prefix, new_paragraph, suffix)
assert original.split(b'<article>', 1)[0] == corrected.split(b'<article>', 1)[0]
assert original.split(b'</article>', 1)[1] == corrected.split(b'</article>', 1)[1]
model_bytes = (W / 'MODEL.json').read_bytes()
assert sha(model_bytes) == '81e047addf166e36e766d0a12b2b286ccee852e64db9a1117d36633e8fdacd3a'
model = json.loads(model_bytes)
null_fields = ['actual_canonical', 'base_url', 'production_url', 'page_publication_date', 'AA', 'legacy_route', 'legacy_redirect', 'follow_up']
assert all(model[k] is None for k in null_fields)
assert model['private_only'] and not model['publication_authority'] and model['robots'] == 'noindex,nofollow'
assert model['native_version'] is None and not model['native_version_field_present']
assert model['host_edition_label'] == 'v1'
assert b'<meta name="robots" content="noindex,nofollow">' in corrected
assert b'rel="canonical"' not in corrected
D = L / 'private-page'
D.mkdir()
native_names = ['thompson-cstar-verification.zip', 'thompson-cstar-source.zip', 'paper.pdf']
unchanged_names = native_names + ['citation.bib', 'research.css']
assert {p.name for p in (W / 'private-page').iterdir()} == set(unchanged_names + ['index.html'])
copied = []
for name in unchanged_names:
    old = W / 'private-page' / name
    shutil.copy2(old, D / name)
    assert (D / name).read_bytes() == old.read_bytes()
    assert stat.S_IMODE((D / name).stat().st_mode) == stat.S_IMODE(old.stat().st_mode)
    if name in native_names:
        assert (D / name).read_bytes() == (S / 'zenodo-files' / name).read_bytes()
    copied.append({'name': name, 'bytes': old.stat().st_size, 'sha256': sha(old.read_bytes()), 'mode_octal': oct(stat.S_IMODE(old.stat().st_mode)), 'unchanged': True})
shutil.copy2(W / 'private-page/index.html', D / 'index.html')
(D / 'index.html').write_bytes(corrected)
shutil.copy2(W / 'MODEL.json', L / 'MODEL.json')
assert (L / 'MODEL.json').read_bytes() == model_bytes
assert json.loads((L / 'MODEL.json').read_text()) == model
assert (D / 'index.html').read_bytes() == corrected
after = custody()
assert before['snapshots'] == after['snapshots'], 'protected original tree changed'
assert before['specific_inputs'] == after['specific_inputs'], 'protected specific input changed'
after['before_after_exact'] = True
(L / 'CUSTODY_AFTER.json').write_text(json.dumps(after, indent=2) + '\n')
edit = {
    'UTC': utc(), 'reason': 'Independent factual P2: reduced-algebra definition must include complex linear span; native manuscript already correct; routine private website copy only',
    'old_clause': old_clause.decode(), 'new_clause': new_clause.decode(),
    'old_paragraph': old_paragraph.decode(), 'new_paragraph': new_paragraph.decode(),
    'old_page_bytes': len(original), 'new_page_bytes': len(corrected),
    'old_page_sha256': sha(original), 'new_page_sha256': sha(corrected),
    'paragraph_start_byte': len(prefix), 'old_paragraph_end_byte_exclusive': len(prefix) + len(old_paragraph), 'new_paragraph_end_byte_exclusive': len(prefix) + len(new_paragraph),
    'unchanged_prefix_bytes': len(prefix), 'unchanged_prefix_sha256': sha(prefix), 'unchanged_suffix_bytes': len(suffix), 'unchanged_suffix_sha256': sha(suffix),
    'whole_article_forward_exact': True, 'whole_article_reverse_exact': True, 'outside_single_literal_clause_unchanged': True,
    'HEAD_and_after_article_bytes_unchanged': True, 'abstract_SEO_native_facts_unchanged_by_exact_outside_span_equality': True,
    'model_change_allowlist': [], 'model_changed_fields': [], 'model_bytes_exact': True, 'model_sha256': sha(model_bytes),
    'unchanged_files': copied, 'native_order_preserved': native_names,
    'source55_14_original_writer27_1_fact14_0_and_specific_inputs_before_after_exact': True,
    'original_builder_reruns': 0, 'scientific_source_execution': 0, 'private_only': True, 'publication_authority': False,
    'all_publication_fields': {key: None for key in null_fields}, 'robots': 'noindex,nofollow',
    'limits': ['Copy transformer only; root must read actual corrected page and obtain an independent corrected-byte fact check', 'No website, stage, production, tracker, collision, legacy or live certificate; original scientific PASS unchanged'],
}
(L / 'COPY_CORRECTION.json').write_text(json.dumps(edit, indent=2) + '\n')
print(json.dumps({'status': 'PRIVATE_CLOSED_COPY_CORRECTED', 'new_page_bytes': len(corrected), 'new_page_sha256': sha(corrected), 'model_bytes_exact': True, 'model_sha256': sha(model_bytes), 'whole_article_forward_reverse_exact': True, 'all_protected_inputs_exact': True, 'publication_authority': False}))
