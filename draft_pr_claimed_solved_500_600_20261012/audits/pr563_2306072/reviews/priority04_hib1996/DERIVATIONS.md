# Independent constructive comparison with Hibschweiler1996

This is a priority/scope derivation, not a re-audit of PR563's entire proof. The full primary article pp789–795 was inspected as text and scans. Its header says789–796, but this seven-page file ends with the bibliography on795. The exact normalized S and actual omitted-slit assumptions agree with the candidate's setting.

## 1. Exact two-point differential and the zero-value case

Write `J(h)=h(ζ1)+h(ζ2)`, `a=f(ζ1)`, `b=f(ζ2)`, with nonzero points ζj in D. Hibschweiler's equation(3) is

`[a²/(a−w)+b²/(b−w)] (dw/w)² > 0`

on the **actual omitted arc** Γ of a global maximizer. In the article's section3 the hypothesis is the complex equality `J(f)=0`, not merely `Re J(f)=0`. Thus `b=−a`, and exact algebra gives

`Φ(w)=−2a²w/(w²−a²)`,

`Q(w)=−2a²/[w(w−a)(w+a)]`.

Because f is univalent and ζj≠0, a≠0. The differential is therefore nondegenerate. The paper discusses complete trajectory continuations of this expression under a rotation. It **does not prove a nonreal parameter pair with a global extremizer satisfying the proposed irrational-phase/dense-continuation conditions**. Its final spiral claim is explicitly conjectural. Neither statement identifies a polar/radial reversal on Γ. Continuing an analytic arc past its finite slit tip does not keep it inside the omitted set. Γ itself has increasing modulus and the usual interior π/4 radial-angle bound.

The general trajectory-density assertion in the paper is cited to outside theory rather than proved there. I do not certify that assertion; it is not needed to establish the article's lack of a proved actual-slit reversal.

## 2. An explicit actual zero-value extremal is a positive control

The paper gives zero-value examples by choosing real points in the interval where Koebe individually maximizes point evaluation. Here is an exact representative, independently specified:

`ζ2=−1/3`, `ζ1=p=(11−4√7)/3`.

The number p is the smaller root of `T(p)=3p²−22p+3=0`, and `1/10<p<1/5`. With `k(z)=z/(1−z)²`,

`k(−1/3)=−3/16`,

`k(p)−3/16=−T(p)/[16(1−p)²]=0`.

The negative point −1/3 lies strictly above `(1−e)/(1+e)` because e>2; p is positive and below1. Brown's point-evaluation theorem therefore gives k as the unique maximizing function at each of these two points. Summing the two inequalities proves **global** extremality of k for J, with `J(k)=0`. It is not a formal-trajectory sufficiency argument. J is nonconstant on S, since its value on the identity is `p−1/3<0`, while its real maximum is0.

The actual omitted arc is `Γ=(−∞,−1/4]`. Polar argument is constant and both radial-angle conventions are zero. Thus the paper's explicit zero-extremal construction cannot serve as this negative example.

Hibschweiler Theorem5 states more: under `f∼J` and `J(f)=0`, real opposite-sign ζ1,ζ2 force `f=k`, and conversely k forces this point condition. The intended reflection proof is compatible with the following corrected calculation.

Let `u=e^(iα)` be the tip preimage. The reflected source expression is

`Φ_disk(z)=A z(z−u)²/[(z−ζ1)(1−barζ1 z)(z−ζ2)(1−barζ2 z)]`.

On `z=e^(iθ)`, each denominator pair becomes `z|1−barζj z|²`, and

`(z−u)²/(zu)=−|1−z/u|²`.

Hence the boundary expression is

`Φ_disk(e^(iθ))=−Au |1−e^(i(θ−α))|²/[|1−barζ1 e^(iθ)|² |1−barζ2 e^(iθ)|²]`.

The printed line on p794 omits this minus sign. Its intended conclusion `Au>0` follows from the corrected expression and the nonpositive boundary differential. Near z=0, the direct expression has leading term2z, so `Au²=2ζ1ζ2`. For real opposite-sign points, `Au>0` and `Au²<0` imply u=−1. The resulting boundary differential is even under θ↦−θ. Equality of natural-coordinate lengths from the tip pairs opposite boundary preimages. Leung's reflection argument then gives the Koebe function. This repairs the local sign slip; it does not create a target reversal.

The source uses the standard boundary regularity of an analytic support slit and the usual quadratic-differential reflection representation. Those analytic premises are classical and are not formally verified by the finite controls here.

## 3. Non-Koebe/nonunique cases do not imply target reversal

Theorem2 uses continuity of point-evaluation extremality at a real `r∈(−1,(1−e)/(1+e))` to exclude both real Koebe rotations for two evaluation points sufficiently near r. Theorem1 and its corollary supply conjugate pairs of distinct extrema for real evaluation pairs or conjugate evaluation pairs. They do not specify a polar derivative with both signs or an interior zero flanked by nonzero radial angles.

A decisive control is `ζ1=ζ2=r=−3/4`, a permitted choice in the theorem's family. J is exactly `2h(r)`. Brown1979's fully inspected point-evaluation examples give distinct non-Koebe extrema related by conjugation, with monotone polar argument and monotone radial-angle magnitude. Thus the two properties emphasized in Hibschweiler's construction are compatible with both requested monotonicities. A mirrored partner is a different omitted arc, not two signs of radial angle on the same arc.

This does **not** prove that every non-Koebe two-evaluation support slit is monotone. Determining whether some unequal/nonreal evaluation pair yields a reversal remains a geometric question not settled by the article. No unpublished classification of that entire family is claimed here.

## 4. Rational-line cases are positive angle cases

Theorem4 assumes a rational support map and passage of the analytically continued arc through an evaluation pole. It invokes Srebro's straight-slit result and then proves the line horizontal. Regardless of the offset, a straight actual omitted half-line has monotone polar and radial angles.

For completeness, orient the line outward by a unit tangent u and write

`w(s)=u[x(s)+iy]`, `x(s)=x0+s`, `s≥0`,

where y is real and constant. Increasing modulus gives x>0 on the regular interior. Then

`θ′(s)=−y/[x(s)²+y²]`,

`β(s)=−arctan[y/x(s)]`, `β′(s)=y/[x(s)²+y²]`,

`d|β|/ds=−|y|/[x(s)²+y²]` for y≠0,

with all angles constant when y=0. Each sign is fixed. This is an independent geometry comparison of the theorem's actual line conclusion, not certification of the external Srebro theorem itself.

## 5. Theorem1 proof details and repair

The rational expression used for a Koebe rotation is

`F(t)=a²/(a−ct)+b²/(b−ct)`, `c=bar x`,

whose expansion is

`F(t)=a+b+2ct+c²(1/a+1/b)t²+c³(1/a²+1/b²)t³+...`.

The printed linear coefficient is missing a factor2. Reality of F still implies c is real, so x=±1 as intended.

The paper next infers real or conjugate a,b from real `a+b` and `1/a+1/b`. That inference requires a degenerate-case check: if a+b=0, both sums vanish even for `a=1+i`, `b=−1−i`. In this case the next coefficient `2c³/a²` is real, so a² is real. Consequently a,b are both real or a pure-imaginary conjugate pair. In the nondegenerate case, the two real sums imply ab real, so a,b are roots of a real quadratic and are real or conjugate. Koebe's conjugation symmetry and univalence then give the stated evaluation-point alternative. This supplies the missing case without a new support construction.

Theorem1(b)'s unique-extremal implication also uses the known actual slit geometry: a support map fixed by conjugation has a conjugation-invariant single omitted arc, with at most one point at each radius. Every such point is real, so the arc is a real ray and normalization gives a real Koebe rotation.

Theorem3 provides necessary inequalities for Koebe extremality, derived from the source differential and elementary competing functions; it does not assert an actual nonmonotone slit. Its corollary restricts evaluation points rather than producing angle sign changes.

## 6. Relation of the functional to PR563

As functionals on H(D), no nonzero scalar multiple of J can equal PR563's finite coefficient functional plus an affine normalization constant: evaluating on z⁵ and z⁶ would require both `ζ1⁵+ζ2⁵=0` and `ζ1⁶+ζ2⁶=0`. Since ζj≠0, division would force `ζ1/ζ2=1`, contradicting the first equality. **Different supporting functionals can share a support point**, so this algebraic distinction alone does not certify novelty or exclude shared extrema.

The strongest verified comparison is narrower: every actual slit explicitly identified in the inspected proofs is a positive-control line or Koebe case, the non-Koebe existence results carry no proved target angle reversal, and the continued-trajectory discussion lacks an actual nonreal extremizer construction and an on-slit reversal proof. This source supplies no verified earlier full negative answer to6.72.
