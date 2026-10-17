#!/usr/bin/env python3
"""Read-only, fail-closed verification of the final public checkpoint edition."""
from pathlib import Path, PurePosixPath
import ast, hashlib, json, re
ROOT=Path(__file__).resolve().parent

def require(ok,why):
    if not ok: raise ValueError(why)
def sha(data): return hashlib.sha256(data).hexdigest()
def read_json(p):
    def unique(pairs):
        out={}
        for k,v in pairs:
            require(k not in out,'duplicate JSON key');out[k]=v
        return out
    return json.loads(p.read_text(),object_pairs_hook=unique)
def inventory(root):
    out=[]
    for p in root.rglob('*'):
        require(not p.is_symlink(),'symbolic link forbidden')
        if p.is_file(): out.append(p.relative_to(root).as_posix())
    return sorted(out)
def verify(root=ROOT):
    root=Path(root)
    m=read_json(root/'MANIFEST.json')
    require(set(m)=={'schema','status','resolution_claimed','checkpoint','files'},'manifest schema')
    require(m['schema']=='ep168-interim-public-v1','manifest version')
    require(m['status']=='UNSOLVED' and m['resolution_claimed'] is False,'manifest mathematical status')
    require(m['checkpoint']=='partial interim mathematical checkpoint','checkpoint scope mismatch')
    files=m['files'];require(type(files) is list and len(files)>=25,'incomplete manifest')
    paths=[]
    for item in files:
        require(type(item) is dict and set(item)=={'path','bytes','sha256'},'file record schema')
        rel=item['path'];require(type(rel) is str,'path type');q=PurePosixPath(rel)
        require(not q.is_absolute() and '..' not in q.parts and str(q)==rel and rel!='MANIFEST.json','unsafe manifest path')
        require(type(item['bytes']) is int and item['bytes']>=0,'invalid byte count')
        require(type(item['sha256']) is str and re.fullmatch('[0-9a-f]{64}',item['sha256']) is not None,'invalid digest')
        p=root/rel;require(p.is_file() and not p.is_symlink(),'missing regular file')
        raw=p.read_bytes();require(len(raw)==item['bytes'] and sha(raw)==item['sha256'],'file identity mismatch: '+rel)
        paths.append(rel)
    require(paths==sorted(set(paths)),'unordered or duplicate paths')
    require(inventory(root)==sorted(paths+['MANIFEST.json']),'unmanifested or missing files')
    f=read_json(root/'FORMULATION.json')
    required={'F': 'maximum cardinality in the finite integer interval', 'alpha': 'limit as N tends to infinity of F(N)/N', 'arithmetic_question': 'rationality or irrationality remains unresolved', 'avoidance': 'no complete {n,2n,3n}, for every positive integer n', 'checkpoint': 'partial interim mathematical checkpoint', 'domain': '{1,...,N}, N a positive integer', 'f': 'maximum avoiding size in the first k smooth numbers; f(0)=0', 'finite_unrestricted_prefixes': 200, 'global_actual_binary_E_claimed': False, 'global_tau_equals_q1_claimed': False, 'id': 1970, 'label': 'EP-168', 'numeric_arithmetic_cutoff': 192, 'numeric_arithmetic_prefixes': 25, 'pair_ratio_avoidance': False, 'problem': 'Erdos Problem 168', 'q0': 'minimum hitting size with excess D=0', 'q1': 'minimum hitting size with excess D<=1', 'record': 1790, 'resolution_claimed': False, 'restored_historical_bytes_claimed': False, 'schema': 'ep168-interim-formulation-v1', 'smooth_order': 'd_1=1; increasing 2^a*3^b, a,b nonnegative integers', 'status': 'UNSOLVED', 'tau': 'minimum hitting size with unrestricted excess'}
    require(set(f)==set(required),'exact formulation schema')
    for k,v in required.items(): require(type(f.get(k)) is type(v) and f[k]==v,'formulation mismatch: '+k)
    a=read_json(root/'AUDIT_BINDINGS.json')
    require(a['status']=='ACCEPTED' and a['resolution_claimed'] is False,'final independent acceptance missing')
    require(a['binding_kind']=='fresh reconstructed public edition; no historical byte restoration','audit provenance mismatch')
    require(a['global_tau_equals_q1_claimed'] is False and a['global_actual_binary_E_claimed'] is False,'audit scope mismatch')
    proofs=sorted(p for p in paths if p.startswith('proofs/') and p.endswith('.md'))
    require([p['path'] for p in a['proofs']]==proofs,'incomplete proof binding')
    for item in a['proofs']:
        raw=(root/item['path']).read_bytes()
        require(sha(raw)==item['sha256'] and len(raw)==item['bytes'],'proof acceptance binding mismatch')
    report=a['acceptance_report']
    require(set(report)=={'path','bytes','sha256'} and report['path']=='audits/ACCEPTANCE_REPORT.md','acceptance report record')
    require((root/report['path']).is_file(),'missing acceptance report')
    raw=(root/report['path']).read_bytes()
    require(type(report['bytes']) is int and len(raw)==report['bytes'] and sha(raw)==report['sha256'],'acceptance report binding mismatch')
    for p in (root/'checks').rglob('*.py'):
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(p.read_text()))),'optimization-sensitive assertion: '+p.name)
    for p in root.rglob('*.md'):
        for link in re.findall(r'\[[^\n\]]+\]\(([^)\s]+)\)',p.read_text()):
            if link.startswith(('http://','https://','#')): continue
            target=(p.parent/link.split('#')[0]).resolve()
            require(target.is_relative_to(root.resolve()) and target.is_file(),'broken local link: '+link)
    return {'status':'PASS','verified_files':len(files),'problem_status':'UNSOLVED','checkpoint':'partial interim mathematical checkpoint','resolution_claimed':False,'scope':'Byte integrity, exact scope, proof acceptance bindings and links; not a machine proof of analytic theorems.'}
if __name__=='__main__': print(json.dumps(verify(),indent=2,sort_keys=True))
