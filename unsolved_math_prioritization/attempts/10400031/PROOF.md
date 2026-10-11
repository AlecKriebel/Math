# Pointwise finite type approximation of the classical knot signature

This AI-assisted manuscript is unrefereed. Acceptance refers to an internal AI mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. This is not a computational reproduction package. No novelty or priority claim is made, and no exhaustive current-openness claim is made.

## Result and exact scope

Problem 10400031 / AMR-103-0031, Ohtsuki Problem 2.9, asks whether there is one sequence of numerical Vassiliev invariants, each defined on every classical knot, converging at every fixed knot to its classical signature. This report does not prove or disprove that assertion.

It proves an exact reformulation: such a sequence exists if and only if every knot of nonzero signature is distinguished from its mirror image by some numerical finite-type invariant. It also provides an explicit sequence converging eventually exactly to the signature modulo 4 on all knots, and a sequence converging eventually exactly to the full signature on the torus knots, with each term still defined on all knots. These partial conclusions do not answer the original all-knots question. No novelty claim is made for the elementary interpolation method or these consequences of standard facts.

The remaining obstruction is a single fixed knot of nonzero signature which is indistinguishable from its mirror by all rational finite-type invariants, or a proof that no such knot exists. Producing different knots for different degree cutoffs does not establish that obstruction.

## 1 Definitions and algebra

Let K denote the countable set of smooth oriented knot types in the oriented 3-sphere. Countability follows from finite knot diagrams. The result is unchanged if one instead forgets the orientation of the knot: signature is invariant under orientation reversal, and an approximating sequence can be averaged with reversal.

For a field F of characteristic zero, an F-valued invariant v has type at most d if its extension by

    v(K_crossing) = v(K_positive) - v(K_negative)

vanishes on every singular knot with d+1 double points. Write V_d(F) for these invariants and V(F) for their union. We use ordinary pointwise convergence of rational or real values, with the signature regarded as integer valued. The degree may depend on the sequence index without any uniform bound.

**Lemma 1.** Constants and finite sums of finite-type invariants are finite type. If u and v have types at most a and b, then uv has type at most a+b. Composing a finite-type invariant with a fixed connected-sum operation, mirroring, or orientation reversal preserves its degree bound.

**Proof.** The assertions about constants and sums follow directly from the definition. For the product, restrict u and v to the 2^r resolutions of an r-singular knot. On this Boolean cube, u has multilinear polynomial degree at most a: every mixed difference in more than a coordinates vanishes. The analogous degree bound holds for v. Their product, after reducing each Boolean variable by x_i^2=x_i, has degree at most a+b. Its full mixed difference therefore vanishes for r>a+b. A fixed connected sum leaves the singular crossings in the varying summand untouched. Mirroring exchanges the positive and negative resolutions, contributing a sign to each difference; reversal also preserves the vanishing condition. This proves the remaining claims. □

The product theorem is also proved in Chmutov-Duzhin-Mostovoy, §3.2.3, printed pp. 66-68 [CDM]. Consequently every finite polynomial in finitely many finite-type invariants is itself a finite-type invariant. No arbitrary nonpolynomial composition will be called finite type here.

## 2 Exact finite interpolation theorem

Define K ~ L if every rational finite-type invariant has the same value on K and L.

**Theorem 2.** For any rational-valued knot invariant f, the following are equivalent:

1. There is a sequence v_n in V(Q) with v_n(K) tending to f(K) for every K.
2. Whenever f(K) differs from f(L), some rational finite-type invariant distinguishes K and L.
3. For every finite set E of knot types, a rational finite-type invariant agrees exactly with f on E.
4. There is a sequence v_n in V(Q) such that for every K, v_n(K)=f(K) for all sufficiently large n.

**Proof.** The implication 1 to 2 follows because equal values at every stage have equal limits. To prove 2 to 3, fix E. For every pair in E having unequal f-values, choose a separating invariant. Collect these finitely many invariants in a feature vector u=(u_1,...,u_r). If no such pair exists, the constant value of f on E suffices.

Otherwise let a_1,...,a_m be the distinct feature vectors u(K) attained on E. By construction f is constant on the knots in E sharing any one a_i; call the value b_i. For an arbitrary knot K define

    L_i(K) = product over j != i of
       [sum over l=1,...,r of (u_l(K)-a_{j,l})^2]
       / [sum over l=1,...,r of (a_{i,l}-a_{j,l})^2].

All denominators are positive rational numbers because the feature vectors are distinct. Thus

    v_E(K) = sum over i=1,...,m of b_i L_i(K)

is a rational polynomial in finitely many finite-type invariants. Lemma 1 makes it finite type on every knot. On a knot with feature vector a_j, the usual cardinal interpolation identities give v_E(K)=b_j=f(K). If all u_l have type at most D, the displayed construction has type at most 2D(m-1).

Enumerate all knot types K_1,K_2,..., once and for all. For E_n={K_1,...,K_n}, choose the invariant from 3. The resulting single sequence is equal to f at K_i for every n>=i. Hence 3 implies 4, and 4 implies 1. □

**Rational versus real values.** Allowing real- or complex-valued finite-type invariants in condition 2 does not change it. Let A_Q be the free rational vector space on knots, and F_{d+1} the rational span of the alternating resolutions of (d+1)-singular knots. If a real-valued invariant of type at most d distinguishes K from L, then K-L is nonzero in A_Q/F_{d+1}. A rational linear functional on that quotient can be chosen nonzero on this element, and gives a rational finite-type separator. Thus for integer-valued signature, allowing real approximants creates no weaker existence question.

**Relation to the general conjecture.** Separation of every pair of distinct knot types would imply condition 2 for every f. It is a sufficient but stronger hypothesis than what signature needs. We do not claim signature detection implies full knot separation. Røgen's density/separation result and Kofman-Rong's Conjectures 7.1-7.3 concern the general problem [R, KR]. [CDM, §3.2.4, printed p. 69] calls condition 2 domination by Vassiliev invariants and explicitly identifies signature domination as an open problem at that source's date.

**Arbitrary functions are not a substitute.** If one actually knew a pointwise approximation to f by arbitrary functions of finitely many finite-type invariants, it would force condition 2, and Theorem 2 would then give genuine finite-type approximants. Countability and finite polynomial interpolation are the missing conversion argument. Merely writing f as an unspecified function of alleged invariant data does not establish the required hypothesis.

## 3 The mirror obstruction is equivalent to the full question

Write mK for the mirror of K. The classical signature satisfies

    sigma(mK) = -sigma(K),
    sigma(K # L) = sigma(K) + sigma(L).

Both statements follow directly from the Seifert-matrix definition: mirroring negates a Seifert form up to transpose, and connected sum gives a block-diagonal form. The symmetric form's inertia therefore changes as asserted.

**Theorem 3.** The pointwise signature approximation problem is equivalent to the following property:

    For every knot J with sigma(J) != 0, there is a rational
    finite-type invariant u with u(J) != u(mJ).

**Proof.** If signature is a pointwise limit and sigma(J) is nonzero, the two limits at J and mJ differ. Some term of the sequence separates the pair.

Conversely, assume the displayed property. Let K and L have different signatures. Put J=K # mL. Then sigma(J)=sigma(K)-sigma(L) is nonzero. Choose u distinguishing J and mJ. Define, for every knot X,

    w(X) = u(X # mL) - u(mX # L).

Lemma 1 shows that w is finite type. Commutativity of connected sum gives w(L)=0. On the other hand,

    w(K) = u(K # mL) - u(mK # L) = u(J)-u(mJ) != 0.

Thus w separates K and L. Theorem 2 now gives one sequence on all knots converging pointwise to signature, even eventually exactly. □

**Equivalent negative certificate.** If K~L but sigma(K)!=sigma(L), then J=K#mL has nonzero signature and J~mJ. Indeed connected sum with a fixed knot and mirroring preserve the equivalence relation, by Lemma 1. This also verifies directly that the mirror formulation loses no counterexamples.

**Symmetries of a possible positive answer.** If v_n tends to signature, then

    a_n(K) = (v_n(K)-v_n(mK))/2

is mirror-odd and still tends to signature. Averaging a_n with orientation reversal makes it reversal invariant. If the starting sequence is eventually exact at each knot, these symmetrizations remain eventually exact, since only finitely many transformed knots enter at each fixed K. Each a_n vanishes on the unknot. We cannot additionally require each approximant to factor through the Seifert form; §6 explains the obstruction to that extra restriction.

## 4 Explicit approximation to signature modulo 4 on all knots

Use the normalized Conway polynomial

    nabla_K(z) = sum over j>=0 of a_{2j}(K) z^(2j), with a_0(K)=1.

Each a_{2j} is of type at most 2j. For completeness, applying the Conway skein relation at r singular crossings introduces the factor z^r; its coefficient of z^(2j) is zero if r>2j. This gives exactly the required finite-type bound.

Put

    D(K) = nabla_K(2i) = sum over j>=0 of (-4)^j a_{2j}(K),
    D_n(K) = sum over j=0,...,n of (-4)^j a_{2j}(K).

The finite sum D_n has type at most 2n. For each fixed K it eventually equals D(K). Notice that D is the **signed normalized** Alexander value Delta_K(-1), not its absolute value, usually called the knot determinant. It is an odd nonzero integer.

**Lemma 4.** The unique representative r(K) of sigma(K) modulo 4 in {0,2} is

    r(K) = 1 - sign D(K).

**Proof.** Let V be a 2g by 2g Seifert matrix and S=V+V^T. With the normalization Delta_K(t)=t^(-g)det(V-tV^T), one has

    D(K) = (-1)^g det S.

The matrix V-V^T is unimodular and S is congruent to it modulo 2; hence det S is odd and S is nonsingular. If S has q negative eigenvalues, then sigma(K)=2g-2q. Therefore

    sign D(K)=(-1)^(g+q)=(-1)^(sigma(K)/2).

This is +1 exactly for sigma(K)=0 modulo 4 and -1 exactly for sigma(K)=2 modulo 4. □

For n>=1, let h_n be the following odd polynomial of degree at most 2n-1:

    h_n(x) = x * sum over k=1,...,n of
      [1/(2k-1)] * product over l != k of
      [x^2-(2l-1)^2] / [(2k-1)^2-(2l-1)^2].

It has rational coefficients and h_n(+(2k-1))=+1, h_n(-(2k-1))=-1 for 1<=k<=n. Define

    R_n(K) = 1 - h_n(D_n(K)).

**Theorem 5.** Each R_n is a rational finite-type invariant on all knots, of type at most 2n(2n-1). For every fixed knot K,

    R_n(K) = r(K)

for all sufficiently large n.

**Proof.** The degree bound follows from Lemma 1 and the degrees of h_n and D_n. Fix K. Choose g_0 with a_{2j}(K)=0 for j>g_0 and choose n at least both g_0 and (|D(K)|+1)/2. Then D_n(K)=D(K), and the latter belongs to the finite interpolation set {±1,±3,...,±(2n-1)}. Thus h_n(D_n(K))=sign D(K). The same is true for every larger n. Apply Lemma 4. □

The proof uses growing polynomial compositions, each genuinely finite type. Neither applying a sign function directly to D_n nor freezing the Conway truncation would prove this result.

A necessary condition for any counterexample pair K~L to the full problem is sigma(K)-sigma(L) in 4Z. In fact such a pair has the same complete Conway polynomial, because every Conway coefficient is finite type. The residue construction says nothing about the missing multiples of 4.

## 5 Full signature on the torus-knot subfamily

This is a partial case, not a replacement of the universal target. It is included because the actual approximants are invariants on all knots.

Throughout this section p and q are coprime integers; noncoprime parameters describe links and are excluded. Every case with |p|=1 or |q|=1 represents the unknot and must be handled before any division by v_2. If zero parameters are allowed, coprimality restricts them to (0,±1) or (±1,0), again the unknot. The enumeration below includes that one knot only once.

Let v_2 and v_3 be the type-two and type-three invariants normalized to equal 1 on the positive trefoil, with v_2 mirror-even and v_3 mirror-odd. Willerton [W, §3, p. 5], citing Alvarez-Labastida, gives

    v_2(T(p,q)) = (p^2-1)(q^2-1)/24,
    v_3(T(p,q)) = pq(p^2-1)(q^2-1)/144.

These two values determine a torus-knot type, including its mirror. Here is the algebraic verification. If the knot is nontrivial, v_2 is positive. From a=v_2 and b=v_3 recover

    P = pq = 6b/a,
    p^2+q^2 = P^2+1-24a,
    p^2 q^2 = P^2.

Thus p^2 and q^2 are the roots of a known quadratic; their unordered pair and the sign of pq determine the torus knot up to the standard identifications (p,q), (q,p), (-p,-q), and (-q,-p). The unknot is the only torus knot with a=0. Torus knots are invertible, so this classification also suffices for oriented knots. In the standard model (r exp(ipt),s exp(iqt)) in the unit 3-sphere, simultaneous complex conjugation reverses t and has determinant +1 in R^4. It lies in the connected group SO(4), giving an orientation-preserving ambient isotopy identifying the knot with its reverse. This establishes the required injectivity, without using a conjecture about colored Jones signatures.

Enumerate the distinct torus-knot types T_1,T_2,..., including both chiralities and the unknot. Set (a_i,b_i)=(v_2(T_i),v_3(T_i)). Define

    Q_n(K) = sum over i=1,...,n of sigma(T_i) *
      product over j != i of
      [(v_2(K)-a_j)^2+(v_3(K)-b_j)^2]
      /[(a_i-a_j)^2+(b_i-b_j)^2].

Every denominator is nonzero. Each factor has finite-type degree at most 6, so Q_n has degree at most 6(n-1). For all n>=i, Q_n(T_i)=sigma(T_i). This proves eventual exact pointwise convergence on every torus knot. It asserts no convergence to signature at knots outside that family. The finite labels sigma(T_i) may be obtained by their ordinary Seifert matrices; interpolation does not compute an unknown label from nowhere.

## 6 Why tempting stronger conclusions fail

### Fixed degree and uniform convergence

A pointwise limit of invariants all of degree at most d is still of degree at most d: take the limit of the finite alternating sum on each (d+1)-singular knot. Since signature is not finite type, no bounded-degree tail can solve the problem.

There is a stronger published finite-cutoff obstruction. Stoimenow [S, Theorem 3 and the following definition, printed p. 467] states that for any fixed knot, any fixed cutoff, and any admissible single Levine-Tristram signature value, a knot with that value can have the same Vassiliev data below the cutoff. Its n-similarity convention is equality in degrees strictly less than n; for an invariant of type at most d one therefore takes n=d+1. At -1 all even values are admissible. Thus, for any fixed finite-type invariant v and base knot K_0, one can find knots L_s with v(L_s)=v(K_0) and sigma(L_s)=s for all even s. Consequently

    sup over all knots K of |v(K)-sigma(K)| = infinity.

This consequence rules out uniform approximation emphatically. It does not rule out the requested pointwise convergence. The logical gap is

    for every d there exists L_d with matching data through d

versus

    there exists one L with matching data for every d.

No compactness principle supplying that exchange has been established here.

There is even a concrete escape mechanism when s differs from sigma(K_0) modulo 4. If L_d matches all invariants through d, then its Conway coefficients up to degree d match K_0's. Once d is at least the Conway degree of K_0, L_d must have a nonzero Conway coefficient of degree greater than d; otherwise its entire Conway polynomial, and hence its signature residue, would agree with K_0's. Thus this kind of moving counterexample necessarily escapes every fixed Conway-degree bound.

### An Alexander-only sequence cannot recover the full signature

Let

    V_+ = [[1,1],[0,1]],   V_- = -V_+.

These are Seifert matrices for opposite trefoils in a suitable sign convention. They have the same normalized Conway polynomial 1+z^2. Their symmetric matrices have signatures +2 and -2. Any sequence whose terms depend only on the complete Conway polynomial takes identical values on these two knots, so it cannot converge to both full signatures. The example is independent of which trefoil is called positive.

A related published restriction is stronger: every rational finite-type invariant that is invariant under S-equivalence is a polynomial in Conway coefficients. This is the Murakami-Ohtsuki result, stated explicitly with that scope by Conant-Mostovoy-Stanford [CMS, v2, p. 2]. Hence rational approximants which individually factor through S-equivalence cannot solve the signature problem, although signature itself factors through S-equivalence. This uses an external theorem; its full clasper proof has not been re-audited in this pass. The preceding Alexander-only counterexample is independent of that theorem.

### Polynomial coefficient approximation and the colored Jones conjecture

Kofman-Rong's actual positive results approximate polynomial coefficients and specializations [KR]. They do not identify full signature as one of those approximated invariants. Such results cannot supply the missing signature-separation hypothesis by themselves.

Garoufalidis [G, v1, §1.3] formulates a colored-Jones jump conjecture for knots whose Alexander roots on the unit circle are simple. The paper explicitly says that its displayed jump formula fails without that simplicity assumption and asks for a higher-order extension to all knots. It is not an unconditional all-knots signature theorem. Its computational verifications were not rerun here, and no source-author code was executed. Our torus partial case uses [W], not that conjecture or its claimed special-case proof.

## 7 Computations and limits

The original arithmetic study used exact Fraction arithmetic; its code and raw outputs are not distributed in this prose edition. It checks the sign interpolation at 210 nodes, the residue identity on 125 genus-one integral Seifert matrices and 16 block-diagonal pairs, torus-feature reconstruction for 156 signed parameter instances, and cardinal interpolation at five nodes. These finite tests corroborate formulas whose general proofs are given above; they do not establish all-knots separation.

Five deliberate negative controls are rejected: replacing the signed Alexander value by its absolute value; confusing a residue with both opposite full signatures; dropping the mirror-sensitive feature; using sign interpolation outside its finite node set; and holding the Conway truncation fixed. The same outcomes hold under normal Python, -O, and -OO, because checks do not depend on assert statements.

## 8 Exact remaining work

A full positive proof must establish the mirror-detection property of Theorem 3, or another hypothesis that implies its pair-separation conclusion. A full negative proof must exhibit one fixed knot with nonzero signature invisible to all finite-type mirror tests, with an all-degree proof. Neither an arbitrary large finite calculation, bounded-degree similarity, polynomial-coefficient recovery, nor a special knot family supplies either outcome.

The bounded primary-literature audit did not locate a current resolution of the exact question. This is not a proof that no resolution exists, an exhaustive literature search, or a priority claim. The proper disposition of this pass is **PARTIAL: exact reduction and proved partial cases; original question unresolved here**.

## References

[O] T. Ohtsuki, editor, Problems on invariants of knots and 3-manifolds, Geometry & Topology Monographs 4 (2002), Problem 2.9, printed p. 403. https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf

[KR] I. Kofman and Y. Rong, Approximating Jones coefficients and other link invariants by Vassiliev invariants, arXiv:math/0007093v1 (2000). https://arxiv.org/abs/math/0007093

[R] P. Røgen, On density of the Vassiliev invariants, Journal of Knot Theory and Its Ramifications 8 (1999), 249-252. Institutional abstract inspected, not the full article: https://orbit.dtu.dk/en/publications/on-density-of-the-vassiliev-invariants

[CDM] S. Chmutov, S. Duzhin and J. Mostovoy, Introduction to Vassiliev Knot Invariants, author-hosted as-submitted text, containing a January 2011 preface reference; §3.2. https://www.math.cinvestav.mx/~mostovoy/cdbook/cdbook-as-submitted.pdf

[S] A. Stoimenow, Some applications of Tristram-Levine signatures and relation to Vassiliev invariants, Advances in Mathematics 194 (2005), 463-484. https://doi.org/10.1016/j.aim.2004.07.003 ; inspected public PDF: https://webhomes.maths.ed.ac.uk/~v1ranick/papers/stoim2.pdf

[W] S. Willerton, On the first two Vassiliev invariants, arXiv:math/0104061v1 (2001), §3. https://arxiv.org/abs/math/0104061

[MO] H. Murakami and T. Ohtsuki, Finite type invariants of knots via their Seifert matrices, arXiv:math/9903069v2 (2000 revision). https://arxiv.org/abs/math/9903069

[CMS] J. Conant, J. Mostovoy and T. Stanford, Finite-type knot invariants based on the band-pass and doubled-delta moves, arXiv:math/0511189v2 (2009 revision). https://arxiv.org/abs/math/0511189

[G] S. Garoufalidis, Does the Jones polynomial determine the signature of a knot?, arXiv:math/0310203v1 (2003). https://arxiv.org/abs/math/0310203
