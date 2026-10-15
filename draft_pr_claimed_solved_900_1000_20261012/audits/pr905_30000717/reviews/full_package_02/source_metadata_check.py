"""Independent final model/metadata/package summary checks, no source copies."""
from pathlib import Path
import json,hashlib,re,datetime,subprocess
HERE=Path(__file__).resolve().parent;AUDIT=HERE.parent.parent;PUB=AUDIT/'publication';ROOT=HERE/'tmp/extracted';results=[]
def req(ok,label):
 if not ok:raise RuntimeError(label)
 results.append(label)
# Exact catalogue IDs inspected in local corpora; do not release selected records.
corpora=[]
for n in ['catalog.json','cache/problems.json']:
 p=Path('/Users/alec/Documents/Math/unsolved_math_prioritization')/n;raw=p.read_bytes();data=json.loads(raw)
 if isinstance(data,dict):
  records=next((v for v in data.values() if isinstance(v,list)),[])
 else:records=data
 matches=[r for r in records if isinstance(r,dict) and str(r.get('problem_id',r.get('id','')))== '30000717']
 req(len(matches)==1,'One exact-ID catalogue record '+n)
 selected=matches[0];(HERE/'private_sources'/('selected_'+Path(n).name)).write_text(json.dumps(selected,indent=2)+'\n')
 text=json.dumps(selected)
 req('OWR-1465-011' in text,'Correct OWR identifier '+n)
 corpora.append({'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'matching_records':1,'selected_record_redistributed':False,'record_keys':list(selected)})
# Active repair present in every summary used for publication.
for n in ['note.tex','README.md','zenodo-deposit.json']:
 s=' '.join((PUB/n).read_text().split()); lower=s.lower()
 req('2010' in s and 'moment-ima-update-new.pdf' in s,'Active dated updated Laurent source '+n)
 req(('6 February 2010' in s) or ('6 February\n2010' in s),'Explicit Laurent date '+n)
 req('2009' in s and ('different Lemma 7.21' in s or 'updated manuscript' in s),'Earlier chapter distinguished '+n)
 req('first' in lower and ('not established' in lower or 'not asserted' in lower or 'no claim' in lower or 'no author-approved formula correction' in lower),'Bounded priority disclosure '+n)
 req('2008' in s and '2009' in s and ('not obtained' in s or 'not obtained;' in s),'Complete HaPham access gap disclosed '+n)
 req(('unrefereed' in s.lower()) and 'human' in s.lower(),'Unrefereed/no human review '+n)
 req('extensive' in s.lower(),'Extensive AI disclosure '+n)
req((ROOT/'SOURCE_VERSION_CORRECTION.md').read_bytes()==(AUDIT/'SOURCE_VERSION_CORRECTION.md').read_bytes(),'Archive includes current source version correction')
req('sealed' in (ROOT/'SOURCE_VERSION_CORRECTION.md').read_text().lower(),'Historical seals expressly qualified')
req((ROOT/'SOURCE_CORRECTION.md').read_bytes()==(AUDIT/'SOURCE_CORRECTION.md').read_bytes(),'Archive includes two-formula qualification')
# Data models and review status.
z=json.loads((PUB/'zenodo-deposit.json').read_text());m=z['metadata']
req(m['upload_type']=='publication' and m['publication_type']=='preprint','Preprint deposit type')
req(m['title']=='A Robinson counterexample to ideal-only tangency certificates','Accurate modest title')
req(m['version']=='1.0' and m['publication_date']=='2026-10-12','Version and publication date')
req(m['access_right']=='open' and m['license']=='cc-by-4.0','Open authored materials/CCBY4')
req(m['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'Author/affiliation/ORCID exact')
req(z['files']==[{'path':'output/pdf/note.pdf','name':'robinson-tangency-certificates-v1.0.pdf'},{'path':'robinson-tangency-source-verification-v1.0.zip'}],'Exactly two deposit file mappings')
req('full ideal' in m['description'] and 'arbitrary degree' in m['description'].lower(),'Full vanishing ideal and unrestricted degree scope')
req('No author-approved formula correction, first bibliographic priority or continued open status' in m['description'],'No unsupported status or normalization promotion')
manifest=json.loads((ROOT/'PACKAGE_MANIFEST.json').read_text())
req(len(manifest['files'])==84,'Exact package payload count')
req(all(Path(n).suffix in ('.json','.md','.py','.tex','.txt') for n in manifest['files']),'Only intentional textual source/verification formats')
req(all(not (ROOT/n).read_bytes().startswith(b'%PDF') for n in manifest['files']),'No disguised primary PDF')
req(all((ROOT/n).read_bytes().decode('utf-8') is not None for n in manifest['files']),'All payloads UTF8')
for n in manifest['files']:
 req(not any(p in Path(n).parts for p in ['private_sources','raw_sources','tmp','__pycache__']), 'No raw/transient archive member '+n)
# Review manifests reference fully included files, not source-assets needed to replay.
for family,key in [('proof_family','artifacts'),('computation_family','files')]:
 p=ROOT/'reviews'/family;m=json.loads((p/'MANIFEST.json').read_text())
 for n,r in m[key].items():
  b=(p/n).read_bytes();req(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'Included sealed review artifact '+family+'/'+n)
# Graph is intentionally metadata-only and equals claimed cardinality.
g=json.loads((ROOT/'reviews/priority_family/CITATION_GRAPH.json').read_text());
req(g['distinct_count']==66 and len(g['records'])==66,'Citation metadata graph cardinality66')
# Compile output mathematical text agrees with released PDF. PDF bytes may differ by creation time.
subprocess.run(['pdftotext','-layout',str(HERE/'tmp/standalone/note.pdf'),str(HERE/'tmp/standalone/note.txt')],check=True)
req((HERE/'tmp/standalone/note.txt').read_bytes()==(HERE/'tmp/pdf_text.txt').read_bytes(),'Standalone compiled PDF text equals released PDF')
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':results,'check_count':len(results),'catalogue':corpora,'source_versions':'Active2010 update dated and linked; earlier chapter context; archived sealed labels globally qualified.','access_gaps':'Complete2008/2009 HaPham texts still unavailable; no inference of first priority/current open status.','pdf_visual_pages':[1,2,3,4],'standalone_compile':'PASS; extracted text identical','public_source_asset_redistribution':False,'no_external_human_contact':True}
(HERE/'evidence/source_metadata_package_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','check_count':len(results)},indent=2))
