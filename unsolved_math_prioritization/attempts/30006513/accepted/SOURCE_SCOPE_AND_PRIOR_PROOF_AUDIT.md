# Finite length of permutation modules source scope and prior proof audit

Date: 8 October 2026 UTC. Target: 30006513, OWR-14299587-002, normal rank 1092.

## Decision

The catalogue's unrestricted finite-length statement is false by a published counterexample. The original Oberwolfach question was narrower: the underlying structure is homogeneous in a finite relational language, and the permutation set is a finite Cartesian power of its domain. That restricted question is not resolved by this counterexample, and the current primary papers inspected here continue to distinguish it from the general ascending-chain question.

The verification hold on the existence and proof of a literal counterexample can be released. The source-formulation discrepancy must remain explicit. This is a credited prior-result audit and source repair, not a new mathematical solution or a proof-search attempt on the original restricted problem. Zero new substantive proof-search turns were used. No GitHub, queue, author-contact, or publication action was taken.

## What the source asks

David M. Evans's contribution, *Permutation modules for Ramsey structures*, in Oberwolfach Report 58/2025, printed pages 3075–3077, first asks an ascending-chain question for a countable omega-categorical structure and a sort in its imaginary expansion. After recording that descending chains can fail for finite-field vector spaces and their projective sorts, page 3076 asks the following distinct finite-length question, here restated:

For a countable structure M homogeneous in a finite relational language, G = Aut(M), and a positive integer k, must the free permutation module on M^k have finite composition length over every coefficient field?

The catalogue instead quantifies over arbitrary omega-categorical M and oligomorphic G-sets W. Its universal assertion is already false. The catalogue's accompanying discussion of the finite-relational homogeneous question does not restore the missing assumption in its formal statement. [S1]

Both arXiv versions of Evans's paper preserve this distinction in Questions 1.1 and 1.2. The latest version is v2, dated 9 September 2026. The PDF saved during the preceding screen is already v2, despite a v1 HTML link in that screen. Fresh version-specific downloads establish which text was inspected. Evans develops tools for Ramsey structures, including a submodule-membership criterion, a duality with definable functions, and a cyclic-generation theorem for finitely generated submodules of the generalized augmentation module. These are not a proof of the general finite-length assertion. The notation F[W] in Evans denotes a definable-function module, whereas the catalogue uses brackets for the free module; below, basis vectors e_w remove that ambiguity. [S2, S3]

## The precise published counterexample

The proof audited here is Mikołaj Bojańczyk, Joanna Fijalkow, Bartek Klin, and Joshua Moerman, *Orbit-Finite-Dimensional Vector Spaces and Weighted Register Automata*, TheoretiCS 3 (2024), Article 13, Section 4.4, Theorem 4.16, using Lemmas 4.14 and 4.15 and Appendix B. The full proof, including the strictness argument, was retrieved and inspected. [S4]

Let V be the direct sum of countably many copies of the two-element field F_2. Set G = GL(V). View V either as a vector-space structure or as the relational structure whose ternary relation is x + y = z, with zero named. Its automorphisms are precisely G. The coefficients are also F_2. The permutation module is

    P = direct_sum_{v in V} F_2 e_v,
    g(e_v) = e_{g(v)}.

Elements have finite support. The basis vector e_0 is not the zero element of P. Addition of basis vectors in P must not be confused with vector addition inside V.

For every n >= 1 and every n-dimensional linear subspace U of V, put

    s_U = sum_{u in U} e_u,
    C_n = span_{F_2}{s_U : dim(U) = n}.

The following is an independent check of the published argument, with elementary bookkeeping made explicit.

### Invariance and descent

Each g in G takes s_U to s_{gU}, preserving dimension. Therefore C_n is an F_2G-submodule.

For an (n+1)-dimensional U, sum s_H over all n-dimensional hyperplanes H of U. There are 2^(n+1)-1 hyperplanes, so e_0 occurs an odd number of times. Each nonzero u occurs in 2^n-1 of them, again an odd number. Thus in characteristic 2 their sum is s_U. This proves C_{n+1} is contained in C_n for every n >= 1. Iteration gives C_n contained in C_m for n > m >= 1.

The lower bound m >= 1 is important: the same statement is not asserted for dimension-zero generators. The hyperplane count is the adjacent-dimension case of the source's Lemma 4.14.

### Strictness and the support bound

The source's Lemma 4.15 states that a nonempty symmetric difference of finitely many n-dimensional linear subspaces has at least 2^n points. Appendix B proves the stronger affine version. Here is the proof check.

Induct on n >= 1. In dimension 1 every affine subspace is a two-point set, and a symmetric difference of such sets has even cardinality; a nonempty result has at least two points.

For n > 1, let X be a nonempty symmetric difference of finitely many affine n-spaces. Its cardinality is even, so choose two distinct points of X. Some coordinate functional l on V separates them. The two slices X intersect l^{-1}(0) and X intersect l^{-1}(1) are both nonempty.

Intersecting an affine n-space A with either level set of l produces the empty set, A itself, or an affine (n-1)-space. If it produces A itself, write A = a + U. The hyperplane identity already checked expresses U as a symmetric difference of its (n-1)-dimensional linear hyperplanes. Translation by a gives the required expression for A in affine (n-1)-spaces. Thus each slice of X is a symmetric difference of affine (n-1)-spaces. The induction hypothesis gives at least 2^(n-1) points in each slice. They are disjoint, so |X| >= 2^n.

Every element of C_n is a finite F_2-linear combination of incidence sums and therefore such a symmetric difference. Consequently every nonzero element of C_n has support at least 2^n. For any n-dimensional U, s_U has exactly 2^n support points and lies in C_n, while it cannot lie in C_{n+1}, whose nonzero elements require at least 2^(n+1) points. Therefore

    P strictly contains C_1 strictly contains C_2 strictly contains C_3 ... .

The first inclusion is strict because all generators of C_1 have even support, whereas e_0 has support one. In fact C_1 is exactly the kernel of the augmentation map sending every e_v to 1: it is spanned by e_0 + e_v for v != 0.

There is a subspace U of every finite dimension, so the strict chain never ends. It violates the descending chain condition and hence rules out finite composition length. It does not exhibit an infinite ascending chain and does not refute the separate general ACC question.

## Verification of the projective sort

The Oberwolfach discussion specifically uses projective space. For this binary example, projective points are in G-equivariant bijection with V minus {0}, since a one-dimensional F_2-subspace has exactly one nonzero vector. Thus W = P(V) can be identified with V minus {0}; it is a definable set, and in particular a legitimate imaginary sort.

Let Q = F_2[W] denote the free permutation module. Define

    pi : P -> Q, with pi(e_0) = 0 and pi(e_v) = e_v for v != 0.

The restriction pi : C_1 -> Q is a G-equivariant linear isomorphism: its inverse sends e_v to e_0 + e_v. Define

    D_n = span_{F_2}{sum_{u in U minus {0}} e_u : dim(U) = n} = pi(C_n).

Because pi is injective on C_1, strictness survives for every n >= 1:

    Q = D_1 strictly contains D_2 strictly contains D_3 ... .

For completeness, a nonzero element of D_n has at least 2^n-1 support points: its unique lift in C_n adds at most the zero-coordinate basis vector. A generator of D_n has exactly 2^n-1 points. Thus the projective chain also has an explicit support-based strictness witness at every level. This is a routine transfer of the published binary construction, not a claim of a separately discovered counterexample.

## Omega categoricity and oligomorphicity

For any t, associate to a tuple (v_1,...,v_t) in V^t the kernel of the linear map F_2^t -> V sending the standard basis to that tuple. Two tuples have the same kernel exactly when the induced correspondence between their spans is a linear isomorphism. That isomorphism extends to an automorphism of V by extending finite bases to countable bases. Thus G-orbits on V^t are classified by subspaces of the finite vector space F_2^t. There are finitely many of these, proving oligomorphicity.

Since the structure is countable, this also gives omega-categoricity by the Ryll-Nardzewski characterization. The restricted action on W = V minus {0} is oligomorphic because W^t is an invariant subset of V^t. It is transitive on W. Stabilizers of individual projective points are open in the natural permutation topology, so the example also meets the source's stronger definable-sort convention rather than merely an unconstrained abstract G-set convention.

Already W = V = M, hence k = 1, refutes the broadened statement. Passing to the projective sort verifies the specific example discussed in the source, but is not needed to refute the catalogue's universal quantifier.

## Why this does not resolve the original homogeneous question

Finite relational presentation and finite relational homogeneity are different requirements. The ternary-addition structure above is finite relational but is not homogeneous as a relational structure.

For an explicit failure, take independent a,b,c,d. The map from {0,a,b,c,a+b+c} to {0,a,b,c,d} fixing 0,a,b,c and sending a+b+c to d preserves the ternary addition relation on these finite induced substructures: neither four-point nonzero set has a three-term dependency. It cannot extend to a linear automorphism because it destroys the four-term dependency a+b+c+(a+b+c)=0.

More generally, no finite relational structure on this domain with the same automorphism group GL(V) can be homogeneous. If r bounds its relation arities, choose l > max(r,3), an l-element binary circuit (a minimal dependent set), and an independent l-element set. Every at-most-r-element subtuple has the same linear-dependency type on the two sides, including repetitions. Hence the coordinatewise bijection preserves every GL(V)-invariant relation of arity at most r. It is an isomorphism of induced finite structures but cannot extend to an element of GL(V), because the full dependency differs.

One can instead make V homogeneous by naming all linear-dependency relations, of unbounded arity, as in LICS 2026 Example 2.5. That relational language is infinite. The functional vector-space language is homogeneous on its finitely generated substructures, but contains functions and therefore also falls outside the source's finite-relational hypothesis. Changing the automorphism group by adding arbitrary extra structure would change the permutation-module problem.

## Coefficient fields and limits of the conclusion

The retrieved TheoretiCS theorem directly proves failure for coefficient field F_2 and underlying vector space over F_2. That single instance is enough to negate the catalogue's claim for every field.

The same fixed action fails for every coefficient field K of characteristic 2 by scalar extension. Indeed K tensor_{F_2} P is naturally K[V], and K tensor_{F_2} C_n is the K-span of the same incidence sums. Tensoring an inclusion of F_2-vector spaces with K is exact, and a nonzero quotient C_n/C_{n+1} remains nonzero. Therefore all strict inclusions persist. The same applies to Q and D_n. This is an elementary corollary of the audited binary result; it is not a claim that the source's parity proof was written for arbitrary coefficients.

This audit does not establish the analogous projective example over every finite base field, nor make a negative assertion for coefficient fields of odd characteristic. No general finite-field extrapolation is necessary. In characteristic zero, the fixed vector-atom action has finite length for every finite power by the positive LICS result below. Its projective sort also has finite length as a submodule/direct summand or equivariant quotient of a finite-power permutation module. Consequently an all-characteristics negative claim for this example would be false.

## Current positive results and remaining source scope

The final published Yang–Bojańczyk–Klin paper is *The Finite Length Property of the Rado Graph and Friends*, LIPIcs 380, LICS 2026, Article 82, pages 82:1–82:27. The final publisher PDF was retrieved; the preceding screen used an author PDF with provisional Article 6 numbering. [S5]

Definition 5.1 assumes a homogeneous structure A for which, for each tuple dimension d, there is a cofinal family B of finite substructures with a common finite bound on the number of Aut(B)-orbits on B^d. The family may depend on d. Theorem 5.4 gives finite length over every characteristic-zero coefficient field. Theorem 5.2 and Corollary 5.5 include smoothly approximated structures, equality atoms, vector atoms over any finite base field, and the Rado graph.

Theorem 7.3 assumes a finite relational vocabulary of arity at most two and a free-amalgamation class of finite irreflexive structures in that vocabulary. It gives finite length over every field for the Fraisse limit after adding a generic total order, even with finitely many constants named. Corollary 7.5 transfers the conclusion to the unordered reduct, again with finitely many constants. Corollary 7.8 also lists equality and ordered atoms, all countable homogeneous tournaments, all countable homogeneous graphs, and certain homogeneous digraphs obtained by forbidding tournaments.

These hypotheses cannot be discarded. Remark 7.4 explicitly retains the arity restriction in the second method. The conclusion on page 82:25 repeats the unrestricted ACC and finite-relational homogeneous finite-length questions as open questions. Neither paper supplies a full resolution of the repaired source target. This audit verifies the positive theorems' stated scope and inspects their organization; it does not certify every proof in those papers. In particular the final conference paper defers some technical details of its second method to a full version.

## Attribution and verification boundaries

Theorem 4.16 and its full strictness proof were checked directly in the published TheoretiCS paper. The LICS paper attributes the binary counterexample also to Evans–Gray, *Kernels and cohomology groups for some finite covers*, Theorem 2.7, and identifies their result as independent. Evans's author bibliography confirms original publication in Logic Colloquium '96, Lecture Notes in Logic 12 (1998); the modern Cambridge reference is a 2017 reissue. OWR cites Ahlbrandt–Ziegler (1991) and the TheoretiCS paper. These earlier historical proof bodies were not retrieved here, so no broader theorem or first-priority claim is certified from them. [S1, S5, S6]

The proof required for a literal counterexample is available and complete in S4; there is no remaining proof-availability hold for the F_2 instance. Any request to verify all finite base fields would require a separate primary-proof check. The original finite-relational homogeneous question remains outside the counterexample's scope.

A dependency-free finite check enumerates all linear and affine subspaces of F_2^d for d = 1,...,4. It checks incidence-span descent, strict rank drops, exact minimum support 2^n, projective minimum support 2^n-1, invariance under standard finite GL generators, and the explicit ternary-addition partial isomorphism. All checks pass. These tests corroborate transcription and small cases; the infinite result rests on the proof above.

## Sources

- S1. David M. Evans, *Permutation modules for Ramsey structures*, Oberwolfach Report 58/2025, pp. 3075–3077, especially pp. 3075–3076. https://ems.press/content/serial-article-files/52445 . Report DOI: https://doi.org/10.4171/OWR/2025/58 .
- S2. David M. Evans, *Permutation modules for Ramsey structures*, arXiv:2603.29606v1, 31 March 2026, Questions 1.1–1.2. https://arxiv.org/pdf/2603.29606v1 .
- S3. Same title, arXiv:2603.29606v2, 9 September 2026, Questions 1.1–1.2, Theorems 1.4 and 3.8, Corollary 3.4. https://arxiv.org/pdf/2603.29606v2 . Version history: https://arxiv.org/abs/2603.29606 .
- S4. Mikołaj Bojańczyk, Joanna Fijalkow, Bartek Klin, Joshua Moerman, *Orbit-Finite-Dimensional Vector Spaces and Weighted Register Automata*, TheoretiCS 3 (2024), Article 13, pp. 1–41. Published 6 May 2024. https://doi.org/10.46298/theoretics.24.13 . Author-hosted published PDF: https://www.cs.ox.ac.uk/people/bartek.klin/papers/theoretics24.pdf . Section 4.4, pp. 18–21; Appendix B, pp. 37–39. The source is CC BY 4.0; the above is an attributed, independently written audit rather than copied source text.
- S5. Jingjie Yang, Mikołaj Bojańczyk, Bartek Klin, *The Finite Length Property of the Rado Graph and Friends*, LIPIcs 380, LICS 2026, Article 82, pp. 82:1–82:27. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.LICS.2026.82 . Final PDF: https://drops.dagstuhl.de/storage/00lipics/lipics-vol380-lics2026/LIPIcs.LICS.2026.82/LIPIcs.LICS.2026.82.pdf . Definitions and results inspected: Example 2.5, Definition 5.1, Theorems 5.2, 5.4, 7.3, Corollaries 5.5, 7.5, 7.8, Remark 7.4, Conclusion. CC BY 4.0.
- S6. David M. Evans, author bibliography, entry 26. https://www.ma.imperial.ac.uk/~dmevans/ . Earlier counterexample attribution is as reported by S5; its proof was not used in place of the directly audited S4 proof.
