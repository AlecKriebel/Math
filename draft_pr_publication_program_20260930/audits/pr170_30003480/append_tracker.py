#!/usr/bin/env python3
"""Append only this accepted published paper, with live headers and readbacks."""
from pathlib import Path
import datetime,json,subprocess
A=Path(__file__).resolve().parent
GWS="/Users/alec/.nvm/versions/node/v22.16.0/bin/gws"
SHEET="1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20"
GID=1254632077
HEADERS=["Original Problem","Solution Chat URL","DOI","Notes"]
def require(c,m):
    if not c: raise RuntimeError(m)
def cli(method,params,body=None):
    args=[GWS,"sheets","spreadsheets",*method,"--params",json.dumps(params)]
    if body is not None: args+=["--json",json.dumps(body)]
    r=subprocess.run(args,capture_output=True,text=True,timeout=90)
    require(r.returncode==0,r.stderr[:900])
    return json.loads(r.stdout)
def save(p,j): p.write_text(json.dumps(j,indent=2)+"\n")
def read(range_):
    return cli(["values","get"],{"spreadsheetId":SHEET,"range":range_})
def main():
    pub=json.loads((A/"ZENODO_PUBLICATION_READBACK.json").read_text())
    gate=json.loads((A/"ROOT_PUBLICATION_GATE.json").read_text())
    require(pub["state"]=="published" and gate["status"]=="READY_FOR_AUTHORIZED_PUBLICATION" and gate["fresh_seal_first_review_clean"],"Actual accepted publication and clean final fresh review required")
    require(pub["title"]=="No single polynomial inequality defines a real binary Gram locus","Unexpected paper")
    d=A/"sheets_tracking";d.mkdir(exist_ok=True)
    private=d/"private";private.mkdir(exist_ok=True)
    meta=cli(["get"],{"spreadsheetId":SHEET,"fields":"sheets.properties"})
    tabs=[x["properties"]["title"] for x in meta["sheets"] if x["properties"]["sheetId"]==GID]
    require(len(tabs)==1,"Target GID unavailable")
    tab="'"+tabs[0].replace("'","''")+"'"
    require(read(tab+"!A1:D1").get("values")==[HEADERS],"Tracker headers changed")
    note=("No single polynomial inequality defines a real binary Gram locus — Alec Kriebel, v1.0.0 (2026-10-12 UTC). "
          "PR170; 30003480; Seigal OWR20/2017 and LAA544(2018) Conjecture1.5. "
          "Full negative resolution in the original closed Frobenius unit-ball domain: for every n>=3 no single "
          "real determinant-only polynomial inequality defines the Gram locus inside its cube or convex hull. "
          "Higher-n proof uses exact zero-determinant faces; positive n4 rational witness refutes the proposed formula. "
          "Established marginal polygon criteria, real constructions and general boundary multiplicity principles credited. "
          "Original September30 GitHub PR creation13:15:23UTC precedes Ferudun October2 exact overlapping stronger "
          "positive-interior theorem DOI10.5281/zenodo.23111048 (record creation20:58:52.851621UTC). "
          "Contemporaneous separate disclosures; no exclusive priority, literal simultaneity, mutual-independence "
          "or archived historical public-visibility certificate. Formal preprint not backdated; bounded source access limits disclosed. "
          "Exact PDF/source/support archive,46274 rational finite controls per baseline, ordinary and optimized outputs identical, "
          "eight deliberately false variants rejected. Universal theorem rests on the written proof, not finite sampling. "
          "Initial full-package review's accidental preseal-summary exposure is explicitly qualified; its two evidence/presentation "
          "issues repaired globally and a new direct-input seal-first whole-package review cleared the final package. "
          "Extensive AI assistance; unrefereed and no conventional human peer review.")
    row=["https://doi.org/10.4171/OWR/2017/20","",pub["doi_url"],note]
    before=read(tab+"!C:C")
    save(private/"DOI_COLUMN_BEFORE.json",before)
    matches=[i+1 for i,x in enumerate(before.get("values",[])) if x and x[0]==pub["doi_url"]]
    require(len(matches)<=1,"Duplicate own DOI already exists")
    request={"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),
             "params":{"spreadsheetId":SHEET,"range":tab+"!A:D","valueInputOption":"RAW",
                       "insertDataOption":"INSERT_ROWS","includeValuesInResponse":True},
             "body":{"majorDimension":"ROWS","values":[row]},
             "target_gid_verified":GID,"actual_headers":HEADERS,"DOI_duplicate_matches":len(matches)}
    append_requests=0
    if matches:
        range_=tab+"!A"+str(matches[0])+":D"+str(matches[0])
        require(read(range_).get("values")==[row],"Existing own DOI row differs; inspect before writing")
    else:
        require(not (d/"APPEND_REQUEST.json").exists(),"Prior append outcome must be inspected before a second write")
        save(d/"APPEND_REQUEST.json",request)
        response=cli(["values","append"],request["params"],request["body"])
        save(d/"APPEND_RESPONSE.json",response)
        range_=response["updates"]["updatedRange"]
        require(response["updates"]["updatedData"].get("values")==[row],"Returned appended values differ")
        append_requests=1
    fresh=read(range_);save(d/"ROW_READBACK.json",fresh)
    require(fresh.get("values")==[row],"Exact row readback differs")
    after=read(tab+"!C:C");save(private/"DOI_COLUMN_AFTER.json",after)
    matches_after=[i+1 for i,x in enumerate(after.get("values",[])) if x and x[0]==pub["doi_url"]]
    require(len(matches_after)==1,"Own DOI does not occur exactly once after readback")
    result={"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status":"TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED","spreadsheet_id":SHEET,
            "sheet_gid":GID,"range":range_,"PR":170,"DOI":pub["doi"],"actual_headers":HEADERS,
            "row_values":row,"append_returned_values_match":True,"exact_row_readback_match":True,
            "second_fresh_DOI_column_readback_matches":matches_after,"DOI_count":1,
            "append_requests":append_requests,"CLI":"Google Workspace CLI",
            "unrelated_sheet_response_bodies_excluded_from_public_files":True,"title":pub["title"]}
    save(A/"TRACKER_ACCEPTANCE.json",result)
    print(json.dumps({k:result[k] for k in ["status","range","DOI","DOI_count","append_requests"]}))
if __name__=="__main__":main()
