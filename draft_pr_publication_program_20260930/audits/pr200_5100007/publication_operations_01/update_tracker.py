"""One exact GWS append, or read-only recovery of that append. No token output."""
from pathlib import Path
from collections import Counter
import datetime,hashlib,json,os,re,subprocess,sys
A=Path(__file__).resolve().parent.parent;D=A/'private_operations/tracker';SID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20';TAB='Math Puzzles';GID=1254632077
CLI='/Users/alec/.nvm/versions/node/v22.16.0/bin/gws';ENV=dict(os.environ);ENV['PATH']=str(Path(CLI).parent)+os.pathsep+ENV.get('PATH','')
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(name,j):
 f=D/name
 with f.open('x') as out:json.dump(j,out,indent=2);out.write('\n')
 return f
def call(name,resources,params,body=None):
 cmd=[CLI,'sheets',*resources,'--params',json.dumps(params)]
 if body is not None:cmd+=['--json',json.dumps(body)]
 p=subprocess.run(cmd,capture_output=True,text=True,env=ENV);save(name,{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 if p.returncode:raise RuntimeError('GWS '+name+' failed; inspect saved redacted output before retry')
 j=json.loads(p.stdout)
 if 'error' in j:raise RuntimeError('GWS returned error '+name)
 return j
def rows(j):return [tuple(x+['']*(4-len(x))) for x in j.get('values',[]) if len(x)<=4]
def get(name,rng):return call(name,['spreadsheets','values','get'],{'spreadsheetId':SID,'range':rng,'valueRenderOption':'UNFORMATTED_VALUE'})
def main():
 if (A/'ROOT_TRACKER_RECEIPT.json').exists():raise RuntimeError('Final tracker receipt already exists; read it instead of appending')
 D.mkdir(parents=True,exist_ok=True);pub=json.loads((A/'ROOT_PUBLICATION_RECEIPT.json').read_bytes());g=json.loads((A/'ROOT_PUBLICATION_GATE_01.json').read_bytes())
 assert pub['actual_publication_verified'] and pub['metadata_exact_verified'] and pub['state']=='published' and pub['gate_sha256']==pin(A/'ROOT_PUBLICATION_GATE_01.json')['sha256'] and g['publication_ready_gate_accepted']
 doi=pub['doi'];row=['k115: outer elliptic billiard focal product (AMR-050-0007)','', 'https://doi.org/'+doi,g['metadata']['title']+'. Primitive least N>=3: phase constant iff4 divides N; all coprime star windings. Positive theorem and overlapping method credited to Ferudun DOI10.5281/zenodo.23093258. Observed Oct1PR/Oct2deposit timeline; historical firstness and independence unresolved. Converse audited Oct16. Extensive AI use; unrefereed, no conventional human peer review. PR200.']
 attempt=len(list(D.glob('sheet_meta_*.json')))+1;tag=str(attempt);meta=call('sheet_meta_'+tag+'.json',['spreadsheets','get'],{'spreadsheetId':SID,'fields':'spreadsheetId,sheets(properties(sheetId,title,gridProperties(rowCount,columnCount)))'})
 assert meta['spreadsheetId']==SID and len([s for s in meta['sheets'] if s['properties']['sheetId']==GID and s['properties']['title']==TAB])==1
 before1=get('before1_'+tag+'.json',"'Math Puzzles'!A:D");before2=get('before2_'+tag+'.json',"'Math Puzzles'!A:D");r1=rows(before1);r2=rows(before2);assert r1[0]==r2[0]==('Original Problem','Solution Chat URL','DOI','Notes')
 assert not (Counter(r1)-Counter(r2)), 'foreign rows disappeared between reads'
 matches=[i for i,r in enumerate(r2,1) if any(doi in str(x) for x in r)]
 if matches:
  assert (D/'APPEND_INFLIGHT.json').exists() and len(matches)==1 and list(r2[matches[0]-1])==row,'Unexpected duplicate DOI; no append authorized'
  rng="'Math Puzzles'!A"+str(matches[0])+':D'+str(matches[0]);recovered=True
 else:
  assert not (D/'APPEND_INFLIGHT.json').exists(),'Prior append outcome unknown; read-only reconciliation required before any retry'
  save('APPEND_INFLIGHT.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'DOI':doi,'row':row,'before2_file':'before2_'+tag+'.json','input':'RAW','insertion':'INSERT_ROWS'})
  resp=call('append_response_'+tag+'.json',['spreadsheets','values','append'],{'spreadsheetId':SID,'range':"'Math Puzzles'!A:D",'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True},{'majorDimension':'ROWS','values':[row]})
  u=resp['updates'];assert u['updatedRows']==1 and u['updatedColumns']==4 and u['updatedCells']==4;rng=u['updatedRange'];assert re.fullmatch(r"'Math Puzzles'!A(\d+):D\1",rng);recovered=False
 own=get('own_readback_'+tag+'.json',rng);assert rows(own)==[tuple(row)]
 after=get('after_'+tag+'.json',"'Math Puzzles'!A:D");ra=rows(after);hits=[r for r in ra if any(doi in str(x) for x in r)];assert hits==[tuple(row)]
 assert not (Counter(r1)-Counter(ra)) and not (Counter(r2)-Counter(ra)),'foreign rows not retained'
 receipt={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':200,'doi':doi,'spreadsheet_id':SID,'sheet_gid':GID,'range':rng,'row':row,'actual_tracker_row_verified':True,'own_row_readback_verified':True,'foreign_rows_retained':True,'two_fresh_full_prechecks':True,'RAW_INSERT_ROWS':True,'B_intentionally_blank_no_verified_chat_share_URL':True,'recovered_unknown_outcome':recovered,'gate_sha256':pub['gate_sha256'],'publication_receipt':pin(A/'ROOT_PUBLICATION_RECEIPT.json'),'private_operation_receipts':'private_operations/tracker/'}
 f=A/'ROOT_TRACKER_RECEIPT.json'
 with f.open('x') as out:json.dump(receipt,out,indent=2);out.write('\n')
 f.chmod(0o444);print(json.dumps(receipt))
if __name__=='__main__':main()
