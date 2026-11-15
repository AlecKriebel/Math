#!/usr/bin/env python3
"""Source-only read-only verifier: no network, writes, math reads or deposited execution."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import json,hashlib,zipfile,stat,unicodedata,subprocess,io
P=Path(__file__).resolve().parents[1];S=P/'sources';A=P/'acquisition';PIN='1f728d52dd3bb791833a837fb3bae7eab1b3a37ce7ecd9c4655b94f4d693cf46'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();load=lambda f:json.loads(f.read_text())
def need(test,label):
 if not test:raise ValueError(label)
need(sha(S/'SOURCE_READY.json')==PIN,'exact READY pin');r=load(S/'SOURCE_READY.json');record=load(Path(r['native_record_body_path']));latest=load(S/'latest.raw.json')
need(record['id']==r['record_id'] and record['status']=='published','exact native published record')
need(record['metadata']['title']==r['title'] and record['metadata'].get('version')==r['version'] and record['metadata']['publication_date']==r['publication_date_declared'],'literal title/version/date')
need(record['created']==r['record_created'] and record.get('updated',record.get('modified'))==r['record_updated'],'separate created/updated')
need(latest['id']==r['latest_record_id'],'actual latest retained without substitution')
versions=[load(f) for f in sorted(S.glob('versions.page-*.raw.json'))];need(len(versions)==r['all_native_versions_pages_acquired'],'all native version pages')
need(versions[0]['hits']['total']==r['all_native_versions_total'] and sum(len(v['hits']['hits']) for v in versions)==r['all_native_versions_total'],'native version total preserved')
need([a['original_api_file_object'] for a in r['all_native_assets_in_original_order']]==record['files'],'whole original file objects and order')
files=load(S/'files.raw.json');entries={a['key']:a for a in files['entries']};need(set(entries)=={a['key'] for a in record['files']},'complete files endpoint keys')
for a in r['all_native_assets_in_original_order']:
 f=Path(a['path']);data=f.read_bytes();orig=a['original_api_file_object'];alg,pin=orig['checksum'].split(':',1)
 need(len(data)==a['bytes']==orig['size'] and sha(f)==a['SHA256'] and hashlib.md5(data).hexdigest()==a['MD5'] and hashlib.new(alg,data).hexdigest().lower()==pin.lower(),'native asset authentication')
 need(entries[orig['key']]['checksum']==orig['checksum'] and entries[orig['key']]['size']==orig['size'],'native file endpoint checksum/size')
# All successful and complete failed native response bytes/headers remain untouched.
receipts=[load(S/'record-attempt2.transport.json')]+load(S/'native.transport.v2.json')+load(S/'asset.transport.v3.json');success=0;failures=[]
for a in receipts:
 need(isinstance(a['response_headers_in_received_order'],list),'native ordered header list')
 b=a['body'];f=Path(b['path']);need(f.stat().st_size==b['bytes'] and sha(f)==b['SHA256'],'actual transport body')
 if a['HTTP_status']==200:success+=1
 else:failures.append(a['HTTP_status'])
need(success==6 and failures==[406],'six complete successful native requests, separate406 body')
need('403' in load(S/'metadata.transport.json')[0]['error'],'initial exception-only403 retained')
need((S/'.gitignore').read_text()=='cache/\n','cache ignore boundary')
custody=load(S/'archive-custody.json');lookup={(a['container'],a['original_member_name']):a for a in custody['regular_members']};containers={a['container']:a for a in custody['containers']};seen=[];expanded=0
for label,c in containers.items():
 f=Path(c['source_path']);need(f.stat().st_size==c['bytes'] and sha(f)==c['SHA256'],'archive container identity');need(c['kind']=='zip','expected ZIP-only exact source')
 with zipfile.ZipFile(f) as z:
  names=z.namelist();need(len(names)==len(set(names)),'no duplicate names');need(len({unicodedata.normalize('NFC',n).casefold() for n in names})==len(names),'no case-normalized collisions')
  for zi in z.infolist():
   name=zi.filename;need(not name.startswith('/') and '..' not in PurePosixPath(name).parts and '\\' not in name,'safe relative path')
   mode=stat.S_IFMT((zi.external_attr>>16)&0xffff);need(mode in (0,stat.S_IFREG,stat.S_IFDIR),'regular or directory mode')
   if zi.is_dir():continue
   body=z.read(zi);a=lookup[(label,name)];need(len(body)==zi.file_size==a['bytes'] and hashlib.sha256(body).hexdigest()==a['SHA256'] and f'{zi.CRC:08x}'==a['CRC32'],'complete CRC/body check')
   need(Path(a['extracted_path']).read_bytes()==body,'exact existing extraction');need(not zipfile.is_zipfile(io.BytesIO(body)),'no actual nested ZIP');seen.append((label,name));expanded+=len(body)
need(set(seen)==set(lookup) and len(seen)==r['archive_custody']['regular_payload_occurrences'] and expanded==r['archive_custody']['expanded_bytes_all_depths'],'complete native archive custody')
need(len(containers)==r['archive_custody']['archive_containers'] and custody['nested_archives']==0 and not custody['unsupported_nested_formats'],'all actual archive formats accounted')
pdf=r['selected_actual_PDF'];f=Path(pdf['path']);need(f.stat().st_size==pdf['bytes'] and sha(f)==pdf['SHA256'],'actual selected native PDF')
info=subprocess.run(['pdfinfo',str(f)],capture_output=True,text=True,check=True).stdout;pages=int(next(line.split(':',1)[1].strip() for line in info.splitlines() if line.startswith('Pages:')));need(pages==pdf['pages'],'complete page count by metadata only')
for a in pdf['byte_identical_ZIP_members']:need(Path(a['extracted_path']).read_bytes()==f.read_bytes(),'exact embedded manuscript')
t=r['controlling_TeX'];need(Path(t['path']).stat().st_size==t['bytes'] and sha(Path(t['path']))==t['SHA256'],'controlling TeX bytes')
need(len(r['all_TeX_candidates'])==1 and r['all_TeX_candidates'][0]['SHA256']==t['SHA256'],'sole controlling TeX structurally identified')
need(r['manuscript_scientifically_read'] is False and r['TeX_scientifically_read'] is False and r['source_programs_builders_finalizers_executed'] is False and r['old_triage_archived_current_review_opinions_read'] is False,'acquisition-only boundaries')
count=None
if (S/'SOURCE_READY_MANIFEST.json').exists():
 m=load(S/'SOURCE_READY_MANIFEST.json')
 for a in m['files']:
  f=S/a['path'];need(f.stat().st_size==a['bytes'] and sha(f)==a['SHA256'],'immutable source file '+a['path'])
 count=len(m['files'])
if (S/'SOURCE_READY_SEAL.json').exists():
 seal=load(S/'SOURCE_READY_SEAL.json');need(seal['manifest_SHA256']==sha(S/'SOURCE_READY_MANIFEST.json') and seal['SOURCE_READY_SHA256']==PIN,'source-ready seal')
print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'record_id':r['record_id'],'status':'PASS_SOURCE_CUSTODY_ONLY','SOURCE_READY_SHA256':PIN,'native_original_assets':len(r['all_native_assets_in_original_order']),'complete_successful_HTTP_bodies':success,'failed_HTTP_bodies_separate':failures,'initial403_exception_only_disclosed':True,'archive_regular_payloads':len(seen),'archive_containers':len(containers),'expanded_bytes':expanded,'manuscript_pages':pages,'controlling_TeX_bytes':t['bytes'],'immutable_source_bindings_checked':count,'manuscript_scientifically_read':False,'mathematical_assessment':None,'deposited_code_executed':False,'network':False,'writes':False},indent=2))
