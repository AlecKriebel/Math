# Weighted badly approximable points on affine lines: endpoint partials

Problem 30003235 / OWR-15169-009, queue rank 995. Author investigation, 7 October 2026. The intended general endpoint problem remains **unsolved after five approaches**. This is an extensively AI-assisted, unrefereed research packet; no novelty, priority, independent review, or formal-proof certification is claimed.

## Target and imported theorems

Write ||t|| = dist(t,Z). Let 0<i,j<1, i+j=1, sigma=min(i,j), tau=1/sigma, and a,b be real with a != 0. Put M(q)=max(||qa||,||qb||), and L={(x,ax+b):x in R}. The intended endpoint assertion is

(E) liminf_{q->infinity} q^tau M(q)>0 implies dim_H(L intersect Bad(i,j))=1.

Here Bad(i,j) consists of the points z=(x,y) for which there is a constant c(z)>0 with max(q^i||qx||,q^j||qy||)>=c(z) for every integer q>=1. Constants can depend on the point. Equivalent power-normalized definitions change only the positive constant. The endpoint hypothesis means there are kappa>0 and q0 with M(q)>=kappa q^(-tau) for q>=q0. It is equivalent to a bound for every q>=1: a zero M(q) would make both coefficients rational and force zeros at all multiples, and otherwise finitely many initial positive quantities can be absorbed into kappa.

We use the following credited inputs, not new claims:

* Weighted transference: z is in Bad(i,j) iff there is c(z)>0 such that H(A,B)|Ax+By+C|>=c(z) for every integer triple with (A,B)!=(0,0), where H(A,B)=max(|A|^(1/i),|B|^(1/j)). This is the dual formulation used by An--Beresnevich--Velani (ABV), Remark 4.
* ABV Theorem 1.2 and Remark 3: for a!=0, a positive excess exponent epsilon in the coefficient condition gives a 1/2-winning set after projection to the x-axis. For nonzero rational a, epsilon=0 suffices already. A countable intersection of 1/2-winning sets is 1/2-winning and has dimension one in each nonempty interval.
* The coordinate-fiber theorem of Badziahin--Pollington--Velani and An: the set {t:(t,eta) in Bad(i,j)} is winning, hence thick, when inf_{q>=1} q^(1/j)||q eta||>0. ABV Remark 5 states this horizontal version and credits An. The vertical version exchanges i and j.
* Classical continued-fraction facts: for consecutive convergent denominators q_n,q_(n+1), 1/(q_n+q_(n+1))<||q_n alpha||<1/q_(n+1); and for q_n<=q<q_(n+1), ||q alpha||>=||q_n alpha||. Only n with p_n the nearest integer are used, which includes all denominators here from q_1=2 onward.

References and inspection boundaries are in SOURCE_AUDIT.md. Finite tests in this packet do not establish these imported infinite theorems or certify the proofs below.

## Approach 1: exact-type continued fractions and direct obstruction

The first attempt asks whether the critical coefficient hypothesis is secretly strong enough to imply some positive excess exponent, or whether a borderline slope can itself force an empty intersection.

**Lemma 1 (a genuine critical family).** For each real t>=2 there is an irrational alpha in (1/3,1/2) satisfying

    inf_{q>=1} q^t ||q alpha|| >= 1/4,
    liminf_{q->infinity} q^(t-epsilon)||q alpha|| = 0  for every epsilon>0.

Construction and proof. Take alpha=[0;2,a_2,a_3,...]. Starting with q_0=1,q_1=2, set a_(n+1)=ceil(q_n^(t-1)) and q_(n+1)=a_(n+1)q_n+q_(n-1). This defines an infinite continued fraction. For n>=1,

    q_n^t <= q_(n+1) <= q_n^t+2q_n <= 3q_n^t.

Consequently 1/(4q_n^t)<||q_n alpha||<1/q_n^t. For any q>=2 choose n with q_n<=q<q_(n+1); best approximation gives ||q alpha||>1/(4q_n^t)>=1/(4q^t). For q=1, alpha>1/3 gives the same lower bound. The upper estimate along q_n gives q_n^(t-epsilon)||q_n alpha||<q_n^(-epsilon)->0. This proves all quantified assertions.

Applying Lemma 1 with t=tau to (a,b)=(alpha,0) gives genuine nonzero irrational-slope endpoint instances that satisfy no strict-exponent hypothesis. Thus merely weakening epsilon in the known theorem does not cover all new inputs.

**Scope counterexample, not a counterexample to (E).** The omission of a!=0 in the OWR overview and in the curated statement matters. Set a=0, i=1/3, j=2/3, and let b be Lemma 1's alpha with t=2. Then q^3||qb||>=q/4, and even q^(3-1/2)||qb||>=q^(1/2)/4. Thus the supposedly known positive-epsilon hypothesis holds. But at its convergent denominators q_n, q_n^(1/j)||q_n b||<q_n^(-1/2)->0. The dual forms (A,B,C)=(0,q_n,-p_n) show that no (x,b) is in Bad(1/3,2/3), for any x. The intersection is empty. This diagnoses a source-scope omission; it does not refute the intended nonzero-slope question.

For a nonzero slope, the known necessary condition follows directly from the dual formulation: take B=q, A nearest to -qa, and C nearest to -qb. Then |Ax+B(ax+b)+C|<=(|x|+1)M(q), while H(A,B)<=(1+|a|)^(1/i)q^tau. Membership of even one point forces a positive lower bound on q^tau M(q). This reconstructs ABV's credited necessity argument. It gives no reverse implication.

**Outcome/gap.** The construction separates the endpoint from every strict exponent and gives an explicit horizontal scope failure. For the intended irrational-slope line it gives neither an empty intersection nor a full-dimensional surviving set. The direct obstruction method stops at necessity.

## Approach 2: perturbing the weights and intersecting winning sets

Try to approach the critical weights from weights covered by the existing theorem.

**Proposition 2.** Suppose (E)'s coefficient hypothesis holds at sigma_0>0. For any finite or countable collection of positive weight pairs (i_n,j_n) with i_n+j_n=1 and min(i_n,j_n)<sigma_0 for each n,

    dim_H(L intersect intersection_n Bad(i_n,j_n))=1.

In fact its x-projection is 1/2-winning. No uniform positive separation of min(i_n,j_n) from sigma_0 is required.

Proof. Put tau_0=1/sigma_0 and tau_n=1/min(i_n,j_n)>tau_0. Select epsilon_n=(tau_n-tau_0)/2>0. From M(q)>=kappa q^(-tau_0),

    q^(tau_n-epsilon_n)M(q)>=kappa q^((tau_n-tau_0)/2).

The right side tends to infinity. Apply ABV's strict-exponent theorem individually to every weight pair. Each projected set is 1/2-winning by their Remark 3, with the same winning parameter though its other constants can vary with n. Their countable intersection is 1/2-winning. The graph map x->(x,ax+b) is bi-Lipschitz and transfers dimension one to L. This is a direct corollary of the credited theorem, with a supplied exponent calculation, not a claimed new winning theorem.

**Why the limiting step is unproved.** The constants witnessing Bad(i_n,j_n) may tend to zero; countable-intersection stability does not assert continuity in the weights. A useful scalar diagnostic is u_q=v_q=q^(-1/2)/log(q+1), for integers q>=2. At weights (1/2,1/2) the weighted maximum is 1/log(q+1)->0. At any fixed unequal weights summing to one, it is q^delta/log(q+1), delta=|i-1/2|>0, which tends to infinity and has positive infimum over q>=2. These are numerical error arrays only, not errors of a claimed real vector. They refute a proposed inference based solely on such lower-bound inequalities, without refuting (E).

**Outcome/gap.** Full dimension is obtained simultaneously at all selected nearby noncritical weights. No uniform lower-bound estimate in n was established, so no point at the critical weight is produced by this approach alone.

## Approach 3: a weighted rational-projective reduction

Try to turn an irrational-slope line into a coordinate fiber by interchanging a homogeneous coordinate with the coordinate of larger weight. The rationality and weight restrictions below are essential to the proof.

**Lemma 3a (allowed transformations).** Rational translations preserve Bad(i,j); swapping x and y swaps i and j. If i>=j, the involution

    T(x,y)=(1/x,y/x),  x!=0,

preserves membership in Bad(i,j).

Proof. For translation by (r,s) in Q^2, choose an integer d>=1 with dr,ds integral. An integer dual form A(x-r)+B(y-s)+C multiplied by d becomes a dual form at (x,y), with coefficients dA,dB,dC-dAr-dBs. Its weighted height is at most d^(1/sigma)H(A,B). Thus a positive lower bound transfers with a fixed positive factor. The inverse translation gives equivalence. The coordinate swap is immediate from the definition.

For inversion let z=(x,y) in Bad(i,j), x!=0, and (u,v)=T(z). Fix an integer dual form F=A'u+B'v+C' with (A',B')!=(0,0). Its height H'=max(|A'|^(1/i),|B'|^(1/j)) is at least one. If |F|>=1, H'|F|>=1. Otherwise

    |C'| <= 1+|u||A'|+|v||B'| <= K max(|A'|,|B'|),
    K=1+|u|+|v| >= 1.

The old form is xF=C'x+B'y+A'. If (C',B')!=(0,0), its old height satisfies

    H(C',B') <= K^(1/i) H',

because i>=j entails |B'|^(1/i)<=|B'|^(1/j) for nonzero integer B'. The old dual inequality now gives H'|F|>=c(z)/(|x| K^(1/i)). If instead C'=B'=0, then A'!=0 and H'|F|=|A'|^(1+1/i)/|x|>=1/|x|. Taking the minimum of these positive bounds proves T(z) is bad. Since T is an involution, the reverse implication follows by the identical argument. This is a direct dual-height proof, not an assertion that all projective maps preserve weighted bad approximation.

**Lemma 3b (coefficient reduction at a rational point).** Suppose L contains (r,s) in Q^2, so b=s-ar. For any t>0,

    inf q^t max(||qa||,||qb||)>0  iff  inf q^t||qa||>0.

Choose d with dr,ds integral and let K=max(d,|dr|)>0. Then M(dq)<=K||qa||, proving the nontrivial direction after applying the coefficient lower bound at dq. The other direction follows from M(q)>=||qa||. If a!=0 and inf q^t||qa||>0, the same condition holds for 1/a. Indeed, for large q and p nearest to q/a, p is nonzero and |p|<=C_a q. Hence

    |a| ||q/a|| = |q-pa| >= ||pa|| >= kappa |p|^(-t)
                  >= kappa C_a^(-t) q^(-t).

The finitely many small q have positive distances because a and 1/a are irrational under this hypothesis. Exchanging a and 1/a gives equivalence.

**Proposition 3 (endpoint for rational-point lines).** For all positive weights i+j=1 and all nonzero-slope lines L containing a rational point, the coefficient hypothesis in (E) implies that Bad(i,j) intersect L has dimension one in every nonempty relatively open interval of L.

Proof. Translate the rational point to (0,0), using Lemma 3a. Lemma 3b turns the coefficient hypothesis into inf q^(1/sigma)||qa||>0. If i>=j, sigma=j, and inversion sends (x,ax), x!=0, to (u,a). The fixed coordinate a therefore satisfies the exact horizontal fiber hypothesis of exponent 1/j. By the credited fiber theorem, the allowed u form a thick set. On compact subintervals away from x=0, x->1/x and the graph parametrizations are bi-Lipschitz. Lemma 3a transfers both membership and dimension, proving the conclusion. If i<j, first exchange the two coordinates and their weights. The new line has slope 1/a and its first coordinate now has the larger weight. Lemma 3b supplies the identical Diophantine condition on 1/a, so the preceding argument applies. Every nonempty open interval contains a smaller interval avoiding the rational point; the missing point has no effect on thickness.

**Outcome/gap.** This proves a scoped endpoint result using the known fiber theorem. Together with ABV's already known rational-slope case it covers two different classes of lines. No new-priority claim is made. A line with irrational slope and b outside Q+Qa has no rational point; a rational translation cannot make its intercept zero. The above proof supplies no reduction for such a line. General real translations or shears are not licensed by Lemma 3a, and no unrestricted weighted projective invariance is asserted.

## Approach 4: near-parallel dual-resonance elimination

Try to run a direct interval-deletion construction from the dual inequalities. This section isolates the scale loss at the endpoint, rather than claiming a Cantor construction has been completed.

Fix a compact parameter interval I with |x|<=X on I. For v=(A,B,C) in Z^3 with (A,B)!=(0,0), set

    h=H(A,B), alpha_v=A+aB, beta_v=C+bB,
    D_v(eta)={x in I: |alpha_v x+beta_v|<eta/h}.

For alpha_v!=0 the unrestricted dangerous interval has length 2eta/(h|alpha_v|). Suppose B!=0 and |alpha_v|<=|a||B|/2. Write Q=|B|. Then |a|Q/2<=|A|<=3|a|Q/2, so

    h_- Q^tau <= h <= h_+ Q^tau,
    h_-=min(1,(|a|/2)^(1/i)),
    h_+=max(1,(3|a|/2)^(1/i)).

These constants are positive, because the intended hypothesis requires a!=0.

**Lemma 4.** Assume the endpoint coefficient bound M(Q)>=kappa Q^(-tau) for every positive integer Q, and 0<eta<=kappa h_-/2. If D_v(eta) is nonempty and the near-parallel conditions above hold, then

    |alpha_v| >= kappa Q^(-tau)/(2(X+1)),
    length(D_v(eta)) <= 4(X+1)eta/(kappa h_-).

Proof. Pick x in D_v(eta). Since A,C are integers,

    kappa Q^(-tau) <= M(Q) <= max(|alpha_v|,|beta_v|)
       <= (X+1)|alpha_v|+eta/h.

Using h>=h_-Q^tau and the bound on eta makes the last term at most kappa Q^(-tau)/2. Rearrangement proves the first inequality, and in particular alpha_v!=0. Multiply by the lower bound on h and use the explicit interval length to get the second.

For comparison, under the stronger bound M(Q)>=kappa Q^(-tau+epsilon), the same argument gives

    length(D_v(eta)) <= 4(X+1)eta Q^(-epsilon)/(kappa h_-).

The small-eta assumption is still sufficient since Q>=1. The endpoint estimate lacks this decay factor.

The loss is realized by actual endpoint inputs: take b=0 and the alpha from Lemma 1 with t=tau as slope a. At v_n=(-p_n,q_n,0), |alpha_v|=||q_n a|| is between (1/4)q_n^(-tau) and q_n^(-tau), while h is comparable to q_n^tau. Thus h|alpha_v| stays between two positive constants, and the unrestricted dangerous intervals have length comparable to eta rather than tending to zero. All are centered at x=0. This is not a counterexample to (E); indeed Proposition 3 handles this line. It shows why a deletion argument based on individual shrinking resonances is insufficient, and why grouping resonances by their common location matters.

**Outcome/gap.** We obtain uniform quantitative elimination and an exact endpoint loss, but not a scale-dependent deletion count for general b. Proving that long dangerous intervals can always be grouped into a small number of removable clusters remains a missing step.

## Approach 5: determinant clustering and a Cantor-tree attempt

Try to repair Approach 4 by collecting dangerous forms within one weighted-height window before deleting any intervals.

**Lemma 5 (an elementary weighted simplex bound).** Fix R>=1, H>=R, m=max(i,j), C_a=1+|a|, and eta>0. Let I=[x_0-r,x_0+r]. Consider all integer triples v=(A,B,C) whose weighted heights h satisfy H/R<=h<=H and for which |(A+aB)x+Bb+C|<eta/h at some x in I. If

    r <= H^(-(1+m))/(24 C_a),  eta <= 1/(24R),

all their coefficient vectors span a space of dimension at most two over R.

Proof. We have |A|<=H^i, |B|<=H^j and |A+aB|<=C_a H^m. Therefore at x_0,

    |F_v(x_0)| <= C_a H^m r+eta R/H = E.

For any three triples replace the third column C by F_v(x_0)=A x_0+B(ax_0+b)+C. This column operation leaves the determinant unchanged. Expansion along permutations bounds its absolute value by

    6 H^(i+j) E = 6 C_a H^(1+m)r+6eta R <= 1/2.

The original determinant is an integer, hence zero. Every three vectors are dependent, which proves the rank bound.

If the span has rank two, choose two independent integer vectors and take their cross product (X,Y,Z). Every rational line Ax+By+C=0 from the family contains the rational projective point [X:Y:Z]. When Z!=0 these lines are concurrent at (X/Z,Y/Z); when Z=0 they have a common direction. Rank-one families are scalar multiples of a single form. These are exact algebraic conclusions, obtained without a statistical assumption on the coefficients.

The lemma is an elementary form of the determinant/simplex mechanism underlying classical bad-approximation constructions. It is a supplied proof and an attempted ingredient, not a claim of a new simplex theorem.

**The attempted construction and precise gap.** A prospective Cantor proof would subdivide each surviving interval into R or more comparable children and remove children meeting all new D_v(eta). Lemma 5 can reduce one height window to a pencil of rational lines. It does not bound the length of the union of their intersections with L, nor the number of surviving children. Near-parallel pencils are exactly where Approach 4 loses decay. Furthermore, the natural geometric scale H^(-(1+m)) need not be the individual dangerous-interval scale 1/(h|alpha_v|). No induction proving a positive branching rate, and no Frostman measure of dimension approaching one, has been established. Thus the desired dimension-one conclusion cannot be inferred from this rank bound.

## Final mathematical disposition

The intended statement (E) for arbitrary irrational a!=0 and b outside Q+Qa is unresolved in this packet. We have proved: an exact critical family and the literal horizontal scope failure; a simultaneous noncritical-weight consequence of the known winning theorem; the critical rational-point-line reduction; a quantitative near-parallel estimate; and a weighted determinant rank lemma. The rational-slope endpoint and coordinate-fiber inputs are credited prior results. None of the countercontrols is a counterexample to the intended (E), and no general current-openness or exhaustive-priority certificate is claimed.
