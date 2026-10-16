import sys,os,json,stat,hashlib,subprocess,datetime
from pathlib import Path
sys.dont_write_bytecode=True
A=Path(__file__).resolve().parents[1];R=A/'reviews/package_05';P=A/'NEWpreprint_v1_0';O=A/'root_reproduction/whole05_20261016';O.mkdir(exist_ok=True)
def need(c,s):
 if not c:raise RuntimeError(s)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def match(p,r):return p.stat().st_size==r.get('bytes',r.get('size')) and sha(p)==r['sha256']
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
freeze=load(R/'INPUT_FREEZE.json')['files'];pins=load(R/'OUTPUT_PINS.json');seal=load(R/'SEAL.json')
need(match(R/'OUTPUT_PINS.json',seal['output_pins']),'seal')
for row in freeze:need(match(A/row['path'],row) and stat.S_IMODE((A/row['path']).stat().st_mode)==row['mode'],'frozen input')
for row in pins['records']:
 p=R/row['path'];need(not p.is_symlink() and match(p,row) and stat.S_IMODE(p.stat().st_mode)==row['mode'] and p.stat().st_nlink==row['nlink'],'settled output')
for row in pins['symlink_fixtures']:
 p=R/row['path'];need(p.is_symlink() and str(p.readlink())==row['target'] and stat.S_IMODE(p.lstat().st_mode)==row['mode'],'owned symlink fixture')
for row in load(R/'SOURCE_READ_LEDGER.json')['sources']:
 need(match(Path(row['path']),row),'source identity')
 if 'text_identity' in row:need(match(Path(row['text_identity']['path']),row['text_identity']),'text identity')
src=(R/'math05.py').read_text().replace('R=Path(__file__).resolve().parent','R=Path('+repr(str(O))+')');(O/'math_replay.py').write_text(src)
src=(R/'guard05.py').read_text().replace("R=Path(__file__).resolve().parent;P=R.parents[1]/'NEWpreprint_v1_0'","R=Path("+repr(str(O))+");P=Path("+repr(str(P))+")");(O/'guard_replay.py').write_text(src)
src=(R/'custody05.py').read_text().replace("R=Path(__file__).resolve().parent;A=R.parents[1];P=A/'NEWpreprint_v1_0'","R=Path("+repr(str(O))+");A=Path("+repr(str(A))+");P=A/'NEWpreprint_v1_0'");(O/'custody_replay.py').write_text(src)
receipts=[]
def run(argv):
 e=os.environ.copy();e['PYTHONDONTWRITEBYTECODE']='1';p=subprocess.run(argv,cwd=O,env=e,capture_output=True,text=True);receipts.append({'argv':argv,'cwd':str(O),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr});save(O/'ACTUAL_COMMANDS.json',receipts);need(p.returncode==0,'actual command failed')
for runtime,tag in [('/opt/homebrew/bin/python3.11','py311'),('/opt/homebrew/bin/python3.14','py314')]:
 for flags,mode in [([], 'normal'),(['-O'],'optimized')]:
  run([runtime,'-B',*flags,str(O/'guard_replay.py'),tag+'-'+mode]);need(load(O/('GUARDS_'+tag+'-'+mode+'.json'))==load(R/('GUARDS_'+tag+'-'+mode+'.json')),'all guard JSON')
for flags in [[],['-O']]:
 run(['/opt/homebrew/bin/python3.14','-B',*flags,str(O/'math_replay.py')]);need(load(O/'NEW_MATH_CONTROLS.json')==load(R/'NEW_MATH_CONTROLS.json'),'all new exact Brownian/nonnested controls')
 run(['/opt/homebrew/bin/python3.14','-B',*flags,str(O/'custody_replay.py')]);x=load(O/'CUSTODY_FULL_REPLAY.json');y=load(R/'CUSTODY_FULL_REPLAY.json');x.pop('utc');y.pop('utc');need(x==y,'complete custody JSON')
for row in freeze:need(match(A/row['path'],row),'postrun input')
for row in pins['records']:need(match(R/row['path'],row),'postrun output')
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_ADOPT_COMPLETE_WHOLE05_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN','ROOT_full_REPORT_independent_analytic_derivation_source_ledger_new_math_guard_custody_code_and_failed_attempt_ledger_read':True,'frozen_regular_inputs':len(freeze),'settled_regular_outputs':len(pins['records']),'owned_fixture_symlinks':len(pins['symlink_fixtures']),'all_frozen_input_size_hash_mode_and_output_size_hash_mode_nlink_and_symlink_targets_checked':True,'output_pins_sha256':sha(R/'OUTPUT_PINS.json'),'review_seal_sha256':sha(R/'SEAL.json'),'actual_root_commands':receipts,'complete_new_exact_math_and_guard_JSON_equals_reviewer':True,'reproduced_full_custody':x,'whole_reviews_completed':5,'minimum_whole_reviews':2,'finding_counts':{'P0':0,'P1':0,'P2':0,'P3':0},'new_complete_whole_review_currently_required':False,'terminal_administration_and_root_final_integrity_required':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'scope':'All fixed H in(1/4,1),T>0,n>=1,every L2 estimator from both uniform grids; independent standard equal-H components and canonical iterated integral. Brownian optimum/smooth rate prior; no endpoint/sharp/H-uniform/adaptive/nonuniform/unequal/correlated claim.','source_boundary':'Actual reviewer primary-body/interface scopes and journal/v1 distinction read; root rehashed10source identities and7text identities. Dickinson/full Jackowski implications, full novelty/method priority/worldwide openness UNKNOWN; no journal-error or publisher-byte identity claim.','PDF_scope':'Reviewer actual all7 delivered page pixels viewed and four supported-runtime/mode compile/PDF rebuilds byte-equal; ROOT did not repeat compilation/render during adoption.','execution_history':'306 recorded actual children=57success248intendedreject1retainedunexpected custody-harness failure. Initial ENOSPC recorder childexit UNKNOWN and not counted complete; actual later fully recorded retry passed. Review-local quoting/schema/prefix association errors corrected without candidate changes.','historical_order_scope':'939 additional1558 global positions differ; multiset/per-stage internal order/first2788/all4346 byte resolutions true. Current explicit qualification supersedes old raw false claim without rewriting historical records.','candidate_and_prior_sealed_records_unchanged':True}
save(A/'ROOT_WHOLE_PACKAGE_REVIEW_05.json',record)
print(json.dumps({'status':'PASS_ROOT_ADOPTED_WHOLE05_ZERO_TERMINAL_ADMIN_REQUIRED','commands':len(receipts),'inputs':len(freeze),'outputs':len(pins['records']),'custody_checks':x['all_hash_checks']}))
