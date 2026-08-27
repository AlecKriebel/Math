# Fresh adversarial mathematical review — 2026-08-26 referee package

Date: 2026-08-26  
Reviewer stream: independent mathematical/proof audit  
Package root (`R` below):
`/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-26_r3/isolated/k2p_principal_d_plus_submission_referee`

**Post-integration disposition.** This document preserves the deliberately
independent mathematical stream and its contemporaneous `UNVERIFIED` labels
for finite computations it did not execute. The separately audited fresh
quick replay (23/23), full replay (41/41), and low-contention outer mutation
control (25/25, zero survivors/blockers) subsequently passed. The integrated
final statuses are therefore Mathematics PASS and computational evidence PASS.
The final scientific recommendation remains HOLD for two theorem-neutral
reproducibility blockers: the stale printed hashes identified here and the
strict-JSON duplicate-name failure found by the independent provenance stream.

## Bottom line

**Scientific recommendation from this stream: HOLD.** I found no
counterexample, invalid implication, or unresolved hand-proof gap in the
stated K2P-SAME theorem. The analytic/topological proof architecture is
mathematically coherent, and the previously reported reconstruction,
rank-crosswalk, parameter-transport, genericity, continuous-time, and
weak-sharpness issues are either repaired or explicitly bounded.

The HOLD is caused by one new, concrete reproducibility defect: the reader
supplement prints the wrong SHA-256 for the load-bearing
`composite_reseal_diff_audit.json` in two places. The artifact, release lock,
and theorem crosswalk agree with one another; the supplement source and PDF
instead repeat a stale hash. This does not alter the theorem or the audit
payload, but it defeats the supplement's exact hash-binding assertion and
requires correction, PDF rebuild, and package resealing before submission.

- Hand/analytic mathematics: **PASS**, conditional only on the exact finite
  classification premise stated in Theorem `thm:bounded`.
- Load-bearing finite computation: **UNVERIFIED in this mathematical stream**;
  it must be adjudicated from the fresh independent execution/code streams.
- Integrated theorem status before those streams are combined: **UNVERIFIED**,
  with no mathematical counterexample established.
- Reproducibility/release status: **HOLD** because of Finding 1.
- Confidence: high (about 0.90) that the hand proof is logically sound; medium
  pending fresh exhaustive execution of C04--C09.

I did not execute or import any submitted Python. I treated stored reports and
PASS labels only as assertions. All independent calculations below were made
from the displayed definitions and primitive graph encodings, using exact
rational arithmetic outside the package.

## Material read and bound

I read the complete 26-page article and 24-page supplement, visually inspected
all 50 rendered pages, read all five declared TeX/Bib inputs in full, and read
the generated certificate appendix, compression tables, theorem/artifact
crosswalk, both feedback dispositions, the aligned promotion manuscript, and
the authoritative proof narratives listed later in this report. I found no
missing text, clipped equations, unreadable tables, or other visual defect.

| Artifact | Lines/pages | SHA-256 |
|---|---:|---|
| `proof_compression_submission/article/main.tex` | 1,866 lines | `d64574e30ef3dac38c91613938a6ce29f7b07688ea791013c56a45e9af0e75c3` |
| `proof_compression_submission/article/references.bib` | 202 lines | `d1b3b50f6e276cc147471dcab9f30ed3a9b629fddc19ffb7fea58d427ee5de6b` |
| `proof_compression_submission/supplement/supplement.tex` | 982 lines | `7b28e0ff620b24256f4eebe61fc233dc21df8ffd7b4b552b51eb579712358bc4` |
| `proof_compression_submission/supplement/certificate_appendix.tex` | 285 lines | `936e8d1879acd224affb053489a618dcfe8d7a7a2a5500bc8f0f85dd1b16794d` |
| `proof_compression_submission/supplement/compression_tables.tex` | 69 lines | `22ff0534b79cf226c9041703ab9d87ab123914bbb55ec1d44c84041a8616be81` |
| `proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf` | 26 pages, 194,327 bytes | `2bca627d072cf96c850a7196be9101a7e061499bbcc61ebbb8ff256d4bf864b9` |
| `proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf` | 24 pages, 160,133 bytes | `4bdcfe32cf3dbcd586d9bf68f3d287e4f5f58aa3384aa5daaf454fde3e361621` |
| `proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.md` | complete | `23b4fd6819aa40da9749327efeded8ff65c3da87c73b034fcc36b609b7c75d6c` |
| `proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json` | complete | `dbdd8fac081cbb523a3eb296f05c10c2166f56acbf128170b2ac51da5991bed8` |
| `proof_compression_submission/FRESH_ADVERSARIAL_R2_DISPOSITION.md` | complete | `456d62013c7defad84996d792158fa1cff53012a4f51445e6dffa5742932bed6` |
| `proof_compression_submission/FEEDBACK_DISPOSITION.md` | complete | `e489f180d443211692aa5f7407aaac7aa76ad266942c019c618e26995da71e3c` |

Hash agreement in this table is provenance evidence only. It was not used as
mathematical validation.

## Claim matrix

`PASS` below means the mathematical implication was checked. `UNVERIFIED`
means the claim includes an exhaustive submitted computation that this stream
deliberately did not execute; it is not shorthand for failure.

| Claim | Status | Proof evidence checked | Submitted computational evidence inspected | Independent attack/check | Exact remaining gap |
|---|---|---|---|---|---|
| C01 principal domain, subdivision, root movement | **PASS** | Article 301--413; domain/rooting proof | Domain certificate/crosswalk bindings | Re-derived inverse-Fourier inequalities; checked exact boundary-near rational families; checked near-identity subdivision and the reticulation-adjacent switching argument | None in the hand proof |
| C02 quartet signs, whole-map tree/sunlet sign, decorated blob tree | **PASS** | Article 415--533; quartet and tree/sunlet proofs | Exact sign certificates and terminal bindings identified | Re-derived the `F_A,G_B` mixture logic and the factorization of `T_3`; checked strict signs use positivity, not sampling | External Corollary 2.12 attribution is left to the literature stream |
| C03 bridge fibre, marginal products, localization, parameter transport | **PASS** | Article 535--846; bridge and local-product proofs | Parameter-transport certificate and v2 mutation report inspected | Checked the two independent C/T and G gauges, degree-two exclusion, analytic normalizers, D-plus product/surjectivity, and fixed-full quantifiers | Exhaustive coverage of every stored transport belongs to computation |
| C04 primitive grammar, canonicalization, completion counts | **UNVERIFIED** | Article 850--1,040; canonicalizer and finite-universe narratives | Primitive/canonicalizer certificates identified | Independently derived the five core tuples and all six printed `C(k,epsilon)` values and raw totals | Fresh exhaustive primitive generation and slow/fast class comparison |
| C05 all 4,379 rank descriptors and 23,822 rank directions | **UNVERIFIED** | Article 1,041--1,164; exact rank-upper proof | Crosswalk now binds `verify_rank_upper_certificates.py`, `syzygy_upper.py`, replay, and v2 mutations | Checked the polynomial-vector-field kernel argument and exact dimension formula; confirmed the sampled-rank substitution is now a full verifier-facing attack | Recompute all 4,379 symbolic upper/lower certificates and 864 transports |
| C06 direct quadratic/cubic/quartic/quintic separators | **UNVERIFIED** | Generated appendix lines 1--285; direct-template narrative | Printed appendix, direct closure, registry, and transports identified | Checked coordinate conventions, direction restrictions, multihomogeneous semantics, and the explicit refusal to infer graph equivalence from repeated bodies | Independent expansion of every target zero/source nonzero pullback |
| C07 corrected raw4/theta2/cycle finite censuses | **UNVERIFIED** | Article 1,087--1,125; cycle/theta2 narratives | Corrected composite, cycle, and reseal artifacts identified | Reconciled the stated arithmetic and hashes read-only; found the stale printed hash in Finding 1 | Fresh regeneration and rowwise comparison of the millions of directions |
| C08 997-parent restoration forest | **UNVERIFIED** | Article 825--846 and 1,127--1,133; restoration archetypes | Forest, historical crosswalk, replay, and parameter transports identified | Independently checked `36,568+256=36,824` and `35,758+606+148+24+248+8=36,792`; traced the worked depth-two archetype and its fixed-full logic | Fresh traversal of every physical child, parent, transport, and terminal |
| C09 arbitrary ordered subdivision words from one-/two-port probes | **UNVERIFIED** | Article 1,135--1,154; probe-word theorem | Primary, independent graph audit, restriction and transport ledgers identified | Checked the mathematical induction: one-port fixes segment, two-port fixes every pairwise order, both deletion orders enforce overlap coherence | Fresh graph reconstruction of all sites/rows/transports |
| C10 triangle germ and contextual gluing; genericity mechanism | **PASS** | Article 1,204--1,474 | Exact triangle and tree/sunlet witnesses identified | Independently recomputed the two exact block determinants `-1/2` and `-1/4`; checked submersion, contextual constant-rank sections, total source-rank-drop image, target incidence sections, and real/complex dimension passage | Global use still inherits C04--C09 |
| C11 global K2P-SAME equivalence and exact reconstruction | **UNVERIFIED** | Article 1,332--1,538 | C11 JSON now correctly names article source/PDF as current authority and demotes the promotion manuscript | Checked both global implications; reconstruction now retains every candidate through assembly and uses exact class membership | Only the fresh verification of the finite bounded premise |
| C12 strict continuous-time transfer | **UNVERIFIED** | Article 1,540--1,588 | Domain/bridge bindings identified | Checked product roots and the simultaneous bridge inequalities exactly; transfer argument itself passes | Inherits C04--C11 rather than adding a new gap |
| C13 weak-class `4n-3` sharpness | **PASS** | Article 1,590--1,799; sharpness proof/audit/crosswalk | Exact graph, tensor, minor, and mutation artifacts identified | Independently rebuilt both four-switch maps, the common tensor, both named 9x9 determinants, physical inequalities, graph non-equivalence, tree-child/non-tree-child rootings, cherry inverse, and dimension induction | None |
| P01 supplement exact hash assertion for composite reseal audit | **FAIL** | Supplement source 752--757 and 790--793; PDF pages 20--21 | Release lock and theorem crosswalk | Direct SHA-256 recomputation | Correct two stale printed values and reseal; see Finding 1 |

## Numbered findings

### 1. Reproducibility-blocking: the supplement prints a stale composite-reseal hash twice

The authority named by the supplement is
`work/final_theorem_release/composite_reseal_diff_audit.json`. Its actual
SHA-256 is:

```text
96e30bae42939fa50dd585ba900bc5bd45e5eb122334de86c34654004212db4c
```

That value is also bound by:

- `work/final_theorem_release/RELEASE_LOCK.json:528-531`;
- `proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json:869`;
- `proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json:754`.

But `proof_compression_submission/supplement/supplement.tex:755` and `:793`
both print:

```text
bc91fee3b7541fcae72c4db2e66776fbfc69c43890718239f0eea41bb2cc0654
```

The stale value is visible in the rendered supplement on PDF pages 20 and 21.
A package-wide search finds it only in those two supplement-source locations;
it is not the hash of the stated authority. The other authority/hash pairs and
frozen anchors in the same tables that I checked recompute correctly.

Severity/effect: **reproducibility-blocking, theorem-neutral**. The JSON audit
itself is coherent, has schema
`k2p-composite-domain-reseal-diff-audit-v1`, status PASS, 2,528 changed theta2
rows, 2,943,712 unchanged theta2 rows, zero raw4 changes, and zero unresolved
rows. I found no mathematical consequence from the stale printed digest.

Smallest adequate remedy: replace both stale strings by the actual SHA, rebuild
the supplement PDF, then refresh every source/PDF/build-report/manifest/outer
ledger/archive binding affected by that rebuild. The underlying composite audit
need not be regenerated unless the rebuild workflow changes it. Downstream
submission artifacts do require resealing.

### 2. Prior proof blocker resolved: reconstruction now retains all candidates

The current authority is unambiguous. Article
`main.tex:1504-1526` retains every bounded candidate not excluded, follows
restoration for each, assembles every coherent graph, groups the finite list by
triangle class, and decides exact semialgebraic membership for every class.
The genericity theorem ensures exactly one feasible class outside `E_N`.

The aligned promotion manuscript says the same at lines 716--737. More
importantly, the detailed C11 JSON crosswalk at lines 1,479--1,505 labels
`main.tex` and the article PDF as current theorem authorities and labels the
promotion manuscript a machine-bound companion, “not current submission proof
authority.” The earlier stale-authority defect is therefore repaired.

### 3. Prior rank-crosswalk blocker resolved

C05 of `THEOREM_ARTIFACT_CROSSWALK.md:20` now lists the production symbolic
verifier, `syzygy_upper.py`, and the exact replay, rather than binding only a
summary. `work/rank_upper_certificates/PROOF.md:24-115` gives a valid global
upper-rank mechanism: polynomial vector fields are placed in the exact kernel
of the full polynomial Jacobian coefficient-by-coefficient; exact rational
evaluation certifies the independent kernel dimension; a nonzero complementary
Jacobian minor supplies the lower bound; affine parameter/output transports
preserve rank.

The v2 mutation report contains one complete coherently resealed package attack
that replaces a symbolic field by sampled evidence and is rejected by the
untouched production verifier at
`RANK_UPPER_SYMBOLIC_FIELD_DIMENSION_FAIL`. This is the intended semantic gate,
not a checksum-only rejection. The all-descriptor replay itself remains for the
fresh computation stream.

### 4. Prior parameter-transport mutation defect resolved, with an honest scope split

The mathematics at article `main.tex:728-778` is now precise: visible edge
classes are equality classes of the full switching/character exponent arrays;
the `s` and `g` products stay paired; tensor-invisible inheritance variables
are forgotten only when both parent choices induce identical visible data; and
`lambda -> 1-lambda` occurs only when a certified graph transport reverses the
stored parent order.

The v2 parameter-transport mutation report records ten useful semantic attacks:
four complete, coherently resealed ledger/certificate attacks run through the
production verifier, and six exact local semantic-validator attacks. All ten
match their intended diagnostics; wrong diagnostics, tracebacks, timeouts,
signals, optimized execution, and stale PASS output are explicit negative
controls. This accurately repairs the prior tautological hash-difference
evidence. It does not pretend that all ten are full end-to-end attacks.

### 5. Nonblocking independence boundary is stated correctly

Supplement `supplement.tex:112-119` expressly disclaims an atlas-free
all-family orbit partition and a second symbolic engine for every
higher-degree polynomial. The finite theorem remains computer-assisted, and
the article `main.tex:1811-1820` says “independent replay” means a separately
implemented program, not independent human review. Supplement lines 892--894
also say mutation sensitivity is not the associated mathematical implication.
This is an evidence limitation, not a hidden theorem premise or a reason by
itself to reject the result.

### 6. No theorem-fatal or proof-blocking mathematical defect found

I attacked every analytic implication listed below and found no invalid square
inverse, lifted abstract marginal relation, target-deletion inverse, remote
compensation step, illicit inheritance quotient, or full-image-identifiability
claim. The historical `work/global_theorem_closure/GLOBAL_PROOF.md` is not a
current authority and was not used to repair the article. Subject to fresh
verification of the explicitly retained finite residue, the main equivalence,
generic identifiability, reconstruction, continuous-time restriction, and
weak-class sharpness follow.

## Detailed mathematical audit

### Definitions, domain, restrictions, and root movement

The binary rooted and one-step standard semi-directed conventions at article
206--244 are quantified consistently. The no-omnian characterization at
246--275 correctly separates weak from strong tree-childness under the fixed
mixed-graph convention. Restriction cleanup is not confused with admissible
rooting cleanup. Ordinary-triangle equivalence at 289--299 preserves labels,
ports, nontriangle factors, and coherent transports and does not claim equality
of complete stochastic images.

Inverse Fourier transformation gives
`(1+2s+g, 1-g, 1-2s+g)/4`, so positive eigenvalues plus strict stochastic
entries give exactly `D_plus`. The near-identity subdivision proof uses
openness and does not assert false universal square-root closure. For exact
boundary attacks, the following rational families satisfy every strict
inequality without floating point:

- near `s=1,g=1`: `s=g=1-1/M`, `M>1`;
- near `g=0`: `s=1/(3M), g=1/M`, `M>1`;
- near the slanted boundary: `s=3/4, g=1/2+1/M`, `M>2`;
- in the CT cone near `g=s^2`: `s=1/2, g=1/4+1/M`, `M>2`.

The root-movement argument treats ordinary reversibility and the special case
adjacent to a reticulation incoming edge switch-by-switch. In the unchosen
parent switch, the residual stem carries total character zero, so the multiplier
is exactly one.

### Pointwise topology and bridge decomposition

The displayed-quartet pullback table is sufficient because `F_t` and `G_t`
are linear in the Fourier tensor and every inheritance weight is strictly
positive. The singleton-versus-multiple and two-multiple displayed-set cases
exhaust all distinct nonempty subsets of three quartet topologies. The
whole-map `T_i` identity is a direct polynomial identity on the original map;
the revoked rooted tree/sunlet oracle is explicitly excluded.

For a fixed bridge character, the cut flattening is a positive rank-one block.
Rank-one uniqueness supplies one scale per sector and incidence. Global
`C <-> T` symmetry forces the paired scales to agree; the G scale is independent.
For unmarked degree at least three, the equations `rho_e rho_f=1` force every
positive `rho_e=1`; the excluded degree-two factor is the only reciprocal
stabilizer. The displayed pair-anchor exponent matrix has full rank, giving
the positive analytic square-root normalizers. Peeling the component-incidence
tree precludes holonomy. Near-identity serial splitting realizes all local
gauge directions physically, so the quotient is not merely an ambient positive
tensor quotient.

### Marginal descriptors, localization, and restoration quantifiers

The paired product map preserves `D_plus`: when `s1*s2>1/2`, expanding
`(2s1-1)(2s2-1)` leaves the strictly positive correction
`2(1-s1)(1-s2)`. The explicit common-`r` section proves surjectivity and a
local physical section. The graph-derived full switching signature prevents
mixing the two K2P sectors and prevents arbitrary inheritance complements.

Localization first fixes the source product box and extracts the focal
projective factor intrinsically through positive bridge normalizers. A finite
semialgebraic cover then selects one fixed target completion type on a
source-open subgerm. Consequently a focal polynomial/rank obstruction cannot
be compensated remotely. The restoration lemma starts from one already fixed
full relation and one actual source insertion/target attachment/transport.
Marginalization produces one enumerated child with an open source restriction;
the proof never lifts a selected abstract child relation or inverts a target
deletion map.

### Core reduction, completion arithmetic, and finite-certificate semantics

The degree sum gives `sum(deg-2)=2(r-1)`. Biconnected binary level two blobs
therefore reduce to a cycle for one reticulation and a theta for two. The
reticulate-pole and same-path exclusions follow from forced path orientations
and directed-cycle contradictions. The four directed theta placements exhaust
the event placements up to the displayed pole/sink symmetries. The repair
clauses at article 973--1,000 have exactly the printed minimal transversals.

Using tuples
`(m,q,r)=(2,1,1),(5,1,2),(5,1,2),(6,2,4),(6,2,2)`, I independently evaluated
the stars-and-bars formula:

| `(k,epsilon)` | independently obtained `C(k,epsilon)` |
|---|---:|
| `(3,1)` | 289 |
| `(3,0)` | 831 |
| `(4,1)` | 831 |
| `(4,0)` | 1,983 |
| `(5,1)` | 1,983 |
| `(5,0)` | 4,155 |

This gives exactly `405,216`, `2,946,240`, and `13,440` raw directions with
the printed source and port-permutation factors. Repair tags remain raw-record
data even when final graphs coincide, so the formula does not silently count
unlabelled isomorphism classes.

The certificate order is logically sound: pointwise sign, directed symbolic
rank, exact polynomial separator, fixed-full restoration, labelled
isomorphism, then ordinary triangle. A rank upper certificate is a polynomial
identity, not sampled rank. A separator requires target pullback zero plus a
strict physical source nonzero witness. Equality terminals require exact
mixed-graph/port/parent transports. The generated appendix explicitly denies
that repeated polynomial bodies license graph-orbit equivalence. The
PC-PARTIAL boundary retains the 75 exceptional rank orbits, 997 restoration
parents, and full probe ledgers.

### Triangle germ, contextual gluing, global equivalence, and genericity

Independent exact elimination on the displayed blocks gives

```text
det(J_0)    = -1/2
det(J_perp) = -1/4
product     =  1/8.
```

Thus each orientation is a submersion onto the nine-dimensional normalized
three-leaf output space at the common strict-CT point. The proof correctly uses
submersion/constant rank, not a square inverse. In context, the contraction
map is restricted once to a generic constant-rank germ and the local triangle
sections are composed with a section of that contraction. Multiple triangles
are handled simultaneously. The bridge incidence scales are then chosen small
enough that the original and both transformed pairs remain in `D_plus`.

Necessity uses pointwise decorated-blob recovery, the complete bridge quotient,
semialgebraic localization, the bounded theorem, and coherent word transport.
Sufficiency uses the common triangle germ, contextual section, and simultaneous
physical gluing. A common full-dimensional physical germ gives the directed
relation in both directions, so no proper one-way containment remains.

For genericity, the complex image closure is irreducible and its dimension
equals maximal physical rank because a nonzero complex-generic minor cannot
vanish on the nonempty real open physical domain. Strong tree-child paths give
`r <= |X|-1`, hence the vertex bound `4|X|-3` and finiteness of labelled
competitors. Crucially, the revised proof removes the image of the **total**
source rank-drop locus by a Nash constant-rank stratification. If a competitor
intersection had full dimension, a target incidence stratum would project with
full rank and yield a physical analytic target section, contradicting the main
theorem. Real semialgebraic and complex Zariski dimensions are then compared
componentwise; every added exceptional component is shown proper before the
finite union is taken.

### Exact reconstruction and continuous-time transfer

The input model is exact-real/QE, not numeric. All unresolved bounded supports
are retained through restoration, word reconstruction, global assembly, and
triangle grouping. Exact existential semialgebraic membership is then decided
for every class. The true class is feasible; a second inequivalent class would
place the tensor in the already excluded competitor intersection. Finiteness
of topologies, forests, sites, and restrictions proves termination. No
bit-complexity or stability claim is smuggled in.

For continuous time, coordinatewise positive roots preserve `s^2<g`, giving
subdivision and marginal sections. In simultaneous bridge gluing, with
`L=max(1,B1/A1^2,B2/A2^2)` and `U=min(1,B1,B2)`, choosing
`s<min(1,A1,A2,sqrt(U/L))` and `Ls^2<g<U` proves exactly that the original and
both transformed pairs satisfy `s^2<g<1`. Nonzero polynomial witnesses remain
nonzero on a dense open subset of the CT domain. The CT result inherits the
finite theorem but has no new logical gap.

### Independent weak-sharpness reconstruction

I reconstructed both three-leaf maps directly from the listed arcs by
enumerating the four reticulation switchings, computing descendant character
sums in the Klein four group, and multiplying the appropriate `s`/`g` edge
coordinates and exact inheritance weights. No stored map or certificate code
was called.

The normalized tensors obtained were exactly:

```text
W : 1, 64009/457492, 64009/457492, 6400/39229939, 1/1372,
    4048/39229939, 4048/39229939, 6400/39229939,
    4048/39229939, 1/1372

W': 1, 15/1024, 15/1024, 5/512, 27/512,
    9/4096, 9/4096, 5/512, 9/4096, 27/512.
```

After multiplying by the stated pendant factors, both yield exactly `1`, six
coordinates equal to `delta^2`, and three coordinates equal to
`(4/5)delta^3`, with `delta=2^-30`.

I then differentiated this independently reconstructed switch map with respect
to the article's named columns. The exact determinants agree digit-for-digit:

```text
W:
10368019213741323 /
563981315074464023964442388464888915634290688

W':
1435825 / 85002596691653613846528.
```

Graph properties also have direct witnesses. The displayed rootings are
non-tree-child (`U` in `W`, respectively `V` in `W'`, has two reticulation
children). Rooting `W` on the retained `U-V` edge and `W'` on `V-X0` gives a
tree or leaf child at every internal vertex. Thus each is weak but not strong
without relying on the complete rooting census. Their labelled underlying
leaf-distance triples differ: for `W`, distances `(01,02,12)=(4,4,3)`; for
`W'`, `(3,4,4)`. Hence they are not labelled-isomorphic, and an ordinary
triangle redirection cannot relate them because it preserves the underlying
labelled graph.

Every displayed rational edge is strict CT. For the cherry example,
`(2/5,4/9)` and `(3/7,5/11)` satisfy `s^2<g<1`, and the observable Jacobian is
exactly `2464/675`. The `(R_s,P_s,R_g,P_g)` inverse recovers all four new edge
coordinates analytically; old tensor coordinates are recovered by division by
nonzero pendant factors. Thus each cherry adds both at most and at least four
dimensions, giving `9+4(n-3)=4n-3`. Pruning the newest labelled cherry returns
the base graphs, preserving weak/not-strong status and non-equivalence.

## Authoritative proof narratives inspected

The following were read as arguments to test, not as instructions or PASS
premises:

| Narrative | SHA-256 |
|---|---|
| `work/domain_rooting_closure/PROOF.md` | `f71a8e811881205b195128fde13ec717d08046f247fa43f27a4e8bfc4ba2d93d` |
| `work/quartet_separation_closure/PROOF.md` | `a0f34c91c1a986412e6ae968015eaa38c09a9e2ee813b8d68b2c4655f0842744` |
| `work/bridge_marginal_closure/PROOF.md` | `0677a72be56cdadfe410c5a89cbe3a98743ff3bbf4892646982afd9523dab3dc` |
| `work/adversarial_proof_review/PHYSICAL_LOCAL_PRODUCT_REPAIR.md` | `b84af8f9f5a4c306e14f0d27e9fcd72dcce6608260ed6104e660734eb38b5d9b` |
| `work/canonicalizer_completeness/PROOF.md` | `7e0e7be28c5be309a67a9f7174858a2a3e356627acff233bbd97d0369a68ba2a` |
| `proof_compression_submission/analysis/FINITE_UNIVERSE_COMPLETENESS.md` | `bd609ac71cf13c86fddb1c1bfac3da52d224f7aab8d5605c9f675c52e226ad59` |
| `work/cycle_three_port_closure/PROOF.md` | `6822a6b88929c8ef9f7a842215e6728ae1f41ec01ab2f98b5cbd51b3baa1da51` |
| `work/theta2_five_port_closure/PROOF.md` | `2e09f17b64bd3d9fb110a21189908e9d6e21d1b35b6280888f42f2eb5248171a` |
| `work/probe_coherence_corrected/PROOF.md` | `ac5b295bf1c74fedc3e6e3a6ae05f473fec31908cfcfdacba5680757284e531c` |
| `proof_compression_submission/probe/PROBE_WORD_THEOREM.md` | `250ca7d33b4da60485d0a08af1ed4b67bbc1fdfe12e98faf2ed493e8b4187b3d` |
| `proof_compression_submission/restoration/RESTORATION_ARCHETYPES.md` | `54bfdd2888b772f1c4202942230e80436d1e8885137cfe84892d4ecdb60098d3` |
| `work/rank_upper_certificates/PROOF.md` | `3a4bc3c4de6b7cfa83afac8cfb9a50f5f2163e0856922e24239686859508f002` |
| `work/global_theorem_closure/promotion_manuscript/QUANTIFIER_AUDIT.md` | `425a041bc3e4cc7bd4f74c952455623ff26f430d9c4ceb006edcac9e8c3765d8` |
| `work/global_proof_adversary/AUDIT.md` | `ccb49a7e3d2fa994dbfbeeceb8b4d115e745b57d536975afeefaabd1ab61b236` |
| `package/original/checkpoint_2/continuation_2/K2P_TREE_SUNLET_SIGN_CERTIFICATE.md` | `f2feaaec71194a794b8b8b6b24a66866803a10fe12ce59a04e7688917b100cc4` |
| `package/original/checkpoint_2/continuation_2/K2P_TRIANGLE_GERM_EXACT.md` | `25593e90d87286d7092b68ba5ac9bc176afba56d98b39becefafb1fe3becbc07` |
| `work/weak_sharpness_closure/PROOF.md` | `dcc36e0ae4299e3f0415d31e73522f224c91506f90062d0a13791af5746e9369` |
| `work/weak_sharpness_audit/PROOF_AUDIT.md` | `d0a4e950a17fe59bda918ed48ff582836ce4592cc4eb97676814cc5ecf1d95aa` |

`work/global_theorem_closure/GLOBAL_PROOF.md`
(`2188d3af3df687093d15a715845c1d7cb65e23aa913900157b318c4769136360`)
was also read but treated as superseded historical material, not current
authority.

## Scope and unrun gates

The article correctly does **not** claim mixed-sign, stochastic-boundary,
singular-edge, higher-level, weak-class identifiability, parameter
identifiability, numerical-stability, bit-complexity, or finite-sample
inference results. The weak-class theorem is a sharpness counterfamily, not a
classification of all weak networks.

Unrun in this mathematical stream:

1. all submitted Python producers/verifiers and their mutation runners;
2. full raw4, theta2, cycle, restoration, and probe regeneration;
3. independent rowwise expansion of every polynomial and rank certificate;
4. external primary-source literature/novelty verification;
5. PDF rebuild and deterministic archive rebuild.

These are not inferred PASS from stored reports. They should be merged from
the dedicated code, execution, provenance, and literature audits.

## Minimal required actions

1. Correct the two stale SHA-256 strings at `supplement.tex:755` and `:793` to
   `96e30bae42939fa50dd585ba900bc5bd45e5eb122334de86c34654004212db4c`.
2. Rebuild the supplement PDF from the five declared sources and refresh all
   downstream build-report, source-manifest, crosswalk, outer-ledger, bundle,
   and archive seals affected by the changed source/PDF bytes.
3. Run the fresh full computational and reproducibility protocol on the exact
   resealed package. If C04--C09 pass independently and no other stream finds a
   defect, the mathematical status may be upgraded from conditional PASS to
   integrated PASS and the scientific recommendation from HOLD to ACCEPT.

No theorem statement, proof architecture, new research direction, or
mixed-sign extension is required by the evidence found here.
