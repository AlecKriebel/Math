"""Independent SOURCE-ONLY controls. Never invoke high-level capture/finalize."""
import sys
assert sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path
import ast, datetime, hashlib, json, stat, types
from pathlib import Path
OWN=Path(__file__).absolute().parent
CASE=OWN.parent
L=CASE/'logical_capture_preparation_01'
EXPECTED={'bytes':41132,'sha256':'09f0e6ab2c22aae6f611f62cb72340ac9c01be237d38962cd577c3b5e015aed1'}
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
raw=(L/'capture_logical_packet.py').read_bytes()
assert pin(raw)==EXPECTED
cap=types.ModuleType('adversarial_source_only_capture');cap.__file__=str(L/'capture_logical_packet.py')
exec(compile(raw,cap.__file__,'exec'),cap.__dict__)
h,e,c=cap.helpers()
results=[]
def check(name,value):
 assert value,name
 results.append({'name':name,'result':'PASS'})
for name,wanted in [('SOURCE_MANIFEST.json',{'bytes':1585,'sha256':'fadf2dae7fe902d6825d8180361dc0acb0bf418a7fd58ea7f9311478b1eb1575'}),('EXTERNAL_SEAL.json',{'bytes':376,'sha256':'ba42a97d4eff12b91e2a1a350b3d61322d82a0895a3b4e38421acf8dbd83eb52'})]:
 data,unused=cap.read_regular(L/name);check('exact frozen '+name,pin(data)==wanted)
manifest=json.loads((L/'SOURCE_MANIFEST.json').read_bytes())
for row in manifest['files']:
 data,unused=cap.read_regular(L/row['path']);check('manifest closure '+row['path'],pin(data)=={k:row[k] for k in ('bytes','sha256')})
check('manifest exact nine files and aggregate',len(manifest['files'])==9 and manifest['total_files']==9 and sum(r['bytes'] for r in manifest['files'])==manifest['total_bytes']==84181)
provided=types.ModuleType('provided_pure_controls');provided.__file__=str(L/'offline_controls.py')
exec(compile((L/'offline_controls.py').read_bytes(),provided.__file__,'exec'),provided.__dict__)
baseline=provided.run_controls()
check('provided exact-source controls all pass',baseline['passed']==67)

# Fresh root exposes only the opaque attempt tuple. No attempt envelope exists.
calls=[]
opaque='a'*40
def tree(entries):return c.tree_hash([(name,*node) for name,node in entries.items()])
entries={'30001321':('040000','tree',opaque)};attempts=tree(entries)
entries2={'attempts':('040000','tree',attempts)};priority=tree(entries2)
entries3={'unsolved_math_prioritization':('040000','tree',priority)};root=tree(entries3)
saved={root:entries3,priority:entries2,attempts:entries}
def replay(method,route,body=None):
 calls.append(route)
 assert method=='GET' and body is None
 oid=route.rsplit('/',1)[1]
 if oid not in saved:raise RuntimeError('Opaque subtree envelope intentionally unavailable')
 return {'sha':oid,'truncated':False,'tree':[{'path':n,'mode':v[0],'type':v[1],'sha':v[2]} for n,v in sorted(saved[oid].items())]}
trees=c.NativeTrees(replay)
check('fresh lookup returns opaque attempt tuple',trees.lookup(root,h.ATTEMPT)==('040000','tree',opaque))
before=list(calls)
opaque_failure=None
try:cap.projected_attempt(h,c,trees,root,{}, {})
except RuntimeError as exc:opaque_failure=str(exc)
check('F01 empty overlay unnecessarily requests opaque attempt envelope',opaque_failure=='Opaque subtree envelope intentionally unavailable' and calls==before+['git/trees/'+opaque])

# The final source selector admits an optional prior-case target independently
# of the accepted carry inventory; strict model load_inputs requires membership.
def row(path,p,oid):return {'path':path,'origin':str(cap.ENGINE/'BASELINE_MEMBERSHIP.json'),**p,'git_blob':oid,'observed_source_mode':292,'role':'SYNTHETIC_METADATA_CONTROL','selection_basis':'No body is read by this metadata control'}
rows=[row(p,v,'1'*40) for p,v in cap.required_carry(h).items()]
rows += [row(p,{k:v[k] for k in ('bytes','sha256')},v['native_blob']) for p,v in h.original_archives().items()]
extra=h.OLD_CASE+'extra_public_metadata.json'
rows.append(row(extra,{'bytes':1,'sha256':'2'*64},'3'*40))
plan={'schema':'pr239-root-positive-public-selection-v1','PR':239,'operational_authority':False,'files':rows,'total_files':len(rows),'total_bytes':sum(r['bytes'] for r in rows)}
selected=cap.selection(h,plan,'completion100',True)
carrypins=cap.required_carry(h)
check('F02 final selection accepts prior target outside minimal carry',extra in selected and extra not in carrypins)
check('F02 strict model target predicate rejects same uncatalogued prior target',not(extra in h.VIEWS or h.public_path(extra) or extra in carrypins or h.science_path(extra)))

# Scope guard binds exact origins but does not classify their contents.
plan2=json.loads(json.dumps(plan));plan2['files'][-1]['path']=h.CASE+'public_note.json'
plan2['files'][-1]['origin']=str(cap.ENGINE/'ROOT_COMPLETE239_READ_SYNTHETIC'/'00001.RAW_STDOUT.json')
check('L01 target filter alone does not enforce private-origin exclusion',h.CASE+'public_note.json' in cap.selection(h,plan2,'completion100',True))
print(json.dumps({'schema':'pr239-independent-logical-capture-source-adversary-controls-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_pin':EXPECTED,'scope':'PURE_FUNCTIONS_AST_AND_READONLY_FROZEN_INPUTS_ONLY','no_high_level_capture_finalize_source_guard_Output_API_Seed_Runtime_lock_or_external_effect':True,'provided_controls_passed':baseline['passed'],'independent_controls_passed':len(results),'results':results,'findings':['F01: empty attempt overlay descends opaque attempt tree','F02: prior-case final target can be outside accepted carry inventory'],'limits':['No high-level capture/finalize or actual config/selection/packet gate was executed.','L01 is a Root exact-selection review obligation, not a demonstrated secret export.']},sort_keys=True,indent=2))
