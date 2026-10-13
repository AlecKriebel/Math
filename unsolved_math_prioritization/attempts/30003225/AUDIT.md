# Independent adversarial audit: free-chain Nash intersections

## Verdict

**ACCEPT the counterexample to the precisely disclosed normalized statement.** The three-free-blowup calculation is correct as an equality of closed reduced sets of formal arcs. Every positive integer contact multiplicity is excluded. The optional all-free-chain formula is also accepted analytically. No mathematical correction is required to the pinned manuscript.

This acceptance is **not** authentication of an author erratum or an unqualified resolution of the intended original conjecture. The source's general notation and its explicit first-divisor specialization are not fully reconciled. The mathematical statement actually disproved must be displayed wherever this result is used.

Audited manuscript: *A three-free-blowup counterexample to the disclosed normalized intersection statement*, 13,104 bytes, SHA-256 `896bfc35dca18a351685fa32d213602fa805a0efa008b535377ed5d547d26613`. Audit date: 13 October 2026 UTC.

## 1. Exact statement accepted

Let the minimal model of a prime divisor E be obtained by blowing up centers c1=0,c2,...,cn. Let Dj be created by cj. Let Fk(E) contain all same-combinatorial-type divisors sharing the first k centers, with c(k+1) free, and let Ik(E) be the intersection of their closed Nash sets.

The claim that Ik(E) must equal C(q ord_Dk) for some positive integer q is false. For n=3,k=2, with c2 the tangent y=0 and c3 any free point on D2,

    I2(E) = {ord x >= 2, ord y >= 3},
    C(q ord_D2) = {ord x >= q, ord y >= 2q}.

The order of the zero series is infinity. Both equalities include the constant arc through closure.

## 2. Blowup geometry and completeness of the family

After the first blowup use x=r,y=ru. Blowing up (r,u)=(0,0) has charts

    U: (x,y) = (x,x²v),
    V: (x,y) = (su,su²).

In V, D2 is u=0 and the strict transform of D1 is s=0. The transition v=1/s identifies the unique omitted point of U on D2 with D1∩D2. It is satellite. Consequently the entire free locus of D2 is the affine line v=a with a in C, and no free center at infinity is missing.

Blow up (x,v)=(0,a). Its two charts have base maps

    (x,w) -> (x, ax²+x³w),
    (z,h) -> (zh, z²h²(a+h)).

The new component Ea has local equations x=0 and h=0 respectively. In the second chart y-ax²=z²h³. The old D2 is z=0, and its intersection with Ea is the unique point outside the first chart. The divisorial valuation is therefore monomial of weights (1,3) in coordinates (x,y-ax²).

The three-free-center minimal model has weighted graph (-2)-(-2)-(-1). A third blowup on D1 away from D2 would have a different minimal model: the blowup at c2 would be extraneous to the resulting prime divisor. A blowup at D1∩D2 has satellite proximity data and a different graph. Thus the same-type family sharing c1,c2 is exactly {Ea:a in C}. This is an exhaustion argument, not a selected one-parameter subfamily of a larger allowed family.

## 3. Formal closure audited without a valuative-converse shortcut

For centered arcs write x=x1 t+x2 t²+... and y=y1 t+y2 t²+.... Define

    Sa = {ord x >= 1, ord(y-ax²) >= 3}.

Its ideal in the centered arc coordinate ring is (y1,y2-a x1²). Eliminating these two generators identifies its coordinate ring with a polynomial ring in the remaining countably many coefficients. It is an irreducible reduced closed cylinder. The nonempty principal open x1≠0 is dense.

Every arc in that principal open has the formal quotient w=(y-ax²)/x³ and lifts transversely to Ea at a smooth point of the exceptional locus. Conversely every nonconstant arc whose lift meets Ea lies in Sa: in the first chart this follows from y-ax²=x³w; in the second it follows from x=zh and y-ax²=z²h³ with ord h>=1. These two charts cover Ea. Hence the entire raw Nash set is contained in Sa, while its transverse subset contains a dense open of Sa. This proves closure(NEa)=Sa directly.

The same two-chart argument for D2 and any fixed q proves

    C(q ord_D2) = {ord x >= q, ord y >= 2q}.

In chart U, the local equation of D2 is x. In chart V, it is u and x=su,y=su². Thus every exact-q lifted arc satisfies the displayed bounds. The open ord x=q in the target coordinate cylinder is dense and lifts in U with order exactly q. No approximation by convergent arcs or unproved implication from valuation domination is needed.

The constant arc is indeed in every closure. For example x=e t,y=a e²t² gives transverse arcs for every nonzero constant e and specializes to the constant arc at e=0.

## 4. Intersection, nonreduced scheme caveat, and witnesses

Intersecting a=0 and a=1 yields ord y>=3 and ord(y-x²)>=3. Thus ord x²>=3, equivalent over a field to ord x>=2. Conversely these two lower bounds imply every parameter-a condition. Therefore two members already give the full family intersection.

At two-jet level, the sum of the defining ideals is (y1,y2,x1²); its radical is (y1,y2,x1). The nonradical ideal does not contain x1. The manuscript explicitly treats an equality of closed sets/reduced supports and does not falsely assert scheme-theoretic equality.

For q=1, (t,t³) belongs to the proposed contact cylinder and not the intersection. For every q>=2, (t²,t³) belongs to the intersection but fails ord y>=2q. These are polynomial, nonconstant, convergent arcs, so neither formal convergence issues nor the constant arc create the counterexample.

The second witness need not itself lift to any finite Ea. It meets the old satellite point. Its membership in every *closed* Nash set is nevertheless explicit: for each fixed a, the polynomial wedge

    x=e t+t²,
    y=a(e t+t²)²+t³-a t⁴

specializes to (t²,t³) at e=0, while at every nonzero e it has ord x=1 and ord(y-ax²)=3 and lifts transversely to Ea. This is a direct check of the closure-dependent part of the argument.

## 5. Independent geometric and dimensional checks

Blowing up the omitted satellite point D1∩D2 gives a different prime divisor F. In chart V use s=p,u=pq, obtaining x=p²q,y=p³q². Thus ord_F=(2,3), and the computed intersection is C(ord_F). For arcs with exact orders (2,3), the inverse expressions p=x²/y and q=y²/x³ give ord p=1 and ord q=0, exhibiting a dense transverse locus on F.

This explains the obstruction geometrically: varying all permitted free centers produces the closed Nash set of the excluded satellite divisor. It does not produce a multiple of D2.

In the full arc space the intersection has codimension 2+3=5. The proposed q-multiple cylinder has codimension q+2q=3q. No positive integer q makes these equal. In the centered arc space subtract 2 from both codimensions. The Jacobians in the free and satellite charts have orders 3 and 4 respectively, agreeing with log discrepancies 4 and 5. These are consistency checks; the explicit cylinder proof and witnesses already establish the result.

## 6. Audit of the optional all-free-chain formula

For n successive free blowups and 2<=k<n, flatten the fixed smooth branch jet in coordinates (x,z). The common tangent is fixed, so x is a parameter for every curvetta in the family. Each subsequent finite free center records the next coefficient, while the unique point at infinity is satellite. Induction gives all completions, with no omissions, as parameters a_k,...,a_(n-1), and their Nash cylinders are

    {ord x>=1, ord(z-sum_(j=k)^(n-1) a_j x^j)>=n}.

This is the same dense-open and two-chart closure argument at each blowup. The all-zero member forces ord z>=n. Comparing it with the member a_k=1 and all other coefficients zero forces k ord x>=n. These imply every member's bound since j>=k. Hence

    Ik(E) = {ord x>=ceil(n/k), ord z>=n}.

The target C(q ord_Dk) has independent coordinate thresholds (q,kq). Two coordinate order cylinders agree only when both thresholds agree, as is seen by choosing independent monomial coordinates of sufficiently high other order. Equality therefore holds exactly when k divides n, with q=n/k. This is a universal analytic argument; finite threshold checks are only sanity checks.

## 7. Source scope and adversarial interpretation review

The primary general statement uses an intersection, not a union. The paper defines the relation with contact at least i but prints a relation without the inequality symbol in its conjecture. Its explicit i=1 specialization uses the divisor created at the origin, while the general expression is indexed by a selected free infinitely-near point. The disclosed normalized statement chooses a precise meaning for these conventions, rather than silently identifying them. See [Fernández de Bobadilla, Pe Pereira, and Popescu-Pampu, §4.2, pp.30–32](https://arxiv.org/pdf/1501.06898v3).

The definitions do not restrict the conjecture to satellite divisors or divisors coming from minimal embedded resolutions of singular branches. The discussion expressly includes nonsatellite prime divisors and the extra free points after a branch is resolved. Thus the all-free example is not excluded by a source-stated hypothesis. The first-exceptional specialization is untouched. See [the same paper, §2, pp.6–7, and Remark 4.14, p.31](https://arxiv.org/pdf/1501.06898v3).

The independent closure proof is consistent with the definitions of transverse liftings and closed Nash sets and with density of the transverse locus. The toric identification agrees with [Ishii, *Maximal divisorial sets in arc spaces*, Example 2.10 and Proposition 3.4](https://arxiv.org/pdf/math/0612185). These are credited background results, not discoveries of this audit.

The workshop statement also uses the intersection and identifies the printed divisor as the one created by blowing up the selected point. That evidence confirms a genuine interpretation issue; it does not authorize choosing an intended correction on the authors' behalf. See [Pe Pereira's contribution, printed pp.2678–2680, especially Conjecture 1 on p.2679](https://ems.press/content/serial-article-files/46651).

No theorem here is claimed about unspecified alternative meanings, about the paper's second conjecture, or about global novelty. No mathematical loophole was found in the normalized counterexample, but its simplicity by itself does not authenticate the source normalization.

## 8. Five-free-blowup case robust to the natural index readings

This section applies the already audited general formula; it does not assume an authenticated correction to the source.

Take a reference divisor E=D5 produced by five successive free blowups along the branch y=0. Each of c2,c3,c4,c5 is a free center, and every reference prefix divisor Dj has monomial weights (1,j), for j=1,...,5. Select the middle free center c3. Keeping only c1,c2 fixed leaves three free choices. Keeping c1,c2,c3 fixed leaves two free choices. Neither family is a singleton or an endpoint degeneracy.

For F2, write the free completions as a2,a3,a4. Their closed Nash sets are

    {ord x>=1, ord(y-a2 x²-a3 x³-a4 x⁴)>=5}.

The all-zero completion and (a2,a3,a4)=(1,0,0) imply ord y>=5 and 2 ord x>=5. Conversely these bounds imply the condition for every parameter tuple. Hence

    I2(E) = {ord x>=3, ord y>=5}.

For F3, write the remaining free choices as a3,a4. The same comparison between (0,0) and (1,0) gives

    I3(E) = {ord x>=2, ord y>=5}.

For every j=1,...,5 and q>=1,

    C(q ord_Dj) = {ord x>=q, ord y>=jq}.

Independent coordinate order bounds must agree if the cylinders agree. Equality with I2 would require q=3 and 3j=5. Equality with I3 would require q=2 and 2j=5. Neither has an integer solution. In fact the arithmetic excludes every integer j>=1, though only reference divisors in the actual minimal model are needed.

### Explicit mapping from source notation to tested variants

1. **Disclosed last-shared normalization.** With k=2, c3 is the first movable free center; the family is F2 and the proposed right side is C(q ord_D2). The first five-blowup calculation disproves this.
2. **Literal created-divisor expression with zero-based centers.** Write p0=c1,p1=c2,p2=c3,p3=c4,p4=c5, consistent with the paper's explicit zero-based chains. Choosing the free point p2 and reading the bare relation as the nearby defined contact-at-least-2 relation gives family F2, while the printed created-divisor phrase gives Ep2=D3. The first calculation also disproves this mixed reading.
3. **Fix the selected free point as well.** Keep c3 fixed, use family F3, and retain the divisor D3 created by c3. The second calculation disproves this coherent alternative. This is exactly the possible repair that is trivial in the three-blowup example, so the five-blowup case removes that endpoint loophole.
4. **One-based point labels in the general sentence.** If p_i=c_i, select p3=c3. A contact-at-least-3 family fixes through c3 and the created divisor is D3. This is again the F3/D3 case, already disproved. This local indexing choice is not asserted to reconcile every other passage of the paper.

The mappings use the source's count of common blown-up points (§2, p.7), its relation defined at the start of §4.2 (p.30), and the created-divisor phrase in the workshop conjecture (p.2679). The indexing caveat remains essential. The calculations establish failure of the explicitly listed variants; they do not certify which variant the authors intended.

For completeness, an *additional explicitly conditional* exact-contact reading of the undefined bare relation would not rescue this example either. At cut k=2 or k=3, take two completions with the first moving coefficient equal to 1 and 2 and every later coefficient zero. Each has exact contact k with the all-zero reference E. Subtracting the two conditions gives k ord x>=5 and then ord y>=5. Thus the exact-contact subfamily has the same reduced intersection for these examples. This observation does not adopt that reading or claim it was source-defined.

**Source-scope conclusion:** the five-blowup case is an accepted counterexample under both natural coherent interpretations identified during normalization, as well as the literal mixed-index reading. This materially strengthens the result beyond a counterexample that could disappear merely by fixing the selected free point. It still does not supply an author-authenticated erratum, settle an unspecified alternative conjecture, or address Conjecture 2. A safe result label is “counterexample to the displayed Nash-intersection assertion under the explicit natural indexing readings,” accompanied by this mapping and caveat.

## 9. Exact controls and limitations

The accompanying independent verifier checks both blowup charts, transition functions, valuation exponents, Jacobians, the satellite chart and its inverse, the two-jet ideal and its nonradical character, a closure wedge, constant-arc specialization, witnesses, the five-blowup four-jet radicals, and negative controls for common incorrect variants. Its explicit failure checks remain active with Python optimization enabled. Normal, -O, and -OO executions produce identical results.

These symbolic controls support the proof; they do not certify source interpretation or replace the analytic exhaustion, density, or universal-quantifier arguments.
