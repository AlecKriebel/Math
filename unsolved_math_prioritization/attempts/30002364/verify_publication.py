"""Externally pinned, isolated publication acceptance. Stdlib only.
This authenticates finite certificates, not the geometric theorems.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
    raise SystemExit('Use python -I -S -B, optionally -O.')
import hashlib, json, pathlib, stat, subprocess, zipfile
SPECS = [{'folder': 'author', 'archive': 'CM_REDUCTION_30002364_AUTHOR_SAFE_FREEZE.zip', 'manifest': 'CM_REDUCTION_30002364_AUTHOR_EXTERNAL_MANIFEST.json', 'bootstrap': 'CM_REDUCTION_30002364_AUTHOR_BOOTSTRAP.py', 'entrypoint': 'verify_math.py', 'pins': {'CM_REDUCTION_30002364_AUTHOR_SAFE_FREEZE.zip': {'bytes': 14326, 'sha256': '32f5ec9f310f62566906cf6b0ff4a1e8cef5a6e9442ecb995c91525a1fb9879e'}, 'CM_REDUCTION_30002364_AUTHOR_EXTERNAL_MANIFEST.json': {'bytes': 1207, 'sha256': '24d868b99bd75c586313062c107bb6d6b1f2f5d5efb939f17d1401e1da6c8212'}, 'CM_REDUCTION_30002364_AUTHOR_BOOTSTRAP.py': {'bytes': 1866, 'sha256': '897a75796bef8d980a0c12808a21ddd9a71cefa7dbf54bd6cf12c8f14ad2d6a5'}}}, {'folder': 'corrected', 'archive': 'CM_REDUCTION_30002364_SECOND_CORRECTED_SAFE.zip', 'manifest': 'CM_REDUCTION_30002364_SECOND_CORRECTED_EXTERNAL_MANIFEST.json', 'bootstrap': 'CM_REDUCTION_30002364_SECOND_CORRECTED_BOOTSTRAP.py', 'entrypoint': 'verify_math.py', 'pins': {'CM_REDUCTION_30002364_SECOND_CORRECTED_SAFE.zip': {'bytes': 14650, 'sha256': 'f1feb693ca4018fa17eaae271b4020e79fe3b8d41bd9618a50af3664c4625f8d'}, 'CM_REDUCTION_30002364_SECOND_CORRECTED_EXTERNAL_MANIFEST.json': {'bytes': 1391, 'sha256': 'a2fecf6549ffa2ff254e34103cebca4400ae51a358ec915385d884a0684f9989'}, 'CM_REDUCTION_30002364_SECOND_CORRECTED_BOOTSTRAP.py': {'bytes': 1866, 'sha256': '109def42a2a8d2acaa863751d5fcb77df8ac2d6da003d215764021a258c9fb51'}}}, {'folder': 'audit_one', 'archive': 'CM_REDUCTION_30002364_FRESH_INDEPENDENT_AUDIT_SAFE.zip', 'manifest': 'CM_REDUCTION_30002364_FRESH_AUDIT_EXTERNAL_MANIFEST.json', 'bootstrap': 'CM_REDUCTION_30002364_FRESH_AUDIT_BOOTSTRAP.py', 'entrypoint': 'independent_exact.py', 'pins': {'CM_REDUCTION_30002364_FRESH_INDEPENDENT_AUDIT_SAFE.zip': {'bytes': 27033, 'sha256': '9f0ed78ed9e154fa73f2b55e0838ecc060adefc827a85fa2ef3c2db2a8a33740'}, 'CM_REDUCTION_30002364_FRESH_AUDIT_EXTERNAL_MANIFEST.json': {'bytes': 2215, 'sha256': '94411439254901040896f6f6222c980f0d7a2f9e9674a900dac623e4c0cff9ff'}, 'CM_REDUCTION_30002364_FRESH_AUDIT_BOOTSTRAP.py': {'bytes': 1872, 'sha256': '2f3ea587857dfc2f30182c4db5d6ef88f55fde86fefe285329885abad2eb4649'}}}, {'folder': 'audit_two', 'archive': 'CM_REDUCTION_30002364_SECOND_INDEPENDENT_REVIEW_SAFE.zip', 'manifest': 'CM_REDUCTION_30002364_SECOND_INDEPENDENT_REVIEW_EXTERNAL_MANIFEST.json', 'bootstrap': 'CM_REDUCTION_30002364_SECOND_INDEPENDENT_REVIEW_BOOTSTRAP.py', 'entrypoint': 'independent_check.py', 'pins': {'CM_REDUCTION_30002364_SECOND_INDEPENDENT_REVIEW_SAFE.zip': {'bytes': 18417, 'sha256': 'e5ebcb312a4bcbbc1d108ced28673f930387027904787a5ff102eeb00f78ee1d'}, 'CM_REDUCTION_30002364_SECOND_INDEPENDENT_REVIEW_EXTERNAL_MANIFEST.json': {'bytes': 1857, 'sha256': '1fe610d4f5dcabc726e59f5c0952126c48fa62063650cd8c0a5d17b5c174e96c'}, 'CM_REDUCTION_30002364_SECOND_INDEPENDENT_REVIEW_BOOTSTRAP.py': {'bytes': 1872, 'sha256': '3dbe8aeaf73ee81d090d4d302163e83cc19d5cb32e083263640f4684a240742e'}}}]
def require(ok, why):
    if not ok: raise RuntimeError(why)
def digest(b): return hashlib.sha256(b).hexdigest()
def regular(p):
    require(p.absolute()==p.resolve() and stat.S_ISREG(p.lstat().st_mode),'noncanonical or nonregular file: '+p.name)
def check(root, manifest_pin, wrapper_pin):
    require(root.absolute()==root.resolve() and stat.S_ISDIR(root.lstat().st_mode),'noncanonical package root')
    script=pathlib.Path(__file__).absolute(); regular(script)
    require(script==root/'verify_publication.py','wrapper must be in verified package')
    require(digest(script.read_bytes())==wrapper_pin,'external wrapper pin')
    mf=root/'PUBLICATION_MANIFEST.json'; regular(mf)
    raw=mf.read_bytes(); require(digest(raw)==manifest_pin,'external manifest pin')
    m=json.loads(raw); expected=m['files']
    require(isinstance(expected,dict) and expected,'invalid inventory')
    wanted_dirs=set()
    for name in expected:
        q=pathlib.PurePosixPath(name)
        require(not q.is_absolute() and str(q)==name and '..' not in q.parts,'unsafe inventory name')
        wanted_dirs.update(str(x) for x in q.parents if str(x)!='.')
    actual_files=set();actual_dirs=set()
    for q in root.rglob('*'):
        name=q.relative_to(root).as_posix(); mode=q.lstat().st_mode
        require(q.absolute()==q.resolve(),'symlink in package')
        if stat.S_ISDIR(mode): actual_dirs.add(name)
        elif stat.S_ISREG(mode): actual_files.add(name)
        else: raise RuntimeError('nonregular package member')
    require(actual_files==set(expected)|{'PUBLICATION_MANIFEST.json'},'strict file inventory')
    require(actual_dirs==wanted_dirs,'strict directory inventory')
    for name,rec in expected.items():
        b=(root/name).read_bytes()
        require({'bytes':len(b),'sha256':digest(b)}==rec,'publication file pin: '+name)
    for spec in SPECS:
        for name,rec in spec['pins'].items():
            b=(root/name).read_bytes();require({'bytes':len(b),'sha256':digest(b)}==rec,'immutable input pin: '+name)
        inner=json.loads((root/spec['manifest']).read_bytes()); archived=inner['archive']
        require(archived['filename']==spec['archive'],'archive identity')
        require(spec['pins'][spec['archive']]=={k:archived[k] for k in ('bytes','sha256')},'archive record')
        with zipfile.ZipFile(root/spec['archive']) as z:
            names=z.namelist();require(len(names)==len(set(names)) and set(names)==set(inner['files']),'archive inventory')
            require(set(x.name for x in (root/spec['folder']).iterdir())==set(names),'extracted inventory')
            for name,rec in inner['files'].items():
                require(pathlib.PurePosixPath(name).name==name,'unsafe archive member')
                info=z.getinfo(name);require(not info.is_dir() and not stat.S_ISLNK(info.external_attr>>16),'nonregular archive member')
                b=z.read(name);require(b==(root/spec['folder']/name).read_bytes(),'archive/member mismatch')
                require({'bytes':len(b),'sha256':digest(b)}==rec,'archive member pin')
    patch=(root/'audit_one/CONVERSE_SCOPE.patch').read_bytes()
    require(patch==(root/'audit_two/CONVERSE_SCOPE.patch').read_bytes(),'two patch copies differ')
    require(len(patch)==6007 and digest(patch)=='6ea4f8b41eb68763a92e8ec1b94f48a3a95b8e1ca6e3d3e323a08e85a11b6f6f','patch pin')
    corrected=digest((root/'corrected/PROOF.md').read_bytes())
    require(corrected=='e6955e4c7e5379e103de79ad3e5dc427d36adab8d36409f81647cbc173495a79','corrected proof pin')
    a=json.loads((root/'audit_one/ACCEPTANCE.json').read_bytes());b=json.loads((root/'audit_two/PATCH_ACCEPTANCE.json').read_bytes())
    require(a['accepted_corrected_proof_sha256']==b['corrected_proof']['sha256']==corrected,'audit acceptance binding')
    require(a['patch_independently_applied_zero_fuzz'] and b['fresh_patch_all_five_files_match'],'patch acceptance')
    return m
if __name__=='__main__':
    require(len(sys.argv) in (4,5) and (len(sys.argv)==4 or sys.argv[4]=='--execute'),'usage: verify_publication.py ROOT MANIFEST_SHA256 WRAPPER_SHA256 [--execute]')
    root=pathlib.Path(sys.argv[1]).absolute();check(root,sys.argv[2],sys.argv[3])
    results={}
    if len(sys.argv)==5:
        for spec in SPECS:
            cmd=[sys.executable,'-I','-S','-B']+(['-O'] if sys.flags.optimize else [])+[str(root/spec['folder']/spec['entrypoint'])]
            cp=subprocess.run(cmd,cwd=root,capture_output=True,text=True,check=True)
            results[spec['folder']]=json.loads(cp.stdout)
        check(root,sys.argv[2],sys.argv[3])
    print(json.dumps({'status':'PASS','strict_preexecution_inventory':True,'four_archives_and_30_members_exact':True,'two_reviews_bind_corrected_proof':True,'geometric_theorems_formally_verified':False,'certificates':results},sort_keys=True))
