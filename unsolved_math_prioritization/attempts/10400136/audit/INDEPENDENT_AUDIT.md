# Independent adversarial audit: Ohtsuki Problem 7.21

**Target:** 10400136 / AMR-103-0136, rank 507  
**Audit date:** 3 October 2026 UTC  
**Verdict:** **PASS — partial analysis / unsolved after five approaches**  
**Not certified:** a solution, a new invariant, a QHI counterexample, or mathematical novelty.

## 1. Scope, independence, and freeze

This review began after the author-stage freeze. The reviewer did not author the package or assist its source research. All ten files listed by the frozen author manifest were read, and their sizes and SHA-256 hashes were independently verified. Including the manifest, the freeze contains eleven files. Its hashes were unchanged after verification.

The author verifier was copied to temporary storage before execution because it writes `exact_results.json`. The frozen version was not executed in place or edited. The reproduced JSON agrees with the frozen result. The additional verifier, results, and this report are separate audit artifacts.

The review challenged: the exact original target; whether modern results settle it; the five algebraic arguments; the applicability of local calculations to global state sums; composite odd orders; zero-state-sum cases; phase versus sign; and the comparison and surgery hypotheses in the tangle route. The literature check was extended to categorical state sums absent from the author bibliography. No source PDF, extracted paper, imported corpus, or private context is included in the audit deliverables.

## 2. Original target and normalization guard

The target is correctly identified. Ohtsuki §7.4 begins with closed oriented W, nonempty L, a flat B-bundle on W, B the upper-triangular subgroup of SL₂(C), and odd N>1. Problem 7.21 asks for an explanation of the Nth-root ambiguity and possibly an extra-structure refinement. The relevant pages are printed 485–486, PDF pages 113–114. The volume date and the article’s June 2004 publication date are distinct. [Ohtsuki, original source](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).

For full distinguished decorated triangulations, equation (7) of *QHI Theory I* includes both vertex and cocycle-edge normalizations. Theorem 5.2 states invariance of H(T_N) modulo μ_N and defines K_N=H(T_N)^N. Thus the author’s starting identity is exact in that convention, including independence from root determinations. It is not a general assertion identifying every later invariant called H_N or K_N. [Baseilhac–Benedetti, Theorem 5.2, p. 29](https://arxiv.org/pdf/math/0201240).

An additional normalization warning is useful: the later PSL₂(C) construction uses different symmetrization factors, and its Remark 4.31 explicitly explains the cocycle-dependent scalar separating the earlier B-valued construction. This supports the audit’s insistence that a future comparison prove the original power identity with its original normalizations. Merely sharing the name QHI is insufficient. [Baseilhac–Benedetti, Remarks 4.30–4.31](https://imag.umontpellier.fr/~baseilhac/QHI1_TOP.pdf).

## 3. Source-theorem checks

### 3.1 The 2015 sign result

The paper defines “cusped manifold” here to have exactly one cusp. Theorem 1.1 uses a canonical Zariski-open subset of the geometric component of the augmented PSL₂(C)-character variety and compatible bulk/boundary weights. Its part (3) replaces μ₂N by μ_N if N≡1 mod 4, or if N≡3 mod 4 and the bulk c-weight vanishes. Proposition 8.2 removes the weight restriction for patterns definable using branched triangulations. Neither selects an Nth-root phase. Theorem 8.4 and equations (66)–(68) explicitly leave a scalar C with C^N=1 after determinant normalization. The author’s use is accurate. [*Analytic families*, Theorem 1.1 and §8](https://msp.org/agt/2015/15-4/agt-v15-n4-p05-s.pdf).

### 3.2 Non-ambiguous structures

Theorem 1.6 concerns an actual QH triangulation of a compact connected oriented manifold with nonempty torus boundary; part (2) requires a connecting sequence of lifted non-ambiguous QH transits. Corollary 1.8 concerns rich triangulations in the cusped setting and retains μ₄N. Corollary 1.11 requires that the character be represented on an ideal-triangulation gluing variety; it normalizes the symmetry defect modulo μ₄. These conditions cannot be omitted when treating arbitrary characters.

For closed pairs, Proposition 1.13 and §8.7 are decisive: normalized defects equal one modulo μ₄, and relative-taut reduced invariants do not distinguish the added relative-taut structure. Non-normalized defects can fail to be well-defined. The author correctly does not infer that all conceivable geometric refinements are impossible. Equation (8) and the following definition agree with every local convention used in Attempt 3. [*Non ambiguous structures*, Theorem 1.6, Corollaries 1.8/1.11, Proposition 1.13, §§8/8.7](https://arxiv.org/pdf/1506.01174v2).

### 3.3 The 2026 comparisons and asymptotics

Garoufalidis–Yu work with a punctured surface of negative Euler characteristic and a suitable generic character admitting a mapping-class-invariant decoration. Their main comparison does not cover the original arbitrary closed triple. Remark 3.12 explicitly retains μ_n for the BB operators and numerical invariants. [Garoufalidis–Yu, §1.2 and Remark 3.12](https://arxiv.org/pdf/2601.03554).

Baseilhac–Ben Aribi treat the figure-eight complement and its geometric character component. Their introduction retains μ₂N, while equation (76) permits μ₄N in the defect/reduced-state-sum factorization. This is evidence about conventions in that family, not proof that no phase refinement exists elsewhere. [Baseilhac–Ben Aribi, p. 2 and §3.3](https://arxiv.org/pdf/2604.16077).

McPhail-Snyder v3 is dated 15 May 2026. The introductory knot formulas concern oriented framed knots, decorated SL₂(C) representations, and chosen log-meridians. Equations (1.1) and (1.3) have the multipliers and shift sizes used in Attempt 5. Section 1.6.1 presents equivalence with BB after a Chern–Simons-root normalization as an expectation. Section 1.2 leaves general-manifold surgery extension for future work. A theorem about unambiguous tangle operators does not supply either missing comparison. [McPhail-Snyder, §§1.1–1.2 and 1.6.1](https://arxiv.org/pdf/2509.02365v3).

### 3.4 Additional adversarial source lead: categorical phase-free invariants

The original gate omitted a relevant older branch. Baseilhac–Benedetti’s 2011 Remarks 2(3), p. 62, discuss categorical invariants of closed triples which may have no phase ambiguity, and caution that their exact relationship to BB/Kashaev state sums requires investigation. The same paper’s equation (2) also changes a vertex normalization from N^(-V) to N^(-(V−2)) to normalize the unknot. Consequently an apparent comparison cannot be read independently of conventions. [*The Kashaev and quantum hyperbolic link invariants*, §2.2 and Remarks 2](https://people.dm.unipi.it/benedett/JGGT.pdf).

The primary papers resolve the apparent contradiction. GKT Theorem 29 only gives invariance up to integer powers of a scalar q̃, and retains a charge cohomology class. Its Borel example, Theorem 50, has q̃=(-1)^((N−1)/2)ζ^(-(N²−1)/8). This is not one: its order is N for N≡1 mod 4 and 2N for N≡3 mod 4. The introduction explicitly leaves the precise BB relationship unclear. [Geer–Kashaev–Turaev, Theorems 29/50](https://arxiv.org/pdf/1008.3103v2).

In contrast, Geer–Patureau-Mirand Theorems 20–21 use the Ψ-system specifically induced by a relative G-spherical category with the stated basic data. For that system q=Id, its generalized Kashaev invariant equals its modified TV invariant, and the charge-class ambiguity disappears. This is a genuine phase-free theorem, but it does not identify that scalar with the original B-valued BB H(T_N), with its edge normalization, or prove its Nth power equals the original K_N. [Geer–Patureau-Mirand, §3.6](https://arxiv.org/pdf/1009.4120v3).

**Effect on verdict:** nonblocking bibliographic addendum. Broad references to retained phase ambiguities must be read as referring to the specified BB families, not every related categorical invariant. The author already makes no universal nonexistence claim and insists on the missing comparison. No inspected source establishes the full claimed target. This remains a bounded source conclusion, not a proof of open status.

## 4. Mathematical audit of all five approaches

### Attempt 1: determinant normalization and projective cocycles — PASS, diagnostic only

Taking determinants in A=λB with A,B of dimension d and determinant one gives λ^d=1, exactly as stated. It gives no preferred λ. A nonzero functional can fix a scalar at one point, but cannot establish compatibility over all parameters and all identities. The trace caveat is necessary.

For odd N, the cyclic shift X has determinant one, and the clock Z has determinant ζ^(N(N−1)/2)=1. Both traces vanish. Evaluating on a basis gives ZX=ζXZ and the multiplier ζ^(bc) for X^a Z^b X^c Z^d. A scalar rephasing cancels from the commutator, so cannot trivialize this projective representation. The displayed cocycle identity is correct for composite as well as prime N.

The independent verifier checks matrices in the actual cyclotomic rings Z[ζ_N] for N=3,5,7,9,15; it does not rely solely on equality of stored phase exponents. In particular it computes the trace of Z as an exact polynomial residue. The countermodel invalidates a general determinant-only inference. It has not been embedded in a QHI move groupoid and cannot establish that the original anomaly is nontrivial.

### Attempt 2: root lifting and covers — PASS, conditional only

The covering-space criterion is correctly applied. The stated connected, locally path-connected hypotheses give path connectivity, and the assumed semilocal simple connectivity is more than is needed here, not an error. The subgroup condition is exactly K_*(π₁X)⊂N Z. After an initial root is fixed the lift is unique; a continuous lift of a holomorphic map is holomorphic by local-root comparison.

The circle example, the d-fold-cover divisibility test, and the failure of a power-of-two cover to kill primitive odd-order monodromy are correct. This does not say that any actual spin or framing construction is a cover of that type. The field criterion K∈(F*)^N is exact, while divisor-order divisibility alone need not settle it; the package avoids that false implication.

The root cover E_K is unramified only over K≠0, and the author states this restriction. It supplies no independent explanation of the state sum. No actual QHI parameter loop or nonzero locus is computed. The route is properly left unresolved.

### Attempt 3: local charge/flattening formulas — PASS, local scope only

Expanding the two quantum-root exponents cancels the εc₀c₁ terms identically, leaving equation (1). Recomputing roots when c changes gives equation (2). Holding the roots fixed would give a different expression; the author does not make that mistake. An even flattening increment gives the ζ^a quantum-root change and the ζ^[m(c₀a₁−c₁a₀)] symmetry change in equation (3). Since gcd((N−1)/2,N)=1, the particular local phase is primitive.

The example w=(2,−1,1/2), f=(0,−1,0) satisfies both the cyclic shape relations and the zero sum of log-branches with the stated principal branch. The old and new charges sum to one. Its nonunit modulus ratio is correct. There is no claim that this change satisfies a closed triangulation’s edge, weight, or charge constraints.

For an actual fixed triangulation, the even-increment edge and fixed-log-weight constraints form an integer kernel. The global product transforms by the displayed linear functional modulo N. For this product alone, vanishing on every allowed increment is necessary and sufficient. A correction of the full state sum requires the reduced contraction too. No C matrix, global kernel basis, closed-state computation, or actual anomaly is supplied. The text explicitly acknowledges each limitation; a synthetic local example has not been promoted into a global counterexample.

### Attempt 4: projected move-graph descent — PASS, conditional only

On the full graph of fully specified presentations with nonzero state sums, labels defined as actual ratios telescope. They are already a coboundary. Thus a loop test there cannot uncover a new obstruction; the base-state quotient is circular.

For a prescribed projected datum D, retaining loops, parallel edges, and oppositely labelled inverse moves makes the cycle-sum criterion equivalent to existence of a potential b. The standard path-integration proof is valid over Z/NZ even when N is composite. No field division or inappropriate linear-algebra rank argument occurs.

The projected three-state path really creates incompatible equations. The independent checks enumerate all potentials rather than reusing the author’s search algorithm. This also tests nonzero self-loops, conflicting parallel edges, and disconnected graphs. The package correctly separates a potential for a chosen graph from a geometrically natural normalization: presentation connectivity and coherence for a genuine structure remain hypotheses. It also restricts all ratios to the nonzero case.

### Attempt 5: Chern–Simons root cancellation and transfer — PASS, conditional only

With the representation and longitude eigenvalue fixed, iterating the classical one-step recurrence N times gives C(µ+N)=ℓ^(2N)C(µ). Transporting an Nth root by ℓ² is therefore consistent. Multiplication by this root cancels the quantum ℓ^(−2) multiplier exactly. The reciprocal root would leave ℓ^(−4), a useful sign check independently tested. Arbitrary independent root choices leave a μ_N factor. Nothing in this calculation provides unit-log-shift, framing, or filling invariance.

The root-lifting assertion requires a scalar function C on the stated parameter domain. Globally the classical object is naturally a line-bundle section; one must supply the log-decoration/trivialization/root-line data needed to enter that setting. The author’s hypotheses make the elementary lifting statement valid, and the transfer proposition explicitly requires coherent root transport. It must not be read as trivializing an arbitrary Chern–Simons line bundle automatically.

The conditional transfer proposition is logically sound. The exact move identity a_(p′)u_m v_m=a_p proves invariance of a_pr_pZ_p, while the separate power identity proves compatibility with the original K_N. Move connectivity and coherent transport are explicitly assumed. If the power identity vanishes then the refined scalar also vanishes, so the author’s zero case is correct. An equality only after Nth powers loses precisely the information sought.

A scalar knot-exterior comparison is insufficient for a general contraction or surgery sum. Powers do not distribute over sums, and relative phases survive that operation. Boundary-operator comparison, specified filling tensors, handle-slide/stabilization identities, and coverage of all original B-bundles remain unproved. This is a list of sufficient hypotheses, not evidence that those hypotheses have been established.

## 5. Exact controls and reproducibility

Run the audit with standard-library Python 3 from the repository layout:

```text
python audit/audit_controls.py
```

For another layout, pass `--author-dir` pointing to the frozen author directory. The script writes only its adjacent `audit_results.json` and its own temporary copy of the author verifier.

The author results reproduced exactly:

- 9,668 matrix products and 9,668 cocycle identities
- 5,000 charge cancellations and 2,500 even-flattening phase checks
- 20 graph, 224 cover-degree, and 164 peripheral controls

Additional independent checks passed:

- 3,125 cyclotomic matrix products and 389 scalar-rephasing pairs
- 3,645 six-coordinate cocycle checks
- 7,290 charge/flattening test pairs, checking multiple identities per pair
- 5 local non-phase/primitive-phase examples
- 881 exhaustively labelled triangles, 115 parallel-edge assignments, 12 graph edge cases
- 9,750 cover-monodromy cases, including negative winding
- 5,355 peripheral-orbit steps, including negative orbit indices
- 30 negative power-comparison/summation controls
- 50 checks of the additional GKT Borel scalar order

These finite checks audit implementations and countermodels. The elementary general arguments in §4 are the proofs of the conditional statements. Neither the counts nor the general algebra certify an actual QHI evaluation, realizable triangulation, move phase, boundary comparison, or surgery identity.

## 6. Disposition and publication limits

No blocking mathematical error was found in the five approaches. The source gate is materially strengthened by §3.4, which should accompany the package if it is shared. The original freeze need not be rewritten to add this separate audit.

The package may be promoted only as an AI-assisted, unrefereed investigation with five unfinished approaches and source-qualified elementary partial analysis. It may not be promoted as resolving Problem 7.21, proving intrinsic QHI phase nontriviality, or constructing a refined closed-triple invariant. Its subjective progress percentage is not a mathematical measurement. No novelty claim has been validated.

**Final disposition: PASS for the partial/unsolved package, with the categorical-literature addendum; the original problem remains unresolved by this work.**
