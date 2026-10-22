#!/usr/bin/env python3
"""Strict exact-artifact replay; the external manifest must be independently trusted."""
import difflib,hashlib,json,pathlib,stat,subprocess,sys,tempfile,zipfile
EXPECTED={'ACCEPTANCE.json','AUDIT.md','AUTHOR_EXTERNAL_MANIFEST.json','AUTHOR_SAFE_FREEZE.zip','CLARIFICATION.patch','CLARIFIED_EXTERNAL_MANIFEST.json','CLARIFIED_SAFE.zip','INDEPENDENT_ALGEBRA_RESULTS.json','INTEGRITY_TEST_RESULTS.json','README.md','SOURCE_INSPECTION.json','SOURCE_PIN_RESULTS.json','independent_algebra.py','test_integrity.py','verify_sources.py','replay.py','REPLAY_RESULTS.json'}
TRUSTED={
'AUTHOR_SAFE_FREEZE.zip':(15877,'d1b572fc384124819c9f0618965bb77e86dd9474dc92dce57466ee3bf386602d'),
'AUTHOR_EXTERNAL_MANIFEST.json':(1975,'7853a1c2eb0c0ae13509de1f8ea2a05b5714170ad5d3a98f802fc54b6a797034'),
'CLARIFIED_SAFE.zip':(16579,'af5efef8873f2a4b6fdc1f454a16d2c3cbac07fd8e103922df736793544d5f8c'),
'CLARIFIED_EXTERNAL_MANIFEST.json':(2302,'f2a7bd92aaeca89f664ba718666ddb7187a1a8a06d7b8a32fede32a5264f52bf')}
PAIR='56eb2b6965848c89fd7f16e3433f3dafb39fb9bf861d801378dfed904b6dcbbd'
def require(x,m):
    if not x:raise ValueError(m)
def sha(x):return hashlib.sha256(x).hexdigest()
def pairs(items):
    d={}
    for k,v in items:
        require(k not in d,'duplicate JSON key');d[k]=v
    return d
def read(p):
    require(p.is_file() and not p.is_symlink(),'unsafe JSON');return json.loads(p.read_bytes(),object_pairs_hook=pairs)
def zip_contents(path,expected):
    require(path.is_file() and not path.is_symlink(),'unsafe archive')
    with zipfile.ZipFile(path) as z:
        infos=z.infolist();names=[i.filename for i in infos]
        require(len(names)==len(set(names)) and set(names)==set(expected),'ZIP inventory')
        for i in infos:
            require(i.filename==pathlib.PurePosixPath(i.filename).name and not i.is_dir(),'unsafe ZIP path')
            require(not stat.S_ISLNK(i.external_attr>>16) and not (i.flag_bits&1),'ZIP link or encryption')
            kind=stat.S_IFMT(i.external_attr>>16);require(kind in (0,stat.S_IFREG),'ZIP special file')
        return {i.filename:z.read(i.filename) for i in infos}
def invoke(script,args,cwd,optimized=False):
    r=subprocess.run([sys.executable,'-B']+(['-O'] if optimized else [])+[str(script),*map(str,args)],cwd=cwd,capture_output=True,timeout=120)
    require(r.returncode==0 and not r.stderr,'subprocess failed: '+script.name+' '+r.stderr.decode(errors='replace'))
    return json.loads(r.stdout),r.stdout

def run_payload(root):
    for n,(size,digest) in TRUSTED.items():
        f=root/n;require(f.is_file() and not f.is_symlink(),'missing trusted payload');b=f.read_bytes();require((len(b),sha(b))==(size,digest),'immutable payload mismatch: '+n)
    a=read(root/'ACCEPTANCE.json')
    require(a['problem_id']==2910 and a['rank']==918 and a['decision']=='ACCEPT_CLARIFIED_SCOPED_PARTIAL','acceptance identity')
    require(a['turns_used']==3 and a['turn_limit']==5 and a['full_problem_solved'] is False and a['full_problem_refuted'] is False and a['novelty_claimed'] is False,'acceptance scope')
    require(a['source_text_or_corpus_included'] is False and a['publication_performed'] is False,'distribution scope')
    require(a['complete_record_report_pair_sha256']==PAIR,'acceptance pair')
    for key in ['accepted_packet','accepted_manifest','preserved_original_packet','preserved_original_manifest']:
        x=a[key];require((x['bytes'],x['sha256'])==TRUSTED[x['name']],'acceptance byte binding')
    sources=read(root/'SOURCE_PIN_RESULTS.json')
    require(sources['result']=='pass' and sources['complete_record_report_pair_sha256']==PAIR and sources['inherited_report_empty'] is True and len(sources['pins'])==7 and all(x['match'] is True for x in sources['pins']),'source receipt')
    insp=read(root/'SOURCE_INSPECTION.json');require(insp['four_source_pdfs_freshly_retrieved_and_exact_byte_matched'] is True and len(insp['retrievals'])==4 and all(x['exact_match'] is True for x in insp['retrievals']),'source retrieval receipt')
    author_runs=[];all_payloads={}
    with tempfile.TemporaryDirectory(prefix='torus-relocated-') as td:
        td=pathlib.Path(td);cwd=td/'unrelated-cwd';cwd.mkdir()
        for label,zn,mn in [('original','AUTHOR_SAFE_FREEZE.zip','AUTHOR_EXTERNAL_MANIFEST.json'),('clarified','CLARIFIED_SAFE.zip','CLARIFIED_EXTERNAL_MANIFEST.json')]:
            manifest=read(root/mn);expected=[x['path'] for x in manifest['files']];payload=zip_contents(root/zn,expected);all_payloads[label]=payload
            target=td/label;target.mkdir()
            for n,b in payload.items():(target/n).write_bytes(b)
            for optimized in (False,True):
                result,_=invoke(target/'verify_packet.py',[target,root/mn,root/zn],cwd,optimized)
                require(result['result']=='pass' and result['files_verified']==10 and result['geometric_theorems_verified_by_code'] is False,'author replay')
                author_runs.append({'packet':label,'optimized':optimized,'result':result})
        original,clarified=all_payloads['original'],all_payloads['clarified']
        changed=sorted(n for n in original if original[n]!=clarified[n]);require(changed==['PROOF.md','sources.json','status.json']==a['changed_files'],'derivative change scope')
        patch=''
        for n in sorted(original):patch+=''.join(difflib.unified_diff(original[n].decode().splitlines(True),clarified[n].decode().splitlines(True),fromfile='original/'+n,tofile='clarified/'+n))
        require(patch.encode()==(root/'CLARIFICATION.patch').read_bytes(),'patch replay')
        for optimized in (False,True):
            algebra,raw=invoke(root/'independent_algebra.py',[],cwd,optimized)
            require(raw==(root/'INDEPENDENT_ALGEBRA_RESULTS.json').read_bytes(),'independent algebra changed')
            require(algebra['matrix_cases']==algebra['mirrored_matrix_cases']==2401 and algebra['negative_controls_rejected']==3 and algebra['certifies_topology'] is False,'independent scope')
        integrity,raw=invoke(root/'test_integrity.py',[],cwd)
        require(raw==(root/'INTEGRITY_TEST_RESULTS.json').read_bytes() and integrity['cli_rejections']==48,'integrity replay')
    return {'result':'pass','problem_id':2910,'accepted_class':'stalled_scoped_partial','author_replays':author_runs,'changed_files':changed,'patch_reproduced':True,'independent_matrix_cases':2401,'independent_mirrored_cases':2401,'arithmetic_negative_controls':3,'package_cli_rejections':48,'source_receipt_bound':True,'source_bytes_rehashed_this_run':False,'geometric_theorems_verified_by_code':False,'full_problem_solved':False,'novelty_claimed':False}

def main():
    require(len(sys.argv)==4,'Usage: replay.py AUDIT_DIRECTORY EXTERNAL_MANIFEST AUDIT_ZIP')
    require(all(not pathlib.Path(x).is_symlink() for x in sys.argv[1:]),'symlink command input')
    root,mp,zp=(pathlib.Path(x).resolve() for x in sys.argv[1:])
    require(root.is_dir() and not pathlib.Path(sys.argv[1]).is_symlink(),'unsafe root')
    m=read(mp);require(m['schema']=='independent-audit-v1' and m['problem_id']==2910,'manifest identity')
    es=m['files'];names=[e['path'] for e in es];require(len(names)==len(set(names)) and set(names)==EXPECTED,'manifest inventory')
    actual=set()
    for f in root.rglob('*'):
        require(f.is_file() and not f.is_symlink(),'unsafe member');actual.add(f.relative_to(root).as_posix())
    require(actual==EXPECTED,'audit inventory')
    for e in es:
        b=(root/e['path']).read_bytes();require(type(e['bytes']) is int and len(b)==e['bytes'] and sha(b)==e['sha256'],'audit member binding: '+e['path'])
    require(zp.is_file() and not pathlib.Path(sys.argv[3]).is_symlink(),'unsafe outer ZIP')
    b=zp.read_bytes();require(len(b)==m['zip']['bytes'] and sha(b)==m['zip']['sha256'],'audit ZIP binding')
    payload=zip_contents(zp,EXPECTED)
    require(all(b==(root/n).read_bytes() for n,b in payload.items()),'audit ZIP payload')
    result=run_payload(root);require(result==read(root/'REPLAY_RESULTS.json'),'recorded replay mismatch');result['audit_files_verified']=len(EXPECTED);result['audit_zip_verified']=True
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:print(json.dumps({'result':'fail','error':str(e)},sort_keys=True),file=sys.stderr);sys.exit(1)
