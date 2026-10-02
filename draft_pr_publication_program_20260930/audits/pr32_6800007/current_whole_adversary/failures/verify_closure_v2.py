#!/usr/bin/env python3
"""Read entire frozen closure and compare complete actual private replay data.
Run only after private replay layout/programs described in REPRODUCE.md exist.
All generated results are written inside this review; no protected input writes.
"""
from pathlib import Path
import json,hashlib,datetime
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
COPY=HERE/'tmp/replay/audits/pr32_6800007'
FRESH_FLAG=HERE/'tmp/priority_replay/audits/pr32_6800007/priority_flag_family'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
closed=[]
for fam,name,key in [('hprinciple_family','MANIFEST.json','files'),('integral_action_family','artifact_manifest.json','members'),('primary_scope_family','MANIFEST.json','files'),('priority_flag_family','MANIFEST.json','files'),('priority_topology_family','MANIFEST.json','files')]:
    p=BASE/fam/name;d=json.loads(p.read_text());entries=d[key]
    for e in entries:
        q=p.parent/e['path'];assert sha(q)==e['sha256'] and q.stat().st_size==e.get('bytes',e.get('size'))
    closed.append({'family':fam,'manifest_sha256':sha(p),'members':len(entries),'all_exact':True})
comparisons=[]
for family,name,clock,path in [('priority_flag_family','CONTROL_RESULTS.json','generated_utc',FRESH_FLAG/'CONTROL_RESULTS.json'),('priority_topology_family','SPECIALIZATION_CHECK.json','recorded_utc',COPY/'priority_topology_family/SPECIALIZATION_CHECK.json')]:
    old=json.loads((BASE/family/name).read_text());new=json.loads(path.read_text());old.pop(clock);new.pop(clock);assert old==new
    comparisons.append({'family':family,'output':name,'complete_equal_except_clock':clock})
assert (HERE/'geometric_controls.stdout').read_bytes()==(BASE/'hprinciple_family/controls_results.json').read_bytes()
assert (HERE/'integral_reproduce.stdout').read_bytes()==(BASE/'integral_action_family/reproduction_results.json').read_bytes()
old=json.loads((BASE/'primary_scope_family/CONTROL_RESULTS.json').read_text());new=json.loads((COPY/'primary_scope_family/CONTROL_RESULTS.json').read_text())
# Preserve complete actual generated structured result before stripping clocks
# in memory for comparison; the captured file remains untouched.
(HERE/'PRIMARY_ACTUAL_COMPLETE_RESULTS.json').write_bytes((COPY/'primary_scope_family/CONTROL_RESULTS.json').read_bytes())
assert len(old['runs'])==len(new['runs'])==8
for item,other in zip(old['runs'],new['runs']):
    assert item['label']==other['label']
    label=item['label'];op=BASE/'primary_scope_family/control_outputs'/f'{label}.stdout';np=COPY/'primary_scope_family/control_outputs'/f'{label}.stdout';assert op.read_bytes()==np.read_bytes()
    os=(BASE/'primary_scope_family/control_outputs'/f'{label}.stderr').read_bytes();ns=(COPY/'primary_scope_family/control_outputs'/f'{label}.stderr').read_bytes()
    normalized=ns.replace(str((COPY/'primary_scope_family').resolve()).encode(),str((BASE/'primary_scope_family').resolve()).encode());assert os==normalized
    for v in [item,other]:
        v.pop('utc_started',None)
        if item['exit_code']:
            for k in ['stderr_sha256','stderr_bytes','failure_excerpt']:v.pop(k,None)
old.pop('utc');new.pop('utc');assert old==new
comparisons.append({'family':'primary_scope_family','complete_actual_results_equal_except':'utc/runs.utc_started; exact expected-failure stderr normalized ONLY the verified absolute private prefix, without altering either captured receipt','actual_output_runs':8})
def leaves(x):return sum(map(leaves,x.values())) if isinstance(x,dict) else sum(map(leaves,x)) if isinstance(x,list) else 1
inventory=[];deps=json.loads((BASE/'reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json').read_text())
for e in deps['files']:
    p=BASE/e['path'];entry={'path':e['path'],'bytes':p.stat().st_size,'sha256':sha(p)}
    assert entry['bytes']==e['bytes'] and entry['sha256']==e['sha256']
    if p.suffix=='.json':
        if not p.read_bytes():
            assert e['path']=='hprinciple_family/reproduction/author_stdout.json'
            entry.update(json_decoded=False,meaning='Preserved empty failed-run stdout, not a JSON receipt or PASS.')
        else:
            data=json.loads(p.read_text());entry.update(json_type=type(data).__name__,scalar_leaves=leaves(data),topology=list(data) if isinstance(data,dict) else len(data))
    elif p.suffix=='.jsonl':
        data=[json.loads(l) for l in p.read_text().splitlines()];entry.update(json_records=len(data),scalar_leaves=leaves(data))
    inventory.append(entry)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'closed_manifests':closed,'actual_complete_output_comparisons':comparisons,'all186_dependencies_read_fully_and_JSON_inventory':inventory,'original_and_closed_firstparty_unchanged':True,'claim_boundary':'Full byte reads and decoded inventory certify binding. Actual relevant programs were separately read and executed. They do not mean every foreign paper was inspected or numerical tests prove universal topology.'}
(HERE/'CLOSURE_AND_COMPLETE_REPLAY_COMPARISON.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'fiveclosedfamilies':closed,'completeactualcomparisons':comparisons,'dependencies':len(inventory)},indent=2))
