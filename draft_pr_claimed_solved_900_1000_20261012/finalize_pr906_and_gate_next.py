"""Record completed PR906 publication and inspect only later draft status gates."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import io
import json
import subprocess
import tarfile

P = Path(__file__).resolve().parent
ROOT = P.parent
A = P/'audits/pr906_30006419'

def require(ok, message):
    if not ok: raise RuntimeError(message)

def run(args):
    return subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True).stdout

def save(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n')

def main():
    now = datetime.now(timezone.utc).isoformat()
    publication = json.loads((A/'publication/ZENODO_PUBLISH.json').read_text())
    merge = json.loads((A/'PR_MERGE_RECEIPT.json').read_text())
    tracker = json.loads((A/'TRACKER_RECEIPT.json').read_text())
    native = json.loads((A/'NATIVE_PUBLICATION_RECEIPT.json').read_text())
    accepted = json.loads((A/'ACCEPTANCE.json').read_text())
    require(publication['state']=='published' and merge['state']=='MERGED' and
            tracker['readback_matches'] and accepted['accepted'], 'Incomplete publication')
    require(len(accepted['full_package_reviews'])>=2, 'Sequential review evidence missing')
    ref = native['commit']; doi = publication['doi']
    q = run(['git','show',ref+':unsolved_math_prioritization/QUEUE.md'])
    rows = [r for r in q.splitlines() if '| 30006419 /' in r]
    require(len(rows)==1 and rows[0].split('|')[8].strip()=='preprint_published' and
            doi in rows[0] and rows[0].split('|')[9].strip()=='2/5', 'Queue readback failed')
    st = json.loads(run(['git','show',ref+':unsolved_math_prioritization/state.json']))
    require(st['30006419']['doi']==doi and st['30006419']['turns_used']==2,
            'State readback failed')
    record = {'utc':now,'pr':906,'problem_id':'30006419',
              'outcome':'accepted_merged_preprint_published',
              'original_pr_head':accepted['original_pr_head'],
              'integrated_pr_head':merge['headRefOid'],
              'merge_commit':merge['mergeCommit']['oid'],'doi':doi,
              'record_url':publication['record_url'],'tracker_range':tracker['updated_range'],
              'native_ledger_commit':ref,'native_ledger_readback_confirmed':True,
              'original_turns_preserved':'2/5',
              'priority_limit':'Bounded audit; first priority and continued openness not asserted; final 2026 publisher mathematical text inaccessible; classical inputs credited',
              'AI_and_peer_review':'Extensive AI assistance; unrefereed; no independent human peer review asserted'}
    save(A/'PUBLICATION_RECORD.json', record)
    integration = ('A fresh independent integration review also verified the queue conflict '
                   'reconciliation and unchanged mathematical/publication bytes. '
                   if (A/'ACCEPTANCE_INTEGRATION_ADDENDUM.json').exists() else '')
    body = f'''Accepted and published after independent universal-proof, exact/mixed-computation, source/model and bounded priority audits.

A compact smooth Riemannian sphere admits a smooth homeomorphism from the round sphere that minimizes Reshetnyak energy on every sufficiently small neighborhood against all same-trace W1,2 competitors, with essentially unbounded infinitesimal distortion. This answers the Reshetnyak member of the inspected general-energy question negatively. The map is neither a global homotopy minimizer nor KS-harmonic. A separate complete-target Korevaar–Schoen theorem gives the elementary nonsharp bound 4+sqrt(17); its stress-zero step also supplies the SL(2)-minimality premise for the older sharper Lytchak–Wenger bound.

Preprint: **A smooth Reshetnyak-harmonic sphere with unbounded distortion**, version 1.0, Alec Kriebel. DOI: [{doi}](https://doi.org/{doi}). The [Zenodo record]({publication['record_url']}) contains the six-page note and source/verification archive.

Sequential fresh full-package adversarial reviews were completed; their findings and global repairs, if any, are recorded in the acceptance receipt. {integration}The question is bound to OWR30/2025 Question1 p1625 and authenticated arXiv2503.08553v1 Question1.9. The revised 2026 publisher body was inaccessible. Classical ingredients are credited. The bounded priority audit has explicit coverage gaps; first bibliographic priority and continued openness through2026 are not asserted.

AI tools were used extensively in development and verification. This is an unrefereed preprint; independent human or journal peer review is not claimed. Uploaded bytes and metadata were verified, and the DOI was appended and read back at {tracker['updated_range']}. Original 2/5 proof-attempt count preserved. Finite controls support the written proofs and are not formal certification.

Original audited head: `{accepted['original_pr_head']}`. Merged head: `{merge['headRefOid']}`. Audit/publication receipts: `draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/`.
'''
    (A/'PR_PUBLISHED_BODY.md').write_text(body)
    run(['gh','pr','edit','906','--repo','AlecKriebel/Math','--title',
         '30006419: accepted harmonic-sphere energy result and published preprint',
         '--body-file',str(A/'PR_PUBLISHED_BODY.md')])
    save(A/'PR_PUBLISHED_METADATA.json', json.loads(run(['gh','pr','view','906',
         '--repo','AlecKriebel/Math','--json','number,title,body,state,mergedAt,mergeCommit,url'])))
    state = json.loads((P/'CURRENT_STATE.json').read_text())
    completed = [r for r in state.get('completed_results',[]) if r['pr']!=906]+[record]
    state.update(utc=now,completed_prs=[r['pr'] for r in completed],completed_results=completed,
                 publication='PR904_PR905_PR906_published_tracker_native_ledgers_verified',
                 shard_completion_estimate_percent=100*len(completed)/12,
                 active_pr=None,active_problem_id=None,phase='next_status_gate',
                 active_pr_completion_estimate_percent=0)
    inventory = json.loads((P/'inventory.json').read_text())
    for entry in inventory:
        if entry['number']==906:
            entry.update(disposition=record['outcome'],doi=doi,tracker_range=tracker['updated_range'])
    with (P/'README.md').open('a') as f:
        f.write(f'\nPR #906 is accepted, merged and published: [{doi}](https://doi.org/{doi}), '
                f'tracker {tracker["updated_range"]}. Exact energy-specific scope, classical '
                'credits, bounded priority and unrefereed AI disclosures are explicit.\n')
    for log in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
        with log.open('a') as f:
            f.write(f'\n### {now} — PR906 completed (100%; shard25%)\n'
                    f'Merged {record["merge_commit"]}; exact reviewed bytes and metadata published '
                    f'under {doi}; tracker {tracker["updated_range"]} and native ledger {ref} '
                    'read back. Other targets untouched; original2/5 preserved.\n')
    # Later PRs are inspected only for status until one passes the exact gate.
    skipped = []
    for prior in sorted((r for r in inventory if r['number']>906),key=lambda r:r['number']):
        number = prior['number']
        pr = json.loads(run(['gh','pr','view',str(number),'--repo','AlecKriebel/Math',
                            '--json','number,title,state,isDraft,headRefOid,headRefName,url']))
        if pr['state']!='OPEN' or not pr['isDraft']:
            skipped.append({'pr':number,'reason':'not_open_draft'})
            continue
        queue = run(['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+
                     pr['headRefOid'],'-H','Accept: application/vnd.github.raw+json'])
        keys = [e['id'] for e in prior['entries']]
        require(len(keys)==1, 'Multiple-target status gate needs narrow reconciliation')
        key = str(keys[0])
        matches = [r for r in queue.splitlines() if '| '+key+' /' in r]
        require(len(matches)==1,'Ambiguous next-target identity')
        status = matches[0].split('|')[8].strip()
        if status!='claimed_solved':
            skipped.append({'pr':number,'problem_id':key,'status':status,'action':'skipped_status_only'})
            prior.update(eligible=False,disposition='skipped_status_gate')
            continue
        folder = P/'audits'/('pr'+str(number)+'_'+key)
        folder.mkdir(parents=True,exist_ok=True)
        pr.update(problem_id=key,status=status,eligible=True,gate_utc=now,
                  queue_row_sha256=hashlib.sha256(matches[0].encode()).hexdigest())
        save(folder/'ELIGIBILITY_GATE.json',pr)
        (folder/'GATED_QUEUE_ROW.md').write_text(matches[0]+'\n')
        run(['git','fetch','--no-write-fetch-head','origin',pr['headRefOid']])
        original = folder/'original'; original.mkdir(exist_ok=True)
        prefix = 'unsolved_math_prioritization/attempts/'+key
        data = subprocess.run(['git','archive',pr['headRefOid'],prefix],cwd=ROOT,
                              check=True,capture_output=True).stdout
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:
            archive.extractall(original,filter='data')
        files = {f.relative_to(original).as_posix():hashlib.sha256(f.read_bytes()).hexdigest()
                 for f in sorted(original.rglob('*')) if f.is_file()}
        save(folder/'ORIGINAL_SNAPSHOT.json',{'utc':now,'head':pr['headRefOid'],'files':files})
        for name in ['mathematics_gates','priority_gate','fresh_full_package_reviews',
                     'candidate_revision','package_revision','package_manifest_sha256']:
            state.pop(name,None)
        state.update(active_pr=number,active_problem_id=key,next_pr=number,
                     phase='PR'+str(number)+'_independent_math_audit',
                     active_original_head=pr['headRefOid'],active_pr_completion_estimate_percent=0)
        break
    save(P/'inventory.json',inventory)
    save(P/'CURRENT_STATE.json',state)
    save(P/'POST_PR906_STATUS_GATES.json',{'utc':now,'skipped':skipped,'next_pr':state.get('active_pr')})
    print(json.dumps({'PR906':record,'next_pr':state.get('active_pr'),'status_only_skips':skipped},indent=2))

if __name__=='__main__': main()
