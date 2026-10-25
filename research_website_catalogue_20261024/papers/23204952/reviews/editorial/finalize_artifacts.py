"""Seal the two bounded editorial handoffs after successful consistency checks."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
def readj(f):return json.loads(f.read_text())
def binding(f):
    b=f.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def savej(f,o):f.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')

CUBIC='''The full original Cartier-index theorem and cubic boundary application are retained at the exact declared external-theorem level. This editorial preparation does not reduce the result to a smooth case, an analytic core or a different conditional replacement. The original scope verdict remains scope-only, with mathematical_verdict, priority_verdict, promotion_decision and defect_decision null and its separate-family pending fields intact. Later root scientific adoption is recorded separately and verbatim; the editor does not manufacture a PASS inside that original object.

The precise criterion is for an irreducible normal projective complex klt Fano of dimension m≥1 with a positive bounded-potential weak Kähler–Einstein current smooth on its regular locus, an actual ample Cartier identity ω_X^[−1]≅L^⊗r for a positive integer r, and r>m/2+1. It concludes anticanonical slope stability on X and every irreducible normal finite quasi-étale cover, exclusion of positive-dimensional product covers, and I=±J for every parallel orthogonal complex structure on the regular locus. The equal-index product of projective spaces verifies sharpness in the general class; it is not advertised as a cubic-fourfold counterexample.

The complete application for n≥5 is public: the complex/polarized GH compactification is homeomorphic to cubic GIT, and the ordinary metric compactification is the quotient by coefficientwise conjugation. It includes the singular boundary, classifies every metric isometry as holomorphic or antiholomorphic, preserves the hyperplane Cartier bundle in the conjugate-target formulation, and identifies all forgetful fibers. The cubic Q-Gorenstein smoothing locus and closed-point interpretation are explicit. The result is not upgraded to schemes, stacks, moduli functors or nonclosed semistable representatives.

The public dependency chain includes every transverse dimension 2≤k≤n, the unrestricted algebraic upper gap, Li–Liu’s minimum over all centered valuations and density identity, Spotti–Sun’s iteration and actual Cartier root, Fujita’s classification, positive CM polarization and the established continuity transfer. Proposition 3 and Corollary 4 remain visibly conditional intermediate deductions. The general criterion does not depend on the gap. The cubic application explicitly accepts the pinned OpenAI preprint and its sole fourfold companion as principal external inputs; neither complete proof has been freshly recertified. Fujita’s required definition and statements were accessible in the official preview; its full chapter proof was not accessed. These limits remain public rather than being hidden in an internal authority object.

DGP splitting, classical Hilbert-polynomial/KV vanishing, local positive-Ricci curvature, reflexive extension and stable simplicity explain the criterion. Donaldson–Sun regularity, normal extension, SGA2 Picard Lefschetz and compact-to-Hausdorff topology explain the singular metric fibers. The cubic application is restricted to actual smoothable GH limits. No arbitrary nonsmoothable metric-completion assertion, Ricci-flat extension, cubic n=4 claim, effective GH-distance estimate, global novelty or formal-verification claim appears. Kong–Shen–Zhao–Zhao’s stronger complex comparison is clearly prior public work. Smooth stability and rigidity and the conjugation convention retain their earlier credit.

The exact edition is version 1.0, manuscript/declared publication date 6 October 2026, created 7 October 2026 UTC. The selected paper.pdf is the entire eight-page deposited reader. All 26 regular archive members were byte-compared with the extracted originals. There is no embedded PDF or nested archive, so the separate selected reader is the only distinct reader. The original slim receipt remains whole: its two entries contain name/url/bytes/sha256/zenodo_checksum, and no HTTP status or API file-object field is invented. SCHEMA_ADAPTER specifies any future read-only consumer view; no shared source helper is edited here.'''

FPS='''The full universal equality characterization is retained: n≥1, r>0, K compact, convex and full-dimensional, and ‖v‖₂≥r for every actual extreme point. The bound is C₂(K)≥[r²+(n+1)‖g_K‖₂²]/(n+2). Equality holds exactly for nondegenerate simplices with all vertices on the radius-r sphere. The public text does not substitute a polytope, smooth-body, exposed-extreme-set, regular-simplex, zero-centroid or origin-containment theorem. Strict extreme norms forbid equality. Dimension one gives [−r,r]. The weaker inequality without the centroid term separately requires centroid zero for equality.

The countable retained-shell construction and absolutely convergent nonnegative deficit are explained directly. Every selected vertex stays an actual extreme point of K. Vanishing radial excess puts all cell vertices on the sphere; vanishing centroid variance gives a common interior centroid, which excludes two cells with disjoint interiors. A separate finite route retains the same two positive-volume cells and gives ab‖u−v_i‖₂²/[(n+1)(n+2)|K|(a+b)]>0 before passing to the limit. This is explicitly body dependent and is not represented as a uniform stability modulus or an algorithm on arbitrary infinite data.

FPS already established the inequality, moment formulas, finite vertex partition and common-centroid rigidity for polytopes. Those proof ingredients and classical finite-dimensional convexity receive substantive credit. The contribution presented is the extension retaining equality for general bodies. The original journal and Oberwolfach question authenticate the historical target. No failed catalogue access, historical search count, current catalogue version, first-priority certification, global literature-absence or current worldwide-open claim is public. The current catalogue access limitation is a bibliographic/status limit, not a missing mathematical premise.

The exact edition is version 1.0.0, manuscript/declared publication date 23 September 2026, created 26 September 2026 UTC. The four-page standalone paper.pdf and complete source-and-verification.zip are the only proposed standalone page assets. All 29 regular ZIP members were byte-compared. The sole embedded four-page PDF is byte-identical to the selected standalone reader; no alternate reader or nested archive exists. The third actual deposited SHA256SUMS is 170 bytes and authenticates the two named payloads. Its ordinary original Zenodo link is in both publication.related_resources and the public supporting-materials section. It is not added as an unneeded local public asset.

This record has custom source interfaces. metadata.normalized.json and zenodo-record.raw.json remain original and separately hash-bound. No sources/record.json alias is created. The complete original receipt object, all three complete file entries, filename/url_from_actual_file_object/status/file_object and the headers, hashes, checksums and other fields are embedded unchanged where required. The separate root authority remains exact. SCHEMA_ADAPTER specifies a future authenticated read-only in-memory view and the narrow checksum-consumption option; it patches no shared consumer now. No original status or false/pending history is rewritten to simulate a fresh verdict.'''

def finalize(id):
    d=P/'papers'/id;e=d/'reviews/editorial';pub=readj(d/'publication.json');promo=readj(d/'promotion.json');root=promo['root_clearance_record']
    before=readj(e/'inputs-before.json');inputs=before['input_bindings'];val=readj(e/'editorial-validation.json')
    assert all(binding(P/n)==v for n,v in inputs.items())
    now=datetime.now(timezone.utc).isoformat()
    with (e/'RESEARCH_LOG.md').open('a') as f:
        f.write(f'- {now}: Final editorial checkpoint, 100% of this assigned preparation. Full proposed public copy read end to end. {val["positive_count"]} positive consistency invariants pass; all {val["negative_controls_rejected"]} meaningful changed-object controls reject in memory, with zero fixture copies. All {len(inputs)} frozen original bindings remain unchanged, including five private packages and their 3030 owned outputs. Complete original custom verdicts, receipt and exact later root authority preserved. No source program, rendering, browser, live/native, shared-core, site, Git, release or outreach action. Overall 203-record programme remains ongoing.\n')
    fully=[]
    def add(path,extent,purpose):
        f=Path(path) if str(path).startswith('/') else d/path
        fully.append(dict(path=str(f.relative_to(P)),**binding(f),extent=extent,purpose=purpose))
    add('sources/paper.pdf',f'Entire actual {pub["pdf_pages"]}-page selected PDF read through complete page text; source matched. Critical formula pages cross-read visually from existing immutable original renders.','Primary deposited manuscript, not an old website article or generated replacement.')
    add(pub['source_binding']['source_tex_path'],'Entire selected standalone TeX, including the full abstract, all theorems/proofs and inline bibliography.','Exact original claim and abstract authority.')
    for lane,a in root['reviews'].items():
        add(P/a['report'],'Entire COMPLETE current final report.','Editorial assimilation of the independent scientific family after root clearance.')
        add(P/a['verdict'],'Entire original custom JSON object, every field.','Preserve original full schema and pending/null/false history without normalization.')
    add(P/root['root_review'],'Entire actual root proof/synthesis.','Later scientific adoption, exact source theorem and proof-coverage limits.')
    add(P/root['root_custody_receipt'],'Entire custody receipt parsed/read; source and authority entries checked.','Independent original-preservation and exact source bindings.')
    add(P/promo['root_clearance_file'],'Entire original JSON read and exact assigned SHA-256 authenticated before configuration preparation.','Separate exact later root authority; no fresh scientific certification by editor.')
    for name in dict.fromkeys([pub['source_binding']['metadata_path'],pub['source_binding']['record_path'],'sources/receipt.json']):
        add(name,'Entire JSON read/parsed with complete original metadata and all actual files retained.','Exact author/date/version/DOI/license/file and custom-interface facts.')
    add(pub['source_binding']['frozen_scope_content_path'],'Entire held source/scope candidate or initial scope reconstruction.','Full original abstract and historical scope, without updating its held/pending status.')
    if id=='23204952':
        for name in ['publication/THEOREMS_AND_DEPENDENCIES.md','publication/boundary_index_proof_notes.md','publication/boundary_rigidity_proof_notes.md']:
            add('sources/published-source/'+name,'Entire original support body.','Exact dependencies/derivations and limits; historical opinions are support, not current authority.')
        for n in [2,6]:add(f'reviews/scope/page-{n}.png','Actual original image viewed; theorem/dependency chain or singular-isometry proof.','Resolve math typography, conjugate-target overbars and exact theorem scope.')
    else:
        add('sources/published-source/owr_4136_011_equality/audit/independent-proof.md','Entire original separate finite-approximation proof.','Retained finite witness, moment convergence and body-dependent strictness scope; not adopted merely on old verdict.')
        add('reviews/analytic/reader/page-3.png','Actual original image viewed in this editorial turn. Entire four-page images already read in the earlier independent analytic assignment.','Exact nonnegative deficit and equality typography.')
        add('sources/SHA256SUMS','Entire 170-byte deposited file, both named payloads authenticated.','Third actual published asset; ordinary original link, no unneeded local page asset.')
    # The scientific lanes/root read critical primary bodies. This preparation
    # does not falsely claim another full primary-paper or upstream proof audit.
    ledger=dict(utc=now,record_id=id,editorial_scope='Entire actual target, all three COMPLETE current reports/full verdicts, exact root proof/custody/clearance and relevant source support before writing the public proposal.',fully_read_or_exactly_parsed=fully,
        mathematical_review_status='Scientific clearance already supplied by root. This lane is editorial assimilation and consistency, not a new independent proof family.',
        primary_reading_limit=('Critical DGP/Li–Liu/Spotti–Sun/DSII/SGA2 interfaces and accessible Fujita assertions are recorded in the fully read current scientific/root reports. The editor did not recertify the complete upstream OAI main/companion, Fujita chapter, KSZZ proof or every foundational source.' if id=='23204952' else 'Actual FPS/OWR primary proof bodies were read in the earlier independent analytic assignment and by the complete current scientific lanes/root. This editorial preparation does not turn bounded later-literature readings into a global absence claim.'),
        submitted_programs_executed=False,templates='Recent approved paper-specific publication/promotion/public-sections structure inspected read-only; existing plain white Arial single-column design required. No shared renderer/checker read or bound as immutable editorial input.',
        all_zip_member_custody='Every regular member byte-compared with the unchanged extracted original; only relevant mathematical support bodies claimed as editorial reading. Historical archived site content is not a reader source.',
        proposed_copy_full_read=True,protected_private_packages=before['prior_private_packages'],protected_private_owned_output_count=3030,mutable_site_or_core_bound=False)
    savej(e/'READ_LEDGER.json',ledger)
    detail=CUBIC if id=='23204952' else FPS
    report=f'''# Editorial handoff — {id}

**Assigned preparation complete: 100%.** These are proposed source-bound public copy and paper-specific configurations after exact root scientific clearance. The new public page is not rendered, staged, browsed, published or live-verified by this lane. Root must read the full report, full PUBLIC_COPY, public-sections, configs and adapter before later staging. The overall 203-record goal is ongoing.

## Mathematical scope, source credit and limits

{detail}

## Complete proposed reader experience

The unchanged title, author Alec Kriebel and ORCID 0009-0001-9320-500X, exact edition and CC BY 4.0 appear in the header specification. The complete original abstract appears as one indexable paragraph headed **Original abstract**, followed by full explanatory paragraphs, the precise theorem, why it holds, limits, honest status/AI disclosure, the paper reader, complete supporting materials, passive substantive collaboration, citation/prepared BibTeX and credited prior work. The original abstract is bound to the actual TeX body and frozen scope field, with an explicit finite typography/math normalization; it is not a shortened record description.

The layout instruction is the existing plain white Arial single-column article, with no new framework or application UI. The proposed canonical URL is {pub['canonical_url']}. The description, scholarly type, full abstract, ORCID, citation title/date/DOI/PDF URL and CC BY schema are provided explicitly in public-sections.json. This document specifies them; it does not claim a renderer emitted them.

There is one on-page iframe for the exact complete selected {pub['pdf_pages']}-page PDF, one direct-open link, and two explicit downloads: the unchanged local selected PDF and its original Zenodo file. The complete original ZIP has local and original Zenodo links. No historical reader, third-party primary body, source cache, audit output or partial/repacked archive is a proposed public asset. No PDF is rebuilt, edited or substituted. All source bytes and original member paths remain exact.

Extensive AI use, unrefereed status, absence of external human/journal peer review and absence of formal proof-assistant certification are explicit. The author retains responsibility. Collaboration is passive and tied to actual research/writing contributions and mutual agreement; no outreach is prepared. follow_up remains null throughout, because no independently supported substantial new question cleared the requested bar. Private audit dates, counts, hashes, acquisition/control/custody narratives and reviewer stories do not enter the public prose. The mathematical external-dependency and attribution limits do.

## Configurations and authority preservation

publication.json and promotion.json were absent at the start. Only those paper-specific files and this new editorial namespace are written. promotion.status is the exact later root scientific PASS, separately attributed. The complete original root JSON, each complete custom original family verdict and full source receipt are preserved as structural objects, with exact source paths/hashes and report bindings. Original receipt and scope files are not normalized, aliased, edited or repacked. No false/pending/null history is converted into a new PASS. Native AA remains null and render/live/browser/native gates remain false.

SCHEMA_ADAPTER.json is a specification for a future authenticated read-only consumer view, plus the exact reader/download/ZIP/schema/BibTeX requirements. It is not a shared helper or renderer patch. Existing shared helpers, current/earlier private-stage packages, shared checker/renderer, actual site, native Sheet, browser, Git, releases, redirects and deployment are untouched. The mutable website/core is deliberately not frozen as an editorial authority. This matters because independent root integration may progress while these editorial originals remain fixed.

## Verification evidence and its limits

The own consistency validator passes **{val['positive_count']} positive invariants** and rejects all **{val['negative_controls_rejected']} meaningful altered-object controls**, entirely in memory with zero fixture copies. Controls remove the first/final abstract qualifications, alter a middle statement, confuse declared and created dates, rewrite custom original verdicts/root authority/receipt fields, lose a reader/download/ZIP/license/BibTeX item, add a cache asset, invent a follow-up/live PASS, and violate the paper’s substantive theorem/dependency/credit constraints. They test actual parsed copies, not booleans inferred from a filename or a synthetic default-PASS review.

All **{val['archive_regular_members_compared']} regular archive members** are byte-compared with the original extraction; selected payload sizes/SHA-256/MD5 match the original receipts and actual file metadata. Full-original-abstract normalization, whole-object equality of every verdict and receipt, exact later root adoption, all source paths/dates/versions and public-section/prose equality are checked. Finite editorial checks do not prove either mathematical theorem or all external sources. No deposited mathematical/verification/build program is run, imported, compiled or rerun.

All **{len(inputs)} frozen original bindings** remain unchanged before and after. This includes the target source/review/root authorities and all five immutable private packages: quadratic, bosonic, slit/Gaussian, surreal/cone/Brownian and the newly sealed dipole/Langlands package. Their **3030 owned outputs**, manifests and existing readiness seals are hash-protected read-only without copies. Their old original-input manifests are not followed into the now-mutable website/core. custody-before-after.json gives every complete before/after binding; inputs-before.json lists the protected scopes. No unrelated mutable website baseline is asserted.

## Complete handoff

- PUBLIC_COPY.md — full proposed public text, including the complete original abstract and prepared BibTeX.
- public-sections.json — ordered full paragraphs, metadata, reader/download links and complete materials.
- ../../publication.json and ../../promotion.json — source-bound copy and separate exact root adoption.
- SCHEMA_ADAPTER.json — future read-only source-interface and reader/schema contract.
- READ_LEDGER.json — exact actual readings, hashes, primary-proof coverage limits and prior package protection.
- editorial-validation.json — complete positive checks, changed-object controls and exact archive member custody.
- custody-before-after.json and inputs-before.json — complete frozen-original before/after bindings.
- abstract-source.tex, published-reader.txt, pdf-reading-binding.json and citation.bib — exact abstract/reader/citation inputs.
- RESEARCH_LOG.md — timestamped checkpoints with assigned completion estimates.
- SEAL.json and SEAL.sha256 — final own artifact/config bindings and explicit gate limits.

The common preparation, consistency and finalization scripts live in the new Cubic editorial folder; both handoffs bind that code explicitly. Root must read all complete outputs before making any integration decision. No further source repair or follow-up research is proposed by this editorial lane.
'''
    (e/'REPORT.md').write_text(report)
    own={}
    for f in sorted(e.rglob('*')):
        if f.is_file() and f.name not in ['SEAL.json','SEAL.sha256']:own[str(f.relative_to(d))]=binding(f)
    for name in ['publication.json','promotion.json']:own[name]=binding(d/name)
    code={}
    for name in ['prepare_configs.py','validate_editorial.py','finalize_artifacts.py']:
        f=P/'papers/23204952/reviews/editorial'/name;code[str(f.relative_to(P))]=binding(f)
    seal=dict(utc=now,record_id=id,status='EDITORIAL_PREPARATION_COMPLETE_RENDERING_PENDING',completion_percent=100,scope='New paper-specific configs and editorial proposal only; root full-handoff reading required before staging.',original_input_count=len(inputs),original_inputs_unchanged=True,original_inputs_before='reviews/editorial/inputs-before.json',before_after_custody='reviews/editorial/custody-before-after.json',owned_output_bindings=own,common_owned_editorial_code_bindings=code,excluded_self=['reviews/editorial/SEAL.json','reviews/editorial/SEAL.sha256'],positive_consistency_invariants=val['positive_count'],negative_controls_rejected=val['negative_controls_rejected'],fixture_copies=0,complete_original_objects_preserved=True,source_programs_rerun=False,rendered=False,live_verified=False,browser_verified=False,native_sheet_mutated=False,native_AA=None,shared_or_private_stage_mutations=False,git_release_deploy_or_outreach=False,overall_goal_complete=False)
    savej(e/'SEAL.json',seal);h=binding(e/'SEAL.json')['sha256'];(e/'SEAL.sha256').write_text(h+'  SEAL.json\n')
    print(id,h,len(own),'own artifact/config bindings')

if __name__=='__main__':
    for id in ['23204952','22983138']:finalize(id)
