"""Append only the verified PR908 publication, with duplicate/readback guards."""
from pathlib import Path
from datetime import datetime, timezone
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
AUDIT = Path(__file__).resolve().parent / 'audits/pr908_30006191'
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
        "https://doi.org/10.4171/owr/2025/7", "", "https://doi.org/"+doi,
        "30006191 / OWR-14299085-005, report p.371; pointwise operator-norm topology p.365. "
        "Maximal norm discontinuity for a bounded-region continuum fermion interaction; v1.0, "
        "5-page research note and source/verification archive. PR #908 merged after independent "
        "mathematical, source/model, computational and primary priority audits plus sequential fresh "
        "whole-package reviews. Explicit d3 fixed smooth potential/region/mode; both unsmeared "
        "orderings; changing Slaters give vector/operator norm2 and state value4. Every fixed "
        "vector/normal state remains continuous. Prior Siebert arxiv2609.34402v1 cluster/phase "
        "mechanism and direct qualitative cutoff adaptation credited; audit-time energy bootstrap "
        "also recovers maximal cutoff limit, not attributed as a stated prior theorem. First priority, "
        "quantitative novelty and continued openness not asserted; bounded coverage gaps disclosed. "
        "Extensive AI assistance; unrefereed, no independent human peer review claimed. "
        "https://github.com/AlecKriebel/Math/pull/908"
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
