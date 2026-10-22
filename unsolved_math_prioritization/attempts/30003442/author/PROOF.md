# A verified small-parameter reduction for largest mixed-characteristic roots

## Scope and status

Let m,d be positive integers. Let P be a real homogeneous polynomial of degree d in m variables, nonvanishing whenever every variable has strictly positive imaginary part, and satisfying ∂iP(1,...,1)=d/m for each i. Put

χP(t)=[∏i(1−∂i)P](t,...,t), and P∞=(x1+...+xm)^d/m^d.

The target asks whether maxroot(χP)≤maxroot(χP∞) for every such P. This note proves it for min(m,d)≤3. It does not resolve the unrestricted question or claim that this partial result is new. Its proofs do not use the symmetric-subclass theorem announced in the 2017 report.

## 1. Normalization and elementary stability facts

Euler's identity gives dP(1)=Σi∂iP(1)=d, so P(1)=1. The following standard closure properties of real stability are used: derivatives, real specializations and limits preserve stability or give zero; and 1−∂i preserves stability. The last fact follows by fixing the other variables in the upper half-plane: if f has all its zeros outside that half-plane, Im(f'/f)<0 there unless f is constant, so f'/f cannot equal 1. The same argument, with a limiting perturbation for degree loss, gives the derivative property; real specialization follows from Hurwitz's theorem.

For completeness P has nonnegative coefficients, even though that is not an additional assumption in the primary statement. If a>0 coordinatewise, P(a) cannot be zero, since P(ia)=i^dP(a) would then violate stability. The positive orthant is connected, so P(a)>0 because P(1)=1. For every fixed positive vector a, the real polynomial P(a+te_i) is real-rooted by real specialization, has no zero at t≥0, and is positive at t=0. Thus all its roots are negative and all its coefficients are nonnegative. In particular ∂iP≥0 on the positive orthant. Iterate this argument on each nonzero derivative (which is homogeneous and stable) to see that every mixed derivative is nonnegative on the positive orthant. Continuity at the origin proves coefficient nonnegativity.

Consequently the coefficients of P define a probability distribution on integer vectors X=(X1,...,Xm) with Xi≥0 and ΣXi=d. Its generating polynomial is P, and EXi=d/m. Each marginal generating function Fi(z)=P(1,...,z,...,1) has nonnegative coefficients, value 1 at z=1, and only nonpositive real zeros. Hence, padding with zero parameters if necessary,

Fi(z)=∏j=1^d(1−θij+θij z),  0≤θij≤1,  Σjθij=d/m.

This is only a representation of each one-coordinate marginal by independent Bernoulli variables; no independence of X1,...,Xm is asserted.

Write Ck(P)=Σ|S|=k ∂SP(1). Homogeneity gives

χP(t)=Σk=0^min(m,d)(−1)^k Ck(P)t^(d−k),  C0=1, C1=d.

Its degree is exactly d and it is real-rooted. In probabilistic notation Ck(P)=E ek(X). For the reference polynomial,

Ck(P∞)=binom(m,k)(d)k/m^k,

where (d)k=d(d−1)...(d−k+1). These formulas include m<d; a zero of multiplicity at least d−m is then present. Degree zero is excluded because a largest root is not defined.

## 2. Exact moment comparison

Set μ=d/m, a=1/m, and

Δ2=Σi,j(θij−a)^2,
Δ3=Σi,j θij^3−d/m^2.

Since Σi,jθij=d and there are md parameters,

Δ2=Σi,jθij²−d/m≥0,
Δ3=Σi,j(θij−a)²(θij+2a).

In particular, with M=min(1,d/m)+2/m,

0≤Δ3≤MΔ2.                                      (2.1)

The upper bound follows because each θij≤min(1,Σjθij)=min(1,d/m).

The Bernoulli-sum moment identities are

EXi²=μ²+μ−Σjθij²,
EXi³=μ³+3μ²+μ−3(μ+1)Σjθij²+2Σjθij³.

Newton's identities and ΣXi=d give

e2(X)=(d²−ΣXi²)/2,
e3(X)=(d³−3dΣXi²+2ΣXi³)/6.

Subtracting the reference case θij=a yields the exact identities

C2(P)−C2(P∞)=Δ2/2,                              (2.2)
C3(P)−C3(P∞)=(d/2−d/m−1)Δ2+(2/3)Δ3.            (2.3)

Only the identity with existing indices is needed in a given dimension.

## 3. The theorem when min(m,d)≤2

If d=1, χP=t−1. If m=1, P=x1^d and χP=t^(d−1)(t−d). The comparison is equality in both cases.

Assume min(m,d)=2 and let a0=C2(P∞). After removing a factor t^(d−2), χP=t²−dt+a0+Δ2/2. Its largest real root is no larger than the largest root of t²−dt+a0, because their discriminants differ by −2Δ2. All roots of the unreduced polynomial are real, and the quadratic's largest root is positive since its two roots sum to d>0. The extra zero roots cannot change the largest root. Explicitly the reference largest root is 1+1/√m when d=2, and (d+√d)/2 when m=2.

## 4. The theorem when min(m,d)=3

Remove the nonnegative power t^(d−3). The remaining cubics are

q(t)=t³−dt²+C2(P)t−C3(P),
q0(t)=t³−dt²+C2(P∞)t−C3(P∞).

Let L be the largest root of q0. It is positive: q0 is real-rooted and its roots sum to d>0. For t>L, q0(t)>0 and q0'(t)>0, as follows immediately from the factorization into real linear factors.

If Δ2=0 then (2.1) gives Δ3=0, and q=q0. Otherwise write

B=2[C3(P)−C3(P∞)]/Δ2.

Equations (2.2)–(2.3) imply

q(t)−q0(t)=(Δ2/2)(t−B),
q'(t)−q0'(t)=Δ2/2.

It suffices to prove B<L: then q(L)>0 and q'(t)>0 for t>L, so q has no real root at or above L.

Case m=3, d≥3. From (2.1), Δ3/Δ2≤5/3. Consequently

B≤d−2d/3−2+(4/3)(5/3)=d/3+2/9.

Direct expansion gives

q0(d/3+u)=u³−(d/3)u−2d/27.

At u=2/9 this equals 8/729−4d/27<0. A monic real-rooted polynomial is positive to the right of its largest root, so L>d/3+2/9≥B.

Case d=3, m≥3. Here θij≤3/m and Δ3/Δ2≤5/m. Thus

B≤3−6/m−2+20/(3m)=1+2/(3m).

Direct expansion gives

q0(1+u)=u³−3u/m−2/m².

At u=2/(3m) this equals 8/(27m³)−4/m²<0. Therefore L>1+2/(3m)≥B.

This completes the proof for min(m,d)≤3, including every positive m,d in those ranges. If Δ2>0 the inequality is strict in the cubic cases; no classification of P from the equality condition Δ2=0 is claimed.

## 5. Exact obstruction to permutation averaging

One cannot reduce the full problem to the announced symmetric subclass by averaging all permutations. Set

P(x,y,z,w)=(x+y)²(z+w)²/16.

Each linear factor has positive imaginary part when its arguments do, so P is stable. It has P(1)=1 and each first partial derivative at 1 equal to 1. Its full permutation average is

Q=[(x+y)²(z+w)²+(x+z)²(y+w)²+(x+w)²(y+z)²]/48.

Yet Q(t,−1,0,1)=(t²+1)/24, which is not real-rooted. Real specialization of a real stable polynomial is real stable or zero, so Q is not stable. Nevertheless permutation equivariance of χ gives χQ=χP=(t²−2t+1/2)², which is real-rooted. Thus real-rootedness of χ, multivariate stability of its input, and stability of full permutation averaging are genuinely different statements.

## 6. Flow signs, corrected flow, and the remaining gap

The printed 2017 report defines T=(Σxi)(Σ∂i)/(md), and prints exp(s(I−T)), while asserting stability preservation and convergence to P∞. This sign cannot be correct. For m=d=2 and P=xy, TP=P∞=(x+y)²/4 and T(P−P∞)=0. At s=log 2 the printed expression is 2xy−P∞, whose χ is t²−2t+3/2 and is not real-rooted.

The corrected semigroup is exp(s(T−I)). Put r=exp(−s/d). It equals the explicit stable substitution

P(x) ↦ P(rx1+(1−r)x̄,...,rxm+(1−r)x̄),  x̄=(Σxi)/m.

To verify the formula, the infinitesimal generator at s=0 is (1/d)Σi(x̄−xi)∂i=T−I by Euler's identity. The substitutions compose by multiplying r; their linear coefficients are nonnegative with row and column sums 1, so they preserve stability and the prescribed gradient. They converge to P(x̄1)=x̄^d=P∞. For P=xy this corrected flow increases, rather than decreases, the largest root: at s=log 2 it is 1/2 xy+1/2 P∞, whose χ=t²−2t+3/4 has largest root 3/2, whereas χxy=(t−1)² has largest root 1. Both printed sign/direction issues have therefore been checked independently, not silently repaired by assumption.

If f=χP, direct differentiation gives

χ(TP)=[(mt−m+d−1)f'(t)−t f''(t)]/(md).

Along the corrected flow, at a simple largest root λ the velocity is

λ'=[λ f''(λ)/f'(λ)−mλ+m−d+1]/(md).

Thus a monotonicity proof would require the numerator to be nonnegative for every admissible input encountered. Stability of the flow alone does not establish that inequality. We do not establish it for all m,d. The cubic argument works because no Ck with k≥4 remain; in larger cases (2.2)–(2.3) do not control the additional coefficients. The unrestricted largest-root problem remains unresolved by this work.

## 7. Scope of the exact computational checks

The verifier's product examples use matrices that are averages of permutation matrices. Their rows and columns sum to one, so products of their row linear forms are homogeneous, real stable, normalized, and have the required gradient. The additional low-parameter examples start from a cyclically invariant product of nonnegative linear forms and apply D=Σ∂i repeatedly, dividing by the current degree at each step. Directional differentiation by D preserves stability: apply single-variable differentiation to the stable polynomial P(x1+u,...,xm+u), then specialize u=0. Cyclic invariance is preserved, so all gradient coordinates remain equal; normalization makes each equal to d/m. Thus their admissibility follows from exact constructions, not from sampling points to test stability.

The program uses rational arithmetic, exact polynomial identities and certified rational real-root isolation. It includes 12 boundary identities, four direct differential-operator crosschecks, 58 admissible polynomial examples (22 in the small-parameter proof range and 36 product-polynomial tests), and four deliberately false-claim controls. The finite product tests check a proper subclass at selected points only. Package-integrity corruption tests are separate from mathematical tests.
