# Independent signed-measure and regularity family audit — PR 23

Audit completed 2026-10-01 UTC. Candidate head: `ea6b192f7e3bc094b78bbc416bf61c609ffa5b2d`. The fourteen frozen attempt files are covered by `snapshot_manifest.json`; the shared queue change is the coordinator's separate scope. Independent scope/reconstruction was sealed in `SCOPE_SEAL.md` before historical reviews and author code were read. This is verification of existing mathematics, with no new central proof search, no external-person communication, and no change to the original 0/5 attempt count.

**Verdict: PASS for the candidate's expressly limited source-status correction.** The strongest verified result is the all-dimensional signed-measure classification on the whole space, with local versions on adapted product boxes. No novelty, new open-problem solution, arbitrary-domain global representation, paper, release or DOI is certified. The imported target lacks a domain and regularity threshold; its historical interpretation is supported by its original explanatory blow-up context. Final catalog disposition belongs to the coordinator.

## Primary source coverage

The [journal PDF](https://www.aimspress.com/aimspress-data/mine/2020/3/PDF/mine-02-03-018.pdf), independently found through the [DOI page](https://doi.org/10.3934/mine.2020018), contains Theorem 2.10 on journal pp.399–400. Its hypothesis expressly allows signed locally finite scalar measures. Cases (i) and (ii), including both proofs, match the two geometric structures in the candidate. [arXiv v2](https://arxiv.org/pdf/1911.01356), pp.12–14, agrees. Lemma 2.1 supplies the rigid kernel; the later Theorem 3.2 uses positivity to simplify tangent structures and is not the general signed theorem. Case (iii) concerns nonsymmetric-product matrices and is outside the target; its ellipticity argument is not used here.

The complete Rindler contribution in [OWR 36/2012](https://publications.mfo.de/bitstream/handle/mfo/3307/OWR_2012_36.pdf?isAllowed=y&sequence=1), pp.2247–2249, was read. Page 2248 explains a step in an already published lower-semicontinuity proof and failure of a simpler structural guess. It does not designate this sentence an open conjecture. The introductory variational domain is bounded Lipschitz; the subsequent discussion is about blow-ups, and does not assert global profiles on that original domain.

The [2011 Rindler paper](https://arxiv.org/pdf/1008.2089), PDF pp.33–34, Propositions 4.7 and 4.9, gives the two-dimensional classification for `LD_loc`, with absolutely continuous strain coefficients in `L1_loc`. Its Section 4.4 explicitly omits the `BD_loc` extension. Example 4.8 is the candidate's quartic example. Earlier Lemmas 4.4–4.5 and tangent arguments use a fixed positive polar measure; they cannot substitute for the later signed theorem. The candidate does not make that substitution.

Source hashes, URLs and exact locations are in `SOURCE_RECEIPTS.json`. All four primary PDFs are retained only in the ignored `tmp/` directory. The three historical primary-PDF hashes independently match the old review's receipts; the journal PDF is an additional independently checked source.

## Universal reconstruction and necessity

The following reconstruction verifies the mechanisms, rather than inferring completeness from finitely many polynomial examples. It also fills the regularization shorthand in the printed proofs. All derivatives below are distributional when the coefficient is a measure. The open domain is a connected product box or the whole space, unless specified otherwise.

Let `P` be a fixed nonzero symmetric matrix. If smooth `u` satisfies `Eu in R P`, one nonzero component of `P` extracts a smooth scalar coefficient `lambda`; consequently `Eu=P lambda dx` and `u in BD_loc`. The signed hypothesis applies directly. For a `BD_loc` displacement with strain in that fixed line, the same component extraction gives a signed scalar Radon measure.

For `Eu=P lambda`, every Saint-Venant tensor entry vanishes:

```
P_jl partial_ik lambda + P_ik partial_jl lambda
- P_jk partial_il lambda - P_il partial_jk lambda = 0.
```

### Independent vectors

First take `P=e1 odot e2`, so `P12=P21=1/2`. Choosing the tensor entries `(i,j,k,l)=(1,2,1,2)`, `(1,2,1,k)`, `(2,1,2,k)` and `(1,k,2,l)` yields, in every dimension,

```
partial_12 lambda = 0,
partial_1k lambda = partial_2k lambda = 0       (k >= 3),
partial_kl lambda = 0                          (k,l >= 3).
```

Thus every transverse first derivative is a constant distribution. Subtracting the corresponding affine transverse function leaves a distribution independent of all transverse variables. The remaining mixed equation on the two-dimensional product yields

```
lambda = mu_1(dx2) + mu_2(dx1) + 2(c dot z) dx.
```

Here a one-variable measure is understood to be lifted with Lebesgue measure in the other coordinates. Distributional separation is the familiar product-domain fact that a distribution with zero derivative in one coordinate is constant in that coordinate, and a distribution with zero mixed derivative is a sum of one-coordinate distributions. A direct justification integrates a test function after subtracting its coordinate average; its zero-average part is a derivative of a compactly supported primitive. Repeating that argument gives the displayed separation. Since `lambda` is Radon, testing it against fixed compact transverse and opposite-coordinate averaging functions makes the separated one-variable distributions Radon as well, up to harmless constant redistribution.

Each signed `mu_i` has a locally BV primitive `H_i`. The displacement

```
(H1(x2)+x2 c dot z, H2(x1)+x1 c dot z, -c x1 x2)
```

is locally integrable and has exactly the above strain. The rigid-kernel argument below proves that every original displacement differs from it by a single rigid motion. This establishes necessity and the BV profile threshold without positivity or a mollified subsequence assumption. In dimension two the transverse space is zero, so `c=0`.

For arbitrary linearly independent `a,b`, let

```
Delta = |a|^2 |b|^2 - (a dot b)^2 > 0,
p = (|b|^2 a - (a dot b)b)/Delta,
q = (|a|^2 b - (a dot b)a)/Delta.
```

Use the matrix `T` with columns `p,q` and an orthonormal basis of the perpendicular complement. Then `T^T a=e1`, `T^T b=e2`. The correct reduction is `w(y)=T^T u(Ty)`. Its strain is transformed by congruence; for a measure the scalar pullback includes `|det T|^-1`. The canonical coordinates are `y1=x dot a`, `y2=x dot b`, while transverse coordinates remain orthonormal. Transforming the canonical displacement back gives exactly candidate `SOURCE_STATUS.md:31`–`:40`, with one constant vector `v` perpendicular to `span{a,b}`. The construction does not assume orthogonality or unit length.

### Parallel nonzero vectors

The original product is `kappa(e odot e)` for a unit vector `e` and a nonzero scalar `kappa`, which may be negative. Absorb `kappa` into the signed scalar measure. In orthogonal coordinates `s=x dot e`, `t_j=x dot v_j`, the entries `(1,j,1,k)` of Saint-Venant force precisely `partial_jk lambda=0` for every transverse `j,k`. Thus

```
lambda = mu(ds) + sum_j t_j gamma_j(ds).
```

The coefficient distributions depend only on `s`. To establish that they are measures, choose compact transverse test functions with moments `integral chi0=1`, `integral t_j chi0=0`, and `integral chi_j=0`, `integral t_k chi_j=delta_jk`. Projecting the original Radon measure against these functions isolates `mu` and each `gamma_j`; local total variation bounds follow from the fixed test-function sup norms. Such moment functions exist on every nonempty transverse product box by elementary linear algebra on distinct small supported bumps.

Integrate `mu` once to obtain `H in BV_loc`. Integrate each `gamma_j` twice: the first primitive is BV and therefore bounded on compact one-dimensional intervals; the second primitive `P_j` is locally Lipschitz and has `P_j' in BV_loc`. The candidate parallel displacement is then an `L1_loc` function with exactly this strain. The mixed terms cancel distributionally. Subtract it from the original displacement and apply the rigid kernel. These are the regularity conditions actually printed in Theorem 2.10; one must not replace the profiles with arbitrary distributions.

For smooth `u`, the scalar coefficient is smooth. In the independent case its one-variable summands can be selected by evaluation on coordinate axes after subtracting the transverse affine part. In the parallel case `h(s)=lambda(s,0)` and `p_j(s)=partial_tj lambda(s,0)` are smooth. Integrating these coefficients gives smooth `H_i,H,P_j`. Hence the draft's smooth formulas follow from the BD theorem with no hidden regularity upgrade. The corresponding absolutely continuous case gives `H_i,H in W1,1_loc`, `P_j in W2,1_loc`, consistent with the 2011 `LD` results.

### Kernel and boundary cases

The distributional identity

```
partial_jk u_i = partial_j (Eu)_ik + partial_k (Eu)_ij - partial_i (Eu)_jk
```

implies that `Eu=0` makes every second derivative vanish. On a connected open set this makes `Du` a constant matrix, and the strain equation forces it to be skew. Translations supply the remaining constant. A disconnected domain has separate rigid motions on its connected components. Over the reals, `a odot b=0` only when at least one vector is zero. In dimension one a nonzero product spans the scalar strain space, so the inclusion adds no restriction beyond the assumed map regularity. These verify `SOURCE_STATUS.md:58`.

## Adversarial controls and reproduction

The exact original eight symbolic checks and historical eleven checks reproduced successfully under `/usr/bin/python3` 3.9.6 / SymPy 1.14.0. Their receipts are `original_replay.txt` and `historical_replay.json`. Every historical JSON check agrees. These test sufficiency/finite compatibility and do not prove all-dimensional necessity.

`fresh_controls.py` adds nineteen controls. Its jump cases evaluate the definition of distributional strain directly, integrating piecewise polynomial `L1` displacements against derivatives of a compact `C1` test function on a cube. They do not differentiate the author's smooth symbolic functions. The independent coefficient contains two oppositely signed jump planes, another jump plane and a transverse affine density; the only nonzero strain component has action `31028/23625`. The parallel example uses Lipschitz positive-part profiles with BV derivatives: its strain is `(2+y)delta(x)+(-3-2z)delta(x-1/2)`, all mixed components cancel, and its `E11` action is `-86/675`.

A nonunit jump normal separately checks the coarea normalization: `u=(J(2y),0,0)` gives `(e1 odot 2e2)` multiplied by half the hyperplane measure. A wrong factor of two is detected. Another negative control takes the prohibited profile `P=J`; it makes the displacement contain `t delta(s)` and the strain contain `t delta'(s)`. Uniformly bounded compact test functions yield action `-8n/105`, unbounded with `n`, proving that this coefficient is not a Radon measure. This explicitly distinguishes distributional formal solutions from admissible BD maps.

Other controls check the dual-basis coordinate/displacement transformation for nonorthogonal, nonunit vectors; a rotated unit parallel direction with negative original scale `-14/3`; the unnormalized `b=2a` and `b=-2a` trap; five incompatible scalar coefficients with nonzero Saint-Venant entries; compatible transverse coefficients; the one-dimensional case; and the rigid kernel. Exact outputs are in `fresh_results.json`. The initial successful seventeen-control receipt is preserved separately. A Python/SymPy Boolean conversion failure, its correction, and the later addition of the two domain controls are preserved in `CONTROL_RUN_HISTORY.md` and the research log.

## Domain boundary and source precision

The argument uses whole products for distributional separation and profile continuation. It works locally on adapted boxes in any open domain. A connected domain alone does not imply global profiles. Two explicit smooth countercontrols use `g(r)=exp(-1/r^2)` for `r>0` and zero otherwise:

- Independent case: two vertical arms `(-3,-1)x(-1,2)` and `(1,3)x(-1,2)`, joined by the bottom strip `(-3,3)x(-1,0)`. Put `u=(g(y),0)` on the right arm and zero elsewhere. Its fixed-line strain coefficient has rectangular cross-difference `2/e` at the four interior points recorded in the fresh controls, whereas any global coefficient `f(x)+h(y)` has cross-difference zero.
- Parallel case: two horizontal arms `(-1,2)x(1,3)` and `(-1,2)x(-3,-1)`, joined by the left strip `(-1,0)x(-3,3)`. Put `u=(g(x),0)` on the upper arm and zero elsewhere. At `x=1`, an affine-in-y coefficient must be constant because it is constant on the upper interval, and therefore cannot also vanish on the lower interval.

The functions glue smoothly because `g` is flat at zero. Both domains are connected bounded Lipschitz domains. They falsify an unrestricted global profile claim, which the candidate expressly declines in `SOURCE_STATUS.md:86`. They do not falsify its whole-space or local assertion.

The printed condition `a != +/-b` is not literally equivalent to independence for arbitrary unnormalized vectors. The publication does not explicitly impose unit normalization at that point. For `b=2a`, the parallel quartic example already disproves using case (i) literally. The candidate's independence/parallel split and unit direction in the second case repair this source ambiguity. The earlier two-dimensional proof's wording about a matrix sending `e1,e2` to `a,b` also has the congruence direction reversed when combined with `T^T u(Tx)`; the dual-basis map above supplies the correct reduction. These are source precision issues, not failures inherited by the candidate's formulas. The proof also contains an evident repeated-index sign typo in the parallel skew-gradient display; the compatibility derivation independently avoids it.

## Findings and exact remaining gap

No P0/P1/P2 mathematical or source-coverage defect was found in the frozen candidate's explicitly scoped claim. The important constraints are already recorded at `SOURCE_STATUS.md:3`, `:23`, `:60`, `:86` and `:88`: source-status correction only, signed whole-space coverage, corrected geometric split, local qualification, and no novelty. No mandatory correction is requested from this family.

An optional precision improvement is to state the theorem's BV and Lipschitz/derivative-BV profile spaces explicitly next to the displayed smooth formulas, and give the journal theorem pages 399–400. The draft already calls its formulas smooth and cites the stronger theorem, so omission of these details is not a false regularity claim.

Exact unresolved scope: an arbitrary-domain global-profile target is neither specified by the imported record nor resolved by this result, and the unrestricted version is false as the controls show. The present artifacts support removing the intended source-derived whole-space/local-blow-up item from a novel-proof queue; they do not support relabeling an independently specified global-domain problem as solved. No new contribution suitable for a paper or immutable DOI snapshot was found. Audit completion estimate: 100%; novel-result completion estimate: 0%.
