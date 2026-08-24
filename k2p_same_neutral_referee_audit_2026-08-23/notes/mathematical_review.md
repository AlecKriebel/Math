# Independent adversarial mathematical review

Date: 23 August 2026 (PDT)

Submission reviewed: /Users/alec/Documents/Math/k2p_same_neutral_referee_audit_2026-08-23/isolated_handoff/materials/k2p_principal_d_plus_submission_referee

This report is confined to the mathematical argument and the semantics that
connect mathematical lemmas to the finite certificate system.  Stored PASS
reports, certificate counts, and hashes were treated as assertions.  I did not
modify the isolated submission and did not contact anyone.

## Verdict from the mathematical track

**HOLD.**  I found no counterexample to the stated K2P-SAME theorem, and the
analytic architecture is substantially stronger than the stored PASS labels
alone suggest.  However, the article's literal displayed-quartet separator
lemma is false under the article's own Fourier-character convention.  That
lemma is load-bearing for tree-of-blobs recovery and for millions of finite
rows labelled as pointwise quartet exclusions.  The graph-level separation
claim is repairable by a uniform character relabelling, but the printed proof
and its claimed exact replay do not currently perform that repair.

The central theorem therefore remains **UNVERIFIED**, not refuted.  Acceptance
would require correction and resealing of the quartet formula and a semantic
replay that checks the corrected Fourier pullbacks.  It also remains
conditional on the independent computational track establishing the exact
finite ledgers and transports; I did not infer their truth from stored replay
reports.

- Mathematics: **HOLD**
- Analytic/local lemmas other than the printed quartet formula: **PASS**, with
  the finite-classification conclusions conditional as specified below.
- Printed quartet formula: **FAIL**
- Computer-assisted bounded classification in this mathematical track:
  **UNVERIFIED**
- Weak-class sharpness theorem: **PASS**
- Confidence that the quartet defect is real: **>99%**
- Confidence in the HOLD rather than REJECT recommendation: **90%**
- Confidence in the independently checked weak-sharpness result: **95%**

## Materials and locations

The article PDF has 26 pages and the reader supplement has 24 pages.  The
mathematical locations below use both source line numbers and PDF pages.

| Artifact | SHA-256 | Role |
|---|---|---|
| proof_compression_submission/article/main.tex | 1107e5395a0e2ad4da0333cda066ae587d9a9854e61aeba3d2aadcf62e23e45b | Authoritative article source |
| proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf | 86b7ace41d025caddcecae2accb04c496a401501b2a6e65233ad60cfc80e3e2a | Article PDF |
| proof_compression_submission/supplement/supplement.tex | fcb9df1f2ac3d31354e7a67ccb94700f1b67c8ef13db985bef34e327c58d58de | Reader-supplement source |
| proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf | 177006b4d2a21d958f1811c3920bbbfca18fdff87cda8da99b97c9c950dd15cb | Reader-supplement PDF |
| proof_compression_submission/article/references.bib | 14dbb4901d924b068c8cc2d050e73bae3cf996a72863a22ade90d6f8e6b4057c | Bibliography |
| proof_compression_submission/supplement/certificate_appendix.tex | ef878c24ff3f6b28d70b6c3dbf90c6d1e7d3c85a2bece621c96f47c409ca0ffa | Generated certificate appendix |
| proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.md | a73ab7c712059ce4c7565d607a43d9ccc62f49353793a1a39e602a12f494f84e | Theorem-to-artifact crosswalk |
| proof_compression_submission/COMPRESSED_BOUNDED_THEOREM.md | 35ce7367470fe29d02247569cf1c16f1cedf4cd0080d84e02aa2c56572b66544 | Bounded theorem narrative |
| proof_compression_submission/analysis/FINITE_UNIVERSE_COMPLETENESS.md | 0604a331bc5112cae814aaae257296fa7f794bd1c3c7adc7f370ebc62e2a25bd | Primitive/completion argument |
| work/domain_rooting_closure/PROOF.md | f71a8e811881205b195128fde13ec717d08046f247fa43f27a4e8bfc4ba2d93d | Domain/rooting narrative |
| work/quartet_separation_closure/PROOF.md | 629c58d44fbee452b2bf535821520354d4b2061a9f541a3543e741028eb4bd3a | Quartet narrative |
| work/bridge_marginal_closure/PROOF.md | 0677a72be56cdadfe410c5a89cbe3a98743ff3bbf4892646982afd9523dab3dc | Bridge/marginal narrative |
| proof_compression_submission/probe/PROBE_WORD_THEOREM.md | ab55aae4e0d0bba65927519d5970ba11f49e9ce211a051d40dfbf114a45d36ec | Arbitrary-word proof |
| work/global_theorem_closure/GLOBAL_PROOF.md | 6d338a62689ca55bb124b892952ff6e0115c336e28e9ba6fe7e4821e12f54b6c | Global proof narrative |
| work/global_theorem_closure/promotion_manuscript/QUANTIFIER_AUDIT.md | 425a041bc3e4cc7bd4f74c952455623ff26f430d9c4ceb006edcac9e8c3765d8 | Quantifier audit |
| work/weak_sharpness_closure/PROOF.md | dcc36e0ae4299e3f0415d31e73522f224c91506f90062d0a13791af5746e9369 | Weak-sharpness proof |
| work/weak_sharpness_audit/PROOF_AUDIT.md | d0a4e950a17fe59bda918ed48ff582836ce4592cc4eb97676814cc5ecf1d95aa | Weak-sharpness audit |

The independent checks preserved outside the isolated submission are:

| Independent artifact | SHA-256 | Result |
|---|---|---|
| scripts/mathematical/verify_quartet_convention_independent.py | 92b8a5c07301ba5367b49926fdccbf5ae0fcb7bd02906b028be7e25da6381b7e | Symbolically derives every printed and corrected split pullback |
| outputs/mathematical/quartet_convention_independent.json | 07af30a348f67a1449044ef5f2024f80e833b9cc682698ccd52969fe39bcc9bf | Printed formula FAIL; corrected formula PASS |
| scripts/mathematical/verify_triangle_germ_independent.py | 1f1e79f40ccfc8904cbedc1fd851e89cd193cc6eec47a5100ef4ff6c38f29fc8 | Reconstructs the map and differentiates it symbolically |
| outputs/mathematical/triangle_germ_independent.json | 4801dabb3f602761da9450560e9baae62c9061973c3365fafb809a9d17008e88 | Exact rank-nine PASS |
| scripts/mathematical/verify_weak_sharpness_independent.py | d09654dcf247bc38e4271ef8252bf27e6ed566cea2d88c8c474a895f3a24f7e1 | Direct graph, switching, Jacobian and cherry reconstruction |
| outputs/mathematical/weak_sharpness_independent.json | a18d67fd9858d217578df413714f3b9e9da88e0f39635f37003574806a3319d3 | Weak-sharpness PASS |

All three scripts import no submission module, atlas, canonicalizer, stored
tensor or expected certificate.  With the sealed project's SymPy environment,
their wall times were approximately 0.39 s, 0.36 s and 0.57 s respectively.

The principal article locations are: definitions at main.tex lines 201–299
(PDF pp. 3–4), Fourier map and physical domain at lines 300–373 (PDF pp.
4–5), pointwise topology recovery at lines 374–523 (PDF pp. 5–7), bridge
fibre at lines 524–681 (PDF pp. 7–9), localization at lines 682–836 (PDF pp.
9–11), finite theorem at lines 837–1192 (PDF pp. 11–16), triangle/global
theorem at lines 1193–1353 (PDF pp. 16–18), genericity at lines 1354–1468
(PDF pp. 18–20), reconstruction at lines 1469–1528 (PDF p. 20),
continuous-time transfer at lines 1529–1578 (PDF pp. 21–22), and weak
sharpness at lines 1579–1789 (PDF pp. 22–24).

The supplement's grammar is at supplement.tex lines 141–230 (PDF pp. 4–6),
certificate decision tree and census at lines 231–339 (PDF pp. 6–8),
restoration/probes at lines 309–396 (PDF pp. 8–9), representative exact
calculations at lines 397–442 (PDF pp. 9–10), weak certificate at lines
443–560 (PDF pp. 10–16), and theorem-to-artifact crosswalk at lines 561–734
(PDF pp. 16–21).

## Finding 1 — false printed quartet separators

**Classification:** proof-blocking and certificate-semantics-blocking; not,
on present evidence, theorem-fatal.

**Location.**  The article fixes the character order (0,C,G,T) and edge
spectrum (1,s,g,s) at main.tex lines 302–313.  Thus C and T, not G and T, are
the equal K2P sector.  Nevertheless lines 416–450, equations (4)–(5), Lemma
3.3 (article PDF p. 6), and work/quartet_separation_closure/PROOF.md lines
8–29 print

    F_A = q_GGGG - q_GGTT,
    G_B = q_GGGG - q_GGTT - q_GTTG + q_GTGT.

**Minimal exact counterexample.**  On a quartet tree with split 12|34, the
Fourier tree monomial formula gives

    q_GGGG = g_1 g_2 g_3 g_4,
    q_GGTT = g_1 g_2 s_3 s_4,

because the internal-edge character is zero in both monomials.  The claimed
F_A therefore need not vanish.  Give the four pendant edges the strict
continuous-time pairs

    (1/2,1/2), (1/2,1/2), (1/2,1/3), (1/2,1/2)

and give the internal edge any strict continuous-time pair, for example
(1/2,1/2).  Every pair satisfies 0<s<1 and s^2<g<1, but

    F_A = 1/24 - 1/16 = -1/48.

This directly falsifies the first sentence of Lemma 3.3 under the declared
convention.

**Smallest mathematical repair.**  Uniformly use the equal C/T sector:

    F_A^correct = q_CCCC - q_CCTT,
    G_B^correct = q_CCCC - q_CCTT - q_CTTC + q_CTCT.

For split A=12|34, F_A^correct is zero.  On either crossing split it is

    (product of the four pendant s_i) (1-g_internal) > 0.

For split B=13|24, G_B^correct equals

    2 (product of the four pendant s_i) (1-g_internal) > 0,

and it is zero on A and C.  Hence the graph-level theorem that unequal
nonempty displayed-quartet sets have disjoint strict images follows exactly
as intended.  This independent correction also shows why the central theorem
has not been disproved.

**Exact comparison with Englander et al. version 4.**  I obtained the primary
version through the official bioRxiv version API
https://api.biorxiv.org/details/biorxiv/10.1101/2025.04.18.649493 and the
official PDF URL
https://www.biorxiv.org/content/10.1101/2025.04.18.649493v4.full.pdf.
The API records version 4 on 4 July 2026.  The PDF inspected on 23 August 2026
is cached at tmp/literature/englander_v4_2026-07-04.pdf, has 31 pages,
927,795 bytes, and SHA-256
69f04a54d7deb5e12485ba566b50bdcffddf5cd1d80c6c7cfb0c656bc504e40d.

On Englander PDF p. 10, Section 2.1.2, the state characters are identified as
A=(0,0), G=(1,0), C=(0,1), T=(1,1), and the K2P constraint is explicitly
a_eG=a_eT.  On p. 12, Proposition 2.9, equation (2) is
q_GGGG-q_GGTT; its proof explicitly invokes a_3G=a_3T and a_4G=a_4T.
Proposition 2.10, equation (3), is
q_GGGG-q_GGTT-q_GTTG+q_GTGT.  Theorem 2.11 starts on p. 12 and concludes
on p. 13; Corollary 2.12 is on p. 13.  The appendix proof of Proposition 2.10
on p. 22 again states a_eG=a_eT for every edge.

Thus the attribution to Englander for the general pointwise displayed-set
theorem and tree-of-blobs corollary is **correct**.  The defect is solely the
submission's specialization: main.tex lines 302–313 changes the order to
(0,C,G,T) and the spectrum to (1,s,g,s), making C/T equal, but lines 419–420
retain Englander's G/T coordinate bodies.  A uniform character permutation
is mathematically harmless only when it is actually applied to those bodies.

**Replay gap.**  work/quartet_separation_closure/verify_quartet_logic.py
(SHA-256 edd0e42ffe14a4dbc30c685ad20dcb0d766547fe0dcefdd6a7ff51cc998c8ae1)
enumerates the seven nonempty subsets of the three topologies and their 21
unordered pairs (lines 25–76).  It assumes abstract F and G zero sets.  It
never constructs the Fourier tree monomials and contains none of the printed
coordinates.  Thus its PASS cannot detect this defect.  The crosswalk claims
this script as the exact replay of C02 at
THEOREM_ARTIFACT_CROSSWALK.md line 17.

**Effect on finite evidence.**  The raw, theta2, cycle, restoration, and probe
ledgers store graph-derived displayed sets and an abstract
displayed-quartet-mismatch reason.  Their graph counts need not change after
the corrected formula is proved.  But their current advertised exact
mathematical binding points to a false literal formula.  The affected
categories include 360,408 raw-four rows, 2,942,592 theta2 rows, 535,920 cycle
completions, 35,758 first-layer and 248 second-layer restoration rows, and
27,758 one-port plus 511,266 two-port probe rows (main.tex lines 1082–1134).

**Required remedy.**

1. Correct equations (4)–(5), their proof, the quartet proof narrative, and
   every statement that binds the abstract F/G family to literal coordinates.
2. Add an independent symbolic test that derives all three split pullbacks
   from the article's own (0,C,G,T), (1,s,g,s) convention and proves the
   zero/strict-sign identities over the stated domain.
3. Add a convention mutation that swaps which character has eigenvalue g and
   fails for the intended formula-level reason.
4. Regenerate the article PDF, supplement/crosswalk if their hashes or
   narrative bindings change, all manifests and release locks, and the handoff
   seal.  The graph ledgers need not be recomputed if a new semantic verifier
   proves that their stored displayed-set predicates bind to the corrected
   family; they do require revalidation and resealing.

## Claim matrix

| # | Claim and location | Status | Independent mathematical evidence | Exact remaining gap |
|---:|---|---|---|---|
| 1 | Network class, admissible rootings, weak/strong tree-childness, fixed mixed graphs, restrictions, ordinary triangles; main.tex 201–299, PDF pp. 3–4 | **PASS** | Checked degree conventions, one-step root suppression, no-omnian criterion in both directions, and that triangle redirection preserves the underlying labelled graph while transporting ports coherently. | No mathematical gap found. Exhaustive rooting computations belong to individual certificates. |
| 2 | Fourier inversion, D_plus, subdivision, root movement; main.tex 300–413, PDF pp. 4–6 | **PASS** | Independently inverted (1,s,g,s), obtaining f0=(1+2s+g)/4, fC=fT=(1-g)/4, fG=(1-2s+g)/4. Strict positivity is exactly D_plus. The near-identity subdivision and switching-by-switching root movement are valid, including the reticulation-adjacent stem case. | None found within the stated strict component. |
| 3 | Quartet and tree-sunlet pointwise separation, decorated tree of blobs; main.tex 414–523, PDF pp. 6–7 | **FAIL** | The literal quartet equations fail by the exact counterexample above. Independently replacing G by C repairs the separator theorem. Independently expanded the sunlet map and reproduced the printed T_i factorization and strict negative sign. Englander v4 pp. 10, 12–13 and 22 support the attributed general theorem under its G/T convention. | Correct and reseal the submission's failed C/T specialization and bind it to a formula-level replay. |
| 4 | Complete two-sector bridge fibre; main.tex 524–681, PDF pp. 7–9 | **PASS** | Positive rank-one cut blocks give one scalar per sector; all-zero normalization fixes sector zero; C/T invariance forces equality of paired scales; G remains independent. The degree-at-least-three anchor matrix has rank d, the normalizers are analytic, and a tree has no holonomy. Near-identity three-edge subdivision supplies the physical local product. | Confidence is moderate-high because the conclusion is local on model charts; no omitted continuous gauge was found. |
| 5 | Paired marginal products, physical sections, switching signatures, invisible coordinates and parent complements; main.tex 684–767, PDF pp. 9–10 | **UNVERIFIED** | The product map is closed and surjective on D_plus, rank two, and has a local section. The visible-signature factorization and the rule that lambda is complemented only after a certified parent-order reversal are mathematically correct. | Completeness and correctness of every stored graph transport and signature are finite computational claims not established by this track. |
| 6 | Semialgebraic localization, finite choices, no compensation, fixed-full restoration; main.tex 769–835, PDF pp. 10–11 | **UNVERIFIED** | Cell-dimension argument, bridge extraction, and fixed-full quantifiers are sound. The proof never lifts an abstract marginal relation or inverts a target deletion map. | It is conditional on the child generator actually containing the unique child induced by every fixed full relation and on all children being separated. |
| 7 | Cycle/theta core reduction, four event placements, exclusions and repairs; main.tex 837–992, PDF pp. 11–14 | **PASS** | Degree excess gives a cycle for r=1 and three internally disjoint pole paths for r=2. Reticulate-pole, same-path and directed-cycle exclusions yield exactly theta0–theta3. Independently took minimal transversals of every no-omnian clause family and reproduced the repair table. | No hand-proof gap found; raw implementation coverage is a computational matter. |
| 8 | Ordered words, sink/dummy roles and C(k,epsilon) counts; main.tex 994–1028, supplement.tex 141–230 | **PASS** | Independently evaluated the binomial formula. Core subtotals are [7,100,100,416,208] for C(4,1), [9,210,210,1036,518] for C(4,0)=C(5,1), and [11,392,392,2240,1120] for C(5,0), giving 831, 1,983 and 4,155. | Correct implementation of every descriptor remains part of the computational audit. |
| 9 | Certificate semantics and finite partitions; main.tex 1030–1153, PDF pp. 14–16; certificate appendix | **FAIL** | Rank-upper/source-minor and target-zero/source-witness implications are mathematically sound in the abstract; labelled isomorphism and triangle terminals have the right direction. The quartet certificate body's advertised semantics are false as printed. | Independent exhaustive generation and exact replay of all non-quartet certificates are required; quartet coordinate semantics must be fixed first. |
| 10 | PC-PARTIAL boundary; main.tex 1155–1191, supplement census/crosswalk | **PASS** | The text explicitly retains direction-specific polynomial bodies, 75 rank representatives, 997 parents, exceptional restoration/probe ledgers, and does not equate literal polynomial-body equality with graph orbit equivalence. | Whether every retained item is correct is computationally unverified here, but the logical boundary is honestly stated. |
| 11 | Rank-nine ordinary-triangle common germ and contextual gluing; main.tex 1193–1319, PDF pp. 16–17 | **PASS** | Independently differentiated the sunlet map at the strict CT symmetric point. Reproduced all six pair coordinates 1/12, three mixed triples 1/48, the exact 4x4 and 5x5 blocks, determinants -1/2 and -1/4, and rank nine. The proof correctly uses submersion/constant rank, not a square inverse, handles all triangles simultaneously, and gives valid D_plus bridge inequalities. | None found. |
| 12 | Both implications in K2P-SAME and absence of proper one-way containment; main.tex 1321–1352, PDF pp. 17–18 | **UNVERIFIED** | The implication from coherent triangle transport to a common germ and hence two directed relations is proved. The converse assembly is logically valid conditional on pointwise recovery, bridge localization, bounded classification and probe coherence. | The printed quartet premise fails and the load-bearing finite bounded theorem is unverified in this track. |
| 13 | Generic identifiability and proper exceptional set; main.tex 1354–1467, PDF pp. 18–20 | **UNVERIFIED** | Independently checked irreducibility, equality of generic complex rank and maximal physical rank, r<=n-1, the 4n-3 vertex bound, finiteness, rank-drop image dimension, Nash target sections, and real-to-complex dimension logic. Each exceptional component is proper. | The argument is conditional on the global K2P-SAME theorem; hence the theorem cannot presently receive unconditional PASS. |
| 14 | Exact reconstruction; main.tex 1469–1527, PDF p. 20 | **UNVERIFIED** | Exact-real/quantifier-elimination assumptions are explicit; all unresolved candidates are retained until assembly; membership is decided by triangle class; the depth and finite loops terminate; the stated bounded restriction count is O(n^9). | Conditional on corrected quartet signs and complete finite restoration/probe evidence. No bit-complexity, stability or finite-sample claim is silently introduced. |
| 15 | Strict continuous-time classification; main.tex 1529–1577, PDF pp. 21–22 | **UNVERIFIED** | Derived D_CT exactly as 0<s<1, s^2<g<1. Power roots stay in D_CT; the maximal rank agrees on the open cone; the triangle witness is CT; and the interval Ls^2<g<U makes both bridge sections CT. | The transfer of the main classification remains conditional on repairing and verifying its principal-domain premises. |
| 16 | Weak-class 4n-3 sharpness; main.tex 1579–1788, PDF pp. 22–24 | **PASS** | Independently regenerated rootings, graph non-equivalence, both four-switch tensors, strict rational CT checks, named Jacobian determinants, cherry inverse and the +4 dimension induction. Details follow below. | No gap found. |

### Dependency impact of C02

The following distinction is important for the final combined review:

- C02's **general external theorem is supported**, but the submission's
  literal specialization and exact-artifact binding are **FAIL**.
- If the separate computational audit establishes C04–C10, then C11
  (global K2P-SAME), C12 (continuous-time classification), the genericity
  theorem and reconstruction remain **UNVERIFIED solely because C02 is
  broken**.  Their internal analytic arguments introduce no additional gap
  found by this review.
- Before importing the computational result, C11 also remains conditional on
  the finite bounded classification, restoration and probes.  I therefore do
  not misdescribe C02 as the only currently unverified premise in this
  mathematical-only track.
- The D_plus/continuous-time domain lemmas, bridge fibre, triangle common
  germ, primitive count formula and weak-sharpness theorem do not depend on
  the faulty coordinate specialization and retain their PASS statuses.

## Detailed independent checks

### 1. Domain, subdivision and marginal products

The inverse Fourier transform at main.tex lines 308–313 is correct.  Because
s>0 and g>0 are imposed separately, f0 is automatically positive; fC=fT>0
is equivalent to g<1; and fG>0 is equivalent to g>2s-1.  This gives exactly
the claimed connected component D_plus.

For two serial factors, with S=s1 s2 and G=g1 g2, the only nontrivial closure
case is S>1/2.  Then

    G > (2s1-1)(2s2-1)
      = (2S-1) + 2(1-s1)(1-s2) > 2S-1.

The fixed-r construction at main.tex lines 705–714 is valid because
max{S,G,2S-G,0}<1.  Its two output differential rows have disjoint support.
For continuous time, coordinatewise positive power roots give
G^(1/m)>S^(2/m), so the same section remains physical.

Boundary-near checks were kept exact: none of the above uses floating-point
sampling.  The quartet counterexample itself lies strictly in D_CT.  The
triangle witness uses (s,g)=(1/2,1/2) and (1/3,1/3), both strictly above
g=s^2.  Every weak-sharpness diagonal edge (x,x) has rational 0<x<1 and hence
x^2<x.

### 2. Whole-map tree-sunlet sign

Starting from

    q_xyz = a_x b_y c_z [delta f_y d_z + (1-delta) f_x e_z],

I substituted the nine three-leaf orbit coordinates directly into
T_3=V^2 X_g-X_s^2 Y_g Z_g.  After cancelling the common positive monomial,
the residual expression factors exactly as

    -delta(1-delta)d_g e_g (1-f_g)^2.

This reproduces main.tex lines 485–515.  It is a whole-map identity and does
not require the revoked rooted tree/sunlet restriction oracle.

### 3. Bridge fibre and physical gluing

Fixing a bridge character gives a positive rank-one flattening block.
Comparing two factorizations yields one positive cut scalar in each sector.
Normalization fixes the zero sector.  Marked anchors force c(C)=c(T);
unmarked degree-d anchors give rho_e rho_f=1 for all pairs, and d>=3 plus
positivity forces every rho_e=1.  In one sector, the exponent vectors for
(1,2),(1,3),(2,3),(1,4),... span all d incidence coordinates, with leading
determinant -2.  Formula (8) therefore gives real-analytic positive
normalizers.  Peeling a bridge tree introduces no cycle on which holonomy
could remain.

The principal-domain simultaneous gluing at main.tex lines 1307–1318 is
valid: taking every relevant s below 1/2 makes g>2s-1 automatic before and
after incidence rescaling.  The continuous-time construction at lines
1557–1573 is also valid.  From s<sqrt(U/L) follows Ls^2<U, so a rational or
real g exists strictly between them; the definitions of L and U imply the
two rescaled inequalities.

### 4. Primitive cores and exact completion arithmetic

The identity sum(deg_B(v)-2)=2(r-1) proves that an r=1 nontrivial block is a
cycle and an r=2 block has precisely two degree-three poles joined by three
internally disjoint paths.  The local source and two reticulation events then
give the four theta placements described at main.tex lines 897–927.  I
separately computed minimal hitting sets of the obstruction clauses:

| Core | Independent minimal repairs |
|---|---|
| cycle | {0}, {1} |
| theta0 | {2,3}, {3,4} |
| theta1 | {2,3}, {2,4} |
| theta2 | {2,3}, {2,5}, {3,4}, {4,5} |
| theta3 | {2}, {4} |

Using only the five tuples (m,q,r)=(2,1,1),(5,1,2),(5,1,2),(6,2,4),
(6,2,2), I independently obtained:

| Count | Per-core contributions | Total |
|---|---|---:|
| C(4,1) | 7, 100, 100, 416, 208 | 831 |
| C(4,0) | 9, 210, 210, 1,036, 518 | 1,983 |
| C(5,1) | 9, 210, 210, 1,036, 518 | 1,983 |
| C(5,0) | 11, 392, 392, 2,240, 1,120 | 4,155 |

This validates the mathematical count compression, not the assertion that
every raw implementation record is present exactly once.

### 5. Localization, restoration and probes

The localization proof has the correct quantifiers.  It starts from one
actual full relation, restricts a source product box, chooses one target type
from a finite semialgebraic cover, and uses an intrinsic bridge quotient to
block remote compensation.  Fixed-full restoration then follows the actual
omitted label, actual source insertion, actual target attachment and actual
transport.  It does not promote a relation seen on an arbitrary marginal and
does not invert a target deletion map.

The arbitrary-word proof is sound conditional on its finite premises.
One-port comparisons identify the segment/site of each label; two-port
comparisons determine pairwise order on a shared directed segment.  Because
the rows arise from actual words, these orders are transitive, and coherent
overlap restrictions assemble a unique word modulo licensed automorphisms and
ordinary-triangle orientation.  The exact completeness of 997 parents,
36,824 restoration edges, 176 anchors, 2,206 sites and the one-/two-port
ledgers is not a prose theorem and is left UNVERIFIED here.

### 6. Ordinary triangle germ

I differentiated the printed sunlet map without using the stored rank
certificate.  At the symmetric point of main.tex lines 1211–1214, all six
normalized pair coordinates are 1/12 and the three mixed triples are 1/48.
The symmetric and anisotropic derivatives are exactly the displayed matrices
J_0 and J_perp; their determinants are -1/2 and -1/4.  There are nine
nonconstant K2P orbit coordinates, so rank nine is maximal.

The conclusion correctly uses the analytic submersion theorem.  It does not
try to invert a square parameter Jacobian.  The contextual proof chooses one
constant-rank chart after taking the product of all triangle output
neighborhoods, so it avoids an invalid induction that could lose genericity
after each replacement.

### 7. Genericity and reconstruction

The polynomial image closure is irreducible.  A nonzero generic complex
Jacobian minor cannot vanish on the nonempty real-open physical domain, so
maximal physical rank equals generic complex rank.  The tree-child path
argument gives r<=n-1; degree balance gives t=n+r-2 and at most 4n-3 rooted
vertices, hence finitely many labelled competitors.

The proof correctly removes the total source rank-drop image, not only one
minor's zero set.  Nash stratification bounds that image by d_N-1.  If a
competitor intersection had physical dimension d_N, a full-rank stratum of
the target incidence correspondence would supply a real-analytic target
section, giving forbidden directed containment.  Real semialgebraic
dimension, real Zariski closure dimension and complexification then show that
each competitor component is proper.  Irreducibility prevents the finite
union from filling V_N.

Reconstruction is explicitly an exact-real decision procedure.  It retains
all candidates through global assembly and decides membership only after
grouping by triangle class.  Quantifier elimination proves termination but
not bit complexity or stability.  Its O(n^9) bound concerns bounded
restrictions in addition to reading the 4^n-entry tensor.  These arguments
are correct conditional on the main classification and finite ledgers.

### 8. Independent weak-sharpness reconstruction

I rebuilt the three-leaf pair from the arc lists at main.tex lines 1594–1601,
without importing the atlas or its canonicalizer.

1. Enumerating admissible root insertions gives (5 admissible, 2 tree-child,
   3 non-tree-child) for W and (7,2,5) for W'.  Thus each graph is weakly but
   not strongly tree-child.
2. The labelled underlying-graph leaf distances (d01,d02,d12) are (4,4,3)
   for W and (3,4,4) for W'.  Hence there is no labelled graph isomorphism.
   Triangle redirection preserves the labelled underlying graph, so the pair
   is not triangle-equivalent.
3. Directly summing the four reticulation switchings gives the normalized
   orbit tensors

       W:
       (1, 64009/457492, 64009/457492, 6400/39229939,
        1/1372, 4048/39229939, 4048/39229939,
        6400/39229939, 4048/39229939, 1/1372)

       W':
       (1, 15/1024, 15/1024, 5/512, 27/512,
        9/4096, 9/4096, 5/512, 9/4096, 27/512).

   After multiplying by the stated rational pendant factors, both give
   q000=1, the six pair coordinates delta^2, and the three mixed coordinates
   (4/5)delta^3.
4. Independent symbolic differentiation of the named columns and rows
   reproduces the two nonzero determinants

       10368019213741323 /
       563981315074464023964442388464888915634290688

   and

       1435825 / 85002596691653613846528.

5. The cherry observables recover u_s,v_s,u_g,v_g.  Their determinant is
   4u_su_g/(v_sv_g), equal to 2464/675 at the printed test pairs.  The new
   tensor factors through the old tensor plus four edge coordinates, giving
   both the upper and lower increment of four dimensions.  Iteration gives
   9+4(n-3)=4n-3.
6. Pruning the newest cherry returns the base graph, so level, weak-not-strong
   status, nonisomorphism and non-triangle-equivalence persist.

This is the strongest fully independent theorem-level verification obtained
in this review.

## Finite classification: exact status

The finite theorem has a clearly stated mathematical universe and decision
order:

- primitive cycle/theta graph encodings;
- source/target incoming modes, selected and dummy roles, ordered port
  permutations, direction and boundary transport;
- pointwise sign, symbolic rank, exact polynomial, fixed-full restoration,
  isomorphism, or triangle terminals in fixed precedence;
- restoration of arbitrary omitted labels under one fixed full relation; and
- one-/two-port reconstruction of arbitrary subdivision words.

The finite universe and certificate semantics are not replaced by the
PC-PARTIAL compression.  That is a sound design.  Nevertheless, a prose read
cannot establish the millions of raw records, symbolic pullbacks, canonical
classes, 997 parents or 544,571 two-port rows.  Stored values such as
corrected_universe_certificate.json
(c80c8781b968b21e1b001d51b6e71650ee74a326bb8b3f0aa56fc5997c224663),
corrected_restoration_forest.json
(43bd2be5e7626a954fc4fa4cf45e8d0e6483c947ddc9cba80f2b1a13351bc3a8),
and probe_coherence_certificate.json
(93de7b0dd3aa581bdf12288eae8cb9ac42f20a9d9bb3eab35eee8ef9a759d390)
are computational evidence, not mathematical premises.  Their status must be
taken from a successful independent code/execution audit after the quartet
semantic repair.

## Literature and attribution audit

This search was targeted and non-exhaustive; it is evidence, not a priority
guarantee.

- Huber et al., “When Are Quarnets Sufficient to Reconstruct Semi-Directed
  Phylogenetic Networks?”, supports the two undirected level-2 generator
  classification invoked in the core reduction:
  https://link.springer.com/article/10.1007/s11538-025-01510-5
- Englander et al., “Identifiability of Phylogenetic Level-2 Networks under
  the Jukes–Cantor Model”, supports in substance the displayed-quartet
  separation and tree-of-blobs implication.  Crucially, its K2P notation uses
  the G/T equal sector, explaining but not curing the submission's convention
  mismatch:
  https://doi.org/10.1101/2025.04.18.649493
- Brits et al., “On Tree–Network Distinguishability and Full Identifiability
  of Phylogenetic Networks”, concerns full identifiability at level 1 modulo
  triangle phenomena and does not subsume the claimed level-2 K2P theorem:
  https://arxiv.org/abs/2607.12919v2

The bibliographic metadata inspected in references.bib are internally
consistent with these records.  I did not obtain an exhaustive novelty or
priority guarantee.  The exact Englander version-4 numbering was checked
directly: Proposition 2.9 and equation (2), Proposition 2.10 and equation (3),
Theorem 2.11, and Corollary 2.12 occur on PDF pp. 12–13, with the full
Proposition 2.10 calculation on p. 22.  The current official PDF byte hash
does not equal the different locally reviewed hash asserted in
work/adversarial_proof_review/TOPOLOGY_DIRECTIONAL_THEOREM.md line 73; that
rendition difference is a provenance question, not a reason to doubt the
theorem text just inspected.

## Scope audit

The manuscript consistently restricts its central claim to binary standard
semi-directed strongly tree-child level-2 networks, strict inheritance
probabilities and the positive-eigenvalue D_plus component.  It does not
claim mixed-sign, boundary, singular-edge, higher-level, weak-class
identifiability, conditioning, numerical stability, bit complexity,
finite-sample inference, or equality of complete stochastic images.

The continuous-time result is a restriction to the strict cone, not a
boundary theorem.  The weak construction proves sharpness by producing a
full-dimensional ambiguity family; it does not assert that every weak
network is ambiguous.  No scope inflation was found.

## Minimal ordered actions

1. Correct the literal quartet separators to the C/T equal sector in the
   article and authoritative proof narrative.
2. Add a symbolic, convention-aware pullback verifier and mutation test; do
   not count the existing seven-subset logic replay as that verifier.
3. Revalidate every displayed-quartet terminal binding against the corrected
   theorem.  If ledger rows contain only graph displayed-set data, document
   why their counts and graph hashes remain unchanged.
4. Complete the independent full finite-universe, restoration and probe
   execution/code audit.  Any layer not actually regenerated remains
   UNVERIFIED.
5. Regenerate affected PDFs, crosswalk entries, reports, manifests and
   release locks; reseal the handoff.
6. Only after steps 1–5, promote the main theorem, genericity,
   reconstruction and continuous-time classification from HOLD/UNVERIFIED to
   PASS if no further defect appears.

Human metadata and release choices are outside this mathematical HOLD and
should not be used to strengthen or weaken the scientific verdict.
