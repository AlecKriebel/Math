#!/usr/bin/env python3
"""Reconcile exact bytes and dated history, then seal the bounded repair."""
from pathlib import Path
import collections,datetime,difflib,hashlib,json
HERE=Path(__file__).resolve().parent;AUDIT=HERE.parent.parent;PACKAGE=AUDIT/'preprint_v1_0'
CHANGED={'build_archive.py','verify_package.py','README.md','EXCLUSION_LEDGER.json','SUPPORT_ALLOWLIST.json','SUPPORT_MANIFEST.json','COPY_MAP.json','SAFE_INPUT_PINS.json','publication/DEPOSIT_BINDING.json','support.zip'}
def require(c,m):
 if not c:raise ValueError(m)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(p.read_text())
def rec(p,base):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return {'path':p.relative_to(base).as_posix(),'bytes':p.stat().st_size,'sha256':h.hexdigest()}
def match(p,r):
 if not p.is_file() or p.is_symlink():return False
 actual=rec(p,p.parent);return actual['bytes']==r['bytes'] and actual['sha256']==r['sha256']
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def packagefiles():return [p for p in sorted(PACKAGE.rglob('*')) if p.is_file() and not {'tmp','__pycache__'}.intersection(p.relative_to(PACKAGE).parts)]
def main():
 require(not (HERE/'SEAL.json').exists(),'already sealed')
 baseline=load(HERE/'INPUT_PINS.json')['records'];saved={r['path']:r for r in load(HERE/'BEFORE_PINS.json')['entries']}
 before_paths={};changes=[];unchanged=[];index=collections.defaultdict(list);bysha=collections.defaultdict(list)
 for r in baseline:
  p=AUDIT/r['path']
  if match(p,r):unchanged.append(r);before_paths[r['path']]=p
  else:
   require(r['path'] in saved,'unauthorized mutation '+r['path']);old=HERE/saved[r['path']]['preserved_path'];require(match(old,r),'before missing '+r['path'])
   before_paths[r['path']]=old;changes.append({'path':r['path'],'before':r,'after':rec(p,AUDIT),'preserved_path':old.relative_to(AUDIT).as_posix()})
  index[(r['bytes'],r['sha256'])].append(before_paths[r['path']]);bysha[r['sha256']].append(before_paths[r['path']])
 require({r['path'].removeprefix('preprint_v1_0/') for r in changes}==CHANGED,'changed set differs')
 for name,r in saved.items():require(match(HERE/r['preserved_path'],r),'saved exact bytes differ '+name)
 for n in ['FINAL_SEAL.json','FINAL_INTEGRITY.json']:
  require(any(r['path']==n for r in unchanged),'dated final history changed '+n)
 # Inspect every pre-existing valid JSON at its actual captured bytes, not the
 # corresponding mutable current pathname. Each file/hash reference is recorded.
 stages=[];omissions=[];jsonfiles=0;reference_count=0;resolved_count=0
 labels=['path','snapshot_path','source_path','package_path','image','name']
 for r in baseline:
  original=before_paths[r['path']]
  if original.suffix!='.json':continue
  try:obj=load(original)
  except (ValueError,UnicodeError):continue
  jsonfiles+=1;refs=[]
  def visit(x,locator='$'):
   nonlocal reference_count,resolved_count
   if isinstance(x,dict):
    if isinstance(x.get('sha256'),str) and len(x['sha256'])==64 and any(k in x and isinstance(x[k],str) for k in labels):
     size=x.get('bytes',x.get('size'));possible=index.get((size,x['sha256']),[]) if isinstance(size,int) else bysha.get(x['sha256'],[])
     row={'locator':locator,'identifiers':{k:x[k] for k in labels if k in x},'sha256':x['sha256']}
     if isinstance(size,int):row['bytes']=size
     reference_count+=1
     if possible:
      # Prefer the exact named path where possible, then an exact retained
      # stage artifact with identical bytes. No hash is rebound to new bytes.
      names=set(row['identifiers'].values());chosen=next((p for p in possible if p.relative_to(AUDIT).as_posix() in names),possible[0])
      row.update(status='RESOLVED_EXACT_RETAINED_BYTES',resolved_path=chosen.relative_to(AUDIT).as_posix(),actual_bytes=chosen.stat().st_size);resolved_count+=1
     else:
      row['status']='INDIVIDUALLY_UNRESOLVED_NOT_REPLAYED_OR_AUTHENTICATED'
      if x['sha256']=='3cceebbd4a4db6264b13adc04460809fc90d4f72918c10f29829e5817f5f5743':
       row['reason']='Pre-existing package02 CHANGE_INVENTORY added-file reference, also distributed as exact dated history, points to a 29119-byte stage-seal digest for which no exact artifact is retained in the entire frozen audit. The immutable actual CURRENT_OUTPUT_PINS_WHOLE03 digest 7a4378d695e7206eb5681a8d3fcecf171ffdc2e025ba2d9cfd081aa9d91cadbb and later valid stage seals resolve exactly. This inventory reference is explicitly unsupported; no missing old blob, successful resolver or original-stage replay is claimed. Neither old inventory nor actual seal is rewritten.'
      elif '/tmp/' in r['path'] and ('bad_binding' in r['path'] or 'bad_binding' in str(row['identifiers'])):
       row['reason']='Intentionally invalid historical binding fixture: false hash or mismatched byte count is negative-test data, not an expected authentic file. Frozen fixture bytes remain unchanged; no artifact is manufactured for the invalid reference.'
      else:row['reason']='No exact file artifact in the frozen audit; individually omitted from any successful historical-byte/replay claim. Original referencing JSON is preserved and hash-pinned.'
      omissions.append(dict(manifest=r['path'],**row))
     refs.append(row)
    for k,v in x.items():visit(v,locator+'/'+k)
   elif isinstance(x,list):
    for i,v in enumerate(x):visit(v,locator+'/'+str(i))
  visit(obj)
  if refs:stages.append({'manifest':r,'resolved_manifest_path':original.relative_to(AUDIT).as_posix(),'records':refs})
 require(len(omissions)==5,'unexpected new historical gaps; inspect individually')
 write(HERE/'PRIOR_PIN_RESOLUTIONS.json',{'utc':utc(),'scope':'Every SHA256 plus file-identifier reference in ALL pre-existing valid JSON files was traversed at exact captured bytes; size/bytes checked when recorded. Missing records are individual omissions, never silent replacements. This is byte custody, not fresh source authentication, Git verification, mathematical review or execution of historical omitted programs.','valid_JSON_files':jsonfiles,'referenced_manifests':len(stages),'reference_occurrences':reference_count,'exact_resolutions':resolved_count,'individual_unresolved_occurrences':len(omissions),'manifests':stages})
 write(HERE/'INDIVIDUAL_OMISSIONS.json',{'scope':'Five pre-existing historical file-reference occurrences do not resolve as authentic file artifacts. Exact missing stale inventory pointer is disclosed twice; three deliberately invalid binding-fixture pointers are negative-test data. All source JSON itself remains exact. No old stage verdict or pin is edited.','records':omissions})
 copies=load(PACKAGE/'COPY_MAP.json')['copies'];old=load(HERE/'before/preprint_v1_0/COPY_MAP.json')['copies'];require(len(old)==163 and len(copies)==165 and copies[:163]==old,'old exact copy map changed')
 require(load(PACKAGE/'SAFE_INPUT_PINS.json')['records']==copies,'SAFE input map differs')
 for r in copies:require(match(AUDIT/r['source_path'],r) and match(PACKAGE/r['package_path'],r),'copy/source byte mismatch '+r['source_path'])
 require(sum(r['source_path'].startswith('submitted/') for r in copies)==9,'nine submitted originals coverage differs')
 submitted=load(AUDIT/'SUBMITTED_PINS.json')['files'];require(len(submitted)==9,'submitted count differs')
 for r in submitted:require(match(AUDIT/r['snapshot_path'],r),'submitted original differs')
 allow=load(PACKAGE/'SUPPORT_ALLOWLIST.json')['members'];excluded=load(PACKAGE/'EXCLUSION_LEDGER.json')['local_package_files'];files=packagefiles();actual={p.relative_to(PACKAGE).as_posix() for p in files}
 require(actual==set(allow)|set(excluded) and not set(allow)&set(excluded),'current complete inclusion/exclusion coverage differs')
 for source in load(HERE/'CASE1064_FINDING.json')['sources']:
  require(match(AUDIT.parent.parent/source['path'],source),'external scope source changed')
 selection=load(PACKAGE/'CASE_ALIAS_SELECTION_LEDGER.json')['records'];require(len(selection)==2 and all(r['included'] for r in selection),'new selection count differs')
 for r in selection:require(match(AUDIT/r['source_path'],r) and match(PACKAGE/r['package_path'],r),'new selection mismatch')
 binding=load(PACKAGE/'publication/DEPOSIT_BINDING.json');oldbinding=load(HERE/'before/preprint_v1_0/publication/DEPOSIT_BINDING.json')
 require(binding['paper_pdf']==oldbinding['paper_pdf'] and binding['schema_version']==oldbinding['schema_version'],'PDF/schema binding changed')
 require(match(PACKAGE/'support.zip',binding['support_archive']),'ZIP binding differs')
 metadata=load(PACKAGE/'metadata.json');require(all(load(PACKAGE/n)['metadata']==metadata for n in ['publication/release_metadata.json','publication/zenodo.json','publication/zenodo-deposit.json']),'bibliographic objects differ')
 semantic=['paper.pdf','paper.tex','metadata.json','publication/release_metadata.json','publication/zenodo.json','publication/zenodo-deposit.json','ATTRIBUTION.md','LICENSE.txt','SOURCE_LEDGER.json','fresh_guard_checker.py','run_checks.py','build_pdf.py','TERMINAL_STATUS.json','TERMINAL_ACCEPTANCE.md','TERMINAL_OUTPUT_PINS.json','CURRENT_OUTPUT_PINS.json','CURRENT_OUTPUT_PINS_WHOLE03.json','OUTPUT_PINS.json','STATUS.json','CURRENT_STATUS.json','CURRENT_STATUS_WHOLE03.json']
 lookup={r['path']:r for r in unchanged}
 for n in semantic:require('preprint_v1_0/'+n in lookup,'protected semantic input changed '+n)
 require(rec(PACKAGE/'paper.pdf',PACKAGE)['sha256']=='67f07f64a5b06c9a4372c285ed438e735fb780d8477b25652bea4f7f6c72e072','PDF pin differs')
 require(rec(PACKAGE/'paper.tex',PACKAGE)['sha256']=='22b01481733113dee52f7c6e2e160f519d580110ee7a9665b2117f77705d2a31','TeX pin differs')
 additions=[rec(p,AUDIT) for p in files if p.relative_to(AUDIT).as_posix() not in {r['path'] for r in baseline}]
 require(len(additions)==6,'added current file count differs')
 write(HERE/'CHANGE_INVENTORY.json',{'utc':utc(),'scope':'Only bounded physical-output guard, current workflow/adoption documentation, exact new authored evidence copies, manifests/ZIP/binding; mathematical and native bibliographic bytes unchanged. All existing-file changes were atomic replacement.','modified':changes,'added_package_files':additions,'authorized_existing_changes':10,'old_copy_records_unchanged':163,'new_exact_copies':2,'publication_ready':False,'new_complete_whole04_required':True,'root_repair_adoption_required':True})
 write(HERE/'PROTECTED_BYTE_RECEIPT.json',{'utc':utc(),'pass':True,'all_prior_regular_inputs':len(baseline),'authorized_modified_existing':len(changes),'unchanged_prior_regular_inputs':len(unchanged),'unchanged_records':unchanged,'explicit_semantic_inputs':[lookup['preprint_v1_0/'+n] for n in semantic],'all_dated_reports_seals_originals_raw_source_tree_and_cache_bytes_unchanged':True,'all_ten_exact_before_bytes_valid':True,'native_manifest_entire_bytes_unchanged':True,'bibliographic_objects_exact_equal':True,'old163_copy_map_records_exact':True,'all165_sources_and_copies_match':True,'current_files':len(files),'archive_members':len(allow),'excluded_local_package_files':len(excluded),'historical_unsupported_reference_occurrences':len(omissions)})
 write(HERE/'COPY_EXCLUSION_RECEIPT.json',{'pass':True,'archive_members':allow,'excluded_current_local_files':excluded,'new_exact_selections':selection,'all_existing163_copies_exact':True,'current165_copies_source_equal':True,'current_package_exact_union':True,'private_prior_regular_inputs_hash_only':len(baseline),'third_party_bodies_or_pixels_runtime_or_old_archives_added_to_delivery':False,'full_scope_evidence_excerpt_explicit_and_fullsource_pinned':True,'historical_omitted_programs_or_original_stage_replays_claimed':False})
 diff=[]
 for change in changes:
  if change['path'].endswith('/support.zip'):continue
  oldp=AUDIT/change['preserved_path'];newp=AUDIT/change['path']
  diff+=list(difflib.unified_diff(oldp.read_text().splitlines(True),newp.read_text().splitlines(True),fromfile='before/'+change['path'],tofile=change['path']))
 for r in additions:
  diff+=list(difflib.unified_diff([],(AUDIT/r['path']).read_text().splitlines(True),fromfile='/dev/null',tofile=r['path']))
 (HERE/'COMPLETE_CODE_PROSE_DIFF.patch').write_text(''.join(diff))
 write(HERE/'FINAL_CURRENT_PINS.json',{'utc':utc(),'scope':'All210 repaired current non-temporary package files, including the separate209-record stage seal.','records':[rec(p,PACKAGE) for p in files]})
 commands=[json.loads(s) for s in (HERE/'EXECUTIONS.jsonl').read_text().splitlines()];require(len(commands)==145 and all((r['returncode']==0)==r['expected_success'] for r in commands),'actual command accounting differs')
 reproduction=load(HERE/'REPRODUCTION_RECEIPTS.json');require(reproduction['pass'] and reproduction['actual_commands']==145 and not (HERE/'scratch').exists(),'validation not settled')
 ziprec=rec(PACKAGE/'support.zip',PACKAGE);pdfrec=rec(PACKAGE/'paper.pdf',PACKAGE);texrec=rec(PACKAGE/'paper.tex',PACKAGE)
 report=f'''# PR1064 CASE-1064 bounded repair

The fresh internal-output case-alias bypass is repaired and passes focused static-filesystem controls. Current status is PENDING_ROOT_CASE_ALIAS_REPAIR_ADOPTION_AND_NEW_COMPLETE_WHOLE04. ROOT repair adoption and a NEW COMPLETE whole04 review remain required; this is not a whole-package review or a new mathematical acceptance. Publication/published/issues flags remain false and the ordered service hold remains after PR1032.

## Claim, scope and mechanism

The exact repaired claim is that build_archive.py permits support.zip or tmp/ inside the kit and ZIP outputs outside it, but rejects fresh unlisted physically internal destinations before directory creation or opening the writer. Path.resolve() can preserve case-alias spelling on the actual case-insensitive filesystem, making the previous lexical containment test insufficient. The replacement walks all output ancestors, including above absent components, and uses samefile against the actual kit root to return the remaining relative suffix. Existing tmp ancestry is also checked by identity. It makes no lowercase or portable case-folding assumption. The original direct/resolved/samefile protected-input loop runs unchanged first. No hostile concurrent-filesystem security claim is made.

Read the FULL program scope report and ROOT_CASE_ALIAS_SCOPE_REVIEW.json, the current full README/builder/verifier/checker/PDF interfaces, original submitted manifest, and root mathematical/priority/whole03 adoptions. The submitted set is exactly nine files. The scope finding is a P3 support-location contract defect; existing-input protection already existed, and the finding is not an overwrite or mathematical defect. The two new authored delivery copies are MECHANISM.md and an explicitly labelled PR1064-only exact excerpt/selected root reproduction evidence, with hashes for the complete source report/adoption. Other PR evidence is deliberately excluded.

## Custody and bounded changes

INPUT_PINS.json froze all {len(baseline)} prior regular audit files by hash only BEFORE any candidate mutation. Source bodies, raw Git/tree captures, pixels, caches, old scratch and all other prior files were read only for hashes; no complete backup was made. BEFORE_PINS.json binds the exact old bytes of every one of the ten permitted existing edits, including the old ZIP kept locally. Atomic replacement avoided writing through historical hardlinks. All {len(unchanged)} other prior regular inputs remain exact, including FINAL_SEAL.json, FINAL_INTEGRITY.json, every dated review/adoption, submitted originals, source/body/cache and old working-tree artifacts.

The ten modified existing files are build_archive.py, verify_package.py, README.md, COPY_MAP.json, SAFE_INPUT_PINS.json, EXCLUSION_LEDGER.json, SUPPORT_ALLOWLIST.json, SUPPORT_MANIFEST.json, support.zip, and publication/DEPOSIT_BINDING.json. Six package files were added: current repair status/acceptance, selected-evidence ledger, two exact authored copies and a separate excluded CASE_ALIAS_OUTPUT_PINS.json. The old163 copy records keep exact order/values; all165 current source/destination bytes match. The current210 files are exactly the union of198 archive members and12 local exclusions. Complete text/JSON additions and edits are in COMPLETE_CODE_PROSE_DIFF.patch; binary ZIP change is fully pinned in CHANGE_INVENTORY.json and ZIP_VERIFICATION.json.

Current status preserves three prior whole reviews (minimum two), latest prior whole03 zero on its dated bytes, and explicitly says the new P3 repair needs ROOT adoption plus NEW COMPLETE whole04. Earlier terminal/readiness records and counts remain byte-exact history. New verifier guards reject coherent attempts to change current gates; old readiness is never relabelled as the verdict on repaired bytes.

## Actual focused validation

All145 recorded subprocess commands settled with their expected outcomes: {sum(r['returncode']==0 for r in commands)} successes and {sum(r['returncode']!=0 for r in commands)} expected nonzero rejections. Four standard-library README commands ran in both normal and optimized Python from a clean ZIP extraction. run_checks.py kept the original entropy checker in normal assertion-active mode; its explicit-guard diagnostics/fault controls retain their disclosed normal/optimized scope. No historical omitted program is represented as newly replayed.

Twenty location controls cover real samefile case aliases with distinct resolve spellings in both script-root directions and both execution modes, fresh leaves, one/two absent descendants and canonical-spelling controls. Each forbidden target and first absent ancestor stayed absent. Sixteen allowed-output controls cover canonical support.zip, tmp/ with missing descendants, actual external ZIPs, and existing tmp case aliases; all outputs matched the canonical ZIP. Eighty representative protected-input controls cover ten current/excluded inputs through direct, file-symlink, hardlink and directory-symlink aliases in both modes. These include paper/source, metadata, builder/verifier, current repair status, manifest, external binding, old terminal seal and native manifest. Every protected extracted member and every canonical current package byte remained unchanged across validation. Representative guards are not described as exhaustive tests of every potential filesystem topology.

Ten strict-binding controls cover valid required presence, required absence, malformed missing fields, wrong archive identity and extra fields in both modes. Ten coherent current-stage negative controls rehash the mutable scratch manifest, then reject false review/adoption/publication/hold values at the verifier. The actual repository-native zenodo.py LOCAL check selected exactly this PDF and ZIP. It did not create a client, read a token, contact a service, create a draft, upload, issue a DOI or publish.

A separate independent ZIP constructor closed the archive before comparing the COMPLETE bytes. Its result is exactly the current canonical ZIP. All198 member names/order, bytes, UTF8 (except PDF), fixed timestamps, Unix0644 regular modes, compression, flags and CRC32 values were checked. Compressor environment is recorded; cross-environment zlib identity remains qualified. The one own extraction/scratch tree was removed only after commands settled and final protected-byte comparisons. No ENOSPC failure occurred in this repair; no planned or incomplete test is counted.

## Historical resolution and exact remaining limits

PRIOR_PIN_RESOLUTIONS.json traverses every SHA256/file-identifier object in all {jsonfiles} pre-existing valid JSON files at their ACTUAL captured bytes, resolving {resolved_count} of {reference_count} reference occurrences to exact retained artifacts. It records every resolution and every individual gap, including references that lack a stored byte count. This extends beyond the named immutable stage seals. No historical path is silently rebound to changed current bytes and no source/Git authentication or historical-stage execution is inferred from matching hashes.

Five references do not represent resolved authentic artifacts. Two are the same pre-existing stale package02 CHANGE_INVENTORY.added_package_files[0] pointer, copied verbatim into dated delivery history: 29119 bytes with SHA256 3cceebbd4a4db6264b13adc04460809fc90d4f72918c10f29829e5817f5f5743. No such blob exists in the frozen audit; it remains an explicitly unsupported historical inventory pointer. The actual unchanged CURRENT_OUTPUT_PINS_WHOLE03.json is 29119 bytes with SHA256 7a4378d695e7206eb5681a8d3fcecf171ffdc2e025ba2d9cfd081aa9d91cadbb and resolves through later valid seals. Neither pointer nor seal is edited, and no missing original artifact is manufactured. The other three pointers occur in intentionally invalid old binding fixtures (zero hash or wrong byte count), whose exact fixture bytes remain unchanged. INDIVIDUAL_OMISSIONS.json records all five separately. These gaps are excluded from every successful resolution/replay claim and are not new evidence about the theorem or source priority.

The mathematical proof, constants, all nine originals, finite checker/adaptation programs, source credits, canonical TeX/PDF and every native bibliographic byte remain unchanged. The PDF is the previously compiled and five-page-viewed paper; no compilation, rendering or marker-based substitute occurred here. It is an explicitly credited corollary of prior marginal-entropy bounds, with novelty, historical priority and worldwide still-open status uncertified/UNKNOWN. Extensive AI assistance, unrefereed status, and no external human peer review or formal proof-assistant certification remain disclosed. No Git, services, external individual communication, other-worker edits, new agents or branch changes occurred in this bounded task.

## Delivery pins and next gate

paper.pdf: {pdfrec['bytes']} bytes, SHA256 {pdfrec['sha256']}.

paper.tex: {texrec['bytes']} bytes, SHA256 {texrec['sha256']}.

support.zip: {ziprec['bytes']} bytes, SHA256 {ziprec['sha256']}.

The native {{metadata, files}} manifest is byte-identical to the prior edition; its objects and asset paths are unchanged, while the external descriptor updates only ZIP hash/size. OUTPUT_PINS.json seals every local repair artifact including exact old bytes, complete report/diff, programs, process receipts and all accounting, excluding itself and the separate SEAL.json. FINAL_CURRENT_PINS.json records every current package file. Root must fully assess the repair plus disclosed historical gap, rehash artifacts, adopt or reject, and commission NEW COMPLETE whole04. This focused repair cannot clear that gate. Bounded repair completion:100%; parent research/publication goal remains incomplete.
'''
 (HERE/'REPORT.md').write_text(report)
 with (HERE/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc()+f' — 100% bounded repair implementation/validation/accounting complete. Ten exact permitted changes; six additions; all{len(unchanged)} other prior regular inputs unchanged. All165 copied records/source bytes exact; complete current allow/exclusion union. Resolved{resolved_count}/{reference_count} historical file-reference occurrences with five individually disclosed pre-existing unsupported/invalid-fixture references, not silently rebound. Full report/diff/current pins/test receipts sealed separately. ROOT repair adoption and NEW COMPLETE whole04 remain outstanding; publication flags false/PR1032 hold.\n')
 outputs=[rec(p,HERE) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name not in ['OUTPUT_PINS.json','SEAL.json']]
 write(HERE/'OUTPUT_PINS.json',{'utc':utc(),'scope':'All local bounded-repair regular outputs and exact old bytes, excluding only this self-seal and separate SEAL.json; no current or historic seal rewritten.','entries':outputs})
 # Recheck all outputs and all current package files before terminal seal.
 for r in outputs:require(match(HERE/r['path'],r),'repair output changed before seal')
 for r in load(HERE/'FINAL_CURRENT_PINS.json')['records']:require(match(PACKAGE/r['path'],r),'current byte changed before seal')
 seal={'utc':utc(),'status':'BOUNDED_CASE_ALIAS_REPAIR_COMPLETE_ROOT_ADOPTION_AND_NEW_COMPLETE_WHOLE04_REQUIRED','pr':1064,'bounded_repair_completion_percent':100,'this_is_a_complete_whole_review':False,'whole_reviews_previously_completed':3,'minimum_required':2,'latest_prior_whole_review_actionable':0,'new_P3_finding_repaired':'CASE-1064','root_repair_adoption_required':True,'new_complete_whole04_required':True,'ready_for_submission':False,'publication_ready':False,'published':False,'issues_updated':False,'ascending_publication_hold_after_pr':1032,'prior_regular_inputs':len(baseline),'authorized_existing_changes':len(changes),'unchanged_prior_regular_inputs':len(unchanged),'new_package_files':len(additions),'current_files':len(files),'archive_members':len(allow),'actual_validation_commands':len(commands),'exact_historical_reference_resolutions':resolved_count,'individual_preexisting_unresolved_reference_occurrences':len(omissions),'mathematical_source_PDF_TeX_checker_and_bibliographic_bytes_unchanged':True,'novelty':'UNKNOWN','historical_priority':'UNKNOWN','paper_pdf':pdfrec,'paper_tex':texrec,'support_zip':ziprec,'native_manifest':rec(PACKAGE/'publication/zenodo-deposit.json',PACKAGE),'output_pins':rec(HERE/'OUTPUT_PINS.json',HERE),'current_pins':rec(HERE/'FINAL_CURRENT_PINS.json',HERE),'report':rec(HERE/'REPORT.md',HERE),'complete_diff':rec(HERE/'COMPLETE_CODE_PROSE_DIFF.patch',HERE),'individual_omissions':rec(HERE/'INDIVIDUAL_OMISSIONS.json',HERE)}
 write(HERE/'SEAL.json',seal)
 print(json.dumps({'pass':True,'local_output_records':len(outputs),'prior_JSON_files':jsonfiles,'historical_reference_occurrences':reference_count,'exact_resolutions':resolved_count,'individual_omissions':len(omissions),'modified':len(changes),'current_files':len(files),'seal':rec(HERE/'SEAL.json',HERE)},indent=2))
if __name__=='__main__':main()
