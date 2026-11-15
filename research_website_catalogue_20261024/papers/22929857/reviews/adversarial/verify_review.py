#!/usr/bin/env python3
"""Read-only custody/result verifier; no source execution, writes or network.
Use check_exact_readonly.py separately to replay exact algebra. This verifier
cannot formally certify the written all-N geometric/topological proof.
"""
from pathlib import Path
import hashlib,json,io,zipfile,subprocess
from datetime import datetime,timezone
P=Path(__file__).resolve().parent;BASE=P.parents[1];SOURCE=BASE/'sources'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
def need(test,label):
    if not test:raise ValueError(label)
need(sha(SOURCE/'SOURCE_READY.json')=='b9a6b2f5d848fd924682faf33ad39c74f80d6d849e1a0081abbc5d5bfdc0bf4d','READY pin')
need(sha(P/'INITIAL_SEAL.json')=='7a4ca57546c78e630e7b1793e5adadb0e36777e5bfedf75fa76e78918ffa7c39','blind initial seal')
initial=load(P/'INITIAL_MANIFEST.json');seal=load(P/'INITIAL_SEAL.json')
need(sha(P/'INITIAL_MANIFEST.json')==seal['manifest_sha256'],'initial manifest binding')
for a in initial['files']:
 f=Path(a['path']);need(f.stat().st_size==a['bytes'] and sha(f)==a['sha256'],'initial member '+str(f))
source=load(P/'SOURCE_BINDINGS.json')
need(sha(SOURCE/'SOURCE_READY_MANIFEST.json')==source['original_manifest_sha256'],'original source manifest')
for a in source['files']:
 f=Path(a['path']);need(f.stat().st_size==a['bytes'] and sha(f)==a['sha256'],'source unchanged '+str(f))
R=load(SOURCE/'SOURCE_READY.json');record=load(SOURCE/'record.raw.json')
need(record['metadata']['version']==R['version']=='1.1','exact version')
need(record['metadata']['publication_date']==R['publication_date_declared']=='2026-09-23','declared date')
need(record['created']==R['record_created'],'separate creation')
assets=R['all_native_assets_in_original_order']
need([a['original_api_file_object'] for a in assets]==record['files'],'whole original native asset objects and order')
need([a['original_api_file_object']['key'] for a in assets]==['reproducibility.zip','paper.pdf'],'native ZIP then PDF')
for a in assets:
 f=Path(a['path']);need(f.stat().st_size==a['bytes'] and sha(f)==a['SHA256'] and hashlib.md5(f.read_bytes()).hexdigest()==a['MD5'],'native asset bytes')
need((SOURCE/'paper.pdf').read_bytes()==(SOURCE/'published-source/paper/main.pdf').read_bytes(),'embedded actual PDF')
reader=subprocess.run(['pdftotext','-layout',str(SOURCE/'paper.pdf'),'-'],text=True,capture_output=True,check=True).stdout
need(len([x for x in reader.split('\f') if x.strip()])==4,'complete four-page searchable reader')
need(len((SOURCE/'published-source/paper/main.tex').read_text().splitlines())==150,'all controlling source lines')
count=0;expanded=0
with zipfile.ZipFile(SOURCE/'reproducibility.zip') as z:
 need(len(z.namelist())==len(set(z.namelist())),'no duplicate names')
 for info in z.infolist():
  need(not info.is_dir() and not info.filename.startswith('/') and '..' not in Path(info.filename).parts,'safe regular member')
  blob=z.read(info);need((SOURCE/'published-source'/info.filename).read_bytes()==blob,'CRC/extraction identity')
  need(not zipfile.is_zipfile(io.BytesIO(blob)),'no hidden nested ZIP')
  count+=1;expanded+=len(blob)
need(count==30 and expanded==208344,'all complete native ZIP payloads')
for line in (SOURCE/'published-source/MANIFEST.sha256').read_text().splitlines():
 digest,name=line.split(None,1);name=name.lstrip('* ').strip();need(sha(SOURCE/'published-source'/name)==digest,'native declared manifest '+name)
own=load(P/'EXACT_RESULTS.json');supplied=load(P/'SUPPLIED_EXACT_RESULTS.json');execution=load(P/'SUPPLIED_EXACT_EXECUTION.json')
need(own['status']=='PASS' and own['count']==26 and len(own['checks'])==26,'recorded independent exact checks')
need(own['source_imports'] is False and own['file_writes'] is False and own['numerical_samples_used_as_proof'] is False,'independent execution boundaries')
need(supplied['passed'] is True and len(supplied['checks'])==10 and all(c['passed'] for c in supplied['checks']),'recorded supplied exact results')
need(execution['exit_code']==0 and execution['script_sha256']==sha(SOURCE/'published-source/verification/verify_exact.py'),'actual supplied invocation identity')
need(execution['argv'][-2:]==['--output',str(P/'SUPPLIED_EXACT_RESULTS.json')],'source-adjacent writes avoided')
need((P/'.gitignore').read_text()=='private-primary/\n','foreign primary ignore boundary')
primary=load(P/'PRIMARY_INTERFACES.json');private=[]
for a in primary['interfaces']:
 f=Path(a['path']);need(f.stat().st_size==a['bytes'] and sha(f)==a['sha256'],'primary byte authentication');private.append(a['sha256'])
# Validate all final own files when this is invoked after finalization.
final_count=None
if (P/'MANIFEST.json').exists():
 m=load(P/'MANIFEST.json')
 for a in m['files']:
  f=Path(a['path']);need(f.stat().st_size==a['bytes'] and sha(f)==a['sha256'],'final packet member '+str(f))
 final_count=len(m['files'])
if (P/'SEAL.json').exists():need(sha(P/'MANIFEST.json')==load(P/'SEAL.json')['manifest_sha256'],'final seal manifest')
print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS_READONLY_CUSTODY_AND_RECORDED_RESULTS','scope':'identity/custody and retained actual bounded runs; not a formal proof of the written theorem','source_files_unchanged':len(source['files']),'initial_files_unchanged':len(initial['files']),'native_ZIP_regular_members':count,'native_expanded_bytes':expanded,'own_exact_checks_recorded':26,'supplied_exact_checks_recorded':10,'actual_primary_body_sha256':private,'current_sibling_opinions_read':False,'final_packet_members_checked':final_count,'source_programs_executed_by_this_verifier':False,'network':False,'writes':False},indent=2))
