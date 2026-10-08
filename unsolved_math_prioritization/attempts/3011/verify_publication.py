#!/usr/bin/env python3
"""Authenticate frozen homeomorphism ANR partial results; replay source-free finite checks."""
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

ACCEPTED = {'accepted/CORRECTIONS.md': {'bytes': 2861, 'sha256': '0fe1edd757ac6c633d851829fb70b83a1f052ec7d0965226cb2a7cf4d85956e8'}, 'accepted/CORRECTIONS.patch': {'bytes': 5212, 'sha256': '08233410b44a52851dc759abdedd7b24b8874a09ec311467648df35cbd8e4976'}, 'accepted/PARAMETRIC_EXTENSION.md': {'bytes': 17261, 'sha256': '3aca28813feb496f55b238c1d1feccf3f9de044d213225f24b63554f12973e91'}, 'accepted/README.md': {'bytes': 1816, 'sha256': '9709c1d9a1a521a5d865396f28b14a11e8cb71bd020d73a0d77a6cb8833a8e57'}, 'accepted/REPORT.md': {'bytes': 25883, 'sha256': 'd57de7c98d615a70fea2bfd3e6b5a338ac83e497adede77034b85e78a3de610f'}, 'accepted/SOURCE_AUDIT.md': {'bytes': 5422, 'sha256': '8a87bce962c50566eed1ce689d681921945b0754fe8c899998eeca9d2daef6fb'}, 'accepted/SOURCE_MANIFEST.json': {'bytes': 6864, 'sha256': '30eae75d0935dd588a0575ec38d421adcd6834dfb9da03a3739b9ed17c782cb9'}, 'accepted/STATUS.json': {'bytes': 1320, 'sha256': 'e6c91a0037fe7625711781af462017873a26ce710727806b56658c868b6caa98'}, 'accepted/VERIFICATION.md': {'bytes': 2815, 'sha256': '947ca7b31a520b47cdbba7a4f1a6d9515be4fa0fa445f2a9d1560a3aba0ee6ea'}, 'accepted/check_formulas.py': {'bytes': 11887, 'sha256': '007d654317303a7817f72c04de6a9484e67b10a34f87ffc9b93d57d637b0aefb'}, 'audit/ADVERSARIAL_REVIEW.md': {'bytes': 9503, 'sha256': 'c76c09c9380ecba6d2da84a58a112c68283222a1d7187013aad1be33762e2e4d'}, 'audit/AUDIT.md': {'bytes': 18438, 'sha256': '13c4e487b0b805145786c509539b0d021c11eaa29fe160d0b557fd280da085e6'}, 'audit/SOURCE_INSPECTION.json': {'bytes': 5299, 'sha256': '18856da053981ba6b3d436d929488eacdc2fd6da1b0181df664fb0f3023af54e'}, 'audit/independent_pl_check.py': {'bytes': 3932, 'sha256': '9c7592eafe7966c48d5d2006eab743b607c1c381cab107a3426600089d608e82'}, 'native_outputs/author_O.json': {'bytes': 729, 'sha256': '0660c7ad97506ed4c94d8a2c9d63904ff1b861c10f2864304bebf0c17afb907f'}, 'native_outputs/author_OO.json': {'bytes': 729, 'sha256': 'c5689a31675689f9add64ea95abd8ec28d7912770ef2ba357540705401d4cdbd'}, 'native_outputs/author_normal.json': {'bytes': 729, 'sha256': 'fa7f5c097b1f9f9a534c7442f572a3f4c64099bcfedf2e2c085ef25b3095d7a4'}, 'native_outputs/independent_O.json': {'bytes': 283, 'sha256': '2c95cb84143c927a20fdcb8d62fa725752d4438e506a6162ef62f09a2703da34'}, 'native_outputs/independent_OO.json': {'bytes': 283, 'sha256': '1ce68dac7a6e94d83de5d569e76fe48268c37893a62c9e1ad1182a9c4d497fcd'}, 'native_outputs/independent_normal.json': {'bytes': 283, 'sha256': 'f4fecb2ae57b2f323bd5064e6c39a47be6657863883bbefd388a5c9ba79a1cff'}, 'PUBLIC_SLICE.json': {'bytes': 6111, 'sha256': '257a0f5893ac3ad33e9df8a27f0c412faec91a7c7abb240753e99c5ac0104c6b'}, 'REPLAY_RESULTS.json': {'bytes': 50139, 'sha256': 'c472e9ffd31dd2fef12a8c054e5b52f2bcfc88db47aa1f62b1476396da0a6cbf'}}
PAYLOAD = set(ACCEPTED) | {'README.md','ACCEPTANCE.md','verify_publication.py','mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json','BOOTSTRAP.py'}
DIRS = {'accepted','audit','native_outputs'}
CASES = [('author', 'inverse_nonstrict', [('a[1] < b[1]', 'a[1] <= b[1]')], 'non-strict negative control was accepted'), ('author', 'alexander_scale', [('result.append((t*x, t*y))', 'result.append((t*x, t*t*y))')], 'Alexander inverse formula'), ('author', 'rotation_identity', [('quarter = [[0, -1], [1, 0]]', 'quarter = [[1, 0], [0, 1]]')], 'projection-collapse witness'), ('author', 'twist_identity', [('twist[2*j][2*j+1] = 1', 'twist[2*j][2*j+1] = 0'), ('inv[2*j][2*j+1] = -1', 'inv[2*j][2*j+1] = 0')], 'twist acts trivially'), ('author', 'cube_boundary', [('y = x+t*beta*(1-x*x)/4', 'y = x+t*beta*(1+x*x)/4')], 'boundary is not fixed'), ('author', 'word_order', [('for j in reversed(range(len(vertices))):', 'for j in range(len(vertices)):')], 'ordered factor formula'), ('author', 'word_zero_scale', [('if scale == 0:', 'if scale == -1:')], 'ordered factor formula'), ('author', 'radial_sign', [('return first+j-pl_eval(vertices[0], radius/tail)', 'return first+j+pl_eval(vertices[0], radius/tail)')], 'recursive interpolation disagrees'), ('author', 'radial_half_angle', [('radius, amplitude = F(1, 4), F(1, 2*n)', 'radius, amplitude = F(1, 4), F(1, 4*n)')], 'factor product does not rotate by pi'), ('independent', 'composition_order', [('ev(f,ev(g,x))', 'ev(g,ev(f,x))')], 'actual noncommutative factor mismatch'), ('independent', 'product_order', [('range(len(vertices)-1,-1,-1) if reverse else range(len(vertices))', 'range(len(vertices)) if reverse else range(len(vertices)-1,-1,-1)')], 'actual noncommutative factor mismatch'), ('independent', 'metric_scale', [('==t*distance(f,g)', '==t*t*distance(f,g)')], 'metric failure'), ('independent', 'factor_inverse', [('inv(alpha(u,vertices[j]))', 'alpha(u,vertices[j])')], 'actual noncommutative factor mismatch')]

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
    exact_int(value['problem_id'], 3011)
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
    import ast
    for name in ['accepted/check_formulas.py','audit/independent_pl_check.py','verify_publication.py','mutation_tests.py','BOOTSTRAP.py']:
        need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(snapshot[name]))),'no optimized-away assertions')
    status=parsed['accepted/STATUS.json']
    need(same(status['problem_id'],3011) and status['status']=='partial' and status['compact_core_resolved'] is False and status['novelty_claim'] is False,'accepted partial status')
    need(same(status['mathematical_approaches'],5) and same(status['literature_or_test_approaches_counted'],0),'five mathematical routes only')
    sl=parsed['PUBLIC_SLICE.json']
    need(sl['full_baseline_patch_replay']=='NOT_RUN' and sl['fresh_pdf_byte_bindings']=='NOT_RUN' and sl['compact_core_resolved'] is False,'honest public-only scope')
    for row in sl['adaptations']:
        need(same(row['published'],dict(bytes=len(snapshot[row['path']]),sha256=sha(snapshot[row['path']]))),'slice adaptation matches published bytes')
    return snapshot


def replay(snapshot):
    """Run all public-only programs, branches and controls; never read omitted inputs."""
    import shutil
    need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000 required')
    modes=[('normal',[]),('O',['-O']),('OO',['-OO'])]
    sources={'author':snapshot['accepted/check_formulas.py'],'independent':snapshot['audit/independent_pl_check.py']}
    with tempfile.TemporaryDirectory(prefix='homeomorphism-public-replay-') as td:
        root=Path(td);ro=root/'readonly';ro.mkdir();writable=root/'writable';writable.mkdir()
        for name,body in sources.items():
            (ro/(name+'.py')).write_bytes(body)
            (writable/(name+'.py')).write_bytes(body)
        for program,name,replacements,error in CASES:
            body=sources[program].decode()
            for old,new in replacements:
                need(body.count(old)==1,'one semantic mutation target '+name)
                body=body.replace(old,new)
            (ro/(program+'_'+name+'.py')).write_text(body)
        before={f.name:sha(f.read_bytes()) for f in ro.iterdir()}
        for f in ro.iterdir():f.chmod(0o444)
        ro.chmod(0o555)
        def execute(args,flags,cwd=ro):
            q=subprocess.run([sys.executable,'-I','-S','-B',*flags,*map(str,args)],cwd=cwd,capture_output=True,timeout=120)
            out=q.stdout.decode().replace(str(root),'<replay>');err=q.stderr.decode().replace(str(root),'<replay>')
            return dict(exit_code=q.returncode,stdout=out,stderr=err,stdout_bytes=len(out.encode()),stdout_sha256=sha(out.encode()))
        try:
            runs=[]
            for program in sources:
                for mode,flags in modes:
                    args=[ro/(program+'.py')]+(['--require-readonly'] if program=='author' else [])
                    r=execute(args,flags);r.update(program=program,mode=mode)
                    need(r['exit_code']==0 and r['stderr']=='' and r['stdout'].encode()==snapshot['native_outputs/'+program+'_'+mode+'.json'],'complete native-output match '+program+' '+mode)
                    runs.append(r)
            probe_code="""import errno,json,os,sys
r={'uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,'directory_mode':oct(os.stat('.').st_mode&0o777),'file_mode':oct(os.stat('author.py').st_mode&0o777),'directory_writable':os.access('.',os.W_OK),'operations':[]}
for name,action in [('create',lambda:os.open('NEW_FILE',os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)),('open_existing',lambda:os.open('author.py',os.O_WRONLY)),('mkdir',lambda:os.mkdir('NEW_DIRECTORY'))]:
 try:
  fd=action()
  if isinstance(fd,int):os.close(fd)
  raise RuntimeError('write allowed')
 except OSError as e:
  if e.errno not in (errno.EACCES,errno.EPERM,errno.EROFS):raise
  r['operations'].append({'name':name,'denied':True,'errno':e.errno})
print(json.dumps(r,sort_keys=True))
"""
            probes=[]
            for i,(mode,flags) in enumerate(modes):
                r=execute(['-c',probe_code],flags);need(r['exit_code']==0 and r['stderr']=='','physical write probes run')
                data=parse(r['stdout']);expected=dict(uid=1000,euid=1000,optimization=i,directory_mode='0o555',file_mode='0o444',directory_writable=False,operations=[dict(name=n,denied=True,errno=13) for n in ['create','open_existing','mkdir']])
                need(same(data,expected),'actual create/existing/mkdir denials');r.update(mode=mode);probes.append(r)
            branches=[]
            for mode,flags in modes:
                ext=root/('external_'+mode+'.json')
                r=execute([ro/'author.py','--require-readonly','--output',ext],flags)
                need(r['exit_code']==0 and r['stdout']==r['stderr']=='','external output execution')
                body=ext.read_bytes();need(body==snapshot['native_outputs/author_'+mode+'.json'],'full external-output byte match');r.update(mode=mode,branch='external_output',file_content=body.decode());branches.append(r)
                r=execute([ro/'author.py','--require-readonly','--output',ro/'FORBIDDEN.json'],flags)
                need(r['exit_code']!=0 and 'RuntimeError: output must be external to packet' in r['stderr'] and not (ro/'FORBIDDEN.json').exists(),'internal output rejected');r.update(mode=mode,branch='inside_output');branches.append(r)
                r=execute([writable/'author.py','--require-readonly'],flags)
                need(r['exit_code']!=0 and 'RuntimeError: packet directory is writable' in r['stderr'],'writable tree rejected');r.update(mode=mode,branch='writable_tree');branches.append(r)
            mutations=[]
            for program,name,replacements,error in CASES:
                outcomes=[]
                for mode,flags in modes:
                    args=[ro/(program+'_'+name+'.py')]+(['--require-readonly'] if program=='author' else [])
                    r=execute(args,flags)
                    need(r['exit_code']!=0 and 'RuntimeError: '+error in r['stderr'],'active semantic rejection '+program+' '+name+' '+mode)
                    r.update(mode=mode);outcomes.append(r)
                mutations.append(dict(program=program,mutation=name,expected_error=error,runs=outcomes))
            guards_code="""import runpy,sys,json
from fractions import Fraction as F
d=runpy.run_path(sys.argv[1]); tests=[('PL domain',lambda:d['pl_eval']([(F(0),F(0)),(F(1),F(1))],F(2))),('bad t negative',lambda:d['alexander']([(F(-1),F(-1)),(F(1),F(1))],F(-1))),('bad t oversized',lambda:d['alexander']([(F(-1),F(-1)),(F(1),F(1))],F(2))),('bad barycentric total',lambda:d['canonical_word']([0,1],[F(1),F(1)])),('bad radial domain',lambda:d['radial_canonical_angle']([[(F(0),F(0)),(F(1),F(0))]],[F(1)],F(2)))]
for name,f in tests:
 try:f()
 except RuntimeError:pass
 else:raise RuntimeError('guard escaped '+name)
print(json.dumps({'guards_rejected':[name for name,_ in tests],'optimization':sys.flags.optimize},sort_keys=True))
"""
            guards=[]
            for i,(mode,flags) in enumerate(modes):
                r=execute(['-c',guards_code,ro/'author.py'],flags)
                need(r['exit_code']==0 and r['stderr']=='' and same(parse(r['stdout']),dict(guards_rejected=['PL domain','bad t negative','bad t oversized','bad barycentric total','bad radial domain'],optimization=i)),'all input guard outputs');r.update(mode=mode);guards.append(r)
            need({f.name:sha(f.read_bytes()) for f in ro.iterdir()}==before,'read-only inputs unchanged')
            return dict(status='PASS',problem_id=3011,mathematical_status='partial',compact_core_resolved=False,turns='5/5',native_runs=runs,physical_write_probes=probes,cli_branches=branches,semantic_mutations=mutations,input_guards=guards,semantic_mutation_count=len(CASES),semantic_mutation_executions=3*len(CASES),total_subprocess_executions=len(runs)+len(probes)+len(branches)+3*len(CASES)+len(guards),readonly_inputs_unchanged=True,fresh_source_retrieval='NOT_RUN',fresh_source_inspection='NOT_RUN',fresh_pdf_byte_bindings='NOT_RUN',full_baseline_patch_replay='NOT_RUN',scope='Complete public-only protocol, not the complete original audit; finite exact consistency checks do not certify ANR, non-ANR or novelty.')
        finally:
            ro.chmod(0o755)
            for f in ro.iterdir():f.chmod(0o644)


def main():
    need(len(sys.argv)==4,'supply external manifest pin, external bootstrap pin, and root')
    mp,bp,location=sys.argv[1:];root=Path(os.path.abspath(location));before=integrity(root,mp,bp)
    result=replay(before)
    need(same(result,parse(before['REPLAY_RESULTS.json'])),'fresh complete public replay equals pinned record')
    need(integrity(root,mp,bp)==before,'entire release unchanged after replay')
    print(json.dumps(dict(status='PASS',optimization=sys.flags.optimize,problem_id=3011,mathematical_status='partial',compact_core_resolved=False,turns='5/5',manifest_sha256=mp,bootstrap_sha256=bp,exact_files=len(FILES),fresh_source_retrieval='NOT_RUN',fresh_source_inspection='NOT_RUN',fresh_pdf_byte_bindings='NOT_RUN',full_baseline_patch_replay='NOT_RUN',replay=result),indent=2,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,UnicodeError,subprocess.TimeoutExpired):
        print('REJECT: publication integrity or replay failed',file=sys.stderr);sys.exit(1)
