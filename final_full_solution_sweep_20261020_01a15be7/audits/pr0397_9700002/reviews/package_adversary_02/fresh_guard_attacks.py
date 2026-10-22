"""New exact-field and pagination attacks on production functions, offline."""
from pathlib import Path
import ast,copy,hashlib,importlib.util,json,sys
from urllib.parse import urlencode

HERE=Path(__file__).resolve().parent
HOME=HERE/'extracted/congestion-fragmentation-verification'
spec=importlib.util.spec_from_file_location('copied_replay',HOME/'replay.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
binding,policy=r.load_controls(HOME)
runtime={'python':'3.9.6','numpy':'2.0.2','scipy':'1.13.1'}
results=[];rejected=0
def leaves(v,path=''):
    if type(v) is dict:
        for k,item in v.items():yield from leaves(item,path+'/'+k)
    elif type(v) is list:
        for i,item in enumerate(v):yield from leaves(item,path+'/'+str(i))
    else:yield path,v
def set_at(v,path,value):
    keys=path.strip('/').split('/');p=v
    for key in keys[:-1]:p=p[int(key)] if type(p) is list else p[key]
    if type(p) is list:p[int(keys[-1])]=value
    else:p[keys[-1]]=value
for comp,script,expected_path,produced in r.COMPONENTS:
    expected=r.strict_json((HOME/'candidate'/expected_path).read_bytes());base=copy.deepcopy(expected)
    if comp=='portable':
        base.update(runtime);base['checks'][0]=copy.deepcopy(policy['portable_metadata']['public_projection'])
    r.compare_records(expected,base,comp,policy,runtime)
    for path,value in leaves(base):
        if path in policy['float_tolerances'].get(comp,{}):continue
        # Runtime metadata and projection exceptions have exact target requirements.
        if type(value) is bool:changed=not value
        elif type(value) in [int,float]:changed=value+1
        elif type(value) is str:changed=value+'__changed'
        elif value is None:changed='changed'
        else:raise AssertionError(type(value))
        attack=copy.deepcopy(base);set_at(attack,path,changed)
        try:r.compare_records(expected,attack,comp,policy,runtime)
        except Exception as error:rejected+=1
        else:raise AssertionError('Accepted exact leaf mutation '+comp+path)
    results.append({'component':comp,'unapproved_leaf_mutations_rejected':rejected-sum(x['unapproved_leaf_mutations_rejected'] for x in results)})

source=HERE/'bound_prepublication_check.py'
tree=ast.parse(source.read_text())
function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='account_search')
ns={'urlencode':urlencode}
exec(compile(ast.Module(body=[function],type_ignores=[]),str(source),'exec'),ns)
class Client:
    base='https://synthetic.invalid'
    def __init__(self,responses):self.responses=list(responses)
    def request(self,*args):
        if not self.responses:raise AssertionError('unexpected additional request')
        return self.responses.pop(0)
def page(ids,total,next_url=None):
    out={'hits':{'total':total,'hits':[{'id':i} for i in ids]},'links':{}}
    if next_url is not None:out['links']['next']=next_url
    return out
account_results=[]
good=ns['account_search'](Client([page([1],2,'next'),page([2],2)]),'x')
assert good['total']==2 and good['pages']==2 and len(good['records'])==2
account_results.append({'name':'complete two-page distinct records','accepted':True})
fixtures=[('repeated record',[page([1],2,'next'),page([1],2)]),
          ('missing final page',[page([1],2)]),
          ('total changes',[page([1],2,'next'),page([2],3)]),
          ('missing total',[page([],None)]),
          ('inexact total',[page([],{'value':0,'relation':'gte'})]),
          ('negative total',[page([],-1)]),
          ('bool total',[page([],False)]),
          ('pagination loop',[page([1],2,'next'),page([2],2,'next')])]
for name,responses in fixtures:
    try:ns['account_search'](Client(responses),'x')
    except Exception as error:account_results.append({'name':name,'accepted':False,'reason':str(error)})
    else:raise AssertionError('Accepted incomplete account result '+name)
result={'all_assertions_passed':True,'replay_source_sha256':hashlib.sha256((HOME/'replay.py').read_bytes()).hexdigest(),
        'rejected_exact_output_leaves':rejected,'component_counts':results,
        'account_function_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'account_pagination_fixtures':account_results,'offline_only':True}
(HERE/'FRESH_GUARD_ATTACKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
