# Exceptional-unit prefixes: exact degrees 7, 8 and 9

Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X  
Computer-assisted research note, 2026-10-04. Full source target: **unsolved**.

## 1. Scope and conventions

Let α be a nonzero algebraic integer, K=Q(α), and let E₀(α) be the length of the initial sequence of positive integers j for which αʲ−1 is a unit of O_K. It is zero when α−1 is not a unit. Write e(d)=max E₀(α), with α of exact degree d. The source conjecture is e(d)<d for every d≥7. The nonzero condition is important in degree one: α=0 would have an infinite prefix. It is automatic in the degrees considered here.

**Scoped theorem (exact finite certificate).**

- e(7)=5;
- e(8)=7;
- e(9)=6.

Additionally, if α is a root of unity of any degree d, E₀(α)<d.

These assertions do not resolve the conjecture in all degrees. No historical-priority claim is made. The low-degree theorem is certified by the finite enumeration justified below; `verify.py` uses only Python's standard library and exact integer/rational arithmetic. The mathematical completeness argument has no bound on the coefficients of a minimal polynomial.

For a monic integer polynomial f put

A_n(f)=Res(Φ_n,f),   B_n(f)=Res(xⁿ−1,f).

This order of resultant arguments is deliberate. If f has degree d then Res(f,Φ_n)=(-1)^(d φ(n)) A_n(f); only absolute values are needed. For n≥3, conjugate pairing gives A_n(f)≥0 and hence |A_n(f)|=1 is equivalent to A_n(f)=1. For n=1,2 the values are f(1), f(-1).

If f is the minimal polynomial of α, the norm criterion for an algebraic integer to be a unit and xⁿ−1=∏_{m|n}Φ_m imply

E₀(α)≥N ⇔ |A_1(f)|=⋯=|A_N(f)|=1.

Indeed B_n=∏_{m|n} A_m, up to the irrelevant norm-order sign. The reverse implication follows by multiplication, and the forward implication inducts on n. This is an equivalence for the full ring of integers, not an assumption that Z[α]=O_K. Norm ±1 implies an integral inverse by the characteristic polynomial.

## 2. A finite residue classification

Set S={1,2,3,4,6}, and

P=∏_{m∈S}Φ_m=x⁸+x⁶−x²−1.

Suppose |A_m(f)|=1 for every m∈S. The remainder of f at each modulus must belong to these complete lists:

- Φ₁=x−1: ±1;
- Φ₂=x+1: ±1;
- Φ₃=x²+x+1: ±1, ±x, ±(x+1);
- Φ₄=x²+1: ±1, ±x;
- Φ₆=x²−x+1: ±1, ±x, ±(x−1).

To see completeness without a unit-group theorem, write a quadratic remainder ax+b. Its respective norm is a²−ab+b², a²+b², or a²+ab+b². Setting the norm equal to 1 gives exactly the displayed finite sets: completing the square bounds |a| and |b| by 1, and direct substitution finishes. At the linear moduli the assertion is immediate.

The five moduli are pairwise coprime over Q. Their degrees sum to 8, so the Chinese remainder theorem gives a unique rational polynomial r of degree <8 for each of the 2·2·6·4·6=576 residue tuples. Only 24 have integral coefficients. An exact enumeration, fully specified in `verify.py`, proves that they are precisely

R={ ±(xʲ mod P): 0≤j≤11 }.

Here the twelve positive representatives are

1, x, x², x³, x⁴, x⁵, x⁶, x⁷,
1+x²−x⁶,
x+x³−x⁷,
−1+x⁴+x⁶,
−x+x⁵+x⁷.

These and their negatives are distinct. This is not an application of CRT over Z: the polynomials are not necessarily comaximal in Z[x]. The rational CRT is followed by an explicit coefficient-integrality test.

### Exact enumeration certificate

The verifier constructs the 8×8 matrix whose j-th column consists of the coefficients of xʲ modulo the five moduli. It inverts that matrix by rational Gaussian elimination. For every one of the 576 choices, it solves for r, tests denominator 1 for all coefficients, independently rechecks the prescribed residues, and asserts that the output set is the displayed 24-element set. The matrix is independent of f and has no numerical or search tolerance. This finite calculation is the only enumeration needed for the residue lemma.

As P is monic, division of any f∈Z[x] by P gives an integral quotient and remainder. Consequently every admissible f, without a height bound, is uniquely Pq+r with q∈Z[x] and r∈R.

## 3. Degree seven

If α has degree seven and E₀(α)≥6, its monic minimal polynomial must itself be one of the r∈R of degree seven and leading coefficient 1. There are exactly three:

x⁷,   x⁷+x⁵−x,   x⁷−x³−x.

All have zero constant term and hence a factor x. None is an irreducible polynomial of degree seven. Thus e(7)≤5.

For the reverse inequality use

f₇=x⁷+x⁶+x⁵+x⁴−x²−x−1.

The exact values (A₁,…,A₆) are (1,−1,1,1,1,7). The verifier proves f₇ irreducible modulo 2 by the finite-field Frobenius criterion, so it is irreducible over Q. A root therefore has degree seven and E₀=5.

## 4. Degree eight

Every monic admissible f of degree eight is P+r with r∈R. Testing A₅=1 leaves seven polynomials. Testing A₇=1 then leaves exactly

x⁸,
F=x⁸+x⁷+x⁶+x⁵−x²−x−1,
G=x⁸+x⁷+x⁶−x³−x²−x−1.

The first is reducible. For both F and G, A₈=9. Therefore no irreducible polynomial of degree eight can have E₀≥8, so e(8)≤7. The verifier proves F irreducible modulo 2 and checks |A_n(F)|=1 for 1≤n≤7. Hence e(8)=7. The seven-polynomial intermediate list and every resultant are included in `results.json`.

## 5. Degree nine

Every monic admissible f of degree nine is

f(x)=P(x)(x+a)+r(x),   a∈Z, r∈R.

For each r, the condition A₅(f)=1 is a quartic equation Q_r(a)=0. Its leading coefficient is A₅(P)=5, so it is never the zero polynomial. The degree bound follows immediately by expressing A₅ as the determinant of a 4×4 multiplication matrix whose entries are affine in a.

The coefficients of every Q_r and every integer root are provided in `results.json`. The verifier recovers Q_r from its five exact values at 0,1,2,3,4 using rational interpolation, and tests four further integer arguments as implementation controls. It finds every integer root using the rational-root theorem: after removing any factor a, an integer root must divide the nonzero constant coefficient. Thus this is an exhaustive calculation over all a∈Z, not a bounded search.

Across all 24 r there are fifteen pairs (r,a) satisfying A₅=1. Exactly three also satisfy A₇=1:

x⁹,   xF,   xG,

where F,G are the polynomials in Section 4. Each has zero constant term and is reducible. Thus e(9)≤6.

For the lower bound take

f₉=x⁹+x⁸+x⁷+x⁶+x⁵−x³−x²−x−1.

Its (A₁,…,A₇) are (1,−1,1,1,1,1,8). The verifier proves irreducibility modulo 5, giving exact degree nine and E₀=6.

### Irreducibility certificates

For each displayed witness, the verifier checks x^(p^d)=x modulo f in F_p[x] and gcd(f,x^(p^(d/q))−x)=1 for every prime divisor q of d. This is the standard necessary-and-sufficient Frobenius criterion for a monic degree-d polynomial to be irreducible. The choices (d,p) are (7,2), (8,2), and (9,5). Modular polynomial operations are explicitly implemented; no computer-algebra library supplies irreducibility conclusions.

## 6. All roots of unity

Let α be a primitive m-th root, m≥2, and let Q be the largest prime power dividing m. The order of αʲ is h=m/gcd(m,j). For h>1,

|N_{Q(α)/Q}(1−αʲ)|=Φ_h(1)^(φ(m)/φ(h)).

The elementary evaluation is Φ_h(1)=p if h is a power of the prime p, and Φ_h(1)=1 otherwise. It follows by induction from ∏_{t|h,t>1}Φ_t(1)=h. For h=1, the difference is zero. The first exponent j with a prime-power order is

min_{p^a || m} m/p^a=m/Q.

No smaller positive j has such an order, and j=m/Q realizes it. Therefore

E₀(α)=m/Q−1.

If ℓ is the largest prime dividing m, then

m/φ(m)=∏_{p|m}p/(p−1) ≤ ∏_{k=2}^ℓ k/(k−1)=ℓ≤Q.

Consequently E₀(α)≤φ(m)−1=d−1. For α=1 the conclusion E₀=0<1 holds separately. This closes the root-of-unity branch, not the entire problem.

## 7. Why this does not settle all degrees

For d≥10, the quotient q in f=Pq+r is a monic polynomial of degree d−8 with at least two unrestricted integer coefficients. Conditions A₅=1, A₇=1, and later resultants become simultaneous norm equations in those coefficients. The finite-residue lemma still holds, but by itself does not bound q or rule out irreducible solutions. No such all-degree theorem is claimed here. Section 6 eliminates roots of unity, so the remaining target is the non-root-of-unity case in every degree d≥10.

The five-route record in `ROUTES.md` identifies other mechanisms examined and their exact limitations. The source's degree-seven result is reproduced and sharpened by this independent certificate; the small-coefficient examples used for lower bounds were already exhibited by Stewart. Novelty of the exact values is not asserted solely from failure to find them in a literature search.
