"""Append only the verified PR909 publication, with duplicate/readback guards."""
from pathlib import Path
from datetime import datetime, timezone
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
AUDIT = Path(__file__).resolve().parent / 'audits/pr909_30001345'
SID = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'

def gws(args):
    result = subprocess.run(['gws', *args], cwd=ROOT, check=True,
                            capture_output=True, text=True)
    return json.loads(result.stdout)

def save(name, value):
    (AUDIT/name).write_text(json.dumps(value, indent=2)+'\n')

def main():
    publication = json.loads((AUDIT/'publication/ZENODO_PUBLISH.json').read_text())
    merge = json.loads((AUDIT/'PR_MERGE_RECEIPT.json').read_text())
    if publication['state'] != 'published' or merge['state'] != 'MERGED':
        raise RuntimeError('Merge and publication must be confirmed first')
    acceptance = json.loads((AUDIT/'ACCEPTANCE.json').read_text())
    if acceptance.get('accepted') is not True:
        raise RuntimeError('Exact package acceptance is required')
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
    row = [
        "https://doi.org/10.4171/OWR/2009/43", "", "https://doi.org/"+doi,
        "30001345 / OWR-4086-003, report pp. 2446–2448. "
        "Classical arrangement counterexamples to summed rough-M semicontinuity; v1.0, "
        "4-page unrefereed note and source/verification archive. PR #909 merged after independent "
        "construction, invariant, exact-computation, source and deep primary priority audits plus "
        "sequential fresh whole-package reviews. Reduced flat multibranch delta-constant fixed-ball "
        "family with finite simultaneous normalization: ordinary-nine central rough 7/delta 36, "
        "twelve nearby triples with summed rough 12/delta 36. Classical Fermat extension excess n²−4 "
        "for every n>=3. Explicitly attributed classical corollary of prior dual-Hesse picture "
        "deformation, constant-term scaling and ordinary-point formula. No construction/method novelty, "
        "firstness or current-openness claim; exact earlier publication of the rough-M observation "
        "unestablished. Only unrestricted literal summed 2009 reading, not marked-section or the "
        "explicitly unibranched 2014 parametric Conjecture 3.8. Extensive AI assistance; no independent "
        "human peer review claimed. Original recovery label 1 verified/5, earlier attempt total unknown. "
        "https://github.com/AlecKriebel/Math/pull/909"
    ]
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
    readback = gws(['sheets','spreadsheets','values','get','--params',
                    json.dumps({'spreadsheetId':SID,'range':updated_range})])
    save('TRACKER_READBACK.json',readback)
    if readback.get('values') != [row]:
        raise RuntimeError('Appended publication row failed exact readback')
    receipt={'utc':datetime.now(timezone.utc).isoformat(),'confirmed':True,
             'spreadsheet_id':SID,'gid':1254632077,'tab_title':target['title'],
             'updated_range':updated_range,'doi':doi,'row':row,
             'append_result':appended,'readback_matches':True,
             'cli':'Google Workspace CLI gws',
             'original_problem_link':'Authenticated primary report DOI; catalogue URL was not authenticated'}
    save('TRACKER_RECEIPT.json',receipt)
    print(json.dumps({'doi':doi,'updated_range':updated_range,'confirmed':True},indent=2))

if __name__=='__main__':
    main()
