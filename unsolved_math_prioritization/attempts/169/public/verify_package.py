#!/usr/bin/env python3
"""Read-only, fail-closed verification of this authored mathematical package."""
import hashlib,json,re,sys
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent

def require(ok,message):
    if not ok:raise ValueError(message)
def digest(data):return hashlib.sha256(data).hexdigest()
def read_json(path):
    def unique(pairs):
        obj={}
        for k,v in pairs:
            require(k not in obj,'duplicate JSON key')
            obj[k]=v
        return obj
    return json.loads(path.read_text(),object_pairs_hook=unique)
def inventory(root):
    paths=[]
    for p in root.rglob('*'):
        require(not p.is_symlink(),'symbolic link forbidden')
        if p.is_file():paths.append(p.relative_to(root).as_posix())
    return sorted(paths)
def verify(root=ROOT):
    manifest=read_json(root/'MANIFEST.json')
    require(set(manifest)=={'schema','problem_status','substantive_passes','resolution_claimed','files'},'manifest schema')
    require(manifest['schema']=='random-translates-public-v1','manifest version')
    require(manifest['problem_status']=='UNSOLVED' and manifest['substantive_passes']==5 and manifest['resolution_claimed'] is False,'manifest mathematical status')
    files=manifest['files'];require(isinstance(files,list) and len(files)>50,'empty/incomplete manifest')
    expected=[]
    for item in files:
        require(set(item)=={'path','bytes','sha256'},'file record schema')
        path=item['path'];parts=PurePosixPath(path)
        require(isinstance(path,str) and not parts.is_absolute() and '..' not in parts.parts and str(parts)==path and path!='MANIFEST.json','unsafe manifest path')
        require(isinstance(item['bytes'],int) and not isinstance(item['bytes'],bool) and item['bytes']>=0,'invalid byte size')
        require(isinstance(item['sha256'],str) and re.fullmatch('[0-9a-f]{64}',item['sha256']) is not None,'invalid digest')
        expected.append(path);p=root/path
        require(p.is_file() and not p.is_symlink(),'missing regular file')
        b=p.read_bytes();require(len(b)==item['bytes'] and digest(b)==item['sha256'],'file identity mismatch: '+path)
    require(expected==sorted(set(expected)),'duplicate or unordered file entries')
    require(inventory(root)==sorted(expected+['MANIFEST.json']),'unmanifested or missing files')
    formulation=read_json(root/'FORMULATION.json')
    required={'affirmative': 'success probability tends to one along all primes', 'cap': 'floor(100*sqrt(p))', 'cap_100k_equivalence_claimed': False, 'centres': 'fully adaptive to all of A', 'event': 'there exists T with |T|<=cap and A+T=Z/pZ', 'final_residual_swap_constant': 'm', 'final_residual_tail_denominator': '2*k*m^2', 'group': 'Z/pZ, p prime', 'historical_conservative_tail_denominator': '8*k*m^2', 'id': 169, 'label': 'GREEN-081', 'law': 'uniform over all subsets of exactly floor(sqrt(p)) elements', 'negative': 'fixed positive failure probability along arbitrarily large primes', 'problem': 'Green Problem 39', 'record': 1789, 'resolution_claimed': False, 'set_size': 'floor(sqrt(p))', 'status': 'UNSOLVED', 'substantive_passes': 5}
    require(set(formulation)==set(required),'exact formulation schema')
    for k,v in required.items():
        require(type(formulation[k]) is type(v) and formulation[k]==v,'exact formulation mismatch: '+k)
    audits=read_json(root/'AUDIT_BINDINGS.json')
    require(audits['original_problem_status']=='UNSOLVED' and audits['substantive_passes']==5 and audits['resolution_claimed'] is False,'audit status mismatch')
    require(len(audits['audit_stages'])==5 and sum(len(x['proof_bindings']) for x in audits['audit_stages'])==21,'incomplete audit coverage')
    for stage in audits['audit_stages']:
        require(digest((root/stage['public_audit_path']).read_bytes())==stage['public_audit']['sha256'],'public audit identity')
        for item in stage['proof_bindings']:
            require(item['original_identity_in_stage_audit'] is True,'unbound original proof')
            require(digest((root/item['public_path']).read_bytes())==item['public_sha256'],'proof binding mismatch')
    for filename in ('ORIGINAL_IDENTITIES.json','CHECKER_IDENTITIES.json'):
        for item in read_json(root/filename)['files']:
            b=(root/item['path']).read_bytes()
            require(len(b)==item['public_bytes'] and digest(b)==item['public_sha256'],'edition identity mismatch')
    for p in root.rglob('*.md'):
        text=p.read_text()
        for link in re.findall(r'\[[^\n\]]+\]\(([^)\s]+\.(?:md|json|py)(?:#[^)]*)?|https?://[^)]+)\)',text):
            if re.match(r'https?://',link) or link.startswith('#'):continue
            target=(p.parent/link.split('#',1)[0]).resolve()
            require(target.is_relative_to(root.resolve()) and target.is_file(),'broken local document link: '+link)
    return {'status':'PASS','verified_files':len(files),'problem_status':'UNSOLVED','substantive_passes':5,'resolution_claimed':False,'scope':'Byte integrity, exact formulation, public-edition bindings and local links; mathematical proofs retain their stated scope.'}
if __name__=='__main__':
    print(json.dumps(verify(),sort_keys=True,indent=2))
