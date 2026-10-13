#!/usr/bin/env python3
"""Append this confirmed DOI through GWS, with duplicate/read-back safeguards."""
import argparse,datetime,json,pathlib,subprocess
A=pathlib.Path(__file__).resolve().parent
ID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
TAB='Math Puzzles'
def call(resource,method,params,body=None):
    cmd=['gws','sheets',*resource.split('.'),method,'--params',json.dumps(params)]
    if body is not None:cmd+=['--json',json.dumps(body,ensure_ascii=False)]
    result=subprocess.run(cmd,check=True,capture_output=True,text=True)
    return json.loads(result.stdout)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--doi',required=True);ap.add_argument('--apply',action='store_true');args=ap.parse_args()
    assert args.doi.startswith('10.5281/zenodo.') and args.doi.removeprefix('10.5281/zenodo.').isdigit()
    info=call('spreadsheets','get',{'spreadsheetId':ID,'fields':'sheets(properties(sheetId,title))'})
    assert any(s['properties']=={'sheetId':1254632077,'title':TAB} for s in info['sheets'])
    headers=call('spreadsheets.values','get',{'spreadsheetId':ID,'range':TAB+'!A1:D1'})['values']
    assert headers==[['Original Problem','Solution Chat URL','DOI','Notes']]
    doi_url='https://doi.org/'+args.doi
    row=['https://www.unsolvedmath.com/problems/30004609','',doi_url,
         "A relation-incidence proof of Tohăneanu's low-exponent supersolvability conjecture. Full characteristic-zero result, including all ranks, products and nonessential arrangements; five-page note and exact verification package. Extensively AI-assisted; unrefereed, no independent human peer review. Credits earlier methods and Ferudun's matching October 12 preprint; no exhaustive first-priority claim. PR #618: https://github.com/AlecKriebel/Math/pull/618"]
    values=call('spreadsheets.values','get',{'spreadsheetId':ID,'range':TAB+'!A:D'}).get('values',[])
    matches=[i+1 for i,r in enumerate(values) if len(r)>2 and r[2] in {args.doi,doi_url}]
    assert len(matches)<=1,'duplicate DOI already present; reconcile without another append'
    ready={'prepared_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'spreadsheet_id':ID,'sheet_id':1254632077,'row':row,'existing_rows':matches,'applied':False}
    (A/'TRACKER_ROW_READY.json').write_text(json.dumps(ready,indent=2,ensure_ascii=False)+'\n')
    if matches:
        actual=(values[matches[0]-1]+['']*4)[:4]
        assert actual==row,'existing DOI row differs; no duplicate append'
        receipt=ready|{'applied':True,'already_present':True,'updated_range':f"'{TAB}'!A{matches[0]}:D{matches[0]}"}
    elif args.apply:
        # Do not automatically repeat an ambiguous POST: inspect the sheet first.
        try:
            response=call('spreadsheets.values','append',{'spreadsheetId':ID,'range':TAB+'!A:D','valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True},{'majorDimension':'ROWS','values':[row]})
        except Exception:
            (A/'TRACKER_UNCONFIRMED.json').write_text(json.dumps(ready|{'action_outcome':'unconfirmed; read sheet before any retry'},indent=2)+'\n')
            raise
        target=response['updates']['updatedRange']
        assert response['updates']['updatedRows']==1 and response['updates']['updatedColumns']==4
        actual=call('spreadsheets.values','get',{'spreadsheetId':ID,'range':target})['values']
        assert actual==[row],'post-write read-back mismatch'
        receipt=ready|{'applied':True,'already_present':False,'updated_range':target,'append_response':response,'read_back':actual}
    else:
        print(json.dumps(ready,indent=2,ensure_ascii=False));return
    receipt['confirmed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (A/'TRACKER_RECEIPT.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'applied':receipt['applied'],'updated_range':receipt['updated_range'],'doi':args.doi,'duplicate_append':False},indent=2))
if __name__=='__main__':main()
