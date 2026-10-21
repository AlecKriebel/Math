"""Computed summaries from preserved primary bytes, never historical receipts."""
from pathlib import Path
import json,re,hashlib,html
S=Path(__file__).resolve().parent
P=S/'private_evidence'
def read(n):return json.loads((P/n/'source.bytes').read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
out={'kind':'computed_metadata_and_version_comparison_not_native_retrieval_receipt'}
out['pr_commits']=[{k:r.get(k) for k in ['sha','html_url']}|{'author':r['commit']['author']['date'],'committer':r['commit']['committer']['date'],'message':r['commit']['message']} for r in read('github_pr329_commits')]
out['trees']={n:[{'name':r['name'],'type':r['type'],'git_blob_or_tree_sha':r['sha']} for r in read(n)] for n in ['gh329_first_tree_noslash','gh329_head_tree_noslash']}
rows=[]
base=S.parent.parent/'snapshot/unsolved_math_prioritization/attempts/20000450'
for name in ['TURN_1.md','FINAL_RESULT.md','SOURCE_THEORY.md','verify_turn1.py']:
 b=(base/name).read_bytes()
 for v in ['first','head']:
  n='gh329_'+v+'_'+name.replace('.','_').lower()
  # Retrieval labels preserve the filename casing: find by actual URL instead.
  d=next(d for d in P.iterdir() if d.is_dir() and (d/'SUMMARY.json').exists() and json.loads((d/'SUMMARY.json').read_text()).get('url','').endswith('/'+name) and (('0a77190' in json.loads((d/'SUMMARY.json').read_text()).get('url','')) if v=='first' else ('96395a4' in json.loads((d/'SUMMARY.json').read_text()).get('url',''))))
  old=(d/'source.bytes').read_bytes()
  rows.append({'scientific_file':name,'version':v,'bytes':len(old),'sha256':sha(old),'exactly_equal_snapshot':old==b,'retrieval_label':d.name})
out['public_scientific_file_comparisons']=rows
rs=read('github_releases')
pattern=re.compile(r'20000450|pentagon|McCallum|qptsurface',re.I)
out['release_metadata']={'page1_count':len(rs),'page2_count':len(read('github_releases_page2')),'records':[{k:r.get(k) for k in ['id','tag_name','name','created_at','published_at','html_url']}|{'target_pattern_hit_in_name_body_or_asset_names':bool(pattern.search(' '.join([r.get('name') or '',r.get('body') or '']+[a['name'] for a in r.get('assets',[])])))} for r in rs],'scope':'All returned names, bodies and asset names scanned; archive file contents not downloaded or searched.'}
for n in ['zenodo_repo_search2','zenodo_exact_target','zenodo_repo_versions','zenodo_pentagonal_torsion']:
 x=read(n)
 out[n]={'total':x.get('hits',{}).get('total'),'returned_count':len(x.get('hits',{}).get('hits',[])),'records':[{'id':r.get('id'),'created':r.get('created'),'updated':r.get('updated'),'title':r.get('metadata',{}).get('title'),'publication_date':r.get('metadata',{}).get('publication_date'),'doi':r.get('doi'),'target_pattern_hit_in_metadata':bool(pattern.search(json.dumps(r.get('metadata',{}))))} for r in x.get('hits',{}).get('hits',[])],'scope':'Returned metadata inspected; full deposited file contents not inspected.'}
out['arxiv_metadata']={}
for n in ['morton_metadata','fisher2008_metadata','fisher2013_metadata','consani_metadata']:
 t=(P/n/'source.bytes').read_text();i=t.find('<h2>Submission history');j=t.find('</div>',i)
 out['arxiv_metadata'][n]=html.unescape(re.sub('<[^>]+>',' ',t[i:j])).strip()
t1=(P/'morton2018_v4/fulltext.layout.txt').read_text()
t2=(P/'morton2019_repository/fulltext.layout.txt').read_text()
out['morton_text_comparison']={'whitespace_normalized_whole_text_equal':''.join(t1.split())==''.join(t2.split()),'pdf_bytes_equal':(P/'morton2018_v4/source.bytes').read_bytes()==(P/'morton2019_repository/source.bytes').read_bytes(),'scope':'Computed comparison of two entire extracted texts; no assertion of publisher-PDF identity.'}
(P/'FINAL_VERSION_COMPARISON.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['trees','release_metadata','zenodo_repo_versions','zenodo_pentagonal_torsion','zenodo_exact_target']},indent=2))
for k in ['release_metadata','zenodo_repo_versions','zenodo_pentagonal_torsion','zenodo_exact_target']:
 v=out[k];print(k,json.dumps({a:b for a,b in v.items() if a!='records'}));print(json.dumps(v.get('records',[]),indent=2))
