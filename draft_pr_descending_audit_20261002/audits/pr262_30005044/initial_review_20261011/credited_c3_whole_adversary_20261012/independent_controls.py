#!/usr/bin/env python3
"""NEW exact content/preservation and finite analytic controls; read-only inputs."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
from collections import Counter, defaultdict
import hashlib, json, subprocess, sys, shutil, difflib

own = Path(__file__).resolve().parent
base = own.parent
parent = base / 'credited_priority_correction_v03_20261012'
c3 = parent / 'candidate/unsolved_math_prioritization/attempts/30005044'
c2 = base / 'scoped_candidate_v02/unsolved_math_prioritization/attempts/30005044'
original = base / 'original_submission/files/unsolved_math_prioritization/attempts/30005044'
counts = Counter()
def ck(value, group):
    assert value, group
    counts[group] += 1
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def section(p,n):
    data=p.read_bytes();start=data.index(f'## {n}.'.encode());end=data.index(f'## {n+1}.'.encode())
    return data[start:end]

inputs=json.loads((own/'INPUT_MANIFEST.json').read_text())
for rec in inputs['files']:
    p=Path(rec['path'])
    ck(sha(p)==rec['sha256'] and p.stat().st_size==rec['bytes'] and oct(p.stat().st_mode&0o777)==rec['mode'], 'whole_input_identity')
for root,name,count in [(c3,'CANDIDATE_MANIFEST.json',37),(parent,'OUTPUT_MANIFEST.json',51)]:
    mf=json.loads((root/name).read_text())
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p!=root/name}
    ck(actual=={x['path'] for x in mf['files']} and len(actual)==count==mf['file_count'], 'complete_manifest_scope')
    for rec in mf['files']:
        p=root/rec['path']
        ck(sha(p)==rec['sha256'] and p.stat().st_size==rec['bytes'] and oct(p.stat().st_mode&0o777)==rec['mode'], 'full_C3_payload_identity')
ck(sha(c3/'CANDIDATE_MANIFEST.json')=='e3ab9c075ad00a7d97651b9218d2c4a83acc366cec847d0783d1eed2a63c3353','assigned_selector')
ck(sha(parent/'OUTPUT_MANIFEST.json')=='a5263cffbac067e40f337132ea99458a333f42728cffbd8835ad8021646144c1','assigned_parent_manifest')
meta=json.loads((parent/'PRESERVATION_METADATA.json').read_text())
for rec in meta['historical16']:
    p=c3/rec['path'];old=original/Path(rec['path']).relative_to('historical_submission')
    ck(p.read_bytes()==old.read_bytes()==(c2/rec['path']).read_bytes(),'all16_historical_bytes')
    ck(oct(p.stat().st_mode&0o777)==rec['mode']==oct((c2/rec['path']).stat().st_mode&0o777)==oct(old.stat().st_mode&0o777),'all16_historical_frozen_modes')
for n in range(1,7):
    ck(section(c3/'PROOF.md',n)==section(c2/'PROOF.md',n),'accepted_sections1_to6')
    if n!=2:ck(section(c3/'PROOF.md',n)==section(original/'PROOF.md',n),'original_sections1_3_to6')
    rec=meta['proof_sections1_to6'][n-1]
    ck(hashlib.sha256(section(c3/'PROOF.md',n)).hexdigest()==rec['sha256'],'section_metadata_sha')
for rec in meta['unchanged_controls_and_receipts']:
    ck((c3/rec['path']).read_bytes()==(c2/rec['path']).read_bytes(),'accepted_control_receipt_preservation')
turn=json.loads((c3/'turns.json').read_text())
ck(turn['events']==json.loads((original/'turns.json').read_text())['events'] and turn['substantive_author_turns']==1 and turn['maximum_author_turns']==5 and turn['added_substantive_author_turns_by_corrections_or_reviews']==0,'budget_and_historical_event')
proposal=json.loads((parent/'STATUS_ASSESSMENT_PROPOSAL.json').read_text())
binding=json.loads((base/'original_submission/BINDING.json').read_text())
old=proposal['original_row'];new=proposal['desired_row'];a=old.split('|');b=new.split('|')
ck(old==binding['exact_target_QUEUE_row'],'authenticated_original_row')
ck([i for i in range(len(a)) if a[i]!=b[i]]==[8,11],'only_status_findings')
ck(a[1].strip()==b[1].strip()=='281' and a[5].strip()==b[5].strip()=='5.0' and a[9].strip()==b[9].strip()=='1/5','row_preserved_rank_impact_budget')
ck(a[8].strip()=='claimed_solved' and b[8].strip()=='already_solved','row_status_boundary')
ck(not proposal['live_mutation_performed'] and 'not a queue.py assess input' in proposal['source_review_hash_binding'],'proposal_not_live_assessment')
for filename,value in [('ORIGINAL_SUBMITTED_QUEUE_ROW.md',old),('DESIRED_QUEUE_ROW_PROPOSAL.md',new)]:
    ck((parent/filename).read_text().rstrip('\n')==value,'row_receipt_exact')
diffmeta=json.loads((parent/'DIFF_METADATA.json').read_text())
oldset={p.relative_to(c2).as_posix() for p in c2.rglob('*') if p.is_file()}
newset={p.relative_to(c3).as_posix() for p in c3.rglob('*') if p.is_file()}
changed={x for x in oldset&newset if (c2/x).read_bytes()!=(c3/x).read_bytes()}
ck(changed=={x['path'] for x in diffmeta['changed_files']} and len(changed)==10,'full_diff_changed_set')
ck(newset-oldset=={x['path'] for x in diffmeta['added_files']} and len(newset-oldset)==4 and not oldset-newset,'full_diff_added_removed')
ck(len(oldset&newset-changed)==24,'full_diff_unchanged_count')
expected=''
for rel in sorted(changed|newset-oldset):
    before=(c2/rel).read_text().splitlines(keepends=True) if rel in oldset else []
    after=(c3/rel).read_text().splitlines(keepends=True)
    expected+=''.join(difflib.unified_diff(before,after,fromfile='accepted_C2/'+rel,tofile='credited_C3/'+rel))
ck(expected==(parent/'C2_TO_C3.diff').read_text(),'entire_diff_exact_regeneration')

# Replay only copied, previously inspected print-only checkers in owned scratch.
replays=[]
for script,receipt in [('verify.py','verification.json'),('independent_review/independent_checks.py','independent_review/INDEPENDENT_CHECKS.json')]:
    scratch=own/'isolated_replay'/Path(script).name
    if not scratch.exists(): shutil.copy2(c3/script,scratch)
    ck(scratch.read_bytes()==(c3/script).read_bytes(),'isolated_script_identity')
    result=subprocess.run([sys.executable,str(scratch)],cwd=own/'isolated_replay',capture_output=True,check=True)
    ck(result.stdout==(c3/receipt).read_bytes(),'isolated_byte_exact_checker_replay')
    saved=own/'isolated_replay'/(Path(receipt).name)
    saved.write_bytes(result.stdout)
    replays.append({'script_sha256':sha(scratch),'receipt_sha256':sha(saved),'assertions':json.loads(result.stdout).get('assertions',json.loads(result.stdout).get('exact_assertions'))})

# Independent exact recovery/schedule identities and a fast-ray countercontrol.
for lam in [Q(1,257),Q(1,3),Q(1),Q(5,2),Q(113)]:
    tau=1/(2*lam)
    for n in range(1,129):
        guards=tau+sum((tau/2**j for j in range(n)),Q())
        ck(guards+2*tau/2**n==3*tau,'common_horizon_recovery_exact_remainder')
        s=tau*(1-Q(1,2**n));incoming=tau*(1-Q(1,2**(n-1)))+Q(2,3)*tau/2**n
        ck(incoming<s<tau and tau*(1-Q(1,2**(n-1)))<=incoming,'finite_path_guard_coverage')
for n in range(128):
    arrival=1-Q(1,2**n);outgoing=1-Q(1,2**(n+1));healing=(outgoing+1)/2
    ck(arrival<outgoing<healing<1,'fast_path_without_simultaneity_negative_control')
for n in range(128):
    D=16**(n+2);tail=Q(1,2**(n+3));window=Q(1,2**(n+2))
    ck(D*tail*window/2==4**(n+1) and 4**(n+1)>=4*(n+1),'explicit_stage_intensity')
ck(Q(1,4)*(1-Q(1,15))==Q(7,30),'explicit_probability_coefficient')

# Rounded plumpness constant: polynomial version of the stated threshold.
for denominator in range(2,40):
    p=Q(1,denominator)
    for m in [1,2,17,256]:
        x=2*m/p;k=-(-x.numerator//x.denominator)
        ck(k*p>=2*m and k<=3*m/p,'retention_rounding')
    M=110592*denominator**3
    ck(Q(M)*p**3==110592 and M>=4,'plump_threshold_constant_twelfth_power')
for h in range(3,129):
    j=h*h
    ck(j<=2*h*h and 2*h*h<h**3,'strict_plump_quantile_cube_control')
for h0 in range(3,30):
    for n in range(9):
        ck(h0**(2**n)>=h0**(n+1),'quantile_series_geometric_majorant')

# Repaired BKV exponents and failure of the old epsilon.
alpha=Q(1,4);s1=Q(3,2);s2=Q(2);eps=Q(1,64);mu=Q(0)
separation=alpha*(s2-s1)/(s2+s1);a=1-(alpha+eps)*s1;delta=a-mu*s2
ck(separation==Q(1,28) and eps<separation and Q(1,16)>separation,'BKV_epsilon_repair')
ck(a==delta==Q(77,128) and -alpha*(s2-s1)+eps*(s2+s1)==-Q(9,128),'BKV_exact_exponents')
for R in [Q(1,100),Q(1,7),Q(1),Q(7),Q(100)]:
    ck(R/(R+1)**2<=1/R,'successful_wait_integral_bound')
    ck((R/(R+1)**2)/(R/(R+1))==1/(R+1),'success_conditioned_wait_negative_bias_control')
for n in range(1,17):
    waits=[Q(j+1,2**(j+3)) for j in range(n)]
    ck(sum((sum(waits[m+1:]) for m in range(n)),Q())==sum((j*waits[j] for j in range(n)),Q()),'residual_double_sum_identity')

# A selected degree is biased; a never-read descendant/recovery probe stays fresh.
states=list(product((1,3),(0,1),(1,2,4),(0,1)))
histories=0
for D in range(1,4):
    table=defaultdict(Counter)
    for config in product(states,repeat=D):
        chosen=next((i for i,state in enumerate(config) if state[0]==3 and state[1]),None)
        if chosen is None:continue
        history=tuple((s[0],s[1]) for s in config)
        table[(history,chosen)][config[chosen][2:]]+=1
    for (history,index),probes in table.items():
        histories+=1;total=sum(probes.values())
        ck(history[index][0]==3,'selected_degree_is_biased')
        ck(all(Q(probes[(d,r)],total)==Q(1,6) for d in (1,2,4) for r in (0,1)),'fresh_descendant_recovery_cylinder')
for denominator in range(2,50):
    for numerator in range(1,denominator):
        bad=Q(numerator,denominator)
        ck((Q(1,3)*bad+Q(2,3)*bad**3)<bad,'quenched_strictness')
ck(Q(1,2)+Q(1,2)*Q(1,2)**2>Q(1,2),'sterile_offspring_breaks_heredity_negative_control')
ck(Q(2)*Q(2)/(1+Q(2))>1,'bounded_binary_tree_survival_mean')
print(json.dumps({'status':'PASS','total_controls':sum(counts.values()),'groups':dict(counts),'isolated_replays':replays,'conditioned_probe_histories':histories,'scope':'Exact input/preservation/finite algebra and negative controls; written report supplies infinite-event derivations and source/credit interpretation.'},indent=2)+'\n')
