from pathlib import Path
import datetime,hashlib,json,re
R=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');P=R/'papers/23431716';O=P/'reviews/publication';S=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=json.loads((O/'before-site-hashes.json').read_text())
slug='chip-firing-halting-simple-digraphs';url='https://aleckriebel.com/research/'+slug+'/'
checks={};oldpaths=set(before['files']);newpaths={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()}
changed=[name for name,digest in before['files'].items() if not (S/name).is_file() or sha(S/name)!=digest]
checks['only_index_and_sitemap_changed']=set(changed)=={'index.html','sitemap.xml'}
checks['only_four_expected_new_files']=newpaths-oldpaths=={slug+'/'+name for name in ['index.html','paper.pdf','pr1098_support_v1_0.zip','citation.bib']}
checks['all_existing_files_retained']=not(oldpaths-newpaths)
checks['renderer_unchanged']=sha(R/'scripts/render_page.py')==before['renderer_sha256']
checks['asset_resolver_unchanged']=sha(R/'scripts/published_assets.py')==before['published_assets_sha256']
checks['css_unchanged']=sha(S/'research.css')==before['files']['research.css']
oldindex=(O/'before-index.html').read_text();index=(S/'index.html').read_text()
pattern=r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)'
a=re.search(pattern,oldindex,re.S);b=re.search(pattern,index,re.S);oldj=json.loads(a.group(2));newj=json.loads(b.group(2))
checks['existing_ordered_index_items_preserved']=newj['mainEntity']['itemListElement'][:-1]==oldj['mainEntity']['itemListElement']
newitem=newj['mainEntity']['itemListElement'][-1]
checks['one_expected_index_item_added']=newitem['url']==url and newj['mainEntity']['numberOfItems']==oldj['mainEntity']['numberOfItems']+1
stripped=index[:b.start(2)]+a.group(2)+index[b.end(2):]
stripped,n=re.subn(r'      <li><a href="/research/'+re.escape(slug)+r'/">.*?</li>\n','',stripped,count=1,flags=re.S)
checks['index_text_otherwise_identical']=n==1 and stripped==oldindex
sitemap=(S/'sitemap.xml').read_text();stripped,n=re.subn(r'  <url><loc>'+re.escape(url)+r'</loc><lastmod>[^<]+</lastmod></url>\n','',sitemap,count=1)
checks['sitemap_text_otherwise_identical']=n==1 and stripped==(O/'before-sitemap.xml').read_text()
checker=(R/'verification/final-content-check.py').read_text()
checker=checker.replace(" '23431716':'published-source/paper.tex',\n",'',1)
start=checker.index(" if rid=='23431716':\n");end=checker.index(" result['papers'][rid]",start)
checks['checker_only_adds_exact_record_mapping_and_scoped_checks']=checker[:start]+checker[end:]==(O/'before-final-content-check.py').read_text()
receipt=json.loads((P/'sources/receipt.json').read_text())
checks['source_public_assets_unchanged']=all(sha(P/'sources'/f['name'])==f['sha256'] for f in receipt['files'])
checks['all124_source_members_unchanged']=all(sha(P/'sources/published-source'/m['member'])==m['sha256'] for m in receipt['archives'][0]['members'])
N=R/'papers/23444839/reviews/scope';freeze=json.loads((N/'SCOPE_FREEZE.json').read_text())
checks['frozen_nevo_scope_unchanged']=all(sha(N/name)==v['sha256'] for name,v in freeze['files'].items())
gate=json.loads((P/'promotion.json').read_text())
checks['all_three_complete_verdicts_preserved']=all(v['verdict']==json.loads((P/v['verdict_file']).read_text()) and sha(P/v['verdict_file'])==v['verdict_sha256'] and sha(P/v['report'])==v['sha256'] for v in gate['reviews'].values())
result={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'changed_existing_site_paths':changed,'new_site_paths':sorted(newpaths-oldpaths),'status':'PASS' if all(checks.values()) else 'FAIL','limits':'Source/content preservation checks, not browser appearance or external HTTP validation.'}
(O/'shared-changes-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
raise SystemExit(0 if result['status']=='PASS' else 1)
