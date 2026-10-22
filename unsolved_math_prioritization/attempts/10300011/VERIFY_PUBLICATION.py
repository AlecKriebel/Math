#!/usr/bin/env python3
"""Fail-closed source-free replay. Authenticate through externally pinned BOOTSTRAP.py."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, io, json, os, re, stat, subprocess, sys, tempfile, zipfile
EXPECTED_MANIFEST='d6baefe7e479d1b1859e183e7ec59b258bf999782e4b142899908dbcb8af225c'
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
    need(m['schema']=='sublamination-publication-manifest-v1','manifest version')
    for key,value in [('problem_id',10300011),('rank',1004),('disposition','unsolved'),('approaches',5)]:
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

def semantics(f):
    pins={'author_original/MANIFEST.json':(1941,'93febcc968a3b244c9cdee7af00fb1ce24519ef03582039cd6b68c2733aab3ae'),'author_original/bootstrap.py':(3011,'7ad7d12073e58e60d33966770689af7dbe7193adfcb5cde38b63f41bc30133c5'),'author_original/author/PROOF.md':(19499,'72186bfc50394149ac96404dda56da480a0f6791f236688c5417f4f7f8bb85d1'),'audit/AUDIT_MANIFEST.json':(1457,'15383c158f59f7678b467781fdba7b9be52bcf629ec354aca862e5cfac02f1e0'),'archives/AUTHOR_V1.zip':(24189,'84795261940f05abad6f2b6208cc0558fde23beeb77ab735c607bac9fcb846a8'),'archives/AUDIT_V1.zip':(20123,'7950ecc8d0da23d87e310710883668711d5e8dff1a92de75a4fd5cb37694d7c3')}
    for n,pin in pins.items():need((len(f[n]),sha(f[n]))==pin,'original external pin: '+n)
    author={n.removeprefix('author_original/'):b for n,b in f.items() if n.startswith('author_original/')}
    audit={n.removeprefix('audit/'):b for n,b in f.items() if n.startswith('audit/')}
    ac=archive_members(f['archives/AUTHOR_V1.zip'],author)
    rc=archive_members(f['archives/AUDIT_V1.zip'],{'audit_v1/'+n:b for n,b in audit.items()})
    subject=load(audit['REVIEWED_SUBJECT.json'])
    need(subject['inventory']=={n:{'bytes':len(b),'sha256':sha(b)} for n,b in author.items()},'reviewed subject mismatch')
    for members,name,extra in [(author,'MANIFEST.json',{'MANIFEST.json','bootstrap.py'}),(audit,'AUDIT_MANIFEST.json',{'AUDIT_MANIFEST.json'})]:
        m=load(members[name]);need(set(members)==set(m['files'])|extra,'inner manifest inventory')
        for n,pin in m['files'].items():need(pin=={'bytes':len(members[n]),'sha256':sha(members[n])},'inner manifest binding')
    a=load(audit['ACCEPTANCE.json']);claims=load(author['author/CLAIMS.json'])
    need(a['decision']=='ACCEPTED_SCOPED_UNSOLVED_REPORT' and a['status']=='unsolved' and type(a['turns']) is int and a['turns']==5,'acceptance scope')
    need(a['general_solution'] is False and a['post_freeze_author_changes'] is False and a['acceptance_blockers']==[],'acceptance limits')
    need(claims['independent_review']=='pending' and claims['general_solution'] is False and claims['status']=='unsolved','historical author disposition')
    need(a['accepted_claims']==claims['claim_ids'],'accepted claim IDs')
    return {'author_archive_members':ac,'audit_archive_members':rc,'original_mathematics_unchanged':True,'post_freeze_correction':False}

def invoke(root,script,*args):
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    c=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/script),*map(str,args)],cwd=root,capture_output=True,timeout=240)
    need(c.returncode==0 and not c.stderr,'replay failed '+script+': '+c.stderr.decode('utf8','replace'))
    return load(c.stdout)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--integrity-only',action='store_true');p.add_argument('--sources-dir',type=Path);p.add_argument('--corpora-dir',type=Path);a=p.parse_args()
    need(not a.integrity_only or (a.sources_dir is None and a.corpora_dir is None),'optional inputs require full replay')
    root=a.root.absolute();before=authenticate(root);report=semantics(before)
    if a.integrity_only:return {'status':'PASS_PUBLICATION_INTEGRITY','problem_id':10300011,**report}
    with tempfile.TemporaryDirectory(prefix='sublamination-publication-') as tmp:
        work=Path(tmp)
        for n,b in before.items():q=work/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
        author=invoke(work,'author_original/bootstrap.py');need(author['status']=='PASS_AUTHENTICATED_AUTHOR_BOUNDARY','author bootstrap status')
        controls=invoke(work,'author_original/author/controls.py');need(controls['status']=='PASS_ADVERSARIAL_CONTROLS' and controls['positive_subprocesses']==6 and controls['rejected_subprocesses']==78,'author controls')
        boundary=invoke(work,'author_original/author/boundary_controls.py');need(boundary['positive_relocated_runs']==3 and boundary['rejected_mutated_runs']==39,'author boundary')
        independent=invoke(work,'audit/independent_controls.py','--subject',work/'author_original');need(independent['status']=='PASS_INDEPENDENT_SCOPED_AUDIT' and independent['positive_subprocesses']==6 and independent['malformed_subprocesses_rejected']==60 and independent['sources_checked'] is False and independent['corpora_checked'] is False,'independent controls')
        ib=invoke(work,'audit/independent_boundary_controls.py','--subject',work/'author_original');need(ib['accepted_exact_copies']==3 and ib['rejected_mutated_copies']==45 and ib['untrusted_marker_executed'] is False,'independent boundary')
        primary={'sources':'NOT_SUPPLIED_NOT_RECHECKED','corpora':'NOT_SUPPLIED_NOT_RECHECKED'}
        if a.sources_dir is not None or a.corpora_dir is not None:
            args=[]
            if a.sources_dir is not None:args+=['--sources-dir',a.sources_dir.absolute()]
            if a.corpora_dir is not None:args+=['--corpora-dir',a.corpora_dir.absolute()]
            actual=invoke(work,'author_original/author/verify.py',*args)
            if a.sources_dir is not None:need(actual.get('source_files_matched')==6,'source match count');primary['sources']='PASS_CURRENT_REHASH'
            if a.corpora_dir is not None:need(actual.get('corpora_matched')=={'problems':15458,'research_results':6701,'selected_record_matches':1},'corpus match result');primary['corpora']='PASS_CURRENT_REHASH'
        report.update(author=author,author_controls=controls,author_boundary=boundary,independent=independent,independent_boundary=ib,primary_rehash=primary)
    need(authenticate(root)==before,'input bytes changed')
    return {'schema':'sublamination-publication-replay-v1','status':'PASS_SCOPED_PUBLICATION','problem_id':10300011,'rank':1004,'disposition':'unsolved','approaches':5,'general_solution':False,'formal_topological_proof':False,'github_ci':False,'source_free_default':True,'publication_manifest_sha256':EXPECTED_MANIFEST,**report}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True))
    except (Reject,OSError,ValueError,KeyError,TypeError,UnicodeError,subprocess.SubprocessError,zipfile.BadZipFile) as exc:
        print('REJECT: '+str(exc),file=sys.stderr);sys.exit(1)
