"""Freeze bounded read-only legacy preflight; no original or Git mutations."""
from pathlib import Path
import datetime,hashlib,json,re,subprocess
from scan import O,P,G,C,PIN,OLD,git,blob,sha,save,checkpoint

if (O/'FINAL_SEAL.json').exists():raise RuntimeError('sealed_packet_no_rewrite')
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
remote=git('ls-remote','--exit-code','origin','refs/heads/main').decode();end=remote.split()[0]
git('cat-file','-e',end+'^{commit}')
starttree=git('rev-parse',PIN+':docs').decode().strip();endtree=git('rev-parse',end+':docs').decode().strip()
if starttree!=endtree:raise RuntimeError('new_remote_docs_tree_requires_additive_review')
(O/'remote-main-end.txt').write_text(remote)
save('REMOTE_END_REVALIDATION.json',{'UTC':utc,'start_remote_pin':PIN,'end_remote_pin':end,'start_docs_tree':starttree,'end_docs_tree':endtree,'docs_trees_identical':True,'exact_docs_delta':git('diff-tree','--no-commit-id','--name-status','-r',PIN,end,'--','docs').decode(),'end_commit_already_cached':True,'no_fetch_or_git_write':True,'local_HEAD':git('rev-parse','HEAD').decode().strip(),'local_branch_symbolic_ref':git('symbolic-ref','-q','HEAD').decode().strip()})
entries=json.loads((O/'docs-tree.json').read_text())['entries'];identities=json.loads((O/'CURRENT_IDENTITIES.json').read_text())['targets']
target_hashes={}
for target in identities:
    rid=target['record_id'];s=P/'papers'/rid/'sources';ready=json.loads((s/'SOURCE_READY.json').read_text());assets=ready['actual_assets'] if 'actual_assets' in ready else ready['all_actual_assets']
    for item in assets:
        path=Path(item['path']);data=path.read_bytes();expected=item.get('SHA256',item.get('sha256'));api=item['api_file_object'];md5=item.get('MD5',item.get('md5'))
        if sha(data)!=expected or hashlib.md5(data).hexdigest()!=md5 or len(data)!=api['size'] or api['checksum']!='md5:'+md5:raise RuntimeError('actual_source_asset_binding_failed')
        target_hashes[expected]={'record_id':rid,'source_path':str(path)}
    tp=Path(target['controlling_TeX']['path']);target_hashes[sha(tp.read_bytes())]={'record_id':rid,'source_path':str(tp)}
source_comparisons=[]
for entry in entries:
    if Path(entry['path']).suffix.lower() not in ['.tex','.zip']:continue
    data=blob(entry['path']);source_comparisons.append({**entry,'SHA256':sha(data),'identical_current_source_asset':target_hashes.get(sha(data))})
save('source-assets-byte-comparison.json',{'pin':PIN,'comparison':'All tracked standalone legacy TeX/ZIP bytes against actual current selected published assets and controlling TeX; no source execution or archive replay.','legacy_assets':source_comparisons,'matches':[x for x in source_comparisons if x['identical_current_source_asset']]})
pdfs=json.loads((O/'pdf-identity-inventory.json').read_text())['documents']
explanations={
 'docs/papers/fps-equality/paper.pdf':'Full4pp actual reader and moved HTML read; inscribed-simplex equality in a second-moment inequality, not SOS-density rate.',
 'docs/papers/gamma-theta-order-12-frontier/paper.pdf':'p5 spanning-tree color class is a dominating-set bound, not all-root objective hardness.',
 'docs/papers/cyclic-bell-exact-values-and-randomness/paper.pdf':'p1 exact quantum Bell SOS identity, not polynomial density hierarchy.',
 'docs/papers/equal-sum-product/paper.pdf':'p1 elementary finite sum-product matrix SOS identity.',
 'docs/papers/hadamard-668-repair-obstructions/paper.pdf':'p8 finite root-energy sum-of-squares systems for Hadamard repair.',
 'docs/papers/lalonde-quantum-coloring/paper.pdf':'pp1,3 projector-coloring rational/trace SOS certificate.',
 'docs/papers/no-universal-death-birth-amplifier/paper.pdf':'pp1,2,5 incoming-weight-column sum-of-squares correction for fixation.',
 'docs/papers/permutation-blind-bell-randomness/paper.pdf':'p1 Bell maximizer certificate, not Lebesgue/SOS-density convergence.'}
save('EXCLUSIONS.json',{'pin':PIN,'actual_topic_hits':[{'path':x['path'],'git_blob':x['git_blob'],'SHA256':x['SHA256'],'pages':x.get('pages'),'matching_page_numbers':sorted({z['page'] for q in x.get('query_hits',{}).values() for z in q}),'reason':explanations[x['path']],'correspondence':False} for x in pdfs if x.get('query_hits')],'nonpublic_project_paths_are_articles':False,'external_or_OWR_archive_accepted_as_article':False})
outcomes=[{'record_id':x['record_id'],'title':x['title'],'reader_SHA256':x['PDF']['SHA256'],'reader_pages':x['pages'],'status':'NO_CORRESPONDING_ARTICLE_IDENTIFIED_IN_PINNED_DOCS_TREE','corresponding_legacy_URL':None,'redirect_candidates':[],'redirect_proposed':False} for x in identities]
save('IDENTITY_VERDICT.json',{'UTC':utc,'assignment_status':'COMPLETE','completion_estimate_percent':100,'start_pin':PIN,'end_pin':end,'docs_tree':starttree,'targets':outcomes,'bounded_negative_not_global_nonexistence':True,'novelty_or_firstness_certified':False,'new_scientific_verdict':False,'next_three_stage_started':False,'root_authority_retained':True,'overall203_programme_complete':False})
before=json.loads((O/'protected-before.json').read_text());changes=[]
for item in before['files']:
    p=Path(item['path']);digest=sha(p.read_bytes()) if p.is_file() else None
    if digest!=item['SHA256']:changes.append({'path':str(p),'before_SHA256':item['SHA256'],'after_SHA256':digest,'actual_after_bytes':p.read_text() if str(p)==str(G/'.git/refs/remotes/origin/main') else None})
allowed=str(G/'.git/refs/remotes/origin/main')
if any(x['path']!=allowed for x in changes):raise RuntimeError('nonref_original_changed:'+repr(changes))
if changes and (G/'.git/refs/remotes/origin/main').read_text().strip()!=end:raise RuntimeError('concurrent_ref_does_not_equal_fresh_end_pin')
save('PRESERVATION_RECEIPT.json',{'UTC':utc,'protected_files':len(before['files']),'unchanged_files':len(before['files'])-len(changes),'nonref_originals_unchanged':True,'production_public_files_unchanged':484,'prior_sealed_two_record_stage_unchanged':True,'only_concurrent_ref_changes':changes,'preflight_git_operations':'ls-remote,rev-parse,cat-file,ls-tree,show,diff-tree,grep,check-ignore,symbolic-ref; read-only; no fetch/checkout/write operation','no_shared_site_config_native_or_original_mutation_by_this_preflight':True})
selected=json.loads((O/'selected-render-custody.json').read_text())['images']
save('READ_LEDGER.json',{'UTC':utc,'current_manuscripts':[{'record_id':x['record_id'],'full_actual_PDF_text_read':True,'pages':x['pages'],'full_controlling_TeX_read':True,'PDF_path':x['PDF']['path'],'PDF_SHA256':x['PDF']['SHA256'],'TeX_path':x['controlling_TeX']['path'],'TeX_SHA256':x['controlling_TeX']['SHA256'],'visual_identity_pages':[1,x['pages']]} for x in identities],'complete_pinned_index_visible_text_read':True,'all47_HTML_identity_metadata_inventory_read':True,'all34_sitemap_URLs_read':True,'all8_weak_PDF_matching_page_contexts_read':True,'full_old_FPS_four_page_reader_and_moved_HTML_read':True,'other_unrelated_old_PDF_bodies_read_entirely':False,'854_page_scope':'Automated extraction/search only, not individual complete reading.','selected_renders_visually_inspected':[{'record_or_exclusion':x['record_or_exclusion'],'page':x['page'],'render_SHA256':x['render_SHA256']} for x in selected],'supplemental_HTML_hit_contexts_read':True,'no_historical_source_audit_or_OWR_archive_used_as_identity_substitute':True})
checkpoint('No corresponding article for any current target; all weak identities excluded. Fresh end pin has identical docs tree; all1553 non-ref protected bindings unchanged, concurrent cached origin/main movement explicitly recorded. No redirect or next3stage prepared.',100)
cache=[]
for p in sorted(C.rglob('*')):
    if p.is_file():cache.append({'path':str(p.relative_to(O)),'bytes':p.stat().st_size,'SHA256':sha(p.read_bytes())})
save('CACHE_MANIFEST.json',{'UTC':utc,'cache_verified_ignored_before_write':True,'ignore_receipt':'cache-ignore-receipt.txt','files':cache})
owned=[]
for p in sorted(O.rglob('*')):
    if p.is_file() and not p.is_relative_to(O/'tmp') and p.name not in ['FINAL_MANIFEST.json','FINAL_SEAL.json'] and '__pycache__' not in p.parts:
        if p.is_symlink():raise RuntimeError('no_owned_symlinks')
        owned.append({'path':str(p.relative_to(O)),'bytes':p.stat().st_size,'SHA256':sha(p.read_bytes())})
save('FINAL_MANIFEST.json',{'UTC':utc,'status':'IMMUTABLE_BOUNDED_LEGACY_PREFLIGHT','namespace':str(O),'files':owned,'ignored_cache_manifest':'CACHE_MANIFEST.json'})
save('FINAL_SEAL.json',{'UTC':utc,'status':'SEALED_COMPLETE_NO_LEGACY_CANDIDATES','manifest':'FINAL_MANIFEST.json','manifest_SHA256':sha((O/'FINAL_MANIFEST.json').read_bytes()),'owned_bindings':len(owned),'ignored_cache_bindings':len(cache),'completion_estimate_percent':100,'publication_or_redirect_authority':False,'overall203_programme_complete':False,'preserve_original':True})
print(json.dumps({'status':'SEALED','owned_bindings':len(owned),'ignored_cache_bindings':len(cache),'manifest_SHA256':sha((O/'FINAL_MANIFEST.json').read_bytes()),'seal_SHA256':sha((O/'FINAL_SEAL.json').read_bytes()),'end_remote_pin':end,'unchanged_docs_tree':starttree},indent=2))
