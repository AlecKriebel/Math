"""Read-only independent package and provenance verification; writes only this review."""
from pathlib import Path, PurePosixPath
import json,hashlib,zipfile,stat,re,io,binascii,subprocess,datetime
R=Path(__file__).resolve().parent; B=R.parent.parent; P=B/'publication'; Z=P/'teichmuller_original_ball_paths_source_audits_v1.zip'; prefix='teichmuller_original_ball_paths_v1/'
def sha(x):return hashlib.sha256(x).hexdigest()
def pin(p):return {'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':{},'entries':[]};checks=out['checks']
with zipfile.ZipFile(Z) as z:
 names=z.namelist();checks['entry_count']=len(names);checks['unique_sorted']=names==sorted(set(names));checks['crc_test']=z.testzip();checks['archive_comment_empty']=not z.comment
 for n in names:
  i=z.getinfo(n);rel=n.removeprefix(prefix);parts=PurePosixPath(n).parts;data=z.read(n);local=P/rel
  row={'path':rel,'bytes':len(data),'sha256':sha(data),'crc_correct':binascii.crc32(data)&0xffffffff==i.CRC,'same_as_publication':local.is_file() and data==local.read_bytes(),'safe_ascii_path':n.isascii() and n.startswith(prefix) and '..' not in parts and not n.startswith('/') and '\\' not in n and ':' not in n,'regular_0644':(i.external_attr>>16)==0o100644,'date':list(i.date_time),'unix':i.create_system==3,'encrypted':bool(i.flag_bits&1),'extra_empty':not i.extra,'comment_empty':not i.comment,'method':i.compress_type}
  out['entries'].append(row)
 checks['all_entry_properties']=all(all(e[k] for k in ['crc_correct','same_as_publication','safe_ascii_path','regular_0644','unix','extra_empty','comment_empty']) and not e['encrypted'] and e['date']==[2026,10,13,0,0,0] and e['method']==8 for e in out['entries'])
 m=json.loads(z.read(prefix+'PACKAGE_MANIFEST.json'));checks['manifest_rows']=len(m['files']);checks['manifest_unique_sorted']=[q['path'] for q in m['files']]==sorted(set(q['path'] for q in m['files']));checks['manifest_exact_entry_set']=set(prefix+q['path'] for q in m['files'])==set(names)-{prefix+'PACKAGE_MANIFEST.json'}
 checks['manifest_all_pins']=all(pin(P/q['path'])=={'bytes':q['bytes'],'sha256':q['sha256']} for q in m['files'])
 checks['manifest_self_hash_excluded']=m['manifest_self_hash_excluded'] and not any(q['path']=='PACKAGE_MANIFEST.json' for q in m['files'])
 # Recompute from independent enumeration; no supplied builder execution.
 files=[P/n for n in ['research_note.tex','research_note.pdf','README.md','SUPPLEMENT.md','metadata.json']]+[p for p in (P/'evidence').rglob('*') if p.is_file()]
 files=sorted(files,key=lambda p:p.relative_to(P).as_posix());rows=[dict(path=p.relative_to(P).as_posix(),**pin(p)) for p in files]
 mm={k:v for k,v in m.items() if k!='files'};mm['files']=rows;checks['independently_enumerated_manifest_bytes']=(json.dumps(mm,indent=2)+'\n').encode()==(P/'PACKAGE_MANIFEST.json').read_bytes()
 stream=io.BytesIO()
 with zipfile.ZipFile(stream,'w',compression=8,compresslevel=9) as zz:
  for name in sorted(names):
   zi=zipfile.ZipInfo(name,(2026,10,13,0,0,0));zi.create_system=3;zi.external_attr=0o100644<<16;zi.compress_type=8;zz.writestr(zi,(P/name.removeprefix(prefix)).read_bytes())
 checks['independent_reconstruction_bytes_equal']=stream.getvalue()==Z.read_bytes();checks['independent_reconstruction_sha256']=sha(stream.getvalue())
 # Inspect every included payload's type and parse all JSON, UTF8 text; binary only our PDF.
 type_rows=[]
 for n in names:
  rel=n.removeprefix(prefix);d=z.read(n);row={'path':rel,'bytes':len(d)}
  if rel=='research_note.pdf':row['kind']='own_candidate_pdf';row['valid_magic']=d.startswith(b'%PDF')
  else:
   s=d.decode('utf-8');row['kind']='authored_json' if rel.endswith('.json') else 'authored_tex' if rel.endswith('.tex') else 'authored_text';row['characters']=len(s);row['json_parsed']=json.loads(s) is not None if rel.endswith('.json') else None
  type_rows.append(row)
 out['payload_type_inspection']=type_rows;checks['third_party_raw_file_absent']=not any(re.search(r'\.(pdf|png|jpe?g|html|txt|zip)$',n,re.I) for n in names if n!=prefix+'research_note.pdf');checks['farb_extract_absent']=prefix+'evidence/metric_01/sources/farb_printed_24_25.txt' not in names and not (P/'evidence/metric_01/sources/farb_printed_24_25.txt').exists()
 # Original git tree and byte comparisons.
 head='6322305d37b8131f034a1b4c3c5e861e4b04844f';base='unsolved_math_prioritization/attempts/11000026'
 tree=subprocess.check_output(['git','ls-tree','-r','--name-only',head,'--',base],text=True).splitlines();out['original_full_tree']=tree
 sp=json.loads((B/'SUBMITTED_PINS.json').read_text());orig=[]
 for q in sp['files']:
  d=subprocess.check_output(['git','show',head+':'+q['repository_path']]);local=B/q['snapshot_path'];package=P/'evidence'/q['snapshot_path']
  orig.append({'path':q['repository_path'],'sha256':sha(d),'bytes':len(d),'git_snapshot_package_bytes_equal':d==local.read_bytes()==package.read_bytes(),'pin_matches':sha(d)==q['sha256'] and len(d)==q['bytes']})
 out['original_files']=orig;checks['original_full_tree_exact_eight']=set(tree)==set(q['repository_path'] for q in sp['files']) and len(tree)==8;checks['all_original_git_bytes_match']=all(q['git_snapshot_package_bytes_equal'] and q['pin_matches'] for q in orig)
 ac=json.loads((P/'evidence/AUDIT_COPY_MANIFEST.json').read_text());copies=[]
 for q in ac['files']:
  p=P/q['path'];s=B/q['audit_source_path'];copies.append({'path':q['path'],'source':q['audit_source_path'],'copies_equal':p.read_bytes()==s.read_bytes(),'pins_correct':pin(p)=={'bytes':q['bytes'],'sha256':q['sha256']}})
 out['author_copies']=copies;checks['author_copy_count']=len(copies);checks['all_author_copies_exact']=all(q['copies_equal'] and q['pins_correct'] for q in copies)
 checks['metadata_wrapper_exact']=json.loads((P/'zenodo-deposit.json').read_text())['metadata']==json.loads((P/'metadata.json').read_text());checks['wrapper_deliverables_exist']=all((P/q['path']).is_file() for q in json.loads((P/'zenodo-deposit.json').read_text())['files'])
 # Navigation: current docs are actual portable links; frozen records contain historic local locators.
 links=[]
 for rel in ['README.md','SUPPLEMENT.md','evidence/INDEX.md']:
  p=P/rel
  for dest in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   if re.match(r'https?://',dest):continue
   target=(p.parent/dest.split('#')[0]).resolve();links.append({'from':rel,'target':dest,'exists':target.exists(),'inside_package':target.is_relative_to(P.resolve())})
 out['current_navigation_links']=links;checks['current_navigation_all_resolve']=all(q['exists'] and q['inside_package'] for q in links)
 # Every historical sha256 pin has a surviving current/private or before-stage byte witness.
 hash_index={}
 for p in B.rglob('*'):
  if p.is_file() and not p.is_relative_to(R):hash_index.setdefault(sha(p.read_bytes()),[]).append(p.relative_to(B).as_posix())
 historical=[]
 def scan(obj,locator,file):
  if isinstance(obj,dict):
   for key,val in obj.items():
    if isinstance(val,str) and re.fullmatch(r'[0-9a-f]{64}',val) and ('sha256' in key or key in ['hash','digest']):
     witnesses=hash_index.get(val,[]);historical.append({'record':file,'json_locator':locator+'/'+key,'sha256':val,'bytes_claim':obj.get('bytes'),'path_claim':obj.get('path',obj.get('snapshot_path',obj.get('private_path'))),'witnesses':witnesses,'witness_found':bool(witnesses),'size_matches':obj.get('bytes') is None or any((B/p).stat().st_size==obj['bytes'] for p in witnesses)})
    else:scan(val,locator+'/'+key,file)
  elif isinstance(obj,list):
   for j,q in enumerate(obj):scan(q,locator+'/'+str(j),file)
 for p in sorted((P/'evidence').rglob('*.json')):scan(json.loads(p.read_text()),'',p.relative_to(P).as_posix())
 out['historical_pin_count']=len(historical);out['historical_unresolved']=[q for q in historical if not q['witness_found'] or not q['size_matches']]
 (R/'HISTORICAL_PIN_RECONCILIATION.json').write_text(json.dumps({'utc':out['utc'],'pins':historical,'unresolved':out['historical_unresolved']},indent=2)+'\n')
 (R/'PACKAGE_VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'checks':checks,'historical_pins':len(historical),'historical_unresolved':out['historical_unresolved']},indent=2))
