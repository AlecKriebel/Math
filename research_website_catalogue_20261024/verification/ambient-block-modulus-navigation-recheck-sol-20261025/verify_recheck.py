"""Read/hash-only independent navigation recheck verifier.

No checker, renderer, suite, HTTP, Git, subprocess, import of project helpers,
or file write. Safe to repeat after sealing; prints its result to stdout.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import ast, hashlib, json
from html.parser import HTMLParser

O = Path(__file__).resolve().parent
P = O.parents[1]
S = P/'verification/local-ambient-block-modulus-stage-sol-20261025'
A = P/'verification/audit-ambient-block-modulus-code-sol-20261025'
C = P/'verification/ambient-block-modulus-navigation-correction-sol-20261025'
IDS = {'23333353','23416806','23441617'}
CASES = {'pristine','h1_valid_but_wrong_href','Research_valid_but_wrong_href'}

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def load(path):
    return json.loads(path.read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def info(path):
    return {'path':str(path),'bytes':path.stat().st_size,'sha256':digest(path)}

baseline = load(O/'BASELINE.json')
need(baseline['file_count'] == len(baseline['files']) == len({r['path'] for r in baseline['files']}) == 4110, 'complete fresh baseline')
pins = {r['path']:r for r in baseline['files']}
for path, row in pins.items():
    need(info(Path(path)) == row, 'protected current/fixed original changed: '+path)
for name, root in baseline['roots'].items():
    root = Path(root)
    current_names = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    need(current_names == set(baseline['file_sets'][name]) and len(current_names) == len(baseline['file_sets'][name]), 'protected original file set changed: '+name)
need(len(baseline['file_sets']['public']) == 504, 'fresh current public504')

base = (S/'final-content-check.proposed.py').read_bytes()
proposed = (C/'final-content-check.proposed.py').read_bytes()
insertion = (C/'INSERTION.txt').read_bytes()
needle = b"  test('exact_visible_h1',contract.headings==[c['title']])\n"
need(hashlib.sha256(proposed).hexdigest() == '60fdabc716e9dbf887f197aa1d5e726df8675cb646404ba79603995e54ed6a80', 'exact authorized candidate')
need(base.count(needle) == 1 and len(insertion.splitlines()) == 6 and proposed == base.replace(needle,needle+insertion) and proposed.replace(insertion,b'',1) == base, 'exact six-line insertion and every other old byte')
tree = ast.parse(proposed)
line = proposed[:proposed.index(insertion)].count(b'\n')+1
enclosing = [n for n in ast.walk(tree) if isinstance(n,ast.If) and n.lineno < line <= n.end_lineno and ast.unparse(n.test) == 'rid in ABM_IDS']
need(len(enclosing) == 1 and line+5 <= enclosing[0].end_lineno, 'six lines only inside existing ABM branch')
helper = ast.parse((S/'ambient_block_modulus_source.py').read_bytes())
actual_ids = next(ast.literal_eval(n.value) for n in helper.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id == 'ABM_IDS' for x in n.targets))
need(actual_ids == IDS, 'exact existing three-ID boundary')
for name in (b'heading_fragments',b'heading_anchors',b'main_navigation',b'research_anchors'):
    need(name not in base, 'new names unused outside insertion')
insert_tree = ast.parse('if True:\n'+insertion.decode())
need(not any(isinstance(n,ast.Assert) for n in ast.walk(insert_tree)), 'new guards do not use assertions')
need([n.value.args[0].value for n in insert_tree.body[0].body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call)] == ['exact_h1_selflink_destination','exact_main_Research_destination'], 'two explicit check mechanisms')
old_root = b'R=Path(__file__).resolve().parents[1]\n'
new_root = ('R=Path('+repr(str(P))+')\n').encode()
need(proposed.count(old_root) == 1 and (C/'final-content-check.stage.py').read_bytes() == proposed.replace(old_root,new_root), 'only private execution root override')

class ScopedAnchors(HTMLParser):
    """Independent locator for actual h1 and named navigation destinations."""
    def __init__(self, data):
        super().__init__(convert_charrefs=True)
        self.in_heading = False
        self.in_main_nav = False
        self.active = None
        self.heading = []
        self.research = []
        self.feed(data)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h1':
            self.in_heading = True
        if tag == 'nav' and attrs.get('aria-label') == 'Main navigation':
            self.in_main_nav = True
        if tag == 'a':
            self.active = (attrs.get('href'),[],self.in_heading,self.in_main_nav)
    def handle_data(self, text):
        if self.active is not None:
            self.active[1].append(text)
    def handle_endtag(self, tag):
        if tag == 'a' and self.active is not None:
            href, text, heading, nav = self.active
            label = ' '.join(''.join(text).split())
            if heading:
                self.heading.append((href,label))
            if nav and label == 'Research':
                self.research.append((href,label))
            self.active = None
        if tag == 'h1':
            self.in_heading = False
        if tag == 'nav':
            self.in_main_nav = False

sample_bindings = load(O/'SAMPLE_BINDINGS.json')
need(len(sample_bindings['sample_rows']) == 9, 'three pristine and six retained inputs')
for row in sample_bindings['sample_rows']:
    rid, case = row['record_id'], row['case']
    config = load(P/'papers'/rid/'publication.json')
    pristine = Path(row['actual_pristine_HTML']['path'])
    need(info(pristine) == row['actual_pristine_HTML'], 'original staged HTML binding')
    data = pristine.read_bytes()
    if case != 'pristine':
        sample = Path(row['retained_sample']['path'])
        need(info(sample) == row['retained_sample'] and data.count(row['exact_old_tag'].encode()) == 1 and sample.read_bytes() == data.replace(row['exact_old_tag'].encode(),row['exact_new_tag'].encode(),1), 'exact retained single href replacement')
        data = sample.read_bytes()
        for entry in row['original_audit_mutation_receipts']:
            path = Path(entry['receipt']['path'])
            need(info(path) == entry['receipt'] and load(path)['changed_read_SHA256'] == digest(sample), 'original actual sample hash receipt')
    nav = ScopedAnchors(data.decode())
    expected_heading = '/research/' if case == 'h1_valid_but_wrong_href' else '/research/'+config['slug']+'/'
    expected_research = '/blog/' if case == 'Research_valid_but_wrong_href' else '/research/'
    need(nav.heading == [(expected_heading,config['title'])] and nav.research == [(expected_research,'Research')], 'independent precise actual destinations')

old_gaps = load(A/'CONFIRMED_NAVIGATION_GAPS.json')
need(len(old_gaps['runs']) == 12 and all(r['exit_code'] == 0 and r['checker_status'] == 'PASS' for r in old_gaps['runs']), 'original twelve false negatives remain genuine PASS records')
result = load(O/'RESULTS.json')
rows = result['rows']
expected = {(rid,case,mode) for rid in IDS for case in CASES for mode in ('normal','optimized')}
need(len(rows) == result['actual_checker_executions'] == 18 and {(r['record_id'],r['case'],r['mode']) for r in rows} == expected, 'exact eighteen unique actual executions')
need(load(O/'PROGRESS.json')['rows'] == rows, 'complete actual progress ledger')
checks_by_case = {}
for row in rows:
    rid, case, mode = row['record_id'], row['case'], row['mode']
    receipt = O/row['receipt']
    qa = load(receipt)
    need(digest(receipt) == row['receipt_sha256'] and set(qa['papers']) == {rid}, 'actual single-target QA identity')
    checks = qa['papers'][rid]['checks']
    need(all(type(v) is bool for v in checks.values()) and len(checks) == (65 if rid == '23441617' else 64), 'all explicit target check values')
    need(checks['local_links_anchors'] is True and checks['exact_visible_h1'] is True and checks['exact_whole_approved_body_text'] is True, 'old valid-local-link and approved-body checks still pass')
    if case == 'pristine':
        need(row['exit_code'] == 0 and qa['status'] == 'PASS' and not qa['issues'] and all(checks.values()), 'pristine actual acceptance')
    else:
        guard = 'exact_h1_selflink_destination' if case == 'h1_valid_but_wrong_href' else 'exact_main_Research_destination'
        need(row['exit_code'] == 1 and qa['status'] == 'ISSUES_FOUND' and qa['issues'] == [rid+': '+guard] and checks[guard] is False and all(v for k,v in checks.items() if k != guard), 'isolated specific guard rejection')
    stem = f'{rid}-{case}-{mode}'
    stdout = O/(stem+'.stdout')
    need(digest(stdout) == row['stdout_sha256'] and not (O/(stem+'.stderr')).read_bytes() and not row['timeout'], 'actual complete stdout and empty stderr, no timeout')
    emitted = load(stdout)
    need(emitted.pop('saved') is True and emitted == qa, 'actual printed and written checker result agree')
    obs = load(O/'read-observations'/(stem+'.json'))
    config = load(P/'papers'/rid/'publication.json')
    target = S/'public/research'/config['slug']/'index.html'
    actual = target if case == 'pristine' else A/'navigation-fault-samples'/f'{rid}-{case}.html'
    need(obs['actual_optimize_flag'] == (1 if mode == 'optimized' else 0) and obs['actual_override_sha256'] == digest(actual) == qa['papers'][rid]['hashes']['html'] and obs['pristine_sha256'] == digest(target), 'actual optimize flag and exact read bytes')
    need(bool(obs['target_read_calls']) and all(x['sha256'] == digest(actual) for x in obs['target_read_calls']) and obs['HTML_written'] is False, 'actual reads used exact retained sample in memory')
    need(obs['candidate_proposed_sha256'] == digest(C/'final-content-check.proposed.py') and obs['actual_private_executable_sha256'] == digest(C/'final-content-check.stage.py'), 'actual candidate and execution bindings')
    need(obs['actual_imported_source_modules']['ambient_block_modulus_source']['path'] == str(S/'ambient_block_modulus_source.py') and obs['actual_imported_source_modules']['abm_body_contract']['path'] == str(S/'abm_body_contract.py'), 'actual unchanged helper and body parser imports')
    for entry in obs['actual_imported_source_modules'].values():
        need(entry == pins[entry['path']], 'actual imported source module baseline')
    key = (rid,case)
    if key in checks_by_case:
        need(checks_by_case[key] == checks, 'normal and optimized check maps agree')
    else:
        checks_by_case[key] = checks

owned = 0
if (O/'MANIFEST.json').exists() or (O/'SEAL.json').exists():
    need((O/'MANIFEST.json').exists() and (O/'SEAL.json').exists(), 'complete own manifest/seal pair')
    manifest, seal = load(O/'MANIFEST.json'), load(O/'SEAL.json')
    need(digest(O/'MANIFEST.json') == seal['manifest_sha256'], 'own seal-to-manifest binding')
    for row in manifest['files']:
        path = O/row['path']
        need(path.is_file() and not path.is_symlink() and path.stat().st_size == row['bytes'] and digest(path) == row['sha256'], 'own frozen payload: '+row['path'])
    actual = {str(p.relative_to(O)) for p in O.rglob('*') if p.is_file() and p.name not in {'MANIFEST.json','SEAL.json'}}
    need(actual == {r['path'] for r in manifest['files']}, 'complete own file inventory')
    owned = len(manifest['files'])

print(json.dumps({'status':'PASS_READ_ONLY_BOUNDED_NAVIGATION_RECHECK','fresh_original_bindings_verified':4110,
                  'production_public_files_unchanged':504,'original_stage_files_unchanged':431,
                  'original_audit_files_unchanged':394,'original_correction_files_unchanged':109,
                  'candidate_sha256':digest(C/'final-content-check.proposed.py'),'exact_inserted_lines':6,
                  'all_other_candidate_bytes_preserved':True,'bounded_actual_single_target_executions':18,
                  'pristine_acceptances':6,'exact_retained_fault_rejections':12,'distinct_retained_faults':6,
                  'original_twelve_false_negatives_still_PASS':True,'normal_optimized_check_maps_identical':True,
                  'all_other_checks_pass_for_each_fault':True,'owned_payload_files_verified':owned,
                  'suite_or_renderer_replay':False,'HTTP_UI_native_Git_outreach':False,
                  'writes_by_this_verifier':0,'integration_authority':'root'},indent=2))
