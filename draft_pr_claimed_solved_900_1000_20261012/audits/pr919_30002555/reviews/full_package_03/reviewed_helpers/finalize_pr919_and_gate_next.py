"""Record completed PR919 publication and inspect only later draft status gates."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import io
import json
import subprocess
import tarfile

P = Path(__file__).resolve().parent
ROOT = P.parent
A = P/'audits/pr919_30002555'

def require(ok, message):
    if not ok: raise RuntimeError(message)

def run(args):
    return subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True).stdout

def save(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n')

def verify_receipt_links(a, publication, merge, accepted, tracker=None, native=None):
    """Fail on stale/cross-target local receipts before downstream writes."""
    def need(ok, label):
        if not ok:
            raise RuntimeError('PR919 receipt linkage: '+label)
    def read(name):
        return json.loads((a/name).read_text())
    head = '704685791ec0053dc0a52590fdef49ed4aae61d9'
    need(accepted.get('accepted') is True and accepted.get('original_pr_head') == head
         and len(accepted.get('full_package_reviews', [])) >= 2, 'exact acceptance')
    freeze_raw = (a/'publication/PREPUBLICATION_FREEZE.json').read_bytes()
    pin = hashlib.sha256(freeze_raw).hexdigest()
    freeze = json.loads(freeze_raw)
    need(pin == accepted.get('freeze_sha256') and freeze['original_pr_head'] == head
         and freeze['pr'] == 919 and freeze['problem_id'] == '30002555'
         and freeze['files'] == accepted['files'], 'accepted frozen target')
    live_head = head
    if (a/'ACCEPTANCE_INTEGRATION_ADDENDUM.json').exists():
        integration = read('ACCEPTANCE_INTEGRATION_ADDENDUM.json')
        need(integration.get('accepted') is True and integration['original_audited_head'] == head,
             'integration acceptance')
        live_head = integration['integrated_head']
    need(merge.get('number') == 919 and merge.get('state') == 'MERGED'
         and merge.get('headRefOid') == live_head, 'merged PR/head')
    merged = merge['mergeCommit']['oid']
    ident = publication.get('id')
    need(type(ident) is int and ident > 0 and publication.get('state') == 'published'
         and publication.get('doi') == '10.5281/zenodo.'+str(ident)
         and publication.get('record_url') == 'https://zenodo.org/records/'+str(ident),
         'published ID/DOI/record')
    intent = read('publication/ZENODO_PUBLISH_INTENT.json')
    need(intent.get('action') == 'publish' and intent.get('pr') == 919
         and intent['accepted_freeze_sha256'] == pin and intent['merged_commit'] == merged,
         'publication intent/accepted freeze/merge')
    descriptor_raw = (a/'publication/zenodo-deposit.json').read_bytes()
    need(hashlib.sha256(descriptor_raw).hexdigest() == intent['descriptor_sha256']
         == freeze['files']['zenodo-deposit.json']['sha256'], 'exact descriptor')
    descriptor = json.loads(descriptor_raw)
    expected = []
    for item in descriptor['files']:
        record = freeze['files'][item['path']]
        data = (a/'publication'/item['path']).read_bytes()
        need(len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256'],
             'current accepted upload bytes')
        expected.append({'name':item['name'], 'size':record['bytes'], 'sha256':record['sha256']})
    need(len(expected) == 2 and publication['files'] == expected, 'published file fingerprints')
    stage = read('publication/ZENODO_STAGE.json')
    inspected = read('publication/ZENODO_INSPECT.json')
    need(stage.get('id') == ident and stage['files'] == expected, 'staged record/files')
    need(inspected.get('id') == ident and inspected.get('doi') == publication['doi']
         and inspected.get('state') == 'published' and inspected['files'] == expected,
         'published readback ID/DOI/files')
    if tracker is not None:
        need(tracker.get('confirmed') is True and tracker.get('readback_matches') is True
             and tracker.get('pr') == 919 and tracker.get('problem_id') == '30002555'
             and tracker.get('original_pr_head') == head and tracker.get('merged_head') == live_head
             and tracker.get('merge_commit') == merged and tracker.get('accepted_freeze_sha256') == pin
             and tracker.get('doi') == publication['doi'] and tracker.get('zenodo_record_id') == ident,
             'tracker target/head/freeze/DOI')
        need(tracker.get('spreadsheet_id') == '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
             and tracker.get('gid') == 1254632077 and tracker.get('tab_title') == 'Math Puzzles'
             and len(tracker['row']) == 4 and tracker['row'][2] == 'https://doi.org/'+publication['doi']
             and read('TRACKER_READBACK.json').get('values') == [tracker['row']],
             'tracker destination/exact row readback')
    if native is not None:
        need(tracker is not None and native.get('push_confirmed') is True, 'native/tracker confirmation')
        event = native['published_event']
        need(event.get('id') == '30002555' and event.get('pr') == 919
             and event.get('doi') == publication['doi'] and event.get('original_pr_head') == head
             and event.get('accepted_freeze_sha256') == pin and event.get('merged_commit') == merged
             and event.get('zenodo_record_id') == ident
             and event['evidence']['tracker_range'] == tracker['updated_range'],
             'native target/head/freeze/DOI/tracker')


def main():
    now = datetime.now(timezone.utc).isoformat()
    publication = json.loads((A/'publication/ZENODO_PUBLISH.json').read_text())
    merge = json.loads((A/'PR_MERGE_RECEIPT.json').read_text())
    tracker = json.loads((A/'TRACKER_RECEIPT.json').read_text())
    native = json.loads((A/'NATIVE_PUBLICATION_RECEIPT.json').read_text())
    accepted = json.loads((A/'ACCEPTANCE.json').read_text())
    verify_receipt_links(A, publication, merge, accepted, tracker, native)
    require(publication['state']=='published' and merge['state']=='MERGED' and
            tracker['readback_matches'] and accepted['accepted'], 'Incomplete publication')
    require(len(accepted['full_package_reviews'])>=2, 'Sequential review evidence missing')
    ref = native['commit']; doi = publication['doi']
    q = run(['git','show',ref+':unsolved_math_prioritization/QUEUE.md'])
    rows = [r for r in q.splitlines() if '| 30002555 /' in r]
    require(len(rows)==1 and rows[0].split('|')[8].strip()=='preprint_published' and
            doi in rows[0] and rows[0].split('|')[9].strip()=='1/5', 'Queue readback failed')
    st = json.loads(run(['git','show',ref+':unsolved_math_prioritization/state.json']))
    require(st['30002555']['doi']==doi and st['30002555']['verified_candidate_approaches']==1 and
            st['30002555']['original_total_attempt_count_known'] is True and
            st['30002555']['turn_count_status']=='one_original_substantive_approach_recorded' and
            st['30002555']['turns_used'] == 1,
            'State readback failed')
    record = {'utc':now,'pr':919,'problem_id':'30002555',
              'outcome':'accepted_merged_preprint_published',
              'original_pr_head':accepted['original_pr_head'],
              'integrated_pr_head':merge['headRefOid'],
              'merge_commit':merge['mergeCommit']['oid'],'doi':doi,
              'record_url':publication['record_url'],'tracker_range':tracker['updated_range'],
              'native_ledger_commit':ref,'native_ledger_readback_confirmed':True,
              'original_turns_preserved':'1/5',
              'priority_limit':'Attributed application: APV2020preprint/2021journal complete prior bridge and ARSVW2023 explicit finite-isometry theorem credited. No new general finiteness, firstness or current-openness claim. Earlier literal named-question negative answer unestablished by bounded search; exact prescribed-matrix scope only.',
              'AI_and_peer_review':'Extensive AI assistance; unrefereed; no independent human peer review asserted'}
    save(A/'PUBLICATION_RECORD.json', record)
    integration = ('A fresh independent integration review also verified the queue conflict '
                   'reconciliation and unchanged mathematical/publication bytes. '
                   if (A/'ACCEPTANCE_INTEGRATION_ADDENDUM.json').exists() else '')
    body = f'''Accepted and published as an attributed application after independent topology, conformal, computation, source/model and two deep primary priority audits.

The exact prescribed-matrix counterexample is X={{0,2/3,1}} and the infinite cyclic rotation group generated by A=(1/5)[[3,-4],[4,3]]. Every power preserves Euclidean norm, yet no tame infinite-genus surface with three nonplanar ends can even contain A in its full matrix Veech group. The proof gives the compact-core, conformal properness and all-n trace recurrence reductions. All27 original files remain unchanged. The actual underlying surface and ends are retained; no flat completeness, finite area or trivial translation kernel is assumed.

Preprint: **A rotational obstruction to prescribed-end Veech realization**, version1.0, Alec Kriebel. DOI: [{doi}](https://doi.org/{doi}). The [Zenodo record]({publication['record_url']}) contains the three-page note and source/verification archive.

The obstruction is an application of established results. Aougab--Patel--Vlamis arXiv2007.01982v1(July4,2020), published Math.Ann.381(2021)459–498, Lemmas4.1/4.2, already gives the complete implication after uniformization to the separate complete Poincare metric on the same Riemann surface and taking the full rotational affine preimage. Artigiani--Randecker--Sadanand--Valdez--Weitze-Schmithusen arXiv2311.00158v1Theorem1.6(2023), v2Theorem1.8(2026), explicitly proves the needed translation-surface finite-isometry principle. No new general finiteness theorem, construction, classification, first-priority assertion or current-openness certificate is claimed. No earlier literal negative answer to OWR2014Question4/RMV2017Question0.2 was established in inspected sources; bounded search is not firstness. Official AGT forthcoming metadata is used without inventing a final journal body/DOI/pages.

The result answers the universal prescribed-matrix question. It does not exclude an abstract cyclic group with another nonorthogonal generator, finite rotation groups, or realize/classify all groups for each end space. The n=1,2 compact-core boundary fails as expected. Separate Jacobs-ladder/lattice/finite-area questions remain outside scope.

Sequential NEW whole-package adversarial reviews and all global repairs are recorded. {integration}The portable release wrapper authenticates the complete closed packet and copied checker bytes before isolated nonoptimized current workers, with controlled historical optimization comparisons. Exact arithmetic and hash controls supplement the written universal proof, not certify mathematics or priority by samples. Historical guard limitations remain documented without rewriting original bytes. Raw third-party source bodies are excluded.

AI tools were used extensively in research, writing, verification and adversarial review. This is an unrefereed preprint; no independent human or journal peer review or formal proof-assistant certification is claimed. Exact reviewed metadata and uploaded bytes were verified, and the DOI row was appended/read back at {tracker['updated_range']}. Original author accounting remains1/5; audits add no author proof-search turn.

Original audited head: `{accepted['original_pr_head']}`. Merged head: `{merge['headRefOid']}`. Audit/publication receipts: `draft_pr_claimed_solved_900_1000_20261012/audits/pr919_30002555/`.
'''
    (A/'PR_PUBLISHED_BODY.md').write_text(body)
    run(['gh','pr','edit','919','--repo','AlecKriebel/Math','--title',
         '30002555: accepted rotational counterexample and published preprint',
         '--body-file',str(A/'PR_PUBLISHED_BODY.md')])
    save(A/'PR_PUBLISHED_METADATA.json', json.loads(run(['gh','pr','view','919',
         '--repo','AlecKriebel/Math','--json','number,title,body,state,mergedAt,mergeCommit,url'])))
    confirmed = json.loads((A/'PR_PUBLISHED_METADATA.json').read_text())
    require(confirmed['state']=='MERGED' and confirmed['body']==body and
            confirmed['mergeCommit']['oid']==merge['mergeCommit']['oid'],
            'Final published PR metadata failed exact readback')
    state = json.loads((P/'CURRENT_STATE.json').read_text())
    completed = [r for r in state.get('completed_results',[]) if r['pr']!=919]+[record]
    state.update(utc=now,completed_prs=[r['pr'] for r in completed],completed_results=completed,
                 publication='PR904_PR905_PR906_PR908_PR909_PR919_published_tracker_native_ledgers_verified',
                 shard_completion_estimate_percent=100*len(completed)/12,
                 active_pr=None,active_problem_id=None,phase='next_status_gate',
                 active_pr_completion_estimate_percent=0)
    inventory = json.loads((P/'inventory.json').read_text())
    for entry in inventory:
        if entry['number']==919:
            entry.update(disposition=record['outcome'],doi=doi,tracker_range=tracker['updated_range'])
    with (P/'README.md').open('a') as f:
        f.write(f'\nPR #919 is accepted, merged and published: [{doi}](https://doi.org/{doi}), '
                f'tracker {tracker["updated_range"]}. Exact prescribed-matrix scope, prior finiteness '
                'credits, bounded priority and unrefereed AI disclosures are explicit.\n')
    for log in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
        with log.open('a') as f:
            f.write(f'\n### {now} — PR919 completed (100%; shard50%)\n'
                    f'Merged {record["merge_commit"]}; exact reviewed bytes and metadata published '
                    f'under {doi}; tracker {tracker["updated_range"]} and native ledger {ref} '
                    'read back. Other targets untouched; original1/5 preserved.\n')
    # Later PRs are inspected only for status until one passes the exact gate.
    skipped = []
    for prior in sorted((r for r in inventory if r['number']>919),key=lambda r:r['number']):
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
    save(P/'POST_PR919_STATUS_GATES.json',{'utc':now,'skipped':skipped,'next_pr':state.get('active_pr')})
    print(json.dumps({'PR919':record,'next_pr':state.get('active_pr'),'status_only_skips':skipped},indent=2))

if __name__=='__main__': main()
