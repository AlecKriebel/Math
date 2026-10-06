"""Exact original-head PR302 merge with current acceptance; stop on uncertainty.

Prepared code grants nothing. Local standard-library approval checks precede
all project module imports and any native Git, PR, or acceptance write.
"""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import ast,copy,fcntl,gzip,hashlib,json,os,signal,sqlite3,stat,subprocess,sys,time,types
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_descending_audit_20261002';N=Path(__file__).parent;A=N.parent
D=A/'publication_preparation';F=A/'preprint_package_v02';S=P/'SHARED_GIT_WINDOW_STATUS.json'
PLAN=N/'CONTENT_PLAN.json';CLEAR=N/'ROOT_NATIVE_INTEGRATION_CLEARANCE.json'
HEAD='eb6e0e999521d84a65f9857d338cad76b84d30db';PREFIX='unsolved_math_prioritization/attempts/30003508';QUEUE='unsolved_math_prioritization/QUEUE.md'
STATE='unsolved_math_prioritization/state.json';HISTORY='unsolved_math_prioritization/history.jsonl';ENDPOINT='https://github.com/AlecKriebel/Math.git'
utc=lambda:datetime.now(timezone.utc).isoformat();sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(Path(p).read_bytes())
def require(v,m):
    if not v:raise RuntimeError(m+'; preserve actual partial state and reconcile read-only; never replay a mutation automatically')
def pin(p):
    p=Path(p);require(p.is_file() and not p.is_symlink(),'literal input '+str(p));b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def names(b):return {x.decode() for x in b.split(b'\0') if x}
def row(b):
    found=[x for x in b.splitlines(keepends=True) if b'| 30003508 /' in x];require(len(found)==1 and len(found[0].split(b'|'))==14,'unique target QUEUE row');return found[0]
def mandatory_inputs():
    return [Path(__file__),A/'snapshot_manifest.json',A/'ROOT_ACTUAL_PUBLICATION_AND_TRACKER_ACCEPTANCE.json',A/'ROOT_MATHEMATICAL_GATE_ACCEPTANCE.json',A/'ROOT_BOUNDED_PRIORITY_GATE_ACCEPTANCE.json',A/'ROOT_FINAL_PREPRINT_PUBLICATION_CLEARANCE.json',A/'ROOT_FINAL_PUBLICATION_OPERATIONS_CLEARANCE.json',F/'SECOND_CANDIDATE_MANIFEST.json',F/'record_metadata.json',F/'spectral_tensor_consistency.pdf',F/'spectral_tensor_verification.zip',D/'REVISED_OPERATOR_MANIFEST.json',*[D/n for n in ['publication_guard.py','run_zenodo_step.py','verify_public_record.py','append_tracker.py']],N/'SOURCE_IDENTITY_PREPARATION_READBACK.json',N/'KNOWN_HELD_BASELINE.json',*[N/'payloads'/n for n in ['acceptance.json','CURRENT_RESULT.md','CURRENT_PRIORITY.md','QUEUE_AFTER.md','PR_BODY.md']],P/'audits/pr305_5100034/root_during_peer_pause_20261005/native_integration_preparation/integrate_pr305.py']
def sourcepair():
    identity=load(N/'SOURCE_IDENTITY_PREPARATION_READBACK.json');source=identity['current_selected_flat_record'];manifest=load(R/'unsolved_math_prioritization/manifest.json')
    require(type(source)==dict and type(source['id']) is int and source['id']==30003508 and source['problem_number']=='OWR-15432-001' and 'problem' not in source and 'proposed_by' in source and source['proposed_by'] is None,'flat typed source')
    require(manifest['revision']==identity['dataset_revision']=='37e53eabe540fb458758e198be61634bd02ee008','source revision')
    data={}
    for name in ['problems.json','research_results.json']:
        b=(R/'unsolved_math_prioritization/cache'/name).read_bytes();e=manifest['files'][name];require(len(b)==e['bytes'] and sha(b)==e['sha256'],'whole raw source cache');data[name]=json.loads(b)
    require([x for x in data['problems.json'] if str(x['id'])=='30003508']==[source] and 'OWR-15432-001' not in data['research_results.json'],'raw selected source/prior key')
    db=R/'unsolved_math_prioritization/cache/catalog.sqlite';require(all(not Path(str(db)+n).exists() for n in ['-wal','-shm','-journal']),'SQL sidecar')
    with sqlite3.connect('file:'+str(db)+'?mode=ro&immutable=1',uri=True) as connection:
        revisions=connection.execute('SELECT revision FROM metadata').fetchall();require(revisions==[(manifest['revision'],)],'exact SQLite metadata revision')
        pairs=connection.execute('SELECT payload,report FROM records WHERE key=?',('30003508',)).fetchall()
    require(len(pairs)==1 and all(x is not None for x in pairs[0]),'typed SQL pair distinct from NULL')
    problem,report=map(json.loads,pairs[0]);require(problem==source and type(report)==dict and report=={},'exact SQL source/report object')
    review=sha(json.dumps([source,{}],sort_keys=True).encode());statement=sha(source['statement'].encode())
    require(review==identity['review_hash']=='b6b5099c060375a6bcea8613927d04f5394016b6ca8d0006603a93a83d164917' and statement==identity['statement_hash']=='18d766257ee3bf1b9871d1d026a360d3266887e8bb0c12550dfac37165784e8f','source fingerprints')
    matches=[x for x in load(R/'unsolved_math_prioritization/catalog.json') if x['id']=='30003508']
    require(len(matches)==1 and matches[0]['review_hash']==review and matches[0]['statement_hash']==statement and matches[0]['present'] is True and matches[0]['eligible'] is True and matches[0]['route']=='proof' and matches[0]['holds']==[],'current catalog eligibility/holds/statement')
    return dict(review_hash=review,statement_hash=statement,dataset_revision=manifest['revision'],SQL_report_literal='{}',historical_source_prior_key_present=False)
def tracker_evidence(acceptance,published,authenticate_execution):
    """Reopen all thirteen actual services and the complete anchored tracker."""
    output=A/'publication_actual';labels={'sheet_metadata','all_rows_before','tracker_dry_run','tracker_append','appended_row_readback','all_rows_after'}
    expected_labels=labels|{'stage','inspect_draft','publish','inspect_published','record','file_spectral_tensor_consistency.pdf','file_spectral_tensor_verification.zip'}
    matches={};seen=set();require(len(acceptance['actual_native_processes'])==13,'thirteen actual immutable ROOT descriptors')
    for expected in acceptance['actual_native_processes']:
        label=Path(expected['stdout']['stored']['path']).parent.name
        require(label in expected_labels and label not in seen,'exact unique service role');seen.add(label)
        capture_dir=output/'private_public_readback' if label=='record' or label.startswith('file_') else None
        out,err,current=authenticate_execution(label,expected['argv'],capture_dir)
        require(current==expected,'every complete actual native/source/approval/argv/PID/time/runtime/stored/logical body equals immutable ROOT descriptor')
        if label in labels:
            matches[label]=json.loads(out)
    require(set(matches)==labels and seen==expected_labels,'all thirteen services and six complete tracker roles')
    complete=load(output/'TRACKER_COMPLETE.json');require(pin(output/'TRACKER_COMPLETE.json')==acceptance['tracker_completion'],'actual tracker receipt body/mode remains ROOT-pinned')
    request=load(output/'TRACKER_ROW_REQUEST.json');require(request['params']==dict(spreadsheetId='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20',range="'Math Puzzles'!A:AQ",valueInputOption='RAW',insertDataOption='INSERT_ROWS',includeValuesInResponse=True),'exact RAW append params')
    row=complete['row'];require(request['body']==dict(majorDimension='ROWS',values=[row]) and len(row)==4 and row[1]=='' and row[2]==published['doi_url'] and '30003508' in row[0] and published['title'] in row[3],'all exact confirmed row cells')
    before=matches['all_rows_before']['values'];after=matches['all_rows_after']['values'];require(len(before)==25 and before[0][:4]==['Original Problem','Solution Chat URL','DOI','Notes'] and after==before+[row],'whole43-column formula prefix plus exact one row')
    require(matches['appended_row_readback']['values']==[row] and sum('30003508' in str(x) for x in after[1:])==sum(published['doi'] in str(x) for x in after[1:])==1,'exact single whole-table DOI/problem row')
    update=matches['tracker_append'];require(update['spreadsheetId']==request['params']['spreadsheetId'] and update['updates']['updatedRange']=="'Math Puzzles'!A26:D26" and (update['updates']['updatedRows'],update['updates']['updatedColumns'],update['updates']['updatedCells'])==(1,4,4),'actual one-row append shape/identity')
    require(complete['status']=='PASS_EXACT_ONE_DOI_ROW_AND_WHOLE_TABLE_READBACK' and complete['single_actual_append_PID']==1555 and complete['all_original_columns_scanned']==43 and complete['all_prior_rows_unchanged'] is True and complete['automatic_retry'] is False,'complete actual tracker interpretation')
    return complete
def main():
    require(not sys.flags.optimize,'optimization forbidden')
    lock=(N/'NATIVE_OPERATION.lock').open('a+b');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    plan=load(PLAN);clear=load(CLEAR);control=load(S);lease=control['descending_302_native_integration_lease']
    require(clear['status']=='PASS_EXACT_PR302_NATIVE_ORIGINAL_HEAD_AND_PRESENT_DAY_ACCEPTANCE' and clear['unresolved_issues']==[] and clear['native_execution_authorized'] is True and pin(CLEAR)['mode']==0o444,'genuine ROOT native clearance')
    require(clear['operator']==pin(__file__) and clear['plan']==pin(PLAN) and pin(__file__)['mode']==pin(PLAN)['mode']==0o444,'exact frozen source/plan')
    bound=plan['bound_inputs'];expected_roles={str(x) for x in mandatory_inputs()}
    require(type(bound) is list and len(bound)==len(expected_roles) and {x['path'] for x in bound}==expected_roles,'all exact nonvacuous input roles')
    for x in bound:require(pin(x['path'])==x,'approved input before every project import')
    review=Path(clear['review_namespace']);require(review.parent==A and review.name.startswith('native_integration_adversary_'),'fresh native review namespace')
    pins=clear['closed_review_pins'];require(set(pins)=={'REPORT.md','DERIVATION.md','READ_SCOPE_LEDGER.md','VERDICT.json','OUTPUT_MANIFEST.json','CLOSURE_SEAL.json'},'all exact closed native review roles')
    for name,x in pins.items():require(pin(review/name)==x and x['mode']==0o444,'closed native review pin')
    require(load(review/'VERDICT.json')['unresolved_issues']==[] and load(review/'VERDICT.json')['execution_authority_granted'] is False,'independent verdict remains nonauthorizing')
    require(not control['shared_git_writes_paused'] and not control['ascending_pr85_publication_integration_window_granted'] and control['ascending_pr85_publication_integration_window_aborted_inactive'] is True,'inactive old peer epoch required')
    require(lease['active'] is True and lease['git_authorized'] is True and lease['plan']==pin(PLAN) and lease['operator']==pin(__file__) and lease['clearance']==pin(CLEAR) and lease['endpoint']==ENDPOINT,'exact current native lease')
    source=pin(__file__);planpin=pin(PLAN);base=current=plan['starting_main'];require(lease['starting_main']==base and plan['original_head']==HEAD and plan['original_author_budget']=='2/5','native epoch and original budget')
    original=load(A/'snapshot_manifest.json');require(original['head']==HEAD and original['original_submitted_status']=='claimed_solved' and original['original_author_turn_count']=='2/5' and len(original['files'])==29,'original intake')
    originals=[x for x in original['files'] if x['path'].startswith(PREFIX+'/')];require(len(originals)==28 and len({x['path'] for x in originals})==28,'original28')
    extras={PREFIX+'/'+n:(N/'payloads'/n).read_bytes() for n in ['acceptance.json','CURRENT_RESULT.md','CURRENT_PRIORITY.md']}
    owned={x['path'] for x in original['files']}|set(extras)|{STATE,HISTORY}
    require(len(owned)==34 and len(plan['allowed_paths'])==34 and set(plan['allowed_paths'])==owned and lease['allowed_paths']==plan['allowed_paths'],'exact34nativepaths')
    # Project modules are definitions-only on import and all four complete
    # current source bodies are approved above, before extending module search.
    sys.path.insert(0,str(D))
    from publication_guard import clearance as publication_clearance,authenticate_execution
    from run_zenodo_step import inspected_publication
    from verify_public_record import verify_public_evidence
    publication_clearance();published=inspected_publication();verify_public_evidence(published)
    acceptance=load(A/'ROOT_ACTUAL_PUBLICATION_AND_TRACKER_ACCEPTANCE.json')
    require(acceptance['status']=='ROOT_ACCEPTS_ACTUAL_PUBLICATION_AND_EXACT_ONE_TRACKER_ROW' and acceptance['DOI']==published['doi']=='10.5281/zenodo.23157237' and acceptance['full_actual_captures_authenticated']==13 and acceptance['tracker_range']=="'Math Puzzles'!A26:D26",'whole actual publication/tracker acceptance')
    tracker=tracker_evidence(acceptance,published,authenticate_execution)
    actual=N/'actual_native_integration';require(not actual.exists(),'previous or uncertain native attempt');actual.mkdir()
    full_inputs=[Path(__file__),PLAN,CLEAR,S,*[Path(x['path']) for x in bound],*[A/'snapshot'/x['path'] for x in originals]]
    archived=[]
    for i,path in enumerate(dict.fromkeys(full_inputs)):
        b=path.read_bytes();q=actual/(str(i)+'_'+path.name+'.source.gz');q.write_bytes(gzip.compress(b,mtime=0));require(gzip.decompress(q.read_bytes())==b,'whole prelaunch input');archived.append(dict(input=pin(path),archive=pin(q)))
    (actual/'ATTEMPT.json').write_text(json.dumps(dict(UTC=utc(),actual_ROOT_recorder_PID=os.getpid(),source=source,plan=planpin,lease_token=lease['token'],outcome='STARTED_UNCERTAIN_UNTIL_FINAL_RECEIPT',automatic_retry=False,full_prelaunch_inputs=archived),indent=2)+'\n')
    framework=mandatory_inputs()[-1];body=framework.read_bytes();require(sha(body)=='0ea02436c0ac1e0070169df466c34ba141c43291e16515b3fd1cce2135071897','exact independently reviewed bounded native recorder')
    tree=ast.parse(body);fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='main');node=next(x for x in fn.body if isinstance(x,ast.FunctionDef) and x.name=='run')
    factory=ast.parse('def factory(actual):\n count=0\n return run\n').body[0];factory.body.insert(1,copy.deepcopy(node));module=ast.fix_missing_locations(ast.Module(body=[factory],type_ignores=[]))
    env=dict(Path=Path,datetime=datetime,timezone=timezone,timedelta=timedelta,hashlib=hashlib,json=json,stat=stat,os=os,sys=sys,subprocess=subprocess,gzip=gzip,signal=signal,R=R,g=types.SimpleNamespace(pin=pin),sha=sha,utc=utc,require=require,__file__=str(Path(__file__).resolve()))
    exec(compile(module,str(framework)+'::unchanged_recording_function','exec'),env);run=env['factory'](actual)
    def git(*args,ok=(0,)):return run(['/usr/bin/git','--no-optional-locks',*args],ok)
    def pr():return json.loads(run(['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/302']))
    require(not git('config','--get-regexp',r'^url\..*\.(insteadOf|pushInsteadOf)$',ok=(0,1)),'Git URL rewrite outside scope')
    require(git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==base and git('ls-remote',ENDPOINT,'refs/heads/main').split()[0].decode()==base,'current main/remote')
    require(not git('diff','--cached','--raw','-z') and not (R/'.git/MERGE_HEAD').exists() and not (R/'.git/index.lock').exists(),'initial staged/merge state busy')
    info=pr();require(info['state']=='open' and info['draft'] is True and info['head']['sha']==HEAD and info['base']['ref']=='main','original open draft identity')
    files=json.loads(run(['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/302/files?per_page=100']));require(len(files)==29 and {(x['filename'],x['sha']) for x in files}=={(x['path'],x['git_blob_sha']) for x in original['files']},'exact incoming API29file domain')
    require(not (R/PREFIX).exists(),'attempt destination already exists')
    for x in originals:
        b=(A/'snapshot'/x['path']).read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'] and blob(b)==x['git_blob_sha'],'all full frozen original blobs')
    before=(R/QUEUE).read_bytes();require(before==git('show',base+':'+QUEUE),'QUEUE is clean');after=(N/'payloads/QUEUE_AFTER.md').read_bytes();br=row(before);ar=row(after);bc=br.split(b'|');ac=ar.split(b'|')
    require(bc[8].strip()==b'queued' and bc[9].strip()==b'0/5' and ac[8].strip()==b'preprint_published' and ac[9].strip()==b'2/5' and [i for i in range(14) if bc[i]!=ac[i]]==[8,9,11,12] and before.replace(br,b'',1)==after.replace(ar,b'',1),'only four target QUEUE cells')
    sb=(R/STATE).read_bytes();hb=(R/HISTORY).read_bytes();require(sb==git('show',base+':'+STATE) and hb==git('show',base+':'+HISTORY),'global state/history clean')
    state=load(R/STATE);require(type(state)==dict and '30003508' not in state and all(str(json.loads(x).get('id'))!='30003508' for x in hb.splitlines() if x),'target absent from all current state/history')
    native_accept=json.loads(extras[PREFIX+'/acceptance.json']);require(native_accept['DOI']==published['doi'] and native_accept['original_head']==HEAD and native_accept['original_author_budget']=='2/5' and native_accept['historical_transitions_asserted'] is False and native_accept['new_central_proof_search_turns']==0,'exact present-day acceptance packet')
    identity=sourcepair();(actual/'ACTUAL_SOURCE_IDENTITY.json').write_text(json.dumps(identity,indent=2)+'\n')
    event=dict(schema='pr302-present-day-acceptance-import/v1',event='acceptance_mirror_import',at=utc(),id='30003508',status='preprint_published',turns_used=2,turn_limit=5,review_hash=identity['review_hash'],readiness_review_hash=identity['review_hash'],statement_hash=identity['statement_hash'],note=ac[11].decode().strip(),evidence=dict(acceptance_path=PREFIX+'/acceptance.json',DOI=published['doi'],original_head=HEAD,original_budget='2/5',new_central_proof_search_turns=0,historical_transitions_asserted=False))
    tail=len(sb.rstrip());require(sb[:tail].endswith(b'}'),'literal state object close');cut=tail-1;insert=(b',' if state else b'')+b'\n'+json.dumps('30003508').encode()+b': '+json.dumps(event,sort_keys=True).encode()
    sa=sb[:cut]+insert+sb[cut:];require(sa[:cut]+sa[cut+len(insert):]==sb and {k:v for k,v in json.loads(sa).items() if k!='30003508'}==state,'state foreign literal bytes and values')
    require(not hb or hb.endswith(b'\n'),'history prefix must end with newline');ha=hb+json.dumps(event,sort_keys=True).encode()+b'\n';require(ha.startswith(hb) and ha[len(hb):].count(b'\n')==1,'exact one new history event')
    expected={x['path']:(A/'snapshot'/x['path']).read_bytes() for x in originals};expected.update(extras);expected.update({QUEUE:after,STATE:sa,HISTORY:ha});require(set(expected)==owned,'whole expected native domain')
    index=git('ls-files','--stage','-z');flags=git('ls-files','-v','-z');dirty=names(git('diff','--name-only','-z','HEAD'));require(not dirty&owned,'native owned dirty paths')
    foreign={p:pin(R/p) for p in dirty};diff=git('diff','--binary','HEAD','--',*sorted(dirty)) if dirty else b''
    held_rows=load(N/'KNOWN_HELD_BASELINE.json')['files'];require(len(held_rows)==len({x['path'] for x in held_rows})==41253,'all known-held baseline rows')
    held=[x for x in held_rows if str(Path(x['path']).relative_to(R)) not in owned and x['path']!=str(S)]
    def held_stable():
        for x in held:require(pin(x['path'])==x,'known-held complete nonowned body/mode')
    held_stable()
    def exclude(b,stage):return [x for x in b.split(b'\0') if x and (x.split(b'\t',1)[1].decode() if stage else x[2:].decode()) not in owned]
    def stable():
        require(git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==current,'local native epoch drift')
        require(names(git('diff','--name-only','-z','HEAD'))-owned==dirty and {p:pin(R/p) for p in dirty}==foreign and (git('diff','--binary','HEAD','--',*sorted(dirty)) if dirty else b'')==diff,'all foreign dirty bodies/modes/diff')
        require(exclude(git('ls-files','--stage','-z'),True)==exclude(index,True) and exclude(git('ls-files','-v','-z'),False)==exclude(flags,False),'entire foreign logical index/flags')
    def authorize():
        require(pin(__file__)==source and pin(PLAN)==planpin and pin(CLEAR)==lease['clearance'],'approved source/plan/clearance drift')
        for x in bound:require(pin(x['path'])==x,'every approved input before write')
        require(load(CLEAR)==clear and load(S)==control and control['descending_302_native_integration_lease']==lease and not control['shared_git_writes_paused'],'exact live source/control/lease')
        stable();publication_clearance();require(sourcepair()==identity,'fresh source identity drift')
        require(inspected_publication()==published and verify_public_evidence(published) and tracker_evidence(acceptance,published,authenticate_execution)==tracker,'complete inspected/public/tracker actual evidence before every native write')
        require(datetime.now(timezone.utc)+timedelta(seconds=75)<=datetime.fromisoformat(lease['expires_UTC']),'native deadline insufficient for command/cleanup/capture')
        require(load(S)==control and load(CLEAR)==clear,'final live control/clearance drift')
    env['authorize']=authorize
    authorize();git('fetch','--no-tags','--no-write-fetch-head',ENDPOINT,'refs/pull/302/head');require(pr()['head']['sha']==HEAD,'head changed during fetch')
    common=git('merge-base',base,HEAD).decode().strip();require(names(git('diff','--name-only','-z',common,HEAD))=={x['path'] for x in original['files']},'local exact original incoming29domain')
    for x in original['files']:
        b=git('show',HEAD+':'+x['path']);require(len(b)==x['bytes'] and sha(b)==x['sha256'] and blob(b)==x['git_blob_sha'] and git('ls-tree',HEAD,'--',x['path']).decode().split()[:3]==['100644','blob',x['git_blob_sha']],'entire original Git source body/mode/blob')
    bodyfile=N/'payloads/PR_BODY.md';pr_body=bodyfile.read_text();require('{{' not in pr_body and published['doi_url'] in pr_body and HEAD in pr_body,'exact final PR annotation')
    authorize();run(['/opt/homebrew/bin/gh','pr','edit','302','--repo','AlecKriebel/Math','--title','Prove smooth fixed-lag spectral diffusion tensor consistency','--body-file',str(bodyfile)])
    info=pr();require(info['body']==pr_body and info['head']['sha']==HEAD,'actual PR annotation readback')
    authorize();git('merge','--no-ff','--no-commit',HEAD,ok=(0,1));require(names(git('diff','--name-only','--diff-filter=U','-z'))<={QUEUE} and (R/'.git/MERGE_HEAD').read_text().strip()==HEAD,'unexpected merge conflict/state')
    for rel,b in expected.items():
        if rel in {x['path'] for x in originals}:continue
        path=R/rel
        if rel in extras:require(not path.exists() and not path.is_symlink(),'new acceptance destination exists')
        authorize();path.parent.mkdir(parents=True,exist_ok=True)
        authorize();path.write_bytes(b);path.chmod(0o644)
    authorize();git('add','--',*sorted(owned));require(names(git('diff','--cached','--name-only','-z'))==owned and not git('diff','--name-only','--diff-filter=U','-z'),'exact staged34domain')
    for rel,b in expected.items():require(git('show',':'+rel)==b and git('ls-files','--stage','--',rel).decode().split()[:3]==['100644',blob(b),'0'],'full staged bodies/modes/blobs')
    held_stable();authorize();git('commit','-m','Accept PR302 published smooth spectral diffusion tensor consistency');current=git('rev-parse','HEAD').decode().strip()
    require(git('show','-s','--format=%P',current).decode().split()==[base,HEAD] and names(git('diff','--name-only','-z',base,current))==owned,'actual exact original-head merge parents/domain')
    for rel,b in expected.items():require(git('show',current+':'+rel)==b and git('ls-tree',current,'--',rel).decode().split()[:3]==['100644','blob',blob(b)] and (R/rel).read_bytes()==b and stat.S_IMODE((R/rel).stat().st_mode)==0o644,'committed/native whole bodies/modes/blobs')
    held_stable();authorize();git('merge-base','--is-ancestor',base,current);require(git('ls-remote',ENDPOINT,'refs/heads/main').split()[0].decode()==base,'remote moved before explicit expected-old descendant push')
    git('push','--force-with-lease=refs/heads/main:'+base,ENDPOINT,current+':refs/heads/main');require(git('ls-remote',ENDPOINT,'refs/heads/main').split()[0].decode()==current,'actual remote merge readback')
    info=pr()
    for observation in range(6):
        if info['merged'] is True and info['merged_at'] and info['head']['sha']==HEAD and info['merge_commit_sha']==current:break
        require(info['head']['sha']==HEAD,'original PR head changed during read-only merge confirmation')
        time.sleep(2);info=pr()
    require(info['merged'] is True and info['merged_at'] and info['head']['sha']==HEAD and info['merge_commit_sha']==current,'GitHub exact merge not confirmed after bounded read-only observations; STOP with honest original exit and later read-only reconciliation')
    stable();held_stable()
    for rel,b in expected.items():
        require((R/rel).read_bytes()==b and pin(R/rel)['mode']==0o644 and git('show',':'+rel)==b and git('ls-files','--stage','--',rel).decode().split()[:3]==['100644',blob(b),'0'] and git('show',current+':'+rel)==b and git('ls-tree',current,'--',rel).decode().split()[:3]==['100644','blob',blob(b)],'final postpush all34 owned live/index/commit complete bytes/modes/blobs')
    require(not git('diff','--cached','--raw','-z') and load(S)==control,'final native index/control')
    receipt=dict(status='PASS_PR302_EXACT_ORIGINAL_HEAD_NATIVE_MERGE_AND_PRESENT_DAY_ACCEPTANCE',UTC=utc(),actual_ROOT_recorder_PID=os.getpid(),original_PR=302,original_head=HEAD,original_author_budget='2/5',original28_bodies_modes_blobs_preserved=True,actual_merge=current,parents=[base,HEAD],owned_paths=sorted(owned),queue_only_target_cells=[8,9,11,12],all_foreign_QUEUE_state_history_literal_bytes_preserved=True,present_day_target_import_only=True,new_central_proof_search_turns=0,historical_transitions_asserted=False,full_foreign_index_flags_dirty_bodies_modes_diff_preserved=True,DOI=published['doi'],tracker_range="'Math Puzzles'!A26:D26",merged_at=info['merged_at'],main_equals_explicit_remote=True,automatic_retry=False,global_descending_completion_checkpoint_pending=True,estimates_percent=dict(mathematics=100,bounded_priority=100,preprint_and_publication=100,native_integration=100,PR302_workflow=95))
    q=N/'ROOT_ACTUAL_NATIVE_MERGE_VERIFICATION.json'
    with q.open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
    q.chmod(0o444);print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
