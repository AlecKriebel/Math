"""Independent byte-binding checks only; does not execute mathematical support."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, re
R=Path(__file__).resolve().parent
B=R.parents[1]
S=B/'sources'
P=S/'published-source/K2P_SAME_Reproducibility_Package_v1.0.5-r1/k2p_same_reproducibility_v1.0.5-r1'
checks=[]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(label,passed,**kw):checks.append({'check':label,'pass':bool(passed),**kw})
receipt=json.loads((S/'receipt.json').read_text())
check('complete seven-file receipt',receipt['complete'] and len(receipt['files'])==7)
for a in receipt['files']:
 p=S/a['name'];check('public file size/SHA256/MD5',p.stat().st_size==a['bytes'] and digest(p)==a['sha256'] and hashlib.md5(p.read_bytes()).hexdigest()==a['md5'],path=a['name'])
for l in (S/'SHA256SUMS').read_text().splitlines():
 h,n=l.split(maxsplit=1);n=n.lstrip('*');check('published SHA256SUMS',digest(S/n)==h,path=n)
manifest=json.loads((P/'ZENODO_REPRODUCIBILITY_MANIFEST.json').read_text())
expected=set(manifest['files'])|{'ZENODO_REPRODUCIBILITY_MANIFEST.json'}
actual={str(x.relative_to(P))for x in P.rglob('*')if x.is_file()}
check('repro manifest exact file universe',actual==expected,expected=len(expected),actual=len(actual),missing=sorted(expected-actual),extra=sorted(actual-expected))
for name,a in manifest['files'].items():
 p=P/name;check('repro internal manifest size/SHA256',p.stat().st_size==a['bytes'] and digest(p)==a['sha256'],path=name)
check('repro internal total bytes',sum((P/n).stat().st_size for n in manifest['files'])==manifest['total_bytes_excluding_manifest'])
cross=json.loads((P/'proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json').read_text())
for c in cross['claims']:
 for field in ['authoritative_artifacts','producer_artifacts','replay_artifacts','mutation_artifacts']:
  for a in c.get(field,[]):
   p=P/a['path'];check('crosswalk declared artifact size/SHA256',p.exists() and p.stat().st_size==a['bytes'] and digest(p)==a['sha256'],path=a['path'],claim=c['claim_id'],role=field)
small=S/'published-source/K2P_SAME_bioRxiv_Source_20260829'
for f in small.rglob('*'):
 if f.is_file():
  other=P/'proof_compression_submission'/f.relative_to(small)
  check('small and complete source ZIP content identity',other.exists() and digest(f)==digest(other),path=str(f.relative_to(small)))
for name in ['K2P_SAME_Principal_Domain_Article.pdf','K2P_SAME_Reader_Supplement.pdf']:
 hits=[f for f in P.rglob('*.pdf')if digest(f)==digest(S/name)]
 check('public PDF appears byte-identically in complete package',len(hits)>0,path=name,matches=[str(x.relative_to(P))for x in hits])
# Compare complete two-paragraph abstract, converting only the literal mathematical
# display/delimiters and Unicode typography used on the candidate page.
src=small/'article/main.tex'
a=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',src.read_text(),re.S).group(1)
a=re.sub(r'\\\[\s*\\Dplus=.*?\\\]', 'D₊ = {(s, g) : 0 < s < 1, 0 < g < 1, g > 2s − 1},',a,flags=re.S)
a=a.replace(r'\(\mathcal T_i\)','Tᵢ').replace(r'\(0<s<1,\ s^2<g<1\)','0 < s < 1, s² < g < 1').replace(r'\(n\ge3\)','n ≥ 3').replace(r'\(4n-3\)','4n − 3')
a='\n\n'.join(' '.join(x.split())for x in re.split(r'\n\s*\n',a.strip()))
content=json.loads((R/'content.json').read_text())
check('complete two-paragraph source abstract',a==content['abstract'],source_sha256=digest(src),paragraph_count=len(a.split('\n\n')))
report={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'source_receipt_sha256':digest(S/'receipt.json'),'checks':checks,'passed':sum(c['pass']for c in checks),'failed':[c for c in checks if not c['pass']],'mathematical_code_executed':False,'scope':'byte integrity, artifact presence and exact abstract transcription only'}
(R/'source-package-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'passed':report['passed'],'failed':report['failed'],'mathematical_code_executed':False},indent=2))
raise SystemExit(bool(report['failed']))
