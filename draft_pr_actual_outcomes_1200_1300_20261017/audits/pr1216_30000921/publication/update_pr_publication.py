#!/usr/bin/env python3
"""Update only the audited problem paths on the pinned PR, using Git objects."""
from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,zipfile
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
BASE='unsolved_math_prioritization/attempts/30000921'
BRANCH='math/30000921-hypercyclic-full-negative'
ORIGINAL='3ee95e0e22a7bb21d7d08e3c4dcd40f60dfd47c3'
NUMBER='1216'
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
def publication_note(pub,tracker):
    note=(
      '# Accepted attributed historical negative answer and published preprint\n\n'
      'There is a dense family of entire functions f hypercyclic for differentiation such that every nonconstant complex polynomial p has |(pf)^(n)(0)| tending to infinity. The same f works for all p, with polynomial-dependent thresholds. Universal polynomial multipliers preserving all HC(D) are exactly nonzero constants. This decisively gives a negative answer to Costakis’s historical2008 Question5 about pointwise p(z)f(z).\n\n'
      'The original fixed-p null-orbit proof required no mathematical repair. A distinct original-question-only reconstruction and a fresh direct-block adversary supplied and verified the stronger simultaneous result. Current mathematical documents separate new additions/executions from immutable original submission and historical audit records. The finer every-input fixed-p null-orbit-coset construction is retained without novelty clearance.\n\n'
      'Positive prior overlap was found: Nikula arXiv1209.6209v1 Theorem1 implies an even stronger frequently hypercyclic simultaneous counterexample family by elementary Gaussian estimates; exact annular existence also follows after null-orbit clipping. Bayart–Matheron arXiv1112.1289v1 Proposition3.3 supplies an earlier general Gaussian-law route. These are credited as prior implications; the exact multiplier corollary was not shown explicitly printed there. No new first solution, first existence, new mechanism, earliest-priority or still-open2026 claim is made. This is an attributed historical-answer and elementary alternative-proof note.\n\n'
      'The coordinate0 collapsed-annulus boundary is handled by Gaussian angular support. Nikula’s served v1 later internal2018 date has unauthenticated cause and is distinguished from official repository2012 and journal2013/2014 dates. Exact diagnostics distinguish three executed algorithm mutations from five fixed-fixture fault-model predicates.\n\n'
      'AI tools were used extensively in research, proof development, source review, computation, internal independent/adversarial verification and writing. Unrefereed; no external human peer review, journal acceptance or formal proof-assistant certification. Sequential different fresh whole-package review/fix rounds are bound to exact publication artifacts.\n\n'
      'Published preprint: ['+pub['doi']+']('+pub['doi_url']+'). Zenodo: '+pub['record_url']+'. Version1.0,17October2026. Four-page PDF and portable TeX-source/verification/priority archive; exact metadata and public artifact checksums verified.\n\n'
      'Google tracker appended once through Google Workspace CLI and read back exactly at '+tracker['updatedRange']+'.\n\n'
      'Evidence: https://github.com/AlecKriebel/Math/tree/main/draft_pr_actual_outcomes_1200_1300_20261017/audits/pr1216_30000921 .\n')
    return note

def desired_files(build,pub,tracker,snapshot):
    files={}
    with zipfile.ZipFile(ROOT/build['verification_zip']['path']) as archive:
        if archive.read('provenance/SUBMITTED_SNAPSHOT.json')!=(ROOT.parent/'SUBMITTED_SNAPSHOT.json').read_bytes():raise RuntimeError('Submitted snapshot differs from reviewed archive')
        allowed={BASE+'/'+n for n in ['ACCEPTANCE.json','ACCEPTANCE.md','AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCES.json','VERIFICATION.json']}
        if len(snapshot['files'])!=8 or {f['path'] for f in snapshot['files']}!=allowed or snapshot['pr']!=int(NUMBER) or snapshot['head']!=ORIGINAL:raise RuntimeError('Unexpected submitted snapshot scope')
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
    if len(files)!=13 or set(files)!=expected:raise RuntimeError('Unexpected intended publication paths')
    return files,publication,note

def expected_identity(pub,tracker,files):
    return {'pr':int(NUMBER),'base':ORIGINAL,'branch':BRANCH,'paths':sorted(files),'files':{n:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(files.items())},'review_gate_sha256':digest(ROOT/'FINAL_REVIEW_GATE.json'),'metadata_sha256':digest(ROOT/'zenodo-deposit.json'),'doi':pub['doi'],'deposit_id':pub['id'],'tracker_range':tracker['updatedRange'],'tracker_receipt_sha256':digest(ROOT/'tracker/TRACKER_RECEIPT.json'),'public_verification_receipt_sha256':digest(ROOT/'PUBLIC_DOWNLOAD_VERIFICATION.json'),'shared_index_modified':False}

def validate_saved(saved,wanted,files):
    for key,value in wanted.items():
        if saved.get(key)!=value:raise RuntimeError('Saved PR intent/receipt differs from current reviewed package at '+key)
    commit=saved.get('commit','')
    if len(commit)!=40 or any(c not in '0123456789abcdef' for c in commit):raise RuntimeError('Invalid saved commit')
    parents=git('rev-list','--parents','-n','1',commit).decode().split()
    if parents!=[commit,ORIGINAL]:raise RuntimeError('Saved publication commit has unexpected parent')
    changed=git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines()
    if sorted(changed)!=sorted(files):raise RuntimeError('Saved publication commit paths differ')
    for name,data in files.items():
        if git('show',commit+':'+name)!=data:raise RuntimeError('Saved commit bytes differ from reviewed package at '+name)
    return commit

def main():
    if git('branch','--show-current').strip()!=b'main':raise RuntimeError('Stay on main')
    build=read('BUILD_RECEIPT.json');gate=read('FINAL_REVIEW_GATE.json');pub=read('PUBLICATION_RECEIPT.json');tracker=read('tracker/TRACKER_RECEIPT.json')
    if gate['status']!='pass' or pub['state']!='published' or not tracker['readback_verified']:raise RuntimeError('Review/publication/tracker gates required')
    if pub.get('metadata_normalizations')!=[]:raise RuntimeError('Exact supplied metadata required')
    metadata=read('zenodo-deposit.json')['metadata']
    if pub['title']!=metadata['title']:raise RuntimeError('Published title differs')
    if tracker['spreadsheetId']!='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' or tracker['gid']!=1254632077:raise RuntimeError('Wrong tracker')
    if len(tracker['row'])!=4 or '30000921' not in tracker['row'][0] or tracker['row'][1]!='' or tracker['row'][2]!=pub['doi_url']:raise RuntimeError('Tracker row does not bind this publication')
    if len(pub['files'])!=2 or {f['name'] for f in pub['files']}!={build[k]['path'] for k in ['pdf','verification_zip']}:raise RuntimeError('Published file inventory differs')
    for key in ['pdf','verification_zip']:
        item=build[key]
        if digest(ROOT/item['path'])!=item['sha256'] or gate[key+'_sha256']!=item['sha256']:raise RuntimeError('Reviewed artifact drift')
        match=next(f for f in pub['files'] if f['name']==item['path'])
        if match['sha256']!=item['sha256'] or match['size']!=item['bytes']:raise RuntimeError('Published artifact drift')
    if gate['metadata_sha256']!=digest(ROOT/'zenodo-deposit.json'):raise RuntimeError('Reviewed metadata drift')
    for name,expected in gate['workflow'].items():
        if digest(ROOT/name)!=expected:raise RuntimeError('Reviewed workflow drift '+name)
    public=read('PUBLIC_DOWNLOAD_VERIFICATION.json')
    if not public.get('public_record_identity_verified') or not public.get('all_supplied_metadata_exact') or public['metadata_manifest_sha256']!=digest(ROOT/'zenodo-deposit.json') or public['doi']!=pub['doi'] or public.get('id')!=pub['id']:raise RuntimeError('Full public metadata verification required')
    expected_public={build[k]['path']:(build[k]['bytes'],build[k]['sha256']) for k in ['pdf','verification_zip']}
    if len(public['files'])!=2 or {f['name']:(f['bytes'],f['sha256']) for f in public['files']}!=expected_public:raise RuntimeError('Public artifact check differs')
    current=pr()
    if current['headRefName']!=BRANCH or current['state']!='OPEN':raise RuntimeError('Unexpected PR branch/state')
    snapshot=json.loads((ROOT.parent/'SUBMITTED_SNAPSHOT.json').read_text())
    files,publication,note=desired_files(build,pub,tracker,snapshot);wanted=expected_identity(pub,tracker,files)
    body=note+'\nThe eight-file MANIFEST.json binds the current mathematical edition. publication_20261017/ adds the reviewed preprint, portable verification archive, matching deposit metadata and publication receipt. Eligibility followed the explicit full original-target solution outcome recorded in this PR because QUEUE.md may be stale.\n'
    permitted_bodies={snapshot['body_sha256'],hashlib.sha256(body.encode()).hexdigest()}
    if hashlib.sha256(current['body'].encode()).hexdigest() not in permitted_bodies:raise RuntimeError('PR body differs from original and intended final body')
    intentpath=ROOT/'PR_BRANCH_INTENT.json';receiptpath=ROOT/'PR_BRANCH_RECEIPT.json'
    if receiptpath.exists():
        old=read(receiptpath.name);commit=validate_saved(old,wanted,files)
        if not intentpath.exists() or validate_saved(read(intentpath.name),wanted,files)!=commit:raise RuntimeError('Receipt/intent disagree')
        remote=git('ls-remote','origin','refs/heads/'+BRANCH).split()[0].decode()
        if current['headRefOid']!=commit or remote!=commit:raise RuntimeError('Recorded PR update no longer current')
        print(json.dumps(old,indent=2));return
    if intentpath.exists():
        intent=read(intentpath.name);commit=validate_saved(intent,wanted,files)
        if current['headRefOid'] not in [ORIGINAL,commit]:raise RuntimeError('Unknown outcome: outside head change')
    else:
        if current['headRefOid']!=ORIGINAL or hashlib.sha256(current['body'].encode()).hexdigest()!=snapshot['body_sha256']:raise RuntimeError('Pinned original PR changed')
        for f in snapshot['files']:
            if git('rev-parse',ORIGINAL+':'+f['path']).decode().strip()!=f['blob']:raise RuntimeError('Original blob mismatch')
        root=ORIGINAL
        for name,data in sorted(files.items()):
            oid=git('hash-object','-w','--stdin',data=data).decode().strip();root=put(root,name.split('/'),oid)
        commit=git('commit-tree',root,'-p',ORIGINAL,data=b'Publish attributed polynomial-multiplier negative answer and verification edition\n').decode().strip()
        git('update-ref','refs/math-audit/1200-1300-20261017/pr1216-publication',commit)
        intent={**wanted,'commit':commit};validate_saved(intent,wanted,files);save(intentpath,intent)
    local=ROOT/'pr_publication_files';local.mkdir(exist_ok=True)
    if any(p.name not in publication for p in local.iterdir()):raise RuntimeError('Unexpected publication child')
    for name,data in publication.items():(local/name).write_bytes(data)
    (ROOT/'PR_BODY_FINAL.md').write_text(body)
    remote=git('ls-remote','origin','refs/heads/'+BRANCH).split()[0].decode()
    if remote==ORIGINAL:
        if pr()['headRefOid']!=ORIGINAL:raise RuntimeError('PR changed before push')
        git('push','origin',commit+':refs/heads/'+BRANCH)
    elif remote!=commit:raise RuntimeError('Remote differs from original and intended update')
    if git('ls-remote','origin','refs/heads/'+BRANCH).split()[0].decode()!=commit:raise RuntimeError('Remote readback differs')
    receipt={**intent,'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'remote_readback_verified':True}
    save(receiptpath,receipt);print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
