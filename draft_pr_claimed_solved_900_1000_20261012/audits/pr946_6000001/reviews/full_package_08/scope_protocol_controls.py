"""Status-only controller identity helper controls; synthetic metadata, no source intake."""
from pathlib import Path
import hashlib,json,copy
from datetime import datetime,timezone
P=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012');O=Path(__file__).resolve().parent;src=P/'resweep_draft_statuses_900_1000.py';b=src.read_bytes();N={'__name__':'_status_helper_only_','__file__':str(src)};exec(compile(b,str(src),'exec'),N)
initial={'headRefOid':'a'*40,'entries':[{'id':'111'}]};pr={'number':999,'headRefOid':'a'*40};calls=[];paths=[]
def run(argv):calls.append(argv);return '\n'.join(paths)
N['run']=run;rows=[]
def case(name,fn):r=fn();rows.append({'case':name,'result':r});return r
r=case('unchanged_head_reuses_exact_initial_identity_without_call',lambda:N['current_identity'](pr,initial));assert r['problem_id']=='111' and not calls
pr['headRefOid']='b'*40
for label,pp,want in [('changed_single',['unsolved_math_prioritization/attempts/222/public/PROOF.md'],'222'),('changed_duplicate_sameID',['unsolved_math_prioritization/attempts/222/a','unsolved_math_prioritization/attempts/222/b'],'222'),('changed_ambiguous',['unsolved_math_prioritization/attempts/222/a','unsolved_math_prioritization/attempts/333/b'],None),('changed_missing',['unsolved_math_prioritization/QUEUE.md'],None),('changed_nonnumeric',['unsolved_math_prioritization/attempts/bad/a'],None)]:
 paths[:]=pp;r=case(label,lambda:N['current_identity'](pr,initial));assert r['identity_reconciled']==(want is not None)
 if want:assert r['problem_id']==want
q='| 1 | 222 / fixture | t | 0 | 0 | 0 | 0 | claimed_solved | 4/5 | | | |\n'
for status in ['claimed_solved','partially_solved','preprint_published','claimed_solved_but_unchecked']:
 r=case('literal_status_'+status,lambda:N['target_status'](q.replace('claimed_solved',status),'222'));assert r['status']==status
for label,bad in [('duplicate',q+q),('missing',q.replace('222 /','333 /'))]:
 try:N['target_status'](bad,'222')
 except RuntimeError as e:rows.append({'case':label,'rejected':True,'reason':str(e)})
 else:raise RuntimeError('Ambiguous scope accepted')
protocol=(P/'INTAKE_SCOPE_PROTOCOL.md').read_bytes();out={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'source':{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()},'protocol':{'bytes':len(protocol),'sha256':hashlib.sha256(protocol).hexdigest()},'cases':rows,'case_count':len(rows),'all_GitHub_calls_fake':True,'math_source_reads':0,'external_writes':0,'interpretation':'Frozen gate_next is metadata proposal only. Controller must bind changed-head filename identity to observed immutable head, refresh actual PR state around scope intake, require exact claimed_solved and independently sweep all101 after ascending work. Prior-target convenience cleanup remains explicit controller duty.'};(O/'SCOPE_PROTOCOL_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','cases':len(rows)}))
