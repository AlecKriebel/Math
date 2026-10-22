"""Read-only closed-packet verifier. Integrity is not a mathematical proof."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, re, runpy, sys

class VerificationFailure(ValueError):
    pass

def need(ok, message):
    if not ok:
        raise VerificationFailure(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def pairs(items):
    d={}
    for k,v in items:
        need(k not in d,'duplicate JSON key: '+k)
        d[k]=v
    return d

def parse(data):
    return json.loads(data.decode('utf-8'),object_pairs_hook=pairs)

def safe(root,name):
    need(type(name) is str and name != '', 'empty/non-string path')
    p=PurePosixPath(name)
    need(not p.is_absolute() and '..' not in p.parts and '.' not in p.parts and '\\' not in name, 'unsafe path')
    need(p.as_posix()==name,'noncanonical path')
    cur=root
    for part in p.parts:
        cur=cur/part
        need(not cur.is_symlink(),'symlink in packet')
    need(cur.is_file(),'missing packet file: '+name)
    return cur

def verify(root,external):
    root=Path(root).resolve()
    need(re.fullmatch('[0-9a-f]{64}',external) is not None,'external SHA256 required')
    need(not (root/'MANIFEST.json').is_symlink(),'manifest symlink')
    raw=(root/'MANIFEST.json').read_bytes()
    need(sha(raw)==external,'external manifest SHA256 mismatch')
    m=parse(raw)
    need(set(m)=={'schema','scope','files'},'manifest schema fields')
    need(m['schema']==1 and m['scope']=='pr1129_projective_adversary','manifest identity')
    need(type(m['files']) is list and len(m['files'])>10,'manifest files list')
    names=set()
    for e in m['files']:
        need(type(e) is dict and set(e)=={'path','bytes','sha256'},'manifest entry schema')
        name=e['path'];need(name not in names,'duplicate manifest member')
        need(name not in {'MANIFEST.json','SEAL.sha256'},'recursive seal member')
        names.add(name)
        path=safe(root,name);data=path.read_bytes()
        need(type(e['bytes']) is int and e['bytes']>=0 and len(data)==e['bytes'],'byte count mismatch: '+name)
        need(re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None and sha(data)==e['sha256'],'file SHA mismatch: '+name)
    observed=set()
    for path in root.rglob('*'):
        need(not path.is_symlink(),'unlisted symlink')
        if path.is_file():
            name=path.relative_to(root).as_posix()
            if name not in {'MANIFEST.json','SEAL.sha256'}:
                observed.add(name)
    need(observed==names,'packet closure mismatch')
    for name in ['CLAIM.json','SOURCE_BINDINGS.json','REVIEW.md','check_projective.py','verify_offline.py','VALIDATION_RUNS.json','RESEARCH_LOG.md','private/head_inventory.json']:
        need(name in names,'required packet member absent: '+name)
    c=parse((root/'CLAIM.json').read_bytes())
    expected={'schema':1,'pr':1129,'problem_id':30005461,'alias':'OWR-12697710-007',
      'head':'26fed29c1130e539ba018a37200f133870f0e036','base':'f6caddda8f8be2cdb3e91494325d8f7f365bc3fc',
      'surface_relation':{'ABC':1,'D^3':-1},'substitution_exponents':[[2,1,0],[1,2,0],[0,0,3],[1,1,1]],
      'parameter_bound':3,'parameter_inequality':'strict','theorem_N_parity':0,'target_power':'N+1',
      'root_degree_in_ABCD':'N+1','substituted_root_degree':'3*(N+1)'}
    for k,v in expected.items():
        need(c.get(k)==v,'claim binding mismatch: '+k)
    inventory=parse((root/'private/head_inventory.json').read_bytes())
    need(inventory.get('head')==expected['head'] and inventory.get('base')==expected['base'],'head inventory binding')
    filenames={'ACCEPTANCE.json','CREDITED_MIXED_EXPONENT_PROOF.md','MANIFEST.json','MATHEMATICAL_AUDIT.md','PROOF.md','README.md','REAL_DELTA_APPENDIX.md','SOURCE_METADATA.json','SOURCE_REVIEW.md','STATUS.json'}
    need(len(inventory['files'])==10 and {Path(e['path']).name for e in inventory['files']}==filenames,'ten-file head inventory')
    for e in inventory['files']:
        need(e['path']=='unsolved_math_prioritization/attempts/30005461/'+Path(e['path']).name,'head path scope')
        name='private/head/'+e['path'];need(name in names,'head source missing')
        data=safe(root,name).read_bytes()
        need(len(data)==e['bytes'] and sha(data)==e['sha256'],'head source digest')
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\x00'+data).hexdigest()
        need(blob==e['blob'],'Git blob mismatch')
        if Path(e['path']).name=='PROOF.md':
            need(sha(data)=='46af7394ebfee7b0de9861693f84ab684502da3be208c626411f24e2538c7d15','immutable principal proof binding')
    s=parse((root/'SOURCE_BINDINGS.json').read_bytes())
    need(s.get('schema')==1 and len(s['primary_sources'])==3,'source schema')
    sources={e['key']:e for e in s['primary_sources']}
    required={'original':('https://ems.press/content/serial-article-files/47007?nt=1','5a9bdc9f9daa12ef35185ceae208c0f2f75e191875827f78b7b6ad0f5cdbf240'),
      'scheiderer_arxiv':('https://arxiv.org/pdf/1104.1772v1','3438ce8a53ad9362a2d885e22d1ec1778f67af8ff22f2f8999d639898d44467b'),
      'cohomology':('https://stacks.math.columbia.edu/tag/01XS','4c788eac610da4c6b3800f3af54e028caccfd5ef877ac84184f8e23c8a372af3')}
    need(set(sources)==set(required),'source keys')
    for key,(url,digest) in required.items():
        e=sources[key];need(e['url']==url and e['sha256']==digest,'primary source binding')
        need(e['file'] in names,'primary source file missing')
        data=safe(root,e['file']).read_bytes()
        need(len(data)==e['bytes'] and sha(data)==digest,'primary source bytes')
    checks=runpy.run_path(str(root/'check_projective.py'),run_name='offline_math')['run_math']()
    need(checks['status']=='pass' and checks['counts']['adverse_controls']==8,'finite controls fail')
    return {'status':'pass','head':expected['head'],'files_checked':len(names),'math':checks,
      'boundary':'Closed packet integrity and finite exact interfaces only; REVIEW.md contains the universal argument. No priority/publication certification.'}

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    a.add_argument('--manifest-sha256',required=True)
    args=a.parse_args()
    try:
        result=verify(args.root,args.manifest_sha256)
    except (ValueError,OSError,KeyError,TypeError) as e:
        print(json.dumps({'status':'fail','reason':str(e)},sort_keys=True));return 1
    print(json.dumps(result,sort_keys=True));return 0

if __name__=='__main__':
    sys.exit(main())
