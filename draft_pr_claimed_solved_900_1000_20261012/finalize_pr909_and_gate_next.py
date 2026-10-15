"""Record completed PR909 publication and inspect only later draft status gates."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import io
import json
import subprocess
import tarfile

P = Path(__file__).resolve().parent
ROOT = P.parent
A = P/'audits/pr909_30001345'

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
    rows = [r for r in q.splitlines() if '| 30001345 /' in r]
    require(len(rows)==1 and rows[0].split('|')[8].strip()=='preprint_published' and
            doi in rows[0] and rows[0].split('|')[9].strip()=='1 verified/5', 'Queue readback failed')
    st = json.loads(run(['git','show',ref+':unsolved_math_prioritization/state.json']))
    require(st['30001345']['doi']==doi and st['30001345']['verified_candidate_approaches']==1 and
            st['30001345']['original_total_attempt_count_known'] is False and
            st['30001345']['turn_count_status']=='total_unknown_earlier_attempt_history_unavailable' and
            st['30001345']['turns_used'] is None,
            'State readback failed')
    record = {'utc':now,'pr':909,'problem_id':'30001345',
              'outcome':'accepted_merged_preprint_published',
              'original_pr_head':accepted['original_pr_head'],
              'integrated_pr_head':merge['headRefOid'],
              'merge_commit':merge['mergeCommit']['oid'],'doi':doi,
              'record_url':publication['record_url'],'tracker_range':tracker['updated_range'],
              'native_ledger_commit':ref,'native_ledger_readback_confirmed':True,
              'original_turns_preserved':'1 verified/5; earlier-attempt count unavailable',
              'priority_limit':'Attributed classical corollary: prior arrangement, deformation method and ordinary-point formula credited. No construction/method novelty, firstness or continued-openness claim. Earlier literal same rough-M theorem not established. Unrestricted literal summed 2009 reading only; not explicitly unibranched 2014 Conjecture3.8',
              'AI_and_peer_review':'Extensive AI assistance; unrefereed; no independent human peer review asserted'}
    save(A/'PUBLICATION_RECORD.json', record)
    integration = ('A fresh independent integration review also verified the queue conflict '
                   'reconciliation and unchanged mathematical/publication bytes. '
                   if (A/'ACCEPTANCE_INTEGRATION_ADDENDUM.json').exists() else '')
    body = f'''Accepted and published as an explicitly attributed classical corollary after independent construction, invariant, exact-computation, source/model and deep primary priority audits.

The explicit reduced flat multibranch delta-constant family has finite simultaneous normalization and a common transverse ball. Its ordinary-nine central point has delta 36 and rough K(K+D)=7; every small nonzero complex fiber has twelve ordinary triples with summed delta 36 and summed rough 12. The original classical Fermat extension gives excess n²−4 for every integer n>=3 by a structural all-n proof, not finite sampling. All 28 original files remain unchanged.

Preprint: **Classical arrangement counterexamples to summed rough-M semicontinuity**, version 1.0, Alec Kriebel. DOI: [{doi}](https://doi.org/{doi}). The [Zenodo record]({publication['record_url']}) contains the four-page note and source/verification archive.

The construction and method are prior: de Jong–van Straten 1998 uses the exact dual-Hesse configuration in the delta-constant picture-deformation framework; Plamenevskaya–Starkston 2023 explicitly scales affine line constants to zero; Borodzik 2014 p. 578 uses contraction to an ordinary multiple point and rough value r−2. Hirzebruch's classical arrangements supply the all-n geometry. The complete local implication is checked in the audits. No new construction/method, first-priority assertion or current-openness certificate is claimed. An earlier literal statement of the exact rough-M inequality was not established; this does not prove firstness, and no 1998 rough-M theorem is invented.

The result answers only the unrestricted literal summed reading of the rough-invariant Questions 2–3 in the 2009 Oberwolfach contribution, printed pp. 2446–2447. The question itself does not literally display a sum; the subsequent fixed-ball comparison supports that reading. No unstated author intention, marked-section result, or solution of the explicitly unibranched parametric Conjecture 3.8 in the 2014 journal paper is asserted. Rational normalization does not make the central fiber unibranched.

Two sequential fresh whole-package adversarial reviews and all global repairs are recorded. {integration}The release authenticates the exact closed original packet and copied checker bytes before isolated nonoptimized execution. Finite exact controls supplement the written analytic proof and do not certify priority or universal analytic conclusions by sampling. Historical checker limitations are preserved and documented, with a separate stronger guard. No raw third-party bodies are distributed.

AI tools were used extensively in research, writing, verification and adversarial review. This is an unrefereed preprint; independent human or journal peer review is not claimed. Uploaded bytes and exact reviewed metadata were verified, and the DOI row was appended/read back at {tracker['updated_range']}. The original recovery count remains **1 verified/5; earlier attempt total unavailable**. These audits add no author proof-search turn and do not invent a complete earlier search history.

Original audited head: `{accepted['original_pr_head']}`. Merged head: `{merge['headRefOid']}`. Audit/publication receipts: `draft_pr_claimed_solved_900_1000_20261012/audits/pr909_30001345/`.
'''
    (A/'PR_PUBLISHED_BODY.md').write_text(body)
    run(['gh','pr','edit','909','--repo','AlecKriebel/Math','--title',
         '30001345: accepted rough-M corollary and published preprint',
         '--body-file',str(A/'PR_PUBLISHED_BODY.md')])
    save(A/'PR_PUBLISHED_METADATA.json', json.loads(run(['gh','pr','view','909',
         '--repo','AlecKriebel/Math','--json','number,title,body,state,mergedAt,mergeCommit,url'])))
    confirmed = json.loads((A/'PR_PUBLISHED_METADATA.json').read_text())
    require(confirmed['state']=='MERGED' and confirmed['body']==body and
            confirmed['mergeCommit']['oid']==merge['mergeCommit']['oid'],
            'Final published PR metadata failed exact readback')
    state = json.loads((P/'CURRENT_STATE.json').read_text())
    completed = [r for r in state.get('completed_results',[]) if r['pr']!=909]+[record]
    state.update(utc=now,completed_prs=[r['pr'] for r in completed],completed_results=completed,
                 publication='PR904_PR905_PR906_PR908_PR909_published_tracker_native_ledgers_verified',
                 shard_completion_estimate_percent=100*len(completed)/12,
                 active_pr=None,active_problem_id=None,phase='next_status_gate',
                 active_pr_completion_estimate_percent=0)
    inventory = json.loads((P/'inventory.json').read_text())
    for entry in inventory:
        if entry['number']==909:
            entry.update(disposition=record['outcome'],doi=doi,tracker_range=tracker['updated_range'])
    with (P/'README.md').open('a') as f:
        f.write(f'\nPR #909 is accepted, merged and published: [{doi}](https://doi.org/{doi}), '
                f'tracker {tracker["updated_range"]}. Exact summed multibranch scope, classical construction/method '
                'credits, bounded priority and unrefereed AI disclosures are explicit.\n')
    for log in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
        with log.open('a') as f:
            f.write(f'\n### {now} — PR909 completed (100%; shard41.67%)\n'
                    f'Merged {record["merge_commit"]}; exact reviewed bytes and metadata published '
                    f'under {doi}; tracker {tracker["updated_range"]} and native ledger {ref} '
                    'read back. Other targets untouched; original1 verified/5 and unavailable earlier history preserved.\n')
    # Later PRs are inspected only for status until one passes the exact gate.
    skipped = []
    for prior in sorted((r for r in inventory if r['number']>909),key=lambda r:r['number']):
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
                     'candidate_revision','package_revision','package_manifest_sha256','review_families',
                     'original_candidate_turns','publication_disposition','priority_status']:
            state.pop(name,None)
        state.update(active_pr=number,active_problem_id=key,next_pr=number,
                     phase='PR'+str(number)+'_independent_math_audit',
                     active_original_head=pr['headRefOid'],active_pr_completion_estimate_percent=0)
        break
    save(P/'inventory.json',inventory)
    save(P/'CURRENT_STATE.json',state)
    save(P/'POST_PR909_STATUS_GATES.json',{'utc':now,'skipped':skipped,'next_pr':state.get('active_pr')})
    print(json.dumps({'PR909':record,'next_pr':state.get('active_pr'),'status_only_skips':skipped},indent=2))

if __name__=='__main__': main()
