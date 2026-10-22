import sys,runpy,json,gzip,hashlib,base64,ast
from pathlib import Path
from datetime import datetime,timezone
sys.dont_write_bytecode=True
O=Path(__file__).resolve().parent
P=O.parent/'publication_package_v1'
def digest(b):return hashlib.sha256(b).hexdigest()
def require(v,s):
 if not v:raise RuntimeError(s)
driver=P/'portable_verification_01/verify_portable.py'
api=runpy.run_path(str(driver),run_name='adversarial_import_only')
guards=[]
for label,f in [('require_false',lambda:api['require'](False,'adversarial false')),('JSON_NaN',lambda:api['parsed'](b'{"x":NaN}')),('numeric_inf',lambda:api['finite_tree']({'x':float('inf')})),('numeric_nan',lambda:api['finite_tree']({'x':float('nan')})),('string_inf',lambda:api['finite_tree']({'x':'inf'}))]:
 try:f()
 except RuntimeError:guards.append(label)
 else:raise RuntimeError('driver guard lost '+label)
pins=json.loads((P/'portable_verification_01/INPUT_PINS.json').read_text())['files']
rows=[]
for name,receipt,rawpath,drv in [('fresh',O/'FRESH_PORTABLE_RUN.json',O/'FRESH_PORTABLE_RUN.json.raw.json.gz',driver.read_bytes()),('archived_success',P/'portable_verification_01/PORTABLE_RUN_RECEIPT_02.json',P/'portable_verification_01/PORTABLE_RUN_RECEIPT_02.json.raw.json.gz',driver.read_bytes()),('archived_ENOSPC',P/'portable_verification_01/ATTEMPT_01_RECEIPT.json',P/'portable_verification_01/ATTEMPT_01_RAW.json.gz',gzip.decompress((P/'portable_verification_01/ATTEMPT_01_DRIVER.py.gz').read_bytes()))]:
 r=json.loads(receipt.read_text());compressed=rawpath.read_bytes();raw=json.loads(gzip.decompress(compressed))
 require(r['driver_sha256']==digest(drv),'driver binding '+name)
 require(r['raw_archive_sha256']==digest(compressed) and r['raw_archive_bytes']==len(compressed),'raw binding '+name)
 records={x['case']:x for x in raw['raw_cases']}
 require(len(records)==len(r['cases'])==r['recorded_cases'],'record count '+name)
 for c in r['cases']:
  z=records[c['case']]
  require(c['source_sha256']==pins[c['source']]['sha256'],'source binding')
  require('-B' in z['argv'],'child -B')
  require(('-O' in z['argv'])==c['optimized'],'child mode binding')
  require(z['argv'][0]==r['python_executable'],'interpreter binding')
  for stream in ['stdout','stderr']:
   b=z[stream+'_utf8'].encode() if stream+'_utf8' in z else base64.b64decode(z[stream+'_b64'])
   require(digest(b)==c[stream+'_sha256'] and len(b)==c[stream+'_bytes'],'stream binding '+name+c['case']+stream)
 require(r['input_before_after_equal_including_ctime'],'immutable snapshot '+name)
 if name!='archived_ENOSPC':require(r['status']=='PASS' and len(records)==28 and r['full_valid_runs']==14 and r['intended_false_rejections']==14 and not r['errors'],'success matrix')
 else:require(r['status']=='FAIL' and len(records)==13 and sum('No space left on device' in x for x in r['errors'])==15,'honest failed attempt')
 rows.append({'name':name,'receipt_sha256':digest(receipt.read_bytes()),'raw_sha256':digest(compressed),'bound_cases':len(records),'status':r['status']})
# Verify archived original-to-live repairs alter only assert enforcement in the AST.
class Harden(ast.NodeTransformer):
 def visit_Assert(self,node):
  return ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError',ctx=ast.Load()),args=[] if node.msg is None else [node.msg],keywords=[]),cause=None)],orelse=[])
M=P/'materials';repair=M/'math_algebra_physical_01/repaired_original_controls_01'
semantics=[]
for rel,live in [('verify.py','verify.py'),('independent_review/independent_check.py','independent_review/independent_check.py')]:
 a=ast.parse((M/'original_submitted_head'/rel).read_text());b=ast.parse((repair/'valid'/live).read_text())
 require(ast.dump(Harden().visit(a),include_attributes=False)==ast.dump(b,include_attributes=False),'repair changed nonassert semantic '+rel)
 semantics.append(rel)
# Check every historical physical execution receipt binds raw stdout/stderr.
historical=[]
for rel,key in [('math_algebra_physical_01/original_execution_receipts.json','receipts'),('math_algebra_physical_01/authored_execution_receipts.json',None),('math_algebra_physical_01/repaired_original_controls_01/REPAIR_EXECUTION_RECEIPTS.json',None)]:
 path=M/rel;doc=json.loads(path.read_text());cases=doc[key] if key else doc
 for c in cases:
  for label in ['stdout','stderr']:
   b=(path.parent/c[label+'_file']).read_bytes();require(digest(b)==c[label+'_sha256'],'historical raw '+rel+c['name']+label)
 historical.append({'receipt':rel,'cases_bound':len(cases)})
report={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','driver_probe_optimized':bool(sys.flags.optimize),'driver_guard_rejections':guards,'portable_raw_bindings':rows,'assert_only_AST_repairs':semantics,'historical_raw_bindings':historical,'limits':'This establishes byte/code/flag/output consistency of archived receipts, not independent authentication of past execution. The fresh run was actually executed during this review.'}
(O/'EXECUTION_BINDINGS_CHECK.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
