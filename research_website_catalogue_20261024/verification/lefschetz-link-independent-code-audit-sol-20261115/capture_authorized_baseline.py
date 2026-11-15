"""Fresh605baseline capture only after root's conditional GO and own initialseal.
No stage writer/candidate access, source/site/Git writes or programme execution.
All snapshots are private ignored blobs; no public upload claim.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,re,xml.etree.ElementTree as ET
A=Path(__file__).resolve().parent;B=A.parents[1];W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
def need(ok,why):
 if not ok:raise ValueError(why)
def binding(b):return {'bytes':len(b),'SHA256':sha256(b).hexdigest()}
def listing(p):
 q=list(p.rglob('*'));need(not any(r.is_symlink() for r in q),'namespace symlinks');return sorted(r for r in q if r.is_file())
def save(n,o):
 p=A/n;need(not p.exists(),'immutable baselinefile');p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
need(sha256((A/'INITIAL_SEAL.json').read_bytes()).hexdigest()=='b8c8a28283a56d5108d351952fb5171043811888e17c52522e6457e4a0e3c44e','substantialinitialsealbeforeactualwebsite')
need((A/'baseline/.gitignore').read_text().splitlines()==['blobs/'],'entirebaselineblobs ignoredfirst')
need(not (A/'baseline/blobs').exists(),'new privatebaseline');(A/'baseline/blobs').mkdir()
commit='27cd946786754d66b44cbb309dae76da238b133e';receipt_path=B/'verification/nash-quotient-robinson-production-integration-preparation-sol-20261115/run-state/PUBLICATION.json';receipt=json.loads(receipt_path.read_text())
need(receipt['commit']==commit and receipt['counts']==[605,90,91] and receipt['deployed'] is False and receipt['native_Sheet_publication_verified'] is False,'actualrootpublicationreceipt notliveauthority')
def snapshot(p):
 b=p.read_bytes();h=sha256(b).hexdigest();dest=A/'baseline/blobs'/h
 if dest.exists():need(dest.read_bytes()==b,'contentaddressedblobcollision')
 else:dest.write_bytes(b)
 return {'original':str(p),'blob':'baseline/blobs/'+h,**binding(b)}
files=listing(W/'public');need(len(files)==605,'fresh605publicnamespace')
rows=[snapshot(p) for p in files];configs=[snapshot(W/n) for n in ['firebase.json','.firebaserc']];pubreceipt=snapshot(receipt_path)
index=(W/'public/research/index.html').read_text();blocks=list(re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',index,re.S));need(len(blocks)==1,'oneindexJSONLD');schema=json.loads(blocks[0][1]);items=schema['mainEntity']['itemListElement'];lis=re.findall(r'<li>.*?</li>',index,re.S)
sitemap=(W/'public/research/sitemap.xml').read_text();nodes=re.findall(r'<url>.*?</url>',sitemap,re.S)
need(schema['mainEntity']['numberOfItems']==len(items)==len(lis)==90,'actual90typedandvisibleentries');need(len(nodes)==len(ET.fromstring(sitemap))==91,'actual91wholeXMLnodes')
E=json.loads((A/'EXPECTED_OUTPUTS.json').read_text());baselinepaths={str(p.relative_to(W/'public')) for p in files};overlay=set(E['exact_overlay_paths'])
need(baselinepaths&overlay=={'research/index.html','research/sitemap.xml'} and len(baselinepaths|overlay)==614 and len(baselinepaths-overlay)==603,'independentactual11overlay/9new/614union')
# Existing qualified core metadata only; no old website aggregate is adopted.
oldcorepath=B/'verification/nash-quotient-robinson-private-stage-sol-20261115/CORE_INPUTS.json';oldcore=json.loads(oldcorepath.read_text());core=[];unchanged=0
for row in oldcore['files']:
 p=Path(row['path']);r=snapshot(p);need(r['bytes']==row['bytes'] and r['SHA256']==row['SHA256'],'wholequalifiedcurrentcore')
 prior=next(q for q in oldcore['original_core_file_bindings'] if q['path']==str(p))
 if p.name=='checkpoint_subtree.py':need(r['SHA256']=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0','onlyrootauthorizedcheckpointpin')
 else:need(r['bytes']==prior['bytes'] and r['SHA256']==prior['SHA256'],'17originalunchanged');unchanged+=1
 core.append(r)
need(len(core)==18 and unchanged==17,'18current17unchangedqualification')
metadata=[snapshot(oldcorepath)]+[snapshot(Path(row['path'])) for row in oldcore['authority_metadata']]
need([str(p) for p in listing(W/'public')]==[str(p) for p in files],'exact605membership stableacrosssnapshot')
for row in rows+configs+core:need(Path(row['original']).read_bytes()==(A/row['blob']).read_bytes(),'fullfreshoriginalmatchescopy')
for n in ['index.html','sitemap.xml','research.css']:(A/'baseline'/n).write_bytes((W/'public/research'/n).read_bytes())
now=datetime.now(timezone.utc).isoformat()
save('BASELINE.json',{'UTC':now,'initial_expectation_seal_beforecapture':'b8c8a28283a56d5108d351952fb5171043811888e17c52522e6457e4a0e3c44e','root_GO_commit':commit,'actual_HEAD_and_origin_master_verified_by_readonlyGit_command':commit,'website_branch':'master','website_root':str(W),'public_files':rows,'site_configs':configs,'root_publication_receipt':pubreceipt,'whole_literal_root_publication_receipt':receipt,'old_complete_index_schema':schema,'old90typedorderedItemList':items,'old90visible_li_bytes':lis,'old91wholeXMLnodebytes':nodes,'actual_counts':[605,90,91],'derived_union_counts':[614,92,93],'new_leaves':9,'overlay_paths':11,'old_nonaggregate_files_preserved':603,'core_files':core,'core_authority_metadata':metadata,'core_qualification':{'current_bindings':18,'original_unchanged':17,'only_authorized_changed_checkpoint_SHA256':'405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0','all18unchanged_claimed':False},'old_593_website_aggregate_adopted':False,'no_Git_index_or_ref_fence':True,'native_verified_published_count_from_root_only':87,'newtriplet_deploy_browser_native_AA_pending':True,'all90verified_claimed':False,'site_source_core_Sheet_Git_or_contact_mutations':False,'writer_implementation_report_outputs_still_unread':True,'publication_authority':False,'canonical_url':None,'AA':None,'follow_up':None})
save('BASELINE_CAPTURE.json',{'UTC':now,'actual_independent_source_and_counts_verified':True,'root_GO_commit':commit,'actual_counts':[605,90,91],'all605public_bufferbytes_snapshotted':True,'derived_virtual_counts':[614,92,93],'paired_stage_outputs_available_or_read':False,'root_native_verified_publications':87,'all90verified_claimed':False,'raw_blobs_ignored_before_creation':True,'completion_percent_bounded_audit':45})
print(json.dumps({'actual_baseline':[605,90,91],'derived_virtual':[614,92,93],'public_buffers':len(rows),'exact_overlay_paths':11,'new_leaves':9,'core_current':18,'core_original_unchanged':17,'source_site_or_Git_writes':False,'writer_still_unread':True,'completion_percent':45}))
