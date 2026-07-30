# End-to-end proof audit

## Verdict

**Mathematical verdict: PASS, with publication exposition repairs.**

The recovered source chain proves the following two claims:

1. For every bipartite Bell scenario with two measurement inputs per party and
   arbitrary finite output sets,
   \[
   \mathcal Q^{\mathrm{POVM}}_2(2,2)
   =
   \mathcal Q^{\mathrm{PVM}}_2(2,2),
   \]
   where both sets are convexified by shared classical randomness and the PVM
   side permits classical output postprocessing without increasing the local
   Hilbert-space dimension.
2. A rational \(3\times2\) Bell functional has a strict fixed-qubit
   POVM-over-PVM gap. Consequently \(3\times2\), up to exchanging the parties,
   is the minimum setting architecture for such a separation.

No load-bearing mathematical gap was found after rederiving D1, D2, D3, and
the final residual closure. Several arguments are too compressed for a paper;
publication-ready wording is supplied below. In this report, **REPAIRED** means
that the source argument is correct but the statement or proof should be
expanded using the supplied wording. It does not mean that a source artifact
was edited.

## Status key

- **PASS** — statement and proof are correct as written, apart from ordinary
  stylistic polishing.
- **REPAIRED** — the mathematical step is correct, but a missing case,
  convention, or logical bridge should be inserted explicitly.
- **UNRESOLVED** — not proved by the source chain or outside the theorem's
  claimed scope.

## Audited sources

### Phase-I / D1–D3

- `phase1_frozen_manuscript.md` (frozen staging source; its required
  arguments are consolidated into `paper/main.tex` and
  `paper/appendices.tex`)
  - operational model and convexification: lines 33–78;
  - D1 theorem: lines 82–142;
  - simple witness: lines 146–257;
  - strengthened witness: lines 261–370;
  - global PVM bound: lines 374–782;
  - locking theorem: lines 786–862;
  - D2: Theorem 10.1, lines 872–950;
  - filtering lemma and D3: lines 952–1045.
- `qubit_povm_pvm_separation_proof.md` (frozen staging source)
  — independent earlier presentation of the simple D1 witness and bound.
- `artifacts/three_by_two_separation/verify_exact.py`
  — canonical comprehensive exact D1 verifier copied byte-for-byte from the
  frozen source and covered by the release manifest.
- `qubit_povm_pvm_separation_verify.py` (frozen staging source)
  — independent exact verifier of the simple D1 witness.
- Coefficient CSVs and both strategy JSON files now under
  `artifacts/three_by_two_separation/`.
- `two_setting_qubit_checkpoint.zip` (frozen staging source)
  — exact preimages of the checkpoint files committed by hash in the closure
  bundle.

### Final closure

- Git commit `49c75ca5d658f030f8b8d3af640254e2d0913df6`,
  `two_setting_qubit_povm_pvm_equivalence/FINAL_RESEARCH_DOSSIER.md`.
  The line references below are to that frozen file:
  - compact separation and residual maximizer: lines 65–125;
  - Lorentz coordinates and metric: lines 129–330;
  - incidence model and physical completeness: lines 334–468;
  - positive multipliers: lines 472–631;
  - metric differential and second variation: lines 635–911;
  - exceptional fibers and rank one: lines 915–1153;
  - rank-zero decomposition: lines 1157–1307;
  - closure and minimum-setting conclusion: lines 1311–1359.
- Exact closure verifier and rank-zero simulator in the same commit.

## Director checklist

| Item | Status | Audit finding |
|---|---|---|
| Operational definition of fixed-qubit POVM/PVM behavior | REPAIRED | Phase-I §1 is correct. The final paper must define branchwise dimension, zero projectors, shared randomness, and classical postprocessing in one formal definition. |
| Compactness and convex separation | PASS | Closure Lemma 2.1 and Corollary 2.2 correctly pass from a point outside the compact PVM hull to a Bell functional whose full POVM maximum is strictly larger. |
| D1 coefficient table | PASS | Dense and sparse CSVs agree exactly with the displayed rational functional. |
| D1 simple POVM strategy | PASS | Effects sum to \(I\), have explicit positive rank-one factorizations, and attain \(L_0=20\sqrt2+16/25\). |
| D1 strengthened strategy | PASS | The algebraic strategy attains \(L_1=(16+8\sqrt{7813})/25\). Its one-parameter optimality is correctly limited to that family. |
| Exhaustion of qubit PVM support patterns | PASS | The six rank partitions of a three-label qubit PVM are exactly the three singleton and three pair supports. |
| Pure-state and Schmidt reduction | PASS | Maximization over the state gives a top eigenvector; local unitaries then give the stated Schmidt form without restricting optimized measurements. |
| Degenerate CHSH branch | PASS | If any CHSH observable is \(\pm I\), the CHSH norm is \(2\), and the auxiliary estimate places the value well below the final upper bound. |
| CHSH deficit estimates | PASS | The state-imbalance and Bob-angle estimates follow from the correlation matrix, Cauchy–Schwarz, and exact scalar inequalities. |
| Robust auxiliary PVM bound | PASS | All singleton and pair supports are covered. The determinant sign, trace-norm formula, square-root comparison, and sign conditions are correct. |
| Global D1 PVM upper bound | PASS | Completing the square gives \(U=20\sqrt2+3/5+(4+3\sqrt2)/250\) for every fixed-qubit PVM strategy, including shared randomness and postprocessing. |
| Strict D1 gaps | PASS | Both \(L_0-U=3(2-\sqrt2)/250>0\) and the strengthened exact gap are certified without numerical inequalities. |
| Locking theorem | PASS | Theorem 9.1 is the exact optimization of \(C\sqrt\delta-K\delta\); Theorem 9.2 is its general-modulus form. |
| D2 binary-POVM reduction | PASS | Every binary qubit POVM decomposes into PVMs with one common shared-randomness variable for the full behavior. |
| D2 Lorentz-cone circuit decomposition | REPAIRED | The proof is correct. The paper should spell out repeated-ray bookkeeping, the \(2\)-versus-\(2\) circuit conclusion, and the rank-one-\(\Omega\) realization. |
| D3 selection of an extreme unrandomized realization | PASS | Compactness and behavior extremality justify choosing a pure entangled state and extremal local POVMs. |
| D3 common-span filtering | REPAIRED | Lemma 10.2 is correct. The paper should explicitly discard zero effects and reapply the span-intersection argument after deterministic postprocessing. |
| D3 exclusion of four-outcome POVMs | PASS | Scalar-only span intersection forces dimensions \(2\) and at most \(3\); the support-perturbation bound \(\sum r_a^2\le4\) leaves a ternary rank-one POVM. |
| Residual global maximizer | PASS | D3 applies to a maximizer of the full POVM problem, so local POVM duality is legitimately invoked in the closure. |
| Lorentz metric normal form | PASS | The determinant identity, five rays, four-parameter Gram matrix, signature, and strict off-diagonal inequalities are correct. |
| Pure-state conformal Lorentz relation | PASS | \(P^Tg^{-1}P=4|\det C|^2h\) follows by polarization and invertibility of the local effect bases and steering map. |
| Local physical completeness | REPAIRED | Lemma 6.1 is correct. The paper should state explicitly that every tangent integrates to a two-sided incidence curve and that all strict physical conditions are open. |
| Smoothness and KKT multipliers | PASS | The five rank-one constraint matrices and normalization differential are independent. |
| Identification and sign of determinant multipliers | REPAIRED | The argument is correct but should be written separately for Bob's binary and ternary inputs, with separate normalization operators and explicit complementary slackness. |
| Hessian square completion | PASS | The sign and order in \(2q(W)\), with \(q(W)=\operatorname{Tr}(SW\Lambda W^T)\), are correct. |
| Ambient inertia and dimension obstruction | PASS | With \(\Lambda>0\), \(q\) has inertia \((4,12)\); a compatible space of dimension at least \(13\) contains a positive direction. |
| Radial normalization | PASS | \(I\) is null and orthogonal to the compatible \(W\)-space, so normalization can be imposed without changing \(q\). |
| Exceptional fibers | REPAIRED | The injectivity proof is correct, but the \(x_0=x_1=0\) and \(x_2=x_3=0\) base-ray subcases should be inserted explicitly. |
| Rank-one stratum | PASS | Injectivity implies exactly one nonzero row of \(\mathcal D\), whose kernel contains no strictly positive multiplier. |
| Rank-zero stratum | PASS | The pentad permutation, equal scaling, interval-intersection lemma, and deterministic local decomposition are correct. |
| Boundary and arbitrary outputs | PASS | These are handled by D2–D3 before entering the genuine residual stratum; the closure does not silently assume all outcomes are positive. |
| Universal \(2\times2\) equality | PASS | The rank-\(\mathcal D\) trichotomy exhausts the residual architecture supplied by D3. |
| Minimum setting architecture | PASS | One-input scenarios are local, \(2\times2\) is closed, and D1 supplies a strict \(3\times2\) separation. |
| Exact global POVM/PVM optimum for the D1 functional | UNRESOLVED | Neither optimum is known exactly. This is expressly outside the theorem and is not needed for separation. |
| Literature novelty and priority | UNRESOLVED | This proof audit does not establish novelty. It requires the separate literature report and accurate historical wording. |

## Publication-ready repaired statements

### Definition: fixed-qubit projective-simulable behavior

> For fixed finite input and output sets, let
> \(\mathcal Q^{\mathrm{POVM}}_2\) be the convex hull of behaviors generated by
> bipartite states on local Hilbert spaces of dimension at most two and arbitrary
> local POVMs. Let \(\mathcal Q^{\mathrm{PVM}}_2\) be the convex hull of
> behaviors generated on the same branchwise dimension bound by local PVMs,
> allowing zero projectors and arbitrary input-dependent classical
> postprocessing of their outcomes. Shared and local classical randomness are
> included in the convex hull; no local ancilla may increase a quantum branch
> above dimension two.

This makes the convention used by every theorem explicit. Stochastic
postprocessing is redundant for a linear support-function calculation, but it
should remain in the operational definition.

### D2: one-binary-party simulation theorem

> **Theorem.** Consider a bipartite Bell scenario with two inputs per party and
> finite outputs. If one party has two binary-output measurements, then every
> behavior generated by local qubits and arbitrary POVMs belongs to
> \(\mathcal Q^{\mathrm{PVM}}_2\).
>
> **Circuit bookkeeping.** After decomposing the binary POVMs into PVMs, fix one
> component and compress each steered positive operator by
> \(\Phi(\sigma)=(\operatorname{Tr}\sigma,
> \operatorname{Tr}\sigma B_0,\operatorname{Tr}\sigma B_1)\). Split every
> compressed vector into labeled extreme-ray terms. Combine repeated collinear
> terms only within the same label, and decompose the resulting positive
> relation into inclusion-minimal positive subrelations. In a cone of linear
> dimension at most three, such a subrelation has at most four signed rays.
> Extremality of a cone ray rules out a noncollinear one-versus-many relation;
> hence each nontrivial subrelation is two-versus-two. The injective lift on
> \(\operatorname{span}_{\mathbb R}\{I,B_0,B_1\}\) gives
> \(R_0+R_1=S_0+S_1=\Omega\). If \(\Omega\) is invertible, its canonical
> purification and the two orthonormal bases
> \(\Omega^{-1/2}(r_0\ r_1)\) and
> \(\Omega^{-1/2}(s_0\ s_1)\) realize the two labeled decompositions by PVMs.
> If \(\Omega\) has rank one, a product purification and two independently
> chosen local PVM bases realize the required binary probability vectors.
> Weighting by \(\operatorname{Tr}\Omega\) and summing the circuits reconstructs
> the full behavior.

### D3: residual architecture theorem

> **Theorem.** If a two-input-per-party Bell functional has a fixed-qubit POVM
> maximum strictly larger than its fixed-qubit PVM maximum, then a maximizing
> behavior has an unrandomized realization with a pure entangled two-qubit
> state such that, on each party, one input is a nondegenerate binary PVM and
> the other is an extremal ternary rank-one POVM. After deleting zero effects,
> the real spans of the two measurements intersect exactly in
> \(\mathbb RI\).
>
> **Postprocessing clause.** Whenever a two-dimensional measurement span is
> replaced by a deterministic postprocessing of its spectral PVM, retain the
> behavior-extreme component that realizes the same behavior and reapply the
> common-span filtering lemma to that realization. This ensures that the final,
> rather than merely the pre-replacement, measurement spans have intersection
> \(\mathbb RI\).

### Integrated physical tangent lemma

> **Lemma.** Let \((P,g)\) be a genuine residual incidence point: \(g\) has
> signature \((1,3)\), all five effect rays and all five steered rays have strict
> future orientation, the reconstructed reduced state is positive definite,
> and \(P\) is invertible. The normalized incidence equations define a smooth
> manifold near \((P,g)\). Every tangent vector to that manifold is the
> derivative at zero of a smooth curve \((P(t),g(t))\), defined for
> \(|t|<\varepsilon\), that remains in the same strict physical stratum. The
> reconstruction in Lemma 6.1 therefore turns it into a two-sided smooth curve
> of genuine residual qubit strategies. This remains true when some joint
> probability at \(t=0\) is zero, because positivity follows from
> \(p_{ij}(t)=\operatorname{Tr}(E_i(t)S_j(t))\ge0\), not from an entrywise-open
> probability condition.

The proof is the submanifold theorem followed by openness of signature, strict
time orientation, invertibility, and positive definiteness.

### Positive determinant multipliers

> **Lemma.** At a residual global POVM maximizer with value strictly above the
> PVM support value, the five incidence determinant multipliers are strictly
> positive.
>
> **Proof bridge.** Pull the incidence Lagrangian back separately to variations
> of Bob's binary input and Bob's ternary input while fixing the state, Alice's
> measurements, and Bob's other input. For each input \(y\), its normalization
> constraint has its own Hermitian multiplier \(\Gamma_y\), and stationarity is
> \[
> K_{b|y}-\Gamma_y+
> 4|\det C|^2\lambda_{b|y}\operatorname{adj}(N_{b|y})=0.
> \]
> Since
> \(\operatorname{adj}(N_{b|y})N_{b|y}=0\), this equation implies
> \((\Gamma_y-K_{b|y})N_{b|y}=0\). Finite POVM duality supplies a positive
> semidefinite dual operator with the same complementary-slackness equations.
> The ranges of the effects of one input span \(\mathbb C^2\), so the
> complementary-slackness normalization operator is unique. Hence
> \[
> \Gamma_y-K_{b|y}
> =4|\det C|^2\lambda_{b|y}\operatorname{adj}(N_{b|y})\ge0,
> \]
> and every \(\lambda_{b|y}\ge0\). If one multiplier were zero, replacing that
> entire input by the corresponding deterministic PVM would preserve the Bell
> value. A nonsignaling behavior with only one nontrivial input on one party is
> local and therefore PVM-realizable, contradicting strict separation. Thus all
> five multipliers are positive.

### Exceptional-fiber completion

> **Lemma.** For a strict residual metric \(g\), the restriction of the
> projective quadratic map \(\Phi\) to the null quadric is injective away from
> the five base rays.
>
> In the exceptional plane \(x_0=x_1\), a nonbase point has
> \(x_0=x_1\ne0\): if \(x_0=x_1=0\), nullness gives
> \(2e x_2x_3=0\) with \(e>0\), hence the point is \(r_3\) or \(r_4\).
> Therefore scaling to \(x_0=x_1=1\) is legitimate. In the exceptional plane
> \(x_2=x_3\), a nonbase point has \(x_2=x_3\ne0\): if both vanish, nullness
> gives \(x_0x_1=0\), hence the point is \(r_1\) or \(r_2\). Therefore scaling
> to \(x_2=x_3=1\) is legitimate. Together with the two coordinate-hyperplane
> cases and the displayed resultant factorizations, these observations exhaust
> every zero of the generic inverse denominator.

### Final theorem

> **Theorem.** For every pair of finite output architectures with two inputs
> per party,
> \[
> \mathcal Q^{\mathrm{POVM}}_2(2,2)
> =
> \mathcal Q^{\mathrm{PVM}}_2(2,2).
> \]
> Consequently, because every scenario with one input on either party is local
> and the rational D1 functional has a strict \(3\times2\) fixed-qubit
> POVM-over-PVM gap, the minimum setting architecture for such a gap is
> \(3\times2\), up to exchanging the parties.

## Verifier boundary

The two D1 verifiers and the closure verifier were rerun successfully with
SymPy 1.14. The rank-zero simulator also passed.

The scripts are exact regression/certificate checks, not formal proofs of every
quantified statement:

- the comprehensive D1 verifier symbolically checks coefficients, both
  strategies, dual factorizations, determinant/discriminant identities,
  square-root identities, rank patterns, and exact gaps;
- D2, D3, compactness, support exhaustion, and sign implications remain human
  proofs;
- the closure verifier checks the metric, quadratic-map and resultant
  identities symbolically, but its pure-state Lorentz and Hessian checks include
  exact test instances rather than a general formal derivation;
- the rank-zero executable tests the symmetric trine instance, while the
  general result comes from the written transportation proof.

## Load-bearing uncertainty

**No unresolved load-bearing mathematical dependency remains in the recovered
chain.** The two places most deserving independent referee attention are:

1. D3's behavior-extremality/common-span reduction from arbitrary finite
   outputs to the residual architecture.
2. The identification of the incidence multipliers with the positive local
   POVM dual slacks.

Both were rederived and passed this audit. Their risk is expository density,
not a located counterexample or logical failure.

The exact global maxima of the displayed D1 functional, equality cases in the
locking bounds, literature novelty, and priority are not part of the proved
mathematical claim.

## Final consolidated-manuscript audit

After the source-chain audit, the completed `paper/main.tex` and
`paper/appendices.tex` received a separate line-referenced consistency pass.
That pass initially identified five exposition issues, all now repaired:

1. smoothness is asserted only on the open \(P\)-invertible genuine residual
   stratum used by the closure;
2. the restricted Bell objective \(L_{\mathsf C}\), coefficient matrix
   \(\mathsf C\), and local score operators \(K_{j|y}\) are defined;
3. the rank-one projector \(\Pi(\mathbf n)\) is defined without colliding with
   \(Q=g^{-1}\);
4. rank-one \(\Omega\), zero terms, repeated rays, and retained labels are
   explicitly handled in D2;
5. optimum notation, “two inputs per party,” and the Lorentz metric \(J\) are
   unambiguous.

The repaired manuscript was rechecked and received **PASS**: no remaining
theorem-invalidating inconsistency, unresolved reference, or missing
load-bearing definition was found.
