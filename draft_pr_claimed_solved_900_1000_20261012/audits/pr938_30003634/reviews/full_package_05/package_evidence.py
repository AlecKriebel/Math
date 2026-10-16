import ast,hashlib,importlib.util,json,sqlite3,sys
from pathlib import Path
from datetime import datetime,timezone
from pypdf import PdfReader
R=Path(__file__).resolve().parent;A=R.parents[1];D=A/'publication';E=R/'private/cold/extracted';ROOT=R.parents[4];sys.dont_write_bytecode=True
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(x,s):
 if not x:raise RuntimeError(s)
def load(p):return json.loads(p.read_bytes())
tree=ast.parse((D/'build_package.py').read_text());fam=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FAMILIES' for t in n.targets)))
seals=[]
for name,(manifest,pin) in fam.items():
 path=E/'reviews'/name/manifest;need(sha(path.read_bytes())==pin,'family seal');m=load(path);records=m.get('files',m.get('public_files',m.get('records')))
 if type(records) is list:records={x['path']:{'bytes':x.get('bytes',x.get('size')),'sha256':x['sha256']} for x in records}
 for n,item in records.items():
  b=(path.parent/n).read_bytes();need(len(b)==item.get('bytes',item.get('size')) and sha(b)==item['sha256'],'family payload')
 seals.append({'family':name,'manifest':manifest,'sha256':pin,'payloads':len(records),'status':'PASS'})
hist=[]
for n,pin in [('01','37feff8cb31bbef2b7f41b98d8f34571923e7a89cb4c8f53226ccd2adf388a91'),('02','36a69cb090d28f33be92963bcf7a62ed2ce756d653c44f07d2f37cb468290716'),('03','caa5253f9c0212cfbde804cc92b8705e59d59e0705d17cba7d8ac92a63ac1d13'),('04','56ee88b8f551d13046ae5dc09fd6b407d544e6e6e5545bc343f9a9eb26ae74f5')]:
 folder=A/'reviews'/('full_package_'+n);need(sha((folder/'MANIFEST.json').read_bytes())==pin,'historical seal')
 for name,record in load(folder/'MANIFEST.json')['files'].items():
  b=(folder/name).read_bytes();need({'bytes':len(b),'sha256':sha(b)}==record,'historical payload')
 hist.append({'round':n,'sha256':pin,'status':'PASS'})
uri='file:'+str(ROOT/'unsolved_math_prioritization/cache/catalog.sqlite')+'?mode=ro';db=sqlite3.connect(uri,uri=True);rows=db.execute('SELECT payload,report FROM records WHERE key=?',('30003634',)).fetchall();db.close();need(len(rows)==1,'source unique');problem,report=map(json.loads,rows[0]);st=sha(problem['statement'].encode());rev=sha(json.dumps([problem,report],sort_keys=True).encode());need(st=='2302f06ebd156e0ce9f1728964208380752184dcd932a117b8b397e409c15d6b' and rev=='eebfb186fc2eefe2cb9756aec0572e127127fc1be6e248d6abad78a4fe298bd9' and report=={},'full source')
(R/'private/actual_selected_source.json').write_text(json.dumps({'problem':problem,'prior_report':report},indent=2)+'\n')
programs=[]
for p in sorted((E/'original_packet').rglob('*.py')):
 tree=ast.parse(p.read_text());programs.append({'path':p.relative_to(E).as_posix(),'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes()),'assert_nodes':sum(isinstance(n,ast.Assert) for n in ast.walk(tree))})
need(len(programs)==9,'nine original programs')
meta=load(D/'zenodo-deposit.json');md=meta['metadata'];need(len(meta['files'])==2 and md['creators'][0]['orcid']=='0009-0001-9320-500X' and md['version']=='1.0' and md['publication_date']=='2026-10-15','metadata')
for name in ['note.tex','prepare_metadata.py','zenodo-deposit.json']:need('Mini-Workshop: Interactions between Low-dimensional Topology and Complex Algebraic Geometry' in (D/name).read_text(),'O3 correctedtitle')
need(load(D/'PREPUBLICATION_FREEZE.json')['package_manifest_sha256'] in md['notes'],'manifest in metadata')
reader=PdfReader(D/'output/pdf/note.pdf');need(len(reader.pages)==4,'four pages')
native=load(E/'strengthening/NATIVE_TURN_RECEIPT.json');history=[json.loads(x) for x in (E/'strengthening/NATIVE_HISTORY.jsonl').read_text().splitlines()];ledger=load(E/'strengthening/ATTEMPT_LEDGER.json');ready=load(E/'strengthening/READINESS.json');need([x['turns_used'] for x in history]==[0,1,1,2] and ledger==history[-1] and ledger['evidence']==ready,'native receipt/history');need(sum(x['arguments'][0]=='turn' for x in native['commands'])==2,'two genuine turncommands');need(sha((ROOT/'unsolved_math_prioritization/queue.py').read_bytes())==native['unmodified_queue_py_sha256'],'native source code')
result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','family_seals':seals,'historical_full_review_seals':hist,'original_program_static_inventory':programs,'source':{'readonly_sqlite':True,'complete_selected_source_read':True,'statement_hash':st,'review_hash':rev,'prior_report':{}},'metadata':{'title':md['title'],'creator':md['creators'][0],'date':md['publication_date'],'version':md['version'],'files':meta['files'],'actual_report_title_corrected':True,'external_manifest_pin_in_notes':True},'pdf':{'pages':4,'metadata':{str(k):str(v) for k,v in reader.metadata.items()},'page_boxes':[[float(x) for x in page.mediabox] for page in reader.pages],'sha256':sha((D/'output/pdf/note.pdf').read_bytes())},'native_accounting':{'actual_saved_counts':[0,1,1,2],'turn_commands':2,'known_total':2,'limit':5,'earlier_subprocesses_observed_by_this_reviewer':False,'this_review_added_proof_turns':0}}
(R/'PACKAGE_AND_METADATA.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','families':len(seals),'historical_seals':3,'programs':9,'source':'PASS','pdf':4,'native_counts':[0,1,1,2]}))
