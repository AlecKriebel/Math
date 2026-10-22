# Turn 3: combine residues, the reduced invariant and arbitrary finite jets

**Result:** an explicit joint-kernel certificate, and an infinite family
showing that adding any finite Taylor jet still does not give an abstract
uniqueness theorem. This is the third substantive attempt. No realization
by knots or counterexample to the original problem is claimed.

Use R, G, u, v, D, r and A_n from Turns 1–2. Let O_(a,b) denote the sum
over distinct theta-symmetry orbit monomials, as defined in Turn 2.

## 1. Explicit simultaneous ambiguity

Set

H=2 O_(2,1)-2 O_(3,1)+O_(4,1)-O_(5,1)+O_(5,2).

**Proposition 3.** H is nonzero, G-invariant, has integral coefficients,
and satisfies

r(H)=0 and A_n(H)=0 for every positive integer n.

It has the compact factorization

H= -D (u+2)(v+2u-3).

Proof. The five orbits are pairwise disjoint, so H is nonzero. One way to
see disjointness is that a canonical representative of an orbit is an
exponent triple (n,m,0) with 0<=2m<=n; our five pairs are distinct in that
region. Equivalently, the coefficient of x^5 y is -1.

All five exponent pairs are primitive, and the group acts unimodularly.
Hence all 54 monomials in H have primitive exponent pairs. The first
orbit has six terms and the others twelve, so the coefficient sum is
2*6-2*12+12-12+12=0. The character-orthogonality formula from Turn 2
gives A_1(H)=0 and A_n(H)=0 for n>1.

For the reduced specialization let C_j=t^j+t^-j. The orbit restrictions
are

r(O_(2,1))=C_2+2C_1,
r(O_(n,m))=2(C_n+C_m+C_(n-m))
for the other four pairs.

Substitution in the displayed linear combination cancels each C_j, proving
r(H)=0. The factorization is an identity in R, obtained by substituting
u=x+y+(xy)^-1+xy+x^-1+y^-1 and
v=(x+y+(xy)^-1)(xy+x^-1+y^-1), then multiplying out. The accompanying
standard-library exact Laurent-arithmetic checker verifies it coefficient
by coefficient, without evaluating roots of unity numerically. ∎

The rational evaluation H(2,3)=-354725/162 is an additional nonzero witness.
It is not used to infer the polynomial identity.

## 2. Common power probes do not repair the loss

For any positive integer p, put H_p(x,y)=H(x^p,y^p).
Then r(H_p)=0. Each exponent pair in H_p has gcd exactly p. Therefore,
for every n, either n divides p and A_n(H_p) is the coefficient sum 0,
or n does not divide p and A_n(H_p)=0 because no exponent is selected.

The supports of H_p for distinct p are disjoint, since their gcds differ.
The family {H_p:p>=1} is consequently linearly independent. Every H_p is
invariant under G, since common power substitution commutes with the
theta action.

## 3. Every fixed finite logarithmic jet can also be made zero

Let J>=0 be a prescribed total Taylor degree. Put m=floor(J/2), choose
L=m+2 distinct positive integers p_1,...,p_L, and define rational weights

c_j=1 / product_{k != j}(p_j^2-p_k^2).

The elementary interpolation identity

sum_j c_j (p_j^2)^d=0, 0<=d<=L-2,

follows by taking the coefficient of X^(L-1) in the Lagrange interpolation
formula for X^d. Now set

H^[J]=sum_j c_j H_(p_j).

It is nonzero because the summands have disjoint supports and every c_j
is nonzero. Multiplying by a common denominator gives a nonzero integral
polynomial with the same properties.

Write H(e^h,e^k)=sum_{d>=0} h_d(h,k), with h_d homogeneous of total
degree d. Simultaneous inversion implies h_d=0 for odd d. Common power
substitution multiplies h_d by p_j^d. Therefore every Taylor term of
H^[J](e^h,e^k) of total degree at most J vanishes by the interpolation
identity. Its reduced specialization and all A_n still vanish by linearity.

This supplies an explicit all-orders family of finite-jet ambiguities;
no finite computation is being substituted for the proof for arbitrary J.

## 4. Meaning of the failed route

In the unrestricted symmetric Laurent target, the following tests together
do not determine the polynomial:

- its full one-variable reduced specialization;
- every unweighted cyclic root-grid residue;
- any specified finite logarithmic Taylor jet;
- normalization at (1,1), integrality, theta symmetry;
- and common-power versions of the same tests.

There is no claim that H or H^[J] occurs as a difference of two actual
knot invariants. Their degrees grow with J, so this result also does not
contradict a reconstruction theorem that uses a *fixed* genus/degree bound
and sufficiently high-degree information. That bounded problem will be
considered in Turn 5.

The joint-kernel computation rules out a tempting comparison shortcut.
It does not rule out direct geometric comparison, or comparison by a
complete surgery characterization. The next attempt tests the latter.

**Remaining full-target gap:** one needs genuinely complete topological
comparison data, not simply agreement on the above necessary checks.
