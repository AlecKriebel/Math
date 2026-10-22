#!/usr/bin/env python3
"""Append this confirmed deposit once; reconcile an uncertain earlier append."""
from pathlib import Path
import datetime,json,re,subprocess,runpy
ROOT=Path(__file__).resolve().parent
SID="1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20"
GID=1254632077
PROBLEM_IDENTIFIERS=('2307072','https://github.com/aleckriebel/math/pull/1274')
# The original problem uses AMR-022-7072; accept its common separator and
# group-zero-padding variants, but never the prefix of a longer alias.
AMR_ALIAS=re.compile(r'(?<![a-z0-9])amr[\s_-]*0*22[\s_-]*0*7072(?![a-z0-9])',re.IGNORECASE)

def row_has_problem_identity(row,publication=None):
 """Known problem aliases at every stage; DOI forms when publication is known."""
 if not isinstance(row,list):raise RuntimeError('Tracker row must be a cell array')
 dois={publication['doi'].casefold(),publication['doi_url'].casefold()} if publication is not None else set()
 return any(any(token in str(cell).casefold() for token in PROBLEM_IDENTIFIERS) or AMR_ALIAS.search(str(cell)) is not None or str(cell).strip().casefold() in dois for cell in row)

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
 context=runpy.run_path(str(ROOT/'prepare_package.py'))['load_context']()
 if context['title']!=title:raise RuntimeError('Tracker title differs from explicit current context')
 return [context['tracker']['original_problem'],"",pub["doi_url"],title+"; v1.0. "+context['tracker']['notes']+" No firstness/current-openness claim. Extensively AI-assisted, unrefereed. https://github.com/AlecKriebel/Math/pull/1274"]


def validate_tracker_receipt(receipt,pub,title):
 if receipt.get('spreadsheetId')!=SID or receipt.get('gid')!=GID or not receipt.get('readback_verified'):raise RuntimeError('Wrong or unverified tracker')
 if receipt.get('row')!=expected_row(pub,title):raise RuntimeError('Full four-cell tracker row differs')
 match=re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1",receipt.get('updatedRange',''))
 if match is None or int(match.group(1))<2:raise RuntimeError('Tracker range must be one A:D data row on Math Puzzles')
 return receipt['updatedRange']

def main():
 runpy.run_path(str(ROOT/'update_pr_publication.py'))['validate_workflow_gate'](json.loads((ROOT/'FINAL_REVIEW_GATE.json').read_text()))
 pub=json.loads((ROOT/"PUBLICATION_RECEIPT.json").read_text())
 title=json.loads((ROOT/"zenodo-deposit.json").read_text())["metadata"]["title"]
 validate_publication_identity(pub,title)
 metadata=call(["spreadsheets","get"],{"spreadsheetId":SID,"fields":"sheets.properties"})
 tabs=[s['properties'] for s in metadata.get('sheets',[]) if s.get('properties',{}).get('sheetId')==GID]
 if len(tabs)!=1 or tabs[0].get('title')!='Math Puzzles':raise RuntimeError('Tracker designated ID/title changed; reconcile before append')
 tab=tabs[0]
 name=tab["title"].replace("'","''"); full="'"+name+"'!A:D"
 data=call(["spreadsheets","values","get"],{"spreadsheetId":SID,"range":full,"valueRenderOption":"UNFORMATTED_VALUE"})
 rows=data.get("values",[])
 if not rows or rows[0]!=["Original Problem","Solution Chat URL","DOI","Notes"]:raise RuntimeError("Unexpected tracker headers")
 row=expected_row(pub,title)
 matches=[(i+1,r) for i,r in enumerate(rows) if row_has_problem_identity(r,pub)]
 out=ROOT/"tracker"; out.mkdir(exist_ok=True)
 intent={"spreadsheetId":SID,"gid":GID,"range":full,"row":row}
 old=out/"INTENT.json"
 if old.exists() and json.loads(old.read_text())!=intent:raise RuntimeError('Earlier append intent differs from current full row')
 if matches:
  if len(matches)!=1 or matches[0][1]!=row:raise RuntimeError("Existing problem/DOI row needs reconciliation; no append made")
  number=matches[0][0]; updated="'"+name+f"'!A{number}:D{number}"
  result={"recovered_existing_exact_row":True,"updatedRange":updated}
 else:
  # Record intent before the one external mutation. A lost response is recovered
  # by the exact DOI/problem search above, never by blindly appending again.
  if old.exists():raise RuntimeError("Earlier append intent has no exact matching row; reconcile before retrying")
  try:
   with old.open('x') as stream:stream.write(json.dumps(intent,indent=2)+'\n')
  except FileExistsError:raise RuntimeError('Concurrent/earlier append intent exists; reconcile read-only')
  result=call(["spreadsheets","values","append"],{"spreadsheetId":SID,"range":full,"valueInputOption":"RAW","insertDataOption":"INSERT_ROWS","includeValuesInResponse":True}, {"majorDimension":"ROWS","values":[row]})
  save(out/"APPEND_RECEIPT.json",result)
  updated=result["updates"]["updatedRange"]
  if result["updates"].get("updatedRows")!=1 or result["updates"].get("updatedColumns")!=4:raise RuntimeError("Unexpected append dimensions; inspect receipt")
 if re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1",updated) is None or int(re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1",updated).group(1))<2:raise RuntimeError('Append returned noncanonical data-row range')
 readback=call(["spreadsheets","values","get"],{"spreadsheetId":SID,"range":updated,"valueRenderOption":"UNFORMATTED_VALUE"})
 save(out/"READBACK.json",readback)
 if readback.get("values")!=[row]:raise RuntimeError("Tracker readback differs")
 summary={"at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"spreadsheetId":SID,"gid":GID,"updatedRange":updated,"row":row,"readback_verified":True,"recovered_existing_exact_row":result.get("recovered_existing_exact_row",False)}
 validate_tracker_receipt(summary,pub,title)
 save(out/"TRACKER_RECEIPT.json",summary)
 print(json.dumps(summary,indent=2))

if __name__=="__main__":main()
