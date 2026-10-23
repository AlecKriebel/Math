"""Independent read-only local PR1131 payload/ZIP custody check, not publication."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7')
P=R/'audits/pr1131_30005455/operations/proposed/preprint'
def sha(b):return hashlib.sha256(b).hexdigest()
def strict(b):
 def pairs(v):
  d={}
  for k,x in v:
   assert k not in d;d[k]=x
  return d
 return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in()).throw(RuntimeError('Nonfinite JSON')))
def main():
 expected=[{'name':'finite-warm-thresholds.pdf','bytes':91613,'sha256':'42c5c632de7e942df6b7c407fb95d877a165281f215e4aa7d1dfa862b08b2157','md5':'845715d7fffb5aba43baddb039692933'},{'name':'finite-warm-thresholds-source-and-verification.zip','bytes':211840,'sha256':'e92f6fa13245686525a0dd8fc4c5327bd03e58a1f02ae7dcae918668c16c5fee','md5':'513e0c50bc16dfe669473fb83695dbca'}]
 for x in expected:
  p=P/x['name'];assert not any(q.is_symlink()for q in[p,*p.parents]);b=p.read_bytes()
  assert len(b)==x['bytes']and sha(b)==x['sha256']and hashlib.md5(b).hexdigest()==x['md5']
 pdf=(P/expected[0]['name']).read_bytes();assert pdf.startswith(b'%PDF-')and b'%%EOF'in pdf[-40:]
 manifest=(P/'zenodo-deposit.json').read_bytes();assert sha(manifest)=='0ca12e07eee0ed88da4f94b82a2404eed4341aaa1f08f9100ecb630014fed6fe';m=strict(manifest)
 assert [x['path']for x in m['files']]==[x['name']for x in expected]
 assert m['metadata']['creators'][0]['orcid']=='0009-0001-9320-500X'and m['metadata']['publication_type']=='preprint'
 assert 'AI tools were extensively involved'in m['metadata']['description']and 'not formal independent human peer review'in m['metadata']['description']
 with zipfile.ZipFile(P/expected[1]['name'])as z:
  ns=z.namelist();assert len(ns)==len(set(ns))==45
  assert all(not PurePosixPath(n).is_absolute()and'..'not in PurePosixPath(n).parts for n in ns)
  assert z.testzip()is None
  mf=strict(z.read('SOURCE_MANIFEST.json'));assert set(mf)==set(ns)-{'SOURCE_MANIFEST.json'}
  for name,pin in mf.items():
   b=z.read(name);assert pin=={'bytes':len(b),'sha256':sha(b)}
  assert z.read('output/pdf/finite-warm-thresholds.pdf')==pdf
  assert strict(z.read('zenodo-deposit.json'))['metadata']==m['metadata']
  size=sum(i.file_size for i in z.infolist())
 return {'status':'PASS_PRIMARY_LOCAL_PR1131_PAYLOAD_AND_COMPLETE_ARCHIVE_MANIFEST','files':expected,'source_ZIP_members':45,'complete_internal_manifest_files':len(mf),'all_ZIP_CRCs':True,'all_internal_sizes_and_SHA256':True,'uncompressed_bytes':size,'embedded_and_external_PDF_identical':True,'embedded_and_external_publication_metadata_identical':True,'canonical_manifest_sha256':sha(manifest),'scope':'Local custody/integrity and declared metadata only; no proof/novelty replay, Zenodo observation, reserved-DOI publication or final clearance.','actual_service_effects':0,'final_clearance':False}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))
