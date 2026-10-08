#!/usr/bin/env python3
"""Fail-closed source-free replay. Authenticate through externally pinned BOOTSTRAP.py."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, io, json, os, re, stat, subprocess, sys, tempfile, zipfile
EXPECTED_MANIFEST='cbe331b23a13155d585e0da046c4bdff4079404ac216e7d60ca13c4285c8b445'
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
    need(m['schema']=='transverse-surgery-publication-manifest-v1','manifest version')
    for key,value in [('problem_id',10300034),('rank',1005),('disposition','unsolved'),('approaches',5)]:
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
    pins={'author_original/AUTHOR_MANIFEST.json':(1787,'690e26d6f9b86e3c95ca74213a49f90c5f9fce5cd769c512bc3698904300e782'),'author_original/bootstrap.py':(4362,'203a1d8f5a9e49dc0eddfc4eff73c39751b07ceb029d544ac6b07d5e4a8f7f6e'),'author_original/packet/PROOF.md':(18562,'c04d615722f2f2498eaeaff86f21cc7b0d5dd0cd8e1e96c324b16fb7413f57e3'),'audit/AUDIT_MANIFEST.json':(1119,'1caba8e539ebb87dc703e921e11f2fdba2bfec30294b97c1b213d51ad7c2ba8d'),'archives/author_packet.zip':(24236,'533268c19efeb1e024777bfca36afbb20ee4e9ee09ab0fd01c7d3fc0bfed8564'),'archives/independent_audit.zip':(25129,'19fc3f87b5ccf9e460204e539071bd2ae66a258d8b5cef4a21d38a65d6f32022')}
    for n,pin in pins.items():need((len(f[n]),sha(f[n]))==pin,'original external pin: '+n)
    author={n.removeprefix('author_original/'):b for n,b in f.items() if n.startswith('author_original/')}
    audit={n.removeprefix('audit/'):b for n,b in f.items() if n.startswith('audit/')}
    ac=archive_members(f['archives/author_packet.zip'],author)
    rc=archive_members(f['archives/independent_audit.zip'],audit)
    need(ac==13 and rc==7,'frozen archive member counts')
    for members,name,prefix,extra in [(author,'AUTHOR_MANIFEST.json','packet/',{'AUTHOR_MANIFEST.json','bootstrap.py'}),(audit,'AUDIT_MANIFEST.json','',{'AUDIT_MANIFEST.json'})]:
        m=load(members[name]);entries=m['files'];expected=set(extra)
        for e in entries:
            n=prefix+e['path'];need(safe(n) and n not in expected,'inner duplicate path');expected.add(n)
            need(type(e['bytes']) is int and e['bytes']==len(members[n]) and e['sha256']==sha(members[n]),'inner manifest binding')
        need(set(members)==expected,'inner manifest inventory')
        need(m['disposition']=='unsolved' and type(m['approaches']) is int and m['approaches']==5,'inner manifest disposition')
    a=load(audit['ACCEPTANCE.json']);claims=load(author['packet/CLAIMS.json'])
    need(a['verdict']=='accept_without_correction' and a['disposition']=='unsolved' and type(a['approach_families']) is int and a['approach_families']==5,'acceptance scope')
    for n in ['correction_patch_required','replacement_author_manifest_required','formal_proof','full_solution','novelty_certified','worldwide_open_status_certified']:need(a[n] is False,'acceptance limit: '+n)
    need(a['original_author_bytes_unchanged'] is True and a['required_corrections']==[],'unchanged acceptance')
    need(claims['independent_audit']=='pending' and claims['full_solution'] is False and claims['disposition']=='unsolved','historical author disposition')
    need(type(claims['approaches']) is int and claims['approaches']==5,'author approach count')
    for k,n in [('author_archive','archives/author_packet.zip'),('author_manifest','author_original/AUTHOR_MANIFEST.json'),('author_bootstrap','author_original/bootstrap.py'),('author_proof','author_original/packet/PROOF.md')]:need(a[k]=={'bytes':len(f[n]),'sha256':sha(f[n])},'audit acceptance pin: '+k)
    need(a['replay_results']=={'bytes':len(audit['REPLAY_RESULTS.json']),'sha256':sha(audit['REPLAY_RESULTS.json'])},'historical replay pin')
    return {'author_archive_members':ac,'audit_archive_members':rc,'original_mathematics_unchanged':True,'post_freeze_correction':False,'audit_scope':a['verdict']}

def invoke(root,script,*args):
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    c=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/script),*map(str,args)],cwd=root,capture_output=True,timeout=600)
    need(c.returncode==0 and not c.stderr,'replay failed '+script+': '+c.stderr.decode('utf8','replace'))
    return load(c.stdout)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--integrity-only',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--problems',type=Path);p.add_argument('--research-results',type=Path);a=p.parse_args()
    need((a.problems is None)==(a.research_results is None),'both complete corpus inputs required')
    need(not a.integrity_only or (a.source_dir is None and a.problems is None),'optional inputs require full replay')
    root=a.root.absolute();before=authenticate(root);report=semantics(before)
    if a.integrity_only:return {'status':'PASS_PUBLICATION_INTEGRITY','problem_id':10300034,**report}
    with tempfile.TemporaryDirectory(prefix='transverse-surgery-publication-') as tmp:
        work=Path(tmp)
        for n,b in before.items():q=work/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
        args=['--author-root',work/'author_original','--author-archive',work/'archives/author_packet.zip']
        if a.source_dir is not None:args+=['--source-dir',a.source_dir.absolute()]
        if a.problems is not None:args+=['--problems',a.problems.absolute(),'--research-results',a.research_results.absolute()]
        replay=invoke(work,'audit/replay_audit.py',*args)
        need(replay['status']=='pass' and replay['original_author_bytes_unchanged'] is True and replay['contents_emitted'] is False,'independent replay status')
        acceptance=load(before['audit/ACCEPTANCE.json'])
        need(len(replay['independent_exact'])==3 and all(r['result']==acceptance['independent_exact_results'] for r in replay['independent_exact']),'independent exact result mismatch')
        need(len(replay['author_bootstrap'])==3 and all(r['result']['status']=='pass' for r in replay['author_bootstrap']),'author bootstrap modes')
        for r in replay['author_adversarial_controls']['modes']:need(r['accepted_controls']==3 and r['rejected_controls']==31,'author rejection controls')
        for r in replay['independent_artifact_controls']['modes']:need(r['accepted']==3 and r['rejected']==27 and r['semantic_payload_rejections']==9,'independent rejection controls')
        need(replay['independent_artifact_controls']['direct_parser_rejections']==7,'direct parser controls')
        primary={'sources':'NOT_RUN','corpora':'NOT_RUN'}
        if a.source_dir is not None:
            need(replay['source_replay']['status']=='pass' and len(replay['source_replay']['sources'])==3,'source rehash');primary['sources']='PASS_CURRENT_REHASH'
        else:need(replay['source_replay']=={'status':'not_requested'},'default source replay')
        if a.problems is not None:
            need(len(replay['full_corpus_replay'])==3 and all(r['result']['status']=='pass' for r in replay['full_corpus_replay']),'corpus rehash');primary['corpora']='PASS_CURRENT_REHASH'
        else:need(replay['full_corpus_replay']=={'status':'not_requested'},'default corpus replay')
        report.update(independent_replay=replay,primary_rehash=primary)
    need(authenticate(root)==before,'input bytes changed')
    return {'schema':'transverse-surgery-publication-replay-v1','status':'PASS_SCOPED_PUBLICATION','problem_id':10300034,'rank':1005,'disposition':'unsolved','approaches':5,'full_solution':False,'formal_topological_proof':False,'github_ci':False,'source_free_default':True,'publication_manifest_sha256':EXPECTED_MANIFEST,**report}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True))
    except (Reject,OSError,ValueError,KeyError,TypeError,UnicodeError,subprocess.SubprocessError,zipfile.BadZipFile) as exc:
        print('REJECT: '+str(exc),file=sys.stderr);sys.exit(1)
