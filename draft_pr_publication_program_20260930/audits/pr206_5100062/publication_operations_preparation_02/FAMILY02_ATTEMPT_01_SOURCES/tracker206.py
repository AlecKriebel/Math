"""PR206 single RAW INSERT_ROWS append or read-only recovery. No import-time action."""
import sys
sys.dont_write_bytecode=True
import argparse,collections,json,math,os,pathlib,re,shutil,subprocess
_common=sys.modules.get('ops_common206')
if _common is None:raise RuntimeError('Root authenticated-buffer loader must preload ops_common206')
globals().update({k:v for k,v in vars(_common).items() if not k.startswith('_')})
SID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
TAB='Math Puzzles'
GID=1254632077
HEADERS=('Original Problem','Solution Chat URL','DOI','Notes')
FULL_RANGE="'Math Puzzles'!A:D"
class SheetProcess:
 def __init__(self,cli=None):self.cli=cli
 def run(self,resources,params,body=None):
  cli=self.cli or '/Users/alec/.nvm/versions/node/v22.16.0/bin/gws';require(type(cli) is str and bool(cli),'Explicit known gws CLI required')
  cli=str(pathlib.Path(cli).resolve());env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env['PATH']=str(pathlib.Path(cli).parent)+os.pathsep+env.get('PATH','')
  argv=[cli,'sheets',*resources,'--params',json.dumps(params)]
  if body is not None:argv+=['--json',json.dumps(body)]
  return subprocess.run(argv,env=env,capture_output=True,text=True,check=False)
def rows(value):
 require(isinstance(value,dict) and 'error' not in value,'Invalid/error sheet response')
 raw=value.get('values',[]);require(isinstance(raw,list),'Invalid values')
 result=[]
 for row in raw:
  require(isinstance(row,list) and len(row)<=4,'Malformed/overwide row; never discard foreign rows')
  for cell in row:
   require(type(cell) in (str,int,float,bool),'Unsupported cell type')
   if isinstance(cell,float):require(math.isfinite(cell),'Nonfinite cell')
  result.append(tuple(row+['']*(4-len(row))))
 return result
def counted(rs):return collections.Counter(json.dumps(list(row),separators=(',',':'),allow_nan=False) for row in rs)
def counter_pin(rs):return digest(encoded(sorted(counted(rs).items())))
def retained(old,new):return not (counted(old)-counted(new))
def hits(rs,doi):
 p=re.compile(re.escape(doi)+r'(?![0-9])')
 return [i for i,row in enumerate(rs,1) if any(p.search(str(x)) for x in row)]
CLAIM='For a proper nested confocal ellipse pair admitting an odd primitive Poncelet billiard family, the product of the signed areas obtained by unit-circle inversion of the original orbit vertices in the two original foci is constant along each admitted family, including all coprime stars and reversal. For every integer r>=1, repeating an odd primitive cycle r times scales each signed area by r and the product by r squared.'
CREDIT='Attributed verification/research note: the historical RGK k903,a target is Table10 on page12, row k903,a dated10/20 (October2020); RGH N=3 and Conjecture1 are credited. Alper Ferudun, DOI10.5281/zenodo.23096994, treats the same target with substantially the same compact flag-curve mechanism. The RGH public-preprint delta defect is disclosed; journal full text/typography were uninspected and no general corrected RGH formula is claimed. Chavez-Caliz DOI10.1007/s40598-020-00154-8 is used. No theorem/formula/method novelty, absolute firstness, certified discovery independence, literal simultaneity or current-open status is claimed. Specified GitHub/Zenodo record dates do not certify first public availability of every byte or repository visibility history.'
EFFORT='Original submitted claimed_solved1/5 is preserved; author turns and actual model/reasoning effort remain unverified. Four Git commits are not four author turns; later audits are separate.'
def row_for(g,doi):return ['k903,a: focal inversion signed-area product (AMR-050-0062)','','https://doi.org/'+doi,g['metadata']['title']+'. '+CLAIM+' '+CREDIT+' '+EFFORT+' Extensive AI; unrefereed; no conventional human peer review. PR206.']
class Tracker:
 def __init__(self,base,transport=None):
  self.base=pathlib.Path(base).resolve();self.directory=self.base/'private_operations/tracker';self.transport=transport if transport is not None else SheetProcess()
 def call(self,name,resources,params,body=None):
  target=self.directory/name
  try:proc=self.transport.run(resources,params,body)
  except Exception as error:
   durable_json(target,dict(UTC=utc(),request=dict(resources=resources,params=params,body=body),transport_exception_type=type(error).__name__,outcome_unconfirmed=True))
   raise RuntimeError('Tracker outcome unconfirmed; preserve inflight/baseline; no retry') from None
  durable_json(target,dict(UTC=utc(),request=dict(resources=resources,params=params,body=body),exit=proc.returncode,stdout=proc.stdout,stderr=proc.stderr))
  require(proc.returncode==0,'GWS failed; inspect private receipt, never echo credentials')
  j=json.loads(proc.stdout,parse_constant=reject_constant);require(isinstance(j,dict) and 'error' not in j,'GWS API error');return j
 def get(self,name,rng):return self.call(name,['spreadsheets','values','get'],dict(spreadsheetId=SID,range=rng,valueRenderOption='UNFORMATTED_VALUE'))
 def original(self,marker,c,pubpin,doi,row):
  j=read(marker);require(j['context']==context_pin(c) and j['publication_receipt']==pubpin and j['DOI']==doi and j['row']==row,'Original append binding differs')
  require(j['spreadsheet_id']==SID and j['sheet_gid']==GID and j['headers']==list(HEADERS) and j['input']=='RAW' and j['insertion']=='INSERT_ROWS','Original append target differs')
  ref=j['original_preappend_baseline'];name=ref['file'];require(pathlib.Path(name).name==name and name.startswith('before2_'),'Unsafe baseline path')
  p=self.directory/name;require(pin(p)==ref['pin'],'Original full baseline changed');raw=read(p)
  require(raw.get('exit')==0 and raw['request']['resources']==['spreadsheets','values','get'] and raw['request']['params']==dict(spreadsheetId=SID,range=FULL_RANGE,valueRenderOption='UNFORMATTED_VALUE'),'Original baseline request/exit differs')
  rs=rows(json.loads(raw['stdout'],parse_constant=reject_constant))
  require(rs and rs[0]==HEADERS and len(rs)==ref['row_count'] and counter_pin(rs)==ref['counter_sha256'] and not hits(rs,doi),'Original baseline header/count/Counter differs')
  require(j.get('expected_range')=="'Math Puzzles'!A"+str(len(rs)+1)+':D'+str(len(rs)+1),'Original expected append range changed')
  return rs
 def run(self,recover_only=False):
  require(type(recover_only) is bool,'Recovery selector must be an actual bool')
  require(not (self.base/'ROOT_TRACKER_RECEIPT.json').exists(),'Final tracker receipt exists; never append again')
  c=load_context(self.base);pp,pub=publication_receipt(c);pubpin=pin(pp);cp=context_pin(c);doi=pub['doi'];row=row_for(c['gate'],doi)
  private_directory(self.directory);marker=self.directory/'APPEND_INFLIGHT.json';original=None
  if marker.exists():original=self.original(marker,c,pubpin,doi,row)
  elif recover_only:raise RuntimeError('Read-only recovery needs original inflight/baseline')
  tag=str(len(list(self.directory.glob('sheet_meta_*.json')))+1).zfill(4)
  meta=self.call('sheet_meta_'+tag+'.json',['spreadsheets','get'],dict(spreadsheetId=SID,fields='spreadsheetId,sheets(properties(sheetId,title,gridProperties(rowCount,columnCount)))'))
  require(meta.get('spreadsheetId')==SID,'Wrong spreadsheet')
  match=[x['properties'] for x in meta.get('sheets',[]) if type(x['properties'].get('sheetId')) is int and x['properties'].get('sheetId')==GID]
  require(len(match)==1 and match[0].get('title')==TAB and type(match[0].get('gridProperties',{}).get('columnCount')) is int and match[0]['gridProperties']['columnCount']>=4,'Wrong gid/tab/grid')
  r1=rows(self.get('before1_'+tag+'.json',FULL_RANGE));r2=rows(self.get('before2_'+tag+'.json',FULL_RANGE))
  require(r1 and r2 and r1[0]==r2[0]==HEADERS,'Four exact headers required')
  require(retained(r1,r2),'Foreign rows disappeared between fresh reads');found=hits(r2,doi)
  if found:
   require(marker.exists() and len(found)==1 and list(r2[found[0]-1])==row,'Unexpected/duplicate DOI; no append')
   require(original is not None and retained(original,r2),'Original preappend foreign rows missing')
   rng="'Math Puzzles'!A"+str(found[0])+':D'+str(found[0]);require(rng==read(marker)['expected_range'],'Recovered row differs from original expected append range');recovered=True
  else:
   require(not marker.exists() and not recover_only,'Original append outcome unknown; read-only recovery only')
   baseline=self.directory/('before2_'+tag+'.json')
   durable_json(marker,dict(UTC=utc(),context=cp,publication_receipt=pubpin,DOI=doi,row=row,spreadsheet_id=SID,sheet_gid=GID,headers=list(HEADERS),original_preappend_baseline=dict(file=baseline.name,pin=pin(baseline),row_count=len(r2),counter_sha256=counter_pin(r2)),input='RAW',insertion='INSERT_ROWS',expected_range="'Math Puzzles'!A"+str(len(r2)+1)+':D'+str(len(r2)+1),mutation_not_yet_launched=True,semantics='Exclusive file+directory fsynced before append; original full baseline/Counter retained; no second append after uncertainty.'))
   original=self.original(marker,c,pubpin,doi,row);same_context(self.base,cp);require(pin(pp)==pubpin,'Publication receipt changed before append')
   response=self.call('append_response_'+tag+'.json',['spreadsheets','values','append'],dict(spreadsheetId=SID,range=FULL_RANGE,valueInputOption='RAW',insertDataOption='INSERT_ROWS',includeValuesInResponse=True),dict(majorDimension='ROWS',values=[row]))
   require(response.get('spreadsheetId')==SID,'Append response spreadsheet differs');u=response['updates'];require(all(type(u.get(k)) is int for k in ('updatedRows','updatedColumns','updatedCells')) and u['updatedRows']==1 and u['updatedColumns']==4 and u['updatedCells']==4,'Append counts differ')
   rng=u['updatedRange'];require(rng==read(marker)['expected_range'],'Appended row differs from original dynamic expected range');require(rows(u.get('updatedData',{}))==[tuple(row)],'Append response values differ');require(bool(re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1",rng)),'Unexpected appended range');recovered=False
  require(rows(self.get('own_readback_'+tag+'.json',rng))==[tuple(row)],'Own row differs')
  after=rows(self.get('after_'+tag+'.json',FULL_RANGE));found=hits(after,doi)
  require(len(found)==1 and after[found[0]-1]==tuple(row),'DOI row not unique/exact')
  require(rng=="'Math Puzzles'!A"+str(found[0])+':D'+str(found[0]),'DOI row shifted after own readback; readonly reconciliation required')
  require(retained(r1,after) and retained(r2,after) and original is not None and retained(original,after),'Foreign rows lost, including original full baseline')
  after2=rows(self.get('after2_'+tag+'.json',FULL_RANGE));found2=hits(after2,doi)
  require(len(found2)==1 and after2[found2[0]-1]==tuple(row) and found2==found and rng=="'Math Puzzles'!A"+str(found2[0])+':D'+str(found2[0]),'Second independent fresh full readback differs')
  require(retained(after,after2) and retained(r1,after2) and retained(r2,after2) and retained(original,after2),'Foreign rows lost in second full readback')
  same_context(self.base,cp);require(pin(pp)==pubpin,'Publication receipt changed during verification')
  result=dict(schema='pr206-root-tracker-receipt-v1',evidence_scope='ACTUAL_ROOT_RECEIPT',UTC=utc(),PR=PR,doi=doi,spreadsheet_id=SID,sheet_gid=GID,range=rng,row=row,actual_tracker_row_verified=True,own_row_readback_verified=True,foreign_rows_retained=True,original_preappend_baseline_retained=True,original_preappend_baseline=read(marker)['original_preappend_baseline'],two_fresh_full_prechecks=True,two_fresh_full_readbacks=True,readback_receipts={name:pin(self.directory/(name+'_'+tag+'.json')) for name in ['own_readback','after','after2']},append_attempt_record=pin(marker),append_response_receipts={x.name:pin(x) for x in self.directory.glob('append_response_*.json')},publication_facts={k:pub[k] for k in ['id','doi','doi_url','record_url','metadata','package','package_safe_files','intended_upload_files','original_head','problem_id']},RAW_INSERT_ROWS=True,B_intentionally_blank_no_verified_chat_share_URL=True,recovered_unknown_outcome=recovered,gate_sha256=c['gate_pin']['sha256'],publication_receipt=pubpin,context=cp,private_operation_receipts='private_operations/tracker/')
  durable_json(self.base/'ROOT_TRACKER_RECEIPT.json',result,readonly=True);return result
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['append','recover']);p.add_argument('--base',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent.parent);p.add_argument('--gws');p.add_argument('--adoption',required=True);p.add_argument('--adoption-bytes',required=True,type=int);p.add_argument('--adoption-sha256',required=True);a=p.parse_args()
 configure_authority(a.adoption,dict(bytes=a.adoption_bytes,sha256=a.adoption_sha256))
 print(json.dumps(Tracker(a.base,SheetProcess(a.gws)).run(a.mode=='recover'),sort_keys=True))
if __name__=='__main__':raise RuntimeError('Live operations require the Root authenticated-buffer dispatcher; direct script execution refused')
