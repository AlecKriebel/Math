#!/usr/bin/env python3
"""Prepared root-only preflight/overlay/prepush/finalize. Root performs Git/remote mutations."""
import argparse
import copy
import sys
from pathlib import Path
sys.dont_write_bytecode = True
import pr44_guards as g

BODY = 'Accept PR44 / 2912 / Kirby4.36 as an UNSOLVED repository report of standard conditional deductions. The finite-support meridional restriction kernel, sufficient relative-degree-one pair-map criterion and conditional integral R^C/R^A for the specified abstract group-pair are valid scoped partials. Neither a degree-one meridian-compatible pair map from the unmarked full(G,pi2module,k) nor two actual smooth/locally flat PL S2-in-S4 exteriors with equal full triples and different homotopy types is realized. Both gaps remain explicit. Original18 and twelve immutable science/helper/result/source/ledger bodies are unchanged; original2/5,new0,audit0. The NEW whole-current source-first audit and genuine ROOT full reading/final reconciliation are separately bound. Global source/category/integral/history qualifications remain operative, including finite checks not proving realization/classification and absent raw prior versus SQL fallback{}. Current model/reasoning/deadline are null. No novelty, project solution, full prior-literature resolution, exhaustive priority, human peer review, paper, new DOI, tracker or release is claimed. One present acceptance event follows the exact original-head no-ff merge, preserves every prior state and the full history prefix, and consumes only the original two turns.
'
PRESENT_SCOPE = 'The NEW whole-current source-first audit has passed for this scoped UNSOLVED standard partial; actual completed acceptance is bound in acceptance.json. SOURCE_PRECISION_QUALIFICATIONS.md and CURRENT_OBSTRUCTION_CONTEXT.md apply globally to OBSTRUCTION.md, every presentation and metadata file. The unmarked full triple supplies no boundary/meridian marking or degree-one pair map; no actual allowed-category equal-full-triple exterior pair is realized. The integral quotient is conditional on the specified abstract group-pair, and augmentation-lattice substitution is invalid. Original18 archive and twelve immutable bodies remain exact. Earlier PENDING/source-only/PASS/runtime/search/access/model statements in the frozen current packet and original archives remain dated attributions at or before its frozen publication; later actual acceptance records alone describe the present disposition. Raw prior absence and SQL fallback{} remain distinct. Original2/5,new0,audit0; current runtime fields null; no novelty, human referee, paper/new DOI/tracker/release.
'

def queue_after(before):
    row=g.selected(before); cells=row.split('|'); g.require(cells[8].strip()=='queued' and cells[9].strip()=='0/5','Fresh original selected row must be queued0/5')
    cells[8]=' unsolved '; cells[9]=' 2/5 '; cells[11]=' Standard meridional duality kernel, sufficient degree-one pair-map criterion and conditional integral kernel for the specified abstract group-pair; unmarked full2type pair-map and actual equal-full-triple exterior realization gaps remain. [Accepted scoped UNSOLVED partial](attempts/2912/ACCEPTANCE.md). Original2/5,new0,audit0; no novelty/paper/new DOI/tracker. '
    after_row='|'.join(cells); changed=[i for i in range(len(cells)) if cells[i]!=row.split('|')[i]]
    g.require(set(changed)=={8,9,11} and cells[10]==row.split('|')[10] and cells[12]==row.split('|')[12],'Only named Status/Findings may change; Chat/DOI preserved')
    g.require(before.count(row.encode())==1,'Unique selected row literal required')
    after=before.replace(row.encode(),after_row.encode(),1)
    g.require(after.replace(after_row.encode(),row.encode(),1)==before,'Whole queue inverse replacement differs')
    return after,after_row


def inventory_guard(before,after,remote,finalized_utc):
    expected=g.derive_inventory(before,remote,finalized_utc)
    g.require(g.equal(after,expected),'Complete typed derived inventory, workflow/program percentages and clocks required')


def main():
    p=argparse.ArgumentParser(description=__doc__); g.args(p); p.add_argument('phase',choices=['preflight','overlay','prepush','finalize']); p.add_argument('--merge-queue-preimage-sha256')
    a=p.parse_args(); frozen,pins=g.gates(a); observation=g.remote(); now=g.stamp()
    if a.phase=='preflight':
        g.required(observation,{'state':'OPEN','isDraft':True},'Actual draft preflight')
        g.require(not g.K.exists() and not g.K.is_symlink() ,'Selected native canonical path must be absent')
        mh=Path(g.git('rev-parse','--git-path','MERGE_HEAD')); mh=mh if mh.is_absolute() else g.R/mh
        g.require(not mh.exists(),'No active merge at preflight')
        foreign=g.foreign_capture(); fresh=g.load(g.R/a.fresh_preimage); g.check(g.R,fresh['files']); head=g.git('rev-parse','HEAD')
        g.require(head==fresh['current_head'],'Root fresh actual HEAD differs')
        g.native_git_snapshot(head,fresh['files'])
        g.native_modes(fresh['files'])
        queue=g.Q.read_bytes(); g.selected(queue); queue_after(queue)
        state=g.load(g.R/'unsolved_math_prioritization/state.json'); inv=g.load(g.B/'inventory.json')
        g.require(all(type(z['turns_used']) is int for z in state.values()) and len(state)==34 and g.ID not in state and sum(z['turns_used'] for z in state.values())==41,'Require postPR43 native33targets/41turns, selected identity absent')
        g.require(inv['completed_count']==33 and sum(z.get('stage')=='complete' for z in inv['items'])==33,'Require32 complete primaries before43')
        item=[z for z in inv['items'] if z['number']==44]; g.require(len(item)==1 and item[0]['headRefOid']==g.HEAD and item[0]['headRefName']=='dot/math-2912' and item[0].get('stage')!='complete','Exact original PR44 inventory required')
        pre={'schema':'pr44-original-head-integration-preflight/v1','utc':now,**pins,'main_before':head,'pr':observation,'foreign_logs':foreign,'whole_queue_before_sha256':g.sha(queue),'selected_row_before':g.selected(queue),'state_before_sha256':g.sha((g.R/'unsolved_math_prioritization/state.json').read_bytes()),'history_before_sha256':g.sha((g.R/'unsolved_math_prioritization/history.jsonl').read_bytes()),'inventory_before_sha256':g.sha((g.B/'inventory.json').read_bytes()),'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'dated_frozen_preimage_not_rewritten':True}
        g.dump(g.A/'integration_preflight.json',pre,exclusive=True); g.write(g.A/'integration_queue_before.md',queue,exclusive=True); g.write(g.A/'integration_inventory_before.json',(g.B/'inventory.json').read_bytes(),exclusive=True); g.write(g.A/'accepted_pr_body.md',BODY.encode(),exclusive=True)
        g.write(g.A/'integration_state_before.json',(g.R/'unsolved_math_prioritization/state.json').read_bytes(),exclusive=True)
        g.write(g.A/'integration_history_before.jsonl',(g.R/'unsolved_math_prioritization/history.jsonl').read_bytes(),exclusive=True)
        g.fresh_check(pre); g.require(g.git('rev-parse','HEAD')==head,'HEAD changed during preflight'); print('PREFLIGHT PASS PR44; root ready/body and original-head no-ff merge remain'); return
    pre=g.preflight_record(pins)
    g.require((g.A/'accepted_pr_body.md').read_bytes()==BODY.encode(),'Reviewed exact body changed')
    before=(g.A/'integration_queue_before.md').read_bytes(); g.require(g.sha(before)==pre['whole_queue_before_sha256'],'Whole fresh queue before changed'); after,row=queue_after(before)
    if a.phase=='overlay':
        g.required(observation,{'state':'OPEN','isDraft':False,'body':BODY},'Actual ready remote')
        g.require(g.git('rev-parse','HEAD')==pre['main_before'] and g.git('rev-parse','MERGE_HEAD')==g.HEAD,'Exact original-head no-ff merge required')
        qpath='unsolved_math_prioritization/QUEUE.md'; conflicts=set(g.git('diff','--name-only','--diff-filter=U').splitlines()); g.require(conflicts<={qpath},'Unexpected merge conflicts require inspection')
        g.require(g.git_bytes('show','HEAD:'+qpath)==before,'Whole main queue before differs')
        if conflicts: g.require(g.git_bytes('show',':2:'+qpath)==before and g.git_bytes('show',':3:'+qpath)==g.git_bytes('show',g.HEAD+':'+qpath),'Exact actual conflict stages differ')
        else: g.require(g.git_bytes('show',':'+qpath)==g.Q.read_bytes(),'Automatic queue index/worktree differ')
        automatic=g.Q.read_bytes(); g.require(a.merge_queue_preimage_sha256 is not None and g.sha(automatic)==g.digest(a.merge_queue_preimage_sha256),'Root must pin/read entire actual automatic-merge queue')
        g.fresh_check(pre,{qpath}); orig=g.rows(g.load(g.A/'snapshot_manifest_v2.json')['files']); g.exact(g.K,{z['path'] for z in orig}); g.original_native(g.K)
        for z in frozen:
            dst=g.K/z['path']; dst.parent.mkdir(parents=True,exist_ok=True); g.write(dst,(g.C/z['path']).read_bytes())
        archive=g.K/'reviewed_pending_administration'; archive.mkdir()
        for n in sorted(g.ADMIN):
            target=archive/n;target.parent.mkdir(parents=True,exist_ok=True);g.write(target,(g.C/n).read_bytes(),exclusive=True)
        g.write(archive/'MANIFEST.json',(g.C/'MANIFEST.json').read_bytes(),exclusive=True)
        for n in g.ADMIN:
            value=g.load(g.K/n); value.update(**g.SCIENCE,**pins,id=2912,current_context_path='CURRENT_CONTEXT_PRESENT.md',current_audit_scope_path='CURRENT_AUDIT_SCOPE_PRESENT.md',current_gate='accepted_qualified_partial',current_verdict=g.WHOLE_VERDICT,status='unsolved_accepted_standard_partial_integration_pending_remote_verification',new_whole_current_gate=g.WHOLE_VERDICT,historical_verdict_transferred=False); g.dump(g.K/n,value)
        for n in ['CURRENT_ACCEPTANCE_SCOPE.md','CURRENT_CONTEXT_PRESENT.md','CURRENT_AUDIT_SCOPE_PRESENT.md']:g.write(g.K/n,PRESENT_SCOPE.encode(),exclusive=True)
        g.write(g.A/'integration_merge_queue_before.md',automatic,exclusive=True)
        g.require(g.Q.read_bytes()==automatic and g.git('rev-parse','HEAD')==pre['main_before'] and g.git('rev-parse','MERGE_HEAD')==g.HEAD,'Merge preimage changed during overlay'); g.fresh_check(pre,{qpath})
        g.write(g.Q,after)
        g.dump(g.K/'ACCEPTED_QUEUE_PATCH.json',{'utc':now,'header_names':g.HEADER,'column_count':12,'named_changes':['Status','Turns','Findings'],'whole_before_sha256':g.sha(before),'whole_after_sha256':g.sha(after),'row_before':g.selected(before),'row_after':row,'all_other_bytes_preserved':True,'selected_chat_DOI_preserved':True,'fresh_preimage_sha256':a.fresh_preimage_sha256},exclusive=True)
        g.canonical(frozen)
        rr=[{'path':n,'bytes':len((g.K/n).read_bytes()),'sha256':g.sha((g.K/n).read_bytes())} for n in sorted(g.canonical_names(frozen))]
        g.dump(g.A/'integration_check.json',{'schema':'pr44-original-head-overlay/v1','utc':now,**pins,'canonical_overlay_files':rr,'whole_queue_after_sha256':g.sha(after),'automatic_merge_queue_preimage_sha256':g.sha(automatic),'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'remote_pending':True},exclusive=True)
        g.fresh_check(pre,{qpath}); print('OVERLAY PASS PR44; root stages exact owned paths and commits'); return
    overlay=g.overlay_record(pins,frozen); g.canonical(frozen)
    g.require(g.Q.read_bytes()==after,'Whole accepted named-column queue differs'); g.fresh_check(pre,{'unsolved_math_prioritization/QUEUE.md'})
    if a.phase=='prepush':
        g.required(observation,{'state':'OPEN','isDraft':False,'body':BODY},'Actual ready prepush')
        g.require(not g.git('diff','--cached','--name-only') and not g.git('diff','--name-only','--',g.K.relative_to(g.R).as_posix(),'unsolved_math_prioritization/QUEUE.md'),'Commit exact canonical and queue first')
        merge=g.git('rev-parse','HEAD'); tree=g.tree(merge,pre,overlay,after)
        g.dump(g.A/'integration_prepush.json',{'schema':'pr44-original-head-prepush/v1','utc':now,**pins,'merge_commit':merge,'merge_tree':tree,'merge_parents':[pre['main_before'],g.HEAD],'canonical_overlay_files':overlay['canonical_overlay_files'],'whole_queue_after_sha256':g.sha(after),'remote_before_push':observation,'actual_push_performed_by_helper':False},exclusive=True)
        print('PREPUSH PASS PR44; root pushes actual exact merge'); return
    g.required(observation,{'state':'MERGED','isDraft':False,'body':BODY},'Actual MERGED body'); g.require(type(observation['mergedAt']) is str and observation['mergedAt'],'Actual merge date required')
    merge=observation['mergeCommit']['oid']; push=g.prepush_record(pins); g.require(push['merge_commit']==merge and g.equal(push['canonical_overlay_files'],overlay['canonical_overlay_files']),'Actual remote/prepush tree binding differs')
    tree=g.tree(merge,pre,overlay,after); g.require(tree==push['merge_tree'],'Actual real merge tree differs')
    g.require(not (g.K/'acceptance.json').exists() and not (g.K/'ACCEPTANCE.md').exists() and not (g.A/'acceptance.json').exists(),'New lowercase accepted receipt must be absent')
    before_inv=g.load(g.A/'integration_inventory_before.json'); inv=g.derive_inventory(before_inv,observation,now)
    inventory_guard(before_inv,inv,observation,now)
    g.dump(g.A/'remote_merge_receipt.json',observation,exclusive=True)
    final={'schema':'pr44-actual-integration-finalization/v1','utc':now,**pins,'pr':44,'before_inventory_sha256':pre['inventory_before_sha256'],'remote_merge_receipt':g.pin(g.A/'remote_merge_receipt.json'),'merge_commit':merge,'merge_tree':tree,'source_sha256':g.sha((g.HERE/'integrate_reviewed_partial.py').read_bytes())}
    g.dump(g.A/'integration_finalization.json',final,exclusive=True)
    g.finalization(pins,pre)
    for n in g.ADMIN:
        value=g.load(g.K/n); value.update(status='unsolved_accepted_standard_partial_merged',merge_commit=merge,merge_tree=tree,merged_at=observation['mergedAt']); g.dump(g.K/n,value)
    accept=g.expected_acceptance(pins,pre)
    g.accepted_invariants(accept,pins,pre); g.dump(g.K/'acceptance.json',accept,exclusive=True)
    g.write(g.K/'ACCEPTANCE.md',('# Accepted unsolved standard-partial partial: 2912 / KP-4.36\n\n'+BODY+'\nActual original-head merge '+merge+', tree '+tree+'. Full exact final reconciliation '+a.final_receipt_sha256+'; original2/5 exact two-turn ledger, source, absent raw prior and SQL fallback remain unchanged.\n').encode(),exclusive=True)
    names=g.canonical_names(frozen,True)-{'MANIFEST.json'}; g.exact(g.K,names)
    rr=[{'path':n,'bytes':len((g.K/n).read_bytes()),'sha256':g.sha((g.K/n).read_bytes())} for n in sorted(names)]
    g.dump(g.K/'MANIFEST.json',{'schema':'pr44-accepted-strict-self-excluding-closure/v1','utc':now,'self_excluded':['MANIFEST.json'],'files_count':len(rr),'files':rr,'foreign_excluded_prefixes':[]},exclusive=True)
    g.manifest(g.K,'MANIFEST.json'); g.canonical(frozen,True)
    for f in g.K.rglob('*'):
        if f.is_file(): f.chmod(0o444)
    g.dump(g.A/'acceptance.json',{**accept,'canonical_manifest_sha256':g.sha((g.K/'MANIFEST.json').read_bytes()),'canonical_manifest_entries':len(rr)},exclusive=True)
    g.manifest(g.K,'MANIFEST.json',frozen=True)
    g.accepted_invariants(g.load(g.K/'acceptance.json'),pins,pre); g.accepted_invariants(g.load(g.A/'acceptance.json'),pins,pre,audit=True)
    g.fresh_check(pre,{'unsolved_math_prioritization/QUEUE.md'}); g.dump(g.B/'inventory.json',inv); inventory_guard(before_inv,g.load(g.B/'inventory.json'),observation,now); g.foreign_check(pre)
    note='\n## '+now+' — PR44 actual accepted qualified scoped partial\n\nWorkflow100%; scientific discovery0%; original2/5,new0,audit0. Actual MERGED original-head/tree checked. Program33/180=18.3333%; one present native mirror remains. No paper/newDOI/tracker/release.\n'
    logdir=g.A/'integration_log_preimages'; g.require(not logdir.exists() and not logdir.is_symlink(),'New retained log-preimage directory required'); logdir.mkdir()
    log_receipt=[]
    for name,f in [('root_problem',g.A/'ROOT_RESEARCH_LOG.md'),('program',g.B/'RESEARCH_LOG.md')]:
        f=g.regular(g.R,f.relative_to(g.R).as_posix()); previous=f.read_bytes(); before_pin=g.pin(f)
        g.write(logdir/(name+'.bin'),previous,exclusive=True)
        g.require(f.read_bytes()==previous,'Actual research-log preimage changed before append')
        g.write(f,previous+note.encode()); log_receipt.append({'log':f.relative_to(g.R).as_posix(),'before':before_pin,'retained_preimage':g.pin(logdir/(name+'.bin')),'after':g.pin(f)})
    g.dump(g.A/'integration_log_append_receipt.json',{'utc':g.stamp(),'logs':log_receipt,'note':note,'source_preparation_did_not_append':True},exclusive=True)
    print('FINALIZE PASS PR44; root present native mirror remains')


if __name__=='__main__': main()
