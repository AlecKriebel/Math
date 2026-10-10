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
