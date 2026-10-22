#!/usr/bin/env python3
"""Fail-closed source-free replay. Authenticate through externally pinned BOOTSTRAP.py."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, io, json, os, re, stat, subprocess, sys, tempfile, zipfile
EXPECTED_MANIFEST='92b3a6cb4ab3efa4bdded1cf4a55383c28aa4cec7c76aadfc0efe5d0170c79af'
class Reject(Exception): pass
def need(c,m):
    if not c: raise Reject(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def pairs(ps):
    d={}
    for k,v in ps:
        need(k not in d,'duplicate JSON key');d[k]=v
    return d
def nonfinite(x): raise Reject('nonfinite JSON constant')
def load(b): return json.loads(b,object_pairs_hook=pairs,parse_constant=nonfinite)
def safe(n): return type(n) is str and n!='' and '\\' not in n and not n.startswith('/') and all(x not in ('','.','..') for x in n.split('/'))
def inventory(root):
    need(not root.is_symlink() and root.is_dir(),'root symlink or not directory')
    out={};dirs=set()
    def visit(d,prefix):
        for e in os.scandir(d):
            name=prefix+e.name;mode=e.stat(follow_symlinks=False).st_mode
            need(not stat.S_ISLNK(mode),'symlink: '+name)
            if stat.S_ISDIR(mode): dirs.add(name);visit(Path(e.path),name+'/')
            else:
                need(stat.S_ISREG(mode),'nonregular member: '+name);out[name]=Path(e.path).read_bytes()
    visit(root,'');return out,dirs

def authenticate(root):
    f,dirs=inventory(root);need('PUBLICATION_MANIFEST.json' in f,'missing manifest')
    raw=f['PUBLICATION_MANIFEST.json'];need(sha(raw)==EXPECTED_MANIFEST,'manifest external pin')
    m=load(raw);need(type(m) is dict and set(m)=={'schema','problem_id','rank','disposition','approaches','files'},'manifest schema')
    need(m['schema']=='even-sided-publication-manifest-v1','manifest version')
    for key,value in [('problem_id',10300037),('rank',1006),('disposition','unsolved'),('approaches',5)]:
        need(type(m[key]) is type(value) and m[key]==value,'manifest identity or scope: '+key)
    need(type(m['files']) is list and m['files'],'manifest files')
    expected={'PUBLICATION_MANIFEST.json','VERIFY_PUBLICATION.py','BOOTSTRAP.py'}
    for e in m['files']:
        need(type(e) is dict and set(e)=={'path','bytes','sha256'},'entry schema');n=e['path']
        need(safe(n) and n not in expected,'unsafe or duplicate entry');expected.add(n)
        need(n in f,'missing: '+n)
        need(type(e['bytes']) is int and e['bytes']>=0 and len(f[n])==e['bytes'],'byte count: '+n)
        need(type(e['sha256']) is str and re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None and sha(f[n])==e['sha256'],'digest: '+n)
    need(set(f)==expected,'file inventory mismatch')
    need(dirs=={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'},'directory inventory mismatch')
    need(f['VERIFY_PUBLICATION.py']==Path(__file__).read_bytes(),'different verifier copy')
    return f

def archive_members(b,expected):
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        names=z.namelist();need(len(names)==len(set(names)) and set(names)==set(expected),'archive inventory')
        for i in z.infolist():
            need(safe(i.filename) and not i.is_dir(),'unsafe archive path')
            mode=i.external_attr>>16;need(not stat.S_ISLNK(mode) and stat.S_IFMT(mode) in (0,stat.S_IFREG),'archive type')
            need(z.read(i)==expected[i.filename],'archive member bytes')
    return len(expected)

def manifest_members(members,name,prefix=''):
    m=load(members[name]);entries=m['files'];need(type(entries) is list,'inner manifest entries')
    seen=set()
    for e in entries:
        n=prefix+e['path'];need(n not in seen and n in members,'inner inventory');seen.add(n)
        need(type(e['bytes']) is int and e['bytes']==len(members[n]) and e['sha256']==sha(members[n]),'inner binding: '+n)
    return seen

def semantics(f):
    pins={'author_original/AUTHOR_MANIFEST.json':'96b8d8549908ac7160ad9b57dcc1eb1b8d0ae5ed393b874d6e2d4e73c7dbc375',
          'author_original/bootstrap.py':'e28741d45e461a11e657c5e6f56e29edf8d19d86d47ac57d938f98007872debc',
          'archives/AUTHOR_V1.zip':'287834e445bf65b67a44dda04973ffcb4d3c23033ee589ae614fced3c4e4525b',
          'audit_original/AUDIT_MANIFEST.json':'ff79cdfc75ae3bdfbe7fcc5a40af33b650f13bc6ff21205c37a34083d6678a43',
          'archives/AUDIT_V1.zip':'b5ef0dea48610de3fb44e95f669db107057ff8e7252c027fd2d0fd3221b25a46',
          'audit_original/CORRECTIONS.patch':'c683d1219c00c641b5b6d49ff57b62078cec64e88a1b8ad7fc9af40df2f43716',
          'corrected/AUTHOR_MANIFEST.json':'642c64c2ddd8c735d7af8894aaaa4ef9085e7d29777e8b78364d1a0d1f3173ef',
          'corrected/packet/PROOF.md':'952c63482b8442a730d3ff3ac8896ba32e98ec550713e3fd87f6d36d19838dc0'}
    for n,pin in pins.items():need(sha(f[n])==pin,'original external pin: '+n)
    sets={key:{n.removeprefix(key+'/'):b for n,b in f.items() if n.startswith(key+'/')} for key in ('author_original','audit_original','corrected')}
    author,audit,corrected=[sets[k] for k in ('author_original','audit_original','corrected')]
    need(len(author)==15 and len(audit)==22 and len(corrected)==15,'snapshot sizes')
    ac=archive_members(f['archives/AUTHOR_V1.zip'],author);rc=archive_members(f['archives/AUDIT_V1.zip'],audit)
    need(len(f['archives/AUTHOR_V1.zip'])==29840 and len(f['archives/AUDIT_V1.zip'])==55009,'archive sizes')
    need(manifest_members(audit,'AUDIT_MANIFEST.json')|{'AUDIT_MANIFEST.json'}==set(audit),'audit inventory')
    need(manifest_members(audit,'CORRECTED_MANIFEST.json','corrected/')=={'corrected/'+n for n in corrected},'corrected inventory')
    for n,b in corrected.items():need(audit['corrected/'+n]==b,'separate corrected adoption mismatch')
    for members in (author,corrected):
        need(manifest_members(members,'AUTHOR_MANIFEST.json','packet/')=={n for n in members if n.startswith('packet/')},'author packet inventory')
    a=load(audit['AUDIT_RECEIPT.json']);claims=load(corrected['packet/CLAIMS.json'])
    need(a['decision']=='accept_corrected_scoped_unsolved_5_of_5' and a['status']=='unsolved' and type(a['turns']) is int and a['turns']==5,'acceptance scope')
    for key in ('universal_resolution','current_worldwide_openness_claim','formal_peer_review_claim','novelty_claim','universal_complete_proof_inspected'):need(a[key] is False,'acceptance limits')
    need(a['acceptance_blockers']==[] and a['universal_announcement_credited'] is True,'acceptance qualifications')
    need(claims['independent_review']=='accepted_after_corrections' and claims['status']=='unsolved','corrected disposition')
    for key in ('general_resolution','finite_checks_prove_topology','local_model_proves_global_essentiality','universal_complete_proof_inspected'):need(claims[key] is False,'corrected limits')
    need(claims['universal_announcement_credited'] is True,'announcement credited')
    return {'author_archive_members':ac,'audit_archive_members':rc,'corrected_members':len(corrected),'original_author_audit_bytes_unchanged':True,'accepted_version':'corrected_only'}

def invoke(root,script,*args):
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    c=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/script),*map(str,args)],cwd=root,capture_output=True,timeout=300)
    need(c.returncode==0 and not c.stderr,'replay failed '+script+': '+c.stderr.decode('utf8','replace'))
    return load(c.stdout)

def patch_replay(work,before):
    patched=work/'patch_replay';patched.mkdir()
    for n,b in before.items():
        if n.startswith('author_original/'):
            q=patched/n.removeprefix('author_original/');q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
    c=subprocess.run(['patch','--batch','--forward','--fuzz=0','-p1','-i',str(work/'audit_original/CORRECTIONS.patch')],cwd=patched,capture_output=True,timeout=60)
    need(c.returncode==0 and not c.stderr and b'offset' not in c.stdout and b'fuzz' not in c.stdout,'actual patch did not apply exactly')
    expected={n.removeprefix('corrected/'):b for n,b in before.items() if n.startswith('corrected/')}
    got,dirs=inventory(patched);need(got==expected,'actual patch reconstruction differs')
    need(dirs=={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'},'patched directory inventory differs')
    return {'status':'PASS_EXACT_PATCH_RECONSTRUCTION','files':len(got),'fuzz':0,'offsets':0}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--integrity-only',action='store_true');p.add_argument('--sources-dir',type=Path);p.add_argument('--corpora-dir',type=Path);a=p.parse_args()
    need((a.sources_dir is None)==(a.corpora_dir is None),'both optional directories required')
    need(not a.integrity_only or a.sources_dir is None,'optional inputs require full replay')
    root=a.root.absolute();before=authenticate(root);report=semantics(before)
    if a.integrity_only:return {'status':'PASS_PUBLICATION_INTEGRITY','problem_id':10300037,**report}
    with tempfile.TemporaryDirectory(prefix='even-sided-publication-') as tmp:
        work=Path(tmp)
        for n,b in before.items():q=work/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
        patch=patch_replay(work,before)
        original=invoke(work,'author_original/bootstrap.py');need(original['status']=='pass','original bootstrap')
        corrected=invoke(work,'corrected/bootstrap.py');need(corrected['status']=='pass','corrected bootstrap')
        reconstructed=invoke(work,'patch_replay/bootstrap.py');need(reconstructed==corrected,'reconstructed replay differs')
        controls=invoke(work,'corrected/test_bootstrap.py');need(controls['status']=='pass' and controls['positive_count']==6 and controls['negative_count']==84 and controls['mutation_case_count']==28,'corrected mutation controls')
        independent=invoke(work,'audit_original/independent_checks.py',work/'author_original',work/'corrected')
        need(independent['status']=='pass' and independent['finite_exact_model_controls']==6247 and independent['malformed_api_controls']==24 and len(independent['package_negative_runs'])==15 and len(independent['positive_runs'])==12,'independent controls')
        primary={'status':'NOT_RUN','reason':'Separately held source and corpus directories not supplied; historical receipts are not a fresh rehash.'}
        if a.sources_dir is not None:
            primary=invoke(work,'corrected/packet/verify_inputs.py',a.sources_dir.absolute(),a.corpora_dir.absolute())
            need(primary['status']=='pass' and primary['pdfs_and_extractions']==7 and primary['corpora']==2 and primary['matched_records']==2,'primary rehash counts')
        report.update(patch_replay=patch,original_bootstrap=original,corrected_bootstrap=corrected,corrected_controls=controls,independent=independent,primary_rehash=primary)
    need(authenticate(root)==before,'input bytes changed')
    return {'schema':'even-sided-publication-replay-v1','status':'PASS_SCOPED_PUBLICATION','problem_id':10300037,'rank':1006,'disposition':'unsolved','approaches':5,'status_scope':'unsolved by this packet, not worldwide openness','general_solution':False,'formal_topological_proof':False,'github_ci':False,'source_free_default':True,'publication_manifest_sha256':EXPECTED_MANIFEST,**report}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True))
    except (Reject,OSError,ValueError,KeyError,TypeError,UnicodeError,subprocess.SubprocessError,zipfile.BadZipFile) as exc:
        print('REJECT: '+str(exc),file=sys.stderr);sys.exit(1)
