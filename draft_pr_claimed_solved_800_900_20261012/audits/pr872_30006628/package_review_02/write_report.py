#!/usr/bin/env python3
"""Assemble this review's authored report and decision from fixed observed receipts."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
HERE=Path(__file__).resolve().parent
seal=json.loads((HERE.parent/'PACKAGE_SEAL_R1.json').read_text())
auth=json.loads((HERE/'UPDATED_AUTHENTICATION.json').read_text())
math=json.loads((HERE/'INDEPENDENT_MATH_CHECKS_NORMAL.json').read_text())
now=datetime.now(timezone.utc).isoformat()
pins='\n'.join('| `'+r['path']+'` | '+str(r['bytes'])+' | `'+r['sha256']+'` |' for r in seal['core_files'])
body='''# Independent adversarial final-package review 02 — PR872 / problem30006628

**Decision: CLEAR on the exact R1 candidate identified below. No blocking mathematical, source-scope, priority-wording, layout, preservation, or verification-engine defect was found. No candidate repair is requested.** This is a completed AI adversarial review, not external human peer review, formal verification, an exhaustive novelty certificate, or authorization to publish. The parent must read this entire report and perform its remaining publication workflow separately.

## Independence, object, and trust

I first read the current complete `note.tex` and the original complete `PROOF.md`, and wrote `INDEPENDENT_RECONSTRUCTION.md` before any earlier family verdict or package verdict. I then checked the argument independently against actual primary text and complete relevant dependency pages, authored a new finite construction and a new tiny-fixture attack suite, and only then compared prior family evidence. Earlier decisions were not mathematical premises. This review did not read the earlier package-review verdict as an acceptance basis. No new central proof-search attempt was made; the original effort counter remains **1/5**.

All writes are confined to this `package_review_02/` directory. The candidate, canonical preprint, originals, PDF, and archive were not modified. I stayed on main, made no Git/PR/release/Zenodo/spreadsheet writes, and contacted no person or other chat. Internal progress went only to the assigning parent.

The candidate is `work/pr872_revision_r1` below the effort folder, with exactly172 regular files. External identification pins, independently checked before any candidate-code execution:

- `PACKAGE_SEAL_R1.json`: SHA256 `9eafa209f3bb74f1ba81fd8eef52087e0d16ea4b05ae8624a1c2a4e36ec5ef22`.
- Current outer manifest: SHA256 `02d511d2c24414615006dd1e97e134061c65888955f534c25d1c12e4edc4d8be`.
- Current outer startup verifier: SHA256 `57b78a4813329b5964f94879b3fbff796d2e0d1e1298f3889b804117ec06d8fe`.
- Portable index: SHA256 `09b94f08b7b30f4657bd0ed18f6c2ef86c58aec4ab1813badd12078c9cf36444`.
- Frozen15-file source manifest: SHA256 `4589f9b70e9a65ae67356544b5ad59644290902bb9b3df80406710a22559e3f8`.

These are separately supplied identification anchors, not hashes learned only from code already executing. The independent authentication program imports no candidate program. It checks the entire outer manifest, all11 core/canonical copies, all143 portable ZIP members, all15 originals against actual Git objects at frozen head `e3d77731b45b5f463df46e769faa01d65fe193ec`, all13 preserved root copies, metadata equality, the exact two-file deposit, and the8 external receipt hashes named in the seal. Thus an adjacent self-hash is not being used to bootstrap trust.

## Exact target and primary-source scope

The theorem fixes n>=3 arbitrary nontrivial finitely generated factors, finite nonempty inverse-closed generating alphabets of actual nonidentity factor elements, and density1/3<d<1. It draws floor(|S_l|^d) independent uniform ROOTED cyclically reduced syllable words with replacement. The limit is through ALL integer lengths. Fixed nonidentity word balls of integer radius>=1 are included. The argument makes no finite-length guarantee, no assertion at d=1/3 or for two factors, and no uniform claim as factors/alphabets/radius/density vary.

I read actual OWR Problem16 pp535–536, its shorthand model on p523, and RQFP arXiv2502.08630v2 Definition1.1, Theorem1.2, Remark1.3 and Question1.9 with surrounding text. These support the target identification, with the important restriction that Question1.9 is literally broader than OWR by allowing two factors. The odd-length universe is empty for two factors, so an unqualified all-length two-factor assertion would be false. The paper does not make it. The already known collapse for n>=3 and d>1/2 is credited; the substantive extension includes every1/3<d<=1/2.

The normal-word universe in OWR p523 and the cyclic universe in RQFP are not silently equated. The final section proves a separate density-slack thinning transfer, audited below. Nothing relies on actual factor word-problem algorithms, factor embeddings, or preservation of a uniform law when ball elements are replaced by arbitrary free representatives.

`PRIMARY_READING_RECEIPTS.json` pins the exact reused local primary PDF/text bytes and records each scope. No fresh web search was needed for this bounded final review. Consequently I do not independently refresh a worldwide current-openness or exhaustive-priority claim. No identity between unread final journal bodies and the read KK/Tropp arXiv versions is asserted, and the original Zuk Proposition6 body was not newly read.

## Analytical reconstruction and attacks

### 1. Perron sign, torsion deletion, and endpoint errors

For the complete multipartite letter matrix A, the quadratic form is the square of the total coordinate sum minus the sum of squares of part sums. On the codimension-one zero-total subspace it is nonpositive. A therefore has at most one positive eigenvalue. Connectivity and a triangle make A primitive, so Perron lambda is simple, lambda>=2, every other eigenvalue has strictly smaller modulus, and all those eigenvalues are nonpositive. The resulting reversible letter walk P has spectrum1 and a remainder in[-rho,0], rho<1. Mere mixing without this sign would not prove the unequal-cut conclusion.

Rooted cyclic counts are trace(A^l). There is no division by rotations or inversions. Reduced free-product normal forms distinguish every syllable string, despite arbitrary relations inside each factor. Inversion preserves each factor, hence the Perron coordinate within that factor.

An even-length reduced block cannot equal its inverse because its middle boundary would join the same factor. An odd inverse-fixed block of length2s+1 is determined by s initial syllables and one self-inverse central letter; its total count is O(lambda^s). This absolute bound applies to every endpoint class and every completion count. With finitely many positive Perron coordinates and fixed A, it gives uniform exponentially small relative errors in both v_t(a,b) and T_h(p,q), including same-factor endpoint pairs. It implies eventual nonemptiness, not nonemptiness at every small length. The symmetry of T follows by inversion/reversal together with factor-invariance of inversion. No torsion-free assumption is needed.

### 2. Formal triangularization, fixed positions, and exact degrees

The inverse-free blocks split into honest two-element inverse pairs. A formal generator may later map to an element satisfying other relations; no injective map into the target quotient is required. Adjacent formal inverse blocks would violate the original syllable boundary, including the wrap-around boundary. Thus the formal triangles are cyclically reduced and their links have no loops.

For an ordered link corner x,y, prescribe adjacent blocks x^{-1},y at that particular corner's original positions. Its joining condition is A[first(x),first(y)]. The remaining block has exact length l-t-u, lies in its inverse-free set, and closes both remaining boundaries; its number is T_(l-t-u)(last(x),last(y)). Reversing the orientation gives the same count by the symmetry just established. Summing the three positions and both orientations gives C0=[6], C1=[[2,2],[2,0]], C2=[[0,2],[2,2]]. This reasoning does not rotate an unequal block pattern and pretend the cutting law was preserved. The normalization is N/Z for original samples, with rejected samples contributing zero, rather than a conditional retained-sample normalization.

Multiplying destination endpoint multiplicity lambda^(u-1) r_c r_f by the completion term lambda^(l-t-u+1) r_b r_f cancels the destination-length dependence. Summing endpoints supplies sum_f r_f^2=1 and sum_c A_ac r_c=lambda r_a. The expected degree is exactly asymptotic to (N/Z)lambda^(l-t+1)r_a r_b h_t. This checks the delicate exponent and rules out an extra uncancelled lambda for the longer type. Consequently the expected minimum degree is bounded below by a positive fixed constant times lambda^(d*l-ceil(l/3)), while the number of vertices is O(lambda^ceil(l/3)). Floors do not change these bounds. At every fixed d>1/3 the degree is exponentially large compared with log(vertex count).

### 3. Exact compression and the negative-times-negative spectrum

The full mean walk maps functions to functions constant on type/first/last endpoint classes. Its nonzero spectrum is therefore that of the exact finite compressed matrix; all additional full-space eigenvalues are zero. Reversibility has class masses proportional to class size times common expected degree. Their limiting normalized values are (h_t/6)r_a^2 r_b^2, with type masses2/3 and1/3 in the appropriate order, not uniform type masses.

The compressed matrix tends to Q tensor P tensor R, R_bf=r_f^2. The last coordinate resets and R has spectrum1,0. Both unequal type walks have spectrum1,-1/2. Multiplying -1/2 by a negative P-eigenvalue produces a POSITIVE nonprincipal eigenvalue. Its maximum is rho/2<1/2. The paper explicitly includes that product; discarding it would be a central error. The equal-length case has nonprincipal upper limit0, with full-space zeros included. The principal limit eigenvalue1 is simple.

Fixed-dimensional reversible spectral continuity gives an eventual mean normalized-Laplacian gap at least gamma=1/2+(1-rho)/4 and eventual mean connectivity. The spare margin is positive for each fixed alphabet. Taking the maximum of the three residue thresholds yields an all-integer assertion. Inverse-fixed deletion parity is already absorbed by the exponential error.

The extreme-imbalance test is analytical, not an extrapolation of finite cases: for sizes(M,1,1), lambda=(1+sqrt(1+8M))/2 and rho=(sqrt(1+8M)-1)/(sqrt(1+8M)+1). The true unequal-limit gap above1/2 is1/(sqrt(1+8M)+1), tending to zero. This refutes a universal-gap shortcut and agrees with the paper's fixed-parameter exclusions. The recorded numerical examples through M=10^12 only illustrate that exact formula.

### 4. Whole-relator concentration and actual normalization

For each original sample, the three edge Laplacians form ONE PSD summand, or zero if rejected. Summands are independent across samples, even when the three edges within one sample coincide. Each edge norm is2, so the whole-sample norm<=6. A signed vertex receives at most one incidence from each block occurrence because no block is its own inverse, giving degree contribution<=3, not an edge-independence claim.

After conjugation by expected degrees, every summand kills the same deterministic vector z=barD^(1/2)1. Restriction to z-perpendicular preserves independence and PSD order and has deterministic expectation minimum>=gamma. I read Tropp1004.4389v7 Corollary5.2 and Remark5.3 on the full page images20–21, resolving the PSD glyph rather than trusting its faulty text extraction. With R=6/delta the lower-tail exponent is epsilon^2*gamma*delta/12. Using a smaller gamma than the actual expectation minimum weakens both threshold and bound legitimately. The scalar upper-tail exponent epsilon^2*delta/9 follows from degree bound3 and the displayed elementary logarithmic inequality. The union bound over vertices requires no independence of their degrees. Both tails vanish by exponential delta growth.

The Laplacian lower bound on the expected-degree centered codimension-one subspace first forces the actual kernel to be constants. This proves connectivity and positive actual degrees before using D^{-1/2}. Generalized max-min can then use that codimension-one subspace; it is not required to equal the actual-degree orthogonal complement. Equivalently, shifting any function by its barD-weighted mean gives energy >=(1-epsilon)gamma times Var_barD; since D<=(1+epsilon)barD, Var_D<=(1+epsilon)Var_barD. This yields the same actual gap lower bound (1-epsilon)gamma/(1+epsilon)>1/2 for the paper's chosen epsilon interval. There is no unsupported orthogonality substitution.

### 5. Index and property-(T) transfer

For any alphabet letters a,b choose a third factor C. When L is even a reduced common suffix beginning in C suffices. When L is odd>=5, the suffix C,D,E,C followed by pairs D,C has the required even length and begins/ends in C. Thus av and b^{-1}v are reduced length-L blocks and cannot be inverse-fixed, including with involutions. Their product (av)(b^{-1}v)^{-1}=ab lies in the block subgroup.

The subgroup K generated by all ab is normal: c(ab)c^{-1}=(ca)(bc^{-1}), with inverse-closedness essential. In F/K all alphabet letters have the same image and its square is1, hence index<=2. Containment in the V_L subgroup and then passage to the actual sampled quotient preserve the index bound. This is valid for L>=4 and all residues, with arbitrary factor relations and no finite-presentation assumption on the factors.

I read KK1106.2242v2 Definition2.12/Theorem2.13 and Remarks2.10–2.11, including the entire criterion page7. Its multigraph convention permits parallel edges, excludes loops through cyclic reduction, and assumes connectivity and gap>1/2. Global inversion of all signed vertices identifies the paper's link convention with that source. Repeated triangular cells leave the group unchanged and supply their actual corner multiplicities, consistent with the source's independent-relator convention. The criterion requires neither independent link edges nor a torsion-free quotient. The auxiliary triangular group therefore has(T), surjects onto its actual block-image subgroup, and finite-index permanence transfers(T) to the full quotient. The implication directions are correct.

### 6. Literal linear-law thinning and all boundaries

For U_l=1^T A^(l-1)1, the cyclic proportion Z_l/U_l tends to lambda/(sum r)^2>0. Among floor(U_l^d) IID linear draws, cyclic acceptance indicators are IID Bernoulli and the retained labels, conditional on any count, are IID uniform cyclic labels. Independence from the count can be formulated by extending the accepted-label sequence with auxiliary labels after the finite draw sequence; only its prescribed initial segment is used on the high-count event. Fix1/3<d'<d: exponential slack puts at least floor(Z_l^d') accepted draws in that event with probability tending to one. The full linear presentation is a further quotient. Thus the transfer does not condition a high-probability assertion on an exponentially rare whole-presentation event, and does not equate the laws.

The proof covers involutions, nontrivial inverse pairs, repeated blocks/relators, rejected samples, every residue, d in(1/3,1/2] as well as known higher densities, and arbitrary fixed imbalance. It deliberately excludes small-length certainty, n=2, d=1/3 and growing-parameter uniformity. No excluded boundary has been silently promoted to a conclusion.

## Fresh finite falsification construction

`independent_math_checks.py` imports none of the inherited diagnostics. It uses the valid radius-one alphabets of (C2 x C2)*C2*C2 with part sizes(2,1,1), all letters involutions. It directly enumerates reduced syllable strings, checks cyclic closure, cuts at fixed positions, removes inverse-fixed blocks, and accumulates every ordered corner. A separately computed completion expression is compared entrywise, and exact endpoint-row compression and degrees are checked.

At lengths9,10,11,12 there are respectively4692,12250,31020,80018 cyclic rooted words, with1008,4344,18708,80018 retained. Total:127980 cyclic words,104078 retained, and18060 exact ordered-pair kernel checks. All pass in normal and optimized Python with byte-identical JSON. Reported Jacobi eigenvalues are explicitly floating diagnostics, not validated spectral bounds or an asymptotic proof.

A particularly direct new stress construction uses block w=(a,c,a,d), whose inverse is distinct and whose first/last factors differ. The cyclic relator w^3 gives THREE PARALLEL edges between w and w^{-1}. Its two-vertex Laplacian is [[3,-3],[-3,3]], with exact spectrum0,6 and degree3 at each vertex. Two repeated samples give eigenvalue12 for their sum while each sample retains norm6. This demonstrates sharpness of both local bounds in the most correlated allowed case, rather than assuming a simple triangle. It also confirms why whole-sample, not independent-edge, concentration is needed.

The new program additionally exhausts two linear draws of length3: linear universe26, cyclic universe12, count distribution196/336/144 for0/1/2 acceptances. Accepted single labels are exactly uniform and the two-label table has every cyclic ordered pair once. This is a finite sanity check of accepted-label independence; the general independence claim is the elementary conditional-product argument above.

## Antecedents and bounded priority wording

I independently read ESI AnnualReport2024 pp77–79 and its copyright/preface information. The same-model syllable-respecting three-block spectral program and its two unfinished steps are explicit on p78. The volume is copyright2025 with an August2025 preface; a2024 project is not a certified2024 public release. The current abstract, introduction, CURRENT_PRIORITY, README and metadata give that antecedent appropriate visibility.

The actual published Ashcroft GGD2023 TheoremB, Definition3.6 and Section6 already handle strict all-integer free-group lengths via almost-equal blocks. The published Drutu–Mackay2019 Lemma12.2 is the direct common-suffix predecessor. The note credits both. The basic link criterion, Perron/Markov language methods, and matrix concentration are also established inputs, not claimed inventions.

The stronger nearby results were not dismissed solely because arbitrary factors may be nonhyperbolic. An atomic virtually free lift can map onto arbitrary factor alphabets while preserving inverse pairs and colors. It still leaves a proper constrained language rather than all word-metric annulus elements or a demonstrated maximal geodesic-combing component. I read Ashcroft2202.12318v2 TheoremsA–B, Theorem3.5/Corollary3.6, weighted graph definitions and Theorems6.2/6.9 with their model setup. Positivity of their scalar vertex weights does not automatically model factor-forbidden corners; invoking those results leaves a model-specific gap unless an actual transfer is supplied. This is a blocked direct-corollary route, not a theorem that no adaptation is possible.

BNW1507.01088v1 Example4.2 is genuine rational/free-product language context; its Theorem4.15 has small-cancellation and degeneration conclusions, not the needed one-third property-(T) theorem. Oppenheim2609.21255v1 Definition1.1/Theorem1.2 improves the Gromov model along four-divisible lengths. Its exact Theorem3.6 requires positive cross-first-letter proportions and connected pair graphs for every distinct letter pair; literal unchanged application cannot ignore target same-factor structural zeros. HHG2507.16677v3 TheoremsA–B use a fixed finite collection of random walks, while TheoremE/CorollaryF and Section6 construct existential special common quotients. They are not the exponential IID exact-syllable law here.

Replacement versus nonreplacement is NOT itself a novelty distinction: a same-support monotone theorem above one third transfers by occupancy and density slack. Ordinary free-group support versus constrained syllable support is a substantive unproved-law-transfer issue. The current contribution is carefully limited to completing the weighted endpoint, torsion deletion/transfer, type spectrum and concentration steps for the stated model. Existing25-query classical and40-query recent reports, with the parent's additional bounded searches, have explicit scopes and access limits. I read their comparisons and reports only after the initial memo; I do not promote their search failure into an exhaustive absence proof. No verified firstness, current worldwide openness, or strategy-invention claim is accepted or needed.

## Whole-package engineering, preservation, and layout

I read all four CURRENT program bodies in full: outer verifier, portable verifier, original checker and deterministic builder. Their trust flow is coherent:

1. Separately authenticate startup code and external manifest/index before execution. The README explicitly says an adjacent manifest or self-hash is insufficient, and that absence of final external acceptance means still under review. The future acceptance is kept outside the ZIP to avoid a circular archive hash.
2. Strictly parse the pinned inventory; reject duplicate JSON keys, nonfinite constants and overflow floats, bad schemas, noninteger/bool sizes, unsafe/noncanonical paths, duplicate rows, file/directory collisions, overlarge declared inventories, and closed-tree extras including empty directories.
3. Before payload reads, screen leaves/directories as ordinary, and use bounded reads with lstat/fstat, nonblocking open and O_NOFOLLOW where available. Internal symlinks, including aliases to ordinary files, and FIFOs are rejected. Chosen roots/outside ancestors may be resolved. No defense against hostile concurrent ancestor replacement is claimed.
4. Authenticate ALL bytes before copied execution. The outer wrapper snapshots verified in-memory portable bytes; the portable verifier snapshots verified checker/payload bytes. The old wrapper is never executed. The builder separately checks its verifier's external hash before copied execution and writes only after successful replay into a fresh/empty output outside the assembly.

The historical outer manifest and all15 original files remain frozen. Thirteen original root copies are unchanged; current README/outer manifest are intentional wrappers and the original versions remain inside source/. Three archives preserve12+7+7=26 members. The new verifier's metadata and regular100644/sorted/fixed-date deflated ZIP checks are appropriate for the new archive. The legacy archives' omitted Unix type bits are explicitly interpreted as implicit regular files; explicit special or executable members reject without altering original bytes.

The external seal and my initial/updated/final authentications bind all172 regular files,143 portable members,11 core files and all canonical copies. The metadata in CURRENT_PUBLICATION, preprint metadata, portable metadata and deposit metadata agrees. Author Alec Kriebel, ORCID0009-0001-9320-500X, AI use, unrefereed status, no completed external human peer review, no formal proof-assistant verification, and finite-diagnostic limits are explicit. The deposit names exactly the paper PDF and verification ZIP, with no third upload.

I visually inspected ALL7 paper pages using existing canonical110dpi renders, after independently matching the underlying canonical PDF to the candidate pin. All text, formulas, references, disclosure footnote, margins and page numbers are readable; no clipping/overlap/broken glyph was found. Page7 is a short continuation of the bibliography. pdfinfo independently reports7 letter-size pages,96815 bytes, no encryption and no JavaScript. No PDF was regenerated. I also visually inspected KKp7 and Tropppp20–21.

The complete portable inventory contains only the new note PDF and the three original evidence ZIPs as PDF/ZIP payloads. The nested26-member inventories were inspected. Downloaded source papers, extracts, renders, full corpora and private credentials are absent from the allowlisted payload. A limited path/content signature scan found no suspicious raw-source paths or credential signatures; this is not advertised as a general secret-scanning guarantee.

## Replays and independent negative controls

The actual outer --full path passed in normal and optimized modes. Each execution authenticated all original files/archives and reproduced14 exact child receipts:6 positives and8 intended negatives across normal and optimized child modes, with no historical-wrapper execution. The same unchanged143-member assembly rebuilt to453413-byte ZIP SHA256 `c300b11741b2f8da35febe771114b5def4489bf91bf6d87d19debc5e6bc57731` in both modes. Byte reproducibility is bounded to the same input bytes, Python ZIP implementation and zlib, as the paper/package states.

The independently authored `adversarial_package_checks.py` passes99 intended rejections and2 grouped positive controls PER mode. It separately attacks the duplicated parser/path guards in all four current programs, then uses tiny actual CLI fixtures. Duplicate keys, nested duplicates, NaN, Infinity and1e999 overflow are distinct cases. The malformed-index fixtures recompute the test external pin deliberately, reaching parser/semantic guards rather than merely demonstrating digest rejection. That artificial resealing does not claim to defeat fixed external trust.

Actual CLI controls cover extra file, extra empty directory, leaf/directory symlinks, FIFO pre-read rejection, inconsistent declared byte count, duplicate inventory row, noncanonical path and boolean size. A changed checker carrying a side-effect marker is rejected before --full execution. A changed inner verifier with an artificially resealed OUTER manifest still fails the inner index binding before execution. A conflicting builder verifier external pin rejects before creating output. Every side-effect marker remains absent. These are genuinely active pre-execution checks, not only searches for guard names.

The review driver initially used two asserts for observed child status/rebuild hash/size. At the parent's request I replaced them with explicit runtime exceptions in this directory and reran the current driver with optimization enabled; all child checks still passed. This was an improvement to this review's evidence tool, not a candidate defect or mathematical repair. The new mathematics and attack programs use explicit runtime guards throughout.

Optional full-source20-receipt replay was NOT rerun here, in accordance with the disk constraint. I authenticated and read the external sealed `ROOT_OUTER_FULL_SOURCE_R1.json`: it records the actual same-index normal replay, with8 positive/12 negative receipts, all20 intended outputs matched, exact15/26/172/143 counts, and no old wrapper. That is previously recorded evidence, distinguished from my own14-receipt replays. Its source-input reads are guarded in the current checker I read in full. This review does not claim independently reretrieved corpora or revalidated their entire contents by another large copy.

## Limits, strongest verified conclusion, and final disposition

The analytical proof, with its named established normal-form, Perron/linear-algebra, KKv2 and Troppv7 inputs, supplies the stated all-length fixed-parameter property-(T) result. I found no remaining unsupported central claim in that deduction. The finite constructions and replays only test identities and artifact behavior. No quantity of finite checks certifies property(T) or all asymptotics; no literature query count certifies novelty.

Runtime trust is trusted Python/stdlib/filesystem with no hostile concurrent ancestor replacement. Startup flags are not an operating-system sandbox. This review used one Python/zlib environment; no cross-runtime byte identity is claimed. The original Zuk and unread final journal bodies remain outside my direct source-body validation. Priority searches are dated/bounded, and no human or formal review is represented.

**Strongest verified result:** the unchanged sealed R1 whole package is internally consistent with a complete model-specific analytical proof for the exact n>=3 fixed-parameter law, preserves its historical evidence, states its source and priority boundaries accurately, renders correctly, and has reproducible authenticated finite checks and archive rebuilding under the documented assumptions. **Remaining blocking mathematical/package gap found: none. Required candidate repairs: none.** Parent publication and external acceptance actions remain separate; this review has not performed or authorized them.

The final unchanged authentication and explicit public file allowlist accompany this report. The public allowlist contains authored review text/code and receipts only. It excludes downloaded PDFs/text/renders, corpora, fixture trees and rebuilt ZIP outputs.

## Exact11 core pins

| Core path in publication_20261015/preprint | Bytes | SHA256 |
| --- | ---: | --- |
'''+pins+'\n'
(HERE/'REPORT.md').write_text(body)
decision={'timestamp_utc':now,'decision':'CLEAR','pr':872,'problem_id':30006628,'review':'new independent adversarial whole-package review02','candidate':'work/pr872_revision_r1','candidate_unchanged':True,'original_effort':'1/5','new_central_proof_search_attempts':0,'external_seal_sha256':'9eafa209f3bb74f1ba81fd8eef52087e0d16ea4b05ae8624a1c2a4e36ec5ef22','outer_manifest_sha256':seal['outer_manifest_sha256'],'outer_verifier_sha256':seal['outer_verifier_sha256'],'outer_files':172,'portable_members':143,'core_files':seal['core_files'],'mathematical_gaps_found':[],'package_gaps_found':[],'required_candidate_repairs':[],'strongest_verified_claim':'The stated fixed n>=3 cyclic syllable density theorem through all integer lengths follows from the model-specific analytical argument and its exact named established inputs; unchanged whole-package engineering and bounded source/priority wording pass.','fresh_finite_checks':{'cyclic_relators':127980,'retained_relators':104078,'exact_kernel_pair_checks':18060,'normal_optimized_identical':True,'sharp_degree3_norm6_power_relator':True,'accepted_label_independence_check':True},'fresh_package_controls':{'intended_rejections_per_mode':99,'grouped_positives_per_mode':2,'changed_code_markers_absent':True,'resealed_parser_distinctions':True},'full_replay':{'own_default_receipts_per_outer_mode':14,'normal_optimized':'PASS','optional_source20':'READ_AUTHENTICATED_SEALED_PARENT_RECEIPT_NOT_RERUN'},'deterministic_rebuild':{'normal':'PASS','optimized':'PASS','bytes':453413,'sha256':'c300b11741b2f8da35febe771114b5def4489bf91bf6d87d19debc5e6bc57731'},'pdf_pages_visually_inspected':7,'deposit_upload_files':2,'formal_verification':False,'completed_external_human_peer_review':False,'exhaustive_novelty_certificate':False,'worldwide_current_openness_certificate':False,'literature_claim_scope':'Dated and bounded primary-source theorem/model comparisons; explicit ESI/Ashcroft/Drutu-Mackay antecedents retained.','publication_actions_performed':False,'completion_estimate_percent':100,'report_sha256':hashlib.sha256((HERE/'REPORT.md').read_bytes()).hexdigest(),'limits':['Established external theorems assumed, not reproved.','Floating eigenvalues are diagnostics, not validated bounds.','No fresh web search; actual relevant primary local bodies inspected with exact scopes.','Trusted Python/stdlib/filesystem; no hostile concurrent ancestor replacement; startup flags not an OS sandbox.','Same Python ZIP implementation/zlib reproduction only.','No independent large optional-source replay in this review.']}
(HERE/'DECISION.json').write_text(json.dumps(decision,indent=2)+'\n')
print(json.dumps({'decision':'CLEAR','report_bytes':len((HERE/'REPORT.md').read_bytes()),'report_sha256':decision['report_sha256']}))
