#!/usr/bin/env python3
"""Authenticate wrapper bytes externally before execution; separately pin the manifest.
Identity and diagnostic replay only, not formal proof verification.
"""
import argparse, ast, difflib, hashlib, json, os, re, shutil, stat, subprocess, sys, tempfile
from pathlib import Path, PurePosixPath
FROZEN = {'public': '1cd8291f2025524b351c5cc3cb5780b35ba5fa4c4afde78c6e288daddd350e9f', 'audit_a': 'bb658595d01a6298a17177304fb04d813c0027ebf414c8757016b2cfed69fbb5', 'audit_b': '0669647dcc2f4be7e501dec657868fee7ca9bac35d419123216edc18e85faffc'}
EXPECTED_ACCEPTANCE = {'schema': 'dihedral-comparison-acceptance-v1', 'date_utc': '2026-10-08', 'problem_id': 30003471, 'problem_number': 'OWR-15427-013', 'rank': 999, 'status': 'claimed_solved', 'turns': '1/5', 'mathematical_argument_accepted': True, 'full_independent_audits': 2, 'proof_unchanged': True, 'required_mathematical_corrections': [], 'dimension': 3, 'nonsimple_vertices_included': True, 'fixed_face_lattice_correspondence': True, 'conclusion': 'weak_corresponding_dihedral_dominance_implies_full_facet_normal_gram_equality', 'original_one_edge_weak_comparison_implied': True, 'support_number_or_edge_length_rigidity_claimed': False, 'brendle_smooth_domain_dependency': 'arXiv:2301.05087v4 Section 2 Propositions 2.9, 2.14, 2.15', 'bi_strategy_credited': True, 'uses_wxy_singular_index': False, 'formal_verification': False, 'human_peer_review': False, 'journal_acceptance': False, 'novelty_claim': False, 'exhaustive_literature_search': False, 'source_files_redistributed': False, 'numeric_controls_are_proof': False, 'proof_sha256': '6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415', 'frozen_manifest_anchors': {'public': '1cd8291f2025524b351c5cc3cb5780b35ba5fa4c4afde78c6e288daddd350e9f', 'audit_a': 'bb658595d01a6298a17177304fb04d813c0027ebf414c8757016b2cfed69fbb5', 'audit_b': '0669647dcc2f4be7e501dec657868fee7ca9bac35d419123216edc18e85faffc'}}
TOP = {'README.md','PUBLICATION_ACCEPTANCE.md','RESEARCH_LOG.md','ACCEPTANCE.json',
       'VERIFY_PUBLICATION.py','TEST_MUTATIONS.py','MUTATION_RESULTS.json',
       'PORTABLE_INDEPENDENT.py','PORTABLE_CONTROLS.patch','PUBLICATION_MANIFEST.json'}
HEX = re.compile(r'[0-9a-f]{64}')

def need(value, message):
    if not value: raise RuntimeError(message)


def sha(data): return hashlib.sha256(data).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def load_json(raw):
    def bad(value): raise ValueError('Nonfinite JSON: ' + value)
    return json.loads(raw, object_pairs_hook=unique, parse_constant=bad)


def regular(path):
    need(stat.S_ISREG(path.lstat().st_mode), 'Nonregular file: ' + str(path))
    return path.read_bytes()


def inventory(root, manifest_name, entries, profile, flat=False):
    need(type(entries) is list and bool(entries), 'Invalid inventory')
    names, directories = {manifest_name}, set()
    for item in entries:
        need(type(item) is dict and set(item) == {'path','bytes','sha256','mode'}, 'Invalid member schema')
        name = item['path']
        need(type(name) is str and name and '\\' not in name, 'Unsafe path')
        parts = name.split('/')
        need(all(re.fullmatch(r'[A-Za-z0-9_.-]+', p) and p not in ('.','..') for p in parts), 'Unsafe path')
        need(PurePosixPath(name).suffix in {'.md','.json','.py','.patch'}, 'Invalid member extension')
        need(not flat or len(parts) == 1, 'Nonflat frozen slice')
        need(name not in names, 'Duplicate inventory path'); names.add(name)
        for parent in PurePosixPath(name).parents:
            if str(parent) != '.': directories.add(str(parent))
        need(type(item['bytes']) is int and item['bytes'] >= 0, 'Invalid byte count')
        need(type(item['sha256']) is str and HEX.fullmatch(item['sha256']) is not None, 'Invalid digest')
        need(type(item['mode']) is str and item['mode'] == '0644', 'Baseline file mode must be 0644')
    actual_files, actual_dirs = set(), set()
    expected_file_mode, expected_dir_mode = (0o644,0o755) if profile == 'baseline' else (0o444,0o555)
    need(stat.S_IMODE(root.lstat().st_mode) == expected_dir_mode, 'Root mode mismatch')
    for directory, subdirs, files in os.walk(root, followlinks=False):
        for name in subdirs + files:
            path = Path(directory)/name; mode = path.lstat().st_mode
            relative = path.relative_to(root).as_posix()
            need(not stat.S_ISLNK(mode), 'Symlink forbidden: ' + relative)
            if stat.S_ISDIR(mode):
                need(stat.S_IMODE(mode) == expected_dir_mode, 'Directory mode mismatch: ' + relative)
                actual_dirs.add(relative)
            else:
                need(stat.S_ISREG(mode), 'Special file forbidden: ' + relative)
                need(stat.S_IMODE(mode) == expected_file_mode, 'File mode mismatch: ' + relative)
                actual_files.add(relative)
    need(actual_files == names and actual_dirs == directories, 'Exact files/directories inventory mismatch')
    for item in entries:
        raw = regular(root/item['path'])
        need(len(raw) == item['bytes'] and sha(raw) == item['sha256'], 'Payload mismatch: ' + item['path'])
    return len(entries)



def typed_equal(a,b):
    if type(a) is not type(b): return False
    if isinstance(a,dict): return a.keys()==b.keys() and all(typed_equal(a[k],b[k]) for k in a)
    if isinstance(a,list): return len(a)==len(b) and all(typed_equal(x,y) for x,y in zip(a,b))
    return a==b


def verify(root,expected,profile='baseline'):
    need(type(expected) is str and HEX.fullmatch(expected) is not None,'Invalid external anchor')
    need(stat.S_ISDIR(root.lstat().st_mode),'Packet root must be a real directory')
    raw=regular(root/'PUBLICATION_MANIFEST.json')
    need(sha(raw)==expected,'Publication manifest anchor mismatch')
    m=load_json(raw)
    need(type(m) is dict and set(m)=={'schema','problem_id','rank','status','turns','source_files_redistributed','frozen_manifest_anchors','baseline_file_mode','files'},'Invalid publication schema')
    need(type(m['schema']) is str and m['schema']=='dihedral-comparison-publication-v1','Wrong schema')
    need(type(m['problem_id']) is int and m['problem_id']==30003471 and type(m['rank']) is int and m['rank']==999,'Wrong target')
    need(type(m['status']) is str and m['status']=='claimed_solved' and type(m['turns']) is str and m['turns']=='1/5','Wrong disposition')
    need(m['source_files_redistributed'] is False and type(m['baseline_file_mode']) is str and m['baseline_file_mode']=='0644','Wrong scope/mode')
    need(typed_equal(m['frozen_manifest_anchors'],FROZEN),'Wrong frozen anchors')
    need({p.name for p in root.iterdir()}==TOP|set(FROZEN),'Top-level inventory mismatch')
    count=inventory(root,'PUBLICATION_MANIFEST.json',m['files'],profile)
    for name,pin in FROZEN.items():
        filename='MANIFEST.json' if name=='public' else 'AUDIT_MANIFEST.json'
        raw=regular(root/name/filename);need(sha(raw)==pin,'Frozen anchor mismatch: '+name)
        inner=load_json(raw);need(type(inner) is dict,'Invalid inner schema')
        if name in ('public','audit_a'):
            fields={'schema','files'}|({'author_packet_manifest_sha256'} if name=='audit_a' else set())
            need(set(inner)==fields and type(inner['schema']) is int and inner['schema']==1,'Invalid inner version')
            if name=='audit_a':need(inner['author_packet_manifest_sha256']==FROZEN['public'],'Audit A target mismatch')
            need(type(inner['files']) is dict and len(inner['files'])==(9 if name=='public' else 3),'Invalid inner inventory')
            items=[]
            for path,record in inner['files'].items():
                need(type(record) is dict and set(record)=={'bytes','sha256'},'Invalid frozen record')
                items.append({'path':path,**record,'mode':'0644'})
        else:
            need(set(inner)=={'blocking_gaps','date','files','formal_verification','independent_control_checks','manifest_sha256','proof_sha256','required_corrections','source_pdfs_included','target_id','verdict'},'Invalid audit B schema')
            need(inner['formal_verification'] is False and inner['source_pdfs_included'] is False,'Audit B scope')
            need(type(inner['target_id']) is int and inner['target_id']==30003471,'Audit B target')
            need(inner['manifest_sha256']==FROZEN['public'] and inner['proof_sha256']==EXPECTED_ACCEPTANCE['proof_sha256'],'Audit B binding')
            need(typed_equal(inner['blocking_gaps'],[]) and typed_equal(inner['required_corrections'],[]),'Audit B gaps')
            need(inner['verdict']=='accept_frozen_mathematical_argument','Audit B verdict')
            need(type(inner['independent_control_checks']) is int and inner['independent_control_checks']==4146,'Audit B count')
            need(type(inner['files']) is list and len(inner['files'])==4,'Audit B inventory')
            items=[]
            for record in inner['files']:
                need(type(record) is dict and set(record)=={'path','bytes','sha256'},'Audit B member')
                items.append({**record,'mode':'0644'})
        inventory(root/name,filename,items,profile,flat=True)
    for path in root.rglob('*.json'): load_json(regular(path))
    for path in root.rglob('*.py'):
        need(not any(isinstance(node,ast.Assert) for node in ast.walk(ast.parse(regular(path)))),'Optimization-removable check: '+path.name)
    need(typed_equal(load_json(regular(root/'ACCEPTANCE.json')),EXPECTED_ACCEPTANCE),'Acceptance scope/type mismatch')
    a=load_json(regular(root/'audit_a/AUDIT_STATUS.json'))
    need(a['mathematical_acceptance'] is True and typed_equal(a['required_corrections'],[]) and a['proof_edited'] is False,'Audit A verdict')
    original=regular(root/'audit_b/independent_controls.py').decode()
    portable=regular(root/'PORTABLE_INDEPENDENT.py').decode()
    patch=''.join(difflib.unified_diff(original.splitlines(keepends=True),portable.splitlines(keepends=True),fromfile='audit_b/independent_controls.py',tofile='PORTABLE_INDEPENDENT.py'))
    need(regular(root/'PORTABLE_CONTROLS.patch').decode()==patch,'Portable adapter diff mismatch')
    return count

def snapshot(root):
    return {p.relative_to(root).as_posix():(stat.S_IMODE(p.lstat().st_mode),sha(regular(p)) if p.is_file() else None) for p in [root,*root.rglob('*')]}


def stage(source,destination):
    shutil.copytree(source,destination)
    destination.chmod(0o755)
    for p in destination.rglob('*'): p.chmod(0o755 if p.is_dir() else 0o644)


def readonly_stage(source,destination):
    stage(source,destination)
    for p in destination.rglob('*'): p.chmod(0o555 if p.is_dir() else 0o444)
    destination.chmod(0o555)


def writable(root):
    root.chmod(0o755)
    for p in root.rglob('*'): p.chmod(0o755 if p.is_dir() else 0o644)



def replay(root,selected,sources=None):
    before=snapshot(root);receipts=[]
    env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
    env['PYTHONDONTWRITEBYTECODE']='1'
    source_state='NOT_RUN_NO_SEPARATELY_SUPPLIED_SOURCES' if sources is None else 'PASS_NINE_EXTERNAL_SOURCE_PINS'
    expected_author=load_json(regular(root/'audit_a/CONTROL_REPLAY.json'))['runs'][0]['result']
    historical=load_json(regular(root/'audit_b/INDEPENDENT_CONTROL_RESULTS.json'))
    expected_independent=json.loads(json.dumps(historical))
    if sources is None:
        need(expected_independent['counts'].pop('source_pin')==9,'Historical source count')
        expected_independent['total_checks']-=9
    expected_independent['source_verification']=source_state
    for label,flags in [('normal',[]),('-O',['-O']),('-OO',['-OO'])]:
        if selected!='all' and label!=selected:continue
        with tempfile.TemporaryDirectory(prefix='dihedral-publication-') as temporary:
            work=Path(temporary);packet=work/'readonly-packet'
            readonly_stage(root,packet);ro_before=snapshot(packet)
            blocked=[]
            for path in [packet/'probe',packet/'public/PROOF.md']:
                try:
                    with path.open('ab'):pass
                except PermissionError:blocked.append(True)
                else:blocked.append(False)
            need(blocked==[True,True],'Read-only probes unexpectedly writable')
            def invoke(script,args=()):
                cp=subprocess.run([sys.executable,'-I','-B',*flags,str(script),*map(str,args)],cwd=work,env=env,capture_output=True,timeout=300)
                need(cp.returncode==0,'Replay failed: '+script.name+': '+cp.stdout.decode(errors='replace')[-1000:]+cp.stderr.decode(errors='replace')[-1000:])
                return load_json(cp.stdout),cp.stdout
            try:
                # The frozen author's self-test mutates temporary copies. Its
                # input is a writable disposable stage, checked for no changes.
                harness=work/'author';stage(root/'public',harness);h_before=snapshot(harness)
                obj,out=invoke(harness/'verify_packet.py',['--manifest-sha256',FROZEN['public'],'--self-test'])
                need(typed_equal(obj,expected_author),'Author controls differ from audit A receipt')
                need(snapshot(harness)==h_before,'Author controls changed their input')
                receipts.append({'mode':label,'suite':'author_and_audit_a_replay','finite_controls':5066,'negative_controls_rejected':19,'stdout_sha256':sha(out)})
                obj,out=invoke(packet/'public/verify_packet.py',['--manifest-sha256',FROZEN['public']])
                baseline={k:v for k,v in expected_author.items() if k!='self_test'}
                need(typed_equal(obj,baseline),'Read-only author replay differs')
                args=['--packet-root',packet]
                if sources is not None:args+=['--source-root',sources]
                obj,out=invoke(packet/'PORTABLE_INDEPENDENT.py',args)
                need(typed_equal(obj,expected_independent),'Independent replay differs beyond disclosed source selection')
                receipts.append({'mode':label,'suite':'independent_audit_b_portable','checks':obj['total_checks'],'source_verification':source_state,'source_hash_checks':obj['counts'].get('source_pin',0),'stdout_sha256':sha(out)})
                need(snapshot(packet)==ro_before,'Read-only replay changed packet')
                receipts.append({'mode':label,'profile':'readonly_0444_0555','write_probes_rejected':2,'unchanged':True})
            finally:writable(packet)
    need(snapshot(root)==before,'Publication packet changed during replay')
    return receipts


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet',type=Path,default=Path(__file__).absolute().parent)
    p.add_argument('--expected-manifest',required=True)
    p.add_argument('--filesystem-profile',choices=['baseline','readonly'],default='baseline')
    p.add_argument('--check-only',action='store_true')
    p.add_argument('--source-root',type=Path,help='Optional separately supplied source PDFs, never included')
    p.add_argument('--mode',choices=['all','normal','-O','-OO'],default='all')
    args=p.parse_args();root=args.packet.absolute()
    try:
        count=verify(root,args.expected_manifest,args.filesystem_profile)
        results=[] if args.check_only else replay(root,args.mode,args.source_root.absolute() if args.source_root is not None else None)
        verify(root,args.expected_manifest,args.filesystem_profile)
        print(json.dumps({'status':'PASS','problem_id':30003471,'publication_manifest_sha256':args.expected_manifest,'bound_files':count,'filesystem_profile':args.filesystem_profile,'check_only':args.check_only,'source_verification':'NOT_RUN_CHECK_ONLY' if args.check_only else ('NOT_RUN_NO_SEPARATELY_SUPPLIED_SOURCES' if args.source_root is None else 'PASS_NINE_EXTERNAL_SOURCE_PINS'),'replays':results,'limits':'Integrity and finite diagnostics; not formal proof, human peer review, journal acceptance, novelty, or global openness certification.'},indent=2,sort_keys=True))
    except (RuntimeError,ValueError,TypeError,KeyError,OSError,SyntaxError,subprocess.SubprocessError) as error:
        print('REJECT: '+str(error),file=sys.stderr);return 1
    return 0

if __name__=='__main__':sys.exit(main())
