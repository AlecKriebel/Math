#!/usr/bin/env python3
"""Update only the audited problem paths on the pinned PR, using Git objects."""
from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,zipfile
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
BASE='unsolved_math_prioritization/attempts/30000418'
BRANCH='audit/30000418-tree-list-labeling-counterexample'
ORIGINAL='d96c9fca74195a8706fd9481eeb35a4c3c0d384c'
NUMBER='1211'
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
def main():
    if git('branch','--show-current').strip()!=b'main':raise RuntimeError('Stay on main')
    build=read('BUILD_RECEIPT.json');gate=read('FINAL_REVIEW_GATE.json');pub=read('PUBLICATION_RECEIPT.json');tracker=read('tracker/TRACKER_RECEIPT.json')
    if gate['status']!='pass' or pub['state']!='published' or not tracker['readback_verified']:raise RuntimeError('Review/publication/tracker gates required')
    for key in ['pdf','verification_zip']:
        item=build[key]
        if digest(ROOT/item['path'])!=item['sha256'] or gate[key+'_sha256']!=item['sha256']:raise RuntimeError('Reviewed file drift')
        match=next(f for f in pub['files'] if f['name']==item['path'])
        if match['sha256']!=item['sha256'] or match['size']!=item['bytes']:raise RuntimeError('Published artifact drift')
    current=pr();intentpath=ROOT/'PR_BRANCH_INTENT.json';receiptpath=ROOT/'PR_BRANCH_RECEIPT.json'
    if receiptpath.exists():
        old=read(receiptpath.name)
        if current['headRefOid']!=old['commit']:raise RuntimeError('Recorded PR update no longer current')
        print(json.dumps(old,indent=2));return
    if current['headRefName']!=BRANCH or current['state']!='OPEN':raise RuntimeError('Unexpected PR branch/state')
    snapshot=json.loads((ROOT.parent/'SUBMITTED_SNAPSHOT.json').read_text())
    if intentpath.exists():
        intent=read(intentpath.name);commit=intent['commit']
        if current['headRefOid'] not in [ORIGINAL,commit]:raise RuntimeError('Unknown outcome; PR changed outside recorded update')
    else:
        if current['headRefOid']!=ORIGINAL or hashlib.sha256(current['body'].encode()).hexdigest()!=snapshot['body_sha256']:raise RuntimeError('Pinned original PR changed')
        for f in snapshot['files']:
            if git('rev-parse',ORIGINAL+':'+f['path']).decode().strip()!=f['blob']:raise RuntimeError('Original blob mismatch')
        local=ROOT/'pr_publication_files';local.mkdir(exist_ok=True)
        for key in ['pdf','verification_zip']:shutil.copyfile(ROOT/build[key]['path'],local/build[key]['path'])
        for name in ['zenodo-deposit.json','PUBLICATION_RECEIPT.json']:shutil.copyfile(ROOT/name,local/name)
        note=(
          '# Accepted result and published preprint\n\n'
          'The explicit eleven-vertex tree has ordinary initial-segment palette5 (zero-based span4) and arbitrary-list number6. The A/B five-list obstruction disproves the universal tree equality printed as Kohl2006 Conjecture4 and dissertation4.4. Independent outward pendant paths preserve both exact values.\n\n'
          'The supplementary state recurrence now explicitly requires list membership and parent-edge compatibility before its child-SDR test. The core construction is unchanged. Kohl’s full contribution spans414–417, with Conjecture4 on416. All eight proof/audit/metadata files have new, internally consistent current-edition bindings; original submitted bytes remain in the immutable audit snapshot.\n\n'
          'The known Delta+3 tree bound is credited to Voigt through Kohl/Kohl–Schreyer–Tuza–Voigt. Fiala–Škrekovski’s2001 cyclic five-list obstruction is credited as earlier general-graph overlap. Historical priority, present openness, minimality and a new obstruction mechanism are unestablished and unclaimed. Relevant unavailable primary-source bodies remain recorded in the supporting audit.\n\n'
          'Extensive AI tools were used in research, proof development, literature review, computation, internal independent/adversarial verification and writing. Unrefereed; no external human peer review or formal proof-assistant certification. Fresh sequential whole-package review/fix rounds are recorded on the exact publication files.\n\n'
          'Published preprint: ['+pub['doi']+']('+pub['doi_url']+'). Zenodo: '+pub['record_url']+'. Version1.0,17October2026. Three-page PDF and portable source/verification/priority archive, exact metadata and file checksums verified.\n\n'
          'The requested Google tracker was updated once via Google Workspace CLI and read back exactly at '+tracker['updatedRange']+'.\n\n'
          'Review/provenance evidence: https://github.com/AlecKriebel/Math/tree/main/draft_pr_actual_outcomes_1200_1300_20261017/audits/pr1211_30000418 .\n')
        (local/'README.md').write_text(note)
        (ROOT/'PR_BODY_FINAL.md').write_text(note+'\nThe eight-file MANIFEST.json binds the current corrected mathematical edition. publication_20261017/ adds the reviewed preprint, reproducible archive, matching deposit metadata and publication receipt. Eligibility followed the explicit full-solution outcome recorded in this PR, because QUEUE.md may be stale.\n')
        files={};root=ORIGINAL
        with zipfile.ZipFile(ROOT/build['verification_zip']['path']) as archive:
            for f in snapshot['files']:
                name=Path(f['path']).name;p=ROOT.parent/'repairs'/name
                if archive.read('corrected_edition/'+name)!=p.read_bytes():raise RuntimeError('Corrected edition differs from reviewed archive')
                files[f['path']]=p
        for p in local.iterdir():
            if not p.is_file():raise RuntimeError('Unexpected publication child')
            files[BASE+'/publication_20261017/'+p.name]=p
        for name,p in sorted(files.items()):
            oid=git('hash-object','-w','--',str(p)).decode().strip();root=put(root,name.split('/'),oid)
        commit=git('commit-tree',root,'-p',ORIGINAL,data=b'Publish audited tree five-list obstruction and corrected verification edition\n').decode().strip()
        changed=git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines()
        if set(changed)!=set(files) or len(files)!=13:raise RuntimeError('Unexpected PR paths')
        for name,p in files.items():
            if git('show',commit+':'+name)!=p.read_bytes():raise RuntimeError('New tree file mismatch')
        intent={'pr':1211,'base':ORIGINAL,'commit':commit,'branch':BRANCH,'paths':changed,'files':{n:{'bytes':p.stat().st_size,'sha256':digest(p)} for n,p in files.items()},'review_gate_sha256':digest(ROOT/'FINAL_REVIEW_GATE.json'),'shared_index_modified':False,'doi':pub['doi']}
        save(intentpath,intent)
    remote=git('ls-remote','origin','refs/heads/'+BRANCH).split()[0].decode()
    if remote==ORIGINAL:
        if pr()['headRefOid']!=ORIGINAL:raise RuntimeError('PR changed before push')
        git('push','origin',commit+':refs/heads/'+BRANCH)
    elif remote!=commit:raise RuntimeError('Remote ref differs from original and intended update')
    if git('ls-remote','origin','refs/heads/'+BRANCH).split()[0].decode()!=commit:raise RuntimeError('Remote branch readback differs')
    receipt={**intent,'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'remote_readback_verified':True}
    save(receiptpath,receipt);print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
