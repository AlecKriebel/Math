from pathlib import Path
import datetime,hashlib,json,os
A=Path(__file__).resolve().parent;C=A.parents[2]
def require(c,m):
 if not c:raise RuntimeError(m)
def load(p):return json.loads(p.read_text())
def pin(p):
 b=p.read_bytes();return {'file':str(p.relative_to(C)) if p.is_relative_to(C) else str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def verify(base,row):
 p=Path(row['path']);p=p if p.is_absolute() else base/p
 require(p.is_file() and not p.is_symlink(),'missing/nonregular pin: '+str(p));b=p.read_bytes()
 require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'pin mismatch: '+str(p));return pin(p)
records=[];selected=[]
name='priority_exact_question_history_20261006';D=A/name;I=load(D/'INPUT_MANIFEST.json');M=load(D/'OUTPUT_MANIFEST.json');V=load(D/'VERDICT.json')
require(not V['novel_resolution_clearance'] and not V['restricted_strengthening_clearance'] and V['restriction_comparison']['same_restricted_theorem_bundle'],'history verdict')
checked=[verify(D,r) for r in I['inputs']+I['cross_family_inputs']+M['files']]
public=[str((D/r['path']).relative_to(C)) for r in M['files'] if not r['private']]+[str((D/'OUTPUT_MANIFEST.json').relative_to(C))]
records.append({'family':name,'verdict':V,'checked_pins':checked,'manifest':pin(D/'OUTPUT_MANIFEST.json'),'public_paths':public});selected+=public
name='priority_classical_network_mechanisms_20261006';D=A/name;M=load(D/'MANIFEST.json');V=load(D/'VERDICT.json')
require(V['status']=='prior_corollary_established' and len(V['covered_restrictions'])>=12,'network verdict')
checked=[verify(D,r) for r in M['public_outputs']+M['excluded_private_source_receipts']]
public=[str((D/r['path']).relative_to(C)) for r in M['public_outputs']]+[str((D/'MANIFEST.json').relative_to(C))]
records.append({'family':name,'verdict':V,'checked_pins':checked,'manifest':pin(D/'MANIFEST.json'),'public_paths':public});selected+=public
name='priority_wong_integer_formulation_20261006';D=A/name;M=load(D/'MANIFEST.json');I=load(D/'INPUT_PINS.json');V=load(D/'VERDICT.json')
require(not V['novel_resolution_clearance'] and not V['novel_restricted_hardness_clearance'],'Wong verdict')
checked=[verify(D,r) for r in I['files']+M['files']]
public=[str((D/p).relative_to(C)) for p in M['selected_public_outputs']]+[str((D/'MANIFEST.json').relative_to(C))]
require(all('private_sources' not in Path(p).parts for p in public),'private selected')
records.append({'family':name,'verdict':V,'checked_pins':checked,'manifest':pin(D/'MANIFEST.json'),'public_paths':public});selected+=public
out={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'PR':107,'full_reports_and_verdicts_read_by_root':True,'three_families_final':True,'private_primary_material_excluded_from_selected_public_outputs':True,'original_effort':'1/5','new_central_proof_search_turns':0,'records':records,'selected_family_public_paths':sorted(set(selected))}
(A/'ROOT_PRIORITY_FAMILY_AUTHENTICATION_20261006.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'actual_operator_PID':os.getpid(),'families':len(records),'checked_pins':sum(len(r['checked_pins']) for r in records),'selected_public_paths':len(set(selected))}))
