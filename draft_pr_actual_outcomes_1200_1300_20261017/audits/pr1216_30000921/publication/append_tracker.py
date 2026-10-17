#!/usr/bin/env python3
"""Append this confirmed deposit once; reconcile an uncertain earlier append."""
from pathlib import Path
import datetime,json,re,subprocess
ROOT=Path(__file__).resolve().parent
SID="1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20"
GID=1254632077

def call(parts,params,body=None):
 args=["gws","sheets",*parts,"--params",json.dumps(params)]
 if body is not None:args += ["--json",json.dumps(body)]
 r=subprocess.run(args,text=True,capture_output=True,timeout=60)
 if r.returncode:raise RuntimeError(r.stderr or r.stdout)
 return json.loads(r.stdout)

def save(path,data):
 path.write_text(json.dumps(data,indent=2)+"\n")

def validate_publication_identity(pub,title):
 if type(pub.get('id')) is not int or pub['id']<=0:raise RuntimeError('Invalid production record id')
 doi='10.5281/zenodo.'+str(pub['id']);doi_url='https://doi.org/'+doi;record_url='https://zenodo.org/records/'+str(pub['id'])
 if pub.get('environment')!='production' or pub.get('state')!='published' or pub.get('metadata_normalizations')!=[]:raise RuntimeError('Confirmed exact production publication required')
 if pub.get('doi')!=doi or pub.get('doi_url')!=doi_url or pub.get('record_url')!=record_url or pub.get('url',doi_url)!=doi_url:raise RuntimeError('Noncanonical DOI/record publication links')
 if pub.get('title')!=title:raise RuntimeError('Publication title differs from reviewed metadata')
 return {'id':pub['id'],'doi':doi,'doi_url':doi_url,'record_url':record_url}

def expected_row(pub,title):
 validate_publication_identity(pub,title)
 return ["OWR-1787-006 (30000921): polynomial multiplication and differentiation hypercyclicity","",pub["doi_url"],title+"; v1.0. Historical universal preservation question answered negatively, with dense simultaneous failures for all nonconstant polynomial multipliers. Older Nikula/Bayart–Matheron Gaussian implications credited; self-contained elementary alternative proof, no new first solution/existence or current-open claim. Extensively AI-assisted, unrefereed. https://github.com/AlecKriebel/Math/pull/1216"]

def validate_tracker_receipt(receipt,pub,title):
 if receipt.get('spreadsheetId')!=SID or receipt.get('gid')!=GID or not receipt.get('readback_verified'):raise RuntimeError('Wrong or unverified tracker')
 if receipt.get('row')!=expected_row(pub,title):raise RuntimeError('Full four-cell tracker row differs')
 match=re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1",receipt.get('updatedRange',''))
 if match is None or int(match.group(1))<2:raise RuntimeError('Tracker range must be one A:D data row on Math Puzzles')
 return receipt['updatedRange']

def main():
 pub=json.loads((ROOT/"PUBLICATION_RECEIPT.json").read_text())
 title=json.loads((ROOT/"zenodo-deposit.json").read_text())["metadata"]["title"]
 validate_publication_identity(pub,title)
 metadata=call(["spreadsheets","get"],{"spreadsheetId":SID,"fields":"sheets.properties"})
 tab=next(s["properties"] for s in metadata["sheets"] if s["properties"]["sheetId"]==GID)
 if tab["title"]!="Math Puzzles":raise RuntimeError("Tracker tab title changed; reconcile before append")
 name=tab["title"].replace("'","''"); full="'"+name+"'!A:D"
 data=call(["spreadsheets","values","get"],{"spreadsheetId":SID,"range":full,"valueRenderOption":"UNFORMATTED_VALUE"})
 rows=data.get("values",[])
 if not rows or rows[0]!=["Original Problem","Solution Chat URL","DOI","Notes"]:raise RuntimeError("Unexpected tracker headers")
 row=expected_row(pub,title)
 matches=[(i+1,r) for i,r in enumerate(rows) if any(pub["doi_url"]==str(c) or "30000921" in str(c) or "1787-006" in str(c) for c in r)]
 out=ROOT/"tracker"; out.mkdir(exist_ok=True)
 intent={"spreadsheetId":SID,"gid":GID,"range":full,"row":row}
 if matches:
  if len(matches)!=1 or matches[0][1]!=row:raise RuntimeError("Existing problem/DOI row needs reconciliation; no append made")
  number=matches[0][0]; updated="'"+name+f"'!A{number}:D{number}"
  result={"recovered_existing_exact_row":True,"updatedRange":updated}
 else:
  # Record intent before the one external mutation. A lost response is recovered
  # by the exact DOI/problem search above, never by blindly appending again.
  old=out/"INTENT.json"
  if old.exists():raise RuntimeError("Earlier append intent has no exact matching row; reconcile before retrying")
  save(old,intent)
  result=call(["spreadsheets","values","append"],{"spreadsheetId":SID,"range":full,"valueInputOption":"RAW","insertDataOption":"INSERT_ROWS","includeValuesInResponse":True}, {"majorDimension":"ROWS","values":[row]})
  save(out/"APPEND_RECEIPT.json",result)
  updated=result["updates"]["updatedRange"]
  if result["updates"].get("updatedRows")!=1 or result["updates"].get("updatedColumns")!=4:raise RuntimeError("Unexpected append dimensions; inspect receipt")
 readback=call(["spreadsheets","values","get"],{"spreadsheetId":SID,"range":updated,"valueRenderOption":"UNFORMATTED_VALUE"})
 save(out/"READBACK.json",readback)
 if readback.get("values")!=[row]:raise RuntimeError("Tracker readback differs")
 summary={"at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"spreadsheetId":SID,"gid":GID,"updatedRange":updated,"row":row,"readback_verified":True,"recovered_existing_exact_row":result.get("recovered_existing_exact_row",False)}
 validate_tracker_receipt(summary,pub,title)
 save(out/"TRACKER_RECEIPT.json",summary)
 print(json.dumps(summary,indent=2))

if __name__=="__main__":main()
