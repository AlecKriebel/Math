"""Read-only independent complete replay of producer AST identity claims."""
from pathlib import Path
import ast,hashlib,json,sys
D=Path(__file__).absolute().parent
P=D.parent/'native_administrative_preparation_01'
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def nodes(p):
    return {n.name:n for n in ast.parse(p.read_bytes()).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def dump(n):return ast.dump(n,include_attributes=False)
def run():
    need(sys.version_info[:2]==(3,11),'Producer AST hashing grammar requires Python3.11')
    o=json.loads((P/'AST_DELTA_PROVENANCE.json').read_bytes());prior={}
    for k,r in o['prior_sources'].items():
        p=Path(r['path']);need(pin(p.read_bytes())=={x:r[x]for x in ['bytes','sha256']},'Prior source pin '+k);prior[k]=nodes(p)
    for k,r in o['current_source_pins'].items():need(pin((P/k).read_bytes())==r,'Current source pin '+k)
    verified=[]
    for filename,records in o['definitions'].items():
        new=nodes(P/filename);need(len(new)==len(records)and set(new)=={r['definition']for r in records},'Complete definition set')
        for r in records:
            n=new[r['definition']];nd=dump(n);need(hashlib.sha256(nd.encode()).hexdigest()==r['AST_sha256']and n.lineno==r['line'],'Exact definition hash/line')
            exact=[];same=[]
            for source,ns in prior.items():
                for name,old in ns.items():
                    row={'source':source,'definition':name}
                    if name==n.name:same.append(row)
                    if dump(old)==nd:exact.append(row)
            canon=lambda xs:sorted((x['source'],x['definition'])for x in xs)
            need(canon(exact)==canon(r['exact_matches'])and canon(same)==canon(r['same_name_comparators']),'Complete independently recomputed match sets')
            status='EXACT_AST'if exact else'ADAPTED_AST'if same else'NEW'
            need(status==r['status'],'Definition classification')
            verified.append({'file':filename,'definition':n.name,'status':status,'AST_sha256':r['AST_sha256']})
    return {'schema':'pr212-independent-exact-AST-replay-v1','python':sys.version.split()[0],'status':'PASS','definitions_verified':len(verified),'exact':sum(r['status']=='EXACT_AST'for r in verified),'adapted':sum(r['status']=='ADAPTED_AST'for r in verified),'new':sum(r['status']=='NEW'for r in verified),'all_exact_matches_same_named_comparators_current_prior_pins_and_lines_recomputed':True,'records':verified,'production_execution_or_acceptance':False,'AST_identity_does_not_transfer_case_authority':True}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
