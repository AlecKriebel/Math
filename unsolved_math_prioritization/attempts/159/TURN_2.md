# Turn 2: support certificates and residue-class trinomial exclusions

Original conjecture unresolved. This turn investigates a combinatorial support route rather than arithmetic conjugates. The conclusions below are exact in arbitrary degree, but their hypotheses are restrictive. Classical coefficient forcing is credited to the existing unfair-polynomial literature; no novelty is claimed.

## 1. A support-only obstruction

Use Turn 1's normalization A(0)=B(0)=1, both monic, with all coefficients in [0,1]. Let U and V be their exact positive-coefficient supports. For s∈U+V, let E_s={(u,v)∈U×V:u+v=s}. The convolution equation is

sum_((u,v)∈E_s) a_u b_v = 1.

If E_s has one element, both coefficients at its endpoints must be 1: a_u b_v=1 with 0<a_u,b_v≤1. Let U_1,V_1 denote the sets of vertices incident to any such uniquely represented sum. These are forced-unit coefficient indices, computable from supports alone.

**Unit-collision certificate.** If some (u,v)∈U_1×V_1 has a sum s with at least two representations, no admissible factorization with exact supports U,V exists. The term a_u b_v is already 1; every other represented term is strictly positive, making c_s>1.

In particular, if every vertex of U and V is incident to a unique-sum edge, any admissible factorization has all its positive coefficients equal to 1. Then every sum must be uniquely represented. Conversely, if all sums are uniquely represented, every pair equation forces all positive coefficients to be 1, and the Boolean support polynomials give a valid factorization. These claims do not assume the conjecture.

The first and last pairs are always unique, so support minima/maxima are included. A certificate may use non-endpoint unique pairs too. An absent certificate is not evidence of an admissible factorization: the unresolved positive real equations remain coupled across all sums.

## 2. An unbounded three-point family

**Proposition.** Fix integers d≥1 and r≥2. If 0<a<1, there is no nonzero polynomial Q with nonnegative real coefficients such that

(1+a x^d+x^(rd)) Q(x)

has all coefficients in {0,1}.

Write Q(x)=sum_(j=0)^(d−1) x^j Q_j(x^d). The product's residue classes modulo d do not interact, so for any nonzero Q_j, (1+a z+z^r)Q_j(z) has Boolean coefficients. Remove its initial zero powers. Its resulting constant coefficient forces the new Q_j to have q_0=1. All q_k remain nonnegative, with q_k=0 outside their finite range.

For 1≤k<r the coefficient equation reads c_k=q_k+a q_(k−1). If q_(k−1)∈(0,1], then 0<a q_(k−1)<1. Thus c_k cannot be zero and must be 1, so

q_k=1−a q_(k−1)∈(0,1).

Starting from q_0=1, this proves q_(r−1)>0. Equivalently the forced values are the explicit alternating sums q_k=(1−(−a)^(k+1))/(1+a), all positive for 0<a<1. At degree r,

c_r=q_r+a q_(r−1)+q_0>1,

a contradiction. Finiteness is respected by extending q with zero coefficients; if Q_j ends earlier, the contradiction simply occurs sooner.

Reversal preserves the nonnegative-factor/Boolean-product hypotheses. Therefore the same exclusion holds for 1+a x^k+x^m whenever either k divides m or m−k divides m, with 0<k<m. In the probability model, any three-point summand with those normalized positions must be uniform whenever its independent sum is uniform; after forcing a∈{0,1}, Turn 1's rational-factor result forces the other summand to be uniform too.

The boundary values a=0 and a=1 are not excluded: the factor itself is then Boolean and Q=1 supplies a valid example. The claim makes no assertion about trinomials with neither divisibility condition. In particular it is not a new proof of the difficult 1+a x²+x^k family for odd k.

## 3. Failed extension and exact remaining gap

The support certificate supplies a finite, checkable contradiction when a forced-unit pair collides with another positive pair. It does not imply that every non-direct support pair has such a collision. The residue proof works because below the first terminal unit coefficient the recurrence has exactly one delayed term and stays strictly positive. Several positive short coefficients can make a cofactor coefficient vanish, so this sign argument cannot be transferred without a new estimate.

The checker exhausts a declared bounded collection of exact support pairs, reports which ones the support criterion leaves unresolved, and tests the residue recurrence with exact rational parameters. Its support scan neither solves the remaining equations nor extends a bounded result to arbitrary degree. The general real-coefficient, arbitrary-support problem remains open after this second turn.
