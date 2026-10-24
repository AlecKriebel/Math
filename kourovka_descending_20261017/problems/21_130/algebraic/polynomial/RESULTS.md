# Single-cycle polynomial probe for Kourovka 21.130

Opened 2026-10-24T19:31:10Z. Latest checkpoint 2026-10-24T19:36:02Z.
Best-guess completion toward the full problem: **8%**. The full claim remains open in this effort. These are self-contained algebraic partial certificates and method obstructions; no novelty claim is made.

The small-n characteristic restrictions from the original polynomial below are superseded by the reduced polynomial in `SLACK_RESULTS.md`, which covers n=3,...,9 in every odd characteristic. The diagnostic obstructions below remain valid for this original polynomial.

## Exact target and status

Given an n-element subset A of a finite abelian group of odd order, n>2, find a cyclic enumeration whose n adjacent sums are distinct. A cycle cover with several components is insufficient. The direct polynomial below enforces exactly one cycle, but its coefficient certificate is unavailable for all even n and in some odd characteristics. No result here applies automatically to abelian groups of exponent p^k with k>1.

## 1. A polynomial that really enforces one cycle

Put N=n(n−1)/2 and

    V(y_0,...,y_(n−1)) = ∏_(0≤i<j<n) (y_j−y_i),
    s_i = x_i+x_(i+1 mod n),
    P_n(x) = V(x_0,...,x_(n−1)) V(s_0,...,s_(n−1)),
    C_n = [x_0^(n−1) ... x_(n−1)^(n−1)] P_n.

The degree is n(n−1). For a finite field F and A⊂F with |A|=n, any nonzero evaluation of P_n on A^n gives the desired cyclic enumeration: the first Vandermonde enforces distinct vertices, so every element of A appears once, and the second enforces distinct sums of consecutive vertices on that fixed n-cycle.

**Grid coefficient lemma, with proof.** Write φ(t)=∏_(a∈A)(t−a). For every polynomial P of total degree at most n(n−1),

    [∏_i x_i^(n−1)]P = ∑_(a_0,...,a_(n−1)∈A) P(a_0,...,a_(n−1)) / ∏_i φ′(a_i).

Indeed the univariate functional L(f)=∑_(a∈A)f(a)/φ′(a) has L(t^k)=0 for k<n−1 and L(t^(n−1))=1 by Lagrange interpolation. Apply its n-fold tensor product to each monomial of P: every monomial other than the target has at least one exponent below n−1, since its total degree is no greater than n(n−1). The target contributes 1. All denominators are nonzero because A is a set.

Consequently, if C_n is nonzero in F, some evaluation of P_n is nonzero. This proves the original conclusion for every n-element subset of every elementary abelian p-group whenever p∤C_n: identify (Z/pZ)^d additively with the field F_(p^d). This field representation is not available for arbitrary odd-order abelian groups.

## 2. Reflection forces C_n=0 for every even n

Apply the variable permutation ρ:x_i↦x_(-i mod n). Its permutation of vertices is i↦−i. Its permutation of edge sums is i↦−i−1, the composition of the vertex permutation with a cyclic shift. The product of the signs of these two permutations is therefore (−1)^(n−1). Thus

    P_n(ρx) = (−1)^(n−1) P_n(x).

The target monomial ∏x_i^(n−1) is fixed by every variable permutation. Over the integers, C_n=(−1)^(n−1)C_n; for even n this gives C_n=0. The integer zero remains zero in every characteristic, including characteristic 2. This blocks this particular central-coefficient proof for every even n; it is not a counterexample to the combinatorial claim.

## 3. Exact odd-n coefficients and characteristic obstructions

The standard-library script `verify.py` computes the following integers. For n=3,4,5,6,7 it also independently multiplies all factors of P_n, discarding monomials with an exponent greater than n−1 (which can never contribute to the target).

| n | C_n | Prime factorization | Elementary odd characteristics certified |
|---:|---:|---|---|
| 3 | 6 | 2·3 | p≠3; p=3 follows trivially for triangles |
| 5 | 980 | 2²·5·7² | every odd p except 5 and 7 |
| 7 | 2,292,864 | 2⁷·3·7·853 | every odd p except 3,7,853 |
| 9 | 87,215,071,680 | 2⁶·3⁵·5·11·101963 | every odd p except 3,5,11,101963 |

These statements also include p<n when a group of characteristic p has at least n elements. For example, C_5≠0 in characteristic 3, so the lemma covers every five-element subset of every elementary abelian 3-group.

For a reproducible exact computation without expanding P_n, let f(x)=V(s(x)). The alternating polynomial

    Alt(f)(x)=∑_(σ∈S_n) sgn(σ) f(x_(σ(0)),...,x_(σ(n−1)))

has degree N. Every alternating polynomial of degree N over Z is an integer multiple κ_nV(x): it vanishes when any two variables agree, hence is divisible by every x_j−x_i, and the product already has degree N. The remaining factor is an integer constant because V has a coefficient ±1. Also

    [∏x_i^(n−1)] V(x)^2 = (−1)^N n!.

This follows directly from the determinant expansion of V: complementary exponent permutations contribute the same sign (−1)^N and there are n! of them. Taking the target coefficient in V(x)Alt(f)(x) gives

    n! C_n = κ_n (−1)^N n!,   hence C_n=(−1)^N κ_n.

Evaluate the polynomial identity at x=(0,1,...,n−1), where V(x)=∏_(k=0)^(n−1)k!, to obtain the exact integer formula used by the script:

    C_n = (−1)^N / (∏k!) · ∑_(σ∈S_n) sgn(σ) ∏_(i<j) (s_j(σ)−s_i(σ)),
    s_i(σ)=σ(i)+σ(i+1 mod n).

This integer calculation is performed before reduction modulo p; its denominator is never inverted in a finite field. In particular, the calculation remains valid when p divides ∏k!.

The n=5 coefficient vanishes modulo 7 even though 7>5. Thus merely assuming the field characteristic exceeds n does not save this certificate. This is a method obstruction only: A={0,1,2,3,4}⊂F_7 has the cyclic order (0,1,2,3,4), whose sums are (1,3,5,0,4), all distinct. Likewise the exceptional prime 853 for n=7 rules out a universal argument based solely on C_7 being nonzero in all characteristics greater than n.

## 4. Why a naive exterior-algebra sum cancels

Let e_g be exterior generators indexed by possible group sums. A tempting invariant is

    W_n(A)=∑_(σ∈S_n) e_(aσ(0)+aσ(1)) ∧ e_(aσ(1)+aσ(2)) ∧ ... ∧ e_(aσ(n−1)+aσ(0)).

Repeated colors vanish automatically in each summand. Unfortunately:

* For even n, rotating the rooted cycle by one vertex rotates n exterior factors, with sign (−1)^(n−1)=−1. Each rotation orbit has n elements and contributes zero.
* For odd n≡3 mod4, reversal of a cycle reverses the order of its n factors with sign (−1)^(n(n−1)/2)=−1, so reversal pairs cancel.

Thus W_n(A)=0 for every A in both cases, including n=3, where every triangle always works. For n≡1 mod4 these particular cancellations do not force zero, but no nonvanishing argument is established. Distinguishing a representative root/orientation removes these symmetry cancellations at the price of losing the corresponding invariant symmetry; it does not prove existence.

## 5. Determinants encode covers unless connectivity is extracted

Use commuting color variables y_g and the symmetric matrix M with M_ij=y_(a_i+a_j) for i≠j and M_ii=0. In a squarefree color monomial, a determinant term cannot contain a 2-cycle because it would repeat its edge color. It can still contain several cycles of length at least 3. A cover with c unoriented components contributes sign (−1)^(n−c), orientation multiplicity 2^c, and its color product. So squarefree terms of det M do not certify a Hamiltonian cycle; covers with different numbers of components may also cancel.

For n>2 there is an exact connected replacement over Q. Add commuting vertex variables z_i satisfying z_i²=0, and set B_ij=z_i M_ij. Then

    [z_0...z_(n−1)] tr(B^n)
      = 2n ∑_(unoriented Hamiltonian cycles H) ∏_(edges {i,j}∈H) y_(a_i+a_j).

Every surviving closed walk uses each vertex once, hence is a single Hamiltonian cycle. Each unoriented cycle has n roots and two orientations. If color variables additionally satisfy y_g²=0, repeated sums vanish, and the result is nonzero if and only if the desired cycle exists. All surviving coefficients are positive rational integers, so there is no cancellation. Equivalently, [t^n](−log det(I−tB))=tr(B^n)/n.

This is an exact reformulation, not progress on nonvanishing. Showing that the squarefree connected coefficient is nonzero is precisely the original central difficulty. No route that merely replaces this with a nonvanishing assertion is promoted as a proof.

## Strongest verified result and exact gap

The finite-field coefficient lemma gives the stated n=5,7,9 partial classes, with exact integer certificates. Reflection and exterior symmetries rigorously block two natural uniform invariants. The remaining full-problem gap is both (i) non-elementary odd groups, which have no additive field embedding, and (ii) all even n and the listed exceptional odd characteristics for the specific CN certificate. No general nonvanishing mechanism for a connected rainbow-cycle invariant has been found.
