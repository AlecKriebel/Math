#!/usr/bin/env python3
"""Externally pinned byte inventory and scoped exact replay, not a proof assistant."""
import argparse, hashlib, json, shutil, stat, subprocess, sys, tempfile, zipfile
from pathlib import Path, PurePosixPath

def need(ok,message):
    if not ok: raise ValueError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def regular(p):need(not p.is_symlink() and stat.S_ISREG(p.lstat().st_mode),'nonregular file: '+str(p))
def check_manifest(root,pin):
    need(not root.is_symlink(),'symlink root')
    need(len(pin)==64 and all(c in '0123456789abcdef' for c in pin),'invalid external pin')
    p=root/'PUBLICATION_MANIFEST.json';regular(p);b=p.read_bytes();need(digest(b)==pin,'external manifest mismatch')
    m=json.loads(b);need(set(m)=={'schema','problem_id','files'} and m['schema']==1 and m['problem_id']==30000789,'manifest schema')
    files=m['files'];dirs=set()
    for n in files:
        pp=PurePosixPath(n);need(str(pp)==n and not pp.is_absolute() and '..' not in pp.parts and '\\' not in n and n!='PUBLICATION_MANIFEST.json','unsafe manifest path')
        dirs.update(str(x) for x in pp.parents if str(x)!='.')
    actual_files=set();actual_dirs=set()
    for p in root.rglob('*'):
        need(not p.is_symlink(),'symlink entry');n=p.relative_to(root).as_posix()
        if p.is_dir():actual_dirs.add(n)
        else:regular(p);actual_files.add(n)
    need(actual_files==set(files)|{'PUBLICATION_MANIFEST.json'},'file inventory mismatch');need(actual_dirs==dirs,'directory inventory mismatch')
    for n,s in files.items():
        b=(root/n).read_bytes();need(set(s)=={'bytes','sha256'} and type(s['bytes']) is int,'member schema');need(len(b)==s['bytes'] and digest(b)==s['sha256'],'member mismatch: '+n)
    return len(actual_files)
def zip_match(path,root):
    expected={p.name for p in root.iterdir()}
    with zipfile.ZipFile(path) as z:
        names=z.namelist();need(len(names)==len(set(names)) and set(names)==expected,'ZIP inventory mismatch')
        for i in z.infolist():
            n=i.filename;need('/' not in n and '\\' not in n and n not in ('','.','..'),'unsafe ZIP name');need(not i.is_dir() and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG),'nonregular ZIP member');need(z.read(n)==(root/n).read_bytes(),'ZIP member mismatch')
    return len(names)
def inner(root,pin,schema):
    b=(root/'MANIFEST.json').read_bytes();need(digest(b)==pin,'inner manifest pin');m=json.loads(b);need(m['schema']==schema,'inner schema')
    entries=m['files'];names=[x['path'] for x in entries];need(names==sorted(set(names)),'inner repeated member');need(set(names)=={p.name for p in root.iterdir()}-{'MANIFEST.json'},'inner inventory')
    for x in entries:
        b=(root/x['path']).read_bytes();need(len(b)==x['bytes'] and digest(b)==x['sha256'],'inner member mismatch')
def patch_check(root):
    patch=root/'independent_audit/corrections.patch';before=(root/'author/STATEMENT_AND_SOURCES.md').read_bytes()
    lines=patch.read_bytes().splitlines(keepends=True)
    removed=[x[1:] for x in lines if x.startswith(b'-') and not x.startswith(b'---')];added=[x[1:] for x in lines if x.startswith(b'+') and not x.startswith(b'+++')]
    need(len(removed)==len(added)==1 and before.count(removed[0])==1,'correction patch shape')
    expected=before.replace(removed[0],added[0]);need(b'overline{C_d}' in added[0] and b'PDE sufficiency' in added[0] and b'necessity for PDE preservation separately conjectural' in added[0],'closure clarification missing')
    with tempfile.TemporaryDirectory(prefix='ricci patch check ') as d:
        p=Path(d);shutil.copyfile(root/'author/STATEMENT_AND_SOURCES.md',p/'STATEMENT_AND_SOURCES.md')
        for args in [['git','apply','--check',str(patch)],['git','apply',str(patch)]]:
            r=subprocess.run(args,cwd=p,capture_output=True);need(r.returncode==0,'actual patch application failed: '+r.stderr.decode())
        need((p/'STATEMENT_AND_SOURCES.md').read_bytes()==expected,'unexpected correction patch result');need({q.name for q in p.iterdir()}=={'STATEMENT_AND_SOURCES.md'},'patch wrote unexpected file')
    need((root/'author/STATEMENT_AND_SOURCES.md').read_bytes()==before,'author freeze changed')
    return digest(expected)
def replay(root,folder,script,result):
    args=[sys.executable,'-I','-B']+(['-O'] if sys.flags.optimize else [])+[str(root/folder/script)]
    r=subprocess.run(args,cwd=root.parent,capture_output=True,timeout=300);need(r.returncode==0,'replay failed: '+r.stderr.decode());need(r.stdout==(root/folder/result).read_bytes(),'exact replay output mismatch');return json.loads(r.stdout)
def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True);a=p.parse_args();invoked=Path(__file__).absolute();root=invoked.parent
    try:
        regular(invoked);count=check_manifest(root,a.expected_manifest);s=json.loads((root/'PUBLICATION_STATUS.json').read_bytes())
        need(s['problem_id']==30000789 and s['status']=='unsolved' and s['turns_used']==s['turn_limit']==5 and s['threshold_solved'] is False,'target disposition')
        for n,x in s['archives'].items():
            b=(root/'archives'/n).read_bytes();need(len(b)==x['bytes'] and digest(b)==x['sha256'],'archive pin mismatch')
        ac=zip_match(root/'archives'/s['author_archive'],root/'author');uc=zip_match(root/'archives'/s['audit_archive'],root/'independent_audit');need(ac==16 and uc==12,'archive counts')
        need((root/'independent_audit/AUTHOR_FREEZE.zip').read_bytes()==(root/'archives'/s['author_archive']).read_bytes(),'nested freeze differs')
        inner(root/'author',s['author_manifest_sha256'],'ricci-dimension-30000789-v1');inner(root/'independent_audit',s['audit_manifest_sha256'],'ricci-dimension-independent-audit-v1')
        corrected_hash=patch_check(root);ar=replay(root,'author','math_check.py','results.json');ir=replay(root,'independent_audit','independent_check.py','independent_results.json')
        need(ar['checks']==85363 and ar['negative_controls_rejected']==5,'author counts');need(ir['checks']==69 and len(ir['negative_controls_rejected'])==4,'independent counts')
        print(json.dumps({'status':'PASS_PUBLICATION_INTEGRITY_AND_REPLAY','problem_id':30000789,'target_status':'unsolved','turns_used':5,'files_verified':count,'publication_manifest_sha256':a.expected_manifest,'author_archive_members':ac,'audit_archive_members':uc,'author_exact_checks':85363,'independent_named_checks':69,'mandatory_correction_S1_actual_patch_application':'PASS','corrected_statement_sha256':corrected_hash,'scope':'Scoped partial results and transport; global threshold remains unproved.'},sort_keys=True,indent=2));return 0
    except Exception as e:print('REJECT: '+str(e),file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())
