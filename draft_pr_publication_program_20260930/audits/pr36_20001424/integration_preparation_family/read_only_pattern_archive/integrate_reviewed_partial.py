"""Guarded administrative integration of the two already-reviewed partial packets.

Never changes a frozen candidate, scientific file, original ledger or old review.
Original PR heads are merged on main separately; this helper resolves only the
current named queue row and copies the reviewed packet with archived admin fields.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, shutil, subprocess
R=Path(__file__).resolve().parents[3]; B=R/'draft_pr_publication_program_20260930'
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R).decode().strip()
CONFIG={34:('7000004','already_solved',2,1,'RESULT.md','reviewed_candidate_v2','source_first_whole_adversary','ROOT_FINAL_SOURCE_FIRST_ACTUAL_REPRODUCTION.json','8afc9a17669c12559aea4287117069a20fbb39eea2af4ffe9bba81d7586a702a','59d86e181c3f269f6af5c57d4b3541baeda6f25a35120320f37c18500f23ae9b'),
35:('2744','unsolved',1,0,'OBSTRUCTION.md','reviewed_candidate','current_whole_adversary','ROOT_NEW_WHOLE_REPRODUCTION.json','65e7ac9d28b8504346d68c771256c2f4642c374d07bbce06bdaecfe85b8f644a','ad28abe21b169dcf49f7cf084cb8e16f55df5d3034b131e9525915ed54973f37')}
def files_bound(base,manifest):
    rows=load(manifest)['files']
    assert len({z['path'] for z in rows})==len(rows)
    for z in rows:
        p=base/z['path'];assert not p.is_symlink();b=p.read_bytes()
        assert len(b)==z['bytes'] and sha(b)==z['sha256'],str(p)
        if '.jsonl' in p.name:
            for line in b.splitlines():json.loads(line)
        elif '.json' in p.name:json.loads(b)
    return rows
def main():
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['preflight','overlay','finalize']);ap.add_argument('--pr',type=int,choices=CONFIG,required=True);a=ap.parse_args()
    identity,status,used,new,artifact,current,family,receipt,csha,hsha=CONFIG[a.pr]
    A=B/'audits'/('pr'+str(a.pr)+'_'+identity);C=A/current;H=A/family;K=R/'unsolved_math_prioritization/attempts'/identity;Q=R/'unsolved_math_prioritization/QUEUE.md'
    assert git('branch','--show-current')=='main'
    assert sha((C/'MANIFEST.json').read_bytes())==csha and sha((H/'MANIFEST.json').read_bytes())==hsha
    frozen=files_bound(C,C/'MANIFEST.json');files_bound(H,H/'MANIFEST.json')
    for z in load(C/'CURRENT_PROOF_DEPENDENCIES.json')['files']:
        b=(A/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
    root=load(A/receipt);assert root['status']=='PASS' and not root['mandatory_corrections' if a.pr==34 else 'mandatory_current_packet_corrections']
    sm=load(A/'snapshot_manifest.json');head=sm['head'];patch=load(C/'CURRENT_QUEUE_PATCH.json');now=stamp()
    remote=json.loads(subprocess.check_output(['gh','pr','view',str(a.pr),'--json','number,url,title,state,isDraft,headRefOid,headRefName,mergeCommit,mergedAt,body'],cwd=R))
    assert remote['headRefOid']==head and remote['headRefName']=='dot/math-'+identity
    prefix='unsolved_math_prioritization/attempts/'+identity+'/'
    for z in sm['files']:
        assert subprocess.check_output(['git','show',head+':'+prefix+z['path']],cwd=R)==(C/'original_archive'/z['path']).read_bytes()
    admin=['README.md','pr_body.md','readiness.json','current_status.json','CURRENT_AUDIT_SCOPE.md','RESEARCH_LOG.md']
    admin+=['CURRENT_SOURCE_CONTEXT.json','CURRENT_RESEARCH_LOG.md'] if a.pr==34 else ['PR_DRAFT.md','provenance.json']
    if a.pr==34:
        body='# Accepted credited counterexample to Ghomi2019 Problem1.4\n\nThe smooth embedded curve Gamma=(cos t,sin t,cos(2t)/4) has positive curvature and globally injective unit Frenet binormal B=(-cos^3 t,sin^3 t,1)/sqrt(1+cos^6 t+sin^6 t). For every0<epsilon<1/3, Gamma+epsilon B is embedded and disjoint, with linking number0 by the explicit orientation-preserving shear and spanning-disk proof.\n\nDisposition already_solved: this is a verified elementary consequence of the exact section2 construction in Ni, Zhang and Zhang, arXiv2606.29231v1, submitted2026-06-28. That source does not print this linking theorem or identify Ghomi; earliest explicit recognition is unestablished. The four stationary binormal values exclude the later strictly-negative-surface-curvature question, which remains outside this result. No novel paper, newDOI or tracker row.\n\nThree distinct original approach families, root proof/source reproduction, and a genuinely source-first NEW complete final v2 adversary passed. Root actually replayed its final closed179-member package and16 outer invocations,77 independent checks,7 mathematical mutants and20 packet mutants. Earlier v1 metadata failure and second v2 ordering violation remain archived and qualified. No old partial verdict is transferred.\n\nCumulative2/5 substantive responses: original1 plus explicitly charged counterexample1; audit0. Extensive AI use; unrefereed AI-audited documentation, without external human review or formal proof-assistant verification. Full proof RESULT.md and acceptance/source/version qualifications in the canonical attempt folder.\n'
        findings='2026-10-02: Accepted credited negative answer to literal2019 GhomiProblem1.4: smooth injective unit binormal has four stationary values; every0<epsilon<1/3 gives embedded disjoint zero-linking push-off. Exact verified elementary consequence of Ni-Zhang-Zhang2606.29231v1 construction; earliest recognition unestablished, later strictly-negative-curvature target excluded. Final genuine source-first gate and actual root replay clean. Original1+new1=2/5, audit0; no paper/newDOI/tracker. PR: https://github.com/AlecKriebel/Math/pull/34.'
    else:
        body='# Accepted unresolved KP-1.85 partial findings\n\nThe universal target remains unresolved: every hyperbolic knot in S3 should have a nonconstant SO(3) character arc on the specified oriented complete-holonomy PSL2(C) component. The original finite-quotient/compact-lifting normalization and conditional complex-conjugation obstruction are valid. Known Euclidean-cone and hyperbolic two-bridge cases are credited. No universal qualifying cone metric, canonical-component bridge or qualifying knot counterexample is supplied.\n\nThree independently sealed algebraic/cone/primary-source families and a NEW genuinely source-first complete current-packet adversary passed. Root independently read the universal certificates and operative primary proofs and actually reproduced9 outer plus6 direct implementations,329 bookkeeping/control checks,33 new scientific diagnostics,6 executed scientific mutants and4 expected false-prose coverage controls. These supplement the proofs and do not resolve the universal gap.\n\nAccepted unsolved partial result, original1/5 substantive response, new0 and audit0. No paper, newDOI or tracker row. Original15 artifacts, full raw source, dated provenance, original review and attempt ledger are preserved. Extensive AI use; unrefereed AI-audited documentation, without external human review or formal proof-assistant verification.\n'
        findings='2026-10-02: Accepted unsolved partial after complete new source-first gate and root actual reproduction. Finite-quotient/compact-lifting normalization and conditional conjugation obstruction valid; credited Dix cone criterion and hyperbolic two-bridge cases. No general SO3 arc on specified oriented complete PSL2 component, universal cone existence or qualifying knot counterexample. Original1/5,new0,audit0; no paper/newDOI/tracker. PR: https://github.com/AlecKriebel/Math/pull/35.'
    if a.phase=='preflight':
        assert remote['state']=='OPEN' and remote['isDraft'] and not K.exists()
        assert not git('diff','--cached','--name-only') and not (R/'.git/MERGE_HEAD').exists()
        q=Q.read_bytes();assert q.count(patch['row_before'].encode())==1
        (A/'integration_queue_before.md').write_bytes(q)
        dump(A/'integration_preflight.json',{'utc':now,'pr':remote,'main_before':git('rev-parse','HEAD'),'whole_queue_before_sha256':sha(q),'dated_reviewed_queue_before_sha256':patch['whole_queue_preimage_sha256'],'selected_original_named_row_unchanged':True,'reviewed_candidate_manifest_sha256':csha,'new_gate_manifest_sha256':hsha,'root_actual_receipt_sha256':sha((A/receipt).read_bytes()),'state_before_sha256':sha((R/'unsolved_math_prioritization/state.json').read_bytes()),'history_before_sha256':sha((R/'unsolved_math_prioritization/history.jsonl').read_bytes()),'attempts':str(used)+'/5','new_substantive_attempts':new,'paper_DOI_tracker':False})
        (A/'accepted_pr_body.md').write_text(body)
        print('PREFLIGHT PASS',a.pr);return
    pre=load(A/'integration_preflight.json')
    if a.phase=='overlay':
        assert remote['state']=='OPEN' and not remote['isDraft'] and remote['body']==body
        assert git('rev-parse','MERGE_HEAD')==head and git('rev-parse','HEAD')==pre['main_before']
        unresolved=git('diff','--name-only','--diff-filter=U').splitlines()
        assert set(unresolved)<= {'unsolved_math_prioritization/QUEUE.md'}
        q=(A/'integration_queue_before.md').read_bytes();assert sha(q)==pre['whole_queue_before_sha256']
        for key in ['state','history']:
            p=R/'unsolved_math_prioritization'/(key+('.json' if key=='state' else '.jsonl'));assert sha(p.read_bytes())==pre[key+'_before_sha256']
        originals={z['path'] for z in sm['files']}
        assert {str(p.relative_to(K)) for p in K.rglob('*') if p.is_file()}==originals
        for z in sm['files']:assert sha((K/z['path']).read_bytes())==z['sha256']
        for z in frozen:
            d=K/z['path'];d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(C/z['path'],d)
        # Remove only byte-verified original top-level paths absent from the reviewed
        # current packet; every removed byte survives in original_archive.
        for rel in originals-{z['path'] for z in frozen}:
            p=K/rel;assert p.read_bytes()==(K/'original_archive'/rel).read_bytes();p.unlink()
        archive=K/'reviewed_pending_administration';archive.mkdir()
        for rel in admin:shutil.copyfile(K/rel,archive/rel)
        shutil.copyfile(C/'MANIFEST.json',archive/'MANIFEST.json')
        (K/'pr_body.md').write_text(body)
        if a.pr==35:(K/'PR_DRAFT.md').write_text(body)
        (K/'README.md').write_text(body+'\nAll original source/ledger/scientific bytes and the reviewed prospective administration are preserved. CURRENT_PROOF_DEPENDENCIES.json resolves from repository audit anchor '+str(A.relative_to(R))+', including its ../ paths after canonical copying. The archived pending gates are historical. Accepted audit receipt and remote merge binding are recorded separately.\n')
        ready=load(K/'readiness.json');ready.update(status='complete_current_gate_accepted_partial_integration',completion_estimate_percent=100,workflow_completion_estimate_percent=100,remaining_gap=('Later strictly-negative-curvature target remains outside scope; earliest explicit recognition unestablished.' if a.pr==34 else ready['remaining_gap']),independent_review='NEW complete source-first adversary and root actual final closure reproduction passed; exact frozen manifests bound in ACCEPTANCE.md.',accepted_at_utc=now,new_whole_manifest_sha256=hsha,reviewed_candidate_manifest_sha256=csha)
        dump(K/'readiness.json',ready)
        st=load(K/'current_status.json');st.update(current_gate='PASS_complete_source_first_and_root_actual_reproduction',queue_status=status,workflow_completion_estimate_percent=100,accepted_at_utc=now,new_whole_manifest_sha256=hsha)
        dump(K/'current_status.json',st)
        extra='CURRENT_SOURCE_CONTEXT.json' if a.pr==34 else 'provenance.json';v=load(K/extra);v.update(accepted_disposition=status,current_complete_gate='PASS',accepted_at_utc=now,dependency_anchor_repository_relative=str(A.relative_to(R)))
        if a.pr==35:v['status']='unsolved_accepted_partial'
        dump(K/extra,v)
        (K/'CURRENT_AUDIT_SCOPE.md').write_text('Accepted '+status+' partial for '+identity+'. The exact frozen scientific/source/ledger scope passed NEW complete source-first review '+hsha+' and root actual final-closure replay. Original reviews, v1 failures and prospective administration are historical; no old clean verdict transferred. All mathematical/source/dependency/ledger bytes are unchanged. Dependency paths resolve from repository audit anchor '+str(A.relative_to(R))+'. Queue integration changes only named Status, Turns and Findings; current mirror and actual remote merge are recorded separately. No paper/newDOI/tracker or human peer review.\n')
        note='\n## '+now+' — Accepted complete-gate partial integration\n\nWorkflow100% for scientific validation; guarded remote acceptance remains to be verified. Disposition '+status+', substantive'+str(used)+'/5, audit0. NEW source-first gate '+hsha+'; actual root final-manifest replay complete. Science/raw source/attempt ledger unchanged; reviewed pending administration archived. No paper/newDOI/tracker.\n'
        for rel in ['RESEARCH_LOG.md']+(['CURRENT_RESEARCH_LOG.md'] if a.pr==34 else []):
            with (K/rel).open('a') as f:f.write(note)
        before=patch['row_before'].split('|');after=before.copy();after[8]=' '+status+' ';after[9]=' '+str(used)+'/5 ';after[11]=' '+findings+' '
        row='|'.join(after);assert len(after)==14 and all(before[i]==after[i] for i in range(14) if i not in [8,9,11])
        updated=q.replace(patch['row_before'].encode(),row.encode());assert updated.replace(row.encode(),patch['row_before'].encode())==q
        Q.write_bytes(updated)
        dump(K/'ACCEPTED_QUEUE_PATCH.json',{'utc':now,'named_changes':['Status','Turns','Findings'],'whole_before_sha256':sha(q),'whole_after_sha256':sha(updated),'row_before':patch['row_before'],'row_after':row,'all_other_bytes_preserved':True,'dated_reviewed_patch_unchanged':True})
        for z in frozen:
            if z['path'] not in admin:assert (K/z['path']).read_bytes()==(C/z['path']).read_bytes(),z['path']
        dump(A/'integration_check.json',{'utc':now,'pr':a.pr,'original_head':head,'queue_before_sha256':sha(q),'queue_after_sha256':sha(updated),'whole_queue_exact_single_row_replacement':True,'selected_chat_DOI_and_all_other_rows_fields_preserved':True,'science_source_ledger_dependency_bytes_unchanged':True,'reviewed_pending_admin_archived':True,'canonical_scientific_artifact_sha256':sha((K/artifact).read_bytes()),'attempts':str(used)+'/5','new_substantive_attempts':new,'remote_pending':True,'paper_DOI_tracker':False})
        print('OVERLAY PASS',a.pr);return
    assert remote['state']=='MERGED' and remote['isDraft'] is False and remote['mergedAt']
    merge=remote['mergeCommit']['oid'];parents=git('show','-s','--format=%P',merge).split();assert parents==[pre['main_before'],head]
    assert git('merge-base','--is-ancestor',merge,'HEAD')==''
    dump(A/'remote_merge_receipt.json',{k:remote[k] for k in ['number','url','state','isDraft','headRefOid','mergeCommit','mergedAt']})
    acceptance={'utc':now,'pr':a.pr,'id':int(identity),'problem_id':int(identity),'problem_number':load(K/'source_record.json')['problem_number'],'outcome':status+'_accepted_partial_merged','queue_status':status,'original_head':head,'merge_commit':merge,'merge_parents':parents,'merged_at':remote['mergedAt'],'remote_state':'MERGED','remote_isDraft':False,'canonical_scientific_artifact_sha256':sha((K/artifact).read_bytes()),'reviewed_candidate_manifest_sha256':csha,'fresh_manifest_sha256':hsha,'original_substantive_attempts':used-new,'new_substantive_attempts':new,'substantive_attempts_used':used,'substantive_attempt_limit':5,'verification_attempts_added':0,'positive_novelty_claim':False,'paper_or_new_doi_or_tracker':False,'human_peer_review_asserted':False,'workflow_completion_estimate_percent':100,'current_mirror':'Separate present source-bound acceptance; state_mirror_receipt.json, without reconstructed historical proof transitions.'}
    dump(K/'acceptance.json',acceptance)
    (K/'ACCEPTANCE.md').write_text('# Accepted '+status.upper()+' partial: '+identity+'\n\nExact original head '+head+' merged on main as '+merge+'; GitHub MERGED/nondraft/date independently verified. Full science '+artifact+' SHA256 '+acceptance['canonical_scientific_artifact_sha256']+' is unchanged from reviewed candidate '+csha+'. NEW genuinely source-first whole gate '+hsha+' and actual root replay passed. Original substantive'+str(used-new)+' plus new'+str(new)+' gives '+str(used)+'/5; audits0. No paper/newDOI/tracker, novelty priority or human peer review asserted.\n\nCurrent scientific/source/dependency/ledger bytes remain unchanged; original artifacts and reviewed pending administration archived. Dependency paths resolve from repository audit anchor '+str(A.relative_to(R))+', not the copied canonical parent. CURRENT_QUEUE_PATCH.json remains the dated prospective snapshot; ACCEPTED_QUEUE_PATCH.json records the guarded actual named-row replacement. Earlier failures, corrected metadata, limited diagnostics and conditional source depth remain qualified by the complete audit reports.\n\n'+body)
    manifest=[{'path':str(p.relative_to(K)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(K.rglob('*')) if p.is_file() and p!=K/'MANIFEST.json']
    dump(K/'MANIFEST.json',{'utc':now,'scope':'Accepted canonical partial package; complete self-excluding manifest including original archive and reviewed pending administrative archive. Science unchanged.','files_count':len(manifest),'files':manifest})
    dump(A/'acceptance.json',{**acceptance,'canonical_manifest_sha256':sha((K/'MANIFEST.json').read_bytes()),'canonical_manifest_entries':len(manifest)})
    inv=load(B/'inventory.json');item=next(x for x in inv['items'] if x['number']==a.pr)
    item.update(stage='complete',outcome=status+'_accepted_partial',queue_status=status,audited_head=head,merge_commit=merge,merged_at=remote['mergedAt'],workflow_completion_estimate_percent=100,original_attempts=str(used-new)+'/5',new_substantive_attempts=new,cumulative_attempts=str(used)+'/5',paper_or_new_doi_or_tracker=False)
    done=sum(x.get('stage')=='complete' for x in inv['items'])
    inv.update(updated_at_utc=now,last_checkpoint_utc=now,completed_count=done,program_completion_estimate_percent=done/180*100,completion_estimate_percent=done/180*100,current_pr=a.pr+1);dump(B/'inventory.json',inv)
    note='\n## '+now+' — PR'+str(a.pr)+' accepted and remotely merged\n\nWorkflow100%. '+status+' partial; exact head '+head+', merge '+merge+'. Complete NEW source-first gate/root actual replay clean, science/source/ledger unchanged, original/pending records archived. Budget'+str(used)+'/5, audit0; no paper/newDOI/tracker. Program'+str(done)+'/180='+str(round(done/180*100,4))+'%; PR18/20 holds retained. Current mirror follows exact source/remote/package verification.\n'
    for p in [A/'RESEARCH_LOG.md',B/'RESEARCH_LOG.md']:
        with p.open('a') as f:f.write(note)
    print('FINALIZE PASS',a.pr,'completed',done,'canonical_members',len(manifest))
if __name__=='__main__':main()
