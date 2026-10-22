"""One authorized RAW tracker append, idempotent readback after unknown outcome."""
from pathlib import Path
import datetime,json,re,subprocess,sys
A=Path(__file__).resolve().parent;D=A/'sheets_tracking';GWS='/Users/alec/.nvm/versions/node/v22.16.0/bin/gws';SID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20';TAB='Math Puzzles'
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def require(x,k):
 if not x:raise RuntimeError(k)
def call(method,params,name,body=None):
 args=[GWS,'sheets','spreadsheets','values',method,'--params',json.dumps(params)]
 if body is not None:args+=['--json',json.dumps(body)]
 r=subprocess.run(args,capture_output=True,timeout=90);(D/(name+'.stdout.json')).write_bytes(r.stdout);(D/(name+'.stderr.txt')).write_bytes(r.stderr)
 require(r.returncode==0,'GWS request failed; inspect saved result before any retry');return json.loads(r.stdout)
def run():
 D.mkdir(exist_ok=True);z=json.loads((A/'ZENODO_PUBLICATION_READBACK.json').read_text());g=json.loads((A/'ROOT_PUBLICATION_GATE.json').read_text());require(z['state']=='published' and g['status']=='READY_FOR_AUTHORIZED_PUBLICATION','Actual publication absent')
 row=["Fuchs Conjecture3.2 /5000007: bare-angle exclusion and parity-selected dodecahedral endpoint theorem",'',z['doi_url'],"A parity-selected endpoint theorem for the regular dodecahedron (PR190). Imported bare-angle exclusion is false by exactly two proper face diagonals per initial face/vertex; explicitly adopted parity-selected endpoint theorem proved. Classical AAH/Troubetzkoy symmetry and Ferudun current contemporaneous exact overlap credited. Original GitHub PR creation01Oct2026 and related DataCite DOIregistration09Oct documented with exact visibility/version/awareness limits; nofirstness, guaranteednovelty, current openness, authenticated author erratum or independence certification. Current Ferudun DOI-version files match inspected website copies; older journal-version comparisons remain incomplete. Exact optimization-safe reproduction and pinned-coordinate norm inconsistency. Extensive AI; unrefereed; no conventional human peer review."]
 full=call('get',{'spreadsheetId':SID,'range':"'Math Puzzles'!A:D",'valueRenderOption':'UNFORMATTED_VALUE'},'PREAPPEND_FRESH_READ')
 matches=[i for i,x in enumerate(full.get('values',[]),1) if any(z['doi'] in str(c) for c in x)]
 require(len(matches)<=1,'Duplicate DOI rows; reconcile without another append')
 if matches:
  idx=matches[0];require(full['values'][idx-1]==row,'Existing DOI row differs; reconcile explicitly');target=f"'Math Puzzles'!A{idx}:D{idx}"
 else:
  require(not (D/'APPEND_ATTEMPT_STARTED.json').exists(),'Earlier append outcome unconfirmed and DOI absent; no automatic second write')
  params={'spreadsheetId':SID,'range':"'Math Puzzles'!A:D",'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True};body={'majorDimension':'ROWS','values':[row]};save(D/'APPEND_REQUEST.json',{'params':params,'body':body});save(D/'APPEND_ATTEMPT_STARTED.json',{'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'DOI':z['doi'],'automatic_second_write_forbidden':True})
  result=call('append',params,'APPEND_RESPONSE',body);target=result['updates']['updatedRange'];require(re.fullmatch(r"'?Math Puzzles'?!A[0-9]+:D[0-9]+",target),'Unexpected append range');require(result['updates']['updatedRows']==1 and result['updates']['updatedColumns']==4,'Unexpected append dimensions')
 for i in [1,2]:
  actual=call('get',{'spreadsheetId':SID,'range':target,'valueRenderOption':'UNFORMATTED_VALUE'},'ROW_READBACK_'+str(i));require(actual.get('values')==[row],'Fresh actual row differs')
 out={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED','spreadsheet_id':SID,'gid':1254632077,'tab':TAB,'range':target,'DOI':z['doi'],'row':row,'actual_rows':1,'actual_fresh_reads':2};save(A/'TRACKER_ACCEPTANCE.json',out);print(json.dumps({'status':out['status'],'range':target,'DOI':z['doi']}))
if __name__=='__main__':run()
