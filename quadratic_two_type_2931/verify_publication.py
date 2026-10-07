#!/usr/bin/env python3
"""Authenticate this exact partial-result publication, then replay bounded checks."""
import sys
if sys.flags.optimize:
    raise SystemExit('REJECT: -O/-OO are unsupported; expected rejection, not mathematical validation.')
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: invoke with -I -S -B')
import hashlib, io, json, os, pathlib, shlex, stat, subprocess, tempfile, zipfile
PINS = {
 'QUADRATIC_TWO_TYPE_2931_UPDATED_INDEPENDENT_AUDIT_SAFE.zip': (52424,'cd960d0ffbb23e383479a93c0b978e952f1cc8e9be92f05fffe72fed1bd166b9'),
 'QUADRATIC_TWO_TYPE_2931_UPDATED_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': (3520,'68978b3d3b2947d46d8ab9e1c1094c891040aaf9a7b0fda23d9366427521e2f5'),
 'QUADRATIC_TWO_TYPE_2931_UPDATED_INDEPENDENT_AUDIT_RECEIPT.json': (1927,'cc1fb1a08c1105c6e4a5a79e804eca034bb95b2ccda306b99f71de620f9224c1'),
 'audit/QUADRATIC_TWO_TYPE_2931_AUTHOR_SAFE_FREEZE.zip': (14117,'a7feb177dbc27c56674e4333675303fa91cfbf2bfb61905273361934b8cca368'),
 'audit/QUADRATIC_TWO_TYPE_2931_AUTHOR_EXTERNAL_MANIFEST.json': (1743,'30bd1af52d976b711cc52a6c30abca55f0832ef9e767702232dc38b6e9051a20'),
 'audit/QUADRATIC_TWO_TYPE_2931_CORRECTED_SAFE.zip': (14294,'ef24b757bb91a0854f13b40892fac78e7ca5a714ff4af14c4b5df4bcdf889c64'),
 'audit/QUADRATIC_TWO_TYPE_2931_CORRECTED_EXTERNAL_MANIFEST.json': (1950,'e2b2d992b3e4be35c8c2302b27f390cc1899b409cc2205a882b63e57aa61ceee'),
 'audit/EXACT_ACCEPTANCE.json': (3421,'fae8dee3a0325e67449c03def18225cd811ac1c58826ffaae9129f3cd392e3f8'),
 'audit/EXACT_ACCEPTANCE.md': (1502,'e63766dcee859c9c01f02f4c0120922923a35ca0c95b8725690b715a4cf973f4'),
 'audit/CORRECTIONS.patch': (8043,'e4fd653aca90738d31f9d645cfab4f3458f5d5ae78d00e4e13109ced7419974c'),
 'audit/REVIEW_PROVENANCE_CORRECTION.patch': (2420,'bd8e1e94fa2f1a33d98541509bdfc38b3025a95478d399ae6ba3d77ac80f09d7'),
}
def need(c,m):
    if not c: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def pairs(items):
    d={}
    for k,v in items:
        need(k not in d,'duplicate JSON key');d[k]=v
    return d
def reject_constant(c): raise ValueError('nonfinite JSON constant')
def decode(b): return json.loads(b,object_pairs_hook=pairs,parse_constant=reject_constant)
def read_regular(p):
    need(stat.S_ISREG(p.lstat().st_mode),'nonregular file: '+p.name)
    return p.read_bytes()
def zip_members(b):
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        infos=z.infolist();ns=[i.filename for i in infos]
        need(len(ns)==len(set(ns)),'duplicate ZIP member')
        for i in infos:
            need(i.filename==pathlib.PurePosixPath(i.filename).name and i.filename not in ('','.','..'),'unsafe ZIP path')
            need(not i.is_dir() and stat.S_ISREG(i.external_attr>>16) and not i.flag_bits&1,'nonregular or encrypted ZIP member')
        return {i.filename:z.read(i) for i in infos}
def main():
    need(len(sys.argv)==3 and sys.argv[1]=='--expected-manifest','trusted manifest digest required')
    anchor=sys.argv[2];need(len(anchor)==64 and all(c in '0123456789abcdef' for c in anchor),'invalid digest')
    root=pathlib.Path(__file__).absolute().parent
    need(all(not p.is_symlink() for p in [root,*root.parents]),'symlink ancestry')
    mb=read_regular(root/'PUBLICATION_MANIFEST.json');need(sha(mb)==anchor,'manifest anchor mismatch')
    manifest=decode(mb);need(manifest['schema']=='quadratic-two-type-publication-v1' and type(manifest['problem_id']) is int and manifest['problem_id']==2931,'identity')
    entries=manifest['files'];names=[e['path'] for e in entries]
    need(len(names)==len(set(names)) and 'PUBLICATION_MANIFEST.json' not in names,'manifest inventory')
    for n in names:
        p=pathlib.PurePosixPath(n);need(not p.is_absolute() and all(c not in ('','.','..') for c in p.parts) and p.as_posix()==n,'unsafe path')
    dirs={parent.as_posix() for n in names for parent in pathlib.PurePosixPath(n).parents if str(parent)!='.'};actual=set()
    for p in root.rglob('*'):
        n=p.relative_to(root).as_posix();mode=p.lstat().st_mode
        if stat.S_ISDIR(mode): need(n in dirs,'unexpected directory')
        else: need(stat.S_ISREG(mode),'link or special file');actual.add(n)
    need(actual==set(names)|{'PUBLICATION_MANIFEST.json'},'file inventory')
    data={}
    for e in entries:
        b=read_regular(root/e['path']);need(type(e['bytes']) is int and len(b)==e['bytes'] and sha(b)==e['sha256'],'member binding: '+e['path']);data[e['path']]=b
    for n,pin in PINS.items(): need((len(data[n]),sha(data[n]))==pin,'immutable pin: '+n)
    meta=decode(data['PUBLICATION_METADATA.json']);need(meta['problem_id']==2931 and meta['rank']==920 and meta['status']=='unsolved' and meta['turns']=='5/5','canonical status')
    for f in ['full_solution','counterexample','new_classification_theorem','novelty_claim','human_peer_review_performed']:need(meta[f] is False,'claim scope: '+f)
    for folder,archive,external in [
      ('audit','QUADRATIC_TWO_TYPE_2931_UPDATED_INDEPENDENT_AUDIT_SAFE.zip','QUADRATIC_TWO_TYPE_2931_UPDATED_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'),
      ('original','audit/QUADRATIC_TWO_TYPE_2931_AUTHOR_SAFE_FREEZE.zip','audit/QUADRATIC_TWO_TYPE_2931_AUTHOR_EXTERNAL_MANIFEST.json'),
      ('corrected','audit/QUADRATIC_TWO_TYPE_2931_CORRECTED_SAFE.zip','audit/QUADRATIC_TWO_TYPE_2931_CORRECTED_EXTERNAL_MANIFEST.json')]:
        ms=zip_members(data[archive]);need(ms=={n[len(folder)+1:]:b for n,b in data.items() if n.startswith(folder+'/')},'ZIP/extraction binding: '+folder)
        mf=decode(data[external]);es=mf['files'];need(len(es)==len(ms) and {e['path'] for e in es}==set(ms),'external member inventory')
        need((len(data[archive]),sha(data[archive]))==(mf['archive']['bytes'],mf['archive']['sha256']),'external archive pin')
        for e in es: need((len(ms[e['path']]),sha(ms[e['path']]))==(e['bytes'],e['sha256']),'external member binding')
    acceptance=decode(data['audit/EXACT_ACCEPTANCE.json']);need(acceptance['verdict']=='ACCEPT_CORRECTED_STALLED_PARTIAL' and acceptance['human_peer_review_performed'] is False and acceptance['review_provenance']=='AI-assisted mathematical review','acceptance scope')
    need(len(acceptance['accepted_members'])==8,'acceptance inventory')
    for e in acceptance['accepted_members']:
        b=data['corrected/'+e['path']];need((len(b),sha(b))==(e['bytes'],e['sha256']),'exact acceptance')
    with tempfile.TemporaryDirectory(prefix='quadratic publication authenticated snapshot ') as td:
        td=pathlib.Path(td);snapshot=td/'packet';snapshot.mkdir();cwd=td/'unrelated cwd';cwd.mkdir()
        for n,b in data.items():
            p=snapshot/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        patched=td/'patched';patched.mkdir()
        for n,b in data.items():
            if n.startswith('original/'):(patched/n.split('/',1)[1]).write_bytes(b)
        r=subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(snapshot/'audit/CORRECTIONS.patch')],cwd=patched,capture_output=True,timeout=30)
        need(r.returncode==0,'mathematical patch command')
        need({p.name:p.read_bytes() for p in patched.iterdir()}=={n.split('/',1)[1]:b for n,b in data.items() if n.startswith('corrected/')},'mathematical patch bytes')
        shim=td/'isolated-python';shim.write_text('#!/bin/sh\nexec '+shlex.quote(os.path.realpath(sys.executable))+' -I -S -B "$@"\n');shim.chmod(0o700)
        launcher="import sys;from pathlib import Path;shim,entry,*args=sys.argv[1:];sys.executable=shim;sys.argv=[entry,*args];exec(compile(Path(entry).read_bytes(),entry,'exec'),{'__name__':'__main__','__file__':entry})"
        env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
        r=subprocess.run([str(shim),'-c',launcher,str(shim),str(snapshot/'audit/replay_audit.py'),str(snapshot/'audit')],cwd=cwd,env=env,capture_output=True,timeout=180)
        need(r.returncode==0 and not r.stderr,'frozen artifact replay failed: '+r.stderr.decode(errors='replace'))
        replay=decode(r.stdout);need(replay['test_count']==36 and len(replay['tests'])==36 and replay['all_expected_outcomes'] is True,'artifact test count')
        for row in replay['tests']:need(row['exit_code']==row['expected_exit'],'unexpected test exit')
    print(json.dumps({'result':'pass','problem_id':2931,'status':'unsolved','turns':'5/5','files_verified':len(data)+1,'artifact_expected_exit_tests':36,'mathematical_patch_reproduced':True,'review_provenance_patch_replayed_by_wrapper':False,'old_audit_distribution':False,'source_bytes_rehashed_this_run':False,'authenticated_snapshot':True,'descendants_isolated_no_site_no_bytecode':True,'automated_mathematical_validation':False},sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:
        print(json.dumps({'result':'fail','error':str(e)},sort_keys=True),file=sys.stderr);sys.exit(2)
