# Degree-corrected fixed-degree copositive closure: research and proof

Scope: row 1847, ID 30003654, OWR15957-007. This is a local mathematical correction and applications audit, not a full solution to an underspecified research program. No queue or repository publication is made here.

Primary-source inspection: the actual OWR contribution is Juan C. Vera, “Positive polynomials on unbounded domains,” joint work with Luis F. Zuluaga, printed pp. 38–39 in the 2017 Copositivity and Complete Positivity report. It asks for consequences and broader applications of a nonnegativity certificate, rather than one specified universal SOS theorem. Related primary source: Peña–Vera–Zuluaga, arXiv:1709.03435v1, September 2017, https://arxiv.org/pdf/1709.03435. Definition preceding Definition 3 defines tilde p by actual highest degree; Theorem 1 uses P_d consisting of degrees at most d. Those two conventions are incompatible in its printed necessity assertion. Source texts and PDFs are not reproduced here.

## Approach 1: exact correction and full proof

Let K be a pointed closed convex cone in R^n, S a closed subset of K, d a nonnegative integer, and h a nonzero polynomial of degree m≤d nonnegative on S. Write h_m for the degree-m homogeneous part of h, p_[d] for the degree-d component of p (zero when deg p<d), and Z=S∩{h=0}. All closures below are coefficient closures in R_d[x]. Then

cl(P_d(S)+h R_{d−m}[x]) = {p∈R_d[x]: p≥0 on Z and p_[d]≥0 on S∞∩{h_m=0}}.    (C)

Proof. A pointed closed convex cone has a linear functional a strictly positive on K\{0}, with a·x≥c||x|| on K for some c>0. Let L(t,u)=t+a·u and let C be the closure of {(1,x)/(1+a·x): x∈S}. It is compact in {t≥0,u∈K,L=1}. Its finite points (t>0) correspond exactly to S, since S is closed. Its points at infinity are exactly {(0,v):v∈S∞, a·v=1}. The last assertion follows in one direction by normalization and in the other by any defining sequence λ_j x_j→v, λ_j↓0, followed by normalization by 1+a·x_j.

For f∈R_d[x], put F(t,u)=t^d f(u/t), continuously extended as a homogeneous polynomial. Put H(t,u)=t^m h(u/t). Then P_d(S) corresponds exactly to F≥0 on C. H≥0 on C. On C∩{H=0}, the finite conditions F≥0 say p≥0 on Z; the infinite conditions say p_[d](v)≥0 wherever h_m(v)=0. Consequently the right side of (C) is exactly F≥0 on C∩{H=0}.

Necessity: every product H Q, where Q is the degree-(d−m) homogenization of q, vanishes on that zero set. Evaluation on C is continuous, so adding such products to nonnegative F and taking coefficient limits preserves nonnegativity there.

Sufficiency: suppose F≥0 on C∩{H=0}. For ε>0, compactness and continuity give δ>0 such that H<δ on C implies F+ε>0 (if the zero set is empty, take δ below min_C H). Let B=max_C |F|. For M≥B/δ, F+ε+M H≥0 on C. Since L=1 on C, the degree-d homogeneous polynomial F+ε L^d+M H L^(d−m) is nonnegative there. Dehomogenizing gives

p+ε(1+a·x)^d+M h(1+a·x)^(d−m) ∈ P_d(S).

Thus p+ε(1+a·x)^d lies in P_d(S)+hR_{d−m}[x] and tends coefficientwise to p. This proves (C). If S is empty the assertion is immediate. The zero polynomial h is handled separately: the left side is P_d(S), without using its undefined degree.

Parity note: no even-degree gap is required. The positive linear form L, not a norm-power or t alone, supplies the degree-gap multiplier. This relies essentially on the pointed-cone containment hypothesis.

## Approach 2: horizon geometry and rational certificates

The proof yields an explicit certificate family with a fixed known denominator:

p/(1+a·x)^d + ε + M h/(1+a·x)^m ≥ 0 on S.

This is an ambient nonnegativity certificate, not automatically an efficiently checkable SOS certificate. Its denominator is strictly positive on K. Coefficient closure corresponds to arbitrarily small ε in this prescribed perturbation direction.

Example with no horizon obstruction: S=R_+^2, h=x², d≥2. Z is the nonnegative y-axis and S∞∩{h_2=0}=Z∞. Every polynomial nonnegative on Z has p_[d] nonnegative on Z∞ by rescaling. Hence the closure equals P_d(Z). This includes odd d and makes the parity point concrete.

Example with a genuine extra horizon obstruction: S=R_+^2, h=(xy+1)(x−y)², d=4. Z is the nonnegative diagonal, but {h_4=0} in S∞ also contains both coordinate axes. Set r=(1+x+y)^3(1+x−y). On Z it is (1+2x)^3>0, but r_[4](0,1)=−1. Therefore r is not in the closure. The infinity evaluation at (0,1) explicitly separates it.

## Approach 3: strict versus weak boundary behavior

Counterexample to printed Theorem 1: for that same h and d=4, let p=1+x−y. With t=y−x,

p+h = 1−t+(xy+1)t² = (t−1/2)²+3/4+xy t² ≥ 3/4 on R_+².

Hence p=(p+h)−h belongs to the unclosed cone sum, while its actual leading form x−y is −1 at (0,1), where h_4=0. The corrected component p_[4] is zero, as required by (C).

Closure cannot generally be omitted. Take S=R_+², h=x², d=2, p=1−xy. On Z={x=0}, p=1>0. The infinity condition holds because p_[2]=−xy vanishes on the y-axis. However p∉P_2(S)+x²R_0[x]: for every constant M, 1−xy+M x² becomes negative at x=1 and sufficiently large y. Yet p+ε(1+x+y)² does belong to that sum. Explicitly, adding Mx² with M≥1/(4ε) makes the quadratic part εy²+(2ε−1)xy+(ε+M)x² nonnegative, while the constant and linear terms are positive. (Choosing the larger simple bound suffices.)

A sufficient condition for exact membership is strict positivity of F on C∩{H=0}; the same compact penalty proof works with ε=0. This means both strict positivity at finite zeros and strict degree-d positivity at all nonzero horizon zeros. It is sufficient, not necessary. Exact membership may hold without strict horizon positivity, as the printed-theorem counterexample demonstrates. Mere strict positivity on the finite zero set is insufficient, as p=1−xy shows.

## Approach 4: dual cone and exact separating functionals

Work in homogeneous degree-d forms, or their restrictions to C. The dual of nonnegative forms on C is the conic hull of point evaluations ev_z, z∈C. This conic hull is closed: evaluation of L^d equals 1 at every z, so a convergent conic combination has bounded total mass; the compact convex hull of the evaluations then supplies the limit. Finite-dimensional separation proves the dual identification. Restriction kernels cause no difficulty: functionals in the dual annihilate them.

Let I=H·(homogeneous forms of degree d−m). The dual of the closed sum is P_d(C)^*∩I^⊥. Any element has a finite positive combination of evaluations. Because H L^(d−m) belongs to I and is nonnegative on C, annihilating it forces every positively weighted support point to satisfy H=0. Conversely every evaluation on C∩{H=0} annihilates I. Thus the dual is exactly the conic hull of those zero-set evaluations. Taking the bipolar proves (C) independently of the compact-penalty argument.

At infinity these functionals test p_[d], not the actual highest nonzero component. This explains the source defect at the linear-algebra level: the map p↦p_[d](v) is linear and continuous on the fixed-degree space, while p↦tilde p(v) generally is neither.

## Approach 5: later lifting literature and limits

Primary sources inspected locally: Kuryatnikova–Vera–Zuluaga, arXiv:1909.06689v1 (2019), and v5 (March 2024), https://arxiv.org/pdf/1909.06689v1 and https://arxiv.org/pdf/1909.06689v5. The 2024 title is “Reducing nonnegativity over general semialgebraic sets to nonnegativity over simple sets.” Definition 2 requires positivity on the finite feasible set and actual leading-form positivity on the nonzero set cut out by the leading constraint polynomials. Theorem 2 provides a copositive lifting with a prescribed positive multiplier and degree bound, under that strong positivity hypothesis. This is a different framework from coefficient closure at one fixed degree.

For the elementary set S=R_+ defined by g(x)=x, the polynomial p=1+x has an explicit lifting with the degree-normalizing multiplier: (1+x)p=F(x,x), where F(x,u)=(1+x)²+(u−x)². F is strictly positive on R_+² and its leading quadratic form is positive away from the origin. This concrete application is checked directly and is not an extrapolation to boundary polynomials.

Exact limitation: v5 Example 4 gives the same diagonal h but p=1+x³−(y−x)³. It is positive on the actual diagonal yet has negative leading form on an extra axis. The example rules out its specified family of orthant liftings even if the allowed degree increases. It does not prove that every polynomial failing strong positivity lacks every conceivable certificate. Strong positivity and genericity claims must retain their representation-dependent hypotheses; a boundary polynomial or a nongeneric presentation is not covered automatically. The paper supplies important applications of the 2017 research direction but not a uniquely defined completion of the OWR question.

## Outcome

Established: a fully proved, degree-corrected closure statement under the original pointed-cone and h≥0 hypotheses; an explicit algebraic counterexample to the printed actual-leading-degree necessity; rational perturbation certificates; exact/nonexact boundary examples; a separate dual proof; and a bounded comparison to later liftings. Still open/underspecified: what complete theorem or application would constitute a resolution of the OWR exploratory question. Independent mathematical audit accepted the correction with the explicit scope exclusions recorded in INDEPENDENT_AUDIT.md.

## Additional source edge case: empty finite zero set

The independent auditor identified, and this worker checked, a separate literal issue in printed Theorem 2: S=R_+, h=x²+1, d=2. Then Z is empty, so its horizon is empty under the source convention. But S∞∩{h_2=0}={0}. The stated horizon equality therefore fails although P_2(Z)=R_2=P_2(S)+hR_0. For the latter equality, given p=ax²+bx+c, choose M>|a|+|b|+|c|+1. Then p+M(x²+1)>0 on R_+: the inequality x≤(1+x²)/2 bounds the linear term. This is an origin-only edge case; it does not invalidate corrected closure formula (C), whose infinite test at the origin is automatic for positive d. A geometric equivalence should either assume Z nonempty or compare nonzero horizon directions. No corrected all-set Theorem 2 equivalence is claimed here without its own proof.
