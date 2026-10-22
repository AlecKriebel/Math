# Fresh analytic adversary: PR 1241 / problem 11000082

**Verdict: PASS for the exact submitted mathematical claim, with its named standard theorem imports. No required mathematical repair was found.** This is a candidate-aware adversarial review, not formal certification, human peer review, or a priority clearance.

## Claim and success criterion

Fix a closed oriented surface of genus `g >= 2` and an integer `k >= 3`. Write `Gamma_0 = pi_1(S)`, `Gamma_(j+1) = [Gamma_0,Gamma_j]`, and `I_g(j) = ker(Mod_g -> Out(Gamma_0/Gamma_j))`. For every positive integer `N`, the target is a real number `r > 0` and at least `N` distinct conjugacy classes in the **ambient orientation-preserving** group `Mod_g`, represented by pseudo-Anosovs of this one fixed `I_g(k)`, with log dilatation `r`.

Farb's printed p.51, Question 7.6 and its preceding multiplicity discussion, is the inspected original target. The definition of the filtration on printed p.14 matches the submission. The candidate proves this ambient version, so there is no reliance on interpreting multiplicity as only subgroup conjugacy. The spectral value may depend on `N`; primitivity and infinite multiplicity at a single fixed value are outside the claim. [Original sourcebook](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf).

All eight files in `submitted/` were read. Their historical acceptance statements were treated as assertions to check, not evidence for correctness. Fresh source retrievals and inspected passages are recorded in `SOURCES_RECEIPT.json`; byte identities are separate from mathematical inspection.

## Dependency and attack ledger

| Step attacked | Disposition and reason |
|---|---|
| Separating filling pair in every fixed genus | PASS. Aougab-Taylor Lemma 2.2 has the required `g >= 2, p = 0` scope; its complete statement and proof were inspected. The numerical bound is unused. The candidate's independent genus-two construction also passes the checks below. [Primary paper](https://arxiv.org/pdf/1510.00995). |
| Congruent-square construction and twist matrices | PASS. Specializing the one-by-one intersection matrix to `[n]` gives equal side lengths. Minimality excludes unmarked bigons. The affine shear parameters are `n` and `-n`. |
| Faithfulness and all nonperipheral words hyperbolic | PASS. For `n > 2`, the two-parabolic fundamental domain has just the two stated cusp types. The freeness proof makes the derivative faithful. Leininger Section 5.1, Lemma 6.3 and its proof, and the complete proof of Theorem 6.1 / Proposition 6.4 were inspected. |
| Full disk stabilizer and unique invariant disk | PASS as explicit standard imports. The affine realization preceding Theorem 3.1, its derivative/dilatation statement, and Theorem 3.2 have precisely the required scope. These are statements about the entire stabilizer. [Primary Leininger paper](https://arxiv.org/pdf/math/0304163). |
| Depth indexing | PASS. The candidate's `L_1(F)` is the zero-indexed lower-central term in the cited convention. The containment in the proof of FLM Proposition 4.8 agrees after this shift. An independent automorphism-filtration justification is supplied in `DERIVATIONS.md`. [FLM primary paper](https://arxiv.org/pdf/math/0603675). |
| Rank-two subgroup at fixed depth | PASS. The nested commutator never vanishes; its conjugate by `B` cannot commute with it. Nielsen-Schreier and Hopficity justify that the displayed generating pair is a free basis. Every nonidentity element has zero `F`-abelianization, excluding both cusp types. |
| Entire stabilizer has integral derivatives in one basis | PASS. The signed saddle-holonomy span is a rank-two sublattice of `Z^2`; every affine derivative preserves it in both directions. The argument works with half-translation sign ambiguity and regular square vertices. |
| Uniform ambient fusion | PASS. The finite covering core gives one possible lift of a fixed cyclic word from each vertex. The bound is independent of word length and power exponent. Passing through the index-six commutator subgroup gives the fixed constant `C = 6|V(Y)|`. |
| Mapping-class conjugators are controlled | PASS. Uniqueness of the invariant disk forces every relevant conjugator into its full stabilizer. Derivative conjugacy is a necessary consequence, which is the direction required. A finite derivative kernel does not invalidate the bound. |
| Equal-trace words | PASS. Horowitz Example 8.2 and its complete proof give `2^m` nonconjugate nonidentity words for every `m`, with an identity valid under every `SL_2` representation. The universal convention and polynomial input were also inspected. [Horowitz primary paper](https://www.math.purdue.edu/~eremenko/Pdf/horowitz.pdf). |
| Spectral normalization and conclusion | PASS. For lifted trace `t`, hyperbolicity gives `|t| > 2` and spectral radius `(|t| + sqrt(t^2-4))/2`. This is the dilatation. The ambient class count is at least `ceil(2^m/C)`, with `g,k,H,C` fixed first. |

The lattice, subgroup, covering-core, and conjugacy deductions are checked in detail in `DERIVATIONS.md`. They do not use source-author code or finite experiments as substitutes for proof.

## Boundary and counterexample attempts

1. **Genus two.** Two sphere curves crossing four times divide either side of either curve into three disks. One branch point per complementary disk gives a connected degree-two branched cover with Euler characteristic `-2`. Each base curve has three branch points on either side, so its preimage is one separating curve; its two sides are once-holed tori. Every face lifts to a disk. A downstairs polygon has at least two sides, so its lift has at least four; upstairs minimality and intersection eight follow. The genus-two center and possible stabilizer kernel cause no additional fusion problem.
2. **Critical two-parabolic parameter.** The exceptional parameter `n = 2` would allow a third cusp type and break the stated zero-abelianization shortcut. It cannot occur: Euler characteristic gives `n >= 2g-1`, and separation makes `n` even, so `n >= 4`.
3. **Nonorientable foliations.** No global abelian differential, globally signed holonomy, or orientable stable foliation is assumed. Using both signs of saddle holonomy handles the half-translation atlas.
4. **A larger stabilizer or nonfaithful derivative.** No finite-index claim for the twist group or stabilizer is made. Only containment of derivatives in `SL(Lambda)/{+/-I}` and faithfulness on `H` are used. Even many lifts of a derivative conjugator cannot create more `H`-classes than the derivative fusion bound permits.
5. **Powers and cyclic rotations.** The covering argument counts lifts of a fixed cyclically reduced word, rather than arbitrary starting positions in a growing word. Thus proper powers introduce no factor depending on exponent or length. No primitive representative is silently selected.
6. **Changing genus, depth, subgroup, or common value.** Only `m` varies after construction. `H` and its finite core remain fixed. The value may vary; unbounded multiplicity does not require it to be distinct for different `m` or fixed for all `m`.
7. **Accidental trace degeneracy.** Universal trace identities are evaluated in an actual lift of the fixed free representation. Faithfulness and pure hyperbolicity independently rule out identity, elliptic, or parabolic words and hence rule out `|t| <= 2`. No generic-representation assumption enters.

These attacks yielded no counterexample or unsupported transfer of the central difficulty.

## Required changes and limits

Required changes: **none** for mathematical validity within the stated scope. The submitted audit supplies the free-basis justification that is compressed in the main proof.

The deepest Teichmuller inputs remain imported theorems. Their actual statements in Leininger were independently read, but that paper collects the underlying results rather than proving them there. The original Bers paper was not obtained: a Project Euclid PDF attempt returned HTML. Accordingly this review does not claim to have inspected Bers' original proof or to have rederived the classification from first principles. Aougab-Taylor's existence theorem is likewise imported; its proof uses genus-two and genus-three seeds, and the present review independently reconstructs only the genus-two seed. These are explicit source boundaries, not newly discovered gaps in the theorem's hypotheses.

No new mathematical experiment was run. File hashing, extraction, rendering, and receipt validation are custody operations. Historical optional trace computations in the submission are neither rerun nor relied on. No claim is made about originality, current openness, publication precedence, primitive spectra, the simple-length-spectrum question, or infinite multiplicity at one value.

**Strongest verified result:** the complete submitted construction proves unbounded multiplicity in every fixed `I_g(k)`, `g >= 2, k >= 3`, counted in ambient orientation-preserving `Mod_g`, conditional only on its correctly scoped named standard imports. **Exact remaining mathematical gap at this import level:** none found.
