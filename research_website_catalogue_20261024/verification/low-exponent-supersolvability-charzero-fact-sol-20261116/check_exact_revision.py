"""One read-only, exact COPY-1 byte/data comparison; no reviewed-code execution."""
from pathlib import Path
from html.parser import HTMLParser
import difflib
import hashlib
import json
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O = P / 'verification/low-exponent-supersolvability-charzero-fact-sol-20261116'
F = P / 'verification/low-exponent-supersolvability-fact-sol-20261116'
B = P / 'verification/low-exponent-supersolvability-editorial-sol-20261116'
N = P / 'verification/low-exponent-supersolvability-charzero-sol-20261116'
S = P / 'papers/23331709/sources'
BEFORE = b'A relation-incidence proof that free central arrangements with nonzero exponents 1 or 2 and at most one 3 are supersolvable, with matching-work credit.'
AFTER = b'Supersolvability in characteristic zero for finite central free arrangements of distinct hyperplanes with nonzero exponents 1 or 2 and at most one 3.'

def need(test, message):
    if not test:
        raise RuntimeError(message)

def pin(path):
    mode = path.lstat().st_mode
    need(stat.S_ISREG(mode), 'Nonordinary file: ' + str(path))
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(), 'mode': oct(stat.S_IMODE(mode))}

def check(expected, actual, message):
    need(all(expected[k] == actual[k] for k in ('bytes', 'SHA256', 'mode')), message)

def scan(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'Nonordinary root')
    files, dirs = {}, {}
    for path in root.rglob('*'):
        info = path.lstat()
        rel = path.relative_to(root).as_posix()
        if stat.S_ISREG(info.st_mode): files[rel] = pin(path)
        else:
            need(stat.S_ISDIR(info.st_mode), 'Symlink/special node: ' + str(path))
            dirs[rel] = oct(stat.S_IMODE(info.st_mode))
    return files, dirs

def packet(root, count, final_bytes, final_sha, manifest_bytes, manifest_sha):
    check({'bytes': final_bytes, 'SHA256': final_sha, 'mode': '0o644'}, pin(root / 'FINAL.json'), 'Packet FINAL differs')
    check({'bytes': manifest_bytes, 'SHA256': manifest_sha, 'mode': '0o644'}, pin(root / 'OWNED_MANIFEST.json'), 'Packet manifest differs')
    manifest = json.loads((root / 'OWNED_MANIFEST.json').read_bytes())
    files, dirs = scan(root)
    need(len(files) == count and not dirs, 'Packet finite extent differs')
    need(set(files) == {x['path'] for x in manifest['files']} | {'FINAL.json', 'OWNED_MANIFEST.json'}, 'Packet names differ')
    for row in manifest['files']:
        actual = files[row['path']]
        need(int(actual['mode'], 8) == int(row['mode'], 8), 'Packet mode differs')
        if not row.get('terminal_control'):
            need(actual['bytes'] == row['bytes'] and actual['SHA256'] == row.get('SHA256', row.get('sha256')), 'Packet buffer differs')
    need(oct(stat.S_IMODE(root.stat().st_mode)) == '0o755', 'Packet root mode differs')
    return {'path': str(root), 'files': count, 'child_directories': 0,
            'FINAL': files['FINAL.json'], 'manifest': files['OWNED_MANIFEST.json'], 'all_buffers_modes_authenticated': True}

old_fact = packet(F, 20, 2762, 'fe5afdec52407323f2665f0b900414312824ae3f315f641edf64c146f452fc50', 3631, 'ba02b7188fc35bf02a249e36ad87a9561bcabb3c0f6ae893fd0d99d357a5994b')
old_writer = packet(B, 22, 10446, '6d2d89ace44b565c9a523c4beaaa375e5f66131f79c8c94b5ddf7715d746fe1b', 5521, '03f5e41139040d259036ae5646aad5248e622612aa6f79ec3aed9e2104835f85')
new_writer = packet(N, 21, 8512, '33560a5b0cb736f49511cc99738e9842ee2fd73bc34918829f04960bac8c402e', 5338, '1eb746ca09fe2c1b578a2db9807dcd9d268c759b99525fd5c549abd0050c066e')
check({'bytes': 787, 'SHA256': '83c4d58fe90312dca7a5ce43231788187f7840080388fef94534be60e94cdd58', 'mode': '0o644'}, pin(O / 'INITIAL_SEAL.json'), 'Continuation INITIAL seal changed')
check({'bytes': 618, 'SHA256': '6f33be3f5c3d7694e3f21df98c136e69aba2da5bd57bb8beeef10ef5a49f4d1f', 'mode': '0o644'}, pin(O / 'INITIAL_MANIFEST.json'), 'Continuation INITIAL manifest changed')
for row in json.loads((O / 'INITIAL_MANIFEST.json').read_bytes())['files']:
    check(row, pin(O / row['path']), 'Continuation INITIAL payload changed')
expect = json.loads((F / 'SOURCE_EXPECTATIONS.json').read_bytes())
check(expect['source_manifest'], pin(S / 'SOURCE_MANIFEST.json'), 'Source manifest changed')
check(expect['source_FINAL'], pin(S / 'SOURCE_FINAL.json'), 'Source FINAL changed')
sm = json.loads((S / 'SOURCE_MANIFEST.json').read_bytes())
sf, sd = scan(S)
se = {x['path']: {k: x[k] for k in ('bytes', 'SHA256', 'mode')} for x in sm['files']}
se.update({'SOURCE_MANIFEST.json': pin(S / 'SOURCE_MANIFEST.json'), 'SOURCE_FINAL.json': pin(S / 'SOURCE_FINAL.json')})
need(sf == se and len(sf) == 120 and len(sd) == 17, 'Whole source bytes/modes/extent differ')
need(sd == {x['path']: x['mode'] for x in sm['directories']}, 'Source directory modes/topology differ')
for key in ('root_clearance', 'root_report', 'controlling_TeX', 'root_PDF_text_read'):
    item = expect[key]
    check(item, pin(Path(item['path'])), 'Inherited source/authority input changed')
changes, diffs = {}, {}
for name, count in [('index.html', 2), ('HEAD.html', 2), ('model.json', 1)]:
    before, after = (B / name).read_bytes(), (N / name).read_bytes()
    need(before.count(BEFORE) == count, 'Old occurrence count differs')
    need(after == before.replace(BEFORE, AFTER), 'Unapproved changed byte in ' + name)
    need(after.count(AFTER) == count and AFTER not in before and BEFORE not in after, 'Revised occurrence count differs')
    changes[name] = {'approved_replacements': count, 'before': pin(B / name), 'after': pin(N / name)}
    diffs[name] = ''.join(difflib.unified_diff(before.decode().splitlines(True), after.decode().splitlines(True),
        fromfile='original/' + name, tofile='corrected/' + name, n=1))
unchanged = ['MAIN.html', 'citation.bib', 'EXPECTED_ABSTRACT.txt', 'low_exponent_supersolvability.pdf', 'low_exponent_verification.zip']
for name in unchanged:
    need((N / name).read_bytes() == (B / name).read_bytes(), 'Preserved deliverable differs')
for name in ('low_exponent_supersolvability.pdf', 'low_exponent_verification.zip'):
    need((N / name).read_bytes() == (S / 'assets' / name).read_bytes(), 'Native original differs')
before_html, after_html = (B / 'index.html').read_text(), (N / 'index.html').read_text()
need(before_html.split('<body>', 1)[1] == after_html.split('<body>', 1)[1], 'Whole body changed')
head, main = (N / 'HEAD.html').read_text().rstrip('\n'), (N / 'MAIN.html').read_text().rstrip('\n')
need(after_html.count(head) == after_html.count(main) == 1, 'Saved HEAD/MAIN index identity differs')
class Meta(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta, self.abstract, self.schema = {}, '', ''
        self.in_abstract = self.in_schema = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta': self.meta[a.get('name', a.get('property'))] = a.get('content')
        if a.get('id') == 'original-abstract': self.in_abstract = True
        if tag == 'script':
            need(a.get('type') == 'application/ld+json', 'Unexpected script')
            self.in_schema = True
    def handle_endtag(self, tag):
        if tag == 'p': self.in_abstract = False
        if tag == 'script': self.in_schema = False
    def handle_data(self, data):
        if self.in_abstract: self.abstract += data
        if self.in_schema: self.schema += data
page = Meta()
page.feed(after_html)
model = json.loads((N / 'model.json').read_bytes())
old_model = json.loads((B / 'model.json').read_bytes())
old_model['description'] = AFTER.decode()
need(model == old_model, 'Unexpected structured model change')
need(page.meta['description'] == page.meta['og:description'] == model['description'] == AFTER.decode(), 'Approved description fields mismatch')
schema = json.loads(page.schema)
need(schema == model['schema'], 'Schema/model mismatch')
def norm(text): return ' '.join(text.replace('K_4', 'K4').replace('’', "'").split())
abstract = norm((F / 'ABSTRACT_EXPECTED.txt').read_text())
need(all(norm(x) == abstract for x in (page.abstract, page.meta['DC.description'], schema['abstract'], model['abstract'])), 'Full inherited source abstract mismatch')
need(all(model[k] is None for k in ('canonical', 'base_url', 'production_url', 'AA', 'follow_up')), 'Private null boundary changed')
need(page.meta['robots'] == 'noindex, nofollow' and model['publication_authority'] is False, 'Private authority boundary changed')
need(model['native_order'] == ['low_exponent_supersolvability.pdf', 'low_exponent_verification.zip'], 'Native order changed')
producer_run = json.loads((N / 'EXECUTION.json').read_bytes())
need(producer_run['ordinary_helper_invocations'] == 1 and producer_run['exit_statuses'] == [0], 'Producer recorded history differs')
need((N / 'check.stderr.txt').read_bytes() == b'', 'Producer literal stderr differs')
print(json.dumps({'status': 'PASS_EXACT_APPROVED_COPY1_CORRECTION', 'record': 23331709, 'row': 167,
    'old_fact_packet': old_fact, 'old_writer_packet': old_writer, 'revised_writer_packet': new_writer,
    'source_all120_buffers_modes_17_dirs_unchanged': True, 'continuation_initial4_unchanged': True,
    'exact_changes': changes, 'independent_unified_diffs': diffs, 'total_replacements': 5,
    'all_other_changed_buffer_bytes_preserved': True, 'whole_body_MAIN_abstract_Bib_native_originals_preserved': True,
    'unchanged_deliverable_pins': {x: pin(N / x) for x in unchanged},
    'full_abstract_visible_DC_schema_model_matches_inherited_contract': True,
    'private_proposed_canonical_AA_followup_boundary_preserved': True,
    'recorded_producer_new_data_run': {'invocations': 1, 'exit': 0, 'stderr_bytes': 0, 'replayed_here': False},
    'old_run_histories_preserved_by_full_old_packet_hashes': True,
    'new_scientific_native_producer_helper_browser_render_network_Git_W_Sheet_or_contact_actions': False,
    'publication_authority': False}, indent=2))
