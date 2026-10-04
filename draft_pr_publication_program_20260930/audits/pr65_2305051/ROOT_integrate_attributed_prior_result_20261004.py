"""Prospective exact-head merge/current mirror. Requires final ROOT gate and real writer acknowledgement."""
from pathlib import Path
import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import sqlite3
import stat
import subprocess
import sys

A=Path(__file__).resolve().parent
P=A.parents[1]
R=P.parent
HEAD='5cc1602c05d79502defb07cec7027963149494d2'
ID='2305051'
CODE='AMR-022-5051'
QUEUE='unsolved_math_prioritization/QUEUE.md'
PREFIX='unsolved_math_prioritization/attempts/'+ID
STATE='unsolved_math_prioritization/state.json'
HISTORY='unsolved_math_prioritization/history.jsonl'
GOAL=Path('/Users/alec/.codex/attachments/4df73d3d-641f-4907-b9ad-c47c468f2589/goal-objective.md')
GOAL_SHA='1e29852cafce156dbc3b745f9d1b7bf973b6d07e4a3c924b901ad27754128d04'
PAUSE='PR65 attributed prior-result integration 20261004'
NOTE='Verified normalized pure-Blaschke Bloch construction; already-resolved Holland target from AAN1999 with explicit attribution HL2019; Kahane mechanism printed Piranian1966 and DSS1966 bridge credited; modified child ordering, exact-method/earliest priority unestablished; accepted attributed progress; AI-assisted unrefereed; original2/5; no new paper/DOI/tracker'

def sha(b):return hashlib.sha256(b).hexdigest()
def jb(v):return (json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def must(ok,msg):
    if not ok:raise RuntimeError(msg)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('phase',choices=['merge','mirror'])
    args=ap.parse_args()
    must(not sys.flags.optimize and __debug__ and sys.flags.ignore_environment and sys.flags.dont_write_bytecode,'Invoke -E -B without optimization')
    O=A/'native_attributed_result_operations_20261004'
    O.mkdir(exist_ok=True)
    D=Path('/Users/alec/.cache/codex-pr65-priority-20261004')/('ROOT_native_'+args.phase+'_20261004')
    D.mkdir(exist_ok=False)
    (D/'PRELAUNCH_OPERATOR.py').write_bytes(Path(__file__).read_bytes())
    commands=[]
    def run(argv,allowed=(0,)):
        now=dt.datetime.now(dt.timezone.utc).isoformat()
        child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err=child.communicate()
        number=str(len(commands)+1)
        (D/(number+'.stdout')).write_bytes(out);(D/(number+'.stderr')).write_bytes(err)
        row={'argv':argv,'cwd':str(R),'actual_child_pid':child.pid,'started_utc':now,'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':child.returncode,'stdout_private_path':str(D/(number+'.stdout')),'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_private_path':str(D/(number+'.stderr')),'stderr_bytes':len(err),'stderr_sha256':sha(err)}
        commands.append(row);(O/(args.phase+'_ACTUAL_COMMANDS.json')).write_bytes(jb(commands))
        must(child.returncode in allowed,'Operation failed; preserve partial state and inspect actual streams')
        return out,child.returncode
    def git(*parts):return run(['git','--no-optional-locks',*parts])[0]
    def pin(p):return {'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
    def check_pin(row):
        p=R/row['path'];p.resolve().relative_to(R)
        must(not p.is_symlink() and p.is_file() and sha(p.read_bytes())==row['sha256'] and len(p.read_bytes())==row['bytes'],'Reviewed evidence drift')
    G=A/'ROOT_PROVIDED_SOURCE_FINAL_DISPOSITION_20261004.json'
    gate=json.loads(G.read_bytes());gate_pin=pin(G)
    must(gate['ROOT_authorizes_guarded_attributed_prior_result_acceptance'] is True and gate['expected_original_head']==HEAD and gate['PR']==65,'Final ROOT disposition absent')
    must(gate['fresh_final_adversary_clean'] is True and gate['ROOT_personally_read_all_four_new_reports'] is True and gate['new_solution_priority_clearance'] is False and gate['audited_outcome']=='already_solved','Scientific gate differs')
    must(gate['candidate_mathematics_verified'] is True and gate['prior_resolution_of_exact_original_problem_verified'] is True and gate['original_proof_turns']=='2/5' and gate['new_original_proof_turns']==0,'Target/budget gate differs')
    must(gate['publication_authorized'] is False and gate['new_paper'] is False and gate['new_DOI'] is None and gate['tracker_append'] is False and gate['PR50_exception_extended'] is False,'Prior-result publication exclusion differs')
    must(sha(GOAL.read_bytes())==GOAL_SHA==gate['goal_objective_sha256'],'Authoritative goal drift')
    for row in gate['bound_current_evidence']:check_pin(row)
    source_root=A/'original_source_authentication_20261004'
    manifest=json.loads((source_root/'ORIGINAL_BLOB_MANIFEST.json').read_bytes())
    originals=[x for x in manifest['artifacts'] if x['incoming_changed_domain'] and x['path']!=QUEUE]
    must(len(originals)==18,'Original incoming science domain differs')
    original_paths={x['path'] for x in originals}
    merge_paths=original_paths|{QUEUE}
    mirror_paths={PREFIX+'/acceptance.json',PREFIX+'/CURRENT_RESULT.md',PREFIX+'/CURRENT_PRIORITY_SPECIALIZATION.md',STATE,HISTORY}
    source=json.loads((source_root/'original'/PREFIX/'source_record.json').read_bytes())
    def check_originals(commit):
        for row in originals:
            must(sha(git('show',commit+':'+row['path']))==row['sha256'],'Original body drift')
            ls=git('ls-tree',commit,'--',row['path']).decode().split()
            must(ls[0]==row['mode'] and ls[2]==row['git_blob_SHA1'],'Original mode/blob drift')
    # Audit/program paths belong to this writer but are not staged by native phases.
    owned=merge_paths|mirror_paths
    def is_owned(p):return p in owned or p.startswith(str(A.relative_to(R))+'/') or p in {str((P/'CURRENT_PROGRESS.json').relative_to(R))}
    def foreign_index():return b'\0'.join(x for x in git('ls-files','--stage','-z').split(b'\0') if x and not is_owned(x.split(b'\t',1)[1].decode()))
    def foreign_dirty():return {x.decode() for x in git('diff','--name-only','-z').split(b'\0') if x and not is_owned(x.decode())}
    def body(p):
        q=R/p
        if not q.exists() and not q.is_symlink():return {'exists':False}
        must(stat.S_ISREG(q.lstat().st_mode),'Foreign dirty nonregular path; inspect')
        return {'exists':True,'mode':q.lstat().st_mode,'sha256':sha(q.read_bytes())}
    must(git('branch','--show-current').strip()==b'main','Stay on main')
    must(not git('diff','--cached','--name-only','-z'),'Shared index occupied; preserve foreign staging')
    mh=Path(git('rev-parse','--git-path','MERGE_HEAD').decode().strip())
    if not mh.is_absolute():mh=R/mh
    must(not mh.exists(),'Existing merge must remain untouched')
    base=git('rev-parse','HEAD').decode().strip()
    must(git('ls-remote','--heads','origin','main').decode().split()[0]==base,'Main/remote diverged')
    bases={base}
    if args.phase=='mirror':
        prior=json.loads((O/'NATIVE_MERGE_RESULT.json').read_bytes())
        must(prior['submitted_head']==HEAD and prior['merge_commit']==base and prior['gate']==gate_pin,'Actual merge continuity differs')
        must(git('show','-s','--format=%P',base).decode().split()==[prior['base'],HEAD],'Exact two-parent merge differs')
        bases.add(prior['base'])
    ack_path=R/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
    def check_window():
        w=json.loads(ack_path.read_bytes())
        must(w['shared_git_writes_paused'] is True and w['paused_for']==PAUSE,'Real exact writer acknowledgement absent')
        must(w['dirty_tracked_bodies_modes_frozen_after_acknowledgement'] is True and w['all_staged_path_count']==0 and not w['owned_staged_paths'],'Writer body/index freeze absent')
        must(w['local_main_at_pause']==w['remote_main_at_pause'] and w['local_main_at_pause'] in bases,'Acknowledged baseline differs')
        must(w.get('utc',w.get('UTC',''))>=gate['UTC'],'Acknowledgement predates final disposition')
        return w
    window=check_window();(D/'ACKNOWLEDGED_WINDOW.json').write_bytes(jb(window))
    fi=foreign_index();fd=foreign_dirty();fb={p:body(p) for p in fd}
    def preserve():
        check_window()
        must(foreign_index()==fi and foreign_dirty()==fd and all(body(p)==v for p,v in fb.items()),'Foreign tracked/index state changed')
        must(pin(G)==gate_pin and sha(GOAL.read_bytes())==GOAL_SHA,'Final gate/goal changed')
        for row in gate['bound_current_evidence']:check_pin(row)
    raw_manifest=json.loads((R/'unsolved_math_prioritization/manifest.json').read_bytes())
    must(raw_manifest['revision']==source['dataset_revision'],'Raw revision changed')
    for name in ('problems.json','research_results.json'):
        b=(R/'unsolved_math_prioritization/cache'/name).read_bytes()
        must({'bytes':len(b),'sha256':sha(b)}==raw_manifest['files'][name],'Raw manifest/body differs')
    problems=json.loads((R/'unsolved_math_prioritization/cache/problems.json').read_bytes())
    matches=[p for p in problems if str(p['id'])==ID]
    reports=json.loads((R/'unsolved_math_prioritization/cache/research_results.json').read_bytes())
    must(matches==[source['problem']] and CODE in reports and reports[CODE]==source['upstream_report'],'Exact raw typed problem/report differs')
    with sqlite3.connect('file:'+str(R/'unsolved_math_prioritization/cache/catalog.sqlite')+'?mode=ro',uri=True) as db:
        row=db.execute('SELECT payload,report FROM records WHERE key=?',(ID,)).fetchone()
        revisions=db.execute('SELECT revision FROM metadata').fetchall()
    must(row is not None and json.loads(row[0])==source['problem'] and row[1] is not None and json.loads(row[1])==source['upstream_report'] and revisions==[(source['dataset_revision'],)],'Exact SQL typed pair differs')
    review_hash=sha(json.dumps([source['problem'],source['upstream_report']],sort_keys=True).encode())
    catalog=[p for p in json.loads((R/'unsolved_math_prioritization/catalog.json').read_bytes()) if p['id']==ID]
    must(len(catalog)==1 and catalog[0]['review_hash']==review_hash,'Current source review fingerprint differs')
    identity={'review_hash':review_hash,'dataset_revision':source['dataset_revision'],'raw_problem_SQL_wrapper_identical':True,'raw_report_present_nonNULL_nonempty_and_SQL_wrapper_identical':True,'historical_OPEN_TRIAGE_not_current_priority_authority':True}
    preserve()
    pr=json.loads(run(['gh','pr','view','65','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,mergeCommit,mergedAt,url'])[0])
    must(pr['headRefOid']==HEAD and pr['baseRefName']=='main' and pr['headRefName']=='dot/math-'+ID,'Fresh PR identity changed')
    aq=json.loads(run(['gh','api','repos/AlecKriebel/Math/contents/'+QUEUE+'?ref='+HEAD])[0]);qb=base64.b64decode(aq['content'])
    qpin=next(x for x in manifest['artifacts'] if x['path']==QUEUE)
    must(sha(qb)==qpin['sha256'] and aq['sha']==qpin['git_blob_SHA1'],'Fresh head QUEUE differs')
    target=[s for s in qb.decode().splitlines() if '| '+ID+' /' in s]
    must(len(target)==1 and target[0].split('|')[8].strip()=='claimed_solved' and target[0].split('|')[9].strip()=='2/5','Fresh submitted eligibility differs')
    _,available=run(['git','--no-optional-locks','cat-file','-e',HEAD+'^{commit}'],allowed=(0,128))
    if available:
        must(args.phase=='merge','Merge object disappeared')
        preserve();git('fetch','--no-tags','--no-write-fetch-head','origin','refs/pull/65/head')
        check=json.loads(run(['gh','pr','view','65','--repo','AlecKriebel/Math','--json','headRefOid,state,isDraft'])[0])
        must(check['headRefOid']==HEAD and check['state']=='OPEN' and check['isDraft'] is True,'Head drift during object import')
    check_originals(HEAD)
    ledger=git('show',HEAD+':'+PREFIX+'/turns.jsonl')
    status=json.loads(git('show',HEAD+':'+PREFIX+'/status.json'))
    must([json.loads(s)['turn'] for s in ledger.splitlines()]==[1,2] and status['turns_used']==2 and status['turn_limit']==5,'Original turn ledger changed')
    qbefore=(R/QUEUE).read_bytes()
    must(qbefore==git('show',base+':'+QUEUE),'Native queue has uncommitted changes')
    if args.phase=='merge':
        must(pr['state']=='OPEN' and pr['isDraft'] is True,'Reviewed original open draft required')
        incoming=json.loads(run(['gh','api','repos/AlecKriebel/Math/pulls/65/files?per_page=100'])[0])
        must({p['filename'] for p in incoming}==merge_paths and len(incoming)==19,'Incoming scope changed')
        common=git('merge-base',base,HEAD).decode().strip()
        must({p.decode() for p in git('diff','--name-only','-z',common,HEAD).split(b'\0') if p}==merge_paths,'Local incoming scope changed')
        must(all(not (R/p).exists() and not (R/p).is_symlink() for p in original_paths),'Native target already exists')
        lines=qbefore.decode().splitlines(keepends=True);ii=[i for i,s in enumerate(lines) if '| '+ID+' /' in s]
        must(len(ii)==1,'Native row not unique');i=ii[0];cells=lines[i].split('|')
        must(len(cells)==14 and cells[8].strip()=='queued' and cells[9].strip()=='0/5' and not cells[12].strip(),'Native target baseline differs')
        cells[8]=' already_solved ';cells[9]=' 2/5 ';cells[11]=' '+NOTE+' ';lines[i]='|'.join(cells);accepted=''.join(lines).encode()
        preserve();_,exit_merge=run(['git','--no-optional-locks','merge','--no-ff','--no-commit',HEAD],allowed=(0,1))
        conflicts={p.decode() for p in git('diff','--name-only','--diff-filter=U','-z').split(b'\0') if p}
        must(conflicts<={QUEUE} and mh.read_text().strip()==HEAD,'Unexpected merge state; inspect retained partial merge')
        preserve();(R/QUEUE).write_bytes(accepted)
        for row in originals:must(sha((R/row['path']).read_bytes())==row['sha256'] and stat.S_IMODE((R/row['path']).stat().st_mode)==0o644,'Imported original body/mode differs')
        git('add','--',QUEUE)
        must(not git('diff','--name-only','--diff-filter=U','-z') and {p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==merge_paths,'Merge staged scope differs')
        preserve();git('commit','-m','Accept PR65 verified Blaschke construction as attributed prior-result progress')
        commit=git('rev-parse','HEAD').decode().strip()
        must(git('show','-s','--format=%P',commit).decode().split()==[base,HEAD] and {p.decode() for p in git('diff','--name-only','-z',base,commit).split(b'\0') if p}==merge_paths,'Exact merge commit differs')
        check_originals(commit);preserve();git('push','origin','main')
        receipt={'phase':'merge','base':base,'submitted_head':HEAD,'merge_commit':commit,'gate':gate_pin,'merge_exit_code':exit_merge,'conflicts':sorted(conflicts),'native_mirror_pending':True}
        out=O/'NATIVE_MERGE_RESULT.json'
    else:
        must(pr['state']=='MERGED' and pr['mergeCommit']['oid']==base,'GitHub has not independently confirmed exact merge')
        check_originals(base)
        sb=(R/STATE).read_bytes();hb=(R/HISTORY).read_bytes()
        must(sb==git('show',base+':'+STATE) and hb==git('show',base+':'+HISTORY),'Native state/history contain uncommitted changes')
        state=json.loads(sb);must(ID not in state and all(str(json.loads(s).get('id'))!=ID for s in hb.splitlines()),'Acceptance already exists')
        must(not hb or hb.endswith(b'\n'),'Incomplete history tail')
        must(all(not (R/p).exists() for p in mirror_paths-{STATE,HISTORY}),'Current acceptance destination exists')
        qt=[s for s in qbefore.decode().splitlines() if '| '+ID+' /' in s]
        must(len(qt)==1 and qt[0].split('|')[8].strip()=='already_solved' and qt[0].split('|')[9].strip()=='2/5' and qt[0].split('|')[11].strip()==NOTE and not qt[0].split('|')[12].strip(),'Current queue differs')
        now=dt.datetime.now(dt.timezone.utc).isoformat();F=A/'attributed_prior_result_preparation_20261004'
        current=(F/'CURRENT_RESULT.md').read_text().replace("Proposed disposition, pending ROOT's reading of the fresh independent final adversary:","Accepted after ROOT's final adjudication and the clean fresh independent final adversary:").replace('Native status, GitHub result and program completion will be recorded only after actual execution and independent readback.','acceptance.json records the actual exact-head merge and current acceptance; program completion requires its separate independent readback.')
        (R/(PREFIX+'/CURRENT_RESULT.md')).write_text(current)
        (R/(PREFIX+'/CURRENT_PRIORITY_SPECIALIZATION.md')).write_bytes((F/'CURRENT_PRIORITY_SPECIALIZATION.md').read_bytes())
        acceptance={'schema':'pr65-current-attributed-prior-result-acceptance/v1','at':now,'actual_author_pid':os.getpid(),'problem_id':ID,'problem_code':CODE,'pr':65,'reviewed_head':HEAD,'merge_commit':base,'merged_at':pr['mergedAt'],'status':'already_solved','accepted_as':'attributed_partial_prior_result','full_source_solved':True,'full_source_solved_meaning':'The exact Holland target is verified from prior work and separately met by the submitted theorem; not a new open-problem resolution.','new_open_problem_resolution':False,'new_solution_priority_clearance':False,'identical_algorithm_or_earliest_priority_certified':False,'original_budget':'2/5','original_turn_ledger':pin(R/(PREFIX+'/turns.jsonl')),'new_original_proof_turns':0,'final_ROOT_gate':gate_pin,'bound_current_evidence':gate['bound_current_evidence'],'current_source_identity':identity,'original_scientific_bodies_are_dated_inputs':True,'current_priority_specialization':pin(R/(PREFIX+'/CURRENT_PRIORITY_SPECIALIZATION.md')),'new_paper':False,'Zenodo_upload':False,'new_publication_DOI':None,'tracker_append':False,'AI_tools_used_extensively':True,'human_peer_review':False,'formal_proof_certification':False,'historical_lifecycle_transitions_reconstructed':False}
        (R/(PREFIX+'/acceptance.json')).write_bytes(jb(acceptance))
        event={'at':now,'event':'acceptance_mirror_import','id':ID,'pr':65,'status':'already_solved','turns_used':2,'turn_limit':5,'review_hash':review_hash,'source_record_hash':sha(json.dumps(source['problem'],sort_keys=True).encode()),'source_report_hash':sha(json.dumps(source['upstream_report'],sort_keys=True).encode()),'statement_hash':sha(source['problem']['statement'].encode()),'note':NOTE,'evidence':{'import_is_present_day_mirror':True,'historical_transitions_asserted':False,'reviewed_head':HEAD,'merge_commit':base,'canonical_acceptance':pin(R/(PREFIX+'/acceptance.json')),'final_ROOT_gate':gate_pin,'original_budget_ledger':pin(R/(PREFIX+'/turns.jsonl')),'full_source_solved':True,'new_open_problem_resolution':False,'accepted_as':'attributed_partial_prior_result','new_paper':False,'new_publication_DOI':None,'tracker_append':False}}
        event['event_id']=sha(json.dumps(event,sort_keys=True).encode());state[ID]=event
        (R/STATE).write_bytes(jb(state));(R/HISTORY).write_bytes(hb+json.dumps(event,ensure_ascii=False,sort_keys=True).encode()+b'\n')
        must({k:v for k,v in json.loads((R/STATE).read_bytes()).items() if k!=ID}==json.loads(sb) and (R/HISTORY).read_bytes().startswith(hb) and len((R/HISTORY).read_bytes()[len(hb):].splitlines())==1,'Other native states/history changed')
        must((R/QUEUE).read_bytes()==qbefore,'Mirror changed queue')
        preserve();git('add','--',*sorted(mirror_paths))
        must({p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==mirror_paths,'Mirror staged scope differs')
        preserve();git('commit','-m','Bind PR65 credited prior-result acceptance to exact merge and supplied-source audits')
        commit=git('rev-parse','HEAD').decode().strip()
        must(git('show','-s','--format=%P',commit).decode().strip()==base and {p.decode() for p in git('diff','--name-only','-z',base,commit).split(b'\0') if p}==mirror_paths,'Mirror commit scope differs')
        check_originals(commit);preserve();git('push','origin','main')
        receipt={'phase':'mirror','merge_commit':base,'acceptance_commit':commit,'submitted_head':HEAD,'gate':gate_pin,'event_id':event['event_id'],'other_native_states_and_history_prefix_preserved':True,'one_present_day_acceptance_event':True,'program_completion_not_conferred':True}
        out=O/'NATIVE_ACCEPTANCE_RESULT.json'
    must(git('ls-remote','--heads','origin','main').decode().split()[0]==commit,'Push readback differs')
    must(not git('diff','--cached','--name-only','-z'),'Shared index not empty after phase')
    check_originals(commit);preserve()
    receipt.update(UTC=dt.datetime.now(dt.timezone.utc).isoformat(),actual_controller_pid=os.getpid(),remote_main=commit,foreign_tracked_bodies_modes_and_index_preserved=True,original_18_bodies_modes_blobs_preserved=True,original_budget='2/5',current_source_identity=identity,new_paper=False,new_DOI=None,tracker_append=False)
    must(not out.exists(),'Actual receipt already exists; preserve it')
    with out.open('xb') as f:f.write(jb(receipt))
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
