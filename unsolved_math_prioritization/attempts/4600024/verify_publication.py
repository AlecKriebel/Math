#!/usr/bin/env python3
"""Verify frozen archives, exact publication inventory, and finite source replays."""
import argparse
import hashlib
import json
import pathlib
import stat
import subprocess
import sys
import zipfile

ROOT = pathlib.Path(__file__).absolute().parent
ARCHIVES = {
    'BLOCK_CODE_EXTENSION_4600024_AUTHOR_SAFE_FREEZE.zip': ('author', 15624, '5775d3247c3a368945025a74975e6498c26ae0755e1138ccc33ff639c47257ef', 9),
    'BLOCK_CODE_EXTENSION_4600024_INDEPENDENT_AUDIT_SAFE.zip': ('audit', 32106, '35396a4ad2a774484bd35f92a782bb2a27ff6af0f670e388bb6ff8ab43331be9', 18),
    'BLOCK_CODE_EXTENSION_4600024_SECOND_ADVERSARIAL_REVIEW_SAFE.zip': ('second_review', 14586, 'e18c1044259d26fe41577db4af57a058263ba7f5521bd8fa19893fe6603e6cca', 9),
}

def need(value, message):
    if not value:
        raise ValueError(message)

def info(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def unique(pairs):
    result = {}
    for k, v in pairs:
        need(k not in result, 'duplicate JSON key: ' + k)
        result[k] = v
    return result

def read(path):
    def reject(v):
        raise ValueError('nonfinite JSON constant: ' + v)
    return json.loads(path.read_bytes(), object_pairs_hook=unique, parse_constant=reject)

def inventory(root, pin):
    need(root.is_dir() and not root.is_symlink(), 'invalid root')
    need(len(pin) == 64 and all(c in '0123456789abcdef' for c in pin), 'invalid manifest pin')
    p = root / 'PUBLICATION_MANIFEST.json'
    need(stat.S_ISREG(p.lstat().st_mode), 'nonregular manifest')
    need(info(p.read_bytes())['sha256'] == pin, 'external manifest pin mismatch')
    m = read(p)
    need(type(m) is dict and set(m) == {'schema', 'files'} and type(m['schema']) is int and m['schema'] == 1, 'manifest schema')
    files = m['files']
    need(type(files) is dict, 'file inventory type')
    expected = set(files) | {'PUBLICATION_MANIFEST.json'}
    need(all(n and not pathlib.PurePosixPath(n).is_absolute() and '..' not in pathlib.PurePosixPath(n).parts and '\\' not in n for n in expected), 'unsafe path')
    actual = set(); dirs = set()
    for q in root.rglob('*'):
        mode = q.lstat().st_mode
        n = q.relative_to(root).as_posix()
        if stat.S_ISREG(mode): actual.add(n)
        elif stat.S_ISDIR(mode): dirs.add(n)
        else: raise ValueError('nonregular member: ' + n)
    need(actual == expected, 'missing or unexpected file')
    want_dirs = {str(p) for n in expected for p in pathlib.PurePosixPath(n).parents if str(p) != '.'}
    need(dirs == want_dirs, 'unexpected directory')
    for n, v in files.items():
        need(type(v) is dict and set(v) == {'bytes', 'sha256'} and type(v['bytes']) is int and v['bytes'] >= 0, 'file metadata')
        need(info((root/n).read_bytes()) == v, 'file mismatch: ' + n)
    inv = read(root/'ARCHIVE_INVENTORY.json')
    need(set(inv) == set(ARCHIVES), 'archive inventory')
    for name, (folder, size, sha, count) in ARCHIVES.items():
        p = root/'archives'/name
        need(info(p.read_bytes()) == {'bytes': size, 'sha256': sha}, 'archive pin mismatch')
        with zipfile.ZipFile(p) as z:
            names = z.namelist()
            need(len(names) == count and len(set(names)) == count, 'archive member count')
            need(all(not pathlib.PurePosixPath(n).is_absolute() and '..' not in pathlib.PurePosixPath(n).parts and '\\' not in n and not n.endswith('/') for n in names), 'unsafe archive member')
            need(set(names) == {q.relative_to(root/folder).as_posix() for q in (root/folder).rglob('*') if q.is_file()}, 'extracted member inventory')
            members = {}
            for n in names:
                b = z.read(n)
                need(b == (root/folder/n).read_bytes(), 'extracted archive mismatch: ' + n)
                members[n] = info(b)
            need(inv[name] == {'folder': folder, 'archive': {'bytes': size, 'sha256': sha}, 'members': members}, 'archive receipt mismatch')
    for q in (root/'author').iterdir():
        need(q.read_bytes() == (root/'audit'/'author'/q.name).read_bytes(), 'audit author differs')
    verdict = read(root/'VERDICT.json')
    need(verdict['status'] == 'claimed_solved' and verdict['turns'] == '3/5' and verdict['effective_gate'] == 'ACCEPT_COMPLETE_EFFECTIVE_PRESCRIBED_MAP_CRITERION', 'acceptance scope')
    need(read(root/'author/STATUS.json')['independent_audit'] == 'pending', 'historical author status changed')
    for path in ['audit/AUDIT_METADATA.json', 'second_review/METADATA.json']:
        v = read(root/path)
        need(v['disposition'] == 'PASS_complete_effective_prescribed_map_criterion' and v['mathematical_corrections_required'] is False, 'audit disposition')
    for key in ['novelty_claimed', 'human_peer_review_claimed', 'formal_verification_claimed', 'practical_efficiency_claimed', 'general_solver_implemented', 'existential_over_map_decided', 'arbitrary_CA_stability_decided']:
        need(verdict[key] is False, 'unsupported assertion: '+key)
    return len(expected)

def run(root, script, optimized):
    flags = ['-I', '-B'] + (['-O'] if optimized else [])
    p = subprocess.run([sys.executable, *flags, str(root/script)], cwd='/', capture_output=True)
    need(p.returncode == 0, script + ': ' + p.stderr.decode(errors='replace'))
    return json.loads(p.stdout, object_pairs_hook=unique)

def corpus_replay(folder):
    pins = {
        'catalog.json': (21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
        'problems.json': (68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
        'research_results.json': (80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
    }
    data = {}; result = {}
    for n, (size, sha) in pins.items():
        p=folder/n; need(stat.S_ISREG(p.lstat().st_mode), 'nonregular corpus')
        b=p.read_bytes(); got=info(b); need(got == {'bytes': size, 'sha256': sha}, 'corpus pin: '+n)
        data[n]=json.loads(b); result[n]=got
    cat=[x for x in data['catalog.json'] if str(x['id'])=='4600024']
    records=[x for x in data['problems.json'] if str(x['id'])=='4600024']
    need(len(cat)==len(records)==1, 'corpus selection')
    c=cat[0]; r=records[0]
    need(c['rank']==820 and r['problem_number']=='AMR-045-0024', 'corpus identity')
    report=data['research_results.json'].get(r['problem_number'], {})
    review=json.dumps([r,report], sort_keys=True).encode()
    expected={'bytes':3101,'sha256':'a50d6c9c7ea7988bd585aca775e161bc43bd8301b87180eef35ca0732e6060c0'}
    need(info(review)==expected, 'complete record/report hash')
    statement=hashlib.sha256(r['statement'].encode()).hexdigest()
    need(statement=='8a98a6c00fc4bbfffdf9d8c9d98e58e5560cbe5dd27e18510219e35c9696d083', 'statement hash')
    return {'status':'PASS','full_corpora':result,'complete_record_and_report':expected,'statement_sha256':statement,'problem_id':4600024,'rank':820}

def verify(root, pin, inventory_only=False, source_dir=None):
    count=inventory(root,pin)
    if inventory_only: return {'status':'PASS_INVENTORY','files':count}
    replays=[]
    for opt in (False,True):
        a=run(root,'author/verify_release.py',opt)
        b=run(root,'audit/verify_audit.py',opt)
        c=run(root,'second_review/verify_review.py',opt)
        need(a['status']=='PASS' and a['mathematical_checks']==3456, 'author replay')
        need(b['status']=='PASS' and b['independent_checks']==221468 and b['integrity_controls']==32, 'audit replay')
        need(c['status']=='PASS' and c['finite_checks']==22859 and c['inventory_controls']==24, 'second replay')
        for script, expected in [('author/verify_math.py','author/MATH_RESULTS.json'),('audit/independent_checks.py','audit/INDEPENDENT_RESULTS.json'),('second_review/checks.py','second_review/RESULTS.json')]:
            need(run(root,script,opt)==read(root/expected), 'direct source mismatch: '+script)
        replays.append({'mode':'optimized' if opt else 'ordinary','author_finite_checks':3456,'first_auditor_finite_checks':221468,'second_reviewer_finite_checks':22859,'first_integrity_controls':32,'second_inventory_controls':24})
    return {'status':'PASS','effective_gate':'ACCEPT_COMPLETE_EFFECTIVE_PRESCRIBED_MAP_CRITERION','files_verified':count,'archive_member_counts':[9,18,9],'replays':replays,'full_corpus_replay':corpus_replay(source_dir) if source_dir else 'NOT_RUN_OPTIONAL_EXTERNAL_INPUTS','source_PDFs_replayed':False,'universal_theorem_formally_verified':False}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('root',nargs='?',type=pathlib.Path,default=ROOT)
    p.add_argument('--manifest-sha256',required=True)
    p.add_argument('--inventory-only',action='store_true')
    p.add_argument('--source-dir',type=pathlib.Path)
    a=p.parse_args()
    try: result=verify(a.root.absolute(),a.manifest_sha256,a.inventory_only,a.source_dir)
    except Exception as e:
        print('FAIL: '+str(e),file=sys.stderr);return 1
    print(json.dumps(result,indent=2,sort_keys=True));return 0

if __name__=='__main__':sys.exit(main())
