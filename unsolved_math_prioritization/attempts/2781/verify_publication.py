"""Externally trust this file and the manifest pin before execution.
Data/byte verification only, never formal mathematical verification.
Python 3.10+ standard library and /usr/bin/patch required on a quiescent filesystem.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: require -I -S -B')
import hashlib,json,os,re,stat,subprocess,tempfile,zipfile
from pathlib import Path,PurePosixPath

def require(ok,message):
    if not ok: raise ValueError(message)
def h(b): return hashlib.sha256(b).hexdigest()
def unique(pairs):
    d={}
    for k,v in pairs:
        require(k not in d,'duplicate JSON key');d[k]=v
    return d
def parse(b):return json.loads(b.decode('utf-8'),object_pairs_hook=unique,parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))
def check_path(p,directory=False):
    for a in [p,*p.parents]: require(not a.is_symlink(),'symlink path component')
    s=p.lstat();require(stat.S_ISDIR(s.st_mode) if directory else stat.S_ISREG(s.st_mode),'nonregular path')
    if not directory:require(s.st_nlink==1,'hard-linked file');require(s.st_mode&0o111==0,'executable file mode')
def record(p):b=p.read_bytes();return {'name':p.name,'bytes':len(b),'sha256':h(b)}
def verify(root,pin):
    root=Path(os.path.abspath(root));check_path(root,True)
    mp=root/'PUBLICATION_MANIFEST.json';check_path(mp)
    require(re.fullmatch('[0-9a-f]{64}',pin) is not None,'bad manifest pin')
    b=mp.read_bytes();require(h(b)==pin,'publication manifest pin mismatch');m=parse(b)
    require(set(m)=={'format','files'} and m['format']=='kirby-surface-2781-publication-inventory-v1','bad publication manifest')
    names=[]
    for row in m['files']:
        require(set(row)=={'path','bytes','sha256'},'bad inventory record')
        name=row['path'];require(isinstance(name,str) and '\\' not in name and not PurePosixPath(name).is_absolute() and all(x not in {'','.','..'} for x in name.split('/')),'unsafe inventory path')
        require(type(row['bytes']) is int and row['bytes']>=0,'bad byte count');require(re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'bad digest');names.append(name)
    require(len(names)==len(set(names))==len(set(x.casefold() for x in names)),'duplicate inventory entry')
    require('PUBLICATION_MANIFEST.json' not in names,'manifest cannot list itself')
    expected_dirs={str(PurePosixPath(x).parent) for x in names if '/' in x}
    for d in list(expected_dirs):expected_dirs.update(str(p) for p in PurePosixPath(d).parents if str(p)!='.')
    files=[];dirs=[]
    for base,ds,fs in os.walk(root,followlinks=False):
        for n in ds: p=Path(base)/n;check_path(p,True);dirs.append(p.relative_to(root).as_posix())
        for n in fs: p=Path(base)/n;check_path(p);files.append(p.relative_to(root).as_posix())
    require(set(files)==set(names)|{'PUBLICATION_MANIFEST.json'} and set(dirs)==expected_dirs,'strict publication inventory mismatch')
    for row in m['files']:
        b=(root/row['path']).read_bytes();require(len(b)==row['bytes'] and h(b)==row['sha256'],'publication member mismatch: '+row['path'])
    meta=parse((root/'PUBLICATION_METADATA.json').read_bytes())
    pins={'original':('eaa93db26033043b36df00fad6951c939ef428977a59489a1d9897fa3333aa65','54d7634813f0d1e95f9f359f3f1561133f4e12020d5b03a0494775b1f5af653c'),'corrected':('b5efa4e9f2b04e67bfe8afe63ad7a365c5c4b5b0d994d02fafbcdddba250bf87','7db232582c4762f383423933bcf0581b46b02a91b4464f8a32aaf1dd705d5997'),'audit':('8732cd2c432d49c226ba6ecebff230f6690ece954bedec7c12b47e0f437bb665','ccf1c66b5d1604e990ef52b8dd27a365d52b5a9779e2053244d9ee51f78eb7c2')}
    require(len(meta['packets'])==3 and {x['role'] for x in meta['packets']}==set(pins),'bad packet roles')
    bootstrap=root/'historical_bootstrap/KIRBY_SURFACE_2781_INDEPENDENT_AUDIT_BOOTSTRAP.py'
    require(h(bootstrap.read_bytes())=='27d4486bc279fe30c0aa2b39a62811be6722b235c81cefa51865b0ccaba8bf76','historical validator pin')
    count=0
    for pack in meta['packets']:
        role=pack['role'];a=root/'archives'/pack['archive']['name'];em=root/'manifests'/pack['external_manifest']['name']
        require(record(a)==pack['archive'] and record(em)==pack['external_manifest'],'outer packet record mismatch')
        require((h(a.read_bytes()),h(em.read_bytes()))==pins[role],'frozen packet pins')
        args=[sys.executable,'-I','-S','-B']+(['-O'] if sys.flags.optimize else [])+[str(bootstrap),str(a),str(em),*pins[role]]
        cp=subprocess.run(args,capture_output=True,text=True,env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8'},timeout=30)
        require(cp.returncode==0,'frozen validator rejected '+role+': '+cp.stdout+cp.stderr)
        result=parse(cp.stdout.encode());require(result['status']=='PASS_DATA_ONLY_INTEGRITY' and result['payload_code_executed'] is False,'unexpected packet result')
        with zipfile.ZipFile(a) as z:
            require(set(z.namelist())=={p.name for p in (root/role).iterdir()},'extracted inventory mismatch')
            for n in z.namelist():require(z.read(n)==(root/role/n).read_bytes(),'extracted member differs')
            count+=len(z.namelist())
    acceptance=parse((root/'audit/ACCEPTANCE.json').read_bytes());byrole={x['role']:x for x in meta['packets']}
    for field,role,key in [('original_freeze','original','archive'),('original_external_manifest','original','external_manifest'),('corrected_archive','corrected','archive'),('corrected_external_manifest','corrected','external_manifest')]:require(acceptance[field]==byrole[role][key],'acceptance packet binding')
    patch=root/'audit/CORRECTION.patch.txt';require(acceptance['correction_patch']==record(patch),'acceptance patch binding')
    require(acceptance['disposition']=='ACCEPT_CORRECTED_PARTIAL_UNSOLVED' and acceptance['full_target_solved'] is False and acceptance['approaches_used']==5 and acceptance['new_approaches_added_by_audit']==0,'acceptance scope')
    require(acceptance['numbered_propositions_accepted']==[1,2,3,4,5],'acceptance propositions')
    patched=['APPROACHES.md','CHECKS.md','PROOF.md','SOURCE_METADATA.json','STATUS.json']
    patch_text=patch.read_text();require(re.findall(r'^--- author/(.*)$',patch_text,re.M)==patched and re.findall(r'^\+\+\+ corrected/(.*)$',patch_text,re.M)==patched,'patch targets')
    with tempfile.TemporaryDirectory(prefix='kp233-patch-') as tmp:
        dest=Path(tmp)
        for p in (root/'original').iterdir():(dest/p.name).write_bytes(p.read_bytes())
        cp=subprocess.run(['/usr/bin/patch','--batch','--fuzz=0','--no-backup-if-mismatch','-p1','--input',str(patch)],cwd=dest,capture_output=True,text=True,env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8'},timeout=30)
        require(cp.returncode==0 and 'offset' not in cp.stdout.lower() and 'fuzz' not in cp.stdout.lower(),'actual patch replay failed')
        for n in patched:require((dest/n).read_bytes()==(root/'corrected'/n).read_bytes(),'patched bytes differ: '+n)
        (dest/'CORRECTIONS.md').write_bytes((root/'corrected/CORRECTIONS.md').read_bytes())
        inner=parse((root/'corrected/MANIFEST.json').read_bytes());rows=[]
        for p in sorted(dest.iterdir()):
            if p.name=='MANIFEST.json':continue
            b=p.read_bytes();rows.append({'path':p.name,'bytes':len(b),'sha256':h(b)})
        inner['files']=rows;rebuilt=(json.dumps(inner,indent=2)+'\n').encode()
        require(rebuilt==(root/'corrected/MANIFEST.json').read_bytes(),'regenerated corrected manifest differs')
    status=parse((root/'corrected/STATUS.json').read_bytes())
    require(status['problem_id']==2781 and status['rank']==859 and status['status']=='unsolved' and status['approaches_used']==status['approach_limit']==5 and status['full_target_solved'] is False,'corrected scope')
    require('Local moving and the existence of a dense global orbit are incomparable' in (root/'corrected/PROOF.md').read_text(),'wording correction absent')
    return {'status':'PASS','problem_id':2781,'rank':859,'canonical_status':'unsolved','turns':'5/5','archive_count':3,'archive_members':count,'original_freeze_preserved':True,'actual_zero_fuzz_patch_replayed':True,'patched_files':patched,'additional_corrected_members':['CORRECTIONS.md','MANIFEST.json'],'corrected_acceptance_bound':True,'strict_publication_inventory':True,'payload_code_executed':False,'formal_mathematical_verification':False,'optimized':bool(sys.flags.optimize)}
if __name__=='__main__':
    try:
        require(len(sys.argv)==3,'usage: verify_publication.py ROOT PUBLICATION_MANIFEST_SHA256')
        print(json.dumps(verify(*sys.argv[1:]),sort_keys=True))
    except Exception as e:
        print(json.dumps({'status':'REJECT','reason':str(e)},sort_keys=True));sys.exit(1)
