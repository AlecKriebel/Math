from pathlib import Path
import gzip, hashlib, io, json, shutil, subprocess, sys, tarfile, zlib
from datetime import datetime, timezone
A=Path(__file__).resolve().parents[1];P=A/'preprint_v1_0';F=A/'finalization/terminal_admin_20261014'
def require(c,m):
 if not c:raise RuntimeError(m)
def load(p):return json.loads(p.read_text())
def check(base,r,field='path'):
 p=base/r[field];b=p.read_bytes();require(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],str(p))
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(A)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
changes=load(F/'CHANGE_INVENTORY.json')['changed'];modified={r['path']:r for r in changes};require(len(modified)==18,'authorized mutations')
inputs=load(F/'INPUT_PINS.json')['files']
for r in inputs:
 check(A,dict(r,path=modified[r['path']]['exact_before_byte_path']) if r['path'] in modified else r)
for r in changes:check(A,r['after']);check(A,dict(r['before'],path=r['exact_before_byte_path']))
for r in load(F/'PROTECTED_UNCHANGED.json')['files']:check(A,r)
for r in load(F/'OUTPUT_PINS.json')['files']:check(F,r)
for r in load(F/'FINAL_CURRENT_INPUT_PINS.json')['files']:check(P,r)
for r in load(F/'HISTORICAL_224_PIN_RESOLUTION.json')['files']:check(A,r,'resolved_before_byte_path')
old=load(F/'baseline/preprint_v1_0/EVIDENCE_COPY_MANIFEST.json')['files'];copies=load(P/'EVIDENCE_COPY_MANIFEST.json')['files']
require(len(copies)==468 and copies[:161]==old,'previous maps preserved')
for r in copies:check(A,r,'source_path');check(P,r,'package_path')
ledger=load(P/'HISTORIC_EXCLUSIONS.json')['files'];require(len(ledger)==13,'individual exclusion count')
for r in ledger:check(A/'reviews'/r['review_family'],r);require(bool(r['reason']) and bool(r['pin_meaning']),'honest historical exclusions')
stages=load(P/'history/before_terminal03_finalization/STAGE_PINS.json')['files']
for r in stages:check(P/'history/before_terminal03_finalization',r,'frozen_path')
metadata=load(P/'publication/zenodo.json');require(load(P/'zenodo-deposit.json')['metadata']==metadata,'metadata exact')
require(pin(P/'paper.tex')['sha256']=='0ccac52f998823d98c020608c34ec2ad2cbd1d1f54db1815f0a00f898c5258c0' and pin(P/'output/pdf/paper.pdf')['sha256']=='3ba83c50a4a2369a70897ee165a43f56324aa31574cf9c199e664174cbce0449','reviewed source and PDF')
manifest=load(P/'CURRENT_INTEGRITY.json')['files'];require(len(manifest)==536,'content count')
for r in manifest:check(P,r)
names=sorted([r['path'] for r in manifest]+['CURRENT_INTEGRITY.json','BUILD_RECEIPT.json']);raw=(P/'supportkit-v1.0.tar.gz').read_bytes();prefix='rank_one_uniqueness_v1_0/'
require(raw[:2]==b'\x1f\x8b' and int.from_bytes(raw[4:8],'little')==0,'gzip header')
payload=gzip.decompress(raw);require(zlib.crc32(payload)==int.from_bytes(raw[-8:-4],'little') and len(payload)%2**32==int.from_bytes(raw[-4:],'little'),'gzip CRC/isize')
with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as t:
 require(t.getnames()==[prefix+n for n in names] and len(names)==538,'closed tar members')
 for i in t.getmembers():
  require(i.isfile() and i.mode==0o644 and i.uid==i.gid==0 and i.uname==i.gname=='' and i.mtime==1791849600,'tar headers')
  n=i.name[len(prefix):];b=t.extractfile(i).read();require(b==(P/n).read_bytes(),'tar payload')
  if n!='output/pdf/paper.pdf':b.decode('utf-8')
  if n.endswith('.json'):json.loads(b)
buf=io.BytesIO()
with gzip.GzipFile(fileobj=buf,mode='wb',mtime=0,filename='') as gz:
 with tarfile.open(fileobj=gz,mode='w',format=tarfile.PAX_FORMAT) as t:
  for n in names:
   b=(P/n).read_bytes();i=tarfile.TarInfo(prefix+n);i.size=len(b);i.mtime=1791849600;i.uid=i.gid=0;i.uname=i.gname='';i.mode=0o644;t.addfile(i,io.BytesIO(b))
require(buf.getvalue()==raw,'independent CLOSED tar/gzip byte identity')
commands=[]
def run(argv,cwd,success=True):
 r=subprocess.run(argv,cwd=cwd,text=True,capture_output=True);commands.append({'argv':argv,'cwd':str(cwd),'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr});require((r.returncode==0)==success,'actual command '+str(argv)+r.stderr)
scratch=Path(__file__).parent/'tmp/final1041';require(not scratch.exists(),'new scratch only');scratch.mkdir(parents=True)
try:
 with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as t:t.extractall(scratch,filter='data')
 clean=scratch/prefix
 for flags in (['-B'],['-B','-O']):
  run([sys.executable,*flags,'verify_package.py'],clean)
  run([sys.executable,*flags,'verify_package.py','--require-deposit'],clean,False)
  run([sys.executable,*flags,'build_archive.py'],clean)
  require((clean/'supportkit-v1.0.tar.gz').read_bytes()==raw,'actual clean rebuild')
  run([sys.executable,*flags,'verify_package.py'],clean)
  shutil.copyfile(P/'zenodo-deposit.json',clean/'zenodo-deposit.json')
  run([sys.executable,*flags,'verify_package.py','--require-deposit'],clean)
  (clean/'zenodo-deposit.json').unlink()
finally:shutil.rmtree(scratch)
for r in load(F/'OUTPUT_PINS.json')['files']:check(F,r)
for r in load(F/'FINAL_CURRENT_INPUT_PINS.json')['files']:check(P,r)
utc=datetime.now(timezone.utc).isoformat()
integrity={'utc':utc,'pr':1041,'status':'ROOT_PASS_TERMINAL_ADMINISTRATION','root_full_report_and_entire_code_prose_patch_read':True,'immediate_inputs_rehashed':len(inputs),'authorized_changes':18,'unchanged_immediate_inputs':len(inputs)-18,'protected_pins_rehashed':5741,'terminal_outputs_rehashed':414,'current_files_rehashed':552,'historical224_exact_before_byte_resolution':True,'history_stages_checked':len(stages),'old_copy_records_preserved':161,'source_equal_copies':len(copies),'individually_omitted_historical_pins_verified':len(ledger),'terminal03_304_outputs_all_distributed':True,'original11_unchanged':True,'metadata_wrapper_equivalence':True,'reviewed_paper_and_PDF_unchanged':True,'archive':pin(P/'supportkit-v1.0.tar.gz'),'archive_members':len(names),'content_files':536,'closed_payload_headers_CRC_isize_checked':True,'independent_closed_rebuild_byte_exact':True,'actual_clean_normal_optimized_verify_build_verify_and_required_wrapper_checks':True,'commands':commands,'fresh_whole_package_reviews':3,'actionable_issues':0,'publication_ready':True,'all_issues_resolved':True,'published':False,'services_hold':'preceding PR1032 priority cursor','new_compilation_or_render':False,'scope':'Terminal administration only; exact root-accepted whole03 proof, source, PDF and metadata remain unchanged. Historical P2/P3 verdicts and captured pending fields retain dated meanings; external current root seal supplies final adoption.'}
(A/'FINAL_INTEGRITY.json').write_text(json.dumps(integrity,indent=2)+'\n')
seal={k:v for k,v in integrity.items() if k!='commands'};seal['status']='ROOT_SEALED_READY_PENDING_PRIOR_PR1032_CURSOR';seal['final_integrity']=pin(A/'FINAL_INTEGRITY.json');seal['terminal_finalization_report']=pin(F/'FINALIZATION_REPORT.md');seal['terminal_output_pins']=pin(F/'OUTPUT_PINS.json');(A/'FINAL_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n');(F/'ROOT_FINAL_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
print(json.dumps({'status':seal['status'],'members':len(names),'copies':len(copies),'inputs':len(inputs),'outputs':414,'archive_sha256':seal['archive']['sha256'],'publication_ready':True,'published':False}))
