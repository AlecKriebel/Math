"""Read-only complete two-stage contracts, old-public bytes and overlays."""
from two_common import *
from two_source import load_bundles
from two_contract import check_page
from build_private import authenticate_baseline
from datetime import date
from html import escape as h
import copy,argparse,re,xml.etree.ElementTree as ET
MONTHS=('January','February','March','April','May','June','July','August','September','October','November','December')
def check_overlays(bundles,index,sitemap,build_date):
 before=(OWN/'baseline/research/index.html').read_text();oldmap=(OWN/'baseline/research/sitemap.xml').read_bytes();now=index.decode();oldli=re.findall(r'<li>.*?</li>',before,re.S);li=re.findall(r'<li>.*?</li>',now,re.S)
 need(len(oldli)==83 and len(li)==85 and li[:83]==oldli,'every_old83_visible_entry_complete_and_unchanged');additions=[];urls=[]
 for b in bundles:
  d=date.fromisoformat(b['publication_date']);stamp=str(d.day)+' '+MONTHS[d.month-1]+' '+str(d.year);url='https://aleckriebel.com/research/'+b['slug']+'/'
  additions.append('<li><a href="/research/'+b['slug']+'/">'+h(b['title'])+'</a><br><span class="entry-meta">'+stamp+' · '+h(b['kind'])+'</span><p>'+h(b['description'])+'</p><p><a href="/research/'+b['slug']+'/'+b['pdf']['name']+'">PDF</a> · <a href="https://doi.org/'+b['doi']+'">Zenodo</a></p></li>');urls.append(url)
 need(li[83:]==additions,'two_complete_new_visible_entries_and_native_dates');rx=r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)';old=re.search(rx,before,re.S);new=re.search(rx,now,re.S);need(old is not None and new is not None,'both_complete_index_schemas');expected=copy.deepcopy(strict_json(old.group(2)));items=expected['mainEntity']['itemListElement'];need(len(items)==expected['mainEntity']['numberOfItems']==83,'saved83_ItemList')
 for b,url in zip(bundles,urls):items.append({'@type':'ListItem','position':len(items)+1,'url':url,'name':b['title']})
 expected['mainEntity']['numberOfItems']=85;need(same(strict_json(new.group(2)),expected),'complete_original_ItemList_plus_exact_two');restored=now[:new.start(2)]+old.group(2)+now[new.end(2):]
 for row in additions:need(restored.count('      '+row+'\n')==1,'single_new_index_row');restored=restored.replace('      '+row+'\n','',1)
 need(restored==before,'every_other_index_byte_unchanged');os=ET.fromstring(oldmap);ns=ET.fromstring(sitemap);ol=[x.text for x in os.findall('{*}url/{*}loc')];nl=[x.text for x in ns.findall('{*}url/{*}loc')];need(len(ol)==84 and nl==ol+urls and len(set(nl))==len(nl)==86,'all_old84_plus_two_sitemap_locations');restored=sitemap.decode()
 for url in urls:
  row='  <url><loc>'+url+'</loc><lastmod>'+build_date+'</lastmod></url>\n';need(restored.count(row)==1,'exact_new_dated_sitemap_row');restored=restored.replace(row,'',1)
 need(restored==oldmap.decode(),'every_other_sitemap_byte_unchanged');return {'old_entries':83,'new_entries':85,'old_sitemap':84,'new_sitemap':86}
def verify(stage_root,build_date,*,current_base=False,bundles=None):
 need(date.fromisoformat(build_date).isoformat()==build_date,'ISO_build_date');root=safe_output(stage_root);need(root.is_dir(),'existing_private_candidate');baseline=authenticate_baseline();bundles=load_bundles() if bundles is None else bundles;expected={'research/index.html','research/sitemap.xml'}
 for b in bundles:expected.update('research/'+b['slug']+'/'+n for n in ['index.html','citation.bib']+[a['name'] for a in b['assets']])
 actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()};need(actual==expected and len(actual)==11,'exact11_paths_including119_fifth_leaf');need(not any(p.is_symlink() for p in root.rglob('*')),'candidate_no_symlinks');old={r['path']:r for r in baseline['public_files']};need(expected&set(old)=={'research/index.html','research/sitemap.xml'},'no_existing_article_or_asset_collision');results=[]
 for b in bundles:
  folder=root/'research'/b['slug'];files={p.name:p.read_bytes() for p in folder.iterdir() if p.is_file()};results.append(check_page(b,files['index.html'],files,build_date))
 overlay=check_overlays(bundles,(root/'research/index.html').read_bytes(),(root/'research/sitemap.xml').read_bytes(),build_date)
 for r in baseline['public_files']:
  if r['path'] not in {'research/index.html','research/sitemap.xml'}:need(bind(contained(PUBLIC,r['path']))=={k:r[k] for k in ['bytes','sha256']},'all574_old_nonoverlay_public_files:'+r['path'])
 for r in baseline['installed_core_files']:need(bind(r['path'])=={k:r[k] for k in ['bytes','sha256']},'all18_current_installed_core_files:'+r['path'])
 if current_base:
  need({str(p.relative_to(PUBLIC)) for p in PUBLIC.rglob('*') if p.is_file()}==set(old) and len(old)==576,'current_exact576_public_namespace')
  for name in ['research/index.html','research/sitemap.xml']:need(bind(PUBLIC/name)=={k:old[name][k] for k in ['bytes','sha256']},'current_old_public_overlay_bytes:'+name)
 return {'literal_custom_status':'PRIVATE_TWO_COMPLETE_ORIGINAL_COPY_NATIVE_ASSETS_AND_OVERLAYS_VALIDATED_PENDING_SEPARATE_ROOT_STAGE_ADOPTION','record_results':results,'overlay_paths':11,'hypothetical_public_union_files':len(set(old)|expected),**overlay,'old_nonoverlay_public_bytes_preserved':574,'current_core_files_preserved':18,'whole_qualified_science_verdicts_retained':6,'all_original_native_schemas_and_failed_transports_preserved':True,'current_base_checked':current_base,'root_final_stage_code_render_adoption':None,'independent_code_audit':None,'production_install_authorized':False,'AA':None,'canonical_assignment':None,'browser_deployment_or_legacy_redirect_authority':False,'source_or_old_campaign_replay':False,'network_or_writes':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--stage-root',type=Path,required=True);p.add_argument('--build-date',required=True);p.add_argument('--current-base',action='store_true');a=p.parse_args();print(json.dumps(verify(a.stage_root,a.build_date,current_base=a.current_base),indent=2))
