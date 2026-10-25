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
if is_surreal:
    mathematical_scope='''The exact theorem concerns an **actual discrete initial additive ordered subgroup G of No**, with inherited addition and order. The constructed actual image **H=T[G] is contained in Oz and initial in the ambient No**. Initiality is closure under every proper ordinal-length sign-sequence prefix, not numerical convexity or merely an abstract tree copy. Set and proper-class groups in NBG with global choice, and the separate zero group, are included. Every individual support remains a set. No full Hahn completion, arbitrary abstract-group embedding theorem, multiplicative/ring isomorphism or simplicity preservation is promoted.

The public proof outline preserves the exact all-ordinal sign rotation, reflection of nonbottom right-prefix obligations, scaling of only the bottom coefficient group, and transport of the actual supports. The **already published appendix**, rather than an editorial repair, supplies additive cut adjunction, pure-term generation, legal unit-perturbation cuts, support-length exhaustion and local actual-set restrictions for proper classes. Classical normal-form, simplicity and monomial/pure-multiple/limit-series cut inputs are credited. The initial-group characterization, real/least-positive classifications, negative-ordinal minimum and general Hahn transport receive prior credit. No firstness, invention of general transport, exhaustive novelty or worldwide current-open claim is made.'''
    source_history='''The scope verdict remains exactly `SCOPE_COMPLETE_PENDING_MATHEMATICAL_REVIEW`, with `mathematical_pass=null`, `root_publication_clearance=false` and `candidate_only=true`. The frozen scope candidate and its original pending gate remain unchanged. Both complete mathematical verdict objects are retained, including their publication limitations. Later root scientific authority is expressed separately; it is not retroactively inserted into those original objects.'''
    date_detail='''The manuscript prints 17 October 2026 without a version number. Version **1.0.0 is the Zenodo metadata label**; the declared publication date is also 17 October 2026. Record creation is **18 October 2026 UTC**, exactly `2026-10-18T01:19:20.906056+00:00`. Public date labels preserve this distinction and make no priority inference.'''
    abstract_detail='''The complete original abstract is retained word-for-word with whitespace normalization only. Fresh exact comparison against the deposited TeX passes; every sentence and qualification remains. It is explicitly headed **Original abstract** in the proposed public copy and section data.'''
    coverage='''The public limits preserve bounded historical coverage, including the unread full 2001 predecessor and Ehrlich’s 2024 handbook chapter, and distinguish the cited author-version numbering from publisher-edition authentication. Those attribution limits are not converted into a new absence-of-prior-work conclusion.'''
else:
    mathematical_scope='''The full conjunction is preserved for the **one-sided cone K={(x,y,z)≥0:xy²≥z³}**: regular algebraic convex geometry; the parameter-100 logarithmically homogeneous self-concordant normal barrier **F=−25 log(z(xy²−z³))** on the complete strict interior; **D³F(a)[h,u,u]≤0 for every interior a, every h in the closed cone and every real u**; and the obstruction to **every homogeneous real defining hyperbolic polynomial of any degree in the same R³**.

The proof outline keeps fixed diagonal normalization, the full nonnegative direction decomposition, exact leading-minor/square identities, and separate t=1 and x-axis certificates. It includes zero, t=0 and h_y=0 directions without asserting strict definiteness there. Boundary divisibility and the nonreal quadratic factor are explained for every prospective interior hyperbolicity direction. Negative curvature is explicitly the mixed third-derivative convention, not sectional curvature. No signed-cone, all-exponent, higher-dimensional lift/projection, all-regular-cone, universal new method or practical-algorithm assertion is promoted.

The known cone is credited to Hildebrand’s family 5. Roy–Xiao’s parameter-3 barrier on this same cone is explicit prior credit; **100 is an existence certificate, not a parameter improvement**. The original 2017 existential question is separated from the broader every-regular-cone question. No exhaustive novelty, firstness or worldwide current-open claim is made.'''
    source_history='''The original scope verdict retains `mathematical_verdict=null`, `publication_gate=HELD_PENDING_SEPARATE_FULL_MATHEMATICAL_GATE` and `page_promotion_permission=false`. The frozen candidate retains its held status and null mathematical verdict. The analytic original remains `status=COMPLETE`, `mathematical_verdict=SUPPORTED_AT_LITERAL_SCOPE` and `publication_clearance=false`; the adversarial original remains `status=COMPLETE`, its complete textual verdict and `promotion_clearance=false`. No conventional `status=PASS` was manufactured inside either custom original object. The later root scientific PASS is separate.'''
    date_detail='''The manuscript and Zenodo metadata both identify **version 1.0.0, 17 October 2026**. Record creation is the same UTC date, exactly `2026-10-17T17:44:20.489806+00:00`. The public edition note states the dates without treating them as evidence of priority.'''
    abstract_detail='''The complete original one-paragraph abstract is preserved. The exact deposited TeX abstract is bound privately, and a fresh explicit typography-normalization comparison matches the public abstract in full: only mathematical display notation, accents, apostrophes and whitespace change. Every sentence and qualification remains, explicitly headed **Original abstract**.'''
    coverage='''Bounded historical coverage remains explicit. The full 2026 Hildebrand article and related prepublication remain literature limits; no exhaustive predecessor or broader-method exclusion is inferred. These are scholarly scope limits, not a public narrative of internal review operations.'''
report=f'''# Complete editorial preparation report: Zenodo {ID}

Completed {now}. Editor as assigned: GPT-6.1 Sol, Ultra; no children. Completion estimate: **100% of the assigned bounded editorial preparation**. This measures the local editorial assignment, not probability of mathematical truth, overall catalogue completion or verified website publication.

## Disposition and authority

Prepared the previously absent `papers/{ID}/publication.json` and `promotion.json`, plus new artifacts only in this paper’s `reviews/editorial/`. The exact later root scientific clearance is `{pro['root_clearance_file']}`, SHA-256 `{pro['root_clearance_sha256']}`. Its full object is embedded unchanged, as are every original review verdict and the complete original source receipt/file entries. This assignment accepts that independently completed scientific authority and supplies source-bound editorial copy; it is **not a new independent mathematical review**.

The state remains **BINDINGS_READY_RENDERING_PENDING**. `rendered_copy_verified`, `live_verified` and `browser_verified` are false; native Sheet AA URL is null. A top-level promotion PASS means only the separately bound later root scientific disposition. No render/live/browser/native publication PASS is assigned here.

## Full reading and exact public scope

Read project AGENTS.md; both complete exact root clearances for the assigned papers; all three complete current final reports and every full original verdict for this record; the entire deposited TeX; the full actual deposited PDF text; the entire scope candidate; metadata/receipt; root prose/custody receipt; and the complete recent Gaussian/slit public-copy and schema-adapter templates. Fresh `pdftotext -layout` extraction of the deposited PDF is retained as `published-reader.txt` and matches the frozen reader text byte-for-byte. PDF page count and searchable text were checked. No visual rendering or browser inspection occurred in this assignment. No newly independent primary-source reading or mathematical-program replay is claimed. READ_LEDGER.json records exact extents and identities.

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

The unchanged {pub['pdf_pages']}-page PDF is specified for on-page embedding, direct opening and explicit local downloading, with its Zenodo original link. The complete original ZIP is specified for local download and original Zenodo access. The archive’s sole embedded reader equals the standalone PDF byte-for-byte; there is one distinct reader and no nested archive. No third-party primary-source cache or additional reader is a public asset. Sources are not regenerated, trimmed or repacked.

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

No frozen input, shared script, site, Sheet, Git branch/commit/push, release/DOI, deployment, UI or external-communication action was taken. No children were spawned; no source repair or claim weakening was attempted. The overall 203-paper catalogue effort remains ongoing outside this bounded assignment.
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
