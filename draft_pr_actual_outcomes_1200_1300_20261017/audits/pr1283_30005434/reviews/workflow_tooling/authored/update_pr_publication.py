#!/usr/bin/env python3
"""Update only the audited problem paths on the pinned PR, using Git objects."""
from pathlib import Path
import datetime,hashlib,json,re,runpy,shutil,subprocess,zipfile
ROOT=Path(__file__).resolve().parent
REPO=Path('/Users/alec/Documents/Math')
SHARED_KIT=REPO/'zenodo_deposit_tool/zenodo.py'
COORDINATOR=ROOT.parents[2]/'publication_coordinators/pr1283.py'
POSTMERGE=ROOT.parents[2]/'publication_coordinators/verify_pr1283_merge.py'
BASE='unsolved_math_prioritization/attempts/30005434'
BRANCH='dot/semibrace-30005434-complete-existence-20261011'
ORIGINAL='4624244af725a80a2b7faf111f6b1ca62aaefe37'
NUMBER='1283'
def git(*args,data=None):
    run=subprocess.run(['git','-c','gc.auto=0',*args],cwd=REPO,input=data,capture_output=True)
    if run.returncode:raise RuntimeError(run.stderr.decode())
    return run.stdout
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def read(n):return json.loads((ROOT/n).read_text())
def exclusive_intent(path,payload):
    if path.is_symlink():raise RuntimeError('Unsafe intent path')
    try:
        with path.open('x') as stream:stream.write(json.dumps(payload,indent=2)+'\n')
    except FileExistsError:raise RuntimeError('Prior/concurrent intent exists; reconcile read-only, never retry blindly')
def digest(p):
    if p.is_symlink() or not p.is_file():raise RuntimeError('Missing/nonregular reviewed file '+str(p))
    return hashlib.sha256(p.read_bytes()).hexdigest()
def pr():
    live=json.loads(subprocess.check_output(['gh','pr','view',NUMBER,'--repo','AlecKriebel/Math','--json','headRefOid,headRefName,baseRefName,state,isDraft,body'],cwd=REPO,text=True))
    if live.get('baseRefName')!='main':raise RuntimeError('PR base must be main')
    return live
def tree(entries):return git('mktree','-z',data=b'\0'.join(entries)+b'\0').decode().strip()
def put(base,parts,oid,kind='blob',mode='100644'):
    entries=[s for s in git('ls-tree','-z',base).split(b'\0') if s] if base else []
    target=parts[0].encode();found=next((s for s in entries if s.split(b'\t',1)[1]==target),None)
    if len(parts)>1:
        child=found.split()[2].decode() if found else None
        oid=put(child,parts[1:],oid,kind,mode);kind='tree';mode='040000'
    entries=[s for s in entries if s.split(b'\t',1)[1]!=target]
    entries.append(f'{mode} {kind} {oid}\t{parts[0]}'.encode());return tree(entries)
def current_context():return runpy.run_path(str(ROOT/'prepare_package.py'))['load_context']()
def publication_note(pub,tracker):
    context=current_context();text=context['publication_text']
    return ('# '+context['title']+'\n\n'+text['summary']+'\n\n'+text['priority_statement']+'\n\n'
      'No firstness or current worldwide openness is claimed. AI tools were used extensively in research, proof development, literature review, internal independent/adversarial verification and writing. Unrefereed; no external human peer review, journal acceptance or formal proof-assistant certification.\n\n'
      +text['verification_scope']+' Omitted third-party source bodies and omitted historical execution bodies are not retroactively authenticated.\n\n'
      +'Published preprint: ['+pub['doi']+']('+pub['doi_url']+'). Zenodo: '+pub['record_url']+'. Version 1.0. Exact supplied metadata and public artifact checksums verified.\n\n'
      +'Google tracker row read back exactly at '+tracker['updatedRange']+'.\n\n'
      +'Evidence: https://github.com/AlecKriebel/Math/tree/main/draft_pr_actual_outcomes_1200_1300_20261017/audits/pr1283_30005434 .\n')

def desired_files(build,pub,tracker,snapshot):
    files={}
    context=current_context()
    if context['edition_mode'] not in {'preserve_submitted','documented_correction'}:raise RuntimeError('Explicit bound current eight-file edition required')
    with zipfile.ZipFile(ROOT/build['verification_zip']['path']) as archive:
        if archive.read('provenance/SUBMITTED_SNAPSHOT.json')!=(ROOT.parent/'SUBMITTED_SNAPSHOT.json').read_bytes():raise RuntimeError('Submitted snapshot differs from reviewed archive')
        names={'ACCEPTANCE.md','AGGREGATE_CHECKS.json','BYTE_PRESERVATION.json','INDEPENDENT_AUDIT.md','MANIFEST.json','PROOF_CLASSIFICATION.md','README.md','SOURCE_METADATA.json'}
        allowed={BASE+'/'+n for n in names}
        if len(snapshot['files'])!=8 or {f['path'] for f in snapshot['files']}!=allowed or snapshot['pr']!=int(NUMBER) or snapshot['problem_id']!=30005434 or snapshot['head']!=ORIGINAL or snapshot['branch']!=BRANCH or snapshot['body_sha256']!='d60b38cf473a47e035624677092725f307da72628f935f80147622a28aef6f93':raise RuntimeError('Unexpected submitted snapshot scope')
        for f in snapshot['files']:
            name=Path(f['path']).name;data=(ROOT.parent/'current_edition'/name).read_bytes()
            if archive.read('current_edition/'+name)!=data:raise RuntimeError('Current edition differs from reviewed archive')
            if archive.read('original_submitted/'+name)!=(ROOT.parent/'submitted'/name).read_bytes():raise RuntimeError('Archived original byte drift '+name)
            if context['source_bindings']['current_edition'][name]!={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}:raise RuntimeError('Current source binding drift '+name)
            files[f['path']]=data
    if build['pdf']['path']!='Semibrace_Existence_Classification_Note_v1.0.pdf' or build['verification_zip']['path']!='Semibrace_Existence_Classification_Verification_v1.0.zip':raise RuntimeError('Unexpected target artifact basenames')
    publication={build[k]['path']:(ROOT/build[k]['path']).read_bytes() for k in ['pdf','verification_zip']}
    publication.update({name:(ROOT/name).read_bytes() for name in ['zenodo-deposit.json','PUBLICATION_RECEIPT.json']})
    note=publication_note(pub,tracker)
    publication['README.md']=note.encode()
    for name,data in publication.items():files[BASE+'/publication_20261017/'+name]=data
    expected={f['path'] for f in snapshot['files']}|{BASE+'/publication_20261017/'+n for n in publication}
    if len(files)!=13 or set(files)!=expected:raise RuntimeError('Unexpected intended thirteen publication paths')
    return files,publication,note

def expected_identity(pub,tracker,files,body):
    return {'pr':int(NUMBER),'base':ORIGINAL,'branch':BRANCH,'paths':sorted(files),'files':{n:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(files.items())},'review_gate_sha256':digest(ROOT/'FINAL_REVIEW_GATE.json'),'metadata_sha256':digest(ROOT/'zenodo-deposit.json'),'doi':pub['doi'],'doi_url':pub['doi_url'],'record_url':pub['record_url'],'deposit_id':pub['id'],'tracker_range':tracker['updatedRange'],'tracker_receipt_sha256':digest(ROOT/'tracker/TRACKER_RECEIPT.json'),'public_verification_receipt_sha256':digest(ROOT/'PUBLIC_DOWNLOAD_VERIFICATION.json'),'body_sha256':hashlib.sha256(body.encode()).hexdigest(),'shared_index_modified':False}

def validate_saved(saved,wanted,files):
    for key,value in wanted.items():
        if saved.get(key)!=value:raise RuntimeError('Saved PR intent/receipt differs from current reviewed package at '+key)
    commit=saved.get('commit','')
    if len(commit)!=40 or any(c not in '0123456789abcdef' for c in commit):raise RuntimeError('Invalid saved commit')
    parents=git('rev-list','--parents','-n','1',commit).decode().split()
    if parents!=[commit,ORIGINAL]:raise RuntimeError('Saved publication commit has unexpected parent')
    changed=git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines()
    if len(changed)!=len(set(changed)) or not set(changed)<=set(files):raise RuntimeError('Saved publication commit paths differ')
    for name,data in files.items():
        if git('show',commit+':'+name)!=data:raise RuntimeError('Saved commit bytes differ from reviewed package at '+name)
    return commit

REQUIRED_WORKFLOW={'prepare_package.py','build_package.py','compile_note.py','verification/verify.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py'}
def utc_time(raw):
    try:value=datetime.datetime.fromisoformat(raw.replace('Z','+00:00'))
    except (ValueError,AttributeError):raise RuntimeError('Actual ISO UTC review timestamp required')
    if value.tzinfo is None or value.utcoffset()!=datetime.timedelta(0):raise RuntimeError('Actual UTC review timestamp required')
    return value

def frozen_input_inventory(path,check_current):
    """Historical inventories remain immutable evidence, not current-byte gates."""
    obj=json.loads(path.read_text());entries=obj.get('files',[])+obj.get('external_readonly_inputs',[]);bound={}
    if not entries:raise RuntimeError('Empty reviewer input inventory')
    for entry in entries:
        if not isinstance(entry,dict) or not isinstance(entry.get('path'),str) or type(entry.get('bytes')) is not int or entry['bytes']<0 or re.fullmatch('[0-9a-f]{64}',entry.get('sha256','')) is None:raise RuntimeError('Malformed historical/current input binding')
        target=Path(entry['path']);target=target if target.is_absolute() else ROOT.parent/target
        if '..' in Path(entry['path']).parts:raise RuntimeError('Unsafe reviewer input path')
        resolved=str(target.resolve())
        if resolved in bound:raise RuntimeError('Duplicate reviewer input binding')
        bound[resolved]=entry
        if check_current and (target.is_symlink() or not target.is_file() or target.stat().st_size!=entry['bytes'] or digest(target)!=entry['sha256']):raise RuntimeError('Latest reviewer frozen input drift '+str(target))
    return bound

def validate_workflow_gate(gate):
    if gate.get('schema')!='math-preprint-final-review-gate-v1' or gate.get('pr')!=int(NUMBER) or gate.get('problem_id')!=30005434 or gate.get('original_head')!=ORIGINAL or gate.get('status')!='pass':raise RuntimeError('Invalid final review gate schema/target/status')
    if set(gate.get('workflow',{}))!=REQUIRED_WORKFLOW:raise RuntimeError('Review gate must cover exactly every required workflow script')
    for name in REQUIRED_WORKFLOW:
        if digest(ROOT/name)!=gate['workflow'][name]:raise RuntimeError('Reviewed workflow drift '+name)
    if digest(COORDINATOR)!=gate.get('deposit_coordinator_sha256'):raise RuntimeError('Reviewed deposit coordinator drift')
    if digest(POSTMERGE)!=gate.get('postmerge_coordinator_sha256'):raise RuntimeError('Reviewed postmerge coordinator drift')
    if digest(SHARED_KIT)!=gate.get('shared_kit_sha256'):raise RuntimeError('Reviewed read-only shared kit drift')
    for key,raw in [('pdf_sha256','Semibrace_Existence_Classification_Note_v1.0.pdf'),('verification_zip_sha256','Semibrace_Existence_Classification_Verification_v1.0.zip'),('metadata_sha256','zenodo-deposit.json'),('source_sha256','manuscript/main.tex'),('current_context_sha256','../CURRENT_PR1283_CONTEXT.json')]:
        if digest(ROOT/raw)!=gate.get(key):raise RuntimeError('Current reviewed artifact drift '+raw)
    context=current_context()
    if json.loads((ROOT/'zenodo-deposit.json').read_text()).get('metadata')!=context['metadata']:raise RuntimeError('Current supplied metadata differs from explicit context')
    sequence=gate.get('reviews',[])
    if len(sequence)<2 or gate.get('latest_review')!=sequence[-1] or len({r.get('reviewer_id') for r in sequence})!=len(sequence):raise RuntimeError('At least two distinct sequential actual fresh whole-package reviews required')
    latest=gate.get('latest_review',{})
    if latest.get('status')!='CLEAN':raise RuntimeError('Fresh final clean review required')
    allowed=(ROOT.parent/'reviews').resolve()
    previous=None
    required={str((ROOT/name).resolve()) for name in REQUIRED_WORKFLOW}|{str((ROOT/raw).resolve()) for raw in ['Semibrace_Existence_Classification_Note_v1.0.pdf','Semibrace_Existence_Classification_Verification_v1.0.zip','zenodo-deposit.json','manuscript/main.tex','COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json','BUILD_RECEIPT.json','../CURRENT_PR1283_CONTEXT.json','../MATH_GATE.json','../PRIORITY_ADJUDICATION.json','../SUBMITTED_SNAPSHOT.json']}|{str(SHARED_KIT.resolve()),str(COORDINATOR.resolve()),str(POSTMERGE.resolve()),str((ROOT.parent/'_local/ready_and_merge.py').resolve())}
    names={'ACCEPTANCE.md','AGGREGATE_CHECKS.json','BYTE_PRESERVATION.json','INDEPENDENT_AUDIT.md','MANIFEST.json','PROOF_CLASSIFICATION.md','README.md','SOURCE_METADATA.json'}
    required|={str((ROOT.parent/folder/name).resolve()) for folder in ['submitted','current_edition'] for name in names}
    required|={str((ROOT.parent/item['path']).resolve()) for item in context['portable_files']}
    required|={str(path.resolve()) for path in (ROOT/'verification').rglob('*') if path.is_file()}
    if context['edition_mode']=='documented_correction':required.add(str((ROOT.parent/'CURRENT_EDITION_CORRECTION.json').resolve()))
    pending_resolutions=[]
    verifier=runpy.run_path(str(ROOT/'verification/verify.py'));verifier['fixture_boundary'](ROOT.parent,gate)
    verifier['authenticate_snapshot'](ROOT.parent/'submitted',json.loads((ROOT.parent/'SUBMITTED_SNAPSHOT.json').read_text()))
    verifier['authenticate_current'](ROOT.parent/'current_edition',context,ROOT.parent/'submitted')
    for name,text in context['edition_text'].items():
        if (ROOT.parent/'current_edition'/name).read_text()!=text:raise RuntimeError('Current explicit prose/edition drift')
    for name,obj in context['structured_records'].items():
        if json.loads((ROOT.parent/'current_edition'/name).read_text())!=obj:raise RuntimeError('Current explicit structured/edition drift')
    for index,record in enumerate(sequence):
        is_latest=index==len(sequence)-1
        if record.get('status') not in {'CLEAN','CHANGES_REQUIRED'} or record.get('actual_review') is not True or record.get('fresh_reviewer') is not True:raise RuntimeError('Literal actual whole-package review evidence required')
        if is_latest and record['status']!='CLEAN':raise RuntimeError('Latest whole-package review must be CLEAN')
        checked={}
        for key in ['report','verdict','manifest','input_freeze']:
            path=(ROOT/record.get(key,'')).resolve()
            try:path.relative_to(allowed)
            except ValueError:raise RuntimeError('Review evidence outside this problem review folder')
            if digest(path)!=record.get(key+'_sha256'):raise RuntimeError('Final review evidence drift '+key)
            checked[key]=path
        if not is_latest:required|={str(path) for path in checked.values()}
        verdict=json.loads(checked['verdict'].read_text());verifier['fixture_boundary'](ROOT.parent,verdict)
        if verdict.get('schema')!='math-pr1283-whole-package-review-v1' or verdict.get('status')!=record['status'] or verdict.get('actual_review') is not True or verdict.get('fresh_reviewer') is not True or verdict.get('reviewer_id')!=record.get('reviewer_id') or verdict.get('pr')!=1283 or verdict.get('problem_id')!=30005434 or verdict.get('original_head')!=ORIGINAL or verdict.get('current_context_sha256')!=record.get('context_sha256') or re.fullmatch('[0-9a-f]{64}',record.get('context_sha256','')) is None or verdict.get('input_freeze_sha256')!=record['input_freeze_sha256']:raise RuntimeError('Actual exact review identity/context/verdict required')
        if is_latest and record['context_sha256']!=gate['current_context_sha256']:raise RuntimeError('Latest review context is not current')
        at=utc_time(verdict.get('at_utc',''))
        if previous is not None and at<=previous:raise RuntimeError('Strictly sequential actual UTC review timestamps required')
        previous=at
        shape=record.get('manifest_schema',{})
        if set(shape)!={'entries_key','path_key','size_key'} or tuple(shape[k] for k in ['entries_key','path_key','size_key']) not in verifier['SCHEMAS'] or shape['entries_key'] in {'members','authored_members','authored_outputs'}:raise RuntimeError('Explicit relative authored reviewer manifest schema required')
        manifest=json.loads(checked['manifest'].read_text());members=manifest.get(shape['entries_key']);listed=set()
        if not isinstance(members,list) or not members:raise RuntimeError('Empty authored reviewer manifest')
        for entry in members:
            name=verifier['safe'](entry.get(shape['path_key']))
            if name in listed:raise RuntimeError('Duplicate authored review member')
            listed.add(name);verifier['check_binding'](verifier['member'](checked['manifest'].parent,name),entry,shape['size_key'])
        for key in ['report','verdict']:
            try:name=checked[key].relative_to(checked['manifest'].parent).as_posix()
            except ValueError:raise RuntimeError('Reviewer manifest/report/verdict family mismatch')
            if name not in listed:raise RuntimeError('Reviewer manifest omits report/verdict')
        bound=frozen_input_inventory(checked['input_freeze'],is_latest)
        context_entry=bound.get(str((ROOT.parent/'CURRENT_PR1283_CONTEXT.json').resolve()))
        if context_entry is None or context_entry['sha256']!=record['context_sha256']:raise RuntimeError('Review inventory/context anchor mismatch')
        if is_latest and not required<=set(bound):raise RuntimeError('Latest input freeze omits actual code/context/gates/package')
        if record['status']=='CHANGES_REQUIRED':
            path=(ROOT/record.get('resolution','')).resolve()
            try:path.relative_to(ROOT.parent.resolve())
            except ValueError:raise RuntimeError('Root resolution outside this audit')
            if digest(path)!=record.get('resolution_sha256'):raise RuntimeError('Root resolution receipt drift')
            required.add(str(path))
            resolution=json.loads(path.read_text())
            if resolution.get('schema')!='math-pr1283-review-resolution-v1' or resolution.get('status')!='RESOLVED' or resolution.get('pr')!=1283 or resolution.get('problem_id')!=30005434 or resolution.get('original_head')!=ORIGINAL or resolution.get('reviewer_id')!=record['reviewer_id'] or resolution.get('review_verdict_sha256')!=record['verdict_sha256'] or resolution.get('review_input_freeze_sha256')!=record['input_freeze_sha256'] or resolution.get('review_context_sha256')!=record['context_sha256'] or resolution.get('resolved_context_sha256')!=gate['current_context_sha256']:raise RuntimeError('Explicit root resolution identity/anchors required')
            items=resolution.get('items')
            if not isinstance(items,list) or not items or any(not isinstance(item,dict) or set(item)!={'finding','resolution','evidence'} or not all(isinstance(text,str) and text.strip() for text in item.values()) for item in items):raise RuntimeError('Explicit root finding/resolution/evidence required')
            resolved_at=utc_time(resolution.get('at_utc',''))
            if resolved_at<=at:raise RuntimeError('Root resolution must follow reviewed findings')
            pending_resolutions.append(resolved_at)
    if any(at>=previous for at in pending_resolutions):raise RuntimeError('Root resolution must precede latest CLEAN review')

def synchronize_pr_body(commit,body,original_body_sha256):
    """Idempotent final-body edit; a branch receipt is complete only after readback."""
    before=pr()
    if before.get('baseRefName')!='main' or before['state']!='OPEN' or before['headRefName']!=BRANCH or before['headRefOid']!=commit:raise RuntimeError('PR API head/state not yet the intended commit; reconcile read-only before retry')
    if git('ls-remote','origin','refs/heads/'+BRANCH).split()[0].decode()!=commit:raise RuntimeError('PR branch changed before body update')
    if hashlib.sha256(before['body'].encode()).hexdigest() not in {original_body_sha256,hashlib.sha256(body.encode()).hexdigest()}:raise RuntimeError('PR body changed outside original/intended text')
    body_intent=ROOT/'PR_BODY_UPDATE_INTENT.json'
    wanted_body={'pr':int(NUMBER),'commit':commit,'body_sha256':hashlib.sha256(body.encode()).hexdigest(),'review_gate_sha256':digest(ROOT/'FINAL_REVIEW_GATE.json')}
    if body_intent.exists():
        if body_intent.is_symlink() or json.loads(body_intent.read_text())!=wanted_body:raise RuntimeError('Saved body intent differs; reconcile read-only')
        if before['body']!=body:raise RuntimeError('Prior body edit intent unconfirmed; reconcile read-only, never retry blindly')
    if before['body']!=body:
        validate_workflow_gate(read('FINAL_REVIEW_GATE.json'))
        exclusive_intent(body_intent,wanted_body)
        run=subprocess.run(['gh','pr','edit',NUMBER,'--repo','AlecKriebel/Math','--body-file',str(ROOT/'PR_BODY_FINAL.md')],cwd=REPO,capture_output=True,text=True,timeout=60)
        if run.returncode:raise RuntimeError('PR body outcome needs read-only reconciliation: '+run.stderr)
    after=pr()
    if after.get('baseRefName')!='main' or after['state']!='OPEN' or after['headRefName']!=BRANCH or after['headRefOid']!=commit or after['body']!=body:raise RuntimeError('Final PR head/body readback differs; no completed receipt saved')
    if git('ls-remote','origin','refs/heads/'+BRANCH).split()[0].decode()!=commit:raise RuntimeError('PR branch changed after body update')
    return {'body_sha256':hashlib.sha256(body.encode()).hexdigest(),'body_readback_verified':True,'operation_stage':'reviewed_branch_and_final_body_verified'}

def main():
    if git('branch','--show-current').strip()!=b'main':raise RuntimeError('Stay on main')
    build=read('BUILD_RECEIPT.json');gate=read('FINAL_REVIEW_GATE.json');pub=read('PUBLICATION_RECEIPT.json');tracker=read('tracker/TRACKER_RECEIPT.json')
    validate_workflow_gate(gate)
    if not tracker['readback_verified']:raise RuntimeError('Tracker gate required')
    metadata=read('zenodo-deposit.json')['metadata']
    shared=runpy.run_path(str(ROOT/'append_tracker.py'))
    identity=shared['validate_publication_identity'](pub,metadata['title'])
    shared['validate_tracker_receipt'](tracker,pub,metadata['title'])
    if len(pub['files'])!=2 or {f['name'] for f in pub['files']}!={build[k]['path'] for k in ['pdf','verification_zip']}:raise RuntimeError('Published file inventory differs')
    for key in ['pdf','verification_zip']:
        item=build[key]
        if digest(ROOT/item['path'])!=item['sha256'] or gate[key+'_sha256']!=item['sha256']:raise RuntimeError('Reviewed artifact drift')
        match=next(f for f in pub['files'] if f['name']==item['path'])
        if match['sha256']!=item['sha256'] or match['size']!=item['bytes']:raise RuntimeError('Published artifact drift')
    if gate['metadata_sha256']!=digest(ROOT/'zenodo-deposit.json'):raise RuntimeError('Reviewed metadata drift')
    public=read('PUBLIC_DOWNLOAD_VERIFICATION.json')
    if not public.get('public_record_identity_verified') or not public.get('all_supplied_metadata_exact') or public['metadata_manifest_sha256']!=digest(ROOT/'zenodo-deposit.json') or public['doi']!=pub['doi'] or public.get('id')!=pub['id'] or public.get('doi_url')!=identity['doi_url'] or public.get('record_url')!=identity['record_url'] or public.get('metadata_fields_verified')!=sorted(metadata):raise RuntimeError('Full public metadata verification required')
    expected_public={build[k]['path']:(build[k]['bytes'],build[k]['sha256']) for k in ['pdf','verification_zip']}
    if len(public['files'])!=2 or {f['name']:(f['bytes'],f['sha256']) for f in public['files']}!=expected_public:raise RuntimeError('Public artifact check differs')
    current=pr()
    if current.get('baseRefName')!='main' or current['headRefName']!=BRANCH or current['state']!='OPEN':raise RuntimeError('Unexpected PR branch/state')
    snapshot=json.loads((ROOT.parent/'SUBMITTED_SNAPSHOT.json').read_text())
    files,publication,note=desired_files(build,pub,tracker,snapshot)
    body=note+'\nThe current eight-file MANIFEST.json binds the seven other current edition records through its explicit files list of file/bytes/sha256. The current source mode and immutable submitted snapshot are separately authenticated; historical acceptance and byte-preservation declarations do not certify current review or missing earlier inputs. publication_20261017/ adds the reviewed preprint, portable verification archive, matching deposit metadata, publication receipt and README. Original historical files are preserved in the portable archive.\n'
    wanted=expected_identity(pub,tracker,files,body)
    permitted_bodies={snapshot['body_sha256'],hashlib.sha256(body.encode()).hexdigest()}
    if hashlib.sha256(current['body'].encode()).hexdigest() not in permitted_bodies:raise RuntimeError('PR body differs from original and intended final body')
    intentpath=ROOT/'PR_BRANCH_INTENT.json';receiptpath=ROOT/'PR_BRANCH_RECEIPT.json'
    if receiptpath.exists():
        old=read(receiptpath.name);commit=validate_saved(old,wanted,files)
        if not intentpath.exists() or validate_saved(read(intentpath.name),wanted,files)!=commit:raise RuntimeError('Receipt/intent disagree')
        remote=git('ls-remote','origin','refs/heads/'+BRANCH).split()[0].decode()
        if current['headRefOid']!=commit or remote!=commit:raise RuntimeError('Recorded PR update no longer current')
        if current['body']!=body or not old.get('body_readback_verified'):raise RuntimeError('Completed PR receipt requires current final-body readback')
        print(json.dumps(old,indent=2));return
    resumed_intent=intentpath.exists()
    if resumed_intent:
        intent=read(intentpath.name);commit=validate_saved(intent,wanted,files)
        if current['headRefOid'] not in [ORIGINAL,commit]:raise RuntimeError('Unknown outcome: outside head change')
    else:
        if current['headRefOid']!=ORIGINAL or hashlib.sha256(current['body'].encode()).hexdigest()!=snapshot['body_sha256']:raise RuntimeError('Pinned original PR changed')
        for f in snapshot['files']:
            if git('rev-parse',ORIGINAL+':'+f['path']).decode().strip()!=f['git_blob_sha1']:raise RuntimeError('Original blob mismatch')
        validate_workflow_gate(gate)
        root=ORIGINAL
        for name,data in sorted(files.items()):
            oid=git('hash-object','-w','--stdin',data=data).decode().strip();root=put(root,name.split('/'),oid)
        commit=git('commit-tree',root,'-p',ORIGINAL,data=b'Publish reviewed semibrace-existence counterexample package and verification package\n').decode().strip()
        git('update-ref','refs/math-audit/1200-1300-20261017/pr1283-publication',commit)
        intent={**wanted,'commit':commit};validate_saved(intent,wanted,files);exclusive_intent(intentpath,intent)
    remote=git('ls-remote','origin','refs/heads/'+BRANCH).split()[0].decode()
    if resumed_intent and remote==ORIGINAL:raise RuntimeError('Prior branch intent not confirmed remotely; reconcile read-only, never repush an uncertain attempt')
    local=ROOT/'pr_publication_files';local.mkdir(exist_ok=True)
    if any(p.name not in publication for p in local.iterdir()):raise RuntimeError('Unexpected publication child')
    for name,data in publication.items():(local/name).write_bytes(data)
    (ROOT/'PR_BODY_FINAL.md').write_text(body)
    remote=git('ls-remote','origin','refs/heads/'+BRANCH).split()[0].decode()
    if remote==ORIGINAL:
        if resumed_intent:raise RuntimeError('Prior branch intent not confirmed remotely; reconcile read-only, never repush an uncertain attempt')
        validate_workflow_gate(gate)
        if digest(ROOT/'FINAL_REVIEW_GATE.json')!=wanted['review_gate_sha256']:raise RuntimeError('Review gate changed before push')
        before_push=pr()
        if before_push.get('baseRefName')!='main' or before_push['headRefOid']!=ORIGINAL:raise RuntimeError('PR base/head changed before push')
        git('push','origin',commit+':refs/heads/'+BRANCH)
    elif remote!=commit:raise RuntimeError('Remote differs from original and intended update')
    if git('ls-remote','origin','refs/heads/'+BRANCH).split()[0].decode()!=commit:raise RuntimeError('Remote readback differs')
    body_result=synchronize_pr_body(commit,body,snapshot['body_sha256'])
    receipt={**intent,**body_result,'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'remote_readback_verified':True}
    save(receiptpath,receipt);print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
