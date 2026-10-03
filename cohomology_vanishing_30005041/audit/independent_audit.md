# Independent adversarial audit: cohomology-vanishing exponents

**Date:** 2026-10-03  
**Target:** queue rank 482, problem 30005041, OWR-9790362-012  
**Verdict:** **PASS for the precisely scoped five-attempt partial-results packet.**

No mathematical or reproducibility defect requiring a HOLD was found. The original fixed-Lamperti-family interval question remains **unsolved in this work, 5/5 attempts**. This audit is not a full solution, a novelty claim, a human-referee certification, or an exhaustive certification of current literature status.

## 1. Frozen input, audit boundary, and reproducibility

The original packet was read and hashed without editing it. Its five manifest-listed files and the manifest are the complete file inventory. All five SHA-256 digests agree with FROZEN_MANIFEST.json, both before and after the audit computations.

- ATTEMPTS.md: `bd764263ce2c166b8c0e2710408f3e07ddae50d10cb63fbaa1eb38aa3d2d00cf`
- FROZEN_MANIFEST.json: `8945c0b8686a4bb95bd6ba74a30ea04b609d4dd7d9ca3946434c5147d7a2264c`

The audit includes a new, self-contained Python standard-library checker. It imports no author module and does not execute the author checker. It uses rational Gaussian elimination on arbitrary signed permutations, denominator-cleared inequalities at new rational exponents, weighted intertwining identities, algebraic exact-sequence dimension checks, and exact tails in the infinite-block construction. The author's separate 6,480-case checker was also rerun once; its complete JSON output agrees byte-for-byte with the frozen recorded output.

Run the independent mathematics checks from any directory:

    python3 independent_controls.py

To include the frozen-byte and inventory checks, supply the original packet directory:

    python3 independent_controls.py --author /path/to/frozen-packet

The optional path is read only. No local source PDF is required to run the controls. The audit deliverables contain no scholarly PDFs, page images, catalogue corpus, credentials, private conversation history, or absolute workspace paths. No remote write was made.

The final recorded run contains **52,164 exact assertion cases**, including all **50,363 signed permutation models on zero through six atoms**. Its output is independent_controls_results.json. These finite computations are consistency checks; the arguments below, not the finite case count, justify infinite-dimensional conclusions.

## 2. Original source and problem identity: PASS

The original question was independently read in the OWR report, printed p. 568, PDF page 52. It fixes one continuous homomorphism into the semidirect product of nonsingular transformations and measurable signs. The exponent-dependent Radon–Nikodym powers then define one fixed Lamperti family. The question concerns the vanishing set of ordinary continuous first cohomology over positive finite exponents. In particular, p=2 is the prescribed Lamperti representation, not an arbitrary replacement Hilbert representation.

The neighboring group-wide result permits changing the action. OWR explicitly explains why that does not settle this fixed-family question. The packet does not confuse the two statements. The publisher also confirms the report's 2022 volume and 11 March 2023 publication date. [Official OWR report](https://ems.press/journals/owr/articles/9790362).

The local primary PDF identities are:

- OWR report: `a2461e38bab4c763106b3bdf7c13c6d7db5af35bad14c34d5e9cb11b69b4c19f`
- Marrakchi–de la Salle arXiv v3: `ac37430fb38eea1cea9b062db5ce35f894184c5fad8285f1e2276b19f6bf0196`

In arXiv:2001.02490v3, printed p. 10, Theorem 5.4 gives downward vanishing for the **formal** subspace and only for **1 <= p < q < infinity**. This subspace is the kernel of the ordinary-cohomology map from Lp to L0. It is not reduced cohomology. No ergodicity or finite invariant measure is required by that theorem. Question 5.5 asks the stronger full-cohomology downward implication; the preceding paragraph leaves the full interval question undetermined. The packet uses exactly this version and exponent range. The complex-valued theorem applies to the real signed setting by taking real and imaginary parts. [Inspected arXiv version](https://arxiv.org/abs/2001.02490v3).

A supplementary primary-source check confirmed the advertised Lavy–Olivier finite invariant ergodic setting in Theorem 3 and Proposition 28, as well as the distinction between its group-wide Hilbert exception and fixed Banach–Lamperti families. This source supplies context; none of the new elementary proofs depends on importing its claims outside their hypotheses. [Primary paper](https://arxiv.org/pdf/1410.0227), [journal record](https://aif.centre-mersenne.org/articles/10.5802/aif.3348/).

The Compositio bibliographic record agrees with volume 159 (2023), pp. 1300–1313 and the stated DOI. The audit does not substitute journal theorem numbering for the inspected arXiv numbering. [Publisher record](https://www.cambridge.org/core/journals/compositio-mathematica/article/abs/isometric-actions-on-lpspaces-dependence-on-the-value-of-p/7F2771D5760A02A9880DE5863B55F84C).

Historical repository searches, the catalogue access result, and the absence of a later solution are not re-certified here. They are appropriately presented in the packet as bounded provenance/status checks, not mathematical proof of novelty or open status.

## 3. Attempt 1: Mazur transport and the no-measurable-invariants lemma: PASS

### The advertised failure is genuine

For the trivial real representation of Z, a cocycle is an additive map. The signed square root sends the values 1 and 4 of the cocycle n -> n to 1 and 2, contradicting additivity. Equivariance of a nonlinear map does not make it a linear cochain map. This elementary counterexample is valid even on a one-point probability space, so it cannot be repaired by measure finiteness.

### The separately proved lemma works for all positive finite exponents

Put alpha=p/q in (0,1). Concavity on one sign and the two-term concavity estimate across opposite signs give the stated pointwise bound with constant 2^(1-alpha). Raising it to q gives an integrable multiple of the pth power of the original difference. Equivariance holds for measurable functions as well as Lp functions: the sign and Radon–Nikodym multiplier transform exactly under the signed power.

Thus, if b=delta_p f is Lp-valued, delta_q(Mf) is Lq-valued. In the packet's discrete scope it is automatically a continuous group cocycle. Formal vanishing at q supplies h in Lq with delta_q(Mf-h)=0. The hypothesis excludes **all measurable invariant vectors**, not just Lq invariant vectors; consequently Mf=h. Its qth power integral is exactly the pth power integral of f. This proves the conclusion, including when p<1 or q<1, without Banach-space machinery.

The Mazur maps biject measurable invariant spaces, so absence of nonzero measurable invariants is exponent independent. This does not identify arbitrary cohomology classes. On the one-point trivial Z example, every formal class is zero while ordinary H1 is nonzero.

Independent controls test the scalar inequality at alpha=2/3, 2/5, 3/5, 3/4, 4/7, 5/7, and 1/7 on signed rational inputs. These are denominator-cleared exact arithmetic checks, not floating-point approximations.

## 4. Attempt 2: finite invariant measure and exact multiplier obstruction: PASS

### Endpoint argument

An equivalent measure conjugates each p-representation by its corresponding density multiplier. With an invariant probability measure, every representation in the family has the same signed-composition formula; the inclusion Lb -> La for a<b is continuous and equivariant. A cocycle at b therefore has a primitive in La if H1 vanishes at a. It is a formal class at b. Vanishing of full H1 at c implies formal vanishing there, and Theorem 5.4 transfers that formal vanishing down to b.

This proves the interval assertion on [1,infinity) for the stated finite-invariant-measure class. It does not rely on ergodicity. Its use of the formal theorem is within the published range, and it does not establish the original all-positive-exponent assertion. Empty measure spaces cause no problem; they are trivial separately if one cannot normalize a zero measure.

### Multiplier boundedness, including quasi-Banach exponents

With 1/r=1/p-1/q, Holder is applied to the integral of |a f|^p with exponents r/p and q/p, both strictly larger than one. It therefore does not require p>=1. The exact operator gauge is ||a||_r.

For necessity, sigma-finiteness and finiteness of a almost everywhere give an increasing exhaustion by finite-measure sets on which a is bounded. Testing on 1_A a^(r/q) is legitimate and yields the lower bound (integral_A a^r)^(1/r). Monotone convergence supplies necessity and the sharp norm. A lower bound on a in the chosen sets is available under strict positivity and causes no loss.

The intertwining equation has the correct orientation for J_g=d((T_g)_*mu)/dmu. Cancelling the common sign gives a/(a composed with T_g^(-1))=J_g^(1/p-1/q). Taking the rth power says precisely that the pushforward density of a^r mu equals itself. Strict positivity and finiteness almost everywhere give equivalence of measure classes, and the Lr condition gives finite total mass.

Both directions are proved, and only this class of multiplication operators is ruled out when no equivalent finite invariant measure exists. Neither arbitrary bounded intertwiners nor nonlinear cocycle mechanisms are excluded.

The independent controls use two-, three-, and five-atom nonsingular models, including multiple orbits and nonconstant masses. They check normalization and all 28 ordered exponent pairs from {1/3,1/2,2/3,1,3/2,2,3,6}, the density equation, exact Holder equality witnesses, and failure of the raw inclusion to intertwine.

## 5. Attempt 3: complete signed atomic Z classification: PASS

The atom-mass normalization is an isometric linear conjugacy for every finite p>0. Sigma-finiteness excludes infinite-mass atoms, so every nonnull atom has the positive finite mass needed by this normalization. It removes all atomic weights without changing the permutation or signs.

For discrete Z, evaluation at the generator identifies cocycles with the coefficient space, and coboundaries with the range of U-I. The sign convention I-U versus U-I does not change the range. No completeness or local convexity assumption is needed for this algebraic identification.

The orbit analysis exhausts every possibility:

1. A finite positive-sign cycle has a nonzero invariant linear functional after a sign gauge; that functional annihilates the range of I-U. Extension by zero to other orbits preserves the obstruction.
2. An infinite orbit is a bilateral shift after gauging. Solving (I-U)x=delta_0 forces two constant tails differing by one. At least one tail is nonzero, which excludes membership in every finite-positive-exponent lp space.
3. On a negative cycle of length n, U^n=-I and the displayed geometric-series inverse is correct. For p>=1 its norm is at most n/2. For p<=1, subadditivity of the pth power gives the stated n/2^p bound. These estimates sum over disjoint blocks; uniformly bounded lengths yield a global inverse for every p>0.
4. If all cycles are negative but their lengths are unbounded, distinct cycles with n_k>=2^k can be selected. After gauging, a constant vector of amplitude n_k^(-1/p) has pth-power norm one and exactly one difference coordinate of magnitude twice that amplitude. The defects are globally p-summable. Any global primitive is forced to equal those vectors on the selected blocks because each block is invertible; its pth-power norm diverges. Adding invariant vectors cannot repair this because a negative finite block has none.

Hence the vanishing set is all (0,infinity) exactly under the three stated conditions and is empty otherwise. The zero space is covered by the vacuous conditions. This classification includes p=1, p=2, and the quasi-Banach range; it says nothing about p=infinity.

The independent checker computes the exact cokernel dimension for every signed permutation on at most six atoms, including arbitrary multi-cycle permutations. It equals the number of positive-sign cycles. Separately, Gaussian elimination inverts negative cycles of lengths 1 through 17 and checks both inverse identities and every entry magnitude. In fact these controls exhibit the exact quasi-operator norm n^(1/p)/2 for 0<p<=1, using the input 2e_0; the packet needs only its weaker bounded-length consequence.

## 6. Attempt 4: uniform primitive estimates: PASS

The finite-generation and Banach hypotheses are doing real work and are explicitly present. For a finite generating set S, cocycle evaluation embeds Z1 into E^S. Every relator imposes a bounded linear equality on generator values; the intersection of these closed conditions is closed even if the presentation has infinitely many relators. Values on generators determine all values by finite word formulas. Thus the displayed generator norm makes Z1 a Banach space.

The invariant subspace is closed, and the induced coboundary map from E/E^G is bounded. Under ordinary H1=0 it is a bijection, so the Banach open mapping theorem gives its bounded inverse. No assumption that every quotient-distance infimum is attained is needed: nonzero cocycles admit representatives within a factor two of their quotient norm; zero cocycles use the zero primitive.

If the component constants are uniform, Tonelli's identity for the finite generator set makes the generator norms of the coordinate cocycles p-summable. The chosen primitives then form a vector in the lp direct sum and agree with the cocycle on generators, hence on all group elements.

Conversely, a component-supported cocycle is a global cocycle. Projecting any global primitive and invariant vector into that component is contractive and gives the component quotient-distance bound. Taking an infimum, or an arbitrary epsilon approximation, proves C_i<=C. No nearest-point or linear-selection assertion is being used.

The proof does not invoke this Banach argument at p<1, and the fixed p is not confused with a simultaneous constant over all exponents. Negative cycles provide exactly the advertised example of individually trivial blocks with a nontrivial direct sum. Their primitive-to-defect lower bound n^(1/p)/2 diverges at each fixed finite p.

### Explicit unreduced-versus-reduced stress test

For the disjoint union of unbounded negative cycles, every finitely supported vector lies in the range of I-U: invert each of its finitely many finite blocks. Such vectors are dense in lp for every finite p>0. Therefore the range is dense while the displayed infinite-block vector is outside it.

Thus this example has nonzero **ordinary** H1 but zero reduced H1. The packet's obstruction is valid precisely because it consistently uses ordinary cohomology. Replacing the range by its closure would destroy this argument and change the target.

The independent controls evaluate exact partial primitive norms and defect tails at eight rational exponents, including 1/3, 1/2, and 2/3. They directly verify that the truncated coboundaries approach the non-coboundary while the forced primitive norms diverge. These checks do not turn a finite calculation into an infinite proof; the geometric-series formulas supply that proof.

## 7. Attempt 5: measurable-cohomology reduction: PASS

The use of the **algebraic** quotient Qp=L0/Lp is essential and correct. In the standard convergence-in-measure topology Lp is dense in L0, so its quotient need not be Hausdorff. The packet does not invoke a topological long exact sequence or assume a Hausdorff quotient.

A Qp-invariant coset means that every delta_p f(g) belongs to Lp. Changing f by an Lp vector changes the resulting cocycle by an actual Lp coboundary. Its class vanishes exactly when f differs from an Lp vector by a measurable invariant vector. This proves the asserted identification of formal classes with Qp^G modulo the image of (L0)^G.

The kernel of H1(Lp)->H1(L0) is, by definition and by this direct argument, the formal subspace. Factoring out that kernel gives the stated injection. For the countable discrete groups at issue here, continuous and algebraic group cocycles agree. This reasoning is not a blanket claim about arbitrary algebraic cocycles for nondiscrete G.

For a hypothetical hole 1<=a<b<c, full vanishing at c forces formal vanishing at b by Theorem 5.4. Every nonzero b-class must therefore survive in the cohomology with L0 coefficients. The lower endpoint alone does not identify this image across exponents because the L0 action remains p-dependent. The nonlinear Mazur bijection on vectors cannot be treated as a cohomology isomorphism.

The necessary condition is accurately limited: it does not claim that such a nonformal class exists, that it would be sufficient to make a hole, or that the full theorem extends below 1. The independent finite-module checks verify the algebraic kernel/quotient dimension identity, including examples with nonformal cohomology and nontrivial extensions.

Here “measurable cohomology” means group cohomology with the specified L0 coefficient module. It should not be read as replacing the cochain definition by a different measurable-cochains theory for nondiscrete groups.

## 8. Source-extraction trap independently caught

The local plain-text extraction of arXiv v3 Proposition 5.6, printed p. 11, omits the overline on B1. Direct visual inspection of the PDF confirms that the conclusion is membership in the **closure of coboundaries**. The truncation argument only gives convergence of coboundaries; a later spectral-gap condition supplies the stronger conclusion in its stated setting.

The frozen packet does **not** misuse this proposition or claim that every formal cocycle for an arbitrary finite-measure-preserving action is an actual coboundary. Its endpoint argument uses Theorem 5.4 instead. This is a successfully passed adversarial check, not a repair request.

The supplementary source-only review is included in source-review/PRIMARY_SOURCE_REVIEW.md. Its local-source verification limits are narrower than the additional publisher and Lavy–Olivier checks documented in this consolidated report.

## 9. Required repairs, optional clarifications, and final disposition

**Mandatory repairs: none. No HOLD condition identified.**

Optional reader-facing clarifications, unnecessary for validity:

- State explicitly beside Proposition 5 that quotient-distance representatives are chosen approximately; no minimizer is assumed.
- Keep the warning that L0 cohomology uses the p-dependent action, and identify “measurable cohomology” as coefficient-module terminology.
- The dense-range observation for unbounded negative cycles would make the ordinary-versus-reduced distinction especially transparent.
- Retain the p>=1 restriction whenever quoting the published formal theorem, even if a condensed OWR summary looks broader.

The remaining substantive obstacle is exactly the one identified in the packet: none of the five routes eliminates or constructs a genuinely nonformal intermediate class while maintaining the required two endpoint vanishings in the same Lamperti family. The diffuse nonsingular case without an equivalent finite invariant measure and the full p<1 problem are not solved here.

**Final disposition: PASS as five substantive partial attempts, with all scoped propositions verified and the original target still unsolved at 5/5.**
