"""Read-only offline validator. Trust requires a separately pinned external receipt."""
import ast, hashlib, json, os, re, stat, subprocess, sys
from pathlib import Path
PINS = {'PROVENANCE.json': {'bytes': 1219, 'sha256': 'b0ee166f7b55d51df13702b22fa39c88bf1a990aea98e36a0ca0416b0bda6d5a'}, 'SOURCE_CITATIONS.md': {'bytes': 3005, 'sha256': '2a4351996d147494533f09480c31ab357816ec99628a8bd11272285ed9ca8e3b'}, 'REPORT.md': {'bytes': 7556, 'sha256': '4d18569b85f41c6963170e7c676952deeaf5e68d7ade3af8fe22d420f036d46a'}, 'PROOF_CHECKS_OPTIMIZED.json': {'bytes': 1795, 'sha256': '399cf5169a4dc59c2a09f5ea956bde8a61a3968a7d7f7061798528ea43ae9896'}, 'PROOF_CHECKS.json': {'bytes': 1795, 'sha256': '399cf5169a4dc59c2a09f5ea956bde8a61a3968a7d7f7061798528ea43ae9896'}, 'PROOF_CHECKS.py': {'bytes': 3138, 'sha256': 'fdaf9a3496c0772f54b61c7ca8d0827b30531068961f5ee05d1fc6c0964900bc'}, 'INDEPENDENT_REVIEW.md': {'bytes': 12412, 'sha256': '5e38d57bee3e5989d9a88951b3d62b9af6b499ad5ebe9285f802f3f92d6e9b12'}, 'SOURCE_METADATA.json': {'bytes': 1028, 'sha256': '213e771836506f74e3836653a6d4084eacfec7a13bb4ee234e47f588064d3cd0'}, 'README.md': {'bytes': 1710, 'sha256': '84e7217a74c5e17263c4bde42b461c1c7e096a67b972b520bf52206e9ba393ba'}}
EXPECTED = {'status': 'PASS', 'matrix': [[1, -1, -1, 1, 0, 0], [0, 0, 1, -1, -1, 1]], 'checks': [{'p': 2, 'additive_dimension': 1, 'group_size': 2, 'functions_checked': 13, 'direct_density_checks': 3, 'shortest_row_support': 4, 'status': 'PASS'}, {'p': 2, 'additive_dimension': 2, 'group_size': 4, 'functions_checked': 97, 'direct_density_checks': 3, 'shortest_row_support': 4, 'status': 'PASS'}, {'p': 2, 'additive_dimension': 3, 'group_size': 8, 'functions_checked': 256, 'direct_density_checks': 3, 'shortest_row_support': 4, 'status': 'PASS'}, {'p': 3, 'additive_dimension': 1, 'group_size': 3, 'functions_checked': 35, 'direct_density_checks': 3, 'shortest_row_support': 4, 'status': 'PASS'}, {'p': 3, 'additive_dimension': 2, 'group_size': 9, 'functions_checked': 512, 'direct_density_checks': 3, 'shortest_row_support': 4, 'status': 'PASS'}, {'p': 5, 'additive_dimension': 1, 'group_size': 5, 'functions_checked': 275, 'direct_density_checks': 3, 'shortest_row_support': 4, 'status': 'PASS'}, {'p': 7, 'additive_dimension': 1, 'group_size': 7, 'functions_checked': 128, 'direct_density_checks': 3, 'shortest_row_support': 4, 'status': 'PASS'}], 'total_functions': 1316, 'limitations': 'Finite exact sanity checks only. Universal proof uses Jensen; extension fields need only their additive group for this ±1 matrix.'}
AST_SHA256 = '5143e41570f24627c4a7c9eb2932bfd9d849c0f82bed3110f1fad0cb1a82a701'
PAYLOAD = frozenset(PINS) | {'validate.py'}
def require(ok, message):
    if not ok: raise ValueError(message)
def exact(a,b):
    if type(a) is not type(b): return False
    if type(b) is dict: return a.keys()==b.keys() and all(exact(a[k],v) for k,v in b.items())
    if type(b) is list: return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    return a==b
def unique(pairs):
    d={}
    for k,v in pairs:
        require(k not in d,'duplicate JSON key')
        d[k]=v
    return d
def read_json(p): return json.loads(p.read_text(),object_pairs_hook=unique)
def preflight(root):
    require(stat.S_ISDIR(os.lstat(root).st_mode),'root must be real directory')
    entries=list(os.scandir(root))
    for e in entries:
        s=os.lstat(e.path)
        require(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'nonregular or multiply linked member: '+e.name)
    require({e.name for e in entries}==PAYLOAD|{'MANIFEST.json'},'inventory mismatch')
def validate(root):
    root=Path(root)
    preflight(root) # Full lstat preflight, including manifest, before content.
    m=read_json(root/'MANIFEST.json')
    require(type(m) is dict and set(m)=={'schema_version','row','id','files'},'manifest schema')
    for k,v in [('schema_version',1),('row',1908),('id',30005119)]:
        require(type(m[k]) is int and m[k]==v,'manifest integer '+k)
    require(type(m['files']) is dict and set(m['files'])==PAYLOAD,'manifest inventory')
    for n,e in m['files'].items():
        require(type(e) is dict and set(e)=={'bytes','sha256'},'entry schema')
        require(type(e['bytes']) is int and e['bytes']>=0,'byte count integer')
        require(type(e['sha256']) is str and re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None,'hash format')
    for n,e in m['files'].items():
        b=(root/n).read_bytes()
        require(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'hash/size mismatch '+n)
    for n,e in PINS.items(): require(exact(m['files'][n],e),'standalone provenance mismatch '+n)
    for n in ['PROOF_CHECKS.json','PROOF_CHECKS_OPTIMIZED.json']:
        require(exact(read_json(root/n),EXPECTED),'exact finite schema/result mismatch')
    tree=ast.parse((root/'PROOF_CHECKS.py').read_text())
    require(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),'assert would disappear under -O')
    require(hashlib.sha256(ast.dump(tree,include_attributes=False).encode()).hexdigest()==AST_SHA256,'checker AST provenance')
    checks=EXPECTED['checks']
    require(sum(c['functions_checked'] for c in checks)==1316,'instance count')
    require(sum(c['direct_density_checks'] for c in checks)==21,'direct check count')
    duplicates=sum(2**c['group_size'] for c in checks if c['group_size']<=5)
    require(1316-duplicates==1256,'unique count')
    outputs={}
    for label,flags in [('normal',[]),('optimized',['-O'])]:
        p=subprocess.run([sys.executable,*flags,'-B',str(root/'PROOF_CHECKS.py')],capture_output=True,text=True,timeout=120)
        require(p.returncode==0 and p.stderr=='','replay failure '+label)
        require(exact(json.loads(p.stdout,object_pairs_hook=unique),EXPECTED),'replay output mismatch '+label)
        require(p.stdout.encode()==(root/('PROOF_CHECKS.json' if label=='normal' else 'PROOF_CHECKS_OPTIMIZED.json')).read_bytes(),'bytewise replay mismatch')
        outputs[label]={'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()}
    return {'status':'PASS','row':1908,'id':30005119,'files_verified':len(PAYLOAD),'test_instances':1316,'unique_group_function_cases':1256,'direct_density_checks':21,'replays':outputs,'scope':'Integrity and finite replay; universal proof is analytic; external receipt required for authenticity.'}
if __name__=='__main__': print(json.dumps(validate(Path(__file__).parent),indent=2))
