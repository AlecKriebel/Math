from pathlib import Path
import ast,contextlib,datetime,hashlib,io,json,re,sys,tempfile
B=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');P=B/'papers/22089373';O=P/'reviews/publication';S=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks={};before=json.loads((O/'before-local-finalization.json').read_text());slug='strong-tree-child-level-2-jukes-cantor-identifiability';url='https://aleckriebel.com/research/'+slug+'/'
old=(O/'before-render_page.py').read_text();new=(B/'scripts/render_page.py').read_text()
checks['renderer_only_optional_escaped_date_label']=new.replace("{h(c.get('publication_date_label', 'Published'))}",'Published')==old
sys.path.insert(0,str(B/'scripts'));sys.dont_write_bytecode=True
# Execute the real old/new renderer code against isolated output directories;
# keep original paper/source files and production pages read-only in these controls.
def render(code,rid,dest,label=None):
 dest.mkdir();(dest/'index.html').write_bytes((O/'before-index.html').read_bytes());(dest/'sitemap.xml').write_bytes((O/'before-sitemap.xml').read_bytes())
 tree=ast.parse(code)
 for n in tree.body:
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SITE' for t in n.targets):n.value=ast.Call(func=ast.Name(id='Path',ctx=ast.Load()),args=[ast.Constant(str(dest))],keywords=[])
 if label is not None:
  for i,n in enumerate(tree.body):
   if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='c' for t in n.targets):
    tree.body.insert(i+1,ast.parse('c["publication_date_label"]='+repr(label)).body[0]);break
 ast.fix_missing_locations(tree);argv=sys.argv;sys.argv=[str(B/'scripts/render_page.py'),rid]
 try:
  with contextlib.redirect_stdout(io.StringIO()):exec(compile(tree,str(B/'scripts/render_page.py'),'exec'),{'__file__':str(B/'scripts/render_page.py'),'__name__':'__main__'})
 finally:sys.argv=argv
 return {str(x.relative_to(dest)):sha(x) for x in dest.rglob('*') if x.is_file()}
with tempfile.TemporaryDirectory(prefix='jc-renderer-regression-') as td:
 t=Path(td)
 for rid in ['23430642','22729355','23147866']:
  checks['unchanged_default_render_'+rid]=render(old,rid,t/(rid+'-old'))==render(new,rid,t/(rid+'-new'))
 render(new,'22089373',t/'jc')
 html=(t/'jc'/slug/'index.html').read_text();checks['custom_date_label_rendered']='<br>Zenodo date <time datetime="2026-08-23">23 August 2026</time>' in html
 render(new,'22089373',t/'escaped',label='<Date & label>')
 html=(t/'escaped'/slug/'index.html').read_text();checks['custom_label_html_escaped']='&lt;Date &amp; label&gt; <time' in html and '<Date & label>' not in html
parsed=ast.parse((B/'verification/final-content-check.py').read_text());selected=ast.Module(body=[x for x in parsed.body if isinstance(x,ast.FunctionDef) and x.name=='normalized_jc_abstract'],type_ignores=[]);ns={'re':re};exec(compile(selected,'normalizer','exec'),ns)
c=json.loads((P/'publication.json').read_text());body=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',(P/c['source_binding']['abstract_source']).read_text(),re.S).group(1);actual=ns['normalized_jc_abstract'](body)
checks['full_abstract_exact']=actual==c['abstract'];checks['truncated_abstract_rejected']=actual!=' '.join(c['abstract'].split()[:-1]);checks['altered_dimension_rejected']=actual!=c['abstract'].replace('2n + 1','2n + 2');checks['added_editorial_sentence_rejected']=actual!=c['abstract']+' This is a new sentence.'
oldpaths=set(before['files']);newpaths={str(x.relative_to(S)) for x in S.rglob('*') if x.is_file()};changed=[name for name,digest in before['files'].items() if not (S/name).is_file() or sha(S/name)!=digest]
checks['only_existing_index_and_sitemap_changed']=set(changed)=={'index.html','sitemap.xml'};checks['all_existing_files_retained']=not(oldpaths-newpaths)
expected=['index.html','citation.bib',c['pdf_filename'],c['supplement_filename']]+[x['filename'] for x in c['additional_assets']]
checks['only_six_expected_new_files']=newpaths-oldpaths=={slug+'/'+name for name in expected}
checks['css_unchanged']=sha(S/'research.css')==before['files']['research.css'];checks['asset_resolver_unchanged']=sha(B/'scripts/published_assets.py')==before['published_assets_sha256'];checks['live_verifier_unchanged']=sha(B/'scripts/verify_live.py')==before['verify_live_sha256']
oldindex=(O/'before-index.html').read_text();index=(S/'index.html').read_text();pattern=r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)';a=re.search(pattern,oldindex,re.S);b=re.search(pattern,index,re.S);oldj=json.loads(a.group(2));newj=json.loads(b.group(2));checks['existing_index_items_preserved']=newj['mainEntity']['itemListElement'][:-1]==oldj['mainEntity']['itemListElement'];checks['one_expected_index_item_added']=newj['mainEntity']['itemListElement'][-1]['url']==url and newj['mainEntity']['numberOfItems']==oldj['mainEntity']['numberOfItems']+1
stripped=index[:b.start(2)]+a.group(2)+index[b.end(2):];stripped,n=re.subn(r'      <li><a href="/research/'+re.escape(slug)+r'/">.*?</li>\n','',stripped,count=1,flags=re.S);checks['index_otherwise_identical']=n==1 and stripped==oldindex
sitemap=(S/'sitemap.xml').read_text();stripped,n=re.subn(r'  <url><loc>'+re.escape(url)+r'</loc><lastmod>[^<]+</lastmod></url>\n','',sitemap,count=1);checks['sitemap_otherwise_identical']=n==1 and stripped==(O/'before-sitemap.xml').read_text()
gate=json.loads((P/'promotion.json').read_text());checks['complete_verdict_objects_unchanged']=all(v['verdict']==json.loads((P/v['verdict_file']).read_text()) and sha(P/v['verdict_file'])==v['verdict_sha256'] and sha(P/v['report'])==v['sha256'] for v in gate['reviews'].values())
for rel in ['sources/receipt.json','sources/related-record-22064121/receipt.json']:
 rp=P/rel;r=json.loads(rp.read_text());checks['all_source_bytes_unchanged_'+r['record_id']]=all(sha(rp.parent/f['name'])==f['sha256'] for f in r['files'])
result={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completion_percent':100,'checks':checks,'status':'PASS' if all(checks.values()) else 'FAIL','changed_existing_site_paths':changed,'new_site_paths':sorted(newpaths-oldpaths),'limits':'Local content/source preservation and isolated renderer controls; browser rendering and live HTTP verification remain separate.'};(O/'shared-changes-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values())
