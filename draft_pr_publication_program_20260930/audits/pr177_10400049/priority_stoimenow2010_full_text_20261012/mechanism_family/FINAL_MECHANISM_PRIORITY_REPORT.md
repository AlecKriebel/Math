# Stoimenow 2010: independent mechanism and equivalence priority audit

Audit UTC: 2026-10-13T03:18:10.624827+00:00
Owner task complete: 100%. Overall PR177 discovery estimate remains 40%.

## Disposition

The supplied 2010 paper is strong prior art for the twist-polynomial mechanism used by PR177. Its published polynomiality statements, together with elementary properties of linking numbers, suffice to derive the exact proposed principal-ideal counterexample in a few steps. No additional finite type theorem, conjectural character-extension property, or computation is needed.

The paper does **not** itself assert the proposed arbitrary-ideal actual-link Nullstellensatz refutation, the ideal `g(4g-1)V`, a character at a nonintegral twist parameter, or the inequality between the radical of that ideal and the ideal of its actual-link zero set. Its algebraic-dependence and norm assertions are different statements. The legitimate classification from this source alone is **published tools with an elementary additional algebraic corollary**, not **an already-published equivalent radical/zero-set assertion**. “Additional” means absent as an assertion in this paper; it is not a global claim that nobody previously made the deduction.

PR177 should credit the polynomiality mechanism explicitly and scale any contribution claim to the exact corollary/formulation that survives a broader priority audit. This audit gives no historical novelty clearance and no recommendation to promote the result as a new finite type mechanism.

## Source and independence

Read-only supplied source: A. Stoimenow, *Application of Braiding Sequences, I: On the Characterization of Vassiliev and Polynomial Link Invariants*, *Communications in Contemporary Mathematics* **12**(5) (2010), 681–726, DOI `10.1142/S0219199710003944`.

The PDF checksum is `86b9466b99f2cf67656b49311e67b97267c807d6c0f99d746a874c74379ca508`. Complete main prose, proofs, and references were read from the private extraction, and the material formulas and conventions were visually checked. Read coverage and first assessment were independently authored and sealed 0444 at `2026-10-13T03:13:08.178508+00:00`, before receiving any root substantive comparison. No sibling report has been read. The subsequently received root positive-characteristic prompt is addressed only in `POST_SEAL_POSITIVE_CHARACTERISTIC_BOUNDARY.md`; it does not alter the first assessment or enter the characteristic-zero proof.

The PDF, extraction, and rendered figures remain private evidence and are not deliverables for redistribution. This report is an independently written paraphrase and derivation.

## Exact target

Let `X_m` be oriented actual links in `S^3` with a fixed `m >= 2` components, including split links, and let `V_m` be the unital commutative complex algebra of all ordinary finite-order finite type invariants on `X_m`, with pointwise multiplication. The same argument applies to the ordinary finite-order algebra `V` on links of all finite component counts. In the latter setting a restriction to a fixed component class is enough; no uniform growth theorem over component counts is assumed.

For an actual link set

`g(L) = sum_(i<j) lk_ij(L)^2`, `h = g(4g-1)`, and `I = h V_m` (or `h V`).

The conclusion to check is

`Z_actual(I) = {L : g(L)=0} != empty`, but `g not in radical(I)`.

This refutes the identity `I(Z_actual(J)) = radical(J)` for arbitrary ideals `J` in the target full algebra. It does not assert a failure of the classical Hilbert Nullstellensatz for a polynomial ring evaluated on all of its complex points.

Component labels are unnecessary for `g`: although an individual indexed linking number uses labels, the sum of their squares is invariant under relabeling. The chosen test family can be labeled for computation without changing `g` or restricting the ambient invariant algebra.

## What the paper actually supplies

1. **Finite type definition and scope.** Section 2.5, journal pp. 689–690, defines the crossing-difference extension, requires orientations, allows values in `C`, and fixes an arbitrary component number for the link theory. This is ordinary finite-order theory, not a formal completion.
2. **Braiding polynomiality.** Definitions 2.2–2.3, pp. 690–691, define replacing an existing crossing by an odd number of half twists, with parallel or antiparallel choices. Theorem 2.1, p. 691, states that degree at most `d` is equivalent to polynomial behavior of total degree at most `d` on every braiding sequence. The paper explicitly attributes the central approach and Theorem 2.1 to reference [63], published in 2000. Its introduction also identifies earlier one-site twist sequences [68], 1994, and multi-site work [63]. Those references are leads, not sources independently inspected by this owner audit.
3. **Growth.** Theorem 1.1, p. 682, with proof concluding pp. 702–703, characterizes finite type invariants using braiding polynomiality plus a polynomial crossing bound. This extends the growth analysis to fixed-component links, tangles, and graph embeddings.
4. **Norm and filtration.** Definitions 4.1–4.2, Theorem 4.1, and Corollary 4.1, pp. 703–705, extract the order from upper/lower asymptotic crossing growth and give norms on successive order quotients. They do not claim a radical/zero-set theorem or characterize all algebra homomorphisms to `C`.
5. **Algebraic dependence.** Section 4.4, pp. 708–710, concerns polynomial relations among finite selections from finite type invariants and specified polynomial evaluations, detected on special alternating knots or specified braid knots. Extended and periodic polynomial behavior appears here. These assertions concern identities valid on all knots, not an arbitrary ideal's conditional zero set. In particular, Theorem 4.4 does not imply that every complex character is evaluation at an actual knot/link. It is also stated in the knot setting, with a preceding remark that the material generalizes to links; this is not an explicit fullV link-ideal theorem.
6. **Link polynomial coefficient questions.** Problem 5.1, p. 714, asks stronger algebraic-independence/surjectivity questions for polynomial coefficients. Those coefficient invariants and questions are not the full finite type invariant algebra in the target.

Reading the remainder of the paper found coefficient independence, mutation/determination, and other-manifold results; none supplies the missing explicit ideal/character assertion. This source-wide negative observation is limited to this exact supplied paper.

## Checkable full-algebra deduction

### 1. Every ambient invariant restricts polynomially

Take

`L_n^(m) = closure(sigma^(2n)) disjoint_union U_(m-2)`, for `n in Z`,

with both braid strands oriented parallel and `U_(m-2)` split unknotted components. For `m=2` there are no added components. Let `v` have finite type order at most `d`, and put `a_v(n)=v(L_n^(m))`.

The forward difference `a_v(n+1)-a_v(n)` is a single singular-crossing evaluation: insert a block of two positive crossings; switching one crossing changes `sigma^2` to `sigma^(-1)sigma=1` after Reidemeister II cancellation. Applying `r` forward differences inserts `r` such difference blocks. Each difference block has a singular factor. In braid group algebra notation,

`(sigma^2-1)^r = sigma^r (sigma-sigma^(-1))^r`.

Closing against `sigma^(2n)` and adding the fixed split components produces the alternating resolution of an `r`-singular link. Thus `Delta^(d+1) a_v(n)=0` for all integers `n`.

Equivalently there is a unique polynomial

`P_v(t) = sum_(r=0)^d Delta^r a_v(0) binom(t,r) in C[t]`

agreeing with every `a_v(n)`. Newton binomials are polynomials over `C`; denominators are invertible. Agreement for negative integers follows from the same difference recurrence, and agreement on all nonnegative integers already gives uniqueness.

This is the paper's published braiding-polynomial mechanism, reconstructed directly from its finite type definition to remove any non-split/split convention ambiguity. The proof applies to **every** `v` in the full finite-order algebra. It is not merely a computation for linking numbers or a selected polynomial subalgebra.

### 2. Restriction is a homomorphism, degree by degree

Define `rho_m(v)=P_v(t)`. For `u,v` in the full algebra, the restrictions of `u+v`, `uv`, and `1` agree at every integer with `P_u+P_v`, `P_u P_v`, and `1`. Polynomial uniqueness gives

`rho_m(u+v)=rho_m(u)+rho_m(v)`, `rho_m(uv)=rho_m(u)rho_m(v)`, `rho_m(1)=1`.

The product `uv` is finite type of order at most `deg(u)+deg(v)`, as follows by distributing the crossing differences between the two factors. Therefore `rho_m` is a unital complex-algebra map on the filtered union of all finite orders. No fixed cutoff common to all invariants is needed.

Consequently `chi_m(v)=rho_m(v)(1/2)` is a character on the **whole** algebra. On the all-component algebra, compose restriction to `X_m` with this map. No theorem extending a character from `C[g]` to the full algebra is being assumed.

If the ambient oriented theory includes the total linking number `sum lk_ij`, then its restriction is `t` and `rho_m` is surjective onto `C[t]`. Surjectivity is unnecessary for the counterexample.

### 3. The actual zero set and radical separation

Each `lk_ij` is an integer on actual links; therefore `g(L)` is a nonnegative integer. Hence `h(L)=0` if and only if `g(L)=0`, because `g(L)=1/4` cannot occur. Since `1` is in the algebra, the zero set of the principal ideal equals the zero set of its generator. The `m`-component unlink has `g=0`, proving nonemptiness.

Linking number has finite type order at most one; the crossing-difference calculation gives a constant first derivative and zero second derivative. The sum of squares is therefore finite type of order at most two, including in the unlabeled and all-component settings. Thus `g` and `h` are elements of the target algebra.

On the test family the only nonzero linking number is the one between the two braid components, with value `n`. Therefore

`rho_m(g)=t^2`, `rho_m(h)=t^2(4t^2-1)`,

and

`chi_m(g)=1/4`, `chi_m(h)=0`.

The character annihilates the whole ideal `hV_m`. If some positive `g^N` were in that ideal, applying the character would give `(1/4)^N=0`, impossible in `C`. Thus `g` vanishes on the nonempty actual zero set but is not in the ideal's radical.

The same obstruction can be checked without character terminology. An equality `g^N=hv` would imply the polynomial identity

`t^(2N)=t^2(4t^2-1)P_v(t)`.

At `t=1/2` the left side is nonzero and the right side zero. This covers every positive `N` and every finite-order candidate `v`.

## Odd/even, split, and completion boundaries

- **Odd local parameters, even total exponents.** Use the Hopf generating diagram `sigma^2`. Keep one crossing and replace the other by an odd parallel braiding `x=2n-1`. Its total exponent is `x+1=2n`, so the number of braid-closure components stays two for every integral `n`. Mixing the knot family `closure(sigma^(2n+1))` into the proof would be an unjustified change of component class. It is not required.
- **The nonintegral evaluation is formal polynomial evaluation.** At `n=1/2`, the local parameter is `x=0`, outside the paper's odd braiding domain. This is allowed for the extension polynomial; it is not evaluation of a two-component actual link at an even/odd mixed braid exponent. Treating `closure(sigma)` as the same link-family evaluation would be false: it has one component, and its `g` is zero.
- **Non-split convention.** Journal p. 688 states a default convention of non-split links and reduced diagrams. The tangles/graphs treatment includes disconnected objects explicitly on p. 689, and the polynomiality mechanism is elementary. Nevertheless the exact `m>2` split-union family and the `n=0` unlink should not be cited as falling under the non-split convention without explanation. The direct singular-difference proof above supplies the required explanation. Polynomial uniqueness could already be obtained on positive integral `n` for `m=2`, where the family is non-split.
- **Full algebra versus selected family.** A selected family alone suffices as a test only because every ambient finite-order invariant has a restriction polynomial and pointwise multiplication becomes polynomial multiplication. This is proved above. No injectivity of `rho_m` is needed; invariants vanishing on the family can lie in its kernel.
- **All component counts.** Fixed-component restriction defines the needed character on the all-component algebra. Source growth constants are for fixed component number; they must not be silently promoted to a global bound for all component counts. Degree-zero functions of component count already show why such a promotion requires separate hypotheses.
- **Completion.** The proof uses finite-degree restriction polynomials. It does not automatically define evaluation at `1/2` on a completed algebra of infinite formal series; convergence and topology would require extra hypotheses. This boundary does not affect the stated uncompleted target.
- **Characteristic zero.** Newton-binomial interpolation and infinite integer polynomial uniqueness are used over `C`. They do not transfer verbatim to positive characteristic. The separate additive note identifies a concrete boundary in the paper's torsion discussion; that issue does not undermine the characteristic-zero deduction.

## Degree and norm consequences: audit deductions, not paper assertions

The restricted polynomial degree provides the lower order bound, while the linking-number product calculation supplies the upper bound. Thus

`deg(g)=2`, `deg(h)=4`, and `deg(g^N)=2N` for positive `N`.

For every diagram with crossing count `c`, write `c_ij` for crossings between components `i` and `j`. Then

`sum |lk_ij| <= (sum c_ij)/2 <= c/2`, hence `0 <= g <= c^2/4`.

It follows that `g^N <= c^(2N)/4^N` and `|h|=4g^2-g <= c^4/4`. On `L_n^(m)`, the crossing number is exactly `2|n|`: the standard diagram achieves this bound and linking number forces at least `2|n|` intercomponent crossings. Consequently, with the paper's liminf/limsup crossing-growth construction applied to the full actual-link classes,

`||g||=1/4`, `||h||=1/4`, `||g^N||=4^(-N)`.

The `m=2` lower bounds use non-split links for every nonzero `n`, and thus also conform to the paper's non-split default. For `m>2`, the full-class formulation in this target includes the added split components; no claim about an unchanged source convention is needed.

These sharp norms are simple extra computations for the proposed invariants, not statements located in Stoimenow 2010. They do not themselves separate `g` from the radical. In particular, the pointwise actual-link quotient

`v_N(L)=g(L)^(N-1)/(4g(L)-1)` when `g(L)>0`, and `v_N(L)=0` when `g(L)=0`,

satisfies `h v_N=g^N` as a function on actual links. For `N=1,2` it is bounded, and for `N>=2` its magnitude is at most `g^(N-2)/3`. Thus it has a polynomial crossing bound. Its twist restriction would be the nonpolynomial rational function `n^(2N-2)/(4n^2-1)` away from `n=0`, so it is not finite type. Polynomial growth alone cannot rule it out. The obstruction is precisely polynomial restriction, not simply its asymptotic order.

## Exact priority comparison

The old theorem plus known linking integrality **implies** the target counterexample after the explicitly supplied character/ideal deduction. The target counterexample does not conversely characterize finite type invariants or recover the old theorem. There is no demonstrated logical equivalence between those published theorem statements and the arbitrary-ideal refutation.

Likewise the paper's ability to detect global polynomial identities on selected actual knot classes says those evaluations separate certain invariant expressions. It does not say that the evaluations exhaust the complex spectrum, and it does not identify the radical of every ideal from a conditional actual-link zero set. A faithful function algebra can still possess complex characters outside its actual evaluation set, as the deduction here demonstrates.

The strongest supported conclusion is therefore narrow and adverse to broad mechanism novelty: **the exact PR177 example is already a readily checkable corollary of published twist-polynomial tools; this paper has not been found to publish the same ideal/actual-zero-set assertion.** The exact remaining historical gap is whether another prior source explicitly stated this or a mathematically equivalent counterexample. No answer to that gap is manufactured from a keyword search, from this one paper's bibliography, or from the existence of an elementary deduction.

## Reproducibility and limits

The core evidence is the complete source read with precise journal locators, the visual convention checks, and the algebraic proof above. No numerical sampling is being substituted for a proof of fullV polynomiality, the character's multiplicativity, nonemptiness, or non-radical membership. The independent first sealed files and their hashes are preserved unchanged. No external contact, chat messaging outside this agent team, or Git/ref/index/native remote/global modification was performed by this owner task.
