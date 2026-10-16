"""Record the completed publication, then gate the next draft without auditing skips."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import io
import json
import subprocess
import tarfile

P=Path(__file__).resolve().parent
ROOT=P.parent
A=P/'audits/pr905_30000717'

def run(args):
    return subprocess.run(args,cwd=ROOT,check=True,text=True,capture_output=True).stdout

def main():
    now=datetime.now(timezone.utc).isoformat()
    publication=json.loads((A/'publication/ZENODO_PUBLISH.json').read_text())
    merge=json.loads((A/'PR_MERGE_RECEIPT.json').read_text())
    tracker=json.loads((A/'TRACKER_RECEIPT.json').read_text())
    native=json.loads((A/'NATIVE_PUBLICATION_RECEIPT.json').read_text())
    accepted=json.loads((A/'ACCEPTANCE.json').read_text())
    if publication['state']!='published' or merge['state']!='MERGED' or not tracker['readback_matches']:
        raise RuntimeError('Publication workflow incomplete')
    ref=native['commit']; doi=publication['doi']
    q=run(['git','show',ref+':unsolved_math_prioritization/QUEUE.md'])
    rows=[r for r in q.splitlines() if '| 30000717 /' in r]
    if len(rows)!=1 or rows[0].split('|')[8].strip()!='preprint_published' or doi not in rows[0]:
        raise RuntimeError('Native queue readback failed')
    st=json.loads(run(['git','show',ref+':unsolved_math_prioritization/state.json']))
    if st['30000717']['doi']!=doi or st['30000717']['turns_used']!=1:
        raise RuntimeError('Native state readback failed')
    record={'utc':now,'pr':905,'problem_id':'30000717',
            'outcome':'accepted_merged_preprint_published',
            'original_pr_head':accepted['original_pr_head'],
            'integrated_pr_head':merge['headRefOid'],
            'merge_commit':merge['mergeCommit']['oid'],'doi':doi,
            'record_url':publication['record_url'],'tracker_range':tracker['updated_range'],
            'native_ledger_commit':ref,'native_ledger_readback_confirmed':True,
            'original_turns_preserved':'1/5',
            'priority_limit':'First priority and continued open status not established or asserted; classical ingredients credited',
            'AI_and_peer_review':'Extensive AI assistance; unrefereed; no independent human peer review asserted'}
    (A/'PUBLICATION_RECORD.json').write_text(json.dumps(record,indent=2)+'\n')
    body=f'''Accepted and published after independent universal-proof, exact-computation, source/model and bounded priority audits.

For the classical Robinson sextic R, every real epsilon >= 0 fails the ideal-only polynomial SOS certificate modulo the full real vanishing ideal of either explicitly defined literal-product or tangency-minor ideal. The proof covers arbitrary finite sums and polynomial degrees. The two source readings and the absence of an authenticated intended-author correction are explicit.

Preprint: **A Robinson counterexample to ideal-only tangency certificates**, version 1.0, Alec Kriebel. DOI: [{doi}](https://doi.org/{doi}). The [Zenodo record]({publication['record_url']}) includes the four-page note and source/verification archive.

Two sequential fresh full-package adversarial reviews were completed. A Laurent manuscript-version/locator mismatch found by the first review was repaired globally; the second found no required or optional repairs. A separate fresh integration audit verified the queue-only conflict reconciliation with main and unchanged reviewed packet bytes. Classical ingredients are credited to Reznick, Schweighofer and Laurent. Full-text priority access gaps are disclosed; first bibliographic priority and continued open status through 2026 are not established or asserted.

AI tools were used extensively in proof development and verification. This is an unrefereed preprint; independent human or journal peer review is not claimed. Uploaded bytes and metadata were verified, and the DOI was appended and read back in the requested tracker at {tracker['updated_range']}. Original 1/5 proof-attempt count preserved.

Original audited head: `{accepted['original_pr_head']}`. Byte-preserving integrated head: `{merge['headRefOid']}`. Audit/publication receipts: `draft_pr_claimed_solved_900_1000_20261012/audits/pr905_30000717/`.
'''
    (A/'PR_PUBLISHED_BODY.md').write_text(body)
    run(['gh','pr','edit','905','--repo','AlecKriebel/Math','--title',
         '30000717: accepted Robinson certificate obstruction and published preprint',
         '--body-file',str(A/'PR_PUBLISHED_BODY.md')])
    (A/'PR_PUBLISHED_METADATA.json').write_text(run(['gh','pr','view','905','--repo',
         'AlecKriebel/Math','--json','number,title,body,state,mergedAt,mergeCommit,url']))
    state=json.loads((P/'CURRENT_STATE.json').read_text())
    completed=[r for r in state.get('completed_results',[]) if r['pr']!=905]+[record]
    state.update(utc=now,completed_prs=[r['pr'] for r in completed],completed_results=completed,
                 publication='PR904_and_PR905_published_tracker_and_native_ledgers_verified',
                 shard_completion_estimate_percent=100*len(completed)/12)
    inventory=json.loads((P/'inventory.json').read_text())
    for entry in inventory:
        if entry['number']==905:
            entry.update(disposition=record['outcome'],doi=doi,tracker_range=tracker['updated_range'])
    (P/'inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
    with (P/'README.md').open('a') as f:
        f.write(f'\nPR #905 is accepted, merged and published: [{doi}](https://doi.org/{doi}), '
                f'tracker {tracker["updated_range"]}. The frozen revision 2 passed the fresh review after '
                'the source-version repair; its queue conflict reconciliation preserved all reviewed bytes.\n')
    for log in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
        with log.open('a') as f:
            f.write(f'\n### {now} — PR905 completed (100%; shard 16.67%)\n'
                    f'Merged {record["merge_commit"]}, exact reviewed files and metadata published '
                    f'under {doi}. Tracker {tracker["updated_range"]} and native ledger {ref} verified. '
                    'Source-version correction retained; priority and unrefereed AI disclosures explicit. '
                    'No other target status altered.\n')
    # No mathematical content is read until this exact-status gate succeeds.
    pr=json.loads(run(['gh','pr','view','906','--repo','AlecKriebel/Math','--json',
                       'number,title,state,isDraft,headRefOid,headRefName,url']))
    q=run(['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+
           pr['headRefOid'],'-H','Accept: application/vnd.github.raw+json'])
    rows=[r for r in q.splitlines() if '| 30006419 /' in r]
    if len(rows)!=1: raise RuntimeError('Next target identity is ambiguous')
    pr.update(problem_id='30006419',status=rows[0].split('|')[8].strip(),
              queue_row_sha256=hashlib.sha256(rows[0].encode()).hexdigest(),gate_utc=now)
    pr['eligible']=pr['state']=='OPEN' and pr['isDraft'] and pr['status']=='claimed_solved'
    B=P/'audits/pr906_30006419'; B.mkdir(parents=True,exist_ok=True)
    (B/'ELIGIBILITY_GATE.json').write_text(json.dumps(pr,indent=2)+'\n')
    if pr['eligible']:
        run(['git','fetch','--no-write-fetch-head','origin',pr['headRefOid']])
        original=B/'original'; original.mkdir(exist_ok=True)
        prefix='unsolved_math_prioritization/attempts/30006419'
        data=subprocess.run(['git','archive',pr['headRefOid'],prefix],cwd=ROOT,
                            check=True,capture_output=True).stdout
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:
            archive.extractall(original,filter='data')
        files={p.relative_to(original).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
               for p in sorted(original.rglob('*')) if p.is_file()}
        (B/'ORIGINAL_SNAPSHOT.json').write_text(json.dumps({'utc':now,'head':pr['headRefOid'],
                                                         'files':files},indent=2)+'\n')
        (B/'GATED_QUEUE_ROW.md').write_text(rows[0]+'\n')
    for key in ['mathematics_gates','priority_gate','fresh_full_package_reviews','candidate_revision']:
        state.pop(key,None)
    state.update(active_pr=906 if pr['eligible'] else None,
                 active_problem_id='30006419' if pr['eligible'] else None,
                 next_pr=906,phase='PR906_independent_math_audit' if pr['eligible'] else 'continue_status_gating',
                 active_pr_completion_estimate_percent=0)
    (P/'CURRENT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps({'PR905':record,'PR906_gate':pr},indent=2))

if __name__=='__main__':
    main()
