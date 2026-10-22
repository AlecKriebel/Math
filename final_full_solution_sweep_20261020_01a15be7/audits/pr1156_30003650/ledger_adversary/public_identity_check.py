#!/usr/bin/env python3
"""Read-only public API and payload identity verification."""
import concurrent.futures,datetime as dt,hashlib,io,json,stat,urllib.request,zipfile
from pathlib import Path,PurePosixPath
D=Path(__file__).resolve().parent;P=D/'private';A=D.parent
plan=json.loads((A/'LEDGER_RECONCILIATION_PLAN.json').read_text())
def get(url):
 req=urllib.request.Request(url,headers={'User-Agent':'Independent-ledger-review/1.0'})
 with urllib.request.urlopen(req,timeout=45) as r:return r.read(),{'status':r.status,'final_url':r.url}
wire,meta=get('https://zenodo.org/api/records/23350364');record=json.loads(wire)
(P/'public_record_fresh.json').write_bytes(wire)
base=json.loads((A.parents[1]/'raw/pr1156/zenodo_23350364.json').read_text())
if record['metadata']!=base['metadata']:raise RuntimeError('metadata changed')
checks=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 futures={f['key']:pool.submit(get,f['links']['self']) for f in record['files']}
 for f in record['files']:
  body,resolution=futures[f['key']].result();expected=next(x for x in plan['existing_publication']['files'] if x['name']==f['key'])
  item={'name':f['key'],'bytes':len(body),'md5':'md5:'+hashlib.md5(body).hexdigest(),'sha256':hashlib.sha256(body).hexdigest(),'resolution':resolution}
  if item['bytes']!=expected['size'] or item['md5']!=f['checksum'] or item['md5']!=expected['checksum'] or item['sha256']!=expected['sha256']:raise RuntimeError('payload mismatch')
  (P/('public_'+f['key'])).write_bytes(body)
  checks.append(item)
_,doi=get('https://doi.org/10.5281/zenodo.23350364')
if doi!={'status':200,'final_url':'https://zenodo.org/records/23350364'}:raise RuntimeError('DOI mismatch')
with zipfile.ZipFile(io.BytesIO((P/'public_source.zip').read_bytes())) as z:
 names=z.namelist()
 if len(set(names))!=18 or len(names)!=18 or z.testzip() is not None:raise RuntimeError('archive inventory')
 for f in z.infolist():
  p=PurePosixPath(f.filename)
  if p.is_absolute() or any(x in ('','.','..') for x in f.filename.split('/')) or '\\' in f.filename or f.is_dir() or stat.S_ISLNK(f.external_attr>>16):raise RuntimeError('unsafe archive')
  z.read(f)
 m=json.loads(z.read('source-archive-manifest.json'))
 (P/'archive_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 for name in ['main.tex','source_and_novelty_review.md','reproducibility/complete_proof.md','reproducibility/canonical_statement.md']:
  (P/('source_'+name.replace('/','_'))).write_bytes(z.read(name))
summary={'at':dt.datetime.now(dt.timezone.utc).isoformat(),'record':record['id'],'doi':record['doi'],'conceptdoi':record['conceptdoi'],'state':record['state'],'submitted':record['submitted'],'metadata_equal_reviewed_baseline':True,'title':record['metadata']['title'],'creators':record['metadata']['creators'],'version':record['metadata']['version'],'publication_date':record['metadata']['publication_date'],'files':checks,'doi_resolution':doi,'archive_members':len(names),'archive_unique_safe_crc':True}
(D/'PUBLIC_IDENTITY_RECEIPT.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
