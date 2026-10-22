# Independent audit of the moving weight obstruction

## Decision and scope

**Accept the mathematical conclusions of frozen REPORT.md Sections 2.3–2.5 and the conditional theorem in Section 5.** The normalized affine Cartan-descendant sequence is admissible for the construction actually printed in Han's arXiv:2606.05854v5 proof of Theorem 2.7. The passage from convergence of each fixed component's zero mode to disappearance of their total tail is false under the stated hypotheses. Section 5's pointwise locally finite spectral argument is valid without rationality or finite generation.

No substantive correction to those conclusions is required. The qualifications below should accompany any acceptance: the affine example has nonzero weight-one space; its derivation is inner; an alternative favorable choice may exist; and the failure of this particular inference proves neither a false innerness theorem nor a counterexample to the target finiteness conjecture.

This review was made independently from the frozen report and primary sources, without consulting another review. It does not certify every section of the frozen packet. The inspected input manifest has SHA-256 a9b478491ffe9f3dd75d177bd863ec8dc2f28ac3ed69f04bce9e35955247e989. Original packet and source files were preserved.

## Primary source identity and inspection

The operative primary manuscript is Jianzhi Han, *Derivations of rational vertex operator algebras are inner*, arXiv:2606.05854v5, submitted July 9, 2026 at 12:46:48 UTC. On October 7, 2026, both the [versioned arXiv record](https://arxiv.org/abs/2606.05854v5) and the [unversioned record](https://arxiv.org/abs/2606.05854) displayed v5 as the latest revision. No journal reference was displayed. This is a statement about the inspected listing, not a claim about editorial acceptance elsewhere.

The inspected [v5 PDF](https://arxiv.org/pdf/2606.05854v5) has 10 pages, 290613 bytes, and SHA-256 1171467d597568d4385aedf560f14e9a3945a67e7bb391b29c61c2a326d590c4. The complete mathematical section was read, including Lemma 2.4, the definitions of E_d and t, Proposition 2.5 with (2.8)–(2.10), Lemma 2.6, and the full Theorem 2.7 proof. PDF pages 7, 8, and 9 were independently rendered and visually inspected. The [official v5 HTML](https://arxiv.org/html/2606.05854v5) was also checked. The PDF was the provided local copy whose bytes were rehashed; this review did not freshly download that PDF.

Two supporting primary PDFs were inspected in their relevant passages:

- Dong, Li, Mason, and Montague, *The radical of a vertex operator algebra*, [q-alg/9608022](https://arxiv.org/abs/q-alg/9608022): Lemma 2.5 and Lemma 3.3. Inspected PDF: 107876 bytes; SHA-256 e57560a8523cba159cb2b94e93679d6f379740f2592f091926d5892666e19ae7.
- Dong, Li, and Mason, *Regularity of rational vertex operator algebras*, [q-alg/9508018](https://arxiv.org/abs/q-alg/9508018): the positive-integral-level affine setup and Theorem 3.7. Inspected PDF: 167360 bytes; SHA-256 973e8b43d3a31b5e07fb1e7490d409b2f9e9c6a8d9bb61196d7183c6b7537ad2.

This report contains authored analysis and bibliographic/verification metadata. It does not package source PDFs, extracted source text, page images, or private coordination material.

## The hypotheses actually used by the construction

Write T=L(-1), and o(a)=a_(k-1) when a has weight k. The relevant requirements are:

1. E_d contains all positive-weight formal representatives whose zero-mode summands are eventually zero on each test vector and whose pointwise sum is d. Its definition imposes no support minimality, preferred representative, or requirement that the representative be produced by one fixed invocation of Lemma 2.4.
2. t(b) is the first weight at least two whose component is not killed by L(1), with infinity when every such component is killed.
3. After proving the t-values have infinite supremum, the theorem's proof selects b_n in E_d with t(b_n) at least n+2.
4. For finite t=t(b_n), the hat operation preserves components below t, deletes component t, and moves each old component of weight i at least t to weight i+1 by the factor -T/i.
5. The subsequent elimination concerns weights 2 through t-1. The referenced argument in Proposition 2.5 removes a component when it is nonzero. Zero components require no subtraction.
6. The resulting support condition permits a degree-one component and a tail starting at t or later. It does not impose a bound on where that tail can act on a fixed vector as n varies.

The finite-supremum contradiction normalizes a finite initial portion of one representative. The later selection of b_n is not stated to be an iteration of that normalization on a fixed initial representative. Nor is each selected b_n required to be fully quasi-primary. Reading either restriction into the proof would add an unstated construction and would require a proof of its relevant convergence properties.

## The affine sequence satisfies every stated requirement

Let V=L_1(sl2), with its Sugawara conformal vector. This is a simple rational CFT-type VOA: the cited positive-level affine regularity theorem applies, and regularity implies rationality. Its weight-one Lie algebra contains nonzero h and e with h_0 e=2e. The current h is primary of weight one.

Set d=h_0. The zero-mode Jacobi identity gives the derivation identity. Since h is primary, [L(m),h_0]=0 for every m. It follows that d annihilates both the vacuum and conformal vector. Thus d is a conformal derivation, and d(e)=2e shows that d is not zero.

For a homogeneous vector a of positive weight k, translation yields

    o(T^r a) = (-1)^r k(k+1)...(k+r-1)o(a).

For N at least one, define

    c_N = (-1)^(N-1) T^(N-1)h / (N-1)!.

Consequently o(c_N)=d for every N. The representative with c_N in degree N and zero elsewhere has finite support and belongs to E_d. Its o-additivity is global finite support, which is stronger than the required pointwise finite support.

The Virasoro relations give, for primary a of weight k,

    L(1)T^r a = r(2k+r-1)T^(r-1)a.

For h this coefficient is r(r+1). In particular,

    L(1)c_N = -N c_(N-1),                    N >= 2,
    L(1)^(N-1)c_N = (-1)^(N-1) N! h.

The second identity proves c_N is nonzero for every N. The first then gives t(c_N)=N for N at least two. Neither a sign convention nor a vanishing descendant excludes the example.

Choose N=n+2 for n at least one and set b_n=c_N. Then t(b_n)=n+2, exactly the allowed lower bound. The displayed hat operation yields a single component:

    hat b_n = -T c_N/N = c_(N+1).

It remains in E_d, and t(hat b_n)=N+1 as required. Every component in weights 2 through N-1 is already zero. Therefore the permitted elimination is vacuous, and tilde b_n=hat b_n has the required final support. A tail starting at N+1 also satisfies a condition allowing a tail from N onward.

For each fixed weight i, tilde b_n^(i) is eventually zero. Its degree-one component is zero for every n. Nevertheless,

    sum_(i>=2) o(tilde b_n^(i)) = d,
    sum_(i>=2) o(tilde b_n^(i))e = 2e,
    o(tilde b_n^(1)) = 0.

The whole tail does not approach zero even on the single fixed vector e. The conclusion that the degree-one zero modes approach d would make 0=2e after evaluation on e.

This example also has natural coherence: b_(n+1)=hat b_n, and every sequence member is obtained by normalized translation of the same h. Thus merely requiring consecutive terms to be related by the hat operation, or requiring eventual agreement of every fixed component, would not exclude it.

## The invalid inference and the alternative-choice qualification

The precise failure occurs on PDF page 9 after continuity on each individual homogeneous component has been invoked. The proof has an identity between d, the degree-one zero mode, and the entire higher-degree zero-mode tail. It then treats the limit of that tail as the sum of the limits of its fixed-degree terms. Eventual finite support for each fixed representative and test vector does not justify that exchange uniformly over the sequence.

For the affine sequence, the unique active index tends to infinity while its contribution stays d. In elementary array notation the tail on e is represented by 2 times the indicator of i=n+3. Every column tends to zero; every row sum equals 2. The VOA construction above realizes this array under the actual derivation and representative hypotheses, so the objection is not merely a generic scalar analogy.

Continuity of o on each V_i does not fix the issue. The input converges coordinatewise in the product of weight spaces, whereas the paper's stated direct-sum topology is stronger. For this particular sequence, failure of direct-sum convergence can be seen explicitly: choose a linear functional on each V_i taking c_i to 1; the sum of the absolute values of these functionals is a continuous seminorm on the locally convex direct sum and is 1 on every c_i. The sequence therefore does not tend to zero there. No continuity of the summed zero-mode map on the product completion has been established, and the example disproves the needed continuity.

There is a favorable alternative choice for this example: the representative h itself has t=infinity and proves d is inner immediately. This does not validate the inference for the b_n choices permitted by the written proof. Conversely, the bad choice does not disprove the existence of favorable choices for all derivations.

An intended preliminary branch for t=infinity would dispose of this particular inner derivation before the bad sequence was used. That would be a reasonable reorganization, but the remaining branch would still require a justified construction with a vanishing total tail or a different argument. No outer derivation is exhibited here, so this review does not claim an actual example in a hypothetical non-inner-only branch.

The last use of the degree-one quotient is not the essential obstruction. Once convergence to d of degree-one zero modes is proved, finite dimensionality supplies closedness of their image in the Hausdorff pointwise operator space. What is missing is the preceding convergence itself.

## General support shifting in Section 2 point 5

The asserted general identity is valid. For m at least one, replace a weight-i component b^(i) by

    S_m(b)^(i+m) = (-1)^m T^m b^(i) / [i(i+1)...(i+m-1)],

and set all other components to zero. There is one old component for each new index; there is no infinite summation inside a fixed target weight. Its zero mode is o(b^(i)). For each test vector, the old eventual-zero bound is merely shifted by m. Thus S_m maps E_d into E_d and kills all components of weights at most m. The frozen report's conclusion t(S_m b)>m, or infinity, is correct.

A useful strengthening clarifies why an implicit finite-t restriction would not supply tail control. For d nonzero and b in E_d, let r be the first nonzero component weight. Translation is injective in positive weight. By the CFT-type decomposition V_j=ker L(1) direct-sum T V_(j-1) for j at least two, a nonzero translated component cannot be quasi-primary. Hence for m at least one,

    t(S_m b) = r+m < infinity.

Take m=n+1. These representatives have t at least n+2 and zero components below t. Their hat is S_(m+1)b, and their specified low-component elimination is again vacuous. They retain total zero-mode sum d and zero degree-one component. This is a conditional construction for every nonzero d with E_d nonempty; it does not assert that an outer derivation exists. It demonstrates that support escape is intrinsic to the permitted representative operations.

## Independent verification of the spectral theorem in Section 5

Assume V is CFT type, q_i belongs to V_i for i at least one, L(1)q_i=0 for i at least two, A_i=o(q_i), and the family A_i is pointwise locally finite. Suppose d=sum_i A_i is a conformal derivation. Define an operator on endomorphisms by

    C(A) = [T,[L(1),A]].

For i at least two the mode commutator and translation identities give

    [L(1),(q_i)_(i-1)] = (i-1)(q_i)_i,
    [T,(q_i)_i] = -i(q_i)_(i-1),
    C(A_i) = -i(i-1)A_i.

For i=1, the possibly nonzero L(1)q_1 lies in the vacuum line, and its mode with index zero vanishes. Thus [L(1),A_1]=0 and C(A_1)=0. It is not necessary to assume q_1 is quasi-primary or L(1)V_1=0.

Here is the essential justification for every termwise operation. If a family F_i is pointwise locally finite and B is any fixed endomorphism, then [B,F_i] is pointwise locally finite: at a fixed v, use bounds for the finite support of F_i v and F_i Bv. Therefore [B,sum_i F_i]=sum_i[B,F_i]. Repeating this argument for a fixed finite word of commutators requires only finitely many transformed test vectors. It applies to each finite power C^r and gives

    C^r(d) = sum_i [-i(i-1)]^r A_i.

Because d is conformal, it commutes with T and L(1), so C(d)=0. Fix v, and let J be the finite set of indices i at least two for which A_i v is nonzero. Define

    P_v(x) = product_(i in J) (1+x/[i(i-1)]).

Then P_v(0)=1, P_v(C)d=d, and the termwise identity for this finite polynomial is justified by the preceding argument. At v, all terms of degree at least two are annihilated, either by their eigenvalue factor or because they already vanish on v. Hence

    d(v) = [P_v(C)d](v) = A_1(v).

The dependence of P_v on v is harmless: the assertion obtained is equality of the same two fixed operators d and A_1 on each v. This proves d=o(q_1).

The argument does not appeal to a uniform support bound across all v, to finite generation, or to rationality. It uses local finiteness, not an unspecified conditionally convergent series. The eigenvalue sign and the distinction between fixed-v finite interpolation and a uniform global polynomial are both correct in the frozen report.

One may even infer that every A_i with i at least two is zero: for each fixed v the finite nonzero eigenvalues are distinct, and the equations for r=1 through the size of J form an invertible Vandermonde system after factoring one eigenvalue from each column. This strengthening is not needed for acceptance.

The stated remaining existence gap is real. Normalization of each finite c_N by descending through translation returns h in degree one, which loses the desired vanishing low-degree pattern. Nothing in the spectral theorem constructs an o-additive quasi-primary representative from an arbitrary infinite representative. Infinite downward normalization may accumulate infinitely many contributions at the same degree. The conditional theorem is therefore a valid implication, not a solution of that existence problem.

As a secondary source-reading qualification, Han's Proposition 2.5 is stated for CFT type but its printed proof invokes rationality to obtain finite generation. The pointwise spectral proof above supplies the relevant implication at the full stated generality without that invocation. This does not repair the later tail-limit step.

## Exact controls and acceptance boundary

The independent `verify_controls.py` checks descendant normalization, L(1)-lowering, the hat sign, support conditions, general m-step translation, and finite spectral interpolation using exact rational arithmetic. It checks descendants through weight 101. Its 1150 positive checks pass. Four deliberately wrong alternatives are rejected: the opposite hat sign, the wrong factorial, the opposite spectral sign, and a zero total tail on the root current. These tests support coefficient fidelity and are not a finite certification of a general VOA theorem. The all-index justifications are in the preceding sections.

The frozen packet's own mathematical check also ran successfully. Its success was not substituted for the independent mathematical argument. The full manifest entries were rehashed at the end of this review to verify that the frozen input remained unchanged.

Final disposition:

- Accept Sections 2.3–2.5 as a valid objection to the written v5 limit inference, with the actual E_d, t, hat, and elimination hypotheses checked.
- Accept the Section 5 pointwise locally finite spectral theorem and its explicit missing-existence qualification.
- Recommend retaining the distinction between the written unrestricted representative selection and any intended but unproved favorable-choice construction.
- Do not infer a counterexample to Han's theorem, a VOA with V_1=0 violating the target conjecture, an accepted resolution of that conjecture, or an exhaustive literature conclusion.

No external contact or publication was performed in this review.
