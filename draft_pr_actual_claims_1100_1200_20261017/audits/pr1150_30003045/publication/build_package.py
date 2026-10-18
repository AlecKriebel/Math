#!/usr/bin/env python3
"""Verify and deterministically rebuild the source archive and portable Zenodo kit."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile,zipfile
HERE=Path(__file__).absolute().parent
PREFIX='draft_pr_actual_claims_1100_1200_20261017/audits/pr1150_30003045'
AUDIT=HERE/PREFIX if (HERE/PREFIX).is_dir() else HERE.parent
PDF='mixed-kato-counterexample.pdf';SOURCE='mixed-kato-counterexample-source-and-verification.zip'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def safe(p):
 p=p.absolute()
 for root in (HERE,AUDIT):
  try:rel=p.relative_to(root)
  except ValueError:continue
  need('..' not in rel.parts,'unsafe path '+str(p))
  cursor=root;need(not cursor.is_symlink(),'symlink root '+str(cursor))
  for part in rel.parts:
   cursor=cursor/part;need(not cursor.is_symlink(),'symlink ancestor/member '+str(cursor))
  return p
 raise ValueError('path outside distribution roots '+str(p))
def pin(p):
 p=safe(p);need(p.is_file(),'missing file '+str(p));b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def encoded(o):return (json.dumps(o,indent=2,sort_keys=True,ensure_ascii=False)+'\n').encode()
def atomic_bytes(path,data):
 safe(path);path.parent.mkdir(parents=True,exist_ok=True);temporary=None
 try:
  with tempfile.NamedTemporaryFile(dir=path.parent,prefix='.'+path.name+'.',delete=False) as f:
   temporary=Path(f.name);f.write(data)
  safe(path);os.replace(temporary,path)
 finally:
  if temporary is not None and temporary.exists():temporary.unlink()
def archive(path,members):
 safe(path);path.parent.mkdir(parents=True,exist_ok=True);temporary=None
 try:
  with tempfile.NamedTemporaryFile(dir=path.parent,prefix='.'+path.name+'.',delete=False) as f:
   temporary=Path(f.name)
   with zipfile.ZipFile(f,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for n,b in sorted(members.items()):
     need(not Path(n).is_absolute() and '..' not in Path(n).parts,'unsafe archive member');i=zipfile.ZipInfo(n,(2026,10,17,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o644<<16;z.writestr(i,b)
  safe(path);os.replace(temporary,path)
 finally:
  if temporary is not None and temporary.exists():temporary.unlink()

def main():
 for destination in [HERE/'output'/SOURCE,HERE/'output/zenodo-upload-kit.zip',HERE/'PACKAGE_RECEIPT.json']:safe(destination)
 pin(HERE/'verification/AUDIT_MEMBERS.json');pin(HERE/'verification/CONTROL_PLAN.json');allowed=json.loads((HERE/'verification/AUDIT_MEMBERS.json').read_text());pin(AUDIT/'ROOT_PDF_QA.json');qa=json.loads((AUDIT/'ROOT_PDF_QA.json').read_text());pdf=HERE/'output/pdf'/PDF
 need(pin(HERE/'main.tex')==qa['source'] and pin(pdf)==qa['pdf'] and qa['pages']==4,'PDF/source QA mismatch');need(pdf.read_bytes().startswith(b'%PDF-'),'PDF magic')
 meta=json.loads((HERE/'zenodo-metadata.json').read_text());dep=json.loads((HERE/'zenodo-deposit.json').read_text());need(dep['metadata']==meta,'metadata differ');need(dep['files']==[{'path':'output/pdf/'+PDF},{'path':'output/'+SOURCE}],'deposit file contract')
 r=subprocess.run([sys.executable,'-B',str(HERE/'verification/verify_all.py')],capture_output=True);need(r.returncode==0 and not r.stderr,'portable diagnostics failed '+r.stderr.decode());replay=json.loads(r.stdout);need(replay==json.loads((HERE/'verification/REPLAY_RECEIPT.json').read_text()),'complete replay mismatch')
 need(replay['status']=='PASS' and len(replay['runs'])==4 and len(replay['actual_wrong_result_failures'])==18,'incomplete verification')
 members={}
 def add(n,p):
  need(n not in members and not Path(n).is_absolute() and '..' not in Path(n).parts,'unsafe/duplicate '+n);pin(p);members[n]=p.read_bytes()
 for n in ['main.tex','README.md','LICENSE.txt','zenodo-metadata.json','zenodo-deposit.json','build_package.py','output/pdf/'+PDF,'verification/verify_all.py','verification/AUDIT_MEMBERS.json','verification/CONTROL_PLAN.json','verification/REPLAY_RECEIPT.json']:add(n,HERE/n)
 for n,want in allowed.items():
  need(pin(AUDIT/n)==want,'audit member changed '+n);add(PREFIX+'/'+n,AUDIT/n)
 members['PROVENANCE.json']=encoded({'source_pr':'https://github.com/AlecKriebel/Math/pull/1150','original_head':'99f43020e142374629848e97113d354b43fd9f8e','reviewed_head':'4e8e5db5c47fb879d97cb1a734a76fd59d8f633a','operative_proof_sha256':'7808df31d74049fe649231a905e6dc330929caa87c86dca6ebfa6dcfb6d6c275','claim':'Explicit negative answer to original three-summand equality at n1; positive n0 boundary; degree4 exponent2, binary bilinear Pfister anisotropic L; all-three-kernel norm-residue exclusion','antecedent':'Exact ALO2019 Definition1.3/Lemma3.1/Theorem1.4 mixed-generator specialization credited; no new generic mixed mechanism or firstness claim','repairs':'Auxiliary exponent-one shortcut replaced by L+K sum membership; attribution paragraph strengthened; package01 flat/ancestor symlink guards, standalone proof reference, intermediate/final proof label and Milne item-label repaired; package02 builder outputs preflighted before any write and generated archives/receipt atomically replaced. Historical original inputs/old acceptance preserved only as superseded timestamped evidence.','priority_limits':'Bounded168queryinputs including overlaps, four approaches; inaccessible final mixed typeset and adjacent nonnormal2020/transfer2022 bodies; no novelty, firstness, global-openness or causal-independence certificate.','review_limits':'Initial6families inherited parent history; no perfect isolation claim. New final complete-package reviews recorded separately outside frozen archive. Extensive AI assistance; unrefereed, no external human peer review or proof-assistant certification.','verification':'Two exact stdlib programs,4ordinary/optimized complete-output matches,18actual wrong-result failures. Finite diagnostic support, not Kato decision oracle.','distribution':'Third-party bodies/extracts/renders/rawservice returns excluded. Authored source/byte metadata and historical custody receipts retained; private-source custody rechecks require independently obtaining sources.','archive_rule':'Explicit frozen authored allowlist. Future operations/reviews/log changes cannot silently enter the release.'})
 manifest={n:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(members.items())};members['SOURCE_MANIFEST.json']=encoded(manifest);out=HERE/'output';archive(out/SOURCE,members)
 portable=dict(dep);portable['files']=[{'path':PDF},{'path':SOURCE}]
 archive(out/'zenodo-upload-kit.zip',{PDF:pdf.read_bytes(),SOURCE:(out/SOURCE).read_bytes(),'README.md':members['README.md'],'zenodo-metadata.json':members['zenodo-metadata.json'],'zenodo-deposit.json':encoded(portable)})
 names=['main.tex','output/pdf/'+PDF,'output/'+SOURCE,'output/zenodo-upload-kit.zip','zenodo-metadata.json','zenodo-deposit.json'];receipt={'files':{n:pin(HERE/n) for n in names},'source_members':manifest,'source_members_including_manifest':len(members),'kit_members':5,'operative_paper_pages':4,'verification':'Two stdlib exact algebra programs normal/optimized;4complete outputs and18actual wrong-result failures; historical13/25absent programs not represented as rerun.'};atomic_bytes(HERE/'PACKAGE_RECEIPT.json',encoded(receipt));print(json.dumps({k:v for k,v in receipt.items() if k!='source_members'},indent=2))
if __name__=='__main__':main()
