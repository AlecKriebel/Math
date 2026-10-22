"""PR204 single RAW INSERT_ROWS append or read-only recovery. No import-time action."""
import sys
sys.dont_write_bytecode=True
import argparse,collections,json,math,os,pathlib,re,shutil,subprocess
from operations_common import *
SID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
TAB='Math Puzzles'
GID=1254632077
HEADERS=('Original Problem','Solution Chat URL','DOI','Notes')
FULL_RANGE="'Math Puzzles'!A:D"
class SheetProcess:
 def __init__(self,cli=None):self.cli=cli
 def run(self,resources,params,body=None):
  cli=self.cli or shutil.which('gws');require(cli,'Normal-user gws not found')
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
 p=re.compile(r'(?<![A-Za-z0-9])'+re.escape(doi)+r'(?![0-9])')
 return [i for i,row in enumerate(rs,1) if any(p.search(str(x)) for x in row)]
def row_for(g,doi):
 notes=(g['metadata']['title']+'. Signed original area times origin pedal to complete original sidelines; a>b>0,0<lambda<b^2,proper confocal ellipse,least N odd or divisible by4,coprime stars/reversal. '
 'Ferudun DOI10.5281/zenodo.23085904 gives the exact theorem/dn-trace identity; DOI10.5281/zenodo.23400541 supplies the credited adjacent-foot method. '
 'Source Table3 does not literally state least period; doubled-six/listed-twelve counterexample protects that qualification. '
 'PR204 and the exact centered record both show October1 object dates,which establish neither firstness,independence nor simultaneity. '
 'No novelty claim. Extensive AI;unrefereed,no conventional human peer review. PR204.')
 return ['k203b: centered original-side pedal-area product (AMR-050-0012)','', 'https://doi.org/'+doi,notes]
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
  return rs
 def run(self,recover_only=False):
  require(not (self.base/'ROOT_TRACKER_RECEIPT.json').exists(),'Final tracker receipt exists; never append again')
  c=load_context(self.base);pp,pub=publication_receipt(c);pubpin=pin(pp);cp=context_pin(c);doi=pub['doi'];row=row_for(c['gate'],doi)
  private_directory(self.directory);marker=self.directory/'APPEND_INFLIGHT.json';original=None
  if marker.exists():original=self.original(marker,c,pubpin,doi,row)
  elif recover_only:raise RuntimeError('Read-only recovery needs original inflight/baseline')
  tag=str(len(list(self.directory.glob('sheet_meta_*.json')))+1).zfill(4)
  meta=self.call('sheet_meta_'+tag+'.json',['spreadsheets','get'],dict(spreadsheetId=SID,fields='spreadsheetId,sheets(properties(sheetId,title,gridProperties(rowCount,columnCount)))'))
  require(meta.get('spreadsheetId')==SID,'Wrong spreadsheet')
  match=[x['properties'] for x in meta.get('sheets',[]) if x['properties'].get('sheetId')==GID]
  require(len(match)==1 and match[0].get('title')==TAB and match[0].get('gridProperties',{}).get('columnCount',0)>=4,'Wrong gid/tab/grid')
  r1=rows(self.get('before1_'+tag+'.json',FULL_RANGE));r2=rows(self.get('before2_'+tag+'.json',FULL_RANGE))
  require(r1 and r2 and r1[0]==r2[0]==HEADERS,'Four exact headers required')
  require(retained(r1,r2),'Foreign rows disappeared between fresh reads');found=hits(r2,doi)
  if found:
   require(marker.exists() and len(found)==1 and list(r2[found[0]-1])==row,'Unexpected/duplicate DOI; no append')
   require(original is not None and retained(original,r2),'Original preappend foreign rows missing')
   rng="'Math Puzzles'!A"+str(found[0])+':D'+str(found[0]);recovered=True
  else:
   require(not marker.exists() and not recover_only,'Original append outcome unknown; read-only recovery only')
   baseline=self.directory/('before2_'+tag+'.json')
   durable_json(marker,dict(UTC=utc(),context=cp,publication_receipt=pubpin,DOI=doi,row=row,spreadsheet_id=SID,sheet_gid=GID,headers=list(HEADERS),original_preappend_baseline=dict(file=baseline.name,pin=pin(baseline),row_count=len(r2),counter_sha256=counter_pin(r2)),input='RAW',insertion='INSERT_ROWS',mutation_not_yet_launched=True,semantics='Exclusive file+directory fsynced before append; original full baseline/Counter retained; no second append after uncertainty.'))
   original=self.original(marker,c,pubpin,doi,row);same_context(self.base,cp);require(pin(pp)==pubpin,'Publication receipt changed before append')
   response=self.call('append_response_'+tag+'.json',['spreadsheets','values','append'],dict(spreadsheetId=SID,range=FULL_RANGE,valueInputOption='RAW',insertDataOption='INSERT_ROWS',includeValuesInResponse=True),dict(majorDimension='ROWS',values=[row]))
   u=response['updates'];require(all(type(u.get(k)) is int for k in ('updatedRows','updatedColumns','updatedCells')) and u['updatedRows']==1 and u['updatedColumns']==4 and u['updatedCells']==4,'Append counts differ')
   rng=u['updatedRange'];require(re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1",rng),'Unexpected appended range');recovered=False
  require(rows(self.get('own_readback_'+tag+'.json',rng))==[tuple(row)],'Own row differs')
  after=rows(self.get('after_'+tag+'.json',FULL_RANGE));found=hits(after,doi)
  require(len(found)==1 and after[found[0]-1]==tuple(row),'DOI row not unique/exact')
  require(retained(r1,after) and retained(r2,after) and original is not None and retained(original,after),'Foreign rows lost, including original full baseline')
  same_context(self.base,cp);require(pin(pp)==pubpin,'Publication receipt changed during verification')
  result=dict(UTC=utc(),PR=PR,doi=doi,spreadsheet_id=SID,sheet_gid=GID,range=rng,row=row,actual_tracker_row_verified=True,own_row_readback_verified=True,foreign_rows_retained=True,original_preappend_baseline_retained=True,original_preappend_baseline=read(marker)['original_preappend_baseline'],two_fresh_full_prechecks=True,RAW_INSERT_ROWS=True,B_intentionally_blank_no_verified_chat_share_URL=True,recovered_unknown_outcome=recovered,gate_sha256=c['gate_pin']['sha256'],publication_receipt=pubpin,context=cp,private_operation_receipts='private_operations/tracker/')
  durable_json(self.base/'ROOT_TRACKER_RECEIPT.json',result,readonly=True);return result
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['append','recover']);p.add_argument('--base',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent.parent);p.add_argument('--gws');a=p.parse_args()
 print(json.dumps(Tracker(a.base,SheetProcess(a.gws)).run(a.mode=='recover'),sort_keys=True))
if __name__=='__main__':main()
