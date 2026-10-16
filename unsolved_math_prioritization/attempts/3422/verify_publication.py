#!/usr/bin/env python3
"""Authenticate frozen the known Sticky Cantor classification; replay source-free finite checks."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile

ACCEPTED = {'PUBLIC_SCOPE.json': {'bytes': 1378, 'sha256': 'be187888f4726cc5682fe04cf9b4fb20dc6b98d0e2bc9c9b2d4423ec6efc682e'}, 'REPLAY_RESULTS.json': {'bytes': 96291, 'sha256': '6cc9576c47f28e8524201eaa942d713a9655bd18d83a7ed3f252243daaa1d3b9'}, 'audit/ACCEPTANCE.json': {'bytes': 1721, 'sha256': 'a601d184c4bb2710b95f7449706879962b807cb062fe0c04a5f3b737958535c2'}, 'audit/ACCEPTANCE_AUDIT.md': {'bytes': 16625, 'sha256': 'a6e6be137158ad87b748ce5d6dd38e0eb8a468825a35da443efc859fa8c57333'}, 'audit/AUDIT_MANIFEST.json': {'bytes': 1636, 'sha256': '277af0f4e696e51f3db1da2234536ff5daa81fdeed25a034d4679ed2a9ad8b53'}, 'audit/INDEPENDENT_INTEGRITY.json': {'bytes': 7319, 'sha256': '235881de647ef42b11712b675bcfbc3614e1f847779007f1b3fa6c7ad5c4b79d'}, 'audit/INDEPENDENT_RUNS.json': {'bytes': 19411, 'sha256': 'a3b3cab3c5aa7846f564b4fc1ebb49a2c3ddda65f1d82eaebb9f5adf0859a776'}, 'audit/INDEPENDENT_RUNS_DRIVER_OO.json': {'bytes': 19411, 'sha256': '1d6ccadf707e403189045b98386cfd7c3aba1612af1ca14b4c429c4cf9018c9a'}, 'audit/README.md': {'bytes': 1721, 'sha256': '515e345b9183483373d548efd7da8e042a3fbfd18cc68f15f5a0a14f8b86ba52'}, 'audit/check_independent.py': {'bytes': 9003, 'sha256': '82dc4b88e1ce9ffafc78b7098297343c38eb82df54761777fd636853125e72ca'}, 'author/CORRECTIONS.md': {'bytes': 630, 'sha256': '7021ce96d9d47efae6e39c3f9dbe3ba587e22884cf62b18b837eb712c52052e4'}, 'author/CORRECTIONS.patch': {'bytes': 1957, 'sha256': 'cb882d7628b69b4f3a39d3460390ff4d86c2ff035cb4c63fd82a4b60ceeef624'}, 'author/PAYLOAD_PINS.json': {'bytes': 1376, 'sha256': '244c8d061af5377a4543392c3a034740198bc6d179620bc0e0bf8e3b147e8237'}, 'author/README.md': {'bytes': 1507, 'sha256': '4d8e777afbeddaf77eaad80eb65983a61e6dc212c18a165c89bf4e3c08cdc732'}, 'author/REPORT.md': {'bytes': 19147, 'sha256': '610fd9185a77647635e6bf3dc1154e980f9400348335a084a9793f0c9ed0a676'}, 'author/SOURCE_AUDIT.md': {'bytes': 5283, 'sha256': 'c9cd736961b3122da55eba5f551d397eedbec9c268f04f88e88578525a628cbb'}, 'author/SOURCE_MANIFEST.json': {'bytes': 6318, 'sha256': 'c2313cd12d5c093c09745104ae404d5600af60c329231cb580e616ec13dc3280'}, 'author/STATUS.json': {'bytes': 1103, 'sha256': 'fb029f4aa320bf1e51b17240aef1bb845551ba30ec688f11f62142c6309fa872'}, 'author/VERIFICATION.md': {'bytes': 3950, 'sha256': '9a45756a9cd25ec5d324ed8d09d9c3b510afdf0131961c3ce5a228249b09d4a1'}, 'author/check_claims.py': {'bytes': 14597, 'sha256': '94bb4af6b13f092d49b37e0fd0177659aa66aaac17270c44fa141ff019aee2c4'}}
PAYLOAD = set(ACCEPTED) | {'README.md','ACCEPTANCE.md','verify_publication.py','mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json','BOOTSTRAP.py'}
DIRS = {'author','audit'}
CASES = [
 ('dilation_wrong_argument','t*pl_value(points,x/t)','t*pl_value(points,t*x)','track diameter bound failed'),
 ('interval_target_on_C','u=l+F(2,5)*L; v=l+F(3,5)*L','u=l; v=l+L/10','target gap meets next Cantor stage'),
 ('magnus_wrong_inverse','return u+v+inverse_word(u)+inverse_word(v)','return u+v+inverse_word(v)+inverse_word(u)','full Magnus leading term failed'),
 ('duality_drop_infinity','if degree==0:return N  # reduced H^0','if degree==0:return 0  # reduced H^0','H2 dimension boundary failed'),
 ('radial_expands','a=multiplier*r','a=r/multiplier','PL strict monotonicity required')]

def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def same(a, b):
    if type(a) is not type(b):
        return False
    if type(b) is dict:
        return set(a) == set(b) and all(same(a[k], v) for k, v in b.items())
    if type(b) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def nonfinite(value):
    raise ValueError('nonfinite JSON number')


def finite(value):
    result = float(value)
    need(math.isfinite(result), 'overflowed JSON number')
    return result


def parse(raw):
    return json.loads(raw, object_pairs_hook=unique, parse_constant=nonfinite, parse_float=finite)


def keys(obj, names):
    need(type(obj) is dict and set(obj) == set(names), 'exact object schema')


def exact_int(value, expected=None):
    need(type(value) is int and value >= 0 and (expected is None or value == expected), 'exact nonnegative integer')


def digest(value):
    need(type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None, 'lowercase SHA-256')


def inventory(root):
    for path in (root, *root.parents):
        need(stat.S_ISDIR(path.lstat().st_mode), 'linked/non-directory root or ancestor')
    files, dirs = set(), set()
    def visit(directory):
        for entry in os.scandir(directory):
            path = Path(entry.path)
            name = path.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                need(name in DIRS, 'extra directory')
                dirs.add(name)
                visit(path)
            else:
                need(stat.S_ISREG(mode), 'symlink or special member')
                files.add(name)
    visit(root)
    need(files == FILES and dirs == DIRS, 'exact recursive inventory')


def ordinary(path):
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_size <= 1000000, 'regular bounded member')
    with os.fdopen(os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)), 'rb') as stream:
        opened = os.fstat(stream.fileno())
        need((before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino), 'member replaced at open')
        raw = stream.read(1000001)
    need(len(raw) == before.st_size, 'member size changed')
    return raw


def manifest(value, snapshot, payload, role=None):
    keys(value, ['schema', 'problem_id', 'files'] + (['role'] if role is not None else []))
    if role is not None:
        need(same(value['role'], role), 'manifest role')
    exact_int(value['schema'], 1)
    exact_int(value['problem_id'], 3422)
    rows = value['files']
    need(type(rows) is list and len(rows) == len(payload), 'manifest list length/type')
    seen = set()
    for row in rows:
        keys(row, ['path', 'bytes', 'sha256'])
        name = row['path']
        need(type(name) is str and name in payload and name not in seen, 'unknown/duplicate manifest path')
        seen.add(name)
        exact_int(row['bytes']); digest(row['sha256'])
        need(same(row, dict(path=name, bytes=len(snapshot[name]), sha256=sha(snapshot[name]))), 'manifest byte binding')
    need(seen == payload, 'manifest inventory')


def integrity(root, manifest_pin, bootstrap_pin):
    digest(manifest_pin); digest(bootstrap_pin)
    inventory(root)
    snapshot = {name: ordinary(root/name) for name in FILES}
    need(sha(snapshot['PUBLICATION_MANIFEST.json']) == manifest_pin, 'external manifest pin')
    need(sha(snapshot['BOOTSTRAP.py']) == bootstrap_pin, 'external bootstrap pin')
    parsed = {name: parse(raw) for name, raw in snapshot.items() if name.endswith('.json')}
    manifest(parsed['PUBLICATION_MANIFEST.json'], snapshot, PAYLOAD)
    for name, row in ACCEPTED.items():
        need(same(row, dict(bytes=len(snapshot[name]), sha256=sha(snapshot[name]))), 'accepted evidence bytes changed')
    pins=parsed['author/PAYLOAD_PINS.json']
    keys(pins,['schema','files']);exact_int(pins['schema'],1)
    # The unmodified inner native manifests have their original schemas; this
    # strict external wrapper binds and validates their entire file inventories.
    for prefix,key in [('author/','author/PAYLOAD_PINS.json'),('audit/','audit/AUDIT_MANIFEST.json')]:
        rows=parsed[key]['files'];expected={n[len(prefix):] for n in ACCEPTED if n.startswith(prefix) and n!=key}
        need(type(rows) is list and len(rows)==len(expected),'inner inventory list')
        seen=set()
        for row in rows:
            keys(row,['path','bytes','sha256']);n=row['path']
            need(type(n) is str and n in expected and n not in seen,'inner manifest path')
            seen.add(n);exact_int(row['bytes']);digest(row['sha256'])
            need(same(row,dict(path=n,bytes=len(snapshot[prefix+n]),sha256=sha(snapshot[prefix+n]))),'inner bytes')
        need(seen==expected,'inner exact inventory')
    import ast
    for name in ['author/check_claims.py','audit/check_independent.py','verify_publication.py','mutation_tests.py','BOOTSTRAP.py']:
        need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(snapshot[name]))),'no optimized-away assertions')
    status=parsed['author/STATUS.json'];decision=parsed['audit/ACCEPTANCE.json']
    need(same(status['problem_id'],3422) and same(status['substantive_proof_search_approaches'],0),'0/5 prior-resolution status')
    need(status['classification']['sticky_exists_iff']=='n >= 4' and status['new_mathematical_discovery_claimed'] is False,'classification and novelty')
    need(decision['audit_outcome']=='accepted_prior_literature_resolution' and decision['new_discovery'] is False and decision['original_Sher_proof_inspected'] is False,'accepted scope')
    need(same(decision['problem_id'],3422) and same(decision['substantive_proof_search_approaches'],0),'accepted identity')
    sl=parsed['PUBLIC_SCOPE.json']
    for name in ['fresh_source_retrieval','fresh_source_inspection','fresh_pdf_byte_bindings','fresh_dataset_byte_bindings','full_baseline_patch_replay','archive_reconstruction']:
        need(sl[name]=='NOT_RUN','honest source-free scope')
    return snapshot


def replay(snapshot):
    """Fresh source-free native executions and independent mathematical mutations."""
    import shutil
    need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000 required')
    modes=[('normal',[]),('O',['-O']),('OO',['-OO'])]
    with tempfile.TemporaryDirectory(prefix='sticky-cantor-public-replay-') as td:
        root=Path(td);ro=root/'author';ro.mkdir();audit=root/'audit';audit.mkdir();cwd=root/'cwd';cwd.mkdir()
        for prefix,dest in [('author/',ro),('audit/',audit)]:
            for name,body in snapshot.items():
                if name.startswith(prefix): (dest/name[len(prefix):]).write_bytes(body)
        def freeze(d):
            for f in d.rglob('*'):f.chmod(0o555 if f.is_dir() else 0o444)
            d.chmod(0o555)
        def thaw(d):
            d.chmod(0o755)
            for f in d.rglob('*'):f.chmod(0o755 if f.is_dir() else 0o644)
        freeze(ro);freeze(audit);freeze(cwd)
        initial={str(f.relative_to(root)):sha(f.read_bytes()) for d in [ro,audit] for f in d.rglob('*') if f.is_file()}
        env=dict(PATH=os.defpath,HOME=str(root),TMPDIR=str(root),LC_ALL='C',PYTHONDONTWRITEBYTECODE='1')
        def execute(args,flags,where=cwd):
            q=subprocess.run([sys.executable,'-I','-S','-B',*flags,*map(str,args)],cwd=where,env=env,capture_output=True,timeout=300)
            out=q.stdout.decode().replace(str(root),'<replay>');err=q.stderr.decode().replace(str(root),'<replay>')
            return dict(exit_code=q.returncode,stdout=out,stderr=err,stdout_bytes=len(out.encode()),stdout_sha256=sha(out.encode()))
        try:
            natives=[];independents=[]
            historical=parse(snapshot['audit/INDEPENDENT_RUNS.json'])
            expected_author={label:next(r['stdout'] for r in historical['runs'] if r['name']=='frozen_'+label) for label,flags in modes}
            for i,(mode,flags) in enumerate(modes):
                r=execute([ro/'check_claims.py','--require-readonly'],flags)
                need(r['exit_code']==0 and r['stderr']=='' and r['stdout']==expected_author[mode],'full native author output '+mode)
                value=parse(r['stdout']);need(same(value['uid'],1000) and same(value['python_optimization'],i),'native runtime types')
                r.update(mode=mode);natives.append(r)
                dest=root/('independent_'+mode)
                r=execute([audit/'check_independent.py',ro,dest],flags)
                need(r['exit_code']==0 and r['stderr']=='','full independent native execution '+mode)
                value=parse((dest/'INDEPENDENT_RUNS.json').read_bytes())
                expected=dict(historical,python_optimization=i)
                need(same(value,expected),'complete independent receipt match '+mode)
                if mode=='OO':need(same(value,parse(snapshot['audit/INDEPENDENT_RUNS_DRIVER_OO.json'])),'historical optimized receipt exact')
                r.update(mode=mode,complete_native_receipt=value);independents.append(r)
            probe_code="""import errno,json,os,sys
r={'uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,'directory_mode':oct(os.stat('.').st_mode&0o777),'file_mode':oct(os.stat('check_claims.py').st_mode&0o777),'directory_writable':os.access('.',os.W_OK),'operations':[]}
for name,action in [('create',lambda:os.open('NEW_FILE',os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)),('open_existing',lambda:os.open('check_claims.py',os.O_WRONLY)),('mkdir',lambda:os.mkdir('NEW_DIRECTORY'))]:
 try:
  fd=action()
  if isinstance(fd,int):os.close(fd)
  raise RuntimeError('write allowed')
 except OSError as e:
  if e.errno not in (errno.EACCES,errno.EPERM,errno.EROFS):raise
  r['operations'].append({'name':name,'denied':True,'errno':e.errno})
print(json.dumps(r,sort_keys=True))
"""
            probes=[];branches=[]
            writable=root/'writable';shutil.copytree(ro,writable);thaw(writable)
            for i,(mode,flags) in enumerate(modes):
                r=execute(['-c',probe_code],flags,ro)
                need(r['exit_code']==0 and r['stderr']=='','physical probes executed')
                goal=dict(uid=1000,euid=1000,optimization=i,directory_mode='0o555',file_mode='0o444',directory_writable=False,operations=[dict(name=n,denied=True,errno=13) for n in ['create','open_existing','mkdir']])
                need(same(parse(r['stdout']),goal),'exact physical permission probes');r.update(mode=mode);probes.append(r)
                ext=root/('external_'+mode+'.json')
                r=execute([ro/'check_claims.py','--require-readonly','--output',ext],flags)
                need(r['exit_code']==0 and r['stdout']==r['stderr']=='' and ext.read_text()==expected_author[mode],'external output exact');r.update(mode=mode,branch='external_output',file_content=ext.read_text());branches.append(r)
                r=execute([ro/'check_claims.py','--require-readonly','--output',ro/'FORBIDDEN.json'],flags)
                need(r['exit_code']==1 and r['stderr']=='RuntimeError: output must be external to the packet\n' and not (ro/'FORBIDDEN.json').exists(),'internal output rejection');r.update(mode=mode,branch='inside_output');branches.append(r)
                r=execute([writable/'check_claims.py','--require-readonly'],flags)
                need(r['exit_code']==1 and r['stderr']=='RuntimeError: packet directory is writable\n','writable tree rejection');r.update(mode=mode,branch='writable_tree');branches.append(r)
            mutations=[]
            for label,old,new,reason in CASES:
                dest=root/label;shutil.copytree(ro,dest);thaw(dest)
                source=(dest/'check_claims.py').read_text();need(source.count(old)==1,'unique semantic mutation target')
                (dest/'check_claims.py').write_text(source.replace(old,new))
                pins=parse((dest/'PAYLOAD_PINS.json').read_bytes())
                for row in pins['files']:
                    if row['path']=='check_claims.py':row.update(bytes=(dest/'check_claims.py').stat().st_size,sha256=sha((dest/'check_claims.py').read_bytes()))
                (dest/'PAYLOAD_PINS.json').write_text(json.dumps(pins,indent=2)+'\n');freeze(dest)
                rows=[]
                for mode,flags in modes:
                    r=execute([dest/'check_claims.py','--require-readonly'],flags)
                    need(r['exit_code']==1 and r['stdout']=='' and r['stderr']=='RuntimeError: '+reason+'\n','repinned semantic rejection '+label+' '+mode)
                    r.update(mode=mode);rows.append(r)
                mutations.append(dict(mutation=label,checker_pin_refreshed=True,expected_error=reason,runs=rows));thaw(dest)
            # Mutate the independent implementation itself, not the author's
            # polynomial implementation, and run just its declared exact tests.
            independent_mutations=[]
            for label,old,new,reason,function in [
                ('matrix_zero_generator','a[start][start+1]=1','a[start][start+1]=0','distinct-letter matrix detection','matrix_tests'),
                ('uniform_metric_false_witness','x=Fraction(m)','x=Fraction(0)','uniform-topology counterexample witness','topology_samples')]:
                source=snapshot['audit/check_independent.py'].decode();need(source.count(old)==1,'independent mutation target')
                source=source.replace(old,new);script=root/(label+'.py');script.write_text(source);script.chmod(0o444)
                runner="import runpy,sys\nd=runpy.run_path(sys.argv[1])\ntry:d[sys.argv[2]]()\nexcept RuntimeError as e:\n print('RuntimeError: '+str(e),file=sys.stderr);sys.exit(1)\n"
                rows=[]
                for mode,flags in modes:
                    r=execute(['-c',runner,script,function],flags)
                    need(r['exit_code']==1 and r['stdout']=='' and r['stderr']=='RuntimeError: '+reason+'\n','independent semantic rejection')
                    r.update(mode=mode);rows.append(r)
                independent_mutations.append(dict(mutation=label,expected_error=reason,runs=rows))
            final={str(f.relative_to(root)):sha(f.read_bytes()) for d in [ro,audit] for f in d.rglob('*') if f.is_file()}
            need(initial==final and not list(cwd.iterdir()),'all source-free inputs unchanged')
            return dict(status='PASS',problem_id=3422,classification='sticky exists iff n >= 4',disposition='already_solved',turns='0/5',new_discovery=False,native_author_runs=natives,native_independent_runs=independents,physical_write_probes=probes,cli_branches=branches,author_semantic_mutations=mutations,independent_semantic_mutations=independent_mutations,extra_semantic_executions=21,top_level_subprocess_executions=39,native_harness_nested_executions=36,readonly_inputs_unchanged=True,fresh_source_retrieval='NOT_RUN',fresh_source_inspection='NOT_RUN',fresh_pdf_byte_bindings='NOT_RUN',fresh_dataset_byte_bindings='NOT_RUN',full_baseline_patch_replay='NOT_RUN',archive_reconstruction='NOT_RUN',scope='Source-free executable replay only. Historical source and corpus checks are retained metadata, not rerun. Finite checks do not prove imported topological theorems or novelty.')
        finally:
            for d in [ro,audit,cwd]:thaw(d)


def main():
    need(len(sys.argv)==4,'supply external manifest pin, external bootstrap pin, and root')
    mp,bp,location=sys.argv[1:];root=Path(os.path.abspath(location));before=integrity(root,mp,bp)
    result=replay(before)
    need(same(result,parse(before['REPLAY_RESULTS.json'])),'fresh complete replay equals pinned record')
    need(integrity(root,mp,bp)==before,'entire release unchanged after replay')
    print(json.dumps(dict(status='PASS',optimization=sys.flags.optimize,problem_id=3422,disposition='already_solved',turns='0/5',manifest_sha256=mp,bootstrap_sha256=bp,exact_files=len(FILES),fresh_pdf_byte_bindings='NOT_RUN',replay=result),indent=2,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,UnicodeError,subprocess.TimeoutExpired):
        print('REJECT: publication integrity or replay failed',file=sys.stderr);sys.exit(1)
