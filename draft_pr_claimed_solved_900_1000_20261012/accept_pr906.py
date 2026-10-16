"""Bind a clean second whole-package review to the exact current release."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
P = Path(__file__).resolve().parent
A = P/'audits/pr906_30006419'

def require(ok,message):
    if not ok: raise RuntimeError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(args):
    return subprocess.run(args,cwd=ROOT,check=True,capture_output=True,text=True).stdout

def main():
    now = datetime.now(timezone.utc).isoformat()
    pub = A/'publication'
    freeze = json.loads((pub/'PREPUBLICATION_FREEZE.json').read_text())
    require(freeze['candidate_revision']==2,'Unexpected candidate revision')
    for name,record in freeze['files'].items():
        f = pub/name
        require(f.is_file() and not f.is_symlink() and f.stat().st_size==record['bytes'] and
                digest(f)==record['sha256'],'Frozen release drift: '+name)
    r2folder = A/'reviews/full_package_02'
    r2 = json.loads((r2folder/'RESULT.json').read_text())
    require(r2.get('clean_for_publication') is True,'Second review does not clear publication')
    require(r2.get('required_repairs')==[],'Required repair remains')
    require(r2.get('optional_improvements')==[],'Optional improvement remains unresolved')
    # This review schema places exact anchors in separately sealed receipts.
    start = json.loads((r2folder/'START_RECEIPT.json').read_text())
    end = json.loads((r2folder/'CANDIDATE_END_RECEIPT.json').read_text())
    replay = json.loads((r2folder/'REPLAY_NORMAL.json').read_text())
    require(start['freeze_sha256']==digest(pub/'PREPUBLICATION_FREEZE.json') and
            end['freeze_sha256']==start['freeze_sha256'] and end['freeze_unchanged'] is True,
            'Second review bound to a different freeze')
    require(start['freeze']==freeze and replay['status']=='PASS' and
            replay['package_manifest_sha256']==freeze['package_manifest_sha256'],
            'Second review bound to a different package')
    require(r2['reviewed_pr_head']==freeze['reviewed_head'] and
            r2['candidate_revision']==2 and r2['verdict']=='PASS', 'Wrong reviewed source scope')
    manifests = {}
    for round in [1,2]:
        folder = A/'reviews'/('full_package_0'+str(round))
        manifest = json.loads((folder/'MANIFEST.json').read_text())
        records = manifest['intentional_public_files']
        for name,record in records.items():
            f = folder/name
            require(f.is_file() and not f.is_symlink() and f.stat().st_size==record['bytes'] and
                    digest(f)==record['sha256'],'Review artifact drift: '+str(f))
        manifests[round] = digest(folder/'MANIFEST.json')
    r1 = json.loads((A/'reviews/full_package_01/RESULT.json').read_text())
    require({r['id'] for r in r1['required_repairs']}=={'R1','R2'},'Unknown first-review repair')
    require((A/'PUBLICATION_REVIEW_CORRECTIONS.md').is_file(),'Release correction absent')
    snapshot = json.loads((A/'ORIGINAL_SNAPSHOT.json').read_text())
    for name,pin in snapshot['files'].items():
        require(digest(A/'original'/name)==pin,'Original snapshot drift')
    pr = json.loads(run(['gh','pr','view','906','--repo','AlecKriebel/Math',
                        '--json','state,isDraft,headRefOid,headRefName,url']))
    require(pr['state']=='OPEN' and pr['isDraft'] and
            pr['headRefOid']==freeze['reviewed_head'],'Live PR drift')
    queue = run(['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+
                 pr['headRefOid'],'-H','Accept: application/vnd.github.raw+json'])
    rows = [r for r in queue.splitlines() if '| 30006419 /' in r]
    require(len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved' and
            rows[0].split('|')[9].strip()=='2/5','Live exact-status gate changed')
    parent = run(['git','ls-remote','origin','refs/heads/main']).split()[0]
    run(['git','fetch','--no-write-fetch-head','origin',parent])
    catalogue = json.loads(run(['git','show',parent+':unsolved_math_prioritization/catalog.json']))
    target = next(r for r in catalogue if str(r['id'])=='30006419')
    require(target.get('present') is True and target.get('holds')==[],
            'Current main target absent or has unresolved review holds')
    source = json.loads((A/'TARGET_IDENTITY_PREFLIGHT.json').read_text())
    require(target['statement_hash']==source['statement_hash'] and
            target['review_hash']==source['review_hash'],'Current main source changed')
    accepted = {'utc':now,'accepted':True,'original_pr_head':pr['headRefOid'],
                'live_gate_status':'claimed_solved','original_attempt_turns':'2/5',
                'candidate_revision':2,'freeze_sha256':digest(pub/'PREPUBLICATION_FREEZE.json'),
                'package_manifest_sha256':freeze['package_manifest_sha256'],
                'files':freeze['files'],
                'exact_claim':'Compact smooth Riemannian sphere and smooth sphere homeomorphism locally minimizing Reshetnyak energy against every matching-trace W1,2 competitor on every required Lipschitz subdomain, with essentially unbounded distortion. Separate complete-target locally KS-minimizing sphere theorem with elementary nonsharp4+sqrt17 estimate; its stress-zero step also implies SL2-minimality and the classical sharper LW estimate applies.',
                'proof_gap':'None found in the exact inspected source framework',
                'source_scope':'OWR30/2025Question1p1625 and arxiv2503.08553v1Question1.9; final2026publisher mathematical body inaccessible',
                'priority':'Bounded71query32source audit; first priority and current openness unresolved, not asserted; classical sharper pointwise KS bound explicitly applies after the proved bridge',
                'full_package_reviews':[
                    {'round':1,'clean_context':True,'manifest_sha256':manifests[1],
                     'required_repairs':['R1 supporting URL','R2 applicable classical KS bound'],
                     'optional_improvements':2,'globally_resolved':True,
                     'evidence':'PUBLICATION_REVIEW_CORRECTIONS.md'},
                    {'round':2,'clean_context':True,'manifest_sha256':manifests[2],
                     'verdict':r2['verdict'],'required_repairs':0,
                     'optional_improvements':0,'clean_for_publication':True}],
                'AI_assisted':True,'unrefereed':True,'independent_human_peer_review':False,
                'formal_machine_proof_certification':False,
                'merge_and_publication_authorized_by_user':True}
    (A/'ACCEPTANCE.json').write_text(json.dumps(accepted,indent=2)+'\n')
    (A/'ACCEPTANCE.md').write_text('Accept the exact original-source Reshetnyak counterexample and separate KS theorem after two sequential fresh whole-package reviews. Both first-review required repairs and optional clarity improvements are globally resolved; the second reports no remaining issues. The stress-zero step supplies the classical sharper LW bound premise; the retained elementary bound is not an improvement. Authenticated 2025 source scope, bounded priority gaps, first-priority uncertainty, extensive AI assistance and unrefereed/no-human-review status are explicit. Merge and publish the unchanged frozen revision2 PDF/verification archive with its exact descriptor. Original2/5 preserved.\n')
    (A/'FINAL_ACCEPTANCE_GATE.json').write_text(json.dumps({'utc':now,'pr':pr,
        'remote_main':parent,'source_identity_unchanged':True,'review_manifests':manifests,
        'original_files_unchanged':30,'freeze_sha256':accepted['freeze_sha256'],
        'exact_queue_status':'claimed_solved'},indent=2)+'\n')
    state = json.loads((P/'CURRENT_STATE.json').read_text())
    state.update(utc=now,phase='PR906_accepted_merge_and_publish_next',
                 active_pr_completion_estimate_percent=96,
                 shard_completion_estimate_percent=(2+.96)/12*100)
    (P/'CURRENT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
    for log in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
        with log.open('a') as f:f.write('\n'+now+' — PR906 accepted at96% workflow/shard24.67%: both original-source theorems pass, review01 required/optional findings globally repaired, fresh review02 clean, exact freeze/review/original/live-source gates unchanged. Merge/publication next; no first-priority or human-review assertion.\n')
    print(json.dumps({'accepted':True,'candidate_revision':2,
                      'freeze_sha256':accepted['freeze_sha256'],'live_status':'claimed_solved'},indent=2))

if __name__=='__main__':main()
