#!/usr/bin/env python3
"""Fail-closed frozen-byte replay. Run through BOOTSTRAP.py with external pins."""
from pathlib import Path, PurePosixPath
import hashlib, io, json, os, re, stat, subprocess, sys, tempfile, zipfile
EXPECTED_MANIFEST='e1aa37ba35b8f119e6e97c632bbd7d29e049dd94722a1253293e793eb7973305'
AUTHOR_ARCHIVE='archives/MINIMAL_SURFACES_10300008_AUTHOR.zip'
AUDIT_ARCHIVE='archives/MINIMAL_SURFACES_10300008_INDEPENDENT_AUDIT.zip'
class Reject(Exception):pass
def need(c,m):
    if not c:raise Reject(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(ps):
    d={}
    for k,v in ps:
        need(k not in d,'duplicate JSON key');d[k]=v
    return d
def load(b):return json.loads(b,object_pairs_hook=pairs)
def safe(n):return type(n) is str and n!='' and '\\' not in n and not n.startswith('/') and all(x not in ('','.','..') for x in n.split('/'))
def inventory(root):
    need(not root.is_symlink() and root.is_dir(),'root symlink or not directory')
    out={};dirs=set()
    def visit(d,prefix):
        for entry in os.scandir(d):
            name=prefix+entry.name;mode=entry.stat(follow_symlinks=False).st_mode
            need(not stat.S_ISLNK(mode),'symlink: '+name)
            if stat.S_ISDIR(mode):dirs.add(name);visit(Path(entry.path),name+'/')
            else:
                need(stat.S_ISREG(mode),'nonregular member: '+name);out[name]=Path(entry.path).read_bytes()
    visit(root,'');return out,dirs

def authenticate(root):
    files,dirs=inventory(root)
    need('PUBLICATION_MANIFEST.json' in files,'missing publication manifest')
    raw=files['PUBLICATION_MANIFEST.json'];need(sha(raw)==EXPECTED_MANIFEST,'publication manifest trust anchor')
    m=load(raw);need(type(m) is dict and set(m)=={'schema','problem_id','rank','disposition','approaches','files'},'manifest schema')
    need(m['schema']=='minimal-surfaces-publication-manifest-v1' and type(m['problem_id']) is int and m['problem_id']==10300008 and type(m['rank']) is int and m['rank']==1003,'identity')
    need(m['disposition']=='unsolved' and type(m['approaches']) is int and m['approaches']==5,'disposition')
    need(type(m['files']) is list and len(m['files'])>0,'manifest inventory')
    expected={'PUBLICATION_MANIFEST.json','VERIFY_PUBLICATION.py','BOOTSTRAP.py'}
    for e in m['files']:
        need(type(e) is dict and set(e)=={'path','bytes','sha256'},'entry schema');n=e['path']
        need(safe(n) and n not in expected,'unsafe or duplicate entry');expected.add(n)
        need(n in files,'missing: '+n);b=files[n]
        need(type(e['bytes']) is int and e['bytes']>=0 and len(b)==e['bytes'],'byte count: '+n)
        need(type(e['sha256']) is str and re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None and sha(b)==e['sha256'],'digest: '+n)
    need(set(files)==expected,'unexpected or missing publication member')
    expected_dirs={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'}
    need(dirs==expected_dirs,'unexpected or missing directory')
    need(files['VERIFY_PUBLICATION.py']==Path(__file__).read_bytes(),'different verifier copy')
    # BOOTSTRAP.py independently authenticates this verifier before executing it.
    # Its own bytes are an external trust anchor, not a self-authenticating claim.
    return files

def archive_members(b,expected):
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        names=z.namelist();need(len(names)==len(set(names)) and set(names)==set(expected),'archive inventory')
        for i in z.infolist():
            need(safe(i.filename) and not i.is_dir(),'unsafe archive path')
            mode=i.external_attr>>16
            need(not stat.S_ISLNK(mode) and (stat.S_IFMT(mode) in (0,stat.S_IFREG)),'archive member type')
            need(z.read(i)==expected[i.filename],'archive member bytes: '+i.filename)
    return len(expected)

def apply_patch(original,patch):
    lines=patch.decode('utf-8').splitlines(keepends=True)
    need(lines[:2]==['--- a/test_bootstrap.py\n','+++ b/test_bootstrap.py\n'],'patch target')
    need(len(lines)>2,'empty patch')
    match=re.fullmatch(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n',lines[2]);need(match is not None,'patch hunk')
    old_start,old_count,new_start,new_count=map(int,match.groups())
    old=[];new=[]
    for line in lines[3:]:
        need(line and line[0] in ' +-','patch line')
        if line[0] in ' -':old.append(line[1:])
        if line[0] in ' +':new.append(line[1:])
    need(len(old)==old_count and len(new)==new_count and old_start==new_start,'patch counts')
    source=original.decode('utf-8').splitlines(keepends=True);start=old_start-1
    need(source[start:start+old_count]==old,'patch context mismatch')
    return ''.join(source[:start]+new+source[start+old_count:]).encode()

def semantic_checks(f):
    ar=load(f['AUTHOR_RECEIPT.json']);audr=load(f['INDEPENDENT_AUDIT_RECEIPT.json'])
    need(sha(f[AUTHOR_ARCHIVE])=='61fc41de148b8502dbc899e9eaa09e5864fabbf98869c691378b50a3001c8274' and len(f[AUTHOR_ARCHIVE])==25054,'original archive pin')
    need(sha(f[AUDIT_ARCHIVE])=='4968d81aed83a50c3dc9fbf4dd078de9e4ef22a521b9621376478e33c9bf10a8' and len(f[AUDIT_ARCHIVE])==26195,'audit archive pin')
    need(sha(f['audit/AUDIT_MANIFEST.json'])=='f13f5487b6e21e396fb60dc28e51cbcc6b74744ce9ce3a49234b990fa1413013','audit manifest pin')
    original={n.removeprefix('author_original/'):b for n,b in f.items() if n.startswith('author_original/')}
    corrected={n.removeprefix('author_corrected/'):b for n,b in f.items() if n.startswith('author_corrected/')}
    audit={n.removeprefix('audit/'):b for n,b in f.items() if n.startswith('audit/')}
    ac=archive_members(f[AUTHOR_ARCHIVE],original);rc=archive_members(f[AUDIT_ARCHIVE],audit)
    need(set(original)==set(corrected),'corrected inventory')
    need([n for n in sorted(original) if original[n]!=corrected[n]]==['test_bootstrap.py'],'correction boundary')
    need(apply_patch(original['test_bootstrap.py'],audit['HARNESS_CORRECTION.patch'])==corrected['test_bootstrap.py']==audit['test_bootstrap.patched.py'],'actual patch replay')
    need(sha(original['bootstrap.py'])=='8c9d563a3db73283718d50c7fefe44f846eda56035df85ea4c8b4dab72b22b2e','outer bootstrap pin')
    need(sha(original['test_bootstrap.py'])=='582fd716a9b52d2b81a19acab2d01b9135c3004b2f37ed9cae95c2deb48a0cd7','original outer harness pin')
    need(sha(corrected['test_bootstrap.py'])=='53d2f1cc91ba3b77d5b350efc66ef6c71a0632f7c5db5339f7a595260509dc85','corrected outer harness pin')
    for e in ar['package_files']:
        b=original[e['path']];need(len(b)==e['bytes'] and sha(b)==e['sha256'],'author receipt binding')
    am=load(audit['AUDIT_MANIFEST.json'])
    need(set(audit)=={e['path'] for e in am['files']}|{'AUDIT_MANIFEST.json'},'audit manifest inventory')
    for e in am['files']:
        b=audit[e['path']];need(len(b)==e['bytes'] and sha(b)==e['sha256'],'audit manifest member')
    a=load(audit['ACCEPTANCE.json'])
    need(a['decision']=='accept_scoped_mathematics_with_harness_correction' and a['disposition']=='unsolved' and type(a['approaches']) is int and a['approaches']==5,'audit acceptance')
    need(a['general_resolution'] is False and a['explicit_independent_isotopy_counterexample'] is False and a['mathematical_patch_required'] is False and a['harness_patch_required'] is True,'scope flags')
    return {'author_archive_members':ac,'audit_archive_members':rc,'actual_patch_applied':True,'mathematical_payload_unchanged':True,'outer_files_independently_bound':True}

def invoke(root,script,*args):
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    cp=subprocess.run([sys.executable,'-I','-S','-B']+flags+[str(root/script),*map(str,args)],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
    need(cp.returncode==0,'replay failed '+script+': '+cp.stderr.decode('utf-8','replace'));need(cp.stderr==b'','replay stderr '+script)
    return cp.stdout

def main():
    need(len(sys.argv) in (2,3),'usage: VERIFY_PUBLICATION.py ROOT [--integrity-only]')
    need(len(sys.argv)==2 or sys.argv[2]=='--integrity-only','unknown option')
    root=Path(sys.argv[1]).absolute();before=authenticate(root);report=semantic_checks(before)
    if len(sys.argv)==3:return {'schema':'minimal-surfaces-publication-integrity-v1','status':'pass','problem_id':10300008,'disposition':'unsolved','approaches':5,**report}
    with tempfile.TemporaryDirectory(prefix='minimal-publication-replay-') as tmp:
        work=Path(tmp)
        # Only authenticated buffered bytes enter the executable staging tree.
        for n,b in before.items():
            p=work/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        bootstrap=invoke(work,'author_original/bootstrap.py')
        harness=invoke(work,'author_corrected/test_bootstrap.py')
        hr=load(harness);record=load(before['author_corrected/REPLAY.json'])
        record.pop('outer_harness_modes');record.pop('outer_harness_outputs_identical')
        need(hr==record,'corrected harness differs from historical annotated replay')
        need(hr['positive_count']==6 and hr['negative_count']==78 and hr['read_only_write_denied'] is True,'corrected harness counts')
        independent=invoke(work,'audit/independent_verify.py',work/AUTHOR_ARCHIVE)
        need(independent==before['audit/INDEPENDENT_RESULTS_normal.json']==before['audit/INDEPENDENT_RESULTS_O.json']==before['audit/INDEPENDENT_RESULTS_OO.json'],'independent replay bytes')
        ir=load(independent)
        need(ir['status']=='pass_with_harness_patch' and ir['independent_malformed_run_count']==30 and ir['read_only_write_denied'] is True,'independent replay scope')
        report.update(author_bootstrap_stdout_sha256=sha(bootstrap),corrected_harness_stdout_sha256=sha(harness),independent_stdout_sha256=sha(independent),corrected_positive_runs=6,corrected_integrity_rejections=78,independent_malformed_runs=30,read_only_write_denied=True)
    need(authenticate(root)==before,'publication bytes changed during replay')
    return {'schema':'minimal-surfaces-publication-replay-v1','status':'pass','problem_id':10300008,'rank':1003,'disposition':'unsolved','approaches':5,'source_free':True,'github_ci':False,'finite_checks_prove_geometry':False,'publication_manifest_sha256':EXPECTED_MANIFEST,**report}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True,indent=2))
    except (Reject,OSError,ValueError,TypeError,KeyError,IndexError,subprocess.SubprocessError,zipfile.BadZipFile) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
