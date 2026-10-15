#!/usr/bin/env python3
"""Own text-only V2 author; no proposed helper imported/compiled/executed."""
import ast
import datetime as dt
import difflib
import hashlib
import json
from pathlib import Path
P=Path(__file__).resolve().parent;A=P.parent;R=A.parents[2];OLD=A/'acceptance_preparation_family';ADV=A/'acceptance_static_adversary_family'
SHA=lambda b:hashlib.sha256(b).hexdigest()
def put(n,v):
 p=P/n;assert not p.exists();p.write_bytes(v if isinstance(v,bytes) else v.encode() if isinstance(v,str) else (json.dumps(v,indent=2)+'\n').encode())
def edit(s,old,new):
 assert s.count(old)==1,old[:100];return s.replace(old,new,1)
def section(s,start,end,new):
 a=s.index(start);b=s.index(end,a);return s[:a]+new+s[b:]
for root,name,pin in [(OLD,'PREPARATION_MANIFEST.json','6e8d07a73f68177ae3b7f446a1416ae39eabd560352fd7685464bcb129d0bcdc'),(ADV,'FIRST_PARTY_MANIFEST.json','31c82a50855cf621859d6bfa182541ec07d77a3727d621ce4adc99597620c6c0')]:
 assert SHA((root/name).read_bytes())==pin
original={n:(OLD/n).read_text() for n in ['pr41_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']}
g=original['pr41_guards.py']
g=edit(g,'import datetime as dt','import copy\nimport datetime as dt')
g=edit(g,'import subprocess','import stat\nimport subprocess')
g=edit(g,'def manifest(base,name,pin=None,count=None):','''def frozen_files(base,values,self_name=None):
    names={z['path'] for z in rows(values)}
    if self_name is not None:names.add(relative(self_name).as_posix())
    for n in names:
        require(stat.S_IMODE(regular(base,n).stat().st_mode)==0o444,'Literal frozen0444 including special permission bits required: '+n)


def manifest(base,name,pin=None,count=None,frozen=False):''')
g=edit(g,"    return rr\n\n\ndef bound(pin):","    if frozen:frozen_files(base,rr,name)\n    return rr\n\n\ndef bound(pin):")
g=edit(g,"    required(o,{'schema':'pr41-root-approved-immutable-acceptance-bindings/v1'", "    exact_reference(o['whole_manifest']);exact_reference(o['root_whole_inspection'])\n    expected=load(HERE/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json')\n    expected.update(status='ROOT_APPROVED_CLOSED_WHOLE_EVIDENCE',created_utc=o['created_utc'],root_full_current_read_completed=True,root_full_whole_read_completed=True,independent_whole_current_pass=True,whole_manifest=o['whole_manifest'],root_whole_inspection=o['root_whole_inspection'])\n    require(equal(o,expected),'Complete typed external ROOT bindings schema/value equality required')\n    required(o,{'schema':'pr41-root-approved-immutable-acceptance-bindings/v1'")
g=edit(g,'def root_binding_input(name,pin_value):', '''def exact_reference(obj):
    require(type(obj) is dict and set(obj)=={'path','bytes','sha256'},'Exact literal path/bytes/SHA reference row required; extensions prohibited')
    rows([obj])
    return obj


def root_binding_input(name,pin_value):''')
g=edit(g,"        exact(root,{z['path'] for z in rows(c['members']+c['foreign_members'])}|{c['manifest_name']})", "        exact(root,{z['path'] for z in rows(c['members']+c['foreign_members'])}|{c['manifest_name']})\n        if c.get('requires_all_members_0444') is True:frozen_files(root,c['members']+c['foreign_members'],c['manifest_name'])")
g=edit(g,"    frozen=manifest(C,'MANIFEST.json',CURRENT_SHA,547)\n    require(all((C/z['path']).stat().st_mode&0o777==0o444 for z in frozen) and (C/'MANIFEST.json').stat().st_mode&0o777==0o444,'Frozen current0444 required')", "    frozen=manifest(C,'MANIFEST.json',CURRENT_SHA,547,frozen=True)")
g=edit(g,"    for z in authored+foreign:\n        require((w/z['path']).stat().st_mode&0o777==0o444,'Whole files must remain0444')", "    frozen_files(w,authored+foreign,'FIRST_PARTY_MANIFEST.json')\n    for z in authored+foreign:")
g=edit(g,"    manifest(HERE,'PREPARATION_MANIFEST.json',a.preparation_manifest_sha256)", "    manifest(HERE,'PREPARATION_MANIFEST.json',a.preparation_manifest_sha256,frozen=True)")
g=edit(g,"    fm=manifest(ps['final_manifest'].parent,'FINAL_MANIFEST.json',a.final_manifest_sha256,2)", "    fm=manifest(ps['final_manifest'].parent,'FINAL_MANIFEST.json',a.final_manifest_sha256,2,frozen=True)")
g=edit(g,"    required(receipt,{'schema':'pr41-actual-final-reconciliation/v1'", "    require(type(receipt) is dict and set(receipt)=={'schema','utc','status','actual_root_reconciliation','pr','problem_id','preparation_manifest_sha256','entire_scope','bindings_before','bindings_after','root_reviewed_plan','reconciliation_source','science_helpers_executed','new_substantive_attempts','audit_turns','shared_mutations'},'Complete actual final receipt keyset required')\n    required(receipt,{'schema':'pr41-actual-final-reconciliation/v1'")
g=section(g,'def accepted_invariants(o,pins,pre):','\ndef canonical_names(','''def derive_inventory(before,remote,finalized_utc):
    require(type(before) is dict and type(before.get('items')) is list and len(before['items'])==180,'Complete retained180-item program inventory required')
    require(all(type(z) is dict and type(z.get('number')) is int for z in before['items']),'Typed original inventory identities required')
    identities=[z['number'] for z in before['items']]
    require(len(set(identities))==180 and identities.count(41)==1,'Exact unique selected original inventory identity required')
    require(type(before.get('completed_count')) is int and before['completed_count']==30 and sum(z.get('stage')=='complete' for z in before['items'])==30,'Actual30 prior primaries required')
    required(remote,{'state':'MERGED','isDraft':False,'number':41,'headRefOid':HEAD,'headRefName':'dot/math-'+ID,'baseRefName':'main'},'Actual merged remote inventory derivation')
    require(type(remote['mergeCommit']) is dict and set(remote['mergeCommit'])=={'oid'} and type(remote['mergeCommit']['oid']) is str and re.fullmatch('[0-9a-f]{40}',remote['mergeCommit']['oid']),'Exact actual merge oid required')
    clock=utc_clock(finalized_utc,'Retained actual finalization UTC');merged=utc_clock(remote['mergedAt'],'Actual merged UTC')
    require(merged<=clock<=dt.datetime.now(dt.timezone.utc),'Actual merged/finalization clocks reversed or future')
    inv=copy.deepcopy(before);chosen=next(z for z in inv['items'] if z['number']==41)
    require(chosen.get('stage')!='complete','Original selected inventory is not already complete')
    chosen.update(stage='complete',outcome='unsolved_accepted_partial',queue_status='unsolved',audited_head=HEAD,merge_commit=remote['mergeCommit']['oid'],merged_at=remote['mergedAt'],workflow_completion_estimate_percent=100,original_attempts='2/5',new_substantive_attempts=0,cumulative_attempts='2/5',paper_or_new_doi_or_tracker=False)
    done=sum(z.get('stage')=='complete' for z in inv['items']);require(done==31,'Exactly31 derived primary completions')
    inv.update(updated_at_utc=finalized_utc,last_checkpoint_utc=finalized_utc,completed_count=31,program_completion_estimate_percent=31/180*100,completion_estimate_percent=31/180*100,current_pr=42)
    return inv


def finalization(pins,pre):
    record=load(A/'integration_finalization.json');remote=load(A/'remote_merge_receipt.json')
    require(type(record) is dict and 'utc' in record,'Actual retained finalization record required')
    expected={'schema':'pr41-actual-integration-finalization/v1','utc':record['utc'],**pins,'pr':41,'before_inventory_sha256':pre['inventory_before_sha256'],'remote_merge_receipt':pin(A/'remote_merge_receipt.json'),'merge_commit':remote['mergeCommit']['oid'],'merge_tree':git('show','-s','--format=%T',remote['mergeCommit']['oid']),'source_sha256':sha((HERE/'integrate_reviewed_partial.py').read_bytes())}
    exact_reference(record['remote_merge_receipt']);require(equal(record,expected),'Complete typed actual finalization record required')
    final_clock=utc_clock(record['utc'],'Actual retained finalization UTC')
    phases=[load(A/n) for n in ['integration_preflight.json','integration_check.json','integration_prepush.json']]
    clocks=[utc_clock(z['utc'],'Actual retained phase UTC') for z in phases]+[final_clock]
    require(clocks==sorted(clocks) and final_clock<=dt.datetime.now(dt.timezone.utc),'Retained integration clocks reversed or future')
    require(utc_clock(remote['mergedAt'],'Actual merged UTC')<=final_clock,'Actual merge is after retained finalization')
    before=(A/'integration_inventory_before.json').read_bytes();require(sha(before)==pre['inventory_before_sha256'],'Entire retained before inventory differs')
    derive_inventory(parse(before),remote,record['utc'])
    return record,remote


def expected_acceptance(pins,pre):
    final,remote=finalization(pins,pre)
    return {'schema':'pr41-accepted-qualified-conditional-partial/v1','utc':final['utc'],**SCIENCE,**pins,'pr':41,'id':9700035,'problem_id':9700035,'problem_number':CODE,'queue_status':'unsolved','outcome':'unsolved_accepted_partial_merged','original_head':HEAD,'original_base':ORIGINAL_BASE,'merge_commit':final['merge_commit'],'merge_tree':final['merge_tree'],'merge_parents':[pre['main_before'],HEAD],'merged_at':remote['mergedAt'],'remote_state':'MERGED','remote_isDraft':False,'canonical_scientific_artifact_sha256':SCIENCE_SHA,'source_record_sha256':SOURCE_SHA,'original_ledger_sha256':LEDGER_SHA,'substantive_attempts_used':2,'substantive_attempt_limit':5,'native_historical_events_inferred':False,'historical_metadata_archival_only':True,'workflow_completion_estimate_percent':100,'full_resolution_completion_estimate_percent':0,'scientific_scope':load(HERE/'SCIENTIFIC_SCOPE.json')}


def accepted_invariants(o,pins,pre,audit=False):
    expected=expected_acceptance(pins,pre)
    if audit:
        expected.update(canonical_manifest_sha256=sha(regular(K,'MANIFEST.json').read_bytes()),canonical_manifest_entries=len(rows(load(K/'MANIFEST.json')['files'])))
    require(equal(o,expected),'Complete typed canonical/audit accepted receipt schema and derived values required; meaningful extensions prohibited')
    source(K)
    for n in ADMIN:
        expected_admin=load(C/n)
        expected_admin.update(**SCIENCE,**pins,id=9700035,current_context_path='CURRENT_CONTEXT_PRESENT.md',current_audit_scope_path='CURRENT_AUDIT_SCOPE_PRESENT.md',current_gate='accepted_qualified_partial',current_verdict=WHOLE_VERDICT,status='unsolved_accepted_partial_merged',new_whole_current_gate=WHOLE_VERDICT,historical_verdict_transferred=False,merge_commit=o['merge_commit'],merge_tree=o['merge_tree'],merged_at=o['merged_at'])
        require(equal(load(K/n),expected_admin),'Complete typed present administrative object differs: '+n)

''')
s=original['seal_final_evidence.py']
s=edit(s,"g.manifest(g.HERE,'PREPARATION_MANIFEST.json',a.preparation_manifest_sha256)","g.manifest(g.HERE,'PREPARATION_MANIFEST.json',a.preparation_manifest_sha256,frozen=True)")
s=edit(s,"    for f in output.iterdir(): f.chmod(0o444)","    for f in output.iterdir(): f.chmod(0o444)\n    g.manifest(output,'FINAL_MANIFEST.json',count=2,frozen=True)")
i=original['integrate_reviewed_partial.py']
i=section(i,'def inventory_guard(before,after):','\ndef main():','''def inventory_guard(before,after,remote,finalized_utc):
    expected=g.derive_inventory(before,remote,finalized_utc)
    g.require(g.equal(after,expected),'Complete typed derived inventory, workflow/program percentages and clocks required')

''')
start="    before_inv=g.load(g.A/'integration_inventory_before.json'); inv=copy.deepcopy(before_inv); chosen=next(z for z in inv['items'] if z['number']==41)"
end="    for n in g.ADMIN:"
first=i.index(start);last=i.index(end,first)
i=i[:first]+'''    before_inv=g.load(g.A/'integration_inventory_before.json'); inv=g.derive_inventory(before_inv,observation,now)
    inventory_guard(before_inv,inv,observation,now)
    g.dump(g.A/'remote_merge_receipt.json',observation,exclusive=True)
    final={'schema':'pr41-actual-integration-finalization/v1','utc':now,**pins,'pr':41,'before_inventory_sha256':pre['inventory_before_sha256'],'remote_merge_receipt':g.pin(g.A/'remote_merge_receipt.json'),'merge_commit':merge,'merge_tree':tree,'source_sha256':g.sha((g.HERE/'integrate_reviewed_partial.py').read_bytes())}
    g.dump(g.A/'integration_finalization.json',final,exclusive=True)
    g.finalization(pins,pre)
'''+i[last:]
i=section(i,"    accept={'schema':'pr41-accepted-qualified-conditional-partial/v1'","    g.accepted_invariants(accept,pins,pre);",'    accept=g.expected_acceptance(pins,pre)\n')
i=edit(i,"    g.accepted_invariants(g.load(g.K/'acceptance.json'),pins,pre); g.accepted_invariants(g.load(g.A/'acceptance.json'),pins,pre)","    g.manifest(g.K,'MANIFEST.json',frozen=True)\n    g.accepted_invariants(g.load(g.K/'acceptance.json'),pins,pre); g.accepted_invariants(g.load(g.A/'acceptance.json'),pins,pre,audit=True)")
i=edit(i,"inventory_guard(before_inv,g.load(g.B/'inventory.json'))","inventory_guard(before_inv,g.load(g.B/'inventory.json'),observation,now)")
m=original['state_mirror_reconciliation.py']
m=edit(m,"g.accepted_invariants(canonical,pins,pre); g.accepted_invariants(audit,pins,pre)","g.accepted_invariants(canonical,pins,pre); g.accepted_invariants(audit,pins,pre,audit=True)")
m=edit(m,"    g.manifest(g.K,'MANIFEST.json',audit['canonical_manifest_sha256'],audit['canonical_manifest_entries']); g.canonical(frozen,True)\n    g.require(all(f.stat().st_mode & 0o777==0o444 for f in g.K.rglob('*') if f.is_file()),'Accepted canonical files must remain0444')","    g.manifest(g.K,'MANIFEST.json',audit['canonical_manifest_sha256'],audit['canonical_manifest_entries'],frozen=True); g.canonical(frozen,True)")
m=edit(m,"inv=g.load(g.B/'inventory.json'); inventory_guard(g.load(g.A/'integration_inventory_before.json'),inv);", "final,retained_remote=g.finalization(pins,pre)\n    inv=g.load(g.B/'inventory.json'); inventory_guard(g.load(g.A/'integration_inventory_before.json'),inv,retained_remote,final['utc']);")
p=original['verify_post_acceptance.py']
p=edit(p,"    g.source(g.K); g.source(g.C); g.accepted_invariants(acceptance,pins,pre); g.foreign_check(pre)","    g.source(g.K); g.source(g.C); g.accepted_invariants(acceptance,pins,pre); g.foreign_check(pre)\n    final,remote=g.finalization(pins,pre);inventory=g.load(g.B/'inventory.json')\n    g.require(g.equal(inventory,g.derive_inventory(g.load(g.A/'integration_inventory_before.json'),remote,final['utc'])),'Complete final typed derived inventory differs')")
p=edit(p,"'program_completion_estimate_percent':31/180*100", "'program_completion_estimate_percent':inventory['program_completion_estimate_percent']")
updated={'pr41_guards.py':g,'seal_final_evidence.py':s,'integrate_reviewed_partial.py':i,'state_mirror_reconciliation.py':m,'verify_post_acceptance.py':p}
deltas=[];source_rows=[]
for n,body in updated.items():
 ast.parse(body);assert '&0o777==' not in body and '& 0o777==' not in body
 put(n,body);deltas.extend(difflib.unified_diff(original[n].splitlines(True),body.splitlines(True),fromfile='closed_v1/'+n,tofile='proposed_v2/'+n))
 source_rows.append({'path':n,'bytes':len(body.encode()),'sha256':SHA(body.encode()),'original_v1_sha256':SHA(original[n].encode())})
put('SOURCE_DELTAS.patch',''.join(deltas))
for n in ['SCIENTIFIC_SCOPE.json','DRAFT_FINAL_PLAN.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FUTURE_GATE_PINS.json']:put(n,(OLD/n).read_bytes())
inputs=json.loads((OLD/'INPUT_BINDINGS.json').read_bytes());inputs['source_revision']='v2';inputs['created_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
for root,name,pin in [(OLD,'PREPARATION_MANIFEST.json','6e8d07a73f68177ae3b7f446a1416ae39eabd560352fd7685464bcb129d0bcdc'),(ADV,'FIRST_PARTY_MANIFEST.json','31c82a50855cf621859d6bfa182541ec07d77a3727d621ce4adc99597620c6c0')]:
 raw=(root/name).read_bytes();manifest=json.loads(raw);key=root.name+'/'+name
 inputs['pins'][key]={'path':(root/name).relative_to(R).as_posix(),'bytes':len(raw),'sha256':pin}
 inputs['closures'].append({'directory':root.name,'manifest_name':name,'manifest_sha256':pin,'members':manifest['files'],'foreign_members':[],'requires_all_members_0444':True})
inputs['previous_source_and_adversary_preserved']=True;inputs['prior_adversary_mandatory_repairs']=['S1','S2','S3'];inputs['future_runtime_binding_inputs_remain_external']=True
put('INPUT_BINDINGS.json',inputs)
put('REVISION_SOURCE_BINDINGS.json',{'schema':'pr41-source-only-acceptance-v2-source-delta/v1','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'repaired_sources':source_rows,'previous_source_manifest_sha256':'6e8d07a73f68177ae3b7f446a1416ae39eabd560352fd7685464bcb129d0bcdc','adversary_manifest_sha256':'31c82a50855cf621859d6bfa182541ec07d77a3727d621ce4adc99597620c6c0','mandatory_admin_repairs':['S1','S2','S3'],'math_and_current547_unchanged':True,'candidate_imported_compiled_or_executed':False,'future_actual_PASS_claimed':False,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0})
for n in ['CONTRACT.md','READ_EXPECTATIONS.md']:put(n,(OLD/n).read_bytes())
print(json.dumps({'status':'SOURCE_ONLY_V2_AUTHORED_NOT_EXECUTED','sources':source_rows,'future_actual_gates':'PENDING','candidate_helpers_imported_compiled_or_executed':False},indent=2))
