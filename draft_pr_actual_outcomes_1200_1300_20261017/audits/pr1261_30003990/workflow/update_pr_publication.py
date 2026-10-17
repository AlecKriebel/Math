#!/usr/bin/env python3
"""Update only the audited problem paths on the pinned PR, using Git objects."""
from pathlib import Path
import datetime,hashlib,json,runpy,shutil,subprocess,zipfile
ROOT=Path(__file__).resolve().parent
REPO=Path('/Users/alec/Documents/Math')
BASE='unsolved_math_prioritization/attempts/30003990'
BRANCH='convex-body-sos-30003990-reviewed'
ORIGINAL='d1ecd7c4368f4909653a44db0c9ca4a5463e6552'
NUMBER='1261'
def git(*args,data=None):
    run=subprocess.run(['git','-c','gc.auto=0',*args],cwd=REPO,input=data,capture_output=True)
    if run.returncode:raise RuntimeError(run.stderr.decode())
    return run.stdout
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def read(n):return json.loads((ROOT/n).read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pr():return json.loads(subprocess.check_output(['gh','pr','view',NUMBER,'--repo','AlecKriebel/Math','--json','headRefOid,headRefName,state,isDraft,body'],cwd=REPO,text=True))
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
      +'Evidence: https://github.com/AlecKriebel/Math/tree/main/draft_pr_actual_outcomes_1200_1300_20261017/audits/pr1261_30003990 .\n')

def desired_files(build,pub,tracker,snapshot):
    files={}
    with zipfile.ZipFile(ROOT/build['verification_zip']['path']) as archive:
        if archive.read('provenance/SUBMITTED_SNAPSHOT.json')!=(ROOT.parent/'SUBMITTED_SNAPSHOT.json').read_bytes():raise RuntimeError('Submitted snapshot differs from reviewed archive')
        names={'ACCEPTANCE.json','AUDIT.md','MOMENT_FORMULATION.md','PROOF.md','PUBLIC_MANIFEST.json','RESULT.md','SOURCE_VERIFICATION.json'}
        allowed={BASE+'/'+n for n in names}
        if len(snapshot['files'])!=7 or {f['path'] for f in snapshot['files']}!=allowed or snapshot['pr']!=int(NUMBER) or snapshot['problem_id']!=30003990 or snapshot['head']!=ORIGINAL or snapshot['branch']!=BRANCH or snapshot['body_sha256']!='729ff3e25a2654fad80086dcb80197e064bb9d6418358d82483c8b7cc28fe77e':raise RuntimeError('Unexpected submitted snapshot scope')
        for f in snapshot['files']:
            name=Path(f['path']).name;data=(ROOT.parent/'current_edition'/name).read_bytes()
            if archive.read('current_edition/'+name)!=data:raise RuntimeError('Current edition differs from reviewed archive')
            files[f['path']]=data
    publication={build[k]['path']:(ROOT/build[k]['path']).read_bytes() for k in ['pdf','verification_zip']}
    publication.update({name:(ROOT/name).read_bytes() for name in ['zenodo-deposit.json','PUBLICATION_RECEIPT.json']})
    note=publication_note(pub,tracker)
    publication['README.md']=note.encode()
    for name,data in publication.items():files[BASE+'/publication_20261017/'+name]=data
    expected={f['path'] for f in snapshot['files']}|{BASE+'/publication_20261017/'+n for n in publication}
    if len(files)!=12 or set(files)!=expected:raise RuntimeError('Unexpected intended twelve publication paths')
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
def validate_workflow_gate(gate):
    if gate.get('schema')!='math-preprint-final-review-gate-v1' or gate.get('pr')!=int(NUMBER) or gate.get('problem_id')!=30003990 or gate.get('original_head')!=ORIGINAL or gate.get('status')!='pass':raise RuntimeError('Invalid final review gate schema/target/status')
    if set(gate.get('workflow',{}))!=REQUIRED_WORKFLOW:raise RuntimeError('Review gate must cover exactly every required workflow script')
    for name in REQUIRED_WORKFLOW:
        if digest(ROOT/name)!=gate['workflow'][name]:raise RuntimeError('Reviewed workflow drift '+name)
    if digest(ROOT/'deposit_coordinator.py')!=gate.get('deposit_coordinator_sha256'):raise RuntimeError('Reviewed deposit coordinator drift')
    for key,raw in [('pdf_sha256','Convex_Body_SOS_Density_Note_v1.0.pdf'),('verification_zip_sha256','Convex_Body_SOS_Density_Verification_v1.0.zip'),('metadata_sha256','zenodo-deposit.json'),('source_sha256','manuscript/main.tex'),('current_context_sha256','../CURRENT_PR1261_CONTEXT.json')]:
        if digest(ROOT/raw)!=gate.get(key):raise RuntimeError('Current reviewed artifact drift '+raw)
    context=current_context()
    if json.loads((ROOT/'zenodo-deposit.json').read_text()).get('metadata')!=context['metadata']:raise RuntimeError('Current supplied metadata differs from explicit context')
    sequence=gate.get('reviews',[])
    if len(sequence)<2 or gate.get('latest_review')!=sequence[-1] or len({r.get('reviewer_id') for r in sequence})!=len(sequence):raise RuntimeError('At least two distinct sequential actual fresh whole-package reviews required')
    latest=gate.get('latest_review',{})
    if latest.get('status')!='CLEAN':raise RuntimeError('Fresh final clean review required')
    allowed=(ROOT.parent/'reviews').resolve()
    previous=''
    required={str((ROOT/name).resolve()) for name in REQUIRED_WORKFLOW}|{str((ROOT/raw).resolve()) for raw in ['deposit_coordinator.py','Convex_Body_SOS_Density_Note_v1.0.pdf','Convex_Body_SOS_Density_Verification_v1.0.zip','zenodo-deposit.json','manuscript/main.tex','COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json','BUILD_RECEIPT.json','../CURRENT_PR1261_CONTEXT.json','../MATH_GATE.json','../PRIORITY_ADJUDICATION.json','../SUBMITTED_SNAPSHOT.json']}
    for record in sequence:
        if record.get('status')!='CLEAN' or record.get('actual_review') is not True:raise RuntimeError('Literal actual CLEAN reviewer evidence required')
        checked={}
        for key in ['report','verdict','input_freeze']:
            path=(ROOT/record.get(key,'')).resolve()
            try:path.relative_to(allowed)
            except ValueError:raise RuntimeError('Review evidence outside this problem review folder')
            if digest(path)!=record.get(key+'_sha256'):raise RuntimeError('Final review evidence drift '+key)
            checked[key]=path
        verdict=json.loads(checked['verdict'].read_text())
        if verdict.get('schema')!='math-pr1261-whole-package-review-v1' or verdict.get('status')!='CLEAN' or verdict.get('actual_review') is not True or verdict.get('reviewer_id')!=record.get('reviewer_id') or verdict.get('pr')!=1261 or verdict.get('problem_id')!=30003990 or verdict.get('original_head')!=ORIGINAL or verdict.get('current_context_sha256')!=gate['current_context_sha256'] or verdict.get('input_freeze_sha256')!=record['input_freeze_sha256']:raise RuntimeError('Current actual whole-package CLEAN verdict required')
        at=verdict.get('at_utc','')
        if not at or at<=previous:raise RuntimeError('Strictly sequential actual review timestamps required')
        previous=at
        freeze=json.loads(checked['input_freeze'].read_text());bound=set()
        for entry in freeze.get('files',[])+freeze.get('external_readonly_inputs',[]):
            path=Path(entry['path']);path=path if path.is_absolute() else ROOT.parent/path
            if path.is_symlink() or not path.is_file() or path.stat().st_size!=entry['bytes'] or digest(path)!=entry['sha256']:raise RuntimeError('Actual reviewer frozen input drift '+str(path))
            bound.add(str(path.resolve()))
        if not required<=bound:raise RuntimeError('Actual reviewer input freeze omits current artifact/workflow')

def synchronize_pr_body(commit,body,original_body_sha256):
    """Idempotent final-body edit; a branch receipt is complete only after readback."""
    before=pr()
    if before['state']!='OPEN' or before['headRefName']!=BRANCH or before['headRefOid']!=commit:raise RuntimeError('PR API head/state not yet the intended commit; reconcile read-only before retry')
    if git('ls-remote','origin','refs/heads/'+BRANCH).split()[0].decode()!=commit:raise RuntimeError('PR branch changed before body update')
    if hashlib.sha256(before['body'].encode()).hexdigest() not in {original_body_sha256,hashlib.sha256(body.encode()).hexdigest()}:raise RuntimeError('PR body changed outside original/intended text')
    if before['body']!=body:
        validate_workflow_gate(read('FINAL_REVIEW_GATE.json'))
        save(ROOT/'PR_BODY_UPDATE_INTENT.json',{'pr':int(NUMBER),'commit':commit,'body_sha256':hashlib.sha256(body.encode()).hexdigest(),'review_gate_sha256':digest(ROOT/'FINAL_REVIEW_GATE.json')})
        run=subprocess.run(['gh','pr','edit',NUMBER,'--repo','AlecKriebel/Math','--body-file',str(ROOT/'PR_BODY_FINAL.md')],cwd=REPO,capture_output=True,text=True,timeout=60)
        if run.returncode:raise RuntimeError('PR body outcome needs read-only reconciliation: '+run.stderr)
    after=pr()
    if after['state']!='OPEN' or after['headRefName']!=BRANCH or after['headRefOid']!=commit or after['body']!=body:raise RuntimeError('Final PR head/body readback differs; no completed receipt saved')
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
    if current['headRefName']!=BRANCH or current['state']!='OPEN':raise RuntimeError('Unexpected PR branch/state')
    snapshot=json.loads((ROOT.parent/'SUBMITTED_SNAPSHOT.json').read_text())
    files,publication,note=desired_files(build,pub,tracker,snapshot)
    body=note+'\nThe seven-file PUBLIC_MANIFEST.json binds the six other current mathematical edition records. publication_20261017/ adds the reviewed preprint, portable verification archive, matching deposit metadata, publication receipt and README. Original historical files are preserved in the portable archive.\n'
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
    if intentpath.exists():
        intent=read(intentpath.name);commit=validate_saved(intent,wanted,files)
        if current['headRefOid'] not in [ORIGINAL,commit]:raise RuntimeError('Unknown outcome: outside head change')
    else:
        if current['headRefOid']!=ORIGINAL or hashlib.sha256(current['body'].encode()).hexdigest()!=snapshot['body_sha256']:raise RuntimeError('Pinned original PR changed')
        for f in snapshot['files']:
            if git('rev-parse',ORIGINAL+':'+f['path']).decode().strip()!=f['blob']:raise RuntimeError('Original blob mismatch')
        validate_workflow_gate(gate)
        root=ORIGINAL
        for name,data in sorted(files.items()):
            oid=git('hash-object','-w','--stdin',data=data).decode().strip();root=put(root,name.split('/'),oid)
        commit=git('commit-tree',root,'-p',ORIGINAL,data=b'Publish reviewed convex-body SOS-density edition and verification package\n').decode().strip()
        git('update-ref','refs/math-audit/1200-1300-20261017/pr1261-publication',commit)
        intent={**wanted,'commit':commit};validate_saved(intent,wanted,files);save(intentpath,intent)
    local=ROOT/'pr_publication_files';local.mkdir(exist_ok=True)
    if any(p.name not in publication for p in local.iterdir()):raise RuntimeError('Unexpected publication child')
    for name,data in publication.items():(local/name).write_bytes(data)
    (ROOT/'PR_BODY_FINAL.md').write_text(body)
    remote=git('ls-remote','origin','refs/heads/'+BRANCH).split()[0].decode()
    if remote==ORIGINAL:
        validate_workflow_gate(gate)
        if digest(ROOT/'FINAL_REVIEW_GATE.json')!=wanted['review_gate_sha256']:raise RuntimeError('Review gate changed before push')
        if pr()['headRefOid']!=ORIGINAL:raise RuntimeError('PR changed before push')
        git('push','origin',commit+':refs/heads/'+BRANCH)
    elif remote!=commit:raise RuntimeError('Remote differs from original and intended update')
    if git('ls-remote','origin','refs/heads/'+BRANCH).split()[0].decode()!=commit:raise RuntimeError('Remote readback differs')
    body_result=synchronize_pr_body(commit,body,snapshot['body_sha256'])
    receipt={**intent,**body_result,'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'remote_readback_verified':True}
    save(receiptpath,receipt);print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
