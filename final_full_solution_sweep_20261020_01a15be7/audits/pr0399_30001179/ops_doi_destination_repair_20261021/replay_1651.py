#!/usr/bin/env python3
"""All previous1651 logic; exact five truthful destination-proof fixture changes."""
from pathlib import Path
import argparse,builtins,difflib,hashlib,io,json,sys,types
from contextlib import redirect_stdout
from unittest.mock import patch
H=Path(__file__).resolve().parent;A=H.parent;O=H/'pre_destination_binding';OLD=O/'ops_record_url_repair_20261021'
NAMES=['ops_binding','prepublication_check','publication_live_gates','repository_integration','verify_published_files','publication_lifecycle','record_publication_ledger']
FIND="'doi_resolution':{'status':200}"
REPLACE="'doi_resolution':{'status':200,'resolved_url':'https://zenodo.org/records/999','destination_verified':{'policy':'pr399-exact-https-record-v1','record':999,'status':200,'resolved_url':'https://zenodo.org/records/999'}}"

def load(name,body,path):
 module=types.ModuleType(name);module.__file__=str(path);sys.modules[name]=module;exec(compile(body,str(path),'exec'),module.__dict__);return module

def implementation(kind='canonical'):
 for n in NAMES:load(n,(A/(n+'.py')).read_bytes(),A/(n+'.py'))
 return tuple(sys.modules[n] for n in NAMES)

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args();output=args.output
 if not output.is_absolute() or not output.is_relative_to(A.parents[1]/'private'):raise RuntimeError('New private output required')
 output.mkdir(parents=True,exist_ok=False);prior=sys.argv;sys.argv=[sys.argv[0],'--canonical'];adapted=[];diff=[];executed=[]
 support=load('controls_support',(OLD/'controls_support.py').read_bytes(),OLD/'controls_support.py');support.AUDIT=A;support.implementation=implementation
 previous=OLD/'pre_record_url_binding/ops_identity_repair_20261021'
 expected={str(OLD/'current_controls.py'):(OLD/'current_controls.py').read_bytes(),str(A/'ops_identity_repair_20261021/integrated_controls.py'):(previous/'integrated_controls.py').read_bytes(),str(A/'ops_identity_repair_20261021/repair_controls.py'):(previous/'repair_controls.py').read_bytes()}
 reg=load('calculate_old_directory_adapter',(previous/'replay_regressions.py').read_bytes(),previous/'replay_regressions.py')
 for name in ['offline_controls.py','repair_controls.py']:
  original=(previous/'pre_review02_binding/publication_operations_preparation'/name).read_text();expected['preserved_regression_fixture/'+name]=reg.adapt(name,original)[0].encode()
 original_compile=builtins.compile
 def fixture_compile(source,filename,mode,*a,**k):
  if str(filename) in expected and mode=='exec':
   body=source.encode() if isinstance(source,str) else source
   if body!=expected[str(filename)] or body.decode().count(FIND)!=1:raise RuntimeError('Expected unchanged fixture source shape '+str(filename))
   changed=body.decode().replace(FIND,REPLACE);adapted.append({'compile_path':str(filename),'verified_before_sha256':hashlib.sha256(body).hexdigest(),'adapted_sha256':hashlib.sha256(changed.encode()).hexdigest(),'changes':1})
   diff.extend(difflib.unified_diff(body.decode().splitlines(keepends=True),changed.splitlines(keepends=True),fromfile='unchanged1651/'+str(filename),tofile='destination_fixture_only/'+str(filename)))
   source=changed
  return original_compile(source,filename,mode,*a,**k)
 try:
  with patch.object(builtins,'compile',fixture_compile):
   for name in ['current_controls.py','replay_530.py','external_controls.py']:
    sys.modules['controls_support']=support;body=(OLD/name).read_bytes();module=load('old1651_'+name.removesuffix('.py'),body,OLD/name)
    if name=='replay_530.py':module.OUTPUT_ROOT=output
    else:module.HERE=output
    with redirect_stdout(io.StringIO()):module.main()
    executed.append({'path':'ops_record_url_repair_20261021/'+name,'sha256':hashlib.sha256(body).hexdigest()})
 finally:sys.argv=prior
 mode='optimized' if sys.flags.optimize else 'normal';current=json.loads((output/('CURRENT_CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'CURRENT_CONTROLS.json')).read_bytes());old=json.loads((output/('prior530_canonical_'+mode)/'REPLAY_RECEIPT.json').read_bytes());bench=json.loads((output/('ROOT_BENCHMARK_canonical_'+mode+'.json')).read_bytes())
 if len(adapted)!=5 or current['controls']!=818 or old['controls']!=530 or bench['conservative_positive_cases']!=296 or len(bench['negative_cases'])!=7 or bench['positive_outcomes']['silently_missed']:raise RuntimeError('All prior obligations or exact five fixture changes not met')
 result={'optimization':sys.flags.optimize,'all_previous_controls':1651,'new_route_controls':818,'older_regressions':530,'root_benchmark':303,'all_passed':True,'actual_provider_attempts':0,'executed_old_programs':executed,'fixture_only_adaptations':adapted,'expected_verdicts_changed':False,'production_guard_bypass_added':False,'old_directory_fixture_adapter_retained':True,'cached_ledger_rows':176}
 (output/'FIXTURE_ADAPTATION.diff').write_text(''.join(diff));(output/'REPLAY_1651.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in {'executed_old_programs','fixture_only_adaptations'}},indent=2))
if __name__=='__main__':main()
