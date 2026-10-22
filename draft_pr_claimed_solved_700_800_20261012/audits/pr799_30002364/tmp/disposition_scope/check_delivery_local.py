"""Local-only administrative identity check of the nine final published PDFs.

Does not re-review their scientific claims, access external services, or mutate
artifacts, production records, native state or the spreadsheet.
"""
from pathlib import Path
import hashlib,json,datetime
W=Path(__file__).resolve().parent;T=W.parent;R=Path('/Users/alec/Documents/Math');D=R/'draft_pr_claimed_solved_700_800_20261012'
EXPECTED=[718,742,764,765,778,781,786,788,789]
def need(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 root=json.loads((T/'root-receipts/ROOT_FINAL_DELIVERY.json').read_text());sheet=json.loads((T/'root-receipts/FINAL_SHEET_READBACK.json').read_text())
 rows=root['nine_exact_published_PDF_deliverables'];need(root['result']=='PASS' and [r['pr'] for r in rows]==EXPECTED,'Nine final published PDFs')
 need(root['new_sheet_writes']==0 and root['new_deposits_or_republications']==0,'No new production operations')
 restoration={r['pr']:r for r in json.loads((D/'final_delivery/RESTORATION_RECEIPT.json').read_text())['papers']}
 meta=json.loads((W/'FINAL_METADATA_CAPTURES.json').read_text());latest={r['number']:r for batch in meta['after'] for r in batch['response'].values()}
 values=sheet['valueRanges'];need(len(values)==9 and sheet['spreadsheetId']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','Fresh nine-range readback identity')
 total=0
 for row,v in zip(rows,values):
  p=R/row['path'];need(p.is_file() and not p.is_symlink(),'Regular final PDF');b=p.read_bytes();need(b.startswith(b'%PDF-') and len(b)==row['bytes'] and sha(b)==row['sha256'],'Final PDF exact bytes')
  need(latest[row['pr']]['merged'] is True and latest[row['pr']]['mergeCommit']['oid']==row['merge_commit'],'Final delivery binding to fresh merged metadata')
  if row['pr'] in restoration:
   old=restoration[row['pr']];need(all(old[k]==row[k] for k in ['problem','doi','bytes','sha256','native_acceptance_sha256']),'Original restored PDF/publication/native binding')
  else:
   a=D/'audits/pr789_30001478/tmp/FINAL_READINESS.json';gate=json.loads(a.read_text());f=[r for r in gate['publication_files'] if r['path'].endswith('.pdf')];need(len(f)==1 and f[0]['bytes']==row['bytes'] and f[0]['sha256']==row['sha256'],'PR789 original frozen PDF identity')
  need(v['range']==row['tracker_range'] and v.get('majorDimension')=='ROWS' and len(v.get('values',[]))==1 and len(v['values'][0])==4,'Four-cell tracker range')
  a,bcell,c,description=v['values'][0];need(a=='https://www.unsolvedmath.com/problems/'+row['problem'] and bcell=='' and c=='https://doi.org/'+row['doi'],'Tracker problem/blankB/DOI identity')
  need('Alec Kriebel' in description and 'unrefereed' in description and 'Extensive AI use' in description and '/pull/'+str(row['pr']) in description,'Tracker authorship and audit disclosures')
  need(row['source_verification_archive_bound'] is True and row['production_and_tracker_receipts_match_frozen_native_bindings'] is True,'Root reviewed immutable source/publication/tracker crossbinding result')
  total+=len(b)
 need(total==638324==root['total_PDF_bytes'],'Exact nine-PDF total')
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','local_PDFs_independently_hashed':9,'total_PDF_bytes':total,'old8_restoration_native_acceptance_bindings_agree':True,'PR789_frozen_readiness_PDF_binding_agrees':True,'fresh_all9_merged_metadata_bindings_agree':True,'fresh_sheet_readback36cells_problem_DOI_and_disclosures_consistent':True,'original_append_and_production_receipt_SHA_bindings_reviewed_in_root_recipe_not_independently_refetched':True,'root_delivery_receipt_sha256':sha((T/'root-receipts/ROOT_FINAL_DELIVERY.json').read_bytes()),'root_sheet_readback_sha256':sha((T/'root-receipts/FINAL_SHEET_READBACK.json').read_bytes()),'new_external_calls':0,'new_external_mutations':0,'new_mathematical_reviews':0}
 (W/'DELIVERY_LOCAL_READBACK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
