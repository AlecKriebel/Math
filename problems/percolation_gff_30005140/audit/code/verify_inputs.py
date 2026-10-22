#!/usr/bin/env python3
"""Recompute public input bindings from caller-supplied files; emit no source content."""
import argparse,hashlib,json
from pathlib import Path

def meta(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 p=argparse.ArgumentParser(description=__doc__)
 for k in ['catalog','problems','research','pdf-dir','author-zip']:p.add_argument('--'+k,type=Path)
 a=p.parse_args();root=Path(__file__).resolve().parents[1];e=json.loads((root/'PROVENANCE_AUDIT.json').read_text());out={}
 if a.author_zip:
  assert meta(a.author_zip.read_bytes())==e['author_zip'];out['author_zip']='PASS'
 if any([a.catalog,a.problems,a.research]):
  if not all([a.catalog,a.problems,a.research]):p.error('Supply all of --catalog --problems --research.')
  loaded={}
  for name,path in [('catalog.json',a.catalog),('problems.json',a.problems),('research_results.json',a.research)]:
   b=path.read_bytes();assert meta(b)==e['corpora'][name]['file'];j=json.loads(b)
   assert len(j)==e['corpora'][name]['record_count'];loaded[name]=j
  ps=loaded['problems.json'];rs=loaded['research_results.json'];cs=loaded['catalog.json']
  selected=[x for x in ps if str(x.get('id'))=='30005140'];cats=[x for x in cs if str(x.get('id'))=='30005140']
  assert len(selected)==len(cats)==1
  item,cat=selected[0],cats[0];assert item['problem_number']=='OWR-10252936-003' and cat['rank']==791
  assert sum(x['problem_number']==item['problem_number'] for x in ps)==1
  assert item['problem_number'] not in rs
  sh=hashlib.sha256(item['statement'].encode()).hexdigest()
  rh=hashlib.sha256(json.dumps([item,rs.get(item['problem_number'],{})],sort_keys=True).encode()).hexdigest()
  assert sh==cat['statement_hash']==e['identity']['statement_sha256']
  assert rh==cat['review_hash']==e['identity']['review_sha256']
  exact=[k for k,v in rs.items() if any(t in (k+' '+json.dumps(v,ensure_ascii=False)).lower() for t in ['30005140','owr-10252936-003','gaussian-free-field maxima on percolation clusters'])]
  assert not exact
  out['corpora']={'status':'PASS','statement_hash_match':True,'review_hash_match':True,'research_exact_matches':0}
 if a.pdf_dir:
  sources=json.loads((root/'SOURCE_AUDIT.json').read_text())['pdfs']
  for s in sources:
   b=(a.pdf_dir/s['name']).read_bytes();assert b.startswith(b'%PDF-') and meta(b)=={k:s[k] for k in ['bytes','sha256']}
  out['pdfs']={'status':'PASS','files_checked':len(sources)}
 if not out:p.error('Supply at least one input group; --help lists options.')
 print(json.dumps({'status':'PASS','checks':out,'scope':'Input identity only; not a proof audit.'},sort_keys=True))
if __name__=='__main__':main()
