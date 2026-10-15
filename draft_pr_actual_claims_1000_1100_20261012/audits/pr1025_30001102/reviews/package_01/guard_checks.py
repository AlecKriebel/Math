#!/usr/bin/env python3
"""Independent black-box attacks on proposed runner guards, in review-local files."""
import importlib.util,pathlib,json,sys,subprocess,hashlib
BASE=pathlib.Path(__file__).resolve().parent
PUBLICATION=BASE.parents[1]/'publication'
spec=importlib.util.spec_from_file_location('reviewed_runner',PUBLICATION/'run_checks.py')
runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
CHILD=BASE/'reproduction/guard_children';CHILD.mkdir(exist_ok=True)
runner.ROOT=CHILD
rows=[]
def checked(name,func):
    try:func()
    except RuntimeError as e:rows.append({'name':name,'status':'REJECTED','reason':str(e)});return
    raise RuntimeError('guard unexpectedly accepted '+name)

def child(name,source):
    path=CHILD/(name+'.py');path.write_text(source);return path

for mode in (0,1,2):
    good=child('good',"import json,sys\nprint(json.dumps({'optimization_mode':sys.flags.optimize},sort_keys=True))\n")
    expected={'exit':0,'stdout':json.dumps({'optimization_mode':mode},sort_keys=True)+'\n','stderr':''}
    result=runner.execute(good,mode,[],expected,'guard_positive')
    rows.append({'name':'positive_mode_'+str(mode),'status':'PASS','stdout_sha256':result['stdout_sha256']})
    checked('stdout_suffix_mode_'+str(mode),lambda:runner.execute(child('suffix',"import json,sys\nprint(json.dumps({'optimization_mode':sys.flags.optimize},sort_keys=True))\nprint('extra')\n"),mode,[],expected,'attack'))
    checked('stderr_mode_'+str(mode),lambda:runner.execute(child('stderr',"import json,sys\nprint(json.dumps({'optimization_mode':sys.flags.optimize},sort_keys=True))\nprint('unexpected',file=sys.stderr)\n"),mode,[],expected,'attack'))
    checked('exit_mode_'+str(mode),lambda:runner.execute(child('exit',"import json,sys\nprint(json.dumps({'optimization_mode':sys.flags.optimize},sort_keys=True))\nraise SystemExit(7)\n"),mode,[],expected,'attack'))
    checked('float_mode_'+str(mode),lambda:runner.execute(child('float',"import json,sys\nprint(json.dumps({'optimization_mode':float(sys.flags.optimize)},sort_keys=True))\n"),mode,[],{'exit':0,'stdout':json.dumps({'optimization_mode':float(mode)},sort_keys=True)+'\n','stderr':''},'attack'))
    checked('wrong_mode_'+str(mode),lambda:runner.execute(child('wrong',"import json,sys\nprint(json.dumps({'optimization_mode':(sys.flags.optimize+1)%3},sort_keys=True))\n"),mode,[],{'exit':0,'stdout':json.dumps({'optimization_mode':(mode+1)%3},sort_keys=True)+'\n','stderr':''},'attack'))
    checked('crash_mode_'+str(mode),lambda:runner.execute(child('crash',"raise SyntaxError('unrelated source failure')\n"),mode,[],{'exit':1,'stdout':json.dumps({'status':'INTENDED_REJECTION','reason':'threshold exact reconstruction','mutation':'omit_negative_layers'},sort_keys=True)+'\n','stderr':''},'attack'))

for name,a,b in [('bool_int',{'x':[True]},{'x':[1]}),('float_int',{'x':[1.0]},{'x':[1]}),('list_tuple',[1],(1,)),('missing_key',{'x':1},{'x':1,'y':0}),('extra_key',{'x':1,'y':0},{'x':1}),('nested_bool',{'x':[{'y':False}]},{'x':[{'y':0}]}),('nested_value',{'x':[{'y':2}]},{'x':[{'y':1}]})]:
    if runner.exact_json_equal(a,b):raise RuntimeError('recursive JSON guard failed '+name)
    rows.append({'name':name,'status':'REJECTED'})
if not runner.exact_json_equal({'a':[1,{'b':None}],'c':True},{'c':True,'a':[1,{'b':None}]}):raise RuntimeError('exact recursive positive failed')
rows.append({'name':'recursive_positive','status':'PASS'})
result={'status':'PASS','guard_controls':len(rows),'runs':rows,'limits':['These checks challenge accidental changes, complete outputs and type confusion; they do not claim a security sandbox or resistance to deliberate source spoofing.']}
(BASE/'reproduction/guard_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='runs'},indent=2))
