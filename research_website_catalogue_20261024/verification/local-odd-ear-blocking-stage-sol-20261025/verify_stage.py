"""Read-only custody/result verification. Never replays a checker or renderer.

Use bundled Python with -B. --preseal checks all evidence before the final
manifest exists; ordinary invocation additionally checks the complete own seal.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import datetime,hashlib,json,re
O=Path(__file__).resolve().parent;P=O.parents[1]
sys.path[:0]=[str(O),str(P/'scripts')]
from odd_ear_blocking_source import OEB_IDS,odd_ear_blocking_source_view,verify_oeb_archive,approved_material_note
from oeb_body_contract import BodyText,expected_body,MATERIAL_NOTES
checks={}
def need(value,name):
 checks[name]=bool(value)
 if not value:raise RuntimeError('read-only stage verification:'+name)
def load(p):return json.loads(Path(p).read_text())
def bnd(p):
 data=Path(p).read_bytes();return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def check_binding(row):return bnd(row['path'])=={k:row[k] for k in ('bytes','sha256')}
base=load(O/'BASELINE.json');frozen=load(O/'FROZEN_INPUT_SET.json');old=frozen['old_configured_record_ids_in_order'];new=frozen['authorized_new_record_ids'];live=Path(base['production_public_root'])
need(len(old)==len(set(old))==67 and new==['23576280','23331258'] and set(new)==OEB_IDS and not set(old)&OEB_IDS,'explicit67_plus_exact2')
need(len(base['files'])==base['file_count']==3863 and all(check_binding(row) for row in base['files']),'all3863_fresh_baseline_bindings')
need({str(p.relative_to(live)) for p in live.rglob('*') if p.is_file()}==set(base['public_file_set']) and len(base['public_file_set'])==516,'exact_current_public516_file_set')
need(bnd(O/'inputs/render_page.py')==bnd(P/'scripts/render_page.py') and bnd(O/'inputs/final-content-check.py')==bnd(P/'verification/final-content-check.py'),'installed_bases_remain_exact')
need(bnd(O/'inputs/final-content-check.py')['sha256']=='60fdabc716e9dbf887f197aa1d5e726df8675cb646404ba79603995e54ed6a80','exact_installed_ABM_checker_base')
need(bnd(O/'inputs/render_page.py')['sha256']=='07f5b47be7ad6202c1e5a66053872d2250ac4429b7e1eb9adba9af49dcdcd486','exact_installed_renderer_base')
expectedfiles={'research/index.html','research/sitemap.xml'};recordfacts={}
for rid in new:
 paper=P/'papers'/rid;c=load(paper/'publication.json');g=load(paper/'promotion.json')
 raw,view,root=odd_ear_blocking_source_view(paper,c,g);folder=O/'public/research'/c['slug'];h=(folder/'index.html').read_text();body=BodyText(h)
 need(body.bodies==1 and body.text==expected_body(c) and body.text==' '.join((O/f'public-copy-{rid}.txt').read_text().split()),'entire_actual_approved_body:'+rid)
 names={'index.html','citation.bib',c['pdf_filename'],c['supplement_filename']}
 need({p.name for p in folder.iterdir() if p.is_file()}==names,'exact_four_article_files:'+rid)
 expectedfiles|={'research/'+c['slug']+'/'+name for name in names}
 need(all((folder/n).read_bytes()==(root/n).read_bytes() for n in (c['pdf_filename'],c['supplement_filename'])),'literal_PDF_and_complete_ZIP:'+rid)
 need((folder/'citation.bib').read_text()==c['prepared_bibtex'],'literal_prepared_BibTeX:'+rid)
 need(approved_material_note(paper)==MATERIAL_NOTES[rid],'record_specific_authored_code_license:'+rid)
 anchors=body.anchors
 heading=re.findall(r'<h1>(.*?)</h1>',h,re.S);h1=BodyText('<body>'+''.join(heading)+'</body>').anchors
 nav=re.findall(r'<nav aria-label="Main navigation">(.*?)</nav>',h,re.S);research=[(a.get('href'),t) for a,t in BodyText('<body>'+''.join(nav)+'</body>').anchors if t=='Research']
 need(len(heading)==1 and [(a.get('href'),t) for a,t in h1]==[('/research/'+c['slug']+'/',c['title'])] and len(nav)==1 and research==[('/research/','Research')],'title_self_and_Main_Research_destinations:'+rid)
 recordfacts[rid]={'native_asset_order':[x['original_api_file_object']['key'] for x in raw['all_assets']],'version':c['version'],'declared_date':c['publication_date'],'created_utc':c['source_binding']['record_created_utc'],'license':c['license'],'pages':c['pdf_pages'],'root_editorial_private_only':True}
need({str(p.relative_to(O/'public')) for p in (O/'public').rglob('*') if p.is_file()}==expectedfiles and len(expectedfiles)==10,'exact_ten_file_overlay')
oldindex=(live/'research/index.html').read_text();newindex=(O/'public/research/index.html').read_text()
oi=re.findall(r'<li>.*?</li>',oldindex,re.S);ni=re.findall(r'<li>.*?</li>',newindex,re.S)
need(len(oi)==68 and len(ni)==70 and ni[:68]==oi,'old68_visible_index_entries_byteidentical')
getdata=lambda s:json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S).group(1))['mainEntity']
a,b=getdata(oldindex),getdata(newindex)
need(b['numberOfItems']==len(b['itemListElement'])==70 and b['itemListElement'][:68]==a['itemListElement'],'old68_index_JSONLD_preserved_and_two_added')
urls=re.findall(r'<loc>(.*?)</loc>',(O/'public/research/sitemap.xml').read_text())
need(len(urls)==71 and urls[:69]==frozen['baseline_sitemap_URLs_in_order'],'old69_sitemap_URLs_preserved_and_two_added')
for mode in ('normal','optimized'):
 q=load(O/mode/'pristine2-final.json');ex=load(O/mode/'pristine2-final.execution.json')
 need(q['status']=='PASS' and list(q['papers'])==new and not q['issues'] and ex['exit_code']==0 and ex['stderr_bytes']==0 and (O/mode/'pristine2-final.stderr').read_bytes()==b'' and all(len(x['checks'])==68 and all(x['checks'].values()) for x in q['papers'].values()),'pristine136_checks:'+mode)
 q=load(O/('source-controls-v2-'+mode+'.stdout'));ex=load(O/('source-controls-v2-'+mode+'.execution.json'))
 need(q['status']=='PASS' and q['pristine_acceptances']==2 and q['rejections']==37 and len(q['checks'])==39 and q['original_arguments_unchanged'] is True and q['source_fixture_writes']==0 and ex['exit_code']==0 and ex['stderr_bytes']==0,'source2_accept_37_reject:'+mode)
cs=load(O/'content-controls/SUMMARY.json');dispatch=load(O/'content-controls/DISPATCH.json')
need(cs['status']=='PASS' and cs['actual_runs']==len(cs['results'])==76 and len(dispatch['cases'])==19,'actual76_content_runs')
seen=set()
for row in cs['results']:
 mode,rid,case=(row[k] for k in ('mode','record_id','case'));key=(mode,rid,case);seen.add(key)
 d=O/'content-controls'/mode/rid/case;ex=load(d/'execution.json');m=load(d/'mutation.json');q=load(d/'qa.json');failed=[k for k,v in q['papers'][rid]['checks'].items() if not v]
 need(ex==row and row['actual_rejection_verified'] is True and row['exit_code']==1 and row['stderr_bytes']==0 and not (d/'stderr').read_bytes() and q['status']=='ISSUES_FOUND' and set(q['papers'])=={rid} and failed==row['failed_checks'] and set(m['expected_failed_checks'])<=set(failed),'actual_expected_content_rejection:'+':'.join(key))
 need(bnd(m['path'])=={'bytes':m['original_bytes'],'sha256':m['original_sha256']} and m['memory_only'] is True and m['original_sha256']!=m['virtual_sha256'],'memory_control_original_unchanged:'+':'.join(key))
need(seen=={(mode,rid,case) for mode in ('normal','optimized') for rid in new for case in dispatch['cases']},'exact76_unique_content_cases')
legacy=load(O/'legacy67/actual-old67.json');ex=load(O/'legacy67/execution.json');once=load(O/'LEGACY_SUITE_ONCE.json')
need(legacy['status']=='PASS' and list(legacy['papers'])==old and sum(len(x['checks']) for x in legacy['papers'].values())==3901 and all(all(x['checks'].values()) for x in legacy['papers'].values()) and ex['exit_code']==0 and ex['verified'] is True and not (O/'legacy67/stderr').read_bytes(),'single_actual_old67_3901_checks')
need(once['checker_dispatches_authorized']==1 and once['old_record_ids_in_order']==old and all(bnd(O/n)==v for n,v in once['tested_programs'].items()),'campaign_tested_programs_remain_exact')
memory=load(O/'memory-equivalence/SUMMARY.json');inputs=load(O/'memory-equivalence/ACTUAL_INPUT_BINDINGS.json')['bindings']
need(memory['status']=='PASS' and memory['paired_records']==67 and memory['complete_renderer_executions']==134 and memory['filesystem_output_writes']==0 and [x['record_id'] for x in memory['results']]==old,'134_actual_renderer_executions')
for row in memory['results']:
 rid=row['record_id'];d=O/'memory-equivalence';q=load(d/(rid+'.stdout'))
 need(row==load(d/(rid+'.execution.json')) and row['verified'] and row['exit_code']==0 and row['stderr_bytes']==0 and not (d/(rid+'.stderr')).read_bytes() and all(q[k] is True for k in ('current_and_proposed_actual_output_bytes_equal','original_reads_equal','renderer_receipts_equal')) and q['complete_renderer_executions']==2 and q['filesystem_output_writes']==0,'actual_output_bytes_equal:'+rid)
need(len(inputs)==1201 and all(bnd(p)==v for p,v in inputs.items()),'all1201_memory_read_inputs_preserved')
need(not (O/'memory-render-not-created').exists(),'no_legacy_output_tree_created')
preservation=load(O/'PRESERVATION.json');need(preservation['status']=='PASS' and preservation['fresh_baseline_bindings_verified']==3863 and preservation['exact_public_file_set_preserved'],'recorded_preservation_pass')
if '--preseal' not in sys.argv:
 manifest=load(O/'MANIFEST.json');seal=load(O/'SEAL.json')
 actual={str(p.relative_to(O)) for p in O.rglob('*') if p.is_file()}-{'MANIFEST.json','SEAL.json'}
 need(actual=={x['relative_path'] for x in manifest['files']} and len(actual)==manifest['payload_file_count'],'entire_own_payload_file_set')
 need(all(bnd(O/x['relative_path'])=={k:x[k] for k in ('bytes','sha256')} for x in manifest['files']),'all_own_payload_hashes')
 need(seal['manifest']==bnd(O/'MANIFEST.json') and seal['status']=='PRIVATE_TWO_RECORD_STAGE_SEALED_FOR_ROOT_REVIEW' and seal['production_integration_authorized'] is False,'whole_own_manifest_seal')
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','checks_passed':len(checks),'preseal':'--preseal' in sys.argv,'fresh_baseline_bindings':3863,'current_public_files':516,'overlay_files':10,'predicted_integrated_public_files':524,'index_items':70,'sitemap_URLs':71,'actual_old67_checks':3901,'actual_paired_renderer_executions':134,'actual_content_rejections':76,'records':recordfacts,'checker_renderer_or_control_campaigns_replayed':False,'writes':0},indent=2))
