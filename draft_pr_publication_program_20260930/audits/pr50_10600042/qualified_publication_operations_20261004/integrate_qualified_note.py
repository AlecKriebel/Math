"""Prospective PR50-only two-phase integration; ROOT must review before execution.

merge imports exact original head and changes only four selected queue cells.
mirror adds a present-day acceptance/state/history mirror after GitHub confirms
the actual merge. Both phases require a freshly confirmed exclusive writer
window, the exact operative package gate, publication and tracker evidence.
Failures preserve partial state for inspection; no reset/stash/abort is used.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import stat
import subprocess
import sys

HEAD='7260315f8b8b193020c09d4ef6df9d943a3a13ff'
ID='10600042'
QUEUE='unsolved_math_prioritization/QUEUE.md'
PREFIX='unsolved_math_prioritization/attempts/'+ID
STATE='unsolved_math_prioritization/state.json'
HISTORY='unsolved_math_prioritization/history.jsonl'
CLAIM='Explicit four classical and eight virtual reversible algebraic scheme families classify ordinary oriented unframed link closures using only even-strand braid states, with arbitrary finite word blocks and the stated syntactic supports.'

def sha(body): return hashlib.sha256(body).hexdigest()
def must(ok,message):
    if not ok: raise RuntimeError(message)
def json_bytes(value): return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase',choices=['merge','mirror'])
    parser.add_argument('--gate',type=Path,required=True)
    parser.add_argument('--exclusive-window-confirmed',action='store_true',required=True)
    args=parser.parse_args()
    must(not sys.flags.optimize and args.exclusive_window_confirmed,'Nonoptimized confirmed-window invocation required')
    own=Path(__file__).resolve().parent; audit=own.parent; repo=own.parents[3]
    phase_dir=own/'private'/('integration-'+args.phase)
    must(not phase_dir.exists(),'A prior attempt exists; inspect it, never blindly repeat')
    phase_dir.mkdir(parents=True)
    (phase_dir/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    commands=[]
    def run(argv,allowed=(0,)):
        started=dt.datetime.now(dt.timezone.utc).isoformat()
        child=subprocess.Popen(argv,cwd=repo,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err=child.communicate(); number=len(commands)+1
        (phase_dir/(str(number)+'.stdout')).write_bytes(out)
        (phase_dir/(str(number)+'.stderr')).write_bytes(err)
        commands.append({'argv':argv,'started_utc':started,'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
                         'actual_pid':child.pid,'exit_code':child.returncode,'stdout_sha256':sha(out),'stderr_sha256':sha(err)})
        (phase_dir/'COMMANDS.json').write_bytes(json_bytes(commands))
        must(child.returncode in allowed,'Command failed; actual streams preserved privately')
        return out,child.returncode
    def git(*parts): return run(['git','--no-optional-locks',*parts])[0]
    def binding(path):
        p=path.resolve(); p.relative_to(repo)
        return {'path':p.relative_to(repo).as_posix(),'sha256':sha(p.read_bytes())}
    def checked_binding(b):
        must(set(b)=={'path','sha256'},'Evidence binding shape differs')
        p=(repo/b['path']).resolve(); p.relative_to(repo)
        must(not p.is_symlink() and p.is_file() and sha(p.read_bytes())==b['sha256'],'Evidence bytes drifted')
        return p
    gate_path=args.gate.resolve(); gate=json.loads(gate_path.read_bytes())
    must(gate['schema']=='pr50-qualified-publication-final-gate/v1' and gate['reviewed_head']==HEAD,'Wrong final gate')
    must(gate['publication_authorized'] is True and gate['user_exception_priority_unresolved'] is True,
         'Explicit qualified-publication authorization missing')
    must(gate['priority_clearance'] is False and gate['historical_priority_certified'] is False and gate['present_openness_certified'] is False,
         'Priority exception must not become certification')
    must(gate['all_current_substantive_findings_resolved'] is True and gate['exact_claim']==CLAIM,'Review/scope gate differs')
    manifest=checked_binding(gate['manifest'])
    must(manifest==audit/'publication_package_v3/zenodo-deposit.json','Wrong operative manifest')
    pins=gate['final_artifacts']
    must(len(pins)==4 and len({b['path'] for b in pins})==4,'Four distinct current artifacts required')
    for b in pins: checked_binding(b)
    manifest_body=json.loads(manifest.read_bytes())
    must(set(manifest_body)=={'metadata','files'} and len(manifest_body['files'])==2,'Current upload domain differs')
    expected_artifacts={manifest.relative_to(repo).as_posix(),
                        (manifest.parent/'even_strand_markov.tex').relative_to(repo).as_posix()}
    for item in manifest_body['files']:
        artifact=(manifest.parent/item['path']).resolve()
        must(artifact.parent==manifest.parent and not artifact.is_symlink(),'Upload path escapes operative folder')
        expected_artifacts.add(artifact.relative_to(repo).as_posix())
    must(gate['manifest'] in pins and {b['path'] for b in pins}==expected_artifacts,
         'Final source/PDF/ZIP/manifest domain not pinned')
    reviews=gate['clean_reviews']
    must(len(reviews)>=2 and len({str(checked_binding(b).parent) for b in reviews})==len(reviews),
         'At least two distinct fresh exact-package review families required')
    publication_path=checked_binding(gate['publication_verification'])
    tracker_path=checked_binding(gate['tracker_verification'])
    pub=json.loads(publication_path.read_bytes()); tracker=json.loads(tracker_path.read_bytes())
    doi=pub['DOI']
    must(pub['published'] is True and pub['all_public_bytes_identical'] is True and pub['manifest']==gate['manifest'],
         'Current publication/public bytes not verified')
    must(pub['historical_priority_certified'] is False and pub['present_openness_certified'] is False,'Publication priority flags differ')
    must(tracker['DOI']==doi and tracker['independent_readback_exact'] is True and tracker['fresh_full_table_exactly_one_matching_problem_DOI_row'] is True,
         'Actual unique tracker readback missing')
    must(tracker['spreadsheet_id']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' and tracker['sheet_id']==1254632077,
         'Tracker destination differs')
    originals=json.loads((audit/'ORIGINAL_MANIFEST.json').read_bytes())['files']
    must(len(originals)==15,'Original scientific domain differs')
    original_paths={x['original_git_path'] for x in originals}
    paths=(original_paths|{QUEUE}) if args.phase=='merge' else {PREFIX+'/acceptance.json',PREFIX+'/CURRENT_RESULT.md',STATE,HISTORY}
    path_bytes={p.encode() for p in paths}
    def committed_originals(commit):
        for item in originals:
            must(sha(git('show',commit+':'+item['original_git_path']))==item['sha256'],'Committed original body differs')
            tree=git('ls-tree',commit,'--',item['original_git_path']).decode().split()
            must(tree[0]==item['git_mode'] and tree[2]==item['git_blob_sha1'],'Committed original mode/blob differs')
    def foreign_index():
        return b'\0'.join(x for x in git('ls-files','--stage','-z').split(b'\0') if x and x.split(b'\t',1)[1] not in path_bytes)
    def file_state(p):
        path=repo/p
        if not path.exists() and not path.is_symlink(): return {'exists':False}
        st=path.lstat(); must(stat.S_ISREG(st.st_mode),'Foreign changed path is not a regular file; inspect')
        return {'exists':True,'mode':st.st_mode,'sha256':sha(path.read_bytes())}
    must(git('branch','--show-current').strip()==b'main','Main required')
    must(not git('diff','--cached','--name-only','-z'),'Real index must be empty; preserve foreign staging')
    must(not (repo/'.git/MERGE_HEAD').exists(),'Existing merge is owned elsewhere')
    base=git('rev-parse','HEAD').decode().strip()
    must(git('ls-remote','--heads','origin','main').decode().split()[0]==base,'Main/remote mismatch')
    valid_pause_bases={base}
    if args.phase=='mirror':
        continuing_merge=json.loads((own/'NATIVE_MERGE_RESULT.json').read_bytes())
        must(continuing_merge['schema']=='pr50-qualified-note-native-merge/v1'
             and continuing_merge['submitted_head']==HEAD and continuing_merge['merge_commit']==base
             and continuing_merge['DOI']==doi and continuing_merge['gate']==binding(gate_path),
             'Continuous writer-window merge identity differs')
        must(git('show','-s','--format=%P',base).decode().strip().split()==[continuing_merge['base'],HEAD],
             'Continuous writer window lacks the exact verified two-parent transition')
        valid_pause_bases.add(continuing_merge['base'])
    window_path=repo/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
    def check_window():
        window=json.loads(window_path.read_bytes())
        must(window['shared_git_writes_paused'] is True and 'PR50' in window['paused_for'],
             'No actual acknowledged PR50 exclusive writer window')
        must(window['local_main_at_pause']==window['remote_main_at_pause']
             and window['local_main_at_pause'] in valid_pause_bases,
             'Acknowledged writer baseline is neither actual phase base nor verified exact merge parent')
        return window
    window=check_window()
    window_binding=binding(window_path)
    (phase_dir/'ACKNOWLEDGED_WINDOW.json').write_bytes(json_bytes(window))
    foreign=foreign_index()
    dirty={p.decode() for p in git('diff','--name-only','-z').split(b'\0') if p and p not in path_bytes}
    foreign_bodies={p:file_state(p) for p in dirty}
    def preserve():
        check_window()
        must(foreign_index()==foreign,'Foreign index changed')
        must(all(file_state(p)==pin for p,pin in foreign_bodies.items()),'Foreign dirty body or mode changed')
        for b in pins+reviews+[gate['publication_verification'],gate['tracker_verification']]: checked_binding(b)
        must(sha(gate_path.read_bytes())==gate_binding['sha256'],'Final gate drifted')
    gate_binding=binding(gate_path)
    pr=json.loads(run(['gh','pr','view','50','--repo','AlecKriebel/Math','--json',
                     'number,state,isDraft,headRefOid,baseRefName,mergeCommit,mergedAt,url'])[0])
    must(pr['headRefOid']==HEAD and pr['baseRefName']=='main','PR identity changed')
    source=json.loads(git('show',HEAD+':'+PREFIX+'/source_record.json'))
    status=json.loads(git('show',HEAD+':'+PREFIX+'/status.json'))
    ledger=git('show',HEAD+':'+PREFIX+'/turns.jsonl')
    must(status['turns_used']==1 and status['turn_limit']==5 and len(ledger.splitlines())==1,'Original 1/5 changed')
    for item in originals:
        must(sha(git('show',HEAD+':'+item['original_git_path']))==item['sha256'],'Original head body differs')
        tree=git('ls-tree',HEAD,'--',item['original_git_path']).decode().split()
        must(tree[0]==item['git_mode'] and tree[2]==item['git_blob_sha1'],'Original head mode/blob differs')
    queue_before=(repo/QUEUE).read_bytes()
    must(queue_before==git('show',base+':'+QUEUE),'Native queue has foreign edits')
    if args.phase=='merge':
        must(pr['state']=='OPEN' and pr['isDraft'] is True,'Open original draft required')
        row=[line for line in git('show',HEAD+':'+QUEUE).decode().splitlines() if '| '+ID+' /' in line]
        must(len(row)==1 and row[0].split('|')[8].strip()=='claimed_solved' and row[0].split('|')[9].strip()=='1/5','Submitted eligibility differs')
        common=git('merge-base',base,HEAD).decode().strip()
        incoming={p.decode() for p in git('diff','--name-only','-z',common,HEAD).split(b'\0') if p}
        must(incoming==paths,'Unexpected submitted scope')
        for p in original_paths: must(not (repo/p).exists(),'An original native file already exists')
        lines=queue_before.decode().splitlines(keepends=True)
        indexes=[i for i,line in enumerate(lines) if '| '+ID+' /' in line]
        must(len(indexes)==1,'Native target row not unique')
        i=indexes[0]; cells=lines[i].split('|')
        must(len(cells)==14 and cells[8].strip()=='queued' and cells[9].strip()=='0/5','Native row baseline differs')
        cells[8]=' preprint_published '; cells[9]=' 1/5 '
        cells[11]=' Verified even-strand classical/virtual ordinary-closure calculus; qualified research note; Nencka priority unresolved (fuller texts inaccessible); AI-assisted, unrefereed; tracker verified '
        cells[12]=' '+doi+' '; lines[i]='|'.join(cells)
        accepted_queue=''.join(lines).encode()
        must(git('rev-parse','HEAD').decode().strip()==base,'Main moved before merge')
        _,merge_exit=run(['git','--no-optional-locks','merge','--no-ff','--no-commit',HEAD],allowed=(0,1))
        conflicts={p.decode() for p in git('diff','--name-only','--diff-filter=U','-z').split(b'\0') if p}
        must(conflicts<={QUEUE} and (repo/'.git/MERGE_HEAD').read_text().strip()==HEAD,'Unexpected conflict/parent; inspect partial merge')
        preserve(); (repo/QUEUE).write_bytes(accepted_queue)
        for item in originals: must(sha((repo/item['original_git_path']).read_bytes())==item['sha256'],'Imported original body differs')
        git('add','--',QUEUE)
        must(not git('diff','--name-only','--diff-filter=U','-z'),'Unresolved conflict remains')
        must({p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==paths,'Merge stage domain differs')
        preserve(); git('commit','-m','Accept PR50 verified research note with unresolved historical priority')
        commit=git('rev-parse','HEAD').decode().strip()
        must(git('show','-s','--format=%P',commit).decode().strip().split()==[base,HEAD],'Two-parent exact-head merge differs')
        must((repo/QUEUE).read_bytes()==accepted_queue,'Accepted queue differs')
        must({p.decode() for p in git('diff','--name-only','-z',base,commit).split(b'\0') if p}==paths,'Committed merge domain differs')
        committed_originals(commit)
        must(not git('diff','--cached','--name-only','-z'),'Real index not empty after merge commit')
        preserve(); git('push','origin','main')
        must(git('ls-remote','--heads','origin','main').decode().split()[0]==commit,'Merge push readback differs')
        preserve()
        receipt={'schema':'pr50-qualified-note-native-merge/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),
                 'actual_pid':os.getpid(),'base':base,'submitted_head':HEAD,'merge_commit':commit,'remote_main':commit,
                 'merge_exit_code':merge_exit,'conflicts':sorted(conflicts),'DOI':doi,'gate':gate_binding,
                 'acknowledged_shared_writer_window':window_binding,
                 'foreign_dirty_bodies_modes_and_index_unchanged':True,'all_15_original_blobs_unchanged':True,
                 'queue_only_target_four_cells_changed':True,'native_mirror_pending':True,'new_central_attempts':0}
        out=own/'NATIVE_MERGE_RESULT.json'
    else:
        merge_path=own/'NATIVE_MERGE_RESULT.json'; merge=json.loads(merge_path.read_bytes())
        must(base==merge['merge_commit'] and merge['gate']==gate_binding and merge['DOI']==doi,'Actual integration receipt differs')
        must(pr['state']=='MERGED' and pr['mergeCommit']['oid']==base,'GitHub has not confirmed exact merge; do not infer')
        with sqlite3.connect('file:'+str(repo/'unsolved_math_prioritization/cache/catalog.sqlite')+'?mode=ro',uri=True) as db:
            row=db.execute('SELECT payload,report FROM records WHERE key=?',(ID,)).fetchone()
        must(row is not None,'Selected current catalog source is missing')
        raw_problem,raw_report=map(json.loads,row)
        must(raw_problem==source['problem'] and raw_report==source['upstream_report'],
             'Selected current source identity differs from original reviewed typed record')
        combined_hash=sha(json.dumps([raw_problem,raw_report],sort_keys=True).encode())
        readiness=json.loads(git('show',HEAD+':'+PREFIX+'/readiness.json'))
        identity_plan=json.loads((audit/'native_acceptance_plan_20261004/PLAN.json').read_bytes())
        # This actual original readiness.json has no review_hash field. The
        # authenticated read-only identity plan supplies the independently
        # reproduced original typed-pair hash; never invent a historical key.
        expected_hash=readiness.get('review_hash',identity_plan['current_selected_identity']['review_hash'])
        must(combined_hash==expected_hash and combined_hash==identity_plan['current_selected_identity']['review_hash'],
             'Current combined source fingerprint differs from authenticated original source binding')
        current_source_identity={'raw_problem_equals_original':True,'raw_report_equals_original':True,
                                 'review_hash':combined_hash,
                                 'original_readiness_review_hash_present':'review_hash' in readiness,
                                 'authenticated_identity_plan':binding(audit/'native_acceptance_plan_20261004/PLAN.json')}
        state_before=(repo/STATE).read_bytes(); history_before=(repo/HISTORY).read_bytes()
        must(state_before==git('show',base+':'+STATE) and history_before==git('show',base+':'+HISTORY),'Foreign native state/history edits')
        state=json.loads(state_before)
        must(ID not in state and all(str(json.loads(x).get('id'))!=ID for x in history_before.splitlines()),'Prior target mirror exists; do not duplicate')
        must(history_before.endswith(b'\n'),'Incomplete history last line')
        must(not (repo/(PREFIX+'/acceptance.json')).exists() and not (repo/(PREFIX+'/CURRENT_RESULT.md')).exists(),'Current native acceptance paths already exist')
        now=dt.datetime.now(dt.timezone.utc).isoformat()
        acceptance={'schema':'pr50-qualified-current-acceptance/v1','at':now,'actual_author_pid':os.getpid(),
                    'problem_id':ID,'problem_code':'AMR-105-0042','pr':50,'reviewed_head':HEAD,
                    'outcome':'verified_research_note_published_priority_unresolved','merge_commit':base,
                    'merged_at':pr['mergedAt'],'doi':doi,'record_url':pub['record_url'],'exact_scope':CLAIM,
                    'final_gate':gate_binding,'final_artifacts':pins,'clean_reviews':reviews,
                    'publication_verification':gate['publication_verification'],'tracker_verification':gate['tracker_verification'],
                    'current_source_identity':current_source_identity,
                    'tracker_row_written':True,'tracker_range':tracker['range'],
                    'original_scientific_files_are_dated_inputs':True,'original_budget':'1/5','new_central_attempts':0,
                    'publication_authorization':'Explicit human exception for PR50 qualified note; inaccessible fuller Nencka texts disclosed.',
                    'historical_priority_certified':False,'present_openness_certified':False,'global_novelty_certified':False,
                    'AI_tools_used_extensively':True,'human_peer_review':False,'formal_proof_certification':False}
        (repo/(PREFIX+'/acceptance.json')).write_bytes(json_bytes(acceptance))
        current=('''# Accepted current result — PR50 / AMR-105-0042

The accepted verified research note is **An even-strand Markov calculus for classical and virtual links**, Alec Kriebel. DOI: https://doi.org/'''+doi+'''.

'''+CLAIM+'''

This is a qualified research note. Nencka's authenticated 1996 announcement is credited. Fuller related 1998/1999 texts and the alternate 1996 report could not be accessed, so historical priority and present openness remain unresolved. Publication follows the human user's explicit exception for PR50; it does not certify novelty or dismiss the inaccessible work.

The operative source, publication files, two fresh review families, exact public-byte readbacks and actual tracker range are bound in acceptance.json. All fifteen original files remain unchanged as historical inputs from head `'''+HEAD+'''`; their dated candidate and review claims do not govern present acceptance. Original substantive attempts remain 1/5, with no additional central proof attempts.

Established Alexander/Markov inputs are imported. Arbitrary finite word blocks are allowed; no minimality, uniform geometric locality, certificate-search algorithm, plat, framed, transverse or welded theorem is claimed. AI tools were used extensively in construction, drafting and verification. This note is unrefereed and has not undergone conventional human peer review or formal proof certification.

Zenodo publication and its public files, the nonduplicate tracker row, and GitHub's exact-head merge are actually verified. State/history contain one present-day acceptance mirror and no reconstructed historical lifecycle transitions.
''')
        (repo/(PREFIX+'/CURRENT_RESULT.md')).write_text(current)
        p=source['problem']; r=source['upstream_report']
        js=lambda v:json.dumps(v,sort_keys=True).encode()
        event={'at':now,'event':'acceptance_mirror_import','id':ID,'pr':50,'status':'preprint_published',
               'turns_used':1,'turn_limit':5,'doi':doi,'review_hash':sha(js([p,r])),
               'source_record_hash':sha(js(p)),'source_report_hash':sha(js(r)),'statement_hash':sha(p['statement'].encode()),
               'note':'Actual current qualified-note acceptance; no historical lifecycle transitions reconstructed; priority unresolved.',
               'evidence':{'authorization':'human_authorized_PR50_priority_exception',
                           'import_is_present_day_mirror':True,'historical_transitions_asserted':False,'reviewed_head':HEAD,
                           'canonical_acceptance':binding(repo/(PREFIX+'/acceptance.json')),
                           'original_budget_ledger':binding(repo/(PREFIX+'/turns.jsonl')),'queue_explicit_budget':'1/5',
                           'publication':gate['publication_verification'],'tracker':gate['tracker_verification'],
                           'final_gate':gate_binding,'merge_commit':base,'historical_priority_certified':False}}
        event['event_id']=sha(js(event)); state[ID]=event
        (repo/STATE).write_bytes(json_bytes(state))
        (repo/HISTORY).write_bytes(history_before+json.dumps(event,ensure_ascii=False,sort_keys=True).encode()+b'\n')
        must({k:v for k,v in json.loads((repo/STATE).read_bytes()).items() if k!=ID}==json.loads(state_before),'Other native states changed')
        must((repo/HISTORY).read_bytes().startswith(history_before) and len((repo/HISTORY).read_bytes()[len(history_before):].splitlines())==1,'History prefix/event count changed')
        must((repo/QUEUE).read_bytes()==queue_before,'Mirror changed queue')
        must(git('rev-parse','HEAD').decode().strip()==base,'Main moved before mirror staging')
        preserve(); git('add','--',*sorted(paths))
        must({p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==paths,'Mirror stage domain differs')
        preserve(); git('commit','-m','Bind PR50 qualified-note acceptance to published DOI and exact merge')
        commit=git('rev-parse','HEAD').decode().strip()
        must(git('show','-s','--format=%P',commit).decode().strip()==base,'Administrative parent differs')
        must({p.decode() for p in git('diff','--name-only','-z',base,commit).split(b'\0') if p}==paths,'Committed mirror domain differs')
        committed_originals(commit)
        must(not git('diff','--cached','--name-only','-z'),'Real index not empty after mirror commit')
        preserve(); git('push','origin','main')
        must(git('ls-remote','--heads','origin','main').decode().split()[0]==commit,'Acceptance push readback differs')
        preserve()
        receipt={'schema':'pr50-qualified-native-mirror/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),
                 'actual_pid':os.getpid(),'merge_commit':base,'acceptance_commit':commit,'remote_main':commit,
                 'event_id':event['event_id'],'DOI':doi,'tracker_range':tracker['range'],
                 'acknowledged_shared_writer_window':window_binding,'current_source_identity':current_source_identity,
                 'other_native_states_and_history_prefix_preserved':True,'foreign_dirty_bodies_modes_and_index_unchanged':True,
                 'exactly_one_current_acceptance_event':True,'original_budget':'1/5','new_central_attempts':0,
                 'historical_priority_certified':False,'program_completion_not_conferred':True}
        out=own/'NATIVE_ACCEPTANCE_RESULT.json'
    committed_originals(commit)
    must(not git('diff','--cached','--name-only','-z'),'Real index not empty after phase')
    must(not out.exists(),'Receipt already exists; preserve it')
    with out.open('x') as stream: json.dump(receipt,stream,indent=2); stream.write('\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__': main()
