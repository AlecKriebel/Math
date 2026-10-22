#!/usr/bin/env python3
"""Replay diagnostics and deterministically rebuild source/Zenodo kit. Never publish."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
HERE=Path(__file__).resolve().parent
PREFIX='draft_pr_actual_claims_1100_1200_20261017/audits/pr1141_30006210'
AUDIT=HERE/PREFIX if (HERE/PREFIX).is_dir() else HERE.parent
PDF='polynomial-compatibility.pdf';SOURCE='polynomial-compatibility-source-and-verification.zip'
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def encoded(d):return (json.dumps(d,indent=2,sort_keys=True)+'\n').encode()
def archive(path,members):
 path.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as z:
  for n,b in sorted(members.items()):
   info=zipfile.ZipInfo(n,(2026,10,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,b)
def main():
 allowed=json.loads((HERE/'verification/AUDIT_MEMBERS.json').read_text());qa=json.loads((AUDIT/'ROOT_PDF_QA.json').read_text());pdf=HERE/'output/pdf'/PDF
 if pin(HERE/'main.tex')!=qa['source'] or pin(pdf)!=qa['pdf'] or qa['pages']!=4:raise RuntimeError('PDF QA pins')
 if not pdf.read_bytes().startswith(b'%PDF-'):raise RuntimeError('PDF magic')
 meta=json.loads((HERE/'zenodo-metadata.json').read_text());dep=json.loads((HERE/'zenodo-deposit.json').read_text())
 if dep['metadata']!=meta:raise RuntimeError('Metadata mismatch')
 checked=subprocess.run([sys.executable,'-B',str(HERE/'verification/verify_all.py')],capture_output=True,text=True)
 if checked.returncode:raise RuntimeError(checked.stderr)
 replay=json.loads(checked.stdout)
 if replay['status']!='PASS' or len(replay['runs'])!=8 or len(replay['actual_failure_guards'])!=40:raise RuntimeError('Incomplete replay')
 # The original replay receipt is frozen input. Fresh runtime fields cannot
 # change the release; every mathematical field was separately replayed above.
 members={}
 def add(name,path):
  if name in members or Path(name).is_absolute() or '..' in Path(name).parts or path.is_symlink():raise RuntimeError('Unsafe member '+name)
  members[name]=path.read_bytes()
 for n in ['main.tex','README.md','LICENSE.txt','zenodo-metadata.json','zenodo-deposit.json','build_package.py','output/pdf/'+PDF,'verification/verify_all.py','verification/AUDIT_MEMBERS.json','verification/CONTROL_PLAN.json','verification/REPLAY_RECEIPT.json']:add(n,HERE/n)
 for n,want in allowed.items():
  f=AUDIT/n
  if pin(f)!=want:raise RuntimeError('Audit pin changed '+n)
  add(PREFIX+'/'+n,f)
 members['PROVENANCE.json']=encoded({'source_pr':'https://github.com/AlecKriebel/Math/pull/1141','source_head':'b1d6bc6ceb66e9c9c98cfae229ee86e5720799e2','source_proof_sha256':'20bf5956520b2b53bb4b415d7d5683a6ae1cf1273bd36372accbc49fab482da1','problem':'30006210 / OWR-14299088-012; Austrin OWR9/2025 p445','claim':'Complete affirmative exact two-real-polynomial uniform Boolean cube deduction: all relative influences<=1/(4096d^8) suffice; disjointness requires maximum>=1/(1024d^8); full squared Fourier norm including constant.','established_inputs':'Li-Li-Li-Liu2026 Lem3.5 separator; OSSS2005 section3.3 Eq6 arbitrary-real covariance; classical Markov/Bernoulli credited through Kothari et al. No new generic separator or covariance theorem.','priority':'Bounded primary audit found no earlier recorded full target-specific deduction in inspected bodies. No novelty, firstness or global-openness certificate; unread full ePrint2022/218,2023/570 and other exact scope limits documented.','historical_editions':'Ten original artifacts unchanged. Current paper/root decision supersede older citation inventories by explicitly crediting OSSS and distributing new exact code. Historical custody pins are records at their timestamps, not current release manifests.','independence':'Three mathematical families; three priority approaches. Precise limited source/snippet and post-core old-audit exposures are disclosed in reports. No external human review.','archive_layout':'Original audit prefix preserved for unmodified historical path lookup; private source bodies/extracts/heading scans/raw APIs/renders excluded.','verification':'Four stdlib exact-integer/rational mathematical checkers ordinary/optimized, all mathematical output fields exact and40 actual wrong-result failures. Finite diagnostics supplement written universal proof, not formal certification.','review_status':'Extensive AI assistance; unrefereed; no external human peer review, journal acceptance or proof-assistant certification.'})
 manifest={n:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(members.items())};members['SOURCE_MANIFEST.json']=encoded(manifest)
 out=HERE/'output';archive(out/SOURCE,members)
 portable=dict(dep);portable['files']=[{'path':PDF},{'path':SOURCE}]
 archive(out/'zenodo-upload-kit.zip',{PDF:pdf.read_bytes(),SOURCE:(out/SOURCE).read_bytes(),'README.md':members['README.md'],'zenodo-metadata.json':members['zenodo-metadata.json'],'zenodo-deposit.json':encoded(portable)})
 files=['main.tex','output/pdf/'+PDF,'output/'+SOURCE,'output/zenodo-upload-kit.zip','zenodo-metadata.json','zenodo-deposit.json']
 receipt={'files':{n:pin(HERE/n) for n in files},'source_members':manifest,'source_members_including_manifest':len(members),'kit_members':5,'operative_paper_pages':4,'verifiers':'Four standard-library exact mathematical programs in both ordinary and optimized modes, all mathematical fields exact, forty actual failure guards.'}
 (HERE/'PACKAGE_RECEIPT.json').write_bytes(encoded(receipt));print(json.dumps({k:v for k,v in receipt.items() if k!='source_members'},indent=2))
if __name__=='__main__':main()
