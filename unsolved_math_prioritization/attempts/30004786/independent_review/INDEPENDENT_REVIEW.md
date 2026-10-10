# Independent final review: sigma–rho Poisson summation / 30004786

**PASS_SCOPED_PARTIALS. No mandatory mathematical correction. The original source-scoped implication remains unsolved after five substantive author turns.** The package proves conditional analytic implications and formulation obstructions; it does not prove or refute general Langlands continuation, construct general global transfer, or derive its strengthened analytic hypotheses from the weak source premise.

This review binds `FROZEN_MANIFEST.json` SHA-256 `5895d268696df9704b20c0f65a44b649ae2d55f8ff39565c6a0f02a5ba4dc480`, including all 15 listed artifacts. `PARTIAL_RESULTS.md` SHA-256 is `88a2512f8fcab3709c2242415c0bc14c077ebf7978d50f42a6243c0bfcbb1fdf`. All author hashes and all three primary PDF hashes were verified. Reviewed 2026-10-01. No novelty or priority certification is made.

## 1. Exact source and hypothesis boundary

I read the actual OWR39/2021 contribution, printed pp2113–2115, and the relevant definitions, theorem proofs and conjectures in Jiang–Luo, *Certain Fourier operators and their associated Poisson summation formulae on GL1*, Pacific J. Math. 326 (2023), 301–372. The OWR display on p2114 and the published refinement on pp363–364 were also checked visually.

The [OWR source](https://doi.org/10.4171/owr/2021/39) states the L-function conjecture for a number field, a split reductive group, a finite-dimensional dual-group representation, and cuspidal sigma. Its Conjecture 1.3 asks for two nontrivial invariant linear functionals related by the Fourier operator. It does not specify actual theta values or boundary asymptotics in that display. The following expectation connects the Poisson program to the L-function conjecture. The later sentence about split classical groups and the standard representation describes a possible construction route, not a restriction of the preceding arbitrary-pair formulation.

The [published Jiang–Luo paper](https://msp.org/pjm/2023/326-2/pjm-v326-n2-p05-p.pdf), Conjectures 1.5 and 7.4, distinguishes the weak formula from a restricted-theta refinement. The latter's displayed normalization explicitly names the sigma-side functional; the candidate appropriately assumes both normalizations in its bilateral theorem rather than treating the second as an immediate consequence of one printed sentence. This cautious formulation does not assert that the authors intended an asymmetric theorem.

The local-transfer and contragredient compatibility assumptions are essential and retained. Theorem 6.2 supplies the source uniform bound in its unitary-sigma setting. The partial theorems also explicitly assume the necessary bounds for pi and its dual; they do not silently extend that cited theorem to every nonunitary representation. Global automorphy of the transferred pi is nowhere used as an input.

## 2. Turn 1: the analytic theta-to-L implication

### Uniform large-norm decay

Lemmas 5.2 and 5.3, and the proof of Theorem 5.4, provide precisely the needed local bounds. After multiplying by one sufficiently positive absolute-value power, all exceptional finite factors are bounded on compact additive support, good finite factors are bounded by 1 on the integers, and the Archimedean product is bounded near coordinate zeros and rapidly decreasing in Euclidean norm. Smooth extension across coordinate zeros is unnecessary and is not claimed.

The compact norm-one idele class group has a compact representative set in the norm-one ideles. A compact finite-idele set is contained in the units outside a common finite set, with bounded valuations at the remaining places. Hence one common fractional-ideal lattice suffices for all representatives. The Archimedean multipliers have a uniform positive lower singular value. Since nonzero lattice vectors have positive minimum norm and the sum of their inverse M-th powers converges for M greater than the real dimension, retaining the radial scale gives the displayed bound `r^(-b-M/d)`. Arbitrarily large M yields uniform rapid decay. Complex places contribute squared absolute values, so the section scaling every Archimedean coordinate by `r^(1/d)` has adelic norm exactly r. There is no unjustified uniformity over a noncompact unit domain.

### Absolute unfolding and a common half-plane

There is a fixed right half-plane for all members of the algebraic restricted tensor product, not a choice of s depending on infinitely many factors. One can see this directly from the source bound: if a good-place basic function satisfies `|phi_v(x)||x|^b<=1` on integral x and equals 1 on the units, its absolute local integral at real part sigma is bounded by

`(1-q_v^(-(sigma-1/2-b)))^(-1)`.

The product converges once `sigma-1/2-b>1`, by the ordinary Dedekind-zeta bound. There are only finitely many exceptional factors in each tensor, and Lemma 5.2 has a representation-dependent uniform local exponent for their convergence. Archimedean infinity is rapid. Thus absolute unfolding in a common sufficiently positive half-plane is legitimate. The same reasoning applies to the dual space, with the larger of the two exponents. This also justifies the evaluations used in turns 2 and 4.

Actual theta inversion supplies the small-norm rapid bound from the dual large-norm bound. The compact norm-one quotient then gives entire Mellin integrals; on a compact s-set, every differentiated logarithmic factor is absorbed by stronger endpoint decay. Haar inversion preserves the quotient multiplicative measure and sends `s-1/2` to `(1-s)-1/2`, giving the correct reflection. No absolute convergence at the small end of the *unperiodized* integral is inferred from cancellation of a theta sum; unfolding is used only in the separately justified right half-plane.

### Nonzero test and completed factors

Theorem 7.1 identifies the local circle subspace with compactly supported smooth functions. At two distinct finite places, choosing one compact unit function and one inverse-Fourier image of a compact unit function therefore creates a legal double-circle test. Theorem 3.10 uses the opposite additive character for the inverse; the candidate uses exactly that inverse. Its local functional equation gives a nonzero meromorphic Mellin factor at the inverse-Fourier place. Exceptional compact Archimedean factors can have strictly positive Mellin evaluations on the real axis. The unramified Euler product is nonzero sufficiently far right.

The finite multiplier includes every exceptional local L-factor, including the Archimedean factors. The local functional equations give its dual transformation by the product of the exceptional epsilon factors, with good-place epsilon equal to 1 in the stated normalization. This is a completed-L statement, not an incomplete-product shortcut. Dividing and cancelling a nonzero meromorphic function is valid as an identity and does not require pointwise nonvanishing everywhere. No entire-L, pole-location or strip-growth theorem follows and none is asserted.

## 3. Turns 2–4: weak functionals, covariance and Fourier square

The algebraic transport lemma is correct. The global convergent evaluation is invariant under principal ideles by the product formula, and Fourier covariance transports invariance to the other space. Local covariance has the right character and half-power: the change of variables contributes `chi(a)^(-1)|a|^(1/2-s)` on both sides. The source Mellin uniqueness makes this an operator identity. The claims are on the algebraic restricted tensor product with explicitly stated weighted-integral seminorms; no unproved continuity on a larger completion is asserted.

The inverse Fourier transform must be distinguished from applying the dual transform with the same additive character. Proposition 2.6 and additive Fourier square give the latter square on a determinant fiber. Replacing g by -g contributes determinant translation by `(-1)^n` and the central-character scalar `omega_pi(-1)`. The local value at -1 is ±1, and it is 1 at almost all good finite places, so the global product kappa is well-defined. The reverse-order square has the same scalar. This establishes the double-circle Fourier stability used in turn 3; translations preserve the spaces and their compact local factors.

With both explicit theta restrictions, applying the weak identity to a translated test gives actual theta inversion. Without the second restriction, that argument stops. This is accurately marked as an additional hypothesis.

For coherent identities in both directions, precomposing twice gives `E=kappa E` because the remaining determinant translation is principal. Thus kappa=1 is necessary for nonzero coherent functionals. Under that explicitly assumed condition, the two symmetrized functionals do satisfy both identities. Their two summands have distinct norm characters `r^a` and `r^(-a)` with a>0, preventing total cancellation. The self-dual specialization is likewise valid. These arguments do not establish central-character compatibility for arbitrary unproved local transfers; the candidate correctly leaves that compatibility conditional.

A permitted test with nonzero convergent Mellin evaluation can be chosen after avoiding a discrete set of exceptional Mellin zeros and poles. On that test the constructed functional's norm orbit is a nonzero one- or two-power expression, incompatible with arbitrary rapid large-norm theta decay. This establishes nonautomatic theta normalization of those particular weak functionals. It does **not** prove a logical counterexample with all original arithmetic assumptions and a false L-function conclusion, nor does it rule out a different canonical theta-normalized functional. The package states those limitations correctly.

## 4. Turn 5: finite actual-theta defect

The averaging measure and multiplicative section are fixed consistently. Local uniform theta convergence gives continuity of the averages, while the proved uniform radial bound gives rapid upper tails. The hypothesis concerns the actual averaged pair `A(r)-Adual(1/r)` for one nonzero-Mellin test, rather than a defect of a manufactured functional.

Splitting at r=1 gives entire upper-tail transforms. For each power-log term the lower integral contributes

`c (-1)^m m!/(z+lambda)^(m+1)`, with `z=s-1/2`.

The reverse defect is exactly `-B(1/r)`. Its coefficient and logarithmic sign produce the same polar part at the reflected variable -z. Consequently both separately constructed meromorphic continuations agree. Their original convergence half-planes need not overlap. No divergent whole-line Mellin integral of a power-log term is evaluated, and no invalid overlapping-half-plane argument is used.

The pole list applies to the continued test-function integral before division by local multipliers. Such division can change the L-function pole set, and the candidate does not claim otherwise. The same completed local-multiplier calculation as in turn 1 then yields the conditional functional equation.

For the finite-dimensional boundary-module criterion, finitely many point evaluations separate a finite-dimensional space of continuous functions. They make its translation matrices continuous; a continuous finite-dimensional representation of the real additive group is an exponential of a fixed matrix. Jordan form gives exponential polynomials. Thus the stated additional module hypothesis really implies the finite power-log defect.

Its nonautomaticity argument is correctly limited. A nonzero averaged theta function is obtained from nonzero unfolding, and its rapid upper decay prevents it from being an exponential polynomial. Subtracting it from a one- or two-power orbit therefore need not lie in a finite-dimensional translation module. This does not rule out cancellation between the two non-finite-dimensional differences, or prove that the actual arithmetic theta defect fails the finite-defect hypothesis.

## 5. Verification and disposition

- All **15 frozen author artifacts** and **3 primary PDFs** hash-match
- Author's **552 exact controls** replay byte-identically in a separate copy
- Separate checker passes **405 exact controls**, including antiderivative reconstruction, continuous piecewise actual-pair defect models, reflected polar parts, half shifts, nontrivial two-space Fourier scales and squares, changed-basis translation modules, and completed local multipliers
- The analytic verdict rests on the source and proof audit above; neither finite checker proves adelic bounds or Langlands theory

The strongest valid results are the three explicitly conditional theta/boundary-to-L implications and the scoped nonautomatic-normalization obstructions. The original weak-premise implication has not been completed. The disposition **unsolved, 5/5** is correct. Preserve the explicit extra hypotheses, unitary/growth scope, algebraic domain, local normalizations, and absence of any claimed arithmetic counterexample in the publication.
