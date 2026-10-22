# Independent audit of the constant obstruction and integral trace repair

Date: 14 October 2026 UTC. Shared mathematical pass: PASS 1/5. This is a fresh independent audit of the completed proof notes, not another mathematical pass. No author proof file or remote repository was modified.

## Verdict

**Accept the stated partial mathematical results, with their written scope restrictions.** No mathematical defect was found in the two reviewed proofs. This acceptance does not certify the requested Eisenstein map, a formula for its relative values, or a new result in the literature.

The accepted results are:

1. The naive substitution of `Z[1/6]` for `Z[1/30]` in the unmodified trace-fixed Gersten complex fails for full CM by the maximal order of `Q(sqrt(-5))`: its left kernel contains nonzero constant 5-torsion.
2. For a product of two elliptic curves over a characteristic-zero field, quotienting **all constants before taking trace-fixed parts** gives an exact sequence at the first two nonzero terms:

   `0 -> (C_2/C)^tf -> C_1^tf -> C_0^tf`.

3. The original left kernel is exactly `C^tf`. For maximal imaginary-quadratic CM this is `K_2(L)[5]` when 5 ramifies, and zero when 5 is unramified, with the coefficient interpretation specified in the proof for a general field.
4. When 5 is unramified in the maximal CM order, the full CM norm traces restore the unquotiented left-exact sequence over `Z[1/6]`.
5. Given a trace-fixed residue primitive, the quotient construction gives the stated unique quotient-valued cocycle and its cohomology class. Its ordinary cocycle-lifting obstruction lies in `H^2(Gamma,C)`. The separate requirement of trace-fixed representatives is correctly not assumed.

Here `C_2`, `C_1`, and `C_0` are the function-field, divisor, and point terms of the Gersten complex; `C` is the image of the constant `K_2(L) tensor Z[1/6]` group. The word "exact" above makes no assertion at `C_0` or about a degree map.

## Frozen reviewed proofs

The complete contents, rather than only the preliminary proposal, were inspected:

- `CONSTANT_FIVE_TORSION_OBSTRUCTION.md`: SHA-256 `3538c215bb6295659adfb5c3e902e6cca036f1a416e8665ee6273c5c68d228ca`.
- `CONSTANT_QUOTIENT_REPAIR.md`: SHA-256 `6943210fbd4d1761d2317e0715491e00688a7a803197d60c6c9c49561f92f9c0`.

The files are in the companion `pass1_five_torsion_review` directory. Subsequent substantive changes require renewed review. The audit also read the frozen construction contract and the source passages listed below.

## 1. Constant obstruction: each standard-input obligation checks

### Existence of nonzero order-5 constants

The exact number-field localization sequence has finite kernel `K_2(O_L)` and surjects onto the direct sum of the finite residue-field multiplicative groups. Its short exact form uses vanishing of finite-field `K_2`, the stable `SK_1` theorem for rings of integers, and Garland's finiteness input. These are genuine standard inputs, not consequences claimed newly proved by the candidate.

A place over the single rational prime 11 suffices: its residue cardinality is `11^f`, hence its multiplicative group has an element of exact order 5. A lift has finite order divisible by 5 because five times the lift is in the finite kernel. Multiplying an element of exact order `N` by `N/5` then gives an element of exact order 5. This does not assert that its tame residue remains nonzero. No unsupported prime-distribution or splitting claim is present.

### Injection into the function field

At the rational origin, the regular local ring of the surface injects into its completion `L[[u,v]]`; its fraction field embeds into `L((u))((v))`. The composite of the two Milnor residue specializations restricts to the identity on constant `K_2^M(L)`. The formula using multiplication by `{t}` followed by the degree-three residue is sufficient: a group retraction on constants is all that is needed, and no canonical ring-specialization assertion is made. Matsumoto's theorem then gives the required injection for Quillen `K_2`.

Tensoring with `Z[1/6]` preserves this injection and does not kill a nonzero order-5 element. A second conceptual check is the rational-origin retraction on motivic cohomology followed by the Gersten injection into the function-field group.

### Residues, transfer, and the full CM monoid

Both entries of a constant Steinberg symbol are units at every geometric divisor, so the residues vanish. A finite CM endomorphism on the product has degree `N(alpha)^2`, and transfer after restriction multiplies by this degree. It therefore acts on constants by exactly `N(alpha)^2`, not by `N(alpha)`.

For `O=Z[sqrt(-5)]` and `alpha=a+b sqrt(-5)` prime to 5, this square norm is `a^4=1 mod 5`. Choosing exceptional element 5 is legitimate. Thus the argument establishes every allowed CM trace, not just the rational scalar traces.

### Sharp invariant-constant classification

For any fixed exceptional element, allowed scalar traces act on constants by `m^4`. CRT excludes every common divisor prime at least 7 from the numbers `m^4-1`. Choosing `m=2 mod 25` excludes a second power of 5. After inverting 2 and 3, their ideal therefore contains 5. Consequently an eventually fixed constant is killed by 5.

For maximal orders the split and inert norm maps modulo 5 are surjective onto `F_5^*`; a unit of norm 2 gives square norm 4. CRT makes it prime to any prescribed exceptional element, so it kills any possible invariant 5-torsion. In the ramified case the residue algebra is the dual-number algebra and every unit norm is a square, giving square norm 1. This proves both directions of the classification.

The maximal-order hypothesis matters. If an order's conductor is divisible by 5, the same non-etale residue shape can occur even when the quadratic field is unramified at 5. The final proofs explicitly exclude that mistaken extension.

## 2. Integral elliptic correspondences: no rational-only step

Use pushforward correspondences and the projectors `pi_0=[0 x E]`, `pi_2=[E x 0]`, `pi_1=Delta-pi_0-pi_2`. The order of the two factors matters. With the stated convention, `pi_0` acts on classes pulled back from the field, while `pi_2` acts on classes pushed forward from the origin.

The orthogonality checks work integrally: one mixed composition has a dimension drop under pushforward, and the other has the zero first Chern class of a line over `Spec L`. There is no positive-dimensional base line bundle being discarded.

Set `M=O_E(0)` and `P=O(Delta-0 x E-E x 0)`. The symmetric line-bundle identity `[m]^*M=M^(m^2)` and the normalized Poincare identity `([m] x id)^*P=P^m` are identities of line bundles over the base field. Pulling back the diagonal therefore proves, integrally,

`Gamma_[m] = m^2 pi_0 + m pi_1 + pi_2`.

No power of `m` is canceled in a torsion group, and no Chern-character denominator or rational Chow decomposition is used. Exterior products consequently give genuine orthogonal summands on `E_1 x E_2` with scalar pushforward weights 0 through 4. The integral action of Chow correspondences on the relevant motivic groups is available; it is not only an action on rational cohomology.

This argument is for elliptic curves over a **field**. It has not been extended here to the universal elliptic family over a positive-dimensional base, where the elementary origin self-intersection check changes.

## 3. Extreme summands and the annihilator

The weight-4 summand of `H^j(A,R(2))` is `H^j(L,R(2))`, and the weight-0 summand is `H^(j-4)(L,R(0))`, by the origin and structure maps. Their splittings are integral.

- For `j=2`, these are exactly the constants and zero.
- For `j=3`, both vanish: `CH^2(Spec L,1)` has no degree-one cycles of codimension 2, and weight-zero negative cohomology vanishes.

Thus `U/C` and `V`, with `U=H^2(A,R(2))` and `V=H^3(A,R(2))`, are direct sums of weights 1, 2, and 3. They are annihilated by `P_m(T_m)=product_(s=1)^3(T_m-m^s)`.

Its augmentation is `r(m)=product_(s=1)^3(1-m^s)`. For each prime `q>=5`, an allowed integer can be chosen by CRT to have multiplicative order greater than 3 modulo `q`. This excludes `q` from the common divisor. The resulting ideal is the unit ideal of `R`, and finite Bezout supplies the augmentation-one annihilator `Phi`. The printed check `99r(2)-5r(3)=1` is correct.

The argument uses a genuine integral splitting plus a finite monoid-algebra element. It does not rely on exactness of a fixed-point functor or on rational diagonalization.

## 4. Fixed lifts and the unramified-5 refinement

For a fixed residue cycle `y`, its class in `V` is both fixed and annihilated by `Phi`, hence zero. For any ordinary lift `z`, every difference `(T_alpha-1)z` belongs to `U`. Modulo constants, applying `Phi` kills all these differences simultaneously and preserves the residue because its augmentation is one. This proves the asserted invariant lift in `C_2/C` for the **full** CM monoid. The monoid algebra is commutative, so the scalar annihilator commutes with the other traces.

The same argument shows `U^tf=C^tf`; it does not silently replace `(C_2/C)^tf` by `C_2^tf/C^tf`.

When 5 is unramified, the degree differences `1-N(alpha)^2` generate the unit ideal of `R` for every exceptional monoid. Scalar traces exclude primes at least 7; the split/inert norm argument excludes 5. The resulting augmentation-one operator `B` kills constants, while `Phi(U)` is contained in constants. Therefore `B Phi` kills all of `U` and still kills `V`. Applying it to an ordinary lift proves unquotiented middle exactness. This is a complete proof of the restricted left-exact repair, rather than an inference from vanishing invariants alone.

## 5. Cocycle and specialization boundary

The conditional cocycle construction is accepted only with its supplied hypothesis of a trace-fixed `eta` with the specified residue. Theorem A then gives uniqueness and the cocycle identity by injectivity, and changing `eta` changes the cocycle by a coboundary.

The two lifting issues in the final note are correctly separated:

1. For an ordinary cocycle lift, the inverse-image coefficient module gives `0 -> C -> G -> Q -> 0` and obstruction in `H^2(Gamma,C)`. Its vanishing is equivalent to existence of a lift of the cohomology class, with the stated ambiguity.
2. A trace-fixed representative for each quotient value first requires surjectivity after taking eventual invariants. At a fixed monoid, its obstruction is the connecting class in `Ext^1_(R[M])(R,C)`, and eventual invariance permits enlargement of the exceptional element. No vanishing in the ramified-5 case is asserted.

Specialization of a quotient by constants naturally remains a quotient by their specialized images. In particular, if the base and specialization fields are equal, that quotient can remove the entire intended field-valued target. This is why the quotient repair is not a solution of the constant-sensitive construction problem.

## 6. Source checks and non-contradiction

The following public sources support the standard inputs and were checked at the indicated locations:

- Sharifi and Venkatesh, [Eisenstein cocycles in motivic cohomology](https://math.ucla.edu/~sharifi/eisensymbol.pdf), Sections 2.1–2.3 and 6.1–6.2, especially Theorem 6.1.1, Proposition 6.1.2, and Lemma 6.2.1. The general decomposition and the displayed elliptic exact sequence explicitly invert 5. The proof of fixed lifting was compared step by step.
- Lecouturier, Sharifi, Shih, and Wang, [Eisenstein cocycles for imaginary quadratic fields](https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf), Section 3.2, printed pp.21–22. The full CM trace-fixed convention and Proposition 3.2.3 use `Z[1/30]`.
- Bass, [K2 des corps globaux](https://numdam.org/item/SB_1970-1971__13__233_0.pdf), Sections 4, 6, and 7: tame-symbol surjectivity, transfer after restriction, and the finiteness input. Garland's original paper is [A finiteness theorem for K2 of a number field](https://annals.math.princeton.edu/1971/94-3/p08), Annals of Mathematics 94 (1971), pp.534–548. Finiteness is used as a standard theorem; its analytic proof was not independently reproved.
- Milne, [Abelian Varieties](https://www.jmilne.org/math/xnotes/AVs.pdf), Sections 5–6, particularly Corollary 6.6, confirms the symmetric line-bundle identity without rational coefficients.
- Voevodsky, [Triangulated categories of motives over a field](https://www.math.ias.edu/Voevodsky/files/files-original/Dropbox/Published_papers/Motives/Collection/s5.pdf), Proposition 2.1.4 and the preceding definition of Chow correspondences, confirms that the correspondence formalism is not rational-only. The direct higher-Chow push-pull action also follows from the integral operations recalled in Sharifi–Venkatesh Section 2.1.

The retained source PDFs for Sharifi–Venkatesh and Lecouturier et al. have SHA-256 hashes `5cfb9ba35b1c0b2b85bc6c3682fbed901ad7c6132676dd86ba3e605a4ad3e7ca` and `3c50732ecd6f44ad448a9d6d77e7543421ea9c12b4ba497a1ebfc1665df6dcb5`, respectively.

The original papers remain uncontradicted: the detected order-5 constants disappear over their coefficient ring. The partial repair for fixed products over fields does not replace the general family theorem. The full construction contract remains open, including residue existence with all required compatibilities, ramified-5 constant normalization, the relative theta prescription, descent, auxiliary removal, integrality, compactification, all levels/components, and the adopted bad-prime identities.
