# Turn 3: lower-central witnesses and exact p-adic loss of visibility

Completed 2026-10-02 UTC. Original unresolved, 3/5 substantive turns; subjective progress 18%. This direction analyzes explicit commutator words in an index-p subgroup, rather than inferring convergence from finite core computations. It eliminates finite-class nilpotent quotients and quantifies why reduction modulo p^e loses the witnesses.

## 1. Cyclic action on a Schreier block

Fix the basis and index-p subgroup U from Turn1. Write t=x_1, y=x_2 and

    y_j=t^j y t^{-j}, 0<=j<p.

The y_j are part of a free pro-p basis of U. Their classes form a rank-p direct summand M of U_ab. Conjugation by t cyclically permutes these classes: the last goes to t^p y t^{-p}, whose class equals that of y because t^p belongs to U. Identify M with Z_p[C_p], with e_j corresponding to y_j, and let S(e_j)=e_{j+1 mod p}, T=S-1.

Define words w_1=y and w_{n+1}=t w_n t^{-1} w_n^{-1}. Then w_n belongs to the nth lower-central term gamma_n(F), and for every n>=1 its image in M is

    [w_n]_ab,U = T^{n-1} e_0.

The other abelianization coordinates are zero. The statement follows by induction: in the abelianization of U, conjugation applies S and multiplication by w_n^{-1} subtracts the previous vector. For n>=2 the words lie in gamma_n(F)<=U. The formula for n=1 is only the initial basis vector.

## 2. Nonvanishing at every lower-central depth

For every k>=1, T^k e_0 is nonzero in Z_p[C_p]. One elementary argument is to evaluate the polynomial (X-1)^k modulo X^p-1 at a primitive pth root of unity in an algebraic closure of Q_p. Its value is nonzero, so its residue class cannot vanish. The next section gives an integral proof and its exact divisibility, avoiding a dependency on local cyclotomic theory.

Consequently gamma_n(F) is not contained in the closed derived subgroup of U for any n>=2. Turn1 therefore implies:

- No lower-central term gamma_n(F), n>=2, is characteristic in both F and U.
- A common characteristic subgroup K cannot contain gamma_n(F) for any finite n.
- The quotient F/K cannot be nilpotent of any finite class. For a nonclosed K this last statement still follows from the explicit words: a nilpotent quotient would put the appropriate w_n in K, contradicting its nonzero image in U_ab.

We use closed lower-central terms when treating pro-p quotients. The actual words lie in the algebraic terms too, so no closure convention affects the exclusions. The standard closedness of these terms in finitely generated profinite groups is also covered by Nikolov–Segal, Theorem1.4 and its consequence on printed174.

This does not say that excluding all lower-central terms excludes every nontrivial characteristic subgroup. The containment direction matters: a surviving K could contain no entire gamma_n(F).

## 3. Exact coefficient valuation

For v in Z_p[C_p], let v_p(v) be the minimum p-adic valuation of its p coefficients, with v_p(0)=infinity. Then for k>=1,

    v_p(T^k e_0)=floor((k-1)/(p-1)).

**Proof.** Let I be the augmentation ideal, the kernel of the coefficient-sum map. It is T Z_p[C_p] and a free Z_p-module of rank p-1. It is saturated in the ambient module: I intersect p^a Z_p[C_p]=p^a I. Indeed if a coefficient-divisible vector has sum0, dividing its coefficients by p^a still gives sum0.

On I, the norm operator 1+S+...+S^{p-1} vanishes, because it annihilates every T multiple. Expanding S=1+T gives

    T^{p-1}=p B on I,
    B=-(1 + sum_{j=1}^{p-2} (binom(p,j+1)/p) T^j).

All displayed coefficients are integral since p is prime. Modulo p, T is nilpotent on I (already T^p=(S-1)^p=S^p-1=0 modulo p). Thus B modulo p is minus identity plus a nilpotent polynomial with zero constant term, so is invertible. Therefore B is an invertible Z_p-linear operator on I and preserves the property of not lying in pI.

Write k-1=a(p-1)+r with 0<=r<p-1. Since T and B commute,

    T^k e_0 = p^a B^a T^{r+1} e_0.

The vector T^{r+1}e_0 belongs to I and is not divisible by p: its expression (X-1)^{r+1} has degree at most p-1 and leading coefficient1, so there is no wraparound reduction modulo X^p-1. Applying B^a preserves that primitivity in I, and saturation identifies it with coefficient primitivity in the ambient module. This proves the exact valuation formula. QED.

For p=2 the empty sum gives B=-1; the formula becomes v_2(T^k e_0)=k-1, consistent with T acting as -2 on the rank-one augmentation ideal.

## 4. What finite reductions can and cannot detect

The word w_n, n>=2, has zero image in the Schreier abelianization block modulo p^e exactly when

    n >= e(p-1)+2.

Its integral p-adic image is nevertheless nonzero for every finite n. Thus checking only modulo p, or modulo any fixed p^e, eventually makes this entire lower-central sequence invisible. That loss of visibility must not be misreported as membership in U' or as a common characteristic subgroup.

The other standard series also cannot themselves solve the problem. A finite Frattini iterate Phi^a(F), a finite term of the lower exponent-p central series, and a finite Zassenhaus term each contain a nonzero p-power of a primitive element (with the power sufficiently large for the specified term). Turn1 excludes such an element from any common characteristic subgroup for {F,U}. For clarity, the latter statement uses the usual definitions: P_1=F, P_{n+1}=closure(P_n^p[P_n,F]), and D_n=closure(product_{i p^j>=n} gamma_i(F)^{p^j}). We make no analogous claim here about every derived-series term.

## 5. Verification and remaining gap

verify_turn3.py computes the exact integer coefficient vectors of (S-1)^k e_0 for several primes and k<=120, checks the valuation formula and every tested visibility threshold, and verifies the integral norm-operator identity on an explicit augmentation basis. These finite controls supplement the all-prime operator proof.

The common characteristic core could still be a nontrivial infinitely generated subgroup whose quotient has infinite nilpotency class and whose behavior escapes every fixed finite abelianization truncation. No family with a proved trivial common core has been constructed. Original unresolved, 3/5.
