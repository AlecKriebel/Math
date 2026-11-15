"""Read-only five-target full-copy/asset/overlay/current-byte fence."""
from five_common import *
from five_source import load_bundles
from five_contract import check_page
from datetime import date
from html import escape as h
import argparse,copy,re,xml.etree.ElementTree as ET
MONTHS=('January','February','March','April','May','June','July','August','September','October','November','December')
def check_overlays(bundles,index,sitemap,build_date):
 before=(OWN/'baseline/research/index.html').read_text();oldmap=(OWN/'baseline/research/sitemap.xml').read_bytes()
 now=index.decode();li=re.findall(r'<li>.*?</li>',now,re.S);oldli=re.findall(r'<li>.*?</li>',before,re.S)
 need(len(oldli)==78 and len(li)==83 and li[:78]==oldli,'all_old78_visible_entries_unchanged')
 additions=[];urls=[]
 for b in bundles:
  d=date.fromisoformat(b['publication_date']);label=str(d.day)+' '+MONTHS[d.month-1]+' '+str(d.year);url='https://aleckriebel.com/research/'+b['slug']+'/'
  additions.append('<li><a href="/research/'+b['slug']+'/">'+h(b['title'])+'</a><br><span class="entry-meta">'+label+' · '+h(b['kind'])+'</span><p>'+h(b['description'])+'</p><p><a href="/research/'+b['slug']+'/'+b['pdf']['name']+'">PDF</a> · <a href="https://doi.org/'+b['doi']+'">Zenodo</a></p></li>');urls.append(url)
 need(li[78:]==additions,'all_five_new_visible_entries_dates_and_destinations')
 rx=r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)';old=re.search(rx,before,re.S);new=re.search(rx,now,re.S)
 need(old is not None and new is not None,'both_complete_index_schemas')
 expected=copy.deepcopy(strict_json(old.group(2)));items=expected['mainEntity']['itemListElement']
 need(len(items)==expected['mainEntity']['numberOfItems']==78,'saved78_ItemList')
 for b,url in zip(bundles,urls):items.append({'@type':'ListItem','position':len(items)+1,'url':url,'name':b['title']})
 expected['mainEntity']['numberOfItems']=83;need(same(strict_json(new.group(2)),expected),'entire_old_plus_five83_ItemList')
 restored=now[:new.start(2)]+old.group(2)+now[new.end(2):]
 for row in additions:need(restored.count('      '+row+'\n')==1,'unique_new_index_addition');restored=restored.replace('      '+row+'\n','',1)
 need(restored==before,'every_other_index_byte_preserved')
 os=ET.fromstring(oldmap);ns=ET.fromstring(sitemap);ol=[n.text for n in os.findall('{*}url/{*}loc')];nl=[n.text for n in ns.findall('{*}url/{*}loc')]
 need(len(ol)==79 and nl==ol+urls and len(set(nl))==len(nl)==84,'exact_old79_plus_five84_sitemap_locations')
 restored=sitemap.decode()
 for url in urls:
  addition='  <url><loc>'+url+'</loc><lastmod>'+build_date+'</lastmod></url>\n';need(restored.count(addition)==1,'unique_dated_sitemap_addition');restored=restored.replace(addition,'',1)
 need(restored==oldmap.decode(),'every_other_sitemap_byte_preserved')
 return {'old_visible_entries_preserved':78,'new_index_entries':83,'new_sitemap_locations':84}
def verify(stage_root,build_date,*,current_base=False,dlab_homepage=True,bundles=None):
 need(date.fromisoformat(build_date).isoformat()==build_date,'explicit_ISO_stage_date');root=safe_output(stage_root);need(root.is_dir(),'existing_private_candidate')
 bundles=load_bundles() if bundles is None else bundles
 if dlab_homepage:authorize_dlab()
 expected={'research/index.html','research/sitemap.xml'}
 for b in bundles:expected.update('research/'+b['slug']+'/'+name for name in ['index.html','citation.bib',b['pdf']['name'],b['zip']['name']])
 actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()};need(actual==expected and len(actual)==22,'exact22_new_overlay_paths')
 need(not any(p.is_symlink() for p in root.rglob('*')),'candidate_no_symlinks')
 baseline=load(OWN/'FRESH_BASELINE.json');old={r['path']:r for r in baseline['public_files']}
 need(expected&set(old)=={'research/index.html','research/sitemap.xml'},'no_old_article_or_asset_collision')
 output={}
 for b in bundles:
  folder=root/'research'/b['slug'];files={p.name:p.read_bytes() for p in folder.iterdir() if p.is_file()}
  output[b['rid']]=check_page(b,files['index.html'],files,build_date,dlab_homepage=dlab_homepage)
 overlay=check_overlays(bundles,(root/'research/index.html').read_bytes(),(root/'research/sitemap.xml').read_bytes(),build_date)
 for r in baseline['public_files']:
  if r['path'] not in {'research/index.html','research/sitemap.xml'}:need(bind(contained(PUBLIC,r['path']))=={k:r[k] for k in ['bytes','sha256']},'all554_old_nonoverlay_public_bytes:'+r['path'])
 for r in baseline['installed_core_files']:need(bind(r['path'])=={k:r[k] for k in ['bytes','sha256']},'all18_current_core_bytes:'+r['path'])
 if current_base:
  files={str(p.relative_to(PUBLIC)) for p in PUBLIC.rglob('*') if p.is_file()};need(files==set(old) and len(files)==556,'current_public556_namespace')
  for name in ['research/index.html','research/sitemap.xml']:need(bind(PUBLIC/name)=={k:old[name][k] for k in ['bytes','sha256']},'current_old_overlay_bytes:'+name)
 return {'literal_custom_status':'PRIVATE_FIVE_COMPLETE_COPY_METADATA_ASSETS_AND_OVERLAYS_VERIFIED_PENDING_ROOT_STAGE_CODE_AUDIT',
  'records':output,'public_overlay_paths':22,'hypothetical_public_files':len(set(old)|expected),
  **overlay,'current_baseline_requested':current_base,'old_nonoverlay_public_files_preserved':554,'installed_current_core_files_preserved':18,
  'original_custom_science_verdicts_preserved_whole':15,'root_full_editorial_copy_adopted_additively':True,
  'Dlab_single_href_private_root_adoption_applied':dlab_homepage,'historical_native_flags_unmodified':True,
  'stage_code_and_independent_audit_adoption_pending':True,'production_install_authorized':False,'canonical_URL_assignment':None,'AA':None,
  'source_programs_old457_69_138_campaigns_or_publication_replayed':False,'network_or_file_writes':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--stage-root',required=True,type=Path);p.add_argument('--build-date',required=True);p.add_argument('--current-base',action='store_true');p.add_argument('--original-dlab-link',action='store_true');a=p.parse_args()
 print(json.dumps(verify(a.stage_root,a.build_date,current_base=a.current_base,dlab_homepage=not a.original_dlab_link),indent=2,sort_keys=True))
