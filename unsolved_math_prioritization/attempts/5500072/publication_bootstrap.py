#!/usr/bin/env python3
"""Fail-closed publication verifier. Authenticate this file externally BEFORE use.
The second argument is the externally trusted PUBLICATION_MANIFEST.json SHA-256.
Optional complete corpus and source inputs are read-only and never emitted.
"""
import argparse,hashlib,io,json,pathlib,re,stat,subprocess,sys,tempfile,zipfile

def require(value,message):
    if not value: raise ValueError(message)
def fp(raw): return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def pairs(rows):
    out={}
    for key,value in rows:
        require(key not in out,'duplicate JSON key');out[key]=value
    return out
def bad_constant(value): raise ValueError('nonfinite JSON')
def parse(raw):return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad_constant)
def verify(root,digest):
    require(root.is_dir() and not root.is_symlink(),'package root')
    require(re.fullmatch('[0-9a-f]{64}',digest) is not None,'external digest syntax')
    manifest_path=root/'PUBLICATION_MANIFEST.json';require(not manifest_path.is_symlink(),'manifest symlink')
    raw=manifest_path.read_bytes();require(fp(raw)['sha256']==digest,'external manifest digest mismatch')
    m=parse(raw);require(m['problem_id']==5500072 and m['status']=='unsolved' and m['approaches_used']==3 and m['full_resolution'] is False,'manifest semantics')
    expected=m['files'];require(isinstance(expected,dict) and expected,'file map')
    for n in expected:
        p=pathlib.PurePosixPath(n);require(not p.is_absolute() and '\\' not in n and all(c not in ('','.','..') for c in p.parts) and str(p)==n,'unsafe expected path')
    dirs={str(p) for n in expected for p in pathlib.PurePosixPath(n).parents if str(p)!='.'}
    actual=[];actual_dirs=[]
    for p in root.rglob('*'):
        require(not p.is_symlink(),'symlink rejected')
        if p.is_dir():actual_dirs.append(p.relative_to(root).as_posix())
        else:require(p.is_file(),'special file rejected');actual.append(p.relative_to(root).as_posix())
    require(set(actual)==set(expected)|{'PUBLICATION_MANIFEST.json'} and set(actual_dirs)==dirs,'exact tree inventory')
    for n,pin in expected.items():require(fp((root/n).read_bytes())==pin,'file mismatch: '+n)
    count=0
    for folder,prefix,ending in [('author','REGULAR_PENTAGON_5500072_AUTHOR_','SAFE_FREEZE.zip'),('audit','REGULAR_PENTAGON_5500072_UPDATED_INDEPENDENT_AUDIT_','SAFE.zip')]:
        a=parse((root/(prefix+'EXTERNAL_MANIFEST.json')).read_bytes());data=(root/(prefix+ending)).read_bytes()
        require(fp(data)==a['archive'],'archive manifest link');require(fp((root/(prefix+'BOOTSTRAP.py')).read_bytes())==a['bootstrap'],'bootstrap manifest link')
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            names=z.namelist();require(len(names)==len(set(names)) and set(names)==set(a['files']),'ZIP exact inventory');require(z.testzip() is None,'ZIP CRC')
            for n in names:
                info=z.getinfo(n);require(n==info.orig_filename and pathlib.PurePosixPath(n).name==n and '\\' not in n and n not in ('.','..'),'ZIP unsafe name')
                require(not info.is_dir() and stat.S_IFMT(info.external_attr>>16) in (0,stat.S_IFREG),'ZIP special member')
                b=z.read(n);require(fp(b)==a['files'][n] and (root/folder/n).read_bytes()==b,'ZIP loose member mismatch');count+=1
    for ending in ['SAFE_FREEZE.zip','EXTERNAL_MANIFEST.json','BOOTSTRAP.py']:
        n='REGULAR_PENTAGON_5500072_AUTHOR_'+ending;require((root/n).read_bytes()==(root/'audit'/n).read_bytes(),'nested unchanged author')
    a=parse((root/'audit/EXACT_ACCEPTANCE.json').read_bytes());require(a['accepted_archive']==dict(file='REGULAR_PENTAGON_5500072_AUTHOR_SAFE_FREEZE.zip',**fp((root/'REGULAR_PENTAGON_5500072_AUTHOR_SAFE_FREEZE.zip').read_bytes())),'accepted object')
    require(a['review_provenance']=={'reviewer_type':'independent AI assistant','human_peer_review':False,'formal_verification':False},'review provenance')
    require(a['approaches_used']==3 and a['full_resolution'] is False and a['novelty_claim'] is False,'bounded acceptance')
    receipt=parse((root/'REGULAR_PENTAGON_5500072_UPDATED_INDEPENDENT_AUDIT_RECEIPT.json').read_bytes())
    require(receipt['full_audit_replay_tests_passed']==81 and receipt['outer_tests_passed']==43 and len(receipt['outer_tests'])==43 and all(t['passed'] is True for t in receipt['outer_tests']),'historical receipt')
    return {'files_verified':len(expected)+1,'archive_members_verified':count,'independent_AI_review':True,'human_peer_review':False,'formal_verification':False}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',type=pathlib.Path);ap.add_argument('manifest_sha256');ap.add_argument('--verify-only',action='store_true')
    for name in ['catalog','problems','reports','source-dir']:ap.add_argument('--'+name,type=pathlib.Path)
    args=ap.parse_args();root=args.root.absolute();out=verify(root,args.manifest_sha256)
    supplied=[getattr(args,n) is not None for n in ['catalog','problems','reports']];require(not any(supplied) or all(supplied),'all three corpora required')
    forwarded=[]
    for name in ['catalog','problems','reports','source_dir']:
        p=getattr(args,name)
        if p is not None:forwarded+=['--'+name.replace('_','-'),str(p.resolve())]
    if not args.verify_only:
        results=[]
        with tempfile.TemporaryDirectory(prefix='regular pentagon publication replay ') as tmp:
            tmp=pathlib.Path(tmp);packet=tmp/'relocated package';packet.mkdir();cwd=tmp/'unrelated working directory';cwd.mkdir()
            for name in ['REGULAR_PENTAGON_5500072_UPDATED_INDEPENDENT_AUDIT_'+x for x in ['BOOTSTRAP.py','SAFE.zip','EXTERNAL_MANIFEST.json']]:
                (packet/name).write_bytes((root/name).read_bytes())
            for optimized in [False,True]:
                flags=['-I','-S','-B']+(['-O'] if optimized else [])
                x=subprocess.run([sys.executable]+flags+[str(packet/'REGULAR_PENTAGON_5500072_UPDATED_INDEPENDENT_AUDIT_BOOTSTRAP.py')]+forwarded,cwd=cwd,capture_output=True,text=True,timeout=300)
                require(x.returncode==0,'authenticated replay failed: '+x.stderr);results.append(parse(x.stdout))
            require(results[0]==results[1],'normal optimized mismatch')
        r=results[0]['replay'];require(r['accepted_original_unchanged'] is True and r['full_resolution'] is False,'replay disposition')
        if all(supplied) and args.source_dir is not None:
            require(r['tests_passed']==81 and r['independent_corpus_verification']['verified'] and r['source_bytes_verified'],'full input checks')
            require(r==parse((root/'audit/audit_replay_results.json').read_bytes()),'recorded replay mismatch')
        out.update({'normal_optimized_identical':True,'replay':results[0]})
    require(verify(root,args.manifest_sha256)=={k:out[k] for k in ['files_verified','archive_members_verified','independent_AI_review','human_peer_review','formal_verification']},'post replay change')
    out.update({'problem_id':5500072,'status':'unsolved','approaches_used':3,'full_resolution':False,'manifest_sha256':args.manifest_sha256})
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
