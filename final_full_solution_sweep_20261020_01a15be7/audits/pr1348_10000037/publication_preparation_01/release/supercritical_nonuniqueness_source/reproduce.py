# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Alec Kriebel
"""Verify this closed scientific source package offline, without writing files."""
from pathlib import Path
import json,hashlib,subprocess,sys
P=Path(__file__).resolve().parent
def need(p,m):
 if not p:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 m=json.loads((P/'PUBLIC_MANIFEST.json').read_bytes());want=m['files']
 actual={p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file() and p!=P/'PUBLIC_MANIFEST.json'}
 need(actual==set(want),'closed scientific member set changed')
 for n,z in want.items():
  f=P/n;need(not f.is_symlink(),'symlink');b=f.read_bytes();need(len(b)==z['bytes'] and sha(b)==z['sha256'],'sealed bytes '+n)
 results={}
 for script,expected in [('exact_checks.py','EXPECTED.json')]:
  wanted=(P/'verification'/expected).read_bytes();outs=[]
  for flags in [[],['-O'],['-OO']]:
   r=subprocess.run([sys.executable,'-B',*flags,str(P/'verification'/script)],capture_output=True)
   need(r.returncode==0,'checker failed '+script);need(r.stdout==wanted,'expected output mismatch '+script);outs.append(r.stdout)
  need(len(set(outs))==1,'optimized-mode mismatch');results[script]={'sha256':sha(wanted),'summary':json.loads(wanted)}
 b=json.loads((P/'BUILD_RECEIPT.json').read_bytes());need(sha((P/'main.tex').read_bytes())==b['source_sha256'],'TeX source provenance');need(sha((P/'paper.pdf').read_bytes())==b['pdf_sha256'],'PDF provenance')
 metadata=json.loads((P/'zenodo-metadata.json').read_bytes());deposit=json.loads((P/'zenodo-deposit.json').read_bytes())
 need(deposit['metadata']==metadata,'metadata/deposit mismatch')
 need(metadata['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'author identity')
 need(metadata['publication_date']=='2026-10-22' and metadata['version']=='1.0.0' and metadata['license']=='cc-by-4.0','date/version/license')
 need('doi' not in metadata and 'prereserve_doi' not in metadata,'no reserved DOI')
 need([x['path'] for x in deposit['files']]==['supercritical-nonuniqueness.pdf','supercritical-nonuniqueness-source-and-verification.zip'],'two scientific upload names')
 print(json.dumps({'status':'PASS','scope':'closed package and finite mechanisms only; universal theorem rests on written proof','publication_performed':False,'results':results,'tex_sha256':b['source_sha256'],'pdf_sha256':b['pdf_sha256']},sort_keys=True,indent=2))
if __name__=='__main__':main()
