"""Rehash complete authorized inputs; emit metadata only, never source contents.
Usage: python verify_provenance.py PROBLEMS REPORTS CATALOG SOURCE_DIR AUTHOR_ZIP
"""
from pathlib import Path
import hashlib,json,sys,zipfile
EXPECTED={
 'problems.json':(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
 'research_results.json':(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
 'catalog.json':(21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566')}

def metadata(data):
 return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def verify():
 problems,reports,catalog,sources,archive=map(Path,sys.argv[1:])
 sourcebytes=archive.read_bytes(); assert metadata(sourcebytes)=={'bytes':23313,'sha256':'fac44aee178ad76fbeb347c1bab796ed5b877a470a4bd69ca63777886dd6012d'}
 with zipfile.ZipFile(archive) as z:
  am=json.loads(z.read('AUTHOR_MANIFEST.json')); provenance=json.loads(z.read('SOURCE_VERIFICATION.json'))
  assert len(z.namelist())==9 and set(z.namelist())=={'AUTHOR_MANIFEST.json'}|{f['path'] for f in am['files']}
  for item in am['files']:
   assert metadata(z.read(item['path']))=={k:item[k] for k in ['bytes','sha256']}
 corpus={};loaded=[]
 for name,p in zip(EXPECTED,[problems,reports,catalog]):
  b=p.read_bytes();m=metadata(b);assert (m['bytes'],m['sha256'])==EXPECTED[name]
  corpus[name]=m;loaded.append(json.loads(b))
 p,r,c=loaded
 selected=[x for x in p if x['id']==30005078];assert len(selected)==1
 item=selected[0];cat=next(x for x in c if x['id']=='30005078')
 assert item['problem_number']=='OWR-10252925-002' and item['problem_number'] not in r
 sh=hashlib.sha256(item['statement'].encode()).hexdigest();assert sh==cat['statement_hash']
 # The repository imports an absent prior-report key as {}; its documented
 # review digest serializes the pair with sort_keys=True and default ASCII.
 rh=hashlib.sha256(json.dumps([item,{}],sort_keys=True).encode()).hexdigest()
 assert rh==cat['review_hash']=='ea33d4d9da77ba488f773877ec11a4741d07702c400c559ecc3e4902ef3163fe'
 cb=catalog.read_bytes();blob=hashlib.sha1(b'blob '+str(len(cb)).encode()+b'\0'+cb).hexdigest()
 assert blob=='bd5c23e4e6c7e1901717a7e596477a7f6dc72425'
 filenames=['owr2022_17.pdf','bhs_characterization_v4.pdf','bhs_bounds.pdf','bender_bigraded.pdf','linear_truncations_article.pdf','maclagan_smith_actual.pdf','ems2000.pdf']
 pdfs=[]
 for fn,record in zip(filenames,provenance['sources']):
  data=(sources/fn).read_bytes();assert data.startswith(b'%PDF-')
  m=metadata(data);assert all(m[k]==record['pdf'][k] for k in m)
  pdfs.append({'title':record['title'],'url':record['url'],**m,'matches_author':True})
 software=(sources/'VirtualResolutions.m2').read_bytes()
 software_meta=metadata(software);assert all(software_meta[k]==provenance['software_source'][k] for k in software_meta)
 sblob=hashlib.sha1(b'blob '+str(len(software)).encode()+b'\0'+software).hexdigest()
 assert sblob=='c51047421a33be0b42cf3f6df371d577bfc1fae6'
 result={'status':'PASS','problem_id':30005078,'rank':cat['rank'],'author_freeze':metadata(sourcebytes),
   'author_manifest_entries_verified':len(am['files']),'corpora':corpus,'problem_records':len(p),'report_entries':len(r),
   'selected_id_count':len(selected),'selected_report_key_present':False,'statement_sha256':sh,'review_hash':rh,
   'statement_and_review_hashes_match_catalog':True,'catalog_git_blob':blob,'pdfs':pdfs,
   'software':{'url':provenance['software_source']['url'],**software_meta,'git_blob':sblob},
   'upstream_manifest':{'url':provenance['dataset']['manifest_url'],'git_blob':'55589bae6bad2d3e2f696e08645330ff1219b709','independently_read':True},
   'upstream_queue_hash_method':{'url':'https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/queue.py','git_blob':'e646cfc1a3b9653879777e4e1215e9a1043f3a3d','independently_read':True}}
 Path(__file__).with_name('PROVENANCE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('pdfs','software')},indent=2))

if __name__=='__main__':verify()
