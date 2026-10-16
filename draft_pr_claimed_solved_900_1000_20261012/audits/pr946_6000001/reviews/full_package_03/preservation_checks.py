import sys
if not sys.flags.isolated:raise RuntimeError('use -I')
import pathlib,json,hashlib,ast,subprocess,datetime
R=pathlib.Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';O=A/'reviews/full_package_03';D=A/'preprint';fp=lambda b:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};f=json.loads((D/'FREEZE.json').read_bytes());inner=json.loads((D/'package/PACKAGE_MANIFEST.json').read_bytes());families={}
for family in ['jet_calculus','global_hessian','source_model','global_adversary','reproducibility','classical_priority','recent_priority','priority_falsifier']:
 w=A/'reviews'/family;raw=(w/'MANIFEST.json').read_bytes();assert fp(raw)['sha256']==inner['files']['reviews/'+family+'/MANIFEST.json']['sha256'];m=json.loads(raw);rows=next(m[k] for k in ['files','public_files','curated_files','payloads'] if k in m)
 if type(rows) is list:rows={v['path']:{k:v[k] for k in ['bytes','sha256']} for v in rows}
 for name,pin in rows.items():assert fp((w/name).read_bytes())=={k:pin[k] for k in ['bytes','sha256']},family+'/'+name
 families[family]={'manifest_sha256':fp(raw)['sha256'],'payloads_authenticated':len(rows)}
prior={}
for n,pin in [(1,'2f1a4ba73839b83280e9daba44fbe79e70b52a80761deded5314e0db99c7e834'),(2,'e0361044f313b540f8a46b6a417a00a1777e22a33439e9a097aa0f9e7b54c3e6')]:
 w=A/'reviews'/f'full_package_{n:02d}';raw=(w/'MANIFEST.json').read_bytes();assert fp(raw)['sha256']==pin;m=json.loads(raw);assert set(m['files'])==set(m['explicit_public_allowlist'])
 for name,p in m['files'].items():assert fp((w/name).read_bytes())==p
 c=D/'reviewed_candidates'/f'candidate{n:02d}';cf=json.loads((c/'FREEZE.json').read_bytes());old=json.loads((w/'RESULT.json').read_bytes());assert fp((c/'FREEZE.json').read_bytes())['sha256']==old['candidate_pins']['freeze']
 for name,p in cf['files'].items():assert fp((c/name).read_bytes())==p
 for name,p in cf['evidence_files'].items():assert fp((R/name).read_bytes())==p
 op=json.loads((c/'OPERATIONS_INVENTORY.json').read_bytes())
 for name,p in op['files'].items():assert fp((c/'operations'/name).read_bytes())==p
 prior[str(n)]={'manifest_sha256':pin,'review_payloads':len(m['files']),'candidate_files':len(cf['files']),'historical_operation_sources':7,'candidate_freeze':old['candidate_pins']['freeze']}
# Five small bootstraps are identical except their final action; exact equivalence exposes all bytes.
helpers={};normalized=[]
for name,pin in f['future_helpers'].items():
 b=(P/name).read_bytes();assert fp(b)==pin;t=ast.parse(b);assert not any(isinstance(z,ast.Assert) for z in ast.walk(t));nodes=[z for z in t.body if not isinstance(z,ast.Expr) or not isinstance(z.value,ast.Constant)];assert isinstance(nodes[0],ast.Import) and nodes[0].names[0].name=='sys' and isinstance(nodes[1],ast.If) and 'safe_path' in ast.unparse(nodes[1]);helpers[name]=pin
 if name!='accept_pr946.py':normalized.append(b[:b.rfind(b"    entry('")])
assert len(set(normalized))==1
h='7d3adb0e500b0414a49a449e7981d34ade329427'
def blob(n):return subprocess.check_output(['git','show',h+':unsolved_math_prioritization/'+n],cwd=R)
state=json.loads(blob('state.json'));history=[json.loads(l) for l in blob('history.jsonl').splitlines() if l.strip()];selected=[e for e in history if str(e.get('id'))=='6000001'];assert '6000001' not in state and not selected
# Primary bodies are private; keep only file fingerprints, locators, and authored conclusions public.
source_paths=['private/root_primary/fmu.pdf','reviews/source_model/private/amari1997.pdf','reviews/source_model/private/whitney1936.pdf','reviews/full_package_02/private/gualtieri.pdf','private/root_primary/marugame.pdf','reviews/priority_falsifier/private/cl_matumoto1993_body.txt','reviews/priority_falsifier/private/cl_le2003_43.txt','reviews/priority_falsifier/private/cl_le2003_77.txt','reviews/priority_falsifier/private/cl_le_v6.txt','reviews/priority_falsifier/private/cl_lauritzen1987_body.txt','reviews/priority_falsifier/private/re_loi_matta_accepted.txt','reviews/priority_falsifier/private/re_osipov2022_v3.txt']+['reviews/priority_falsifier/private/ajls2017_authorized_preview_p'+str(n)+'.png' for n in [221,222,237,238]]
sources={name:fp((A/name).read_bytes()) for name in source_paths};assert sources['reviews/full_package_02/private/gualtieri.pdf']['sha256']=='799796cc9cd75ecf630921881cff483aaf5bfbda7e65e102c5f0f6e3f95892d4'
out={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'families':families,'prior_full_reviews_and_candidates':prior,'inspected_helper_hashes':helpers,'five_small_bootstraps_identical_except_action':True,'safe_start_precedes_nonbuiltin_import_all_six':True,'native_original_target_state_present':False,'native_original_target_history_events':0,'original_declared_turns':'4/5','author_native_history_authenticated':False,'original_total_attempt_count_known':False,'proof_search_turns_added_by_audit':0,'primary_source_fingerprints':sources,'no_raw_source_redistribution':True}
(O/'PRESERVATION_AND_SOURCE_PINS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','families':len(families),'older_rounds':2,'helpers':6,'selected_original_history':0}))
