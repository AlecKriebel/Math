#!/usr/bin/env python3
"""Append this confirmed deposit once; reconcile an uncertain earlier append."""
from pathlib import Path
import datetime,json,subprocess
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

def main():
 pub=json.loads((ROOT/"PUBLICATION_RECEIPT.json").read_text())
 if pub.get("state")!="published" or not pub.get("doi_url"):raise RuntimeError("Confirmed publication required")
 metadata=call(["spreadsheets","get"],{"spreadsheetId":SID,"fields":"sheets.properties"})
 tab=next(s["properties"] for s in metadata["sheets"] if s["properties"]["sheetId"]==GID)
 name=tab["title"].replace("'","''"); full="'"+name+"'!A:D"
 data=call(["spreadsheets","values","get"],{"spreadsheetId":SID,"range":full,"valueRenderOption":"UNFORMATTED_VALUE"})
 rows=data.get("values",[])
 if not rows or rows[0]!=["Original Problem","Solution Chat URL","DOI","Notes"]:raise RuntimeError("Unexpected tracker headers")
 title=json.loads((ROOT/"zenodo-deposit.json").read_text())["metadata"]["title"]
 row=["OWR-1189-008 (30000418): tree L(2,1) arbitrary-list equality","",pub["doi_url"],title+"; v1.0. Historical tree equality refuted: ordinary palette5/span4, arbitrary-list number6. Known upper bound and earlier cyclic Fiala–Škrekovski2001 example credited; historical priority and current openness unestablished. Extensively AI-assisted, unrefereed. https://github.com/AlecKriebel/Math/pull/1211"]
 matches=[(i+1,r) for i,r in enumerate(rows) if any(pub["doi_url"]==str(c) or "30000418" in str(c) or "1189-008" in str(c) for c in r)]
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
 save(out/"TRACKER_RECEIPT.json",summary)
 print(json.dumps(summary,indent=2))

if __name__=="__main__":main()
