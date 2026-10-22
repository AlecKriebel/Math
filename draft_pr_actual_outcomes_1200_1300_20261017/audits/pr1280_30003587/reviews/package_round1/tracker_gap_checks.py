from pathlib import Path
import contextlib,copy,datetime,hashlib,importlib.util,io,json,runpy,tempfile,types,sys
H=Path(__file__).resolve().parent;A=H.parent.parent;P=A/'publication';tempfile.tempdir=str(H/'_local')
def load(path):
 s=importlib.util.spec_from_file_location('own_'+path.stem+str(id(path)),path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def need(v,m):
 if not v:raise RuntimeError(m)
v=runpy.run_path(str(P/'verification/verify.py'));context=v['load_context'](A,P);pub={'environment':'production','state':'published','metadata_normalizations':[],'id':123,'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123','record_url':'https://zenodo.org/records/123','title':context['title']};out=[]
for text in ['Published DOI: 10.5281/zenodo.123','Published at https://doi.org/10.5281/zenodo.123 (v1.0)','PR1280','PR 1280','#1280']:
 for column in range(4):
  with tempfile.TemporaryDirectory(prefix='actual-append-gap-',dir=H/'_local') as tmp:
   p=Path(tmp);t=load(P/'append_tracker.py');t.ROOT=p;save=lambda path,obj:path.write_text(json.dumps(obj)+'\n');save(p/'PUBLICATION_RECEIPT.json',pub);save(p/'zenodo-deposit.json',{'metadata':context['metadata']});save(p/'FINAL_REVIEW_GATE.json',{'valid_earlier_package_gate_stub':True});row=['','','',''];row[column]=text;rows=[['Original Problem','Solution Chat URL','DOI','Notes'],row];events=[]
   def route(path):
    if Path(path).name=='update_pr_publication.py':return {'validate_workflow_gate':lambda g:None}
    if Path(path).name=='prepare_package.py':return {'load_context':lambda:copy.deepcopy(context)}
    raise RuntimeError('unexpected module')
   t.runpy=types.SimpleNamespace(run_path=route)
   def call(parts,params,body=None):
    events.append(parts)
    if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':1254632077,'title':'Math Puzzles'}}]}
    if parts==['spreadsheets','values','get']:return {'values':copy.deepcopy(rows if params['range']=="'Math Puzzles'!A:D" else [rows[-1]])}
    if parts==['spreadsheets','values','append']:
     rows.append(copy.deepcopy(body['values'][0]));return {'updates':{'updatedRange':"'Math Puzzles'!A3:D3",'updatedRows':1,'updatedColumns':4}}
    raise RuntimeError('unexpected service')
   t.call=call
   with contextlib.redirect_stdout(io.StringIO()):t.main()
   need(events.count(['spreadsheets','values','append'])==1,'gap not reproduced');out.append({'existing_identity':text,'column':column,'unexpected_append':True,'readback_verified':json.loads((p/'tracker/TRACKER_RECEIPT.json').read_text())['readback_verified'],'all_calls_mocked':True})
(H/('TRACKER_GAP_CHECKS'+('' if sys.flags.optimize==0 else '_'+str(sys.flags.optimize))+'.json')).write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_source_sha256':hashlib.sha256((P/'append_tracker.py').read_bytes()).hexdigest(),'cases':out,'scope':'Actual append main with exact current context/metadata, mocked valid earlier gate and mocked services; receipt id123 is synthetic.'},indent=2)+'\n');print('confirmed '+str(len(out))+' duplicate-identity appends in isolated fixtures')
