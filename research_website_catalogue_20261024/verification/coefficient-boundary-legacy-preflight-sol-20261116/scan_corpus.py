#!/usr/bin/env python3
"""Read-only identity/search over the already authenticated current docs cache."""
from pathlib import Path
import hashlib,html,json,re,unicodedata,datetime,collections
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O=P/'verification/coefficient-boundary-legacy-preflight-sol-20261116'
i=json.loads((O/'INITIAL.json').read_bytes());pin=i['authenticated_corpus_interface'];raw=Path(pin['path']).read_bytes();assert len(raw)==pin['bytes']and hashlib.sha256(raw).hexdigest()==pin['SHA256'];x=json.loads(raw)
assert x['current_docs_subtree']==i['opening_docs_tree']=='f5f5fb2fb18196b604d7b568e3e58ccc1bf127b3'
def digest(b):return hashlib.sha256(b).hexdigest()
def pinned(row):
 p=Path(row['path']);b=p.read_bytes();assert len(b)==row['bytes']and digest(b)==row['SHA256'];return b
bindings=x['whole_blob_bindings'];reps=x['whole_text_representations'];assert len(bindings)==254 and len(reps)==260
by_path={r['path']:r for r in bindings};assert len(by_path)==254
tree={};html_paths=set()
for r in bindings:
 b=pinned(r['reused_complete_body']);assert len(b)==r['bytes']and digest(b)==r['SHA256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob'];parts=r['path'].split('/');assert parts.pop(0)=='docs';d=tree
 for part in parts[:-1]:d=d.setdefault(part,{})
 assert parts[-1]not in d;d[parts[-1]]=r
 if r['path'].endswith('.html'):html_paths.add(r['path'])
def tree_sha(d):
 chunks=[]
 for name,value in sorted(d.items(),key=lambda kv:(kv[0]+('/'if 'blob'not in kv[1]else'')).encode()):
  is_blob='blob'in value;mode=value['mode']if is_blob else'40000';oid=value['blob']if is_blob else tree_sha(value);chunks.append(mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(oid))
 b=b''.join(chunks);return hashlib.sha1(b'tree '+str(len(b)).encode()+b'\0'+b).hexdigest()
reconstructed=tree_sha(tree);assert reconstructed==i['opening_docs_tree']and len(html_paths)==47
queries={}
for r in i['native_identity_fields']:
 terms={'native_exact_title':r['native_title'],'native_DOI':r['native_DOI'],'native_record_id':r['record_id']}
 terms.update({'alias_'+str(n):s for n,s in enumerate(['coefficient normalization','positive definite forms','Brandes']if r['row']==143 else['boundary twist','boundarytwist','boundary multitwist','restricted boundary','finiteness deduction'],1)})
 queries[r['record_id']]=terms
def normalized(s):return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFKD',html.unescape(s)).casefold()).strip()
def hits(text,terms):
 out=[];fold=text.casefold();norm=normalized(text)
 for key,term in terms.items():
  matched=(term.casefold()in fold)if key in ['native_DOI','native_record_id']else(normalized(term)in norm)
  if matched:out.append(key)
 return out
path_hits=[];text_hits=[];coverage={p:set()for p in html_paths}
for r in bindings:
 for rid,terms in queries.items():
  h=hits(r['path'],terms)
  if h:path_hits.append({'record_id':rid,'public_path':r['path'],'matched_terms':h,'HTML':r['path']in html_paths})
for r in reps:
 b=pinned(r['text_file']);assert r['public_path']in by_path and r['blob']==by_path[r['public_path']]['blob'];text=b.decode('utf-8')
 if r['public_path']in coverage:coverage[r['public_path']].add(r['kind'])
 for rid,terms in queries.items():
  h=hits(text,terms)
  if h:text_hits.append({'record_id':rid,'public_path':r['public_path'],'kind':r['kind'],'matched_terms':h,'text_file':r['text_file'],'HTML':r['public_path']in html_paths})
assert all({'raw_UTF8','decoded_HTML'}<=v for v in coverage.values())
print(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'COMPLETE_BOUNDED_CACHE_SEARCH','docs_tree_reconstructed':reconstructed,'whole_current_blob_bodies_authenticated':len(bindings),'whole_pathnames_searched':len(bindings),'complete_text_representations_searched':len(reps),'representation_kinds':dict(collections.Counter(r['kind']for r in reps)),'HTML_paths':len(html_paths),'all47HTML_raw_and_decoded_coverage':True,'queries':queries,'path_hits':path_hits,'text_hits':text_hits,'distinct_HTML_hit_paths':sorted({r['public_path']for r in text_hits if r['HTML']}),'network_corpus_refetches':0,'new_PDF_extractions':0,'new_scientific_source_reading_or_replay':False,'limits':'Search current enumerated docs corpus only; assets/project/path/text hits are not themselves matching HTML articles. Whole candidate HTML inspection and closing connector identity are separate.'},ensure_ascii=False,indent=2))
