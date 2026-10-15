"""Append only the verified PR938 publication, with duplicate/readback guards."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
AUDIT = Path(__file__).resolve().parent / 'audits/pr938_30003634'
SID = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'

def gws(args):
    result = subprocess.run(['gws', *args], cwd=ROOT, check=True,
                            capture_output=True, text=True)
    return json.loads(result.stdout)

def save(name, value):
    (AUDIT/name).write_text(json.dumps(value, indent=2)+'\n')

def valid_tracker_range(value):
    if type(value) is not str:
        return False
    match = re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1", value)
    return match is not None and int(match[1]) >= 2


def verify_receipt_links(a, publication, merge, accepted, tracker=None, native=None):
    """Fail on stale/cross-target local receipts before downstream writes."""
    def need(ok, label):
        if not ok:
            raise RuntimeError('PR938 receipt linkage: '+label)
    def read(name):
        return json.loads((a/name).read_text())
    head = '2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b'
    need(accepted.get('accepted') is True and accepted.get('original_pr_head') == head
         and len(accepted.get('full_package_reviews', [])) >= 2, 'exact acceptance')
    freeze_raw = (a/'publication/PREPUBLICATION_FREEZE.json').read_bytes()
    pin = hashlib.sha256(freeze_raw).hexdigest()
    freeze = json.loads(freeze_raw)
    need(pin == accepted.get('freeze_sha256') and freeze['original_pr_head'] == head
         and freeze['pr'] == 938 and freeze['problem_id'] == '30003634'
         and freeze['files'] == accepted['files'], 'accepted frozen target')
    live_head = head
    if (a/'ACCEPTANCE_INTEGRATION_ADDENDUM.json').exists():
        integration = read('ACCEPTANCE_INTEGRATION_ADDENDUM.json')
        need(integration.get('accepted') is True and integration['original_audited_head'] == head,
             'integration acceptance')
        live_head = integration['integrated_head']
    need(merge.get('number') == 938 and merge.get('state') == 'MERGED'
         and merge.get('headRefOid') == live_head, 'merged PR/head')
    merged = merge['mergeCommit']['oid']
    ident = publication.get('id')
    need(type(ident) is int and ident > 0 and publication.get('state') == 'published'
         and publication.get('doi') == '10.5281/zenodo.'+str(ident)
         and publication.get('record_url') == 'https://zenodo.org/records/'+str(ident),
         'published ID/DOI/record')
    intent = read('publication/ZENODO_PUBLISH_INTENT.json')
    need(intent.get('action') == 'publish' and intent.get('pr') == 938
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
             and tracker.get('pr') == 938 and tracker.get('problem_id') == '30003634'
             and tracker.get('original_pr_head') == head and tracker.get('merged_head') == live_head
             and tracker.get('merge_commit') == merged and tracker.get('accepted_freeze_sha256') == pin
             and tracker.get('doi') == publication['doi'] and tracker.get('zenodo_record_id') == ident,
             'tracker target/head/freeze/DOI')
        need(valid_tracker_range(tracker.get('updated_range')), 'tracker exact destination/columns/single data row')
        readback = read('TRACKER_READBACK.json')
        need(readback.get('range') == tracker['updated_range'], 'tracker exact returned/readback A1 range')
        need(tracker.get('spreadsheet_id') == '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
             and tracker.get('gid') == 1254632077 and tracker.get('tab_title') == 'Math Puzzles'
             and len(tracker['row']) == 4 and tracker['row'][2] == 'https://doi.org/'+publication['doi']
             and read('TRACKER_READBACK.json').get('values') == [tracker['row']],
             'tracker destination/exact row readback')
    if native is not None:
        need(tracker is not None and native.get('push_confirmed') is True, 'native/tracker confirmation')
        event = native['published_event']
        need(event.get('id') == '30003634' and event.get('pr') == 938
             and event.get('doi') == publication['doi'] and event.get('original_pr_head') == head
             and event.get('accepted_freeze_sha256') == pin and event.get('merged_commit') == merged
             and event.get('zenodo_record_id') == ident
             and event['evidence']['tracker_range'] == tracker['updated_range'],
             'native target/head/freeze/DOI/tracker')


def main():
    publication = json.loads((AUDIT/'publication/ZENODO_PUBLISH.json').read_text())
    merge = json.loads((AUDIT/'PR_MERGE_RECEIPT.json').read_text())
    if publication['state'] != 'published' or merge['state'] != 'MERGED':
        raise RuntimeError('Merge and publication must be confirmed first')
    acceptance = json.loads((AUDIT/'ACCEPTANCE.json').read_text())
    if acceptance.get('accepted') is not True:
        raise RuntimeError('Exact package acceptance is required')
    verify_receipt_links(AUDIT, publication, merge, acceptance)
    doi = publication['doi']
    if doi != f"10.5281/zenodo.{publication['id']}":
        raise RuntimeError('Unexpected DOI')
    tabs = gws(['sheets','spreadsheets','get','--params',
                json.dumps({'spreadsheetId':SID,'fields':'sheets.properties'})])
    target = next(x['properties'] for x in tabs['sheets']
                  if x['properties']['sheetId']==1254632077)
    if target['title'] != 'Math Puzzles':
        raise RuntimeError('Target tab identity changed')
    table = "'Math Puzzles'!A:D"
    existing = gws(['sheets','spreadsheets','values','get','--params',
                    json.dumps({'spreadsheetId':SID,'range':table})])
    save('tracker_existing_rows_private.json', existing)
    if existing.get('values',[[]])[0] != ['Original Problem','Solution Chat URL','DOI','Notes']:
        raise RuntimeError('Tracker header changed')
    row = ["https://doi.org/10.4171/OWR/2017/50", "", "https://doi.org/"+doi,
        "30003634 / OWR-15955-011, Harvey-Park-Ray Question3p3021. Deep derived pure braids need not be 1-solvable; v1.0,4-page unrefereed note and source/verification archive. For every m>=3 and finite k>=1, P_m^(k) is not contained in integral smooth F_1^m; hence the proposed containment fails for every n>=1. Distinct existential witnesses may depend on depth; no common braid in the derived intersection. The original explicit104-letter P3^(3) witness has signature-2; finite Goeritz and Meyer checks supplement the universal proof. General signature/quasimorphism tools are credited to Gambaudo-Ghys, Calegari and Kawasaki etal2025Lemma7.12; Otto/Toffoli supply the actual solvability/signature framework. Bounded independent deep priority audits establish no complete predecessor; no firstness/current-openness or new general group theorem claim. PR #938 merged after distinct mathematical families and sequential NEW whole-package adversarial reviews. Extensive AI assistance; no independent human review or formal proof certification. Original observed1/5 preserved; one new completed strengthening counted separately, known combined2/5. https://github.com/AlecKriebel/Math/pull/938"]

    hits = [(i+1,r) for i,r in enumerate(existing.get('values',[]))
            if any(doi in str(v) for v in r)]
    if hits:
        if len(hits)!=1 or hits[0][1]!=row:
            raise RuntimeError('Existing DOI entry requires reconciliation')
        index=hits[0][0]
        updated_range=f"'Math Puzzles'!A{index}:D{index}"
        appended={'recovered_existing_identical_row':True}
    else:
        params={'spreadsheetId':SID,'range':table,'valueInputOption':'RAW',
                'insertDataOption':'INSERT_ROWS'}
        save('TRACKER_APPEND_INTENT.json',{'params':params,'row':row})
        appended = gws(['sheets','spreadsheets','values','append','--params',
                        json.dumps(params),'--json',json.dumps({'values':[row]})])
        save('TRACKER_APPEND_RESPONSE.json', appended)
        updated_range=appended['updates']['updatedRange']
        if appended['updates']['updatedRows']!=1 or appended['updates']['updatedCells']!=4:
            raise RuntimeError('Unexpected append dimensions')
    if not valid_tracker_range(updated_range):
        raise RuntimeError('Tracker append/recovery range is not the intended single Math Puzzles A:D data row')
    readback = gws(['sheets','spreadsheets','values','get','--params',
                    json.dumps({'spreadsheetId':SID,'range':updated_range})])
    save('TRACKER_READBACK.json',readback)
    if readback.get('values') != [row] or readback.get('range') != updated_range:
        raise RuntimeError('Appended publication row failed exact readback')
    receipt={'utc':datetime.now(timezone.utc).isoformat(),'confirmed':True,
             'pr':938,'problem_id':'30003634','original_pr_head':acceptance['original_pr_head'],
             'merged_head':merge['headRefOid'],'merge_commit':merge['mergeCommit']['oid'],
             'accepted_freeze_sha256':acceptance['freeze_sha256'],'zenodo_record_id':publication['id'],
             'spreadsheet_id':SID,'gid':1254632077,'tab_title':target['title'],
             'updated_range':updated_range,'doi':doi,'row':row,
             'append_result':appended,'readback_matches':True,
             'cli':'Google Workspace CLI gws',
             'original_problem_link':'Authenticated primary report DOI; catalogue URL was not authenticated'}
    save('TRACKER_RECEIPT.json',receipt)
    print(json.dumps({'doi':doi,'updated_range':updated_range,'confirmed':True},indent=2))

if __name__=='__main__':
    main()
