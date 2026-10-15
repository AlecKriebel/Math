# Algebra/groups batch 2 candidates

Checkpoint 2026-10-06 21:48 America/Los_Angeles. Scope triage completion estimate 90%; upstream validity and full priority audit not undertaken. Sources read directly; recommendations conditional on their stated theorems.

## 1. Positive-characteristic Kaplansky idempotent conjecture — recommended

**Exact target.** A finitely presented torsion-free G with a finite two-dimensional classifying space has a nontrivial idempotent in F_2[G]. Same holds after every characteristic-two field extension. Exhibit nonzero cyclic projective P with R ≅ R ⊕ P, hence [P]=0 in K_0(R).

**Input:** family197, `A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026/build/sections/introduction.tex`, main theorem: ab=1, ac=0, c≠0. Let e=1−ba; e²=e, e≠0, e≠1. Take P=eR. The direct sum R=baR⊕eR and maps r↦br, x↦ax identify baR with R. This is a precise cancellation failure, not merely an unsupported K-theory inference.

**Gap:** essentially only extraction of source coefficients and group presentation, maps/certificate checks, priority attribution. Characteristic0 is specifically excluded by family207, so this does not refute the Kadison–Kaplansky C*-algebra conjecture. Do not infer Farrell–Jones, hyperlinearity, or characteristic-zero non-direct-finiteness.

**Novelty search:** source197 contains no idempotent corollary; catalogue idempotent entries confined to characteristic0 family207. Lean197 scope covers earlier torsion example, not this newer torsion-free theorem. A formalization claim requires new work.

**Impact:** 8.8–9.0 under user's theorem-impact metric; independent publication novelty low because inference is elementary. Primary background: https://arxiv.org/abs/1904.04847 and https://www.mfo.de/occasion/2211/www_view (original search result https://publications.mfo.de/bitstream/handle/mfo/3944/OWR_2022_11.pdf?isAllowed=y&sequence=4).

## 2. C*-simplicity of Thompson F, T, Aut(F), Comm(F) — recommended

**Exact target.** Reduced group C*-algebras of F, T, Aut(F), and abstract Comm(F) are simple (and have unique tracial states). More generally any countable circle-homeomorphism overgroup containing the standard copy of F is C*-simple; corresponding line-action version uses specified standard embedding.

**Input:** family248 nonamenability of F, plus Le Boudec–Matte Bon `Subgroup dynamics and C*-simplicity of homeomorphism groups`, Theorem4.1, Corollary4.2, Theorem4.3, Corollary4.4. Direct primary PDF checked: https://www.numdam.org/item/10.24033/asens.2361.pdf pages27–28 (printed581–582). Theorem4.1 DOES say containing F, not T. Cor4.4 treats Aut(F) and Comm(F).

**Gap:** short theorem chain; hypotheses match exactly. Unique trace can be added via standard general theorem C*-simplicity implies unique trace. V already C*-simple independently, so do not include V as new.

**Novelty search:** family248 intro cites only older implication C*-simplicity T⇒nonamenable F; its consequences section contains unitarizability/percolation, no reverse C*-simplicity result. No LeBoudec/MatteBon reference in family248. Broad manuscript references search found no relevant matching consequence. Primary equivalence is long established, and credit belongs there plus upstream.

**Impact:** 8.0; very high tractability. This package settles a recognizable operator-algebra question for canonical groups, but adds no new general C*-simplicity mechanism.

## 3. Sperner property for all graded Artinian complete intersections in characteristic zero — recommended

**Exact target.** For standard graded A=k[x_1,...,x_n]/(f_1,...,f_n), homogeneous regular sequence, char(k)=0, the Dilworth number max_{I⊂A} μ_A(I) equals max_j dim_k A_j. Equivalently, the largest minimal generator count of an ideal equals the largest coefficient of ∏_i(1+t+...+t^{deg f_i−1}). The maximum covers all ideals, via graded reduction. Remove linear regular-sequence elements before applying upstream statement degrees≥2.

**Input:** family200 EGH characteristic0 corollary in `Commuting-Division-Coefficient-Forms-and-the-Artinian-Eisenbud-Green-Harris-Conjecture-September-23-2026/build/sections/01-introduction.tex`, cor:characteristic-zero. Combine Harima–Wachi–Watanabe Theorem11, https://arxiv.org/html/1601.06928 (published Proc AMS 145(4), DOI10.1090/proc/13347). Their matching-property route transfers the pure-powers ideal shadow inequality to every CI and then gives Sperner.

**Gap:** no central new proof step. Audit arbitrary ideals, field descent, and degree-one elimination. Do NOT claim weak or strong Lefschetz: Sperner is weaker and does not imply them. Do NOT extend to positive characteristic or nongraded complete intersections without work.

**Novelty search:** no Sperner mention in either family200 manuscript, nor global catalogue; corpus-wide tex search only unrelated thin-tree/Tingley sources. Source200 does already contain local cohomology and quadratic Cayley–Bacharach applications: exclude those.

**Impact:** 8.0, high tractability. Named complete-intersection conjecture, major niche theorem, conditional reduction already published.

## 4. Sharp Gram-rank bounds on strictly positive SOS boundary — secondary

Family200 also supplies EGH hypothesis in Laplagne–Valdettaro, https://arxiv.org/html/2012.05951 Theorem3.17 (version numbering differs from old v1). For homogeneous f>0 away from0 on boundary of SOS cone Σ_{n,2d}, every Gram matrix has rank ≤ binom(n+d−1,d)−C(n,d,2d), where C=6 if d=2,n≥4 and C=3d−2 if d≥3,n≥3; trivial Hilbert cases must be excluded. Hence every decomposition into linearly independent degree-d forms has at most that many squares. Their Section4 supplies sharpness examples. Need verify source final version's constructions/exceptions before promoting “sharp for all”. No family200 mention of Laplagne/Valdettaro. This is an established conditional theorem, not newly invented bound. Impact7.7–8.0, immediate theorem-chain, perhaps bundle with Sperner as an EGH application paper.

## 5. Veronese secant-index sequences — secondary

Family200 EGH supplies exactness of Jorgenson's combinatorial lower bounds for secant-index sequence of every Veronese variety. Primary https://arxiv.org/abs/2003.08481 / https://arxiv.org/html/2003.08481 states the implication. Secant indices here mean maximal cardinalities of finite reduced linear sections of each dimension, not generic secant variety dimensions or tensor ranks. Exact algorithm/formula and theorem hypothesis still require extraction. Impact7.3–7.7; straightforward but narrower. No Jorgenson/secant-index mention in family200 sources.

## Rejected / deprioritized

- Bass⇒homotopy idempotent fixed-point theorem: already explicitly in family207 sections01/09.
- Hyperbolic one-relator hereditary conjugacy separability, virtual retractions and profinite cohomology: already explicitly in family258 section11.
- Standard nonamenable critical percolation exponents: explicitly in family214 consequences. Slightly-supercritical tails via Hutchcroft2022 may be unstated, but source already cites/uses same theorem and it is a weak novelty candidate.
- Cannon⇒carpet classification and wreath Hopfian consequences: user has existing efforts; excluded as requested.
- Single-fold Diophantine unique-solution height impossibility: clear but lower impact/existential extraction; prior notes retain details.
