#!/usr/bin/env python3
"""Fail-closed source-free replay. Authenticate through externally pinned BOOTSTRAP.py."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, io, json, os, re, stat, subprocess, sys, tempfile, zipfile
EXPECTED_MANIFEST='70776b44c1e86111fa457d5b4ac0001c511866efcd5507b0e155818a2976031b'
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
    need(m['schema']=='fixed-span-publication-manifest-v1','manifest version')
    for key,value in [('problem_id',10400013),('rank',1009),('disposition','unsolved'),('approaches',5)]:
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
    pins={'author_original/AUTHOR_MANIFEST.json':(1470,'a8e8ce66abc1366122e72cd8086b9cba999e04e05b9f8d1b7b41111d3a2fbcd6'),'author_original/bootstrap.py':(3282,'152ab44196e87e7660de8b4c16faf2c1475b5416c83fd3fdfbc520f57660e4ef'),'author_original/test_bootstrap.py':(6946,'011f4a4e76bcd40b0aa1fe79163f116d7d28df03c28468e3f315b69bf626c114'),'author_original/packet/PROOF.md':(17400,'90f3e9bd8283230ad00937cbbe2574b44b0bc332f9cfc6a54bbfb2dcb36c7d12'),'audit/AUDIT_MANIFEST.json':(4287,'3ad8e7d10f4cd2aaa86dfae48e973642515bcc7c01c8b76ea01e4a3264781d3b'),'archives/AUTHOR_FREEZE.zip':(24812,'49798e2b582bf9565bd729f8b83ed25939377fc46fe72ce6c5e402cea71ec626'),'archives/AUDIT_FREEZE.zip':(51149,'6882e34ff72553e137bc3508b5c5c347b1fef79161da8a39741adc21badef319'),'audit/corrected_freeze/AUTHOR_MANIFEST.json':(1470,'32340d733f2fec7dc01d00c39a96767e69dfc2509be1b6c309461e40bb9fc251'),'audit/corrected_freeze/packet/verify.py':(9608,'695f62f0a39034c2d083b3ddbea89634917728fa4f3d2df995a544a53cee3a2b')}
    for n,pin in pins.items():need((len(f[n]),sha(f[n]))==pin,'external frozen pin: '+n)
    author={n.removeprefix('author_original/'):b for n,b in f.items() if n.startswith('author_original/')}
    audit={n.removeprefix('audit/'):b for n,b in f.items() if n.startswith('audit/')}
    corrected={n.removeprefix('corrected_freeze/'):b for n,b in audit.items() if n.startswith('corrected_freeze/')}
    ac=archive_members(f['archives/AUTHOR_FREEZE.zip'],author)
    rc=archive_members(f['archives/AUDIT_FREEZE.zip'],audit)
    need(ac==12 and rc==26 and len(corrected)==12,'frozen member counts')
    for members,name,prefix,extra in [(author,'AUTHOR_MANIFEST.json','packet/',{'AUTHOR_MANIFEST.json','bootstrap.py','test_bootstrap.py'}),(corrected,'AUTHOR_MANIFEST.json','packet/',{'AUTHOR_MANIFEST.json','bootstrap.py','test_bootstrap.py'}),(audit,'AUDIT_MANIFEST.json','',{'AUDIT_MANIFEST.json'})]:
        m=load(members[name]);expected=set(extra)
        for e in m['files']:
            n=prefix+e['path'];need(safe(n) and n not in expected,'inner duplicate or unsafe path');expected.add(n)
            need(type(e['bytes']) is int and e['bytes']==len(members[n]) and e['sha256']==sha(members[n]),'inner manifest binding')
        need(set(members)==expected,'inner manifest inventory')
    need(author['packet/PROOF.md']==corrected['packet/PROOF.md'],'mathematical proof changed')
    need(set(author)==set(corrected),'correction member inventory')
    changed=sorted(n for n in author if author[n]!=corrected[n])
    need(changed==['AUTHOR_MANIFEST.json','bootstrap.py','packet/verify.py'],'unexpected correction scope')
    cm=load(audit['CORRECTED_MANIFEST.json'])
    need(set(cm['files'])==set(corrected),'corrected manifest inventory')
    for n,b in corrected.items():need(cm['files'][n]=={'bytes':len(b),'sha256':sha(b)},'corrected byte binding')
    a=load(audit['ACCEPTANCE.json']);claims=load(author['packet/CLAIMS.json'])
    need(a['decision']=='ACCEPT_SCOPED_PARTIAL_RESULTS_WITH_VERIFIER_CORRECTION' and a['status']=='unsolved' and type(a['approaches']) is int and a['approaches']==5,'acceptance disposition')
    for n in ['full_resolution','knot_counterexample','formal_specialization_families_realized','human_peer_review_claimed','novelty_certified','mathematical_corrections_required','source_dependent_theorems_reproved_from_first_principles']:need(a[n] is False,'acceptance limit: '+n)
    for n in ['proof_text_unchanged','implementation_correction_required_and_applied','independent_mathematical_review_completed','fixed_two_strand_exterior_required','same_adequate_diagram_genus_required','bounded_braid_index_theorem_accepted','link_jones_counterexample_credited']:need(a[n] is True,'accepted qualification: '+n)
    need(a['link_counterexample_components']==2 and a['link_counterexample_span']==2,'link scope')
    need(a['general_knot_clauses_unresolved_by_attempt']==['Jones','Q','skein/HOMFLY','Kauffman'],'remaining clauses')
    need(claims['independent_audit_completed'] is False and claims['full_resolution'] is False and claims['status']=='unsolved','historical author scope')
    need(claims['approaches']==5 and claims==load(corrected['packet/CLAIMS.json']),'historical author claims preserved')
    return {'author_archive_members':ac,'audit_archive_members':rc,'corrected_freeze_members':len(corrected),'original_mathematics_unchanged':True,'correction_changed_paths':changed,'audit_scope':a['decision']}

def invoke(root,script,*args):
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    c=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/script),*map(str,args)],cwd=root,capture_output=True,timeout=600)
    need(c.returncode==0 and not c.stderr,'replay failed '+script+': '+c.stderr.decode('utf8','replace'))
    return load(c.stdout)

def permissions(root,readonly):
    if not readonly:root.chmod(0o755)
    for p in root.rglob('*'):p.chmod((0o555 if p.is_dir() else 0o444) if readonly else (0o755 if p.is_dir() else 0o644))
    root.chmod(0o555 if readonly else 0o755)

def primary_rehash(f,a):
    ids=load(f['author_original/packet/SOURCE_IDENTITIES.json']);result={'sources':'NOT_RUN','corpora':'NOT_RUN','record_join':'NOT_RUN'}
    if a.source_dir is not None:
        matches=[]
        for e in ids['public_pdf_sources']:
            p=a.source_dir/(e['id']+'.pdf');need(p.is_file() and not p.is_symlink(),'missing or symlink PDF input')
            b=p.read_bytes();need((len(b),sha(b))==(e['bytes'],e['sha256']),'PDF bytes mismatch: '+e['id']);matches.append({'id':e['id'],'bytes':len(b),'sha256':sha(b)})
        result['sources']='PASS_CURRENT_REHASH';result['source_matches']=matches
    if a.problems is not None:
        matches=[]
        for p,e in zip([a.problems,a.research_results],ids['catalog_inputs']):
            need(p.is_file() and not p.is_symlink(),'missing or symlink corpus input')
            b=p.read_bytes();need((len(b),sha(b))==(e['bytes'],e['sha256']),'corpus bytes mismatch: '+e['name']);matches.append({'name':e['name'],'bytes':len(b),'sha256':sha(b)})
        result['corpora']='PASS_CURRENT_REHASH';result['corpus_matches']=matches
        # Whole-corpus byte identity is checked here; historical record joins are
        # preserved in SOURCE_READBACK.json, not advertised as freshly rerun.
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--integrity-only',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--problems',type=Path);p.add_argument('--research-results',type=Path);a=p.parse_args()
    need((a.problems is None)==(a.research_results is None),'both complete corpus inputs required')
    need(not a.integrity_only or (a.source_dir is None and a.problems is None),'optional inputs require full replay')
    root=a.root.absolute();before=authenticate(root);report=semantics(before)
    if a.integrity_only:return {'status':'PASS_PUBLICATION_INTEGRITY','problem_id':10400013,**report}
    need(os.geteuid()!=0,'full replay requires unprivileged execution for enforced read-only tests')
    with tempfile.TemporaryDirectory(prefix='fixed-span-publication-') as tmp:
        work=Path(tmp)
        for n,b in before.items():q=work/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
        original=work/'author_original';corrected=work/'audit/corrected_freeze';patched=work/'patched'
        import shutil
        shutil.copytree(original,patched)
        patch=subprocess.run(['patch','--batch','--forward','--fuzz=0','-p1','-i',str(work/'audit/CORRECTION.patch')],cwd=patched,capture_output=True,timeout=30)
        need(patch.returncode==0 and not patch.stderr and b'offset' not in patch.stdout and b'fuzz' not in patch.stdout,'actual correction patch replay failed')
        need(inventory(patched)==inventory(corrected),'actual patch does not reproduce corrected freeze')
        report['actual_patch_replay']='PASS_EXACT_ALL_12_MEMBERS'
        for r in (original,corrected):permissions(r,True)
        try:
            controls=[]
            for label,r in [('original',original),('corrected',corrected)]:
                result=invoke(work,r.relative_to(work).as_posix()+'/test_bootstrap.py')
                need(result['status']=='PASS' and result['positive_count']==6 and result['negative_count']==78 and result['semantic_negative_count']==45,'author controls changed')
                need(result['read_only_write_denied'] is True,'read-only author control failed')
                controls.append({'layout':label,'positive_replays':6,'integrity_rejections':78,'semantic_rejections':45})
            independent=invoke(work,'audit/independent_checks.py',original,corrected)
            need(independent['status']=='PASS' and independent['checks']==57250 and independent['original_float_regression_cases']==6,'independent exact replay')
            need(independent['negative_replay_count']==99 and len(independent['positive_replays'])==9,'independent controls changed')
            need(independent['both_freezes_unchanged'] is True and independent['read_only_write_denied'] is True,'independent input integrity')
            report['author_controls']=controls
            report['independent_checks']={'checks':independent['checks'],'categories':independent['categories'],'negative_replays':99,'positive_replays':9,'original_float_regression_cases':6,'read_only_write_denied':True,'both_freezes_unchanged':True}
        finally:
            for r in (original,corrected):permissions(r,False)
        report['primary_rehash']=primary_rehash(before,a)
    need(authenticate(root)==before,'input bytes changed')
    return {'schema':'fixed-span-publication-replay-v1','status':'PASS_SCOPED_PUBLICATION','problem_id':10400013,'rank':1009,'disposition':'unsolved','approaches':5,'full_resolution':False,'knot_counterexample':False,'formal_proof':False,'github_ci':False,'source_free_default':a.source_dir is None and a.problems is None,'publication_manifest_sha256':EXPECTED_MANIFEST,**report}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True))
    except (Reject,OSError,ValueError,KeyError,TypeError,UnicodeError,subprocess.SubprocessError,zipfile.BadZipFile) as exc:
        print('REJECT: '+str(exc),file=sys.stderr);sys.exit(1)
