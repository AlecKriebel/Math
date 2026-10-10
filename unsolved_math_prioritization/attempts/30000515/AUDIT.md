# Independent audit: numerical Godeaux partial result

Problem 30000515 / OWR-1276-008. Audit date: 10 October 2026 UTC.

## Verdict

**ACCEPT_PARTIAL.** The submitted partial deductions are mathematically sound under the stated smooth, connected, minimal complex projective general-type hypotheses, with p_g=q=0 and K^2=1. No mathematical correction to the submitted proof is required. This is not acceptance of the requested topological simple-connectivity conclusion, and no novelty is claimed.

The independently checked conclusions are:

1. Every divisor in |2K| is 2-connected if and only if Pic(S) has no nonzero torsion.
2. These equivalent conditions imply H_1(S,Z)=0 and a perfect topological fundamental group.
3. Every connected finite unramified topological cover of any numerical Godeaux surface has degree at most six.
4. Under the connectedness condition, every finite quotient of pi_1(S) is trivial. Thus there is no nontrivial connected finite cover, the profinite completion is trivial, and the algebraic fundamental group is trivial.
5. Topological simple connectivity follows if pi_1(S) is additionally finite or residually finite. Neither additional property is proved here.

The four-distinct-bicanonical-base-points assumption is not used in conclusions 1-4. It remains part of the original unresolved target.

## Independent reconstruction and hypothesis checks

### Torsion gives an intersection-one decomposition

If tau is nonzero torsion, its real first Chern class is zero. A nontrivial numerically trivial line bundle cannot have a section: a nonempty effective zero divisor intersects an ample divisor positively, and a nowhere-zero section trivializes the bundle. Consequently h^0(tau)=h^0(-tau)=0.

Surface Riemann-Roch and Serre duality give chi(K+tau)=1 and h^2(K+tau)=h^0(-tau)=0. Hence K+tau and K-tau both have effective representatives D_+ and D_-. Their K-degrees are one, so neither divisor is zero. Their sum is linearly equivalent to 2K, and D_+.D_-=1. This contradicts 2-connectedness. An order-two class may produce equal divisors; the definition permits this, so the argument includes a double component.

Only existence, not uniqueness, of the two effective representatives is needed. No vanishing theorem for h^1(K+tau) is assumed.

### The converse, including nonample K and shared components

On the smooth minimal surface, K is nef and has positive square one. For C=A+B linearly equivalent to 2K with nonzero effective A,B, put k=K.A. Nefness gives k in {0,1,2}. There is no assumption that A and B have disjoint support.

For k=0, A has nonzero numerical class, because it intersects an ample divisor positively. Hodge index applies to the orthogonal complement of every positive-square class, including a nef class that is not ample. Thus A^2<0. Riemann-Roch, equivalently adjunction parity for the Cartier divisor A, makes A^2+K.A even. Therefore A^2<=-2 and A.B=-A^2>=2. This remains valid for nonreduced or disconnected A: only the parity identity is used. For k=2, apply the same argument to B.

For k=1, Hodge index gives A^2<=1 and parity makes A^2 odd. Since A.B=2-A^2, the only possibility for A.B<2 is A^2=1, A.B=1. The class A-K is K-orthogonal and has square zero; negative definiteness implies it is numerically zero.

The exponential sequence, with H^1(O_S)=H^2(O_S)=0, gives c_1:Pic(S)~H^2(S,Z). Here analytic and algebraic Picard groups agree by projectivity. All real degree-two cohomology classes are therefore real linear combinations of divisor classes. The Poincare intersection pairing on H^2(S,R) is nondegenerate. A numerically trivial divisor has zero real class and thus torsion integral class. With no Picard torsion, A is linearly equivalent to K, contradicting h^0(K)=p_g=0.

This proves the equivalence on the smooth minimal surface without importing a canonical-model connectedness assertion. In particular, exceptional (-2)-curves and the cases K.A=0 or K.B=0 are not discarded. If K is ample, only k=1 remains and the same parity argument gives intersection at least three; that optional stronger remark is also correct.

### Integral first homology, not only rational homology

Since S is a compact Kahler surface, b_1=2q=0. Its integral H_1 is finitely generated and therefore finite. Universal coefficients give

    0 -> Ext^1(H_1(S,Z),Z) -> H^2(S,Z) -> Hom(H_2(S,Z),Z) -> 0.

The right-hand group is torsion-free. Thus the torsion subgroup in H^2 is precisely the finite Ext group, noncanonically isomorphic to H_1. The exponential-sequence calculation makes this torsion vanish, so H_1(S,Z)=0. Degree-one Hurewicz identifies this with trivial abelianization. No rational-coefficient conclusion is substituted for the necessary integral statement.

### Covers are compact projective minimal general-type surfaces

A connected finite topological covering f:Y->S inherits a unique complex structure by pulling back holomorphic charts. It is a compact smooth complex surface, and f is locally biholomorphic. A positive Hermitian line bundle on S pulls back to a positive line bundle on Y; Kodaira embedding therefore makes Y projective. Equivalently one can use the complex finite-cover comparison theorem. Once Y is projective, the holomorphic map is algebraic by the usual graph/Chow argument.

There is no ramification divisor, so K_Y=f^*K_S. Pullback and the projection formula give nefness and K_Y^2=d>0. Nefness excludes a (-1)-curve by adjunction, hence Y is minimal. Nefness and positive square make K_Y big, so Y is of general type. For example, Riemann-Roch for mK_Y, with h^0((1-m)K_Y)=0 for m>1, directly supplies quadratic growth. These arguments do not require q(Y)=0.

The tangent bundle pulls back under a local biholomorphism, or equivalently Euler characteristic multiplies for a finite cover. Noether's formula therefore gives chi(O_Y)=d chi(O_S)=d. The smooth minimal general-type Noether inequality is

    K_Y^2 >= 2p_g(Y)-4 = 2chi(O_Y)+2q(Y)-6 >= 2chi(O_Y)-6.

Substitution gives d>=2d-6, hence d<=6. The direction of the inequality is correct. This deliberately weak bound does not establish d<=5, and it does not apply to an infinite, noncompact universal cover.

### Every finite quotient and every finite cover

For any finite quotient G of Gamma=pi_1(S), the normal kernel determines a regular connected cover of degree |G|. The preceding bound gives |G|<=6. A quotient of a perfect group is perfect. No nontrivial group of orders 2 through 6 is perfect: prime orders are cyclic, order four is abelian, and an order-six group has a normal Sylow three-subgroup with a quotient of order two.

A nonregular connected finite cover would give a proper finite-index subgroup H. The transitive action on Gamma/H has nontrivial finite image whenever the index is greater than one, contradicting the preceding conclusion. Thus the argument excludes all connected finite covers, not just regular or abelian ones. The comparison of finite topological and finite etale covers over C identifies pi_1^alg with the profinite completion.

## Source and model safeguards

The original report states the Picard-torsion consequence and separately conjectures simple connectivity; the two conclusions are not conflated. Catanese-Pignatelli's relevant lemma has standing restrictions on torsion and concerns the canonical model. Schreyer-Stenger's later Lemma 2.1 gives the broader canonical-model version. The submitted proof instead derives its smooth-surface statement directly, with the zero-K-degree cases retained.

There is a minor source-level typographical error in the inspected arXiv:2201.12065v1 proof of Lemma 2.1: the expansion of (D_1+D_2)^2 displays a single cross term. The correct identity is D_1^2+D_2^2=4-2D_1.D_2, as displayed in Catanese-Pignatelli, Lemma 1.10. The corrected expression is still nonnegative when D_1.D_2<=2. This does not affect the submitted proof, which uses A.B=2K.A-A^2 directly, and it creates no obstacle to acceptance.

The finite-cover conclusions are established background, not a new algebraic simple-connectivity theorem. The sharper algebraic-group classification is not needed. The known eight-dimensional simply connected family is locally complete, while the inspected continuation explicitly leaves special-line loci unresolved. A locally complete family is not an exhaustion of all target surfaces. No computational experiment over a finite field is promoted to a universal classification.

## Exact residual and acceptance boundary

The original target remains unresolved by this package. A hypothetical counterexample must have an infinite, finitely presented, perfect pi_1 with no nontrivial finite quotient and no proper finite-index subgroup, while satisfying all smooth numerical Godeaux and four-simple-base-point hypotheses. Compact smooth manifolds have finitely presented fundamental groups. Nothing here proves such a group is impossible in this geometric class, and nothing constructs an example.

The bicanonical fibration's genus-four computation and four sections do not compute its vanishing-cycle normal subgroup. Neither residual finiteness, finiteness, nor a complete smooth-deformation classification may be inserted as an unstated final step. No present global-openness or priority certification is made.

## Integrity and review limits

The frozen original proof, status and source review were read and independently audited. Recorded source identities were rehashed and selected primary-source statements inspected as described in SOURCE_AUDIT.md. Publication preparation rechecked the frozen author and audit identities and replayed the supplementary arithmetic in normal, -O and -OO Python. Verification programs and arithmetic tests check integrity and finite regression properties; the mathematical acceptance is this written review, not a formal proof certificate.

This separately identified edition preserves every mathematical proof argument and every substantive audit finding, including the source-level cross-term typo and the unresolved topological boundary. It removes only private accounting and updates the review wrapper. ACCEPTANCE.json identifies both the frozen original and distributed documents. The proof and audit are AI-assisted and unrefereed; internal acceptance does not mean external human peer review, journal acceptance, formal proof-assistant certification or historical novelty.
