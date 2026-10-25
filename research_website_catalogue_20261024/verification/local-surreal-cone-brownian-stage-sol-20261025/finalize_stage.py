"""Recheck all frozen inputs and seal only this owned private package."""
from pathlib import Path
import datetime,hashlib,json
O=Path(__file__).resolve().parent;R=O.parents[1];IDS=['23444606','23440119','23224103']
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
 p=O/name;assert not p.exists(),p;p.write_text(obj if isinstance(obj,str) else json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
before=json.loads((O/'inputs-before.json').read_text())['bindings'];old=json.loads((O/'old-comparison-inputs-before.json').read_text())['bindings']
assert all(before[k]==v for k,v in old.items() if k in before)
inputs=dict(before,**old);after={path:{'bytes':Path(path).stat().st_size,'sha256':sha(Path(path))} for path in inputs}
assert inputs==after
save('integrity-after.json',{'utc':now(),'status':'PASS','original_bindings':len(inputs),'initial_lean_baseline':len(before),'old_renderer_read_bindings':len(old),'all_originals_unchanged':True,'bindings':after})
edits=json.loads((O/'reversible-proposal-edits.json').read_text())
for kind,name in [('renderer','render_page'),('checker','final-content-check')]:
 proposed=(O/(name+'.proposed.py')).read_text()
 for original,replacement,count in reversed(edits[kind]):assert proposed.count(replacement)==count;proposed=proposed.replace(replacement,original)
 assert proposed==(O/'inputs'/(name+'.py')).read_text()
save('entire-existing-scripts-preservation.json',{'utc':now(),'status':'PASS','exact_reversal_recovers_entire_installed_renderer':True,'exact_reversal_recovers_entire_installed_checker':True,'all_old_quadratic_bosonic_amplifier_slit_gaussian_and_other_branches_preserved':True})
bindings={};ledger=[]
for rid in IDS:
 p=R/'papers'/rid;c=json.loads((p/'publication.json').read_text());g=json.loads((p/'promotion.json').read_text())
 bindings[rid]={'publication':{'path':str(p/'publication.json'),'sha256':sha(p/'publication.json')},'promotion':{'path':str(p/'promotion.json'),'sha256':sha(p/'promotion.json')},'complete_original_source_binding':c['source_binding'],'complete_original_custom_reviews':g['reviews'],'separate_later_root_scientific_authority':{'path':g['root_clearance_file'],'sha256':g['root_clearance_sha256'],'scope_gate_resolution':g['scope_gate_resolution']},'separate_root_editorial_authority':{'path':f'verification/root-editorial-{rid}-20261025.json','sha256':sha(R/f'verification/root-editorial-{rid}-20261025.json')},'actual_public_copy':{'path':f'public-copy-{rid}.txt','sha256':sha(O/f'public-copy-{rid}.txt')},'actual_complete_ordered_sections':{'path':f'public-sections-{rid}.json','sha256':sha(O/f'public-sections-{rid}.json')}}
 for rel in ['publication.json','promotion.json','reviews/editorial/REPORT.md','reviews/editorial/PUBLIC_COPY.md','reviews/editorial/public-sections.json','reviews/editorial/SCHEMA_ADAPTER.json','reviews/editorial/SEAL.json']:
  path=p/rel;ledger.append({'path':str(path),'sha256':sha(path),'scope':'Entire editorial content and complete parsed JSON/config objects; repeated embedded source authorities compared exactly to their separate originals.'})
 for kind in ['editorial','clearance']:
  path=R/f'verification/root-{kind}-{rid}-20261025.json';ledger.append({'path':str(path),'sha256':sha(path),'scope':'Entire exact separate root authority, as also embedded in the full source-bound promotion record.'})
 for name in [f'public-copy-{rid}.txt',f'public-sections-{rid}.json']:
  ledger.append({'path':str(O/name),'sha256':sha(O/name),'scope':'Entire actual staged body read; every ordered paragraph/reference/list item/heading compared to approved source data.'})
save('source-bindings.json',{'utc':now(),'records':bindings,'original_objects_unchanged':True,'source_aliases_receipt_rewrites_or_config_edits':False})
save('READ_LEDGER.json',{'utc':now(),'model':'GPT-6.1 Sol Ultra','children':0,'entries':ledger,'limits':'Source-bound editorial/static stage work, not a new independent scientific proof assessment. No actual-site render, live HTTP/browser/native publication or novel-priority clearance.'})
validation=json.loads((O/'stage-validation.json').read_text());validation['completion_percent']=100;validation['scope']='Bounded private staging only; overall203-paper goal ongoing.';save('completion.json',validation)
with (O/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — 100% of bounded private stage: 204/204 content checks,40 altered-read rejections,all51 old configured renderer outputs/dispatches unchanged, and all'+str(len(inputs))+' frozen input bindings unchanged. Complete actual copies read. Production/root publication gates remain separate.\n')
report=f'''# Private surreal, cone and Brownian staging

Status: **PRIVATE_STAGE_CHECKS_PASS_PENDING_ROOT_ACCEPTANCE_AND_PUBLICATION_GATES**.
Completion: **100% of this bounded private staging assignment**. The overall203-paper catalogue program remains ongoing. Model: GPT-6.1 Sol Ultra; no descendants.

All writes are confined to `verification/local-surreal-cone-brownian-stage-sol-20261025/`. Production and the prior slit/Gaussian package were not changed. No source, config, original review/verdict/receipt/seal, shared script, actual site, Git, deployment, redirect, browser, native Sheet or release mutation occurred. No person was contacted or messaged and no outreach was prepared. No deposited mathematical program, installer, environment, compiler or authored source entry point was rerun; no download or dependency installation was needed.

## Complete reviewable package

The three real private pages and their unchanged PDF/complete-ZIP assets are under:

- `public/research/initial-omnific-models-discrete-surreal-groups/` (23444606).
- `public/research/negative-curvature-normal-barrier-nonhyperbolicity-cone/` (23440119).
- `public/research/brownian-first-visit-cell-lengths-circle-joint-laplace-transform/` (23224103).

`public-copy-{{ID}}.txt` contains each complete actual visible body, read in full. `public-sections-{{ID}}.json` gives all11 actual ordered headings, every paragraph, complete list-item text and every link/download flag. All abstract/plain/result/proof/limits/status paragraphs and all background references/notes match the approved public-sections specifications exactly. The approved reader introductions and substantive collaboration text also appear unchanged.

`render_page.proposed.py` and `final-content-check.proposed.py` are the full final production sources. `proposed-shared-renderer.diff` and `proposed-shared-checker.diff` are exact unified patches against the current installed scripts named in the dispatch. `render_page.stage.py` and `final-content-check.stage.py` are explicit private execution copies; `renderer-staging-overrides.diff` and `checker-staging-overrides.diff` show only their original read-only ROOT/import/private-SITE changes. No private-stage path or fallback appears in the production proposals or production diffs. No helper or asset-resolver change is proposed.

The target report/stdout/stderr, compact altered-read cases/reports, full old-renderer comparison and source-dispatch comparison, index/sitemap checks, source/reading bindings and custody records are included. `stage-readiness-manifest.json` binds all original inputs and all owned output files except itself to avoid circularity. Its SHA-256 is the package seal.

## Bounded renderer and checker changes

The renderer extends the existing narrow original-abstract/download/material allowlists by exactly these three IDs and adds their approved short PDF-reader introductions. Every full original abstract is displayed under **Original abstract**. Each new page has two explicit local PDF download anchors, ordinary direct-open links, one same-file iframe, the unchanged original Zenodo PDF link and the complete local-download/original-Zenodo ZIP links. New3 alone receive their specified CC BY4.0 header link/ScholarlyArticle license and the exact sealed prepared editorial `citation.bib`, including edition/source date and unrefereed/AI notes. The established simple white personal-blog layout and common header/byline/navigation remain.

The checker adds only the exact three source TeX mappings, a narrow abstract normalizer and a bounded three-record branch. Surreal abstract normalization joins whitespace only. Brownian joins whitespace and normalizes its single named apostrophe. Cone normalizes only the explicitly listed TeX mathematical typography, accents/apostrophes and whitespace. Unknown commands fail closed.

Checks bind exact publication/promotion bytes, separate science and editorial root authorities and full editorial seals, complete original custom review objects/reports/paths plus separate later dispositions, full raw receipt/file objects, readable metadata and API asset identity, original raw-record schema where applicable, MD5/SHA-256/size, exact source TeX/full abstract/frozen candidate, date/version/manuscript-edition distinctions, source-custody receipts, all archive members/readers, citation/license/index/sitemap, full actual section prose and the main scientific boundaries. No conventional PASS is inserted into an original custom verdict and no receipt, source alias or config is rewritten.

For new3 only, citation-author spelling is checked against their prepared BibTeX's `Kriebel, Alec`. The new3 background-link comparison decodes ordinary HTML entities so the surreal primary URL's exact ampersand survives correctly escaped href markup. The initial failed report is retained as `target-stage-check-initial.*`; it exposed a checker comparison issue, with no source or copy correction. Every other original branch is preserved.

## Scientific copy and original history

Surreal preserves actual initial additive G with inherited addition/order, actual image H=T[G] contained in Oz and initial in **ambient No**, all proper ordinal-length prefixes, sets/proper classes in NBG/global choice, set-sized individual supports and zero. The sign rotation, nonbottom right-prefix obligations, bottom-only dyadic normalization, actual-support transport and already published appendix remain. No numerical-convexity, abstract tree-copy, arbitrary-group, multiplicative/simplicity-preserving or full-Hahn-completion conclusion replaces that claim. Prior characterization/transport/classification credit and unverified priority limits remain. The manuscript's17October2026 date without a version is distinct from Zenodo metadata version1.0.0 and18October record creation. The original pending/null scope and both complete original mathematical verdicts remain unchanged.

Cone preserves the one-sided nonnegative K, entire strict-interior barrier F=−25log(z(xy²−z³)), parameter **100**, exact dual gradient norm100, every interior base/every closed-cone direction/every real test vector, degeneracies and every-degree defining-polynomial obstruction in the same R³. Exact t=1/x-axis certificates and t=0/h=0/h_y=0 cases remain. Mixed third-derivative sign is distinguished from sectional curvature. Hildebrand's known cone and Roy–Xiao's **parameter3** barrier receive explicit prior credit:100 is an existence certificate with no parameter improvement or optimality claim. No signed/all-exponent/all-cone/lift/projection or practical-algorithm extension is introduced. Version1.0.0/date17October2026 and same-day creation remain exact. Original COMPLETE/custom verdicts and scope null/held/prohibition fields remain complete.

Brownian preserves every finite k≥1, fixed distinct labeled seeds on R/Z, independent continuing standard Brownian motions with generator1/2, real nonnegative transforms, finite deterministic coefficient integrals, cumulative physical clocks retaining within-walker correlations, all mixed moments/full joint compact-simplex measure, IID labeled versus sorted/equally spaced seed laws, and the exact uniform **outer** factorial remainder theta_max^(N+1)/(N+1)! for every N≥0. It preserves singleton flux addition, continuing traversal and spatially-null a.s. ties. It claims no inner Fourier-tail/quadrature certificate, deterministic coincident-seed extension, independent query clocks, unequal-per-particle diffusivity invariance, density/efficiency/large-k or discrete-limit result. Classical methods and bounded historical coverage remain credited.7October2026 manuscript/publication date, metadata version1.0 and later metadata update remain distinct. Original COMPLETE/custom verdicts and held/null/false scope fields remain unchanged.

Every paper retains extensive AI use, unrefereed/no human or journal peer review/no formal proof-assistant certification, named-author responsibility, passive collaboration with actual contributions and mutual agreement, bounded historical-priority/novelty language and null follow-up. No private audit count/hash/date/custody/control narrative appears on the public pages. The common site shell adds its standard navigation/contact links, citation display-name order and one stock authorship paragraph; full prepared BibTeX is available through its download link rather than repeated as visible code.

## Verification and preservation

The final target passed **204/204** content checks with empty stderr: **68/68 for each paper**. The unchanged PDFs remain searchable at7,5 and6 pages. Every one of the145 surreal,26 cone and52 Brownian ZIP members matches its original extracted bytes. The sole surreal/cone embedded PDFs each equal their respective standalone reader; Brownian's complete52-member ZIP has no embedded PDF. None has a nested archive and no extra reader/cache is public.

The private index has **55** unique entries: every old52 visible list item is byte-identical and every old52 structured entry is exact and in order. Only the new surreal,cone,Brownian URLs are appended, in that order. The sitemap has **56** unique URLs including its root: all old53 URLs remain exact and ordered, followed by only those three. CSS and robots are byte-identical.

All **51** old TEX_PATHS and abstract dispatches were compared on their actual published TeX and are unchanged; the pilot manual page remains unmapped. Exact reversal of the recorded edits recovers the entire installed renderer and checker byte-for-byte, preserving all quadratic/bosonic/amplifier/slit/Gaussian and other branches.

All **51 configured old pages** were actually executed under both complete current and proposed renderers. Output writes were captured as exact bytes in memory, including copied assets, HTML, BibTeX and existing shared metadata; pypdf read the captured output PDF bytes. Every output digest/size agrees. `memory_render.py` records zero filesystem output writes and original read bindings. This is an executable before/after comparison, not a prediction from source inspection. The manual pilot has no publication config and remains unchanged in the actual452-file baseline. No actual-site render occurred.

**40 meaningful controls were rejected** by complete checker executions on the one pristine private stage. They test first/middle/final abstract truncation for all3, wrong citation DOI, corrupted PDF/ZIP bytes, exact source-TeX changes, science-root byte changes, added deep custom-verdict fields, receipt sizes, surreal actual-H/class-support changes, cone100-versus3/prior-improvement changes, Brownian independent-query-clock/inner-remainder changes, canonical/index/sitemap omission and replacing the Brownian manuscript date by its later metadata-update date. Controls override only changed bytes returned by Path reads; exact changes are retained in `controls/cases.json`. They create **zero fixture-stage copies**, modify no original inputs, and retain compact report or fail-closed exception evidence. They do not rerun any authored source mathematics.

## Custody and remaining gates

All **{len(inputs)}** original bindings rehash unchanged:878 lean initial bindings including all **452 actual site files**, all relevant new3 sources/configs/editorial/scientific/root authorities and current52 integration core, plus350 original read bindings used by the old renderer/dispatch comparisons, with overlaps deduplicated. No unrelated runtime inventory, full research program, environment or old asset tree was copied. Before sealing, the package was about4.4MiB; the final manifest adds a small metadata overhead.

Root must read this complete report, the complete final production proposals/diffs and all three complete actual public copies before authorizing physical integration. The separate current52 browser/native process and actual new3 production integration/rendered-copy acceptance, local/live HTTP and asset-byte verification, desktop/mobile browser inspection, deployment/index freshness and native Sheet AA gates remain root-owned. Native AA stays blank until verified live. **No production render, HTTP/live/browser/mobile/deployment/native-publication/Git/release PASS is claimed by this private stage.**
'''
save('REPORT.md',report)
outputs={str(p.relative_to(O)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(O.rglob('*')) if p.is_file() and p.name!='stage-readiness-manifest.json'}
save('stage-readiness-manifest.json',{'utc':now(),'status':'PRIVATE_STAGE_COMPLETE_PENDING_ROOT_AND_PUBLICATION_GATES','completion_percent':100,'scope':'Bounded private three-paper staging only; overall203-paper goal ongoing.','original_input_bindings':inputs,'all_original_inputs_unchanged':True,'owned_output_bindings':outputs,'excluded_self':'stage-readiness-manifest.json','proposal_sha256':{name:sha(O/name) for name in ['render_page.proposed.py','final-content-check.proposed.py']},'production_live_browser_native_pass':False})
print(json.dumps({'status':'PRIVATE_STAGE_COMPLETE','completion_percent':100,'original_bindings_unchanged':len(inputs),'owned_outputs':len(outputs),'manifest_sha256':sha(O/'stage-readiness-manifest.json')}))
