#!/usr/bin/env python3
"""Rebuild the authored source archive and upload kit; never recompile or publish."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
HERE=Path(__file__).resolve().parent
PREFIX='draft_pr_actual_claims_1100_1200_20261017/audits/pr1136_2307037'
AUDIT=HERE/PREFIX if (HERE/PREFIX).is_dir() else HERE.parent
PDF='fixed-area-squared-poles.pdf';SOURCE='fixed-area-squared-poles-source-and-verification.zip'
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def encoded(d):return (json.dumps(d,indent=2,sort_keys=True)+'\n').encode()
def archive(path,members):
 path.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as z:
  for n,b in sorted(members.items()):
   info=zipfile.ZipInfo(n,(2026,10,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,b)
def main():
 allowed=json.loads((HERE/'verification/AUDIT_MEMBERS.json').read_text())
 qa=json.loads((AUDIT/'ROOT_PDF_QA.json').read_text());pdf=HERE/'output/pdf'/PDF
 if pin(HERE/'main.tex')!=qa['source'] or pin(pdf)!=qa['pdf'] or qa['pages']!=4:raise RuntimeError('PDF QA pins')
 if not pdf.read_bytes().startswith(b'%PDF-'):raise RuntimeError('PDF magic')
 meta=json.loads((HERE/'zenodo-metadata.json').read_text());dep=json.loads((HERE/'zenodo-deposit.json').read_text())
 if dep['metadata']!=meta:raise RuntimeError('Metadata mismatch')
 checked=subprocess.run([sys.executable,'-B',str(HERE/'verification/verify_all.py')],capture_output=True,text=True)
 if checked.returncode:raise RuntimeError(checked.stderr)
 # Replay output may contain runtime metadata; frozen original receipt remains an
 # archive input. A rebuild checks its complete content through the runner.
 replay=json.loads(checked.stdout)
 if replay['status']!='PASS':raise RuntimeError('Replay')
 members={}
 def add(name,path):
  if name in members or Path(name).is_absolute() or '..' in Path(name).parts or path.is_symlink():raise RuntimeError('Unsafe member '+name)
  members[name]=path.read_bytes()
 for n in ['main.tex','README.md','LICENSE.txt','zenodo-metadata.json','zenodo-deposit.json','build_package.py','output/pdf/'+PDF,'verification/verify_all.py','verification/AUDIT_MEMBERS.json','verification/CONTROL_PLAN.json','verification/REPLAY_RECEIPT.json']:
  add(n,HERE/n)
 for n,want in allowed.items():
  f=AUDIT/n
  if pin(f)!=want:raise RuntimeError('Audit pin changed '+n)
  add(PREFIX+'/'+n,f)
 members['PROVENANCE.json']=encoded({'source_pr':'https://github.com/AlecKriebel/Math/pull/1136','source_head':'cbbe7826cca914588018c840ba99c6b7a59fa7f5','source_proof_sha256':'32e68249400aad782b77c74405890f9929fc8576ab8a13d59a3b8db75dea9bdc','problem':'2307037 / AMR-022-7037; Hayman–Lingham7.37; Baernstein','claim':'Full affirmative deduction, exact-area compact sameSforallR;2pi leading sharp; additive pi(log2+1/e) not claimed optimal.','priority':'Established EH1995 and LP2009 inputs, recent Lin/Guerra mechanisms credited; no first-priority certification. Leung AMS Abstracts11(1990)p181 and13(1992)p440 bodies restricted/unread; relevance unresolved. Further full/final source gaps documented.','historical_editions':'All twelve source artifacts preserved unchanged; current paper/root decision supersede historical inspection/priority summaries. Historical end pins are records at their timestamps, not release manifests.','archive_layout':'Original audit prefix preserved for unmodified historical utility path lookup. No private full bodies, extracts, raw API responses or renders redistributed.','verification':'Three mathematical programs offline ordinary/optimized; fourth target program optional hash-pinned primary-source download in disposable mirror. Floating results diagnostic, not proof certificates.','review_status':'Extensive AI assistance; unrefereed; no external human peer review, journal acceptance or formal proof-assistant certification.'})
 manifest={n:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(members.items())};members['SOURCE_MANIFEST.json']=encoded(manifest)
 out=HERE/'output';archive(out/SOURCE,members)
 portable=dict(dep);portable['files']=[{'path':PDF},{'path':SOURCE}]
 archive(out/'zenodo-upload-kit.zip',{PDF:pdf.read_bytes(),SOURCE:(out/SOURCE).read_bytes(),'README.md':members['README.md'],'zenodo-metadata.json':members['zenodo-metadata.json'],'zenodo-deposit.json':encoded(portable)})
 files=['main.tex','output/pdf/'+PDF,'output/'+SOURCE,'output/zenodo-upload-kit.zip','zenodo-metadata.json','zenodo-deposit.json']
 receipt={'files':{n:pin(HERE/n) for n in files},'source_members':manifest,'source_members_including_manifest':len(members),'kit_members':5,'operative_paper_pages':4,'verifiers':'Three pinned standard-library mathematical programs ordinary/optimized offline; complete outputs with explicit runtime metadata and floating-diagnostic tolerance. Four actual failing-oracle executions. Fourth source-dependent target program optional.'}
 (HERE/'PACKAGE_RECEIPT.json').write_bytes(encoded(receipt));print(json.dumps({k:v for k,v in receipt.items() if k!='source_members'},indent=2))
if __name__=='__main__':main()
