#!/usr/bin/env python3
"""Fail-closed replay of the final-v3 literal disproof and two final audits."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, re, stat, subprocess, sys, tempfile
EXPECTED_MANIFEST='e5748a840564410c91e0c4268415a802401a642f7b484494d9e0daa8831160cb'
AUTHOR_MANIFEST='abc975e091ff72d9b020f238ef4ff7884a4ce9c0ed755b34f45626c1ef74158c'
AUTHOR_BOOTSTRAP='301e0c33f5eafccb1701687ae9cfbd574496b0ef1fd357bb4c4efe728c2379fa'
PROOF='ef2895590a3f7a32fe87e391fce50860df2f61c55c46e1732d6f934928017762'
class Reject(Exception):pass
def need(c,m):
    if not c:raise Reject(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(ps):
    d={}
    for k,v in ps:
        need(k not in d,'duplicate JSON key');d[k]=v
    return d
def nonfinite(x):raise Reject('nonfinite JSON constant')
def load(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=nonfinite)
def safe(n):return type(n) is str and bool(n) and '\\' not in n and not n.startswith('/') and all(x not in ('','.','..') for x in n.split('/'))
def inventory(root):
    need(not root.is_symlink() and root.is_dir(),'root must be a nonsymlink directory')
    files={};dirs=set()
    def visit(d,prefix):
        for e in os.scandir(d):
            n=prefix+e.name;mode=e.stat(follow_symlinks=False).st_mode
            need(not stat.S_ISLNK(mode),'symlink: '+n)
            if stat.S_ISDIR(mode):dirs.add(n);visit(Path(e.path),n+'/')
            else:
                need(stat.S_ISREG(mode),'nonregular member: '+n)
                need(e.stat(follow_symlinks=False).st_size<=2000000,'oversized member: '+n)
                files[n]=Path(e.path).read_bytes()
    visit(root,'');return files,dirs
def authenticate(root):
    f,dirs=inventory(root);need('PUBLICATION_MANIFEST.json' in f,'missing manifest')
    raw=f['PUBLICATION_MANIFEST.json'];need(sha(raw)==EXPECTED_MANIFEST,'manifest trust anchor')
    m=load(raw);need(type(m) is dict and set(m)=={'schema','problem_id','rank','status','resolution','approaches','files'},'manifest schema')
    for k,v in [('schema','habiro-publication-manifest-v1'),('problem_id',10400145),('rank',1010),('status','claimed_solved'),('resolution','negative_literal_statement'),('approaches',1)]:
        need(type(m[k]) is type(v) and m[k]==v,'manifest identity: '+k)
    need(type(m['files']) is list and bool(m['files']),'manifest files')
    expected={'PUBLICATION_MANIFEST.json','VERIFY_PUBLICATION.py','BOOTSTRAP.py'}
    for e in m['files']:
        need(type(e) is dict and set(e)=={'path','bytes','sha256'},'entry schema')
        n=e['path'];need(safe(n) and n not in expected,'unsafe or duplicate path');expected.add(n)
        need(n in f,'missing: '+n)
        need(type(e['bytes']) is int and e['bytes']>=0 and e['bytes']==len(f[n]),'byte count: '+n)
        need(type(e['sha256']) is str and re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None and sha(f[n])==e['sha256'],'hash: '+n)
    need(set(f)==expected,'file inventory mismatch')
    need(dirs=={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'},'directory inventory mismatch')
    need(f['VERIFY_PUBLICATION.py']==Path(__file__).read_bytes(),'different verifier copy')
    return f
def inner(f,manifest,prefix,extra):
    m=load(f[manifest]);seen=set(extra)
    for e in m['files']:
        n=prefix+e['path'];need(safe(n) and n not in seen,'inner unsafe or duplicate path');seen.add(n)
        need(type(e['bytes']) is int and len(f[n])==e['bytes'] and sha(f[n])==e['sha256'],'inner binding')
    need({n for n in f if n.startswith(prefix)}==seen,'inner inventory')
    return len(seen)
def semantics(f):
    pins={'author_v3/AUTHOR_MANIFEST.json':AUTHOR_MANIFEST,'author_v3/bootstrap.py':AUTHOR_BOOTSTRAP,'author_v3/packet/PROOF_AND_STATUS.md':PROOF,'FINAL_AUDIT_MANIFEST.json':'2ba36792f0aabd6afc082e3b70e0327d2018c3640715834e3dc32c2276a14aa9','SOURCE_BRIDGE_AUDIT_MANIFEST.json':'2c99bfa0fef6a10bdd723c8908af998dde0a6bae452f1542c303d1a13c9263cb','REPLAY_CONTROLS.json':'d8dfa72218d7ee2729c2819860f3ec14121ac12e1d5bce7db3440eefe14c20b2'}
    for n,h in pins.items():need(sha(f[n])==h,'accepted frozen pin: '+n)
    counts=[inner(f,'author_v3/AUTHOR_MANIFEST.json','author_v3/packet/',set()),inner(f,'FINAL_AUDIT_MANIFEST.json','audit_algebra/',set()),inner(f,'SOURCE_BRIDGE_AUDIT_MANIFEST.json','audit_source_bridge/',set())]
    need(counts==[9,4,6],'accepted payload counts')
    need(len([n for n in f if n.startswith('author_v3/')])==11,'author freeze count')
    a=load(f['audit_algebra/ACCEPTANCE.json']);b=load(f['audit_source_bridge/ACCEPTANCE.json']);c=load(f['author_v3/packet/CLAIMS.json'])
    for x in (a,b):
        need(type(x['problem_id']) is int and x['problem_id']==10400145 and type(x['rank']) is int and x['rank']==1010,'audit identity')
        need(x['accepted_author_manifest_sha256']==AUTHOR_MANIFEST and x['accepted_author_bootstrap_sha256']==AUTHOR_BOOTSTRAP,'audit author binding')
    need(a['verdict']=='accepted_negative_literal_statement' and a['full_original_scope'] is True,'audit one disposition')
    need(a['accepted_author_proof_sha256']==PROOF and a['mathematical_gaps_found']==[] and a['mathematical_patches_required']==[],'audit one proof')
    for k in ['formal_verification_claim','human_referee_claim','novelty_claim']:need(a[k] is False,'audit one claim limit')
    need(b['decision']=='ACCEPT' and b['resolution']=='negative_literal_statement' and b['remaining_blockers']==[] and b['mathematical_corrections_required'] is False and b['independent_full_proof_review'] is True,'audit two disposition')
    need(c['status']=='claimed_solved' and c['resolution']=='negative_literal_statement' and type(c['approaches_used']) is int and c['approaches_used']==1 and c['full_original_scope'] is True,'author disposition')
    for k in ['formal_verification_claim','human_review_claim','novelty_claim']:need(c[k] is False,'author claim limit')
    return {'accepted_author_files':11,'final_algebra_audit_files':4,'final_source_bridge_audit_files':6,'accepted_proof_sha256':PROOF,'mathematical_correction_required':False}
def invoke(root,script,*args):
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    p=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/script),*map(str,args)],cwd=root,capture_output=True,timeout=240)
    need(p.returncode==0 and not p.stderr,'replay failed '+script+': '+p.stderr.decode('utf8','replace'))
    return load(p.stdout)
def primary(f,a):
    out={'sources':'NOT_RUN','corpora':'NOT_RUN','fresh_source_inspection':'NOT_RUN','fresh_download':'NOT_RUN','fresh_record_join':'NOT_RUN'}
    def match(p,e):
        need(not p.is_symlink() and p.is_file(),'missing or symlink optional input')
        raw=p.read_bytes();need((len(raw),sha(raw))==(e['bytes'],e['sha256']),'optional input mismatch')
        return {'bytes':len(raw),'sha256':sha(raw)}
    if a.source_dir is not None:
        names={'O':'ohtsuki2002.pdf','L':'le_psu_author.pdf','HL':'habiro_le_v2.pdf','LQ':'le_quantum.pdf','H':'habiro2008.pdf','L-preprint':'le_psu.pdf','HL-older':'habiro_le.pdf','BG':'beliakova_gorsky.pdf','HL-published':'habiro_le_published.pdf'}
        out['source_matches']=[{'id':e['id'],**match(a.source_dir/names[e['id']],e)} for e in load(f['author_v3/packet/SOURCE_METADATA.json'])['sources']]
        need(len(out['source_matches'])==9,'source count');out['sources']='PASS_CURRENT_BYTE_REHASH'
    if a.problems is not None:
        out['corpus_matches']=[{'name':e['name'],**match(p,e)} for p,e in zip([a.problems,a.research_results],load(f['CORPUS_VERIFICATION.json'])['datasets'])]
        need(len(out['corpus_matches'])==2,'corpus count');out['corpora']='PASS_CURRENT_BYTE_REHASH'
    return out
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--integrity-only',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--problems',type=Path);p.add_argument('--research-results',type=Path);a=p.parse_args()
    need((a.problems is None)==(a.research_results is None),'both complete corpus inputs required')
    need(not a.integrity_only or (a.source_dir is None and a.problems is None),'optional inputs require full replay')
    root=a.root.absolute();before=authenticate(root);report=semantics(before)
    if a.integrity_only:return {'status':'PASS_PUBLICATION_INTEGRITY','problem_id':10400145,**report}
    need(os.geteuid()!=0,'full replay requires an unprivileged account')
    author=root/'author_v3'
    baseline=invoke(root,'author_v3/bootstrap.py',author/'packet');need(baseline['status']=='PASS' and baseline['files']==9,'author replay result')
    audit=invoke(root,'audit_algebra/audit_controls.py',author)
    need(audit['status']=='PASS' and len(audit['negative_controls'])==15 and all(c['rejected'] is True for c in audit['negative_controls']) and audit['hostile_import_control'] is True and audit['author_originals_unchanged'] is True,'audit algebra replay result')
    need(audit['source_checks']==[],'unexpected source rehash in source-free audit')
    with tempfile.TemporaryDirectory(prefix='habiro-publication-') as tmp:
        receipt=Path(tmp)/'replay.json'
        bridge=invoke(root,'audit_source_bridge/run_audit.py',author,AUTHOR_MANIFEST,AUTHOR_BOOTSTRAP,receipt)
        r=load(receipt.read_bytes())
        need(bridge['status']=='PASS' and bridge['controls']==72 and r['control_count']==72 and r['author_bytes_unchanged'] is True,'source bridge replay result')
        need(r['write_denied_probe'] is True and type(r['write_denied_errno']) is int and r['write_denied_errno']==30,'read-only enforcement')
        need(len(r['read_only'])==3 and len(r['algebra_read_only'])==3 and len(r['baseline'])==3 and len(r['algebra'])==3,'source bridge mode matrix')
        need(all(c.get('rejected') is True or c.get('expected_pass') is True for c in r['controls']),'source bridge controls')
    report['replay']={'author':'PASS','algebra_audit_negative_controls':15,'bridge_controls':72,'read_only_write_denied_errno':30,'all_three_modes_in_each_audit':True,'finite_math':audit['math']}
    report['optional_inputs']=primary(before,a)
    need(authenticate(root)==before,'input bytes changed')
    return {'schema':'habiro-publication-replay-v1','status':'PASS_LITERAL_DISPROOF_REPLAY','problem_id':10400145,'rank':1010,'disposition':'claimed_solved','approaches':1,'resolution':'negative_literal_statement','formal_proof':False,'human_peer_review':False,'novelty_claim':False,'github_ci':False,'publication_manifest_sha256':EXPECTED_MANIFEST,**report}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True))
    except (Reject,OSError,ValueError,KeyError,TypeError,UnicodeError,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
