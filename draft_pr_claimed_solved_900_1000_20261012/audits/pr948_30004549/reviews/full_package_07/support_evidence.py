from pathlib import Path
import json,os,datetime,hashlib,stat,ast
R=Path(__file__).parent;A=R.parents[1];D=A/'preprint';W=A/'publication/workflow';P=A.parents[1]
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,d):
 raw=(json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode()
 with (R/n).open('wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert (R/n).read_bytes()==raw
f=json.loads((D/'FREEZE.json').read_bytes());manifest=json.loads((D/'package/PACKAGE_MANIFEST.json').read_bytes());files={}
for name,pin in manifest['files'].items():
 path=D/'package'/name;b=path.read_bytes();assert len(b)==pin['bytes'] and sha(b)==pin['sha256'] and stat.S_ISREG(path.stat().st_mode) and stat.S_IMODE(path.stat().st_mode)==0o644 and path.stat().st_nlink==1
 files[name]={'bytes':len(b),'sha256':sha(b),'mode':'0644','text_decodable':not name.endswith(('.pdf','.zip'))}
# Reading all bytes is mechanical inventory, not a claim of substantive reading of each JSON leaf.
private=(A/'source_record_private.txt').read_bytes();assert all(private not in (D/'package'/name).read_bytes() for name in files if not name.endswith(('.pdf','.zip')))
assert [name for name in files if name.endswith('.pdf')]==['paper/note.pdf']
assert not [name for name in files if any(x in name.lower().split('/') for x in ['private','private_fixtures','cache','runtime','credentials','__pycache__'])]
aliases=[D/'anti-invariant-four-manifold-v1.0.pdf',D/'package/paper/note.pdf',D/'output/pdf/note.pdf'];assert len({sha(p.read_bytes()) for p in aliases})==1
helpers={n:(P/n).read_text() for n in f['future_helpers'] if n!='accept_pr948.py'};normalized={n:s[:s.rfind("entry('")] for n,s in helpers.items()};assert len(set(normalized.values()))==1
nested=[]
for path in W.rglob('*.json'):
 if path.name not in ['MANIFEST.json','SNAPSHOT_MANIFEST.json']:continue
 doc=json.loads(path.read_bytes());mapping=doc.get('files',doc.get('payloads',{}))
 if not isinstance(mapping,dict):continue
 for name,pin in mapping.items():
  p=path.parent/name;b=p.read_bytes();assert len(b)==pin['bytes'] and sha(b)==pin['sha256'],str(p)
 nested.append({'path_relative_to_workflow':path.relative_to(W).as_posix(),'sha256':sha(path.read_bytes()),'payloads':len(mapping)})
profile=json.loads((R/'profile/DEVELOPMENT_RESULTS.json').read_bytes());assert profile['event_count']==85 and len(profile['events'])==85 and not [e for e in profile['events'] if 'skip' in e.get('outcome','').lower()]
poison=[e for e in profile['events'] if e['test']=='ambient_import_poison_positive_control'];assert len(poison)==1 and poison[0]['outcome']=='controlled_poison_executed_without_isolation'
prior={x['source_relative_to_audit']:x['source_sha256'] for x in json.loads((A/'reviews/full_package_06/PRIMARY_SUPPORT.json').read_bytes())['selected_sources']};primary=json.loads((R/'PRIMARY_INVENTORY.json').read_bytes())
for row in primary['records']:assert row['source_sha256']==prior[row['source_relative_to_audit']];row['pages_personally_read']=row['pages_extracted']
primary.update(status='SELECTED_PRIMARY_PASSAGES_PERSONALLY_READ',completed_utc=utc(),limits='11 retained bodies, selected pages only, not complete source readings or journal-final equivalence. Raw texts/body copies excluded. Exact per-query web timestamps not captured. Reading followed INITIAL_ATTACK.')
save('PRIMARY_SUPPORT.json',primary)
render=[]
for i in range(1,6):
 path=R/f'pdf_qa/page-{i}.png';render.append({'page':i,'bytes':path.stat().st_size,'sha256':sha(path.read_bytes()),'personally_viewed':True,'assessment':{1:'Title, author/ORCID/date/version, abstract, definitions, theorem and generic-credit paragraph legible.',2:'Compactification, Stokes and simultaneous chart/full-cutoff relations legible, no collision.',3:'Gram, positive-kernel construction, gluing and Frobenius obstruction legible.',4:'Scope comparisons, credit/limits, AI/unrefereed/CC-BY disclosure and first references legible.',5:'Remaining bibliography/version/withdrawal references legible, no clipping or unresolved references.'}[i]})
save('PDF_VISUAL_QA.json',{'utc':utc(),'pdf_sha256':sha(aliases[0].read_bytes()),'render_recipe':['pdftoppm','-r','95','-png',str(aliases[0]),str(R/'pdf_qa/page')],'pages':render,'pages_total':5,'recompiled':False,'all_aliases_identical':[str(p) for p in aliases]})
save('PACKAGE_AND_WORKFLOW_BOUNDARIES.json',{'utc':utc(),'package_payload_count':len(files),'envelope_additional':1,'mechanical_byte_read_inventory':files,'scope':'Bytes individually read/authenticated. Substantive reading separately stated; hash equality is not understanding.','no_exact_raw_source_record_in_public_text':True,'public_pdf_count':1,'only_descriptor_uploads':json.loads((D/'zenodo-deposit.json').read_bytes())['files'],'launcher_differences_only_terminal_entry_selector':True,'nested_workflow_seals':nested,'nested_count':len(nested),'profile_events':85,'profile_skips':0,'actual_poison_control':poison,'remaining_private_fixture_under_W':[p.name for p in W.glob('private-fixture-*')]})
print(json.dumps({'package_payloads':len(files),'nested_seals':len(nested),'profile':85,'primary_read':11,'pdf_viewed':5,'leftover_W_fixtures':[p.name for p in W.glob('private-fixture-*')]}))
