import sys,os,json,hashlib,subprocess,datetime,collections,stat
from pathlib import Path
sys.dont_write_bytecode=True
A=Path(__file__).resolve().parents[1];R=A/'reviews/package_04';O=A/'root_reproduction/whole04_20261016';O.mkdir(exist_ok=True);P=A/'NEWpreprint_v1_0'
def load(p):return json.loads(p.read_text())
def need(v,s):
 if not v:raise RuntimeError(s)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def match(p,r):return p.is_file() and p.stat().st_size==r['bytes'] and digest(p)==r['sha256']
def save(p,v):p.write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
frozen=load(R/'FROZEN_INPUTS.json')['files'];outs=load(R/'OUTPUT_PINS.json')['files']
for r in frozen:
 p=A/r['path'];need(match(p,r),'frozen '+r['path']);need(oct(stat.S_IMODE(p.stat().st_mode))==r['mode'],'mode '+r['path'])
for r in outs:need(match(R/r['path'],r),'output '+r['path'])
seal=load(R/'SEAL.json');need(digest(R/'OUTPUT_PINS.json')==seal['output_pins_sha256'],'seal')
src=(R/'review04.py').read_text();mathbody=src[src.index('# Fractions-based independent polynomial mechanism.'):src.index('# Metadata/root uploader identity and files.')]
header="import json,math\nfrom fractions import Fraction as F\nfrom pathlib import Path\nO=Path("+repr(str(O))+ ")\ndef need(x,s):\n if not x:raise RuntimeError(s)\ndef save(n,v):(O/n).write_text(json.dumps(v,indent=2,allow_nan=False)+'\\n')\n"
exact="\nremainder=der(der(phi))[:]\nwhile len(remainder)>2:\n k=len(remainder)-3;c=remainder[-1]\n for j,q in enumerate([F(1,7),F(-1),F(1)]):remainder[k+j]-=c*q\n remainder.pop()\nneed(remainder==[F(4,49),F(0)],'exact stationary remainder')\nneed(val(der(der(phi)),F(1,2))==F(-1,8) and 4*F(4,49)+2*F(1,8)==F(113,196),'exact variation')\nv=json.loads((O/'INDEPENDENT_MATH_CHECKS.json').read_text());v['N_g_exact_independent']={'quadratic_stationary_root_equation':'7x^2-7x+1=0','phi_second_modulo_quadratic':'4/49','phi_second_at_half':'-1/8','total_variation':'113/196'};save('INDEPENDENT_MATH_CHECKS.json',v)\n"
(O/'math_replay.py').write_text(header+mathbody+exact)
guard=(R/'guard04.py').read_text().replace("OWN=Path(__file__).resolve().parent;P=OWN.parents[1]/'NEWpreprint_v1_0'","OWN=Path("+repr(str(O))+");P=Path("+repr(str(P))+")")
(O/'guard_replay.py').write_text(guard)
custody=(R/'custody04.py').read_text().replace("ROOT=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent;P=ROOT/'NEWpreprint_v1_0';Q=ROOT/'repairs/portability01'","ROOT=Path("+repr(str(A))+");O=Path("+repr(str(O))+");P=ROOT/'NEWpreprint_v1_0';Q=ROOT/'repairs/portability01'").replace("load(O/'FROZEN_INPUTS.json')","load(Path("+repr(str(R/'FROZEN_INPUTS.json'))+"))")
(O/'custody_replay.py').write_text(custody)
receipts=[]
def run(argv):
 e=os.environ.copy();e['PYTHONDONTWRITEBYTECODE']='1';p=subprocess.run(argv,cwd=O,env=e,capture_output=True,text=True);receipts.append({'argv':argv,'cwd':str(O),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr});save(O/'ACTUAL_COMMANDS.json',receipts);need(p.returncode==0,'actual command failed')
for py in ['/opt/homebrew/bin/python3.11','/opt/homebrew/bin/python3.14']:
 for opt in [[],['-O']]:
  run([py,'-B',*opt,str(O/'math_replay.py')]);need(load(O/'INDEPENDENT_MATH_CHECKS.json')==load(R/'INDEPENDENT_MATH_CHECKS.json'),'math JSON')
  tag=Path(py).name+('_optimized' if opt else '_normal');run([py,'-B',*opt,str(O/'guard_replay.py'),tag]);need(load(O/('GUARD_'+tag+'.json'))==load(R/'FINITE_FAULTS.json'),'guard JSON')
for opt in [[],['-O']]:run(['/opt/homebrew/bin/python3.14','-B',*opt,str(O/'custody_replay.py')])
old=load(A/'repairs/case_alias01/HISTORICAL_STAGE_RESOLUTION.json');new=load(A/'repairs/portability01/HISTORICAL_STAGE_RESOLUTION.json');keys=['stage','captured_path','bytes','sha256'];tu=lambda r:tuple(r[k] for k in keys)
before=list(map(tu,old['additional_terminal_rows']));after=list(map(tu,new['records'][2788:]));mismatch=[i for i,(x,y) in enumerate(zip(before,after)) if x!=y]
need(len(before)==len(after)==1558 and len(mismatch)==939 and mismatch[0]==30,'counterexample quantification');need(collections.Counter(before)==collections.Counter(after),'multiset')
need(list(map(tu,old['records']))==list(map(tu,new['records'][:2788])),'first2788')
for stage in {r[0] for r in before}:need([r for r in before if r[0]==stage]==[r for r in after if r[0]==stage],'stage order')
for r in frozen:need(match(A/r['path'],r),'post replay frozen')
for r in outs:need(match(R/r['path'],r),'post replay output')
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_ADOPT_COMPLETE_WHOLE04_ONE_P3_REPAIR_AND_NEW_WHOLE05_REQUIRED','full_report_initial_frozen_derivation_completion_sources_and_new_control_sources_read':True,'frozen_inputs':len(frozen),'settled_outputs':len(outs),'output_pins_sha256':digest(R/'OUTPUT_PINS.json'),'actual_root_commands':receipts,'same_complete_independent_math_and_fault_JSON':True,'historical_order_finding':{'id':'WHOLE04-P3-01','scope':'Local custody report global order claim only; all historical bytes and per-stage order are preserved. Public paper/README/SUPPLEMENT unaffected.','additional_rows':1558,'mismatched_global_positions':len(mismatch),'first_mismatch_additional_index':mismatch[0],'same_row_multiset':True,'per_stage_order_preserved':True,'first2788_order_preserved':True},'source_access_scope':'Retained primary interfaces read by reviewer; ROOT read complete source ledger. Not a fresh worldwide priority certificate. Dickinson/Jackowski implications and full novelty remain UNKNOWN.','review_attempt_scope':'24 standard child command records retained; outer orchestrator exit was not retained. Earlier actual failures/ENOSPC and corrected local harness retained without invented success.','reviews_completed':4,'minimum_reviews_required':2,'finding_counts':{'P0':0,'P1':0,'P2':0,'P3':1},'new_complete_whole05_required':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'no_candidate_or_prior_review_changed':True}
save(A/'ROOT_WHOLE_PACKAGE_REVIEW_04.json',record)
print(json.dumps({'status':'PASS_ADOPTED_ONE_P3','frozen':len(frozen),'outputs':len(outs),'commands':len(receipts),'order_mismatches':len(mismatch)}))
