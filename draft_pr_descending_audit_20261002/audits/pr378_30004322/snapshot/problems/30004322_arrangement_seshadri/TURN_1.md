# Turn1: an explicit finite test below the volume threshold

First substantive turn, original line-arrangement conjecture unresolved. The following is a concrete reduction using classical adjunction, Cauchy–Schwarz and fat-point linear algebra. It is not a historical novelty claim or a replacement for the known workshop linear-programming results.

## 1. Setup and the obstruction degree

Let Z consist ofr≥2 distinct complex projective points, and letk≥2 be the maximum number on any line. Assume

    r<k².

For an integral plane curveC of degreed letm_i=mult_{p_i}C andS=Σm_i. A curve violating the proposed line bound has

    d/S<1/k, hence S≥kd+1.                              (1)

A line cannot violate it by the definition ofk. Blow up the distinct points. The strict transform ofC is integral, and its arithmetic genus is nonnegative. Adjunction on the smooth blowup, with classdH−Σm_iE_i and canonical class−3H+ΣE_i, gives

    Σm_i(m_i−1)≤(d−1)(d−2).                            (2)

This uses no very-general-point assumption and no ordinary-singularity assumption. The arithmetic genus of the strict transform is h¹(O_C')≥0 since an integral proper complex curve has h⁰(O_C')=1. Thus it also applies when some m_i are0 or1. Classical adjunction and blowup intersection formulas, rather than a new genus inequality, are the inputs.

Cauchy–Schwarz now yields

    S²−rS≤r(d²−3d+2).                                  (3)

Set
    A=k²−r>0,
    B=2k−rk+3r,
    C₀=1−3r<0,
    Δ=B²−4AC₀.

Let
    D=max{ ceil(r/(2k)), floor((-B+sqrt(Δ))/(2A)) }.       (4)

This is an explicit nonnegative integer computable with integer arithmetic:
the second floor equals(-B+isqrt(Δ)) div(2A), where isqrt is the floor square root.

**Theorem1.** Every integral curve satisfying(1) has degree at mostD.

**Proof.** Ifd>D, then d≥ceil(r/(2k)) and kd+1≥r/2. The functionx²−rx is nondecreasing forx≥r/2. Inserting(1) into(3) therefore gives

    A d²+B d+C₀≤0.                                     (5)

SinceA>0 andC₀<0, this quadratic has one negative and one positive root. Formula(4) putsd strictly beyond the positive root, contradicting(5). The case of degrees below the monotonicity threshold is already included inD. The use of isqrt is exact because−B and2A are integers. ∎

This is a degree bound for every violating irreducible curve, not a cutoff inferred from finite experiments.

## 2. Terminating exact linear-algebra algorithm

Suppose the point coordinates are given in an effectively presented characteristic-zero subfield ofC with exact arithmetic and decidable equality, for example a number field. No computability claim is made for arbitrary unspecified transcendental complex inputs.

Compute k by testing the finitely many lines through pairs of points. Forr=1 return1. If r≥k², this particular algorithm returns 'outside certified range' without a Seshadri conclusion. Otherwise computeD from(4).

For each integer2≤d≤D enumerate vectors
    m=(m_1,...,m_r)∈{0,...,d}^r
satisfying
    S=Σm_i≥kd+1,
    Σm_i(m_i−1)≤(d−1)(d−2).
For each vector form the exact linear spaceV(d;m) of degree-d homogeneous polynomials vanishing to order at leastm_i atp_i. Choose a nonzero coordinate at each point, dehomogenize in that chart and impose that every Taylor coefficient of total order belowm_i vanish. These are explicit homogeneous linear equations in the binomial(d+2,2) coefficients. Exact row reduction decides whetherV(d;m) contains a nonzero polynomial.

If every such space iszero, returnepsilon=1/k. Otherwise return the minimum of1/k and all ratiosd/S with nonzeroV(d;m).

**Theorem2.** The procedure terminates and returns the exact multipoint Seshadri constant for every supplied point set in the range r<k².

**Proof.** All loops are finite and each test is finite linear algebra. If a nonzero polynomialF lies inV(d;m), its actual multiplicity sumT is at leastS. FactorF into integral components with multiplicity. Components with zero total multiplicity contribute only positive degree. The ratio degree(F)/T is at least the smallest Seshadri ratio of its components meetingZ. Hence

    epsilon(Z)≤d/T≤d/S.                                 (6)

Thus every candidate value is an upper bound for epsilon, even whenF is reducible or nonreduced; an irreducibility oracle is unnecessary.

Conversely, lines supply1/k. If epsilon<1/k, by the infimum definition there exists a violating integral curve. Every such curve has degree≤D by Theorem1; its true vector has entries≤d and satisfies the enumerated genus condition. There are finitely many possible pairs(d,m), so the ratios of all violating curves belong to a finite set. Their infimum is therefore attained by one of them. Its defining polynomial belongs to the correspondingV(d;m), and its exact ratio is included. Together with(6) this proves equality of the algorithm's output with epsilon. If no violating curve exists, the line upper bound is already exact. ∎

For singular sets of line arrangements, this gives a terminating certificate of equality or a genuine violating polynomial whenever r<k² and coordinates are exact. It does not assert that such a certificate always has the affirmative result, or that all arrangements lie in this range. A nonzero test polynomial is an actual witness; feasibility of multiplicity inequalities alone is not.

## 3. Two exact controls and why the arrangement hypothesis matters

For a five-line star arrangement, take affine lines y=t x+t² fort=0,...,4. Their ten pair intersections are (−s−t,−st), s<t. Exact collinearity givesr=10,k=4 andD=2. In degreetwo the genus filter permits only0/1 multiplicities. Every nine-point evaluation matrix has full rank6, so no violating conic exists. The algorithm returns1/4. This is a reproduction of the credited star-family result, not a newly solved case.

For an arbitrary point-set control, take seven parabola points(t,t²),t=0,...,6, andq=(1/2,1/2). There are eight points andk=3: a line meets the parabola in at mosttwo points, andq lies on the secant through t=0,1. Formula(4) givesD=2. The conic y=x² contains exactlyseven points, yielding2/7<1/3. The degree-two linear systems show no conic through all eight; hence the algorithm gives the exact value2/7. This is a counterexample to extending the line-computed assertion to **arbitrary** finite point sets, not to the source arrangement conjecture. We make no claim that this set is the full singular locus of a line arrangement.

## 4. Remaining gap

The general source assertion is not resolved. In particular, no universal r<k² theorem for arrangement singular sets is assumed here. Even within that range the finite algorithm may be expensive; it is a termination result with explicit matrices, not a polynomial-time claim. The boundary r=k², and any arrangement withr>k², are outside this certificate. The latter would already conflict with1/k by the classical volume boundepsilon≤1/sqrt(r), but no such arrangement is constructed here.

The next turn will seek stronger structural certificates for genuine arrangements rather than extrapolating either control to the original conjecture.
