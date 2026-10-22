from pathlib import Path,PurePosixPath
import ast,copy,json,hashlib,datetime as dt,argparse,io,uuid,zipfile,contextlib,sys,types
from urllib.parse import quote
home=Path(__file__).resolve().parent
# Load only actual production definitions, with every provider call replaced by local fixtures.
source=home/'bound_ops/verify_published_files.py';tree=ast.parse(source.read_text());env={'Path':Path,'PurePosixPath':PurePosixPath,'json':json,'hashlib':hashlib,'dt':dt,'argparse':argparse,'io':io,'uuid':uuid,'zipfile':zipfile,'quote':quote}
exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='main'],type_ignores=[]),str(source),'exec'),env)
zsource=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py');zt=ast.parse(zsource.read_text());ze={'DepositError':type('DepositError',(RuntimeError,),{}),'re':__import__('re'),'html':__import__('html')};exec(compile(ast.Module(body=[x for x in zt.body if isinstance(x,ast.FunctionDef) and x.name in {'server_files','matching_file','verify'}],type_ignores=[]),str(zsource),'exec'),ze)
metadata=json.loads((home/'bound_release/zenodo-deposit.json').read_text())['metadata'];payloads={n:(home/'bound_release'/n).read_bytes() for n in ['congestion-fragmentation.pdf','congestion-fragmentation-verification.zip']}
selected=[{'name':n,'path':str(home/'bound_release'/n),'size':len(b),'sha256':hashlib.sha256(b).hexdigest(),'md5':hashlib.md5(b).hexdigest()} for n,b in payloads.items()]
remote_files=[{'key':v['name'],'size':v['size'],'checksum':'md5:'+v['md5']} for v in selected]
identifier=999;doi='10.5281/zenodo.999';inspectionbase={'id':identifier,'state':'published','doi':doi,'doi_url':'https://doi.org/'+doi,'doi_resolution':{'http_status':200,'resolved_url':'https://zenodo.org/records/999'},'metadata_normalizations':[]}
publicbase={'id':identifier,'doi':doi,'metadata':copy.deepcopy(metadata),'files':remote_files};cases=[];work=home/'public_verifier_fixtures';work.mkdir(exist_ok=False)
def writejson(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def writebytes(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(v)
def run(label,mutation,ok=False):
 a=work/label;a.mkdir();(a/'raw/pr0397').mkdir(parents=True);audit=a/'audit';audit.mkdir();env['AUDIT']=audit;env['ROOT']=a
 remote={'metadata':copy.deepcopy(metadata),'files':copy.deepcopy(remote_files)};public=copy.deepcopy(publicbase);inspection=copy.deepcopy(inspectionbase);downloads=dict(payloads);mutation(remote,public,inspection,downloads)
 def inspect(args):
  assert args.command=='inspect' and args.check_doi is True and args.sandbox is False
  norms=ze['verify'](remote,metadata,selected);return dict(inspection,metadata_normalizations=norms)
 z=types.SimpleNamespace(load_manifest=lambda p:(metadata,selected),run=inspect,server_files=ze['server_files'],matching_file=ze['matching_file']);env['zenodo']=z;env['require_release_clearance']=lambda:True;env['atomic_json']=writejson;env['atomic_bytes']=writebytes
 def fetch(url):
  if '/api/records/' in url:return json.dumps(public).encode(),200,url
  name=url.rsplit('/',1)[1].split('?')[0];return downloads[name],200,url
 env['fetch']=fetch
 old=sys.argv;sys.argv=['verify_published_files.py','--deposit-id','999']
 try:
  with contextlib.redirect_stdout(io.StringIO()):env['main']()
 except Exception as ex:cases.append({'case':label,'expected':'accept' if ok else 'reject','actual':'reject','exception':type(ex).__name__,'reason':str(ex)});assert not ok,(label,str(ex))
 else:cases.append({'case':label,'expected':'accept' if ok else 'reject','actual':'accept'});assert ok,label
 finally:sys.argv=old
run('exact_public_record_pdf_zip_all138members',lambda r,p,i,d:None,True)
run('authenticated_metadata_description_changed',lambda r,p,i,d:r['metadata'].update(description='changed'))
run('authenticated_metadata_creator_changed',lambda r,p,i,d:r['metadata']['creators'][0].update(name='changed'))
run('authenticated_metadata_AI_disclosure_missing',lambda r,p,i,d:r['metadata'].update(description=r['metadata']['description'].split('<p>AI tools')[0]))
run('authenticated_file_checksum_changed',lambda r,p,i,d:r['files'][0].update(checksum='md5:bad'))
run('inspection_wrong_id',lambda r,p,i,d:i.update(id=998))
run('inspection_not_published',lambda r,p,i,d:i.update(state='ready_to_publish'))
run('inspection_DOI_wrong',lambda r,p,i,d:i.update(doi='10.5281/zenodo.998'))
run('inspection_DOI_unresolved',lambda r,p,i,d:i['doi_resolution'].update(http_status=404))
run('public_wrong_id',lambda r,p,i,d:p.update(id=998))
run('public_wrong_DOI',lambda r,p,i,d:p.update(doi='10.5281/zenodo.998'))
run('public_title_changed',lambda r,p,i,d:p['metadata'].update(title='changed'))
run('public_version_changed',lambda r,p,i,d:p['metadata'].update(version='2'))
run('public_extra_payload',lambda r,p,i,d:p['files'].append({'key':'other.pdf','size':1,'checksum':'md5:bad'}))
run('public_missing_payload',lambda r,p,i,d:p['files'].pop())
run('public_duplicate_payload',lambda r,p,i,d:p['files'].append(copy.deepcopy(p['files'][0])))
run('public_metadata_file_size_changed',lambda r,p,i,d:p['files'][0].update(size=1))
run('actual_downloaded_pdf_changed',lambda r,p,i,d:d.update({'congestion-fragmentation.pdf':b'changed'}))
run('actual_downloaded_zip_changed',lambda r,p,i,d:d.update({'congestion-fragmentation-verification.zip':d['congestion-fragmentation-verification.zip']+b'changed'}))
out={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'all_assertions_passed':True,'controls':len(cases),'accepted':sum(x['actual']=='accept' for x in cases),'rejected':sum(x['actual']=='reject' for x in cases),'cases':cases,'scope':'Actual candidate public verifier main and existing Zenodo metadata/file verifier AST; synthetic provider replies and local files only. Exact release bytes used for positive PDF/ZIP case. No network, account state, publication or shared filesystem mutation.'};(home/'PUBLIC_VERIFIER_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='cases'}))
