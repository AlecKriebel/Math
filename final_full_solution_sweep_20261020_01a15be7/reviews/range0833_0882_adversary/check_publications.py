from pathlib import Path,PurePosixPath
import json,hashlib,datetime,urllib.request,concurrent.futures,subprocess,zipfile,io,stat
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7'); O=Path(__file__).resolve().parent; D=O/'downloads_private';D.mkdir(exist_ok=True)
H=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.run(['git',*a],cwd=R.parent,capture_output=True,check=True).stdout
def fetch(url,path):
 if path.exists() and not path.name.endswith('_doi.html'):
  data=path.read_bytes(); return {'url':url,'bytes':len(data),'sha256':H(data),'at':datetime.datetime.fromtimestamp(path.stat().st_mtime,datetime.timezone.utc).isoformat(),'custody':'fresh current-review download reused after interrupted validation'}
 req=urllib.request.Request(url,headers={'User-Agent':'IndependentResearchVerification/1.0'})
 with urllib.request.urlopen(req,timeout=45) as f: data=f.read(); final=f.url; ctype=f.headers.get('Content-Type')
 path.write_bytes(data); return {'url':url,'final_url':final,'content_type':ctype,'bytes':len(data),'sha256':H(data),'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
cases={n:json.loads((O/f'inputs/PR{n:04}_PUBLICATION_COVERAGE_DETAILS.json').read_text()) for n in [838,872,880]}
receipts={}; errs=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 jobs={ex.submit(fetch,f'https://zenodo.org/api/records/{d["record"]}',D/f'pr{n}_record.json'):f'pr{n}_record' for n,d in cases.items()}
 jobs.update({ex.submit(fetch,f'https://doi.org/{d["doi"]}',D/f'pr{n}_doi.html'):f'pr{n}_doi' for n,d in cases.items()})
 for fut,key in jobs.items():
  try:receipts[key]=fut.result()
  except Exception as e:errs.append({'key':key,'error':repr(e)})
metas={n:json.loads((D/f'pr{n}_record.json').read_text()) for n in cases}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 jobs={ex.submit(fetch,f['links']['self'],D/f'pr{n}_{f["key"]}'):f'pr{n}_{f["key"]}' for n,m in metas.items() for f in m['files']}
 for fut,key in jobs.items():
  try:receipts[key]=fut.result()
  except Exception as e:errs.append({'key':key,'error':repr(e)})
(O/'PUBLICATION_RETRIEVAL_RECEIPTS.json').write_text(json.dumps({'receipts':receipts,'errors':errs},indent=2)+'\n')
results=[]
ledger=json.loads((O/'inputs/ledger_live_private.json').read_text())['values']
for n,d in cases.items():
 meta=metas[n]; dis=json.loads((O/f'inputs/disposition_{n:04}.json').read_text()); expected_files={x['name']:x for x in d['public_files']}
 checks={'metadata_doi_identity':meta['doi']==d['doi'],'record_id_identity':int(meta['id'])==d['record'],'files_exact_names':set(expected_files)==set(f['key'] for f in meta['files']),'public_status':meta.get('submitted') is True or meta.get('status')=='published','doi_resolves_to_record':str(d['record']) in receipts.get(f'pr{n}_doi',{}).get('final_url','')}; file_results=[]
 for f in meta['files']:
  data=(D/f'pr{n}_{f["key"]}').read_bytes(); e=expected_files[f['key']]; alg,md=f['checksum'].split(':'); checks[f'file_{f["key"]}']=len(data)==f['size']==e['bytes'] and hashlib.new(alg,data).hexdigest()==md and H(data)==e['sha256']; file_results.append({'name':f['key'],'bytes':len(data),'sha256':H(data),'metadata_checksum':f['checksum']})
 zname=next(k for k in expected_files if k.endswith('.zip')); pdfname=next(k for k in expected_files if k.endswith('.pdf'))
 with zipfile.ZipFile(D/f'pr{n}_{zname}') as z:
  names=z.namelist(); checks['zip_crc']=z.testzip() is None; checks['safe_unique_zip']=len(names)==len(set(names)) and all(not PurePosixPath(x).is_absolute() and '..' not in PurePosixPath(x).parts and '\\' not in x and not stat.S_ISLNK(a.external_attr>>16) for x,a in zip(names,z.infolist()))
  ix=json.loads(z.read('package_index.json')); entries=ix['files']; checks['closed_manifest']=set(a['path'] for a in entries)==set(names)-{'package_index.json'} and len(entries)==len(names)-1; checks['manifest_exact']=all(len(z.read(x['path']))==x['bytes'] and H(z.read(x['path']))==x['sha256'] for x in entries); checks['count_matches_root']=len(names)==d['archive_members'] and len(entries)==d['manifested_payloads']; checks['manifest_hash_matches_root']=H(z.read('package_index.json'))==d['manifest_sha256']; checks['external_pdf_equals_embedded']=z.read('note.pdf')==(D/f'pr{n}_{pdfname}').read_bytes()
  bindings=[]
  # Derive the historical inventory directly from the immutable source tree.
  prefix='random_property_t_30006628/' if n==872 else f'unsolved_math_prioritization/attempts/{d["problem_id"]}/'
  originals=git('ls-tree','-r','--name-only',d['source_head'],'--',prefix).decode().splitlines(); mapping={b['path']:b for b in d['original_bindings']}
  checks['historical_original_inventory_complete']=set(originals)==set(mapping)
  for path in originals:
   member='source/'+path[len(prefix):]; payload=z.read(member); historical=git('show',d['source_head']+':'+path); current=git('show',dis['inventory_head_sha']+':'+path)
   bindings.append({'path':path,'archive_member':member,'bytes':len(payload),'sha256':H(payload),'historical_equal':payload==historical,'current_equal':payload==current,'root_receipt_equal':mapping[path]['sha256']==H(payload) and mapping[path]['current_head_match']==(payload==current)})
  checks['historical_originals_exact']=all(x['historical_equal'] and x['root_receipt_equal'] for x in bindings)
  checks['current_wrappers_only_differ']=sorted(x['path'] for x in bindings if not x['current_equal'])==sorted(d['current_wrapper_differences']) if isinstance(d['current_wrapper_differences'][0],str) else sorted(x['path'] for x in bindings if not x['current_equal'])==sorted(x['path'] for x in d['current_wrapper_differences'])
  checks['current_paper_copies_exact']=all(git('show',dis['inventory_head_sha']+':'+path)==z.read('note.tex' if path.endswith('.tex') else 'note.pdf') for path in d['public_pdf_and_manuscript_match_all_current_head_copies'])
  (D/f'pr{n}_note.tex').write_bytes(z.read('note.tex')); (D/f'pr{n}_note.pdf').write_bytes(z.read('note.pdf')); (D/f'pr{n}_archive_README.md').write_bytes(z.read('README.md')); (D/f'pr{n}_CURRENT_PRIORITY.md').write_bytes(z.read('CURRENT_PRIORITY.md'))
 row=ledger[d['ledger_row']-1]; joined=' '.join(row); idmatches=[i+1 for i,x in enumerate(ledger) if d['problem_id'] in ' '.join(x)]; doimatches=[i+1 for i,x in enumerate(ledger) if d['doi'] in ' '.join(x)]; prmatches=[i+1 for i,x in enumerate(ledger) if f'https://github.com/AlecKriebel/Math/pull/{n}' in ' '.join(x)]
 checks['ledger_unique_identity']=idmatches==doimatches==prmatches==[d['ledger_row']]
 results.append({'pr':n,'record':d['record'],'doi':d['doi'],'ledger_row':d['ledger_row'],'checks':checks,'files':file_results,'members':len(names),'manifest_entries':len(entries),'historical_original_count':len(originals),'historical_bindings':bindings,'current_wrapper_differences':[x['path'] for x in bindings if not x['current_equal']],'semantic_scope_review':'manual in REPORT.md; artifact checks alone are not proof or priority certification'})
(O/'PUBLICATION_RESULTS.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'receipts':receipts,'errors':errs,'results':results},indent=2)+'\n')
print(json.dumps({'errors':errs,'cases':[{'pr':x['pr'],'failures':[k for k,v in x['checks'].items() if not v],'files':x['files'],'members':x['members'],'manifest_entries':x['manifest_entries'],'historical_original_count':x['historical_original_count'],'current_wrapper_differences':x['current_wrapper_differences']} for x in results]},indent=2))
