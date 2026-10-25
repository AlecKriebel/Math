#!/usr/bin/env python3
"""Write this bounded editorial handoff and hash seal once, without staging."""
from pathlib import Path
import datetime
import hashlib
import json

PAPER=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
ROOT=PAPER.parents[1]
ID=PAPER.name
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj):
    with p.open('x') as f:f.write(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
pub=load(PAPER/'publication.json')
pro=load(PAPER/'promotion.json')
validation=load(OUT/'editorial-validation-20261025-01.json')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
is_surreal=ID=='23444606'
mathematical_scope='The full Theorem 1 and both kernel/discovery lemmas are preserved for every finite integer k≥1, distinct fixed LABELED seeds on R/Z, continuing independent standard Brownian motions with generator (1/2)d²/dx², and REAL NONNEGATIVE transform variables. The coefficient construction uses finite permutation and label sums and ordinary deterministic integrals of explicit interval-exit kernels. Owner inequalities compare CUMULATIVE PHYSICAL clocks, retaining the correlations among one walker’s query visits. No unknown hitting law or owner probability is left as an unevaluated probabilistic definition inside the coefficient construction.\n\nThe complete JOINT measure follows from all homogeneous moment polynomials, all mixed moments, and compact-simplex uniqueness. The exact uniform-in-distinct-seeds degree-N OUTER remainder is theta_max^(N+1)/(N+1)! for every N≥0, without an extra exponential factor. Equally spaced starts are fixed-seed specializations; IID uniform LABELED starts use coefficient-wise seed averaging. Sorted seed labels require their own ordered law; equally spaced labels have cyclic/dihedral symmetry while IID labels are fully permutation exchangeable.\n\nThe short public proof preserves singleton endpoint-flux addition, continuing traversal of earlier queries, whole-walker independence and within-walker correlation. Measurability/Fubini gives ties of zero spatial measure almost surely, not absence of ties simultaneously everywhere. Null query/seed/collision diagonals do not become a deterministic coincident-seed extension. The public limits exclude compact/named densities, efficient evaluators, inner Fourier-tail or quadrature certificates, large-k claims, unequal-per-particle diffusivity invariance and a claimed discrete-to-Brownian limit proof. Classical painting, heat kernels, strong Markov iteration, moment expansion and determinacy receive explicit credit.'
source_history='The complete original scope verdict retains task_status=COMPLETE, scope_verdict=LITERAL_FULL_TARGET_MODEL_AND_CREDIT_SCOPE_COMPLETE, mathematical_verdict=null, mathematical_clearance=false, publication_clearance=false, page_promotion_permission=false and its held candidate status. The frozen content candidate retains all original pending/null/false fields. The analytic original retains status=COMPLETE, mathematical_verdict=SUPPORTED_AT_LITERAL_SCOPE, exact_remaining_mathematical_gap_at_literal_scope=null and publication_clearance=false; the adversarial original retains status=COMPLETE, its complete textual verdict, exact_remaining_mathematical_gap_found=null and publication_clearance=false. No conventional status=PASS was inserted into an original reviewer object. Later root scientific PASS is separate.'
date_detail='The manuscript prints **7 October 2026** without a version number. **Version 1.0** is recorded in Zenodo and support metadata, and the declared publication date is also 7 October 2026. Record creation is exactly `2026-10-07T21:53:43.146386+00:00`; the later `2026-10-10T21:22:19.823663+00:00` metadata update is not used to invent another manuscript edition. Public date labels preserve these distinctions without a priority inference.'
abstract_detail='The complete original single-paragraph abstract is retained with all words, sentences and qualifications. Fresh comparison against the deposited TeX passes under whitespace joining and one straight-to-curly apostrophe normalization only. The proposed public copy and section data explicitly use **Original abstract**; it is neither shortened nor silently rewritten.'
coverage='Historical priority, full novelty, independent discovery and current worldwide openness remain unverified. The incomplete Gomes/Dicker coverage is a bounded attribution limit. The authenticated historical 2010 author-book custody versus current URL timeout is retained in the original private scientific authorities, not retold as a public audit timeline. This editorial assignment neither reacquires the book nor makes a fresh primary-body retrieval claim.'
report=f'''# Complete editorial preparation report: Zenodo {ID}

Completed {now}. Editor as assigned: GPT-6.1 Sol, Ultra; no children. Completion estimate: **100% of the assigned bounded editorial preparation**. This measures the local editorial assignment, not probability of mathematical truth, overall catalogue completion or verified website publication.

## Disposition and authority

Prepared the previously absent `papers/{ID}/publication.json` and `promotion.json`, plus new artifacts only in this paper’s `reviews/editorial/`. The exact later root scientific clearance is `{pro['root_clearance_file']}`, SHA-256 `{pro['root_clearance_sha256']}`. Its full object is embedded unchanged, as are every original review verdict and the complete original source receipt/file entries. This assignment accepts that independently completed scientific authority and supplies source-bound editorial copy; it is **not a new independent mathematical review**.

The state remains **BINDINGS_READY_RENDERING_PENDING**. `rendered_copy_verified`, `live_verified` and `browser_verified` are false; native Sheet AA URL is null. A top-level promotion PASS means only the separately bound later root scientific disposition. No render/live/browser/native publication PASS is assigned here.

## Full reading and exact public scope

Read project AGENTS.md; the complete exact root clearance for this paper; all three complete current final reports and every full original verdict for this record; the entire deposited TeX; the full actual deposited PDF text; the entire scope candidate; metadata/receipt; root prose/custody receipt; and the complete recent Gaussian/slit public-copy and schema-adapter templates. Fresh `pdftotext -layout` extraction of the deposited PDF is retained as `published-reader.txt` and matches the frozen reader text byte-for-byte. PDF page count and searchable text were checked. No visual rendering or browser inspection occurred in this assignment. No newly independent primary-source reading or mathematical-program replay is claimed. READ_LEDGER.json records exact extents and identities.

{mathematical_scope}

## Abstract, dates and preserved original history

{abstract_detail}

{date_detail}

{source_history}

{coverage}

## Complete public copy and scholarly metadata

PUBLIC_COPY.md is the full proposed public article; public-sections.json supplies the same complete paragraphs, links, citation, BibTeX and local-PDF iframe specification for staging. Both include accessible explanation, exact result, concise mathematical mechanism, limitations, extensive-AI and unrefereed disclosure, no human/journal review or formal proof-assistant certification claim, author responsibility, and passive substantive collaboration wording. Authorship and responsibilities depend on actual research/writing contributions and mutual agreement. Follow-up remains null.

The draft carries exact title, author and ORCID, edition date/version, description, final canonical, DOI, license, citation and BibTeX. Private hashes, review timestamps, report/receipt paths, replay counts and internal control stories are excluded from public prose. No individual outreach was prepared or initiated.

Final proposed canonical: {pub['canonical_url']}

The unchanged {pub['pdf_pages']}-page PDF is specified for on-page embedding, direct opening and explicit local downloading, with its Zenodo original link. The complete original ZIP is specified for local download and original Zenodo access. The complete support ZIP has no embedded PDF and no nested archive; the standalone six-page PDF is the only reader. No third-party primary-source cache or additional reader is a public asset. Sources are not regenerated, trimmed or repacked.

## Fresh editorial validation and custody

`editorial-validation-20261025-01.json` records **{validation['checks_passed']} successful editorial assertions**. These are identity, schema, wording and custody assertions, not independent mathematical claims or evidence that finite tests prove the universal theorems. Fresh checks preserve all **{validation['frozen_files_preserved']}** frozen input files, compare all **{validation['archive_members_compared']}** original ZIP members to their extracted bytes, and rehash all **{validation['family_seal_bindings_rehashed']}** final family-seal bindings listed by root. Every source, source candidate, existing review, verdict, receipt, seal and exact root clearance remains unchanged. Config/canonical/metadata and original-abstract identity checks pass, as do full original custom-object equality, all proposed section/paragraph/reference/link mappings, explicit download/iframe specifications, disclosures, passive authorship wording and canonical uniqueness against existing publication configs.

PDF SHA-256: `{pro['pdf_sha256']}`.

Complete ZIP SHA-256: `{pro['supplement_sha256']}`.

Publication config SHA-256: `{sha(PAPER/'publication.json')}`.

Promotion config SHA-256: `{sha(PAPER/'promotion.json')}`.

The validator writes only an explicitly supplied unused stem in this editorial directory. It executes no deposited source helper, build or mathematical program and makes no network call. The after-custody receipt records every frozen binding, archive member and final family-seal binding.

## Bounded adapter and handoff requirements

SCHEMA_ADAPTER.json describes staging requirements without editing a shared script. The current renderer’s hardcoded Abstract heading must become **Original abstract** for the actual page, and its full original text must remain intact. Carry through the explicit local PDF download attribute, direct-open link, same-file iframe, full ZIP/local-original links, all public sections and citation/BibTeX. Preserve complete custom verdict objects and consult separate root authority rather than normalize original pending/custom statuses into a fabricated PASS.

Use the established **plain white, Arial, single-column personal-blog layout**, ordinary links and simple headings. No framework or extra visual asset is proposed. Actual staging must carry full indexable prose, metadata/canonical/ScholarlyArticle and citation tags, research navigation/index/ItemList and sitemap.

**Root must read this entire report, the full PUBLIC_COPY, public-sections, both configs, adapter and seal before authorizing staging.** Actual rendered-copy/source-asset comparison, local HTTP/link/open/download tests, live HTTP/byte tests, desktop/mobile browser inspection and native Sheet AA publication remain root gates. AA stays blank until verified live. These specifications do not claim completion of those gates.

No frozen input, shared script, site, Sheet, Git branch/commit/push, release/DOI, deployment, UI or external-communication action was taken. The previously completed surreal/cone editorial configs, copies and seals were not modified. No children were spawned; no source repair or claim weakening was attempted. The overall 203-paper catalogue effort remains ongoing outside this bounded assignment.
'''
with (OUT/'REPORT.md').open('x') as f:f.write(report)
with (OUT/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — Final complete public copy read and editorial consistency/custody checks passed; full report, adapter and handoff complete. Completion estimate: **100% of assigned bounded editorial preparation**. Actual rendered/live/browser/native publication remains pending under root authority. No scientific repair, frozen-source/shared-file mutation or external publication action.\n')
files=sorted(p for p in OUT.rglob('*') if p.is_file() and p.name not in ['SEAL.json','SEAL.sha256'])+[PAPER/'publication.json',PAPER/'promotion.json']
seal={
    'record_id':ID,'sealed_utc':now,'status':'COMPLETE_EDITORIAL_BINDINGS_RENDERING_PENDING',
    'completion_percent':100,'root_clearance_file':pro['root_clearance_file'],'root_clearance_sha256':pro['root_clearance_sha256'],
    'files':[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files],
    'frozen_input_baseline':'frozen-inputs-before.json','frozen_inputs_unchanged':True,
    'validation':'editorial-validation-20261025-01.json','validation_sha256':sha(OUT/'editorial-validation-20261025-01.json'),
    'original_review_objects_and_receipt_preserved':True,'full_original_abstract_preserved':True,
    'no_source_programs_executed':True,'new_mathematical_review_claimed':False,
    'website_rendered':False,'live_verified':False,'browser_verified':False,'native_sheet_aa_url':None,
    'parent_must_read_full_handoff_before_staging':True,'children_spawned':False
}
write(OUT/'SEAL.json',seal)
with (OUT/'SEAL.sha256').open('x') as f:f.write(sha(OUT/'SEAL.json')+'  SEAL.json\n')
print(json.dumps({'record_id':ID,'report':str(OUT/'REPORT.md'),'seal_sha256':sha(OUT/'SEAL.json'),'publication_sha256':sha(PAPER/'publication.json'),'promotion_sha256':sha(PAPER/'promotion.json')}))
