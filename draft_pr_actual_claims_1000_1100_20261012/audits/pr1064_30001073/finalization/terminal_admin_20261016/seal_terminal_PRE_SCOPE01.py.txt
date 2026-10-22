#!/usr/bin/env python3
"""Final custody/selection/stage ledgers and cycle-free local terminal seal."""
from pathlib import Path
import collections, datetime, difflib, hashlib, json, stat
HERE=Path(__file__).resolve().parent;AUDIT=HERE.parent.parent;PACKAGE=AUDIT/'preprint_v1_0'
MUTABLE={'preprint_v1_0/'+n for n in ['README.md','verify_package.py','COPY_MAP.json','SAFE_INPUT_PINS.json','EXCLUSION_LEDGER.json','SUPPORT_ALLOWLIST.json','SUPPORT_MANIFEST.json','support.zip','publication/DEPOSIT_BINDING.json']}
def need(c,m):
 if not c:raise RuntimeError(m)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def write(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def rec(p,root):
 b=p.read_bytes();return {'path':p.relative_to(root).as_posix(),'bytes':len(b),'sha256':sha(b)}
def match(p,r):return p.is_file() and not p.is_symlink() and p.stat().st_size==r['bytes'] and sha(p.read_bytes())==r['sha256']
def pkgfiles():return sorted(p for p in PACKAGE.rglob('*') if p.is_file() and not p.is_relative_to(PACKAGE/'tmp'))

def main():
 need(not (HERE/'SEAL.json').exists(),'terminal stage already sealed')
 repro=load(HERE/'REPRODUCTION_RECEIPTS.json');need(repro['pass'] and repro['all_processes_settled'],'validation incomplete')
 initial=load(HERE/'INPUT_PINS.json')['records'];before=load(HERE/'BEFORE_PINS.json')['entries'];byname={r['path']:r for r in initial};beforemap={r['path']:r for r in before}
 # Every pre-existing regular byte and mode is either unchanged or preserved
 # exactly in the initial-before directory; no pre-existing path is deleted.
 protected=[];changed=[];retained=[];byhash=collections.defaultdict(list)
 for r in initial:
  p=AUDIT/r['path'];need(p.exists(),'preexisting path removed '+r['path'])
  if r['path'] in MUTABLE:
   saved=HERE/beforemap[r['path']]['preserved_path'];need(match(saved,r),'before bytes differ '+r['path']);need(stat.S_IMODE(saved.stat().st_mode)==r['mode'],'before mode differs')
   need(not match(p,r),'allowed mutable file unexpectedly unchanged '+r['path'])
   changed.append({'path':r['path'],'before':{k:r[k] for k in ['bytes','sha256','mode']},'preserved_path':str(saved.relative_to(AUDIT)),'after':rec(p,AUDIT)})
   actual=saved
  else:
   need(match(p,r),'protected bytes changed '+r['path']);need(stat.S_IMODE(p.stat().st_mode)==r['mode'],'protected mode changed '+r['path']);protected.append(r);actual=p
  retained.append({'original_path':r['path'],'bytes':r['bytes'],'sha256':r['sha256'],'retained_path':actual.relative_to(AUDIT).as_posix(),'mode_preserved':True});byhash[(r['bytes'],r['sha256'])].append(actual)
 need(len(changed)==9 and len(protected)==1105,'initial partition changed')
 write(HERE/'PROTECTED_BYTE_RECEIPT.json',{'utc':utc(),'scope':'All1114 preexisting regular audit files. Only the nine explicitly allowed package administrative/build records differ; each exact initial byte/mode is preserved under local before/. Every other1105 file retains its bytes/mode at its original path. No omitted source/cache/old-scratch exception.','initial_count':len(initial),'unchanged_count':len(protected),'preserved_before_count':len(changed),'unchanged_records':protected,'changed_records':changed,'retained_initial_artifacts':retained})
 # Resolve each original package stage and selected review/repair output pin by
 # exact bytes, never by blindly substituting its current logical path.
 stages=['preprint_v1_0/OUTPUT_PINS.json','preprint_v1_0/CURRENT_OUTPUT_PINS.json','preprint_v1_0/CURRENT_OUTPUT_PINS_WHOLE03.json','preprint_v1_0/TERMINAL_OUTPUT_PINS.json','preprint_v1_0/CASE_ALIAS_OUTPUT_PINS.json','repairs/case_alias01/OUTPUT_PINS.json','reviews/package_04/OUTPUT_PINS.json']
 resolved=[]
 for name in stages:
  p=AUDIT/name;entries=load(p)['entries'];rows=[]
  for r in entries:
   candidates=byhash[(r['bytes'],r['sha256'])];need(bool(candidates),'sealed old stage artifact absent '+name+' '+r['path']);actual=candidates[0];need(match(actual,r),'resolved stage bytes')
   rows.append({'original_record':r,'retained_exact_path':actual.relative_to(AUDIT).as_posix(),'status':'EXACT_RETAINED_BYTES_NOT_ORIGINAL_STAGE_EXECUTION'})
  resolved.append({'manifest':rec(p,AUDIT),'stage_entries':len(entries),'records':rows})
 write(HERE/'PRIOR_STAGE_RECEIPTS.json',{'utc':utc(),'scope':'Individual exact retained-byte resolution of the seven explicitly named stage/output inventories. This does not execute historical programs, authenticate every historical pointer, resolve the known stale inventory digest or create an all-history certificate.','stages':resolved,'entries_resolved':sum(s['stage_entries'] for s in resolved)})
 historical=load(AUDIT/'reviews/package_04/HISTORICAL_CUSTODY_RECHECK.json');exceptions=historical['unsupported_occurrences'];need(len(exceptions)==5,'known exceptions count')
 pinned=[]
 for e in exceptions:
  p=AUDIT/e['manifest'];need(match(p,byname[e['manifest']]),'historical exception source changed')
  need(not byhash[(e['bytes'],e['sha256'])],'known unsupported digest unexpectedly manufactured')
  pinned.append({'exception':e,'unchanged_manifest':rec(p,AUDIT)})
 actual=PACKAGE/'CURRENT_OUTPUT_PINS_WHOLE03.json';need(actual.stat().st_size==29119 and sha(actual.read_bytes())=='7a4378d695e7206eb5681a8d3fcecf171ffdc2e025ba2d9cfd081aa9d91cadbb','actual immutable whole03 seal changed')
 write(HERE/'HISTORICAL_EXCEPTIONS_PRESERVED.json',{'scope':'Carry forward exactly the five individually unsupported occurrences from ROOT-adopted whole04. No pointer rewrite, fabricated old blob, all-pointer authentication or original-stage replay. The full whole04 recheck is dated evidence, not a new universal-history audit.','whole04_recheck':rec(AUDIT/'reviews/package_04/HISTORICAL_CUSTODY_RECHECK.json',AUDIT),'historical_reference_occurrences':14818,'whole04_exact_retained_reference_occurrences':14813,'unsupported_occurrences':pinned,'actual_immutable_whole03_seal':rec(actual,AUDIT),'later_sealed_actual_bytes_resolve':True,'historical_missing_digest_recreated':False})
 # Every old copy remains byte-exact, in the same order and with the same fields.
 old=load(HERE/'before/preprint_v1_0/COPY_MAP.json')['copies'];copies=load(PACKAGE/'COPY_MAP.json')['copies'];need(len(old)==165 and len(copies)==176 and copies[:165]==old,'copy prefix changed')
 need(load(PACKAGE/'SAFE_INPUT_PINS.json')['records']==copies,'safe pins differ')
 for c in copies:
  need(match(AUDIT/c['source_path'],c) and match(PACKAGE/c['package_path'],c),'source/delivery copy differs '+c['source_path'])
 oldallow=load(HERE/'before/preprint_v1_0/SUPPORT_ALLOWLIST.json')['members'];allow=load(PACKAGE/'SUPPORT_ALLOWLIST.json')['members'];need(set(oldallow).issubset(allow) and len(oldallow)==198 and len(allow)==212,'member boundary changed')
 exclusions=load(PACKAGE/'EXCLUSION_LEDGER.json');oldex=load(HERE/'before/preprint_v1_0/EXCLUSION_LEDGER.json')
 need(exclusions['local_package_files'][:12]==oldex['local_package_files'] and exclusions['source_exclusion_groups'][:-1]==oldex['source_exclusion_groups'],'old exclusion partitions changed')
 ledger=load(PACKAGE/'TERMINAL_SELECTION_LEDGER_20261016.json');included=[r for r in ledger['records'] if r['included']];need(len(ledger['records'])==27 and len(included)==11,'evidence selection count')
 need([{k:r[k] for k in ['source_path','package_path','bytes','sha256']} for r in included]==copies[165:],'selection/copy append differs')
 write(HERE/'COPY_AND_BOUNDARY_RECEIPTS.json',{'scope':'All176 source/destination copies rehashed; exact first 165 row values/order retained, eleven selected authored additions. The old198-member boundary is a strict subset of current212; old 12 exclusions and all old source-exclusion groups remain exact prefixes. Older historical selection ledgers themselves are protected unchanged.','copies':copies,'old_prefix_rows':165,'new_rows':11,'selection_records':27,'selected_records':11,'old_members':198,'new_members':212,'added_members':sorted(set(allow)-set(oldallow)),'old_local_exclusion_prefix_unchanged':True,'old_source_exclusion_groups_prefix_unchanged':True})
 status='TERMINAL_STATUS_20261016.json';need((AUDIT/status).read_bytes()==(PACKAGE/status).read_bytes(),'outer/package status differs')
 # Current stage seal is excluded from the distributed archive, avoiding cycles.
 newseal=PACKAGE/'TERMINAL_OUTPUT_PINS_20261016.json';need(not newseal.exists(),'dated stage seal already exists')
 current_pre=[rec(p,PACKAGE) for p in pkgfiles()];need(len(current_pre)==224,'pre-seal package count')
 write(newseal,{'schema_version':1,'snapshot_date':'2026-10-16','scope':'Every current non-tmp package file before this separately excluded dated seal. Includes the current ZIP/binding/native manifest and all unchanged earlier seals; excludes only self to avoid a cycle. This is local administrative stage custody, not ROOT external final integrity or readiness promotion.','entries':current_pre,'count':len(current_pre),'publication_ready':False,'published':False,'issues_resolved':False,'root_external_final_integrity_required':True,'services_held_after_pr':1032})
 current=[rec(p,PACKAGE) for p in pkgfiles()];need(len(current)==225,'post-seal count')
 paths={r['path'] for r in current};need(paths==set(allow)|set(exclusions['local_package_files']),'exact current member/exclusion partition')
 write(HERE/'FINAL_CURRENT_PINS.json',{'utc':utc(),'scope':'All225 current package files; exactly212 distributed plus13 explicitly local excluded files. Temporary output is ignored separately. ROOT NEW external final integrity remains required.','records':current,'count':len(current),'distributed_count':len(allow),'local_excluded_count':len(exclusions['local_package_files'])})
 # Complete actual operative text delta, including exact additions. Binary ZIP
 # is identified by before/after pins rather than an unreadable binary patch.
 allnow=[p for p in AUDIT.rglob('*') if p.is_file() and not p.is_relative_to(HERE)];new=[p for p in allnow if p.relative_to(AUDIT).as_posix() not in byname]
 expectednew={PACKAGE/r['package_path'] for r in included}|{PACKAGE/n for n in [status,'TERMINAL_ACCEPTANCE_20261016.md','TERMINAL_SELECTION_LEDGER_20261016.json','TERMINAL_OUTPUT_PINS_20261016.json']}|{AUDIT/status}
 need(set(new)==expectednew,'unexpected new non-finalization file')
 patches=[];diffindex=[]
 for name in sorted(MUTABLE|{p.relative_to(AUDIT).as_posix() for p in new}):
  p=AUDIT/name;oldbytes=(HERE/beforemap[name]['preserved_path']).read_bytes() if name in beforemap else b'';newbytes=p.read_bytes()
  try:a=oldbytes.decode('utf8');b=newbytes.decode('utf8')
  except UnicodeError:
   patches.append('Binary delta '+name+'; exact before/after identities are in CHANGE_INVENTORY.json and BEFORE_PINS.json.\n');continue
  patches.extend(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile=('before/'+name if name in beforemap else '/dev/null'),tofile=name))
  diffindex.append(name)
 (HERE/'COMPLETE_CODE_PROSE_DIFF.patch').write_text(''.join(patches))
 # A short operative-only view accompanies the complete text delta.
 operative=[]
 for name in ['preprint_v1_0/README.md','preprint_v1_0/verify_package.py']:
  a=(HERE/beforemap[name]['preserved_path']).read_text();b=(AUDIT/name).read_text();operative.extend(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='before/'+name,tofile=name))
 for name in ['preprint_v1_0/TERMINAL_ACCEPTANCE_20261016.md','preprint_v1_0/TERMINAL_STATUS_20261016.json']:
  operative.extend(difflib.unified_diff([], (AUDIT/name).read_text().splitlines(True),fromfile='/dev/null',tofile=name))
 (HERE/'OPERATIVE_CODE_PROSE_DIFF.patch').write_text(''.join(operative))
 write(HERE/'CHANGE_INVENTORY.json',{'utc':utc(),'scope':'Exact actual delta outside this new finalization. Nine administrative/build mutations, sixteen additions, zero removals. Paper/PDF/math/bibliography/native manifest/path guards and all old history/status/seal bytes are protected.','modified_files':changed,'added_files':[rec(p,AUDIT) for p in sorted(new)],'removed_files':[],'complete_text_diff_files':diffindex,'new_finalization_authored_code_files':['terminal_admin.py','validate_terminal.py','seal_terminal.py'],'binary_delta_paths':['preprint_v1_0/support.zip'],'all_initial_artifacts_retained':True})
 external=load(HERE/'EXTERNAL_INPUT_PINS.json')['entries']
 for r in external:need(match(Path(r['path']),r),'external local checker changed')
 # Inventory ignored own scratch without deleting any retained failure evidence.
 scratch=[rec(p,HERE) for p in sorted((HERE/'tmp').rglob('*')) if p.is_file() and not p.is_symlink()]
 write(HERE/'SCRATCH_INVENTORY.json',{'scope':'Own ignored retained validation scratch only; all actual failures/negative controls and compiler-preflight fixtures remain available. No preexisting file/source/runtime/cache was removed. Links are listed separately; no scratch bytes are part of scholarly delivery.','records':scratch,'symlinks':[{'path':p.relative_to(HERE).as_posix(),'target':str(p.readlink())} for p in sorted((HERE/'tmp').rglob('*')) if p.is_symlink()],'regular_count':len(scratch),'regular_bytes':sum(r['bytes'] for r in scratch)})
 controls=load(HERE/'SEMANTIC_AND_GUARD_CONTROLS.json');ziprec=rec(PACKAGE/'support.zip',PACKAGE);pdfrec=rec(PACKAGE/'paper.pdf',PACKAGE)
 report=f'''# PR1064 bounded terminal administration, 16 October 2026

The authorized administrative reconciliation is complete. Four complete whole-package reviews have finished (minimum two); latest whole04 is ZERO actionable P0–P3 and ROOT-adopted. No further complete whole review is currently required. ROOT must still read and independently reproduce/adopt this terminal administration and create NEW external final integrity. No readiness promotion is made. ready_for_submission, publication_ready, published, issues_updated and issues_resolved remain false; the ascending service hold stays after PR1032. An actionable new finding requires bounded repair and NEW complete whole05. This work is administrative, not a fifth whole review or a new mathematical/source result.

## Frozen boundary and exact change

All 1,114 preexisting regular audit files (130,310,771 bytes), excluding only this new finalization folder, were frozen before candidate changes. There were no symlinks. The initial boundary includes every old source/cache/runtime/scratch/old archive file; no hidden local exemption was applied. Exact before copies preserve all nine mutable file identities and modes, including the old 620,042-byte ZIP SHA256 2fb6bfa2ef9b1f0c3173527cd136fe175d1d5a93a1bc5ffadb66ee2951a9077f. No old pointer or stage seal was overwritten. At final custody all 1,105 other preexisting files retain original bytes and modes, and all nine exact initial mutable artifacts remain in before/. All old FINAL_SEAL/FINAL_INTEGRITY/status/report bytes remain unchanged.

The nine mutations are README, verify_package, COPY_MAP, SAFE_INPUT_PINS, EXCLUSION_LEDGER, SUPPORT_ALLOWLIST, SUPPORT_MANIFEST, support.zip and external DEPOSIT_BINDING. Separate dated outer/kit status, acceptance, selection ledger, an excluded local package-stage seal and eleven exact selected whole04/ROOT evidence copies are added. Sixteen new non-finalization files and zero removals result. The first 165 COPY_MAP rows retain their complete values and order; all 176 source/copy pairs were rehashed. Earlier 198-member boundary and old 12-file exclusion prefix persist; current 225 files partition exactly into 212 distributed members and 13 local exclusions. Every prior history/selection partition is preserved.

The only operative program change adds explicit semantic checks for the new dated terminal status and its copied whole04 verdict/ROOT adoption. Old status checks remain checks of their dated historical states. Archive/PDF builders, run_checks, fresh_guard_checker and original checker are unchanged. The complete actual text delta, including every added text artifact and stage seal, is COMPLETE_CODE_PROSE_DIFF.patch; OPERATIVE_CODE_PROSE_DIFF.patch is a shorter review view. Exact before/after pins identify the binary ZIP delta. All three new local authoring/validation/sealing programs are retained here in full.

## Actual reproduction and controls

All {repro['actual_top_level_subprocess_commands']} final-pass top-level subprocess commands settled with expected outcomes: {repro['successes']} successes and {repro['expected_nonzero_rejections']} expected nonzero rejections. EXECUTIONS.jsonl preserves actual argv/cwd/return/stdout/stderr. An earlier harness attempt stopped after 247 expected process results when its case-alias fixture construction divided two strings. This was a local TypeError before the builder was invoked for that control, not a package finding. FAILED_ATTEMPT01.json, exact invalid code, EXECUTIONS_ATTEMPT01.jsonl and the complete first scratch tree preserve the incident. The corrected harness ran a fresh complete validation; none of the incomplete first attempt is counted as final-pass coverage. Both normal and optimized modes ran the four standard-library README commands from one clean extraction and the canonical strict required-binding verifier. Both clean archive rebuilds equal the complete canonical bytes. Independent raw ZIP parsing checks every local/central header, deflate payload, CRC, size, timestamp, mode and offset; exact EOCD forbids prefix/gaps/extras/comments/trailer. Independent level9 reconstruction is byte-identical in the recorded Python/zlib environment; cross-environment compressor-byte identity is qualified.

Full mathematical JSON objects were compared, not only counts. The original checker executes normal -I -B with active assertions, and its complete object equals ROOT baseline after only completed_utc/python/platform projection. The explicit-raise guard checker's complete objects agree normal/-O and with both frozen baselines after that same declared projection; all seven actual faults fail in both modes in each supplied runner. Whole04's independent rigorous controls produce the exact 22,938-byte full JSON SHA256 3a78eac75ceb08583a0ae09927d944b296039aae15e17b1cddf8df708fe8e523 in both modes, matching both frozen whole04 outputs. Endpoint, deleted zero-marginal mass and deleted sequential KL faults fail in both modes. The analytic proof remains universal; supplied Fraction/Decimal diagnostics are finite non-interval corroboration, while whole04's 241 rational interval pairs, formal prime-log identities and 1000 exact matrices are finite rigorous controls.

Every {controls['protected_inputs']} protected extraction file was exercised through an actual hardlink in both modes ({controls['all_protected_hardlinks_rejected_both_modes']} rejections), including all 13 local exclusion paths. The future dated stage-seal path used an explicitly labelled test sentinel before actual sealing. Direct/file-symlink/directory-symlink/case aliases for six key files are rejected before a writer sentinel opens. Physical case-root containment rejects fresh leaves and absent nested descendants before creating any output/directory, in both actual case-spelling directions. Ordinary designated ZIP regeneration, tmp/case-tmp and external output succeed byte-identically. These claims concern a static filesystem.

All {len(controls['semantic_controls'])} coherent status/copied-evidence semantic controls fail in normal/-O after manifest and, as applicable, copy-map/safe-pin rehashing, preventing a masking hash rejection. Same-byte allowlist/manifest symlinks fail bootstrap safety checks. Actual required binding passes; required absence, missing fields, wrong size/hash/schema and extra fields fail. PDF canonical/direct/directory/case/child-hardlink/child-symlink preflight controls fail before compilation; no compiler or render is run. All protected sentinels remain unchanged.

The native repository uploader's actual LOCAL check succeeds and selects the exact current PDF/ZIP sizes and SHA256. Its check branch was read and returns before state/token/client creation. No service mode was run. Bare metadata and all three metadata wrappers remain identical bibliographic objects; native paths remain ../paper.pdf and ../support.zip. The uploader manifest's own bytes are protected unchanged. The external binding is excluded from ZIP to avoid a cycle and binds both deliverables.

## Historical custody and limits

PRIOR_STAGE_RECEIPTS individually resolves {sum(s['stage_entries'] for s in resolved)} rows across the seven explicitly named stage/output inventories by exact retained bytes. Historical programs are not rerun or claimed to execute against this new edition. This limited inventory resolution is not a claim that every historical pointer resolves.

Exactly five known historical reference occurrences remain unsupported and explicitly excluded from successful resolution claims. Two unchanged local/copied package02 CHANGE_INVENTORY.added_package_files[0] rows name a 29,119-byte SHA256 3cceebbd4a4db6264b13adc04460809fc90d4f72918c10f29829e5817f5f5743 artifact for which no exact blob is retained. The actual immutable CURRENT_OUTPUT_PINS_WHOLE03.json has the same byte count and SHA256 7a4378d695e7206eb5681a8d3fcecf171ffdc2e025ba2d9cfd081aa9d91cadbb; later valid seals bind those actual bytes. Three deliberately invalid binding fixtures are the other unsupported occurrences. All five source manifests remain byte-exact. No missing bytes were manufactured and no pointer was rewritten. The complete whole04 historical recheck remains dated 14,818-reference/14,813-exact evidence and is copied verbatim; this administration does not invent a broader all-history audit.

The paper is unchanged: {pdfrec['bytes']} bytes, SHA256 {pdfrec['sha256']}. No PDF recompilation or rerender is needed for unchanged bytes; whole04 records actual successful compilation and individual views of all five pages. Source formulas, mathematical distinctions, credited-corollary framing, UNKNOWN novelty/priority, author/ORCID/license, extensive AI assistance, unrefereed status and lack of external human peer review/formal certification remain intact. No exhaustive literature, deep general-girth proof, novelty or worldwide-open certificate is claimed.

## Delivery and handoff

Current ZIP: {ziprec['bytes']} bytes, 212 members, SHA256 {ziprec['sha256']}. FINAL_CURRENT_PINS covers 225 current package files; dated local TERMINAL_OUTPUT_PINS_20261016 covers the 224 pre-self-seal files. This local finalization OUTPUT_PINS plus SEAL is separate and cycle-free. Old FINAL seals remain dated history. All actual scratch is retained ignored with individual hash inventory, including process/negative-control evidence; no preexisting source/cache/old scratch was removed. No ENOSPC failure occurred in this new bounded stage. Prior failure evidence is unchanged.

No Git/index/branch, network/service/upload/DOI/release, PR/issue/tracker/queue, other-shard operation or outreach occurred. No other subagent was spawned. Only the human user may communicate externally. ROOT's independent final read/reproduction/adoption and NEW external final integrity remain required. Bounded terminal-administration completion 100%; this percentage does not estimate historical novelty discovery or publication readiness.
'''
 (HERE/'REPORT.md').write_text(report)
 with (HERE/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc()+' — 100% of bounded terminal administration: complete protected/before/current/copy/stage ledgers, historical exception preservation, full operative/code/prose diffs and report settled. All initial files retained exactly or in saved before copies; no mathematical change or readiness promotion. ROOT independent adoption and NEW external final integrity remain required. Output inventory/seal are the final writes.\n')
 # Recheck every package and initial record after all report/ledger writes.
 for r in current:need(match(PACKAGE/r['path'],r),'current changed while sealing '+r['path'])
 for r in retained:need(match(AUDIT/r['retained_path'],r),'initial retained artifact changed while sealing')
 outputs=[rec(p,HERE) for p in sorted(HERE.rglob('*')) if p.is_file() and not p.is_relative_to(HERE/'tmp') and p.name not in {'OUTPUT_PINS.json','SEAL.json'}]
 write(HERE/'OUTPUT_PINS.json',{'utc':utc(),'scope':'Every retained non-tmp file in this new terminal finalization, including exact before files and complete local code/diffs/reports/receipts. Excludes only this inventory and separate seal; ignored scratch is individually inventoried separately and retained.','entries':outputs,'count':len(outputs)})
 write(HERE/'SEAL.json',{'utc':utc(),'stage':'BOUNDED_TERMINAL_ADMIN_COMPLETE_PENDING_ROOT_EXTERNAL_FINAL_INTEGRITY','output_inventory':rec(HERE/'OUTPUT_PINS.json',HERE),'outputs':len(outputs),'input_inventory':rec(HERE/'INPUT_PINS.json',HERE),'before_inventory':rec(HERE/'BEFORE_PINS.json',HERE),'current_package_inventory':rec(HERE/'FINAL_CURRENT_PINS.json',HERE),'dated_package_stage_seal':rec(newseal,AUDIT),'outer_status':rec(AUDIT/status,AUDIT),'paper_pdf':pdfrec,'support_archive':ziprec,'whole_package_reviews_completed':4,'minimum_whole_reviews':2,'latest04_ZERO_ROOT_adopted':True,'new_complete_whole_review_currently_required':False,'root_external_final_integrity_required':True,'publication_ready':False,'published':False,'issues_resolved':False,'services_held_after_pr':1032,'all_processes_settled':True,'initial_inputs':len(initial),'initial_unchanged':len(protected),'exact_before_retained':len(changed),'all_old_FINAL_seals_statuses_reports_unchanged':True,'bounded_admin_completion_percent':100})
 print(json.dumps({'sealed':True,'outputs':len(outputs),'current_package_files':len(current),'members':len(allow),'zip':ziprec,'ROOT_external_final_integrity_required':True},indent=2))

if __name__=='__main__':main()
