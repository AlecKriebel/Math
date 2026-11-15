"""Verify this planning packet; optionally recheck current applicability. No writes."""
from pathlib import Path
import hashlib,json,sys,subprocess
sys.dont_write_bytecode=True
O=Path(__file__).resolve().parent
def need(x,m):
    if not x:raise RuntimeError(m)
def load(p):return json.loads(p.read_text())
def bind(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
need(sys.argv[1:] in [[],['--check-current-mechanics']],'Optional --check-current-mechanics only')
s=load(O/'FINAL_SEAL.json');m=load(O/'OWNED_MANIFEST.json')
need(bind(O/'OWNED_MANIFEST.json')['sha256']==s['manifest_sha256'],'Owned manifest seal')
need({str(x.relative_to(O)) for x in O.rglob('*') if x.is_file()}=={x['path'] for x in m['files']}|{'OWNED_MANIFEST.json','FINAL_SEAL.json'},'Closed owned inventory')
for x in m['files']:need(bind(O/x['path'])=={k:x[k] for k in ['bytes','sha256']},'Owned '+x['path'])
inputs=load(O/'INPUT_BINDINGS.json')
for x in inputs:need(bind(Path(x['path']))=={k:x[k] for k in ['bytes','sha256']},'Selected source/core input '+x['path'])
v=load(O/'VERDICT.json');t=load(O/'TARGET_SCHEMA_NOTES.json')
need(set(t)=={'23124601','23333046','23383952','23539734','22929857','23320818'},'Exact six records')
need(v['literal_custom_verdict']=='PLANNING_ONLY_WAITING_ROOT_COPY_ADOPTIONS_AND_PRIVATE_STAGE_AUTHORIZATION','Literal custom verdict')
need(v['planned_overlay_paths']==len(t)*4+2==26 and v['planned_new_article_files']==24,'Conditional ownership arithmetic')
need(v['conditional_future_counts']==[v['observed_public_counts'][0]+24,v['observed_public_counts'][1]+6,v['observed_public_counts'][2]+6],'Conditional count arithmetic')
need(all(x['current_canonical_url'] is None and x['AA'] is None and x['additional_assets']==[] and x['target_public_directory_absent_at_plan'] for x in t.values()),'Historical private metadata observation')
need(not any(v[k] for k in ['implementation_created','private_stage_run','production_writes','old_campaigns_replayed','publication_authority']),'Planning-only boundary')
if sys.argv[1:]:
    ob=load(O/'OBSERVED_CURRENT_MECHANICS.json')
    for x in ob['selected_website_bindings']:need(bind(Path(x['path']))=={k:x[k] for k in ['bytes','sha256']},'Current selected website applicability')
    site=Path(ob['selected_website_bindings'][0]['path']).parents[2]
    need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=site,text=True).strip()==ob['website_HEAD'],'Current website HEAD applicability')
print(json.dumps({'status':'PASS','owned_payloads':len(m['files']),'selected_source_core_bindings':len(inputs),'target_count':len(t),'planning_only':True,'implementation_or_render_run':False,'current_mechanics_checked':bool(sys.argv[1:]),'writes':0,'network':0},sort_keys=True))
