#!/usr/bin/env python3
"""Offline regression of all five first-review findings. No operational main."""
import ast,copy,hashlib,importlib.util,json,re,shutil,sys,tempfile
from pathlib import Path
P=Path(__file__).resolve().parent;A=P/'audits/pr938_30003634';D=A/'publication'
SEAL='37feff8cb31bbef2b7f41b98d8f34571923e7a89cb4c8f53226ccd2adf388a91'
def need(ok,label):
 if not ok:raise RuntimeError(label)
def module(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def rejects(fn,*args):
 try:fn(*args)
 except (RuntimeError,ValueError,KeyError,TypeError):return True
 return False
def main():
 accept=module(P/'accept_pr938.py','acceptance_regression');merge=module(P/'merge_pr938.py','merge_regression');verify=module(D/'verify_package.py','package_regression')
 first=A/'reviews/full_package_01';raw=(first/'MANIFEST.json').read_bytes();need(hashlib.sha256(raw).hexdigest()==SEAL,'First-review external seal drift');mapping=json.loads(raw);accept.authenticate_review_records(first,mapping)
 pin='a'*64;seq=lambda *ns:[str(n).zfill(2)+':'+pin for n in ns]
 for good in [seq(1,2),seq(1,2,3)]:accept.validate_review_sequence(good)
 for bad in [seq(1,3),seq(2,1),seq(1,1),seq(1,2,4),seq(1)]:need(rejects(accept.validate_review_sequence,bad),'R1 sequence accepted')
 empty={'files':{},'explicit_public_allowlist':[]};need(rejects(accept.validate_review_inventory,empty),'R2 empty map accepted')
 missing=copy.deepcopy(mapping);missing['files'].pop('RESULT.json');missing['explicit_public_allowlist'].remove('RESULT.json');need(rejects(accept.validate_review_inventory,missing),'R2 unsealed verdict accepted')
 scratch=A/'private/review01_repairs';scratch.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory(dir=scratch) as td:
  folder=Path(td)
  for name in mapping['files']:
   q=folder/name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(first/name,q)
  accept.authenticate_review_records(folder,mapping)
  result=folder/'RESULT.json';x=json.loads(result.read_text());x['clean_for_preprint']=True;x['required_issues']=[];result.write_text(json.dumps(x))
  need(rejects(accept.authenticate_review_records,folder,mapping),'R2 mutated sealed verdict accepted')
 body='exact reviewed description\n';freeze={'pr_description_sha256':hashlib.sha256(body.encode()).hexdigest()};merge.require_reviewed_description({'body':body},freeze)
 for bad in [{'body':body+'unreviewed'},{'body':None},{}]:need(rejects(merge.require_reviewed_description,bad,freeze),'R3 body drift accepted')
 view_tree=ast.parse((P/'merge_pr938.py').read_text());view=next(n for n in view_tree.body if isinstance(n,ast.FunctionDef) and n.name=='view');need(any(isinstance(n,ast.Constant) and isinstance(n.value,str) and 'mergeStateStatus,body' in n.value for n in ast.walk(view)),'R3 actual view omits body')
 expected={'n':1,'m':3,'goeritz_inertia':[23,25,0]};verify.equivalent(copy.deepcopy(expected),expected)
 for key,value in [('n',True),('m',3.0),('goeritz_inertia',[23,25,False])]:
  altered=copy.deepcopy(expected);altered[key]=value;need(altered==expected and rejects(verify.equivalent,altered,expected),'O1 scalar false equivalence accepted')
 observed=[]
 for filename in ['append_pr938_tracker.py','update_pr938_publication_ledger.py']:
  # Execute the actual pure range function, without importing the native writer's
  # deliberately nonoptimized-only module or calling any operational main.
  tree=ast.parse((P/filename).read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='valid_tracker_range');ns={'re':re};exec(compile(ast.Module(body=[fn],type_ignores=[]),str(P/filename),'exec'),ns);valid=ns['valid_tracker_range']
  need(valid("'Math Puzzles'!A10:D10"),'O2 valid range rejected')
  bads=["'Other tab'!A10:D10","'Math Puzzles'!B10:E10","'Math Puzzles'!A10:D11","'Math Puzzles'!A1:D1","'Math Puzzles'!A0:D0",None]
  need(all(not valid(x) for x in bads),'O2 wrong destination/span/row accepted')
  link=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='verify_receipt_links');text=ast.unparse(link)
  need('valid_tracker_range' in text and "readback.get('range')" in text,'O2 downstream range/readback guard absent');observed.append(filename)
 need(hashlib.sha256((first/'MANIFEST.json').read_bytes()).hexdigest()==SEAL,'Sealed review changed')
 print(json.dumps({'status':'PASS','actual_parent_optimization':sys.flags.optimize,'operational_mains_called':False,'sealed_review_payloads_authenticated':len(mapping['files']),'R1':{'valid_sequences':2,'invalid_sequences_rejected':5},'R2':{'empty_map_rejected':True,'unsealed_result_rejected':True,'sealed_result_mutation_rejected':True},'R3':{'valid_body_passed':True,'body_drift_or_missing_rejected':3,'actual_view_requests_body':True},'O1':{'strict_bool_float_negative_controls_rejected':3},'O2':{'actual_pure_functions_checked':observed,'invalid_ranges_rejected_each':6,'downstream_exact_readback_range_guards_present':True},'source_first_review_unchanged':True},indent=2))
if __name__=='__main__':main()
