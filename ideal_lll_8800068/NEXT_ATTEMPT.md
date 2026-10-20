# Next construction attempt: exact nonshortest controls and the missing flag inequality

Date: 2026-10-20. Scope remains the cyclic family L(n,m)=m Z^n+Z u, u=(1,...,1), and exact classical LLL. These results do not resolve the general coefficient-ideal sharp-rate question.

## 1. Exact shortest-vector formula, without the earlier sufficient hypothesis

For every positive integer m and n,

    lambda_1(L(n,m)) = min(m,sqrt(n)).

Indeed, a vector with common residue zero modulo m has norm at least m unless it is zero. With nonzero common residue, every coordinate is a nonzero integer, so the norm is at least sqrt(n). Both m e_1 and u belong to L.

When m>sqrt(n) and m>=3, the only shortest vectors are +/-u: equality in the coordinatewise estimate requires all coordinates in {+1,-1}, and these signs cannot be mixed in one residue class modulo m>=3. When m=2 and m>sqrt(n), mixed-sign vectors are also shortest; specifically the exceptional n=2,3 instances have a full-dimensional shortest-vector span. This distinction matters for the earlier orbit-rank obstruction.

The earlier assumption m>sqrt(2n) was sufficient but unnecessary for the exact shortest norm. Its uses in CYCLIC.md and CONSTRUCTION_ATTEMPT.md remain correct as stated. The large-modulus proof there applies unchanged; the new formula expands the low-modulus regime that can be investigated correctly.

## 2. Smallest-dimensional nonshortest-first countercontrol

For n=3,m=2, take rows

    (2,0,0), (1,1,1), (-1,1,-1).

The determinant has absolute value 4=m^(n-1), and every row has congruent coordinates modulo 2, so this is a basis of L(3,2). Gram-Schmidt squared lengths are (4,2,2), with mu_21=1/2, mu_31=-1/2, mu_32=0. The first Lovasz inequality is equality: 2+(1/2)^2*4=3=(3/4)*4; the second is 2>=3/2. Thus the basis is reduced but ||b_1||/lambda_1=2/sqrt(3)>1.

This is the smallest possible dimension in this family. Dimension 1 is immediate. In dimension 2, m=1 gives Z^2 and m=2 gives a rotated square lattice; their Hermite bounds give first squared norm at most sqrt(2) and 2sqrt(2), respectively, forcing shortestness by their norm spectra. For m>=3, lambda_1^2=2; any nonconstant vector has squared norm at least ceil(m^2/2)>=5, whereas the generic LLL SVP bound permits at most 2lambda_1^2=4. A nonshortest constant vector cannot be a primitive basis vector. Hence no dimension-2 counterexample exists.

The n=3,m=2 control has multiple independent shortest vectors and is NOT a genuinely rank-one-shortest-set example.

## 3. An unbounded-dimensional exact rank-one-shortest-set family

Let m>=3 and choose any integer

    ceil(3m^2/4) <= n <= m^2-1.

Take the basis

    b_1=m e_1,  b_2=u,  b_j=m e_(j-1)  (3<=j<=n).

It is a basis of L(n,m), by row permutation of its standard basis, with determinant magnitude m^(n-1). Its Gram-Schmidt data are

    D_1=m^2,
    D_2=n-1,
    D_j=m^2 (n-j+1)/(n-j+2),             3<=j<=n;
    mu_21=1/m;
    mu_i1=0,                            i>=3;
    mu_i2=m/(n-1),                      i>=3;
    mu_ij=-1/(n-j+1),                   i>j>=3.

All size-reduction coefficients have magnitude at most 1/2. For mu_i2 this follows from n-1>=2m; the stated integer parameter interval implies this, including m=3,n>=7. The first Lovasz inequality is exactly n>=(3/4)m^2. At the next boundary,

    D_3+mu_32^2 D_2 = m^2 >= (3/4)(n-1).

At each remaining boundary j>=4,

    D_j+mu_(j,j-1)^2 D_(j-1)=D_(j-1)>=(3/4)D_(j-1).

Thus the basis is reduced. Since m>sqrt(n) and m>=3, its only shortest vectors are +/-u. Nevertheless

    ||b_1||/lambda_1 = m/sqrt(n) > 1.

For every even m>=4, choosing n=3m^2/4 gives the exact ratio sqrt(4/3). In particular, the family has growing dimension, a genuinely rank-one shortest-vector span, and nonshortest reduced first vectors, but only a CONSTANT approximation loss. It does not approach the desired exponential rate.

Reproduction:

    python computation/verify_countercontrols.py

The independent exact Fraction-based audit records membership, determinants, all size-reduction inequalities, all Lovasz inequalities, and Gram-Schmidt squared lengths. Machine-readable bases/results are in computation/countercontrol_results.json. Besides the n=3,m=2 example, checked instances are (n,m)=(7,3),(12,4),(19,5),(27,6), with ratio squared respectively 9/7,4/3,25/19,4/3. These are exact verified controls rather than stochastic discoveries or numerical near-misses.

## 4. Why delaying u behind coordinate axes cannot amplify the loss

Consider the restricted ansatz whose first k-1 rows are distinct coordinate vectors m e_i and whose kth row is u, for k>=2. Immediately before inserting u, D_(k-1)=m^2, while D_k=n-k+1 and mu_(k,k-1)=1/m. The kth Lovasz inequality necessarily requires

    n-k+2 >= (3/4)m^2.

Hence m^2/n <= (4/3)(n-k+2)/n <=4/3. As long as this prefix is preserved, no choice of suffix can turn it into an exponentially bad reduced basis. In particular the entire coordinate-prefix ansatz is impossible in the earlier strong-gap region m>sqrt(2n). This is a structural limitation of the construction, not a theorem about all bases of L(n,m).

## 5. Precisely what remains unproved

The conjecture that every reduced basis in this family is shortest-first is false, even with only two shortest vectors. Conversely, the examples do not disprove a constant or polynomial approximation bound for ALL reduced bases of this particular family.

The large-modulus theorem controls m, not the size of the integer coefficient vector z in a primitive first row b_1=m z+a u. Its prefix-minor divisibility estimate is one-sided: prefix covolumes are at least m^(k-1), and LLL bounds them from above using the pivot of u. This bounds the modulus but gives no polynomial bound on ||z|| or ||b_1||/sqrt(n) throughout the remaining modulus window. A genuine no-go proof would need an additional constraint on arbitrary unimodular flags, not merely the coordinate-prefix flag. A sharp construction would instead need such a noncoordinate flag to spread the short relation across many positions while meeting all exact size-reduction and Lovasz conditions.

No such inequality or sharp-rate construction is proved in this attempt. The concrete advances are the exact shortest formula, smallest-dimensional countercontrol, the unbounded-dimensional constant-loss reduced family, and the proved constant-factor limitation of the coordinate-prefix ansatz.
