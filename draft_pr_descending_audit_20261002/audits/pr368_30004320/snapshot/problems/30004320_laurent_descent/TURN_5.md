# Author turn 5: reductive isotropy with tame Weyl group; a wild Brauer obstruction

Status: final substantive author turn, 5/5. The original arbitrary-field,
arbitrary-homogeneous-space question remains unresolved. This turn proves
an additional restricted class and exhibits a precise failure of the
proposed full-Puiseux strategy outside it. No sixth author search follows.

Let k have characteristic p>0, K=k((t)), and L be the full Puiseux union
from turn 3. Perfect fields, and all constant torsors, remain credited prior
results. The results below are original exposition of combinations of
standard machinery; historical novelty has not been established.

## 1. Add a maximal torus to the gerbe object

**Theorem.** Let G be a smooth affine k-group and X a smooth homogeneous
G-variety. Suppose its geometric stabilizer H is smooth, its identity
component H^0 is reductive, and

    p does not divide |W(H^0)| · |pi_0(H)|.                (1)

Here W is the geometric Weyl group and pi_0 is the geometric component
group. Then X(K) nonempty implies X(k) nonempty. More precisely, every
x in X(K) is G(L)-equivalent to some x_0 in X(k).

The condition concerns the stabilizer, not the acting group. The acting
group is not required to be reductive or H1-trivial. The theorem includes
connected reductive stabilizers whose Weyl-group order is prime to p.

### Construction and proof

Put C=[X/G]. Define C^Tor to have objects (eta,T), where eta is an object
of C and T is a maximal torus of Aut(eta)^0. Morphisms are isomorphisms
of eta carrying the specified torus to the specified torus. This is an
algebraic gerbe over k. Indeed, locally where C is neutral and a maximal
torus of its stabilizer has been chosen, it is the classifying gerbe of
that torus's normalizer. Maximal tori are conjugate étale-locally, and the
scheme parametrizing them is smooth; these descriptions glue by fppf
descent. This is the scheme-theoretic maximal-torus construction of
Conrad, *Reductive Group Schemes*, Theorem3.2.6, not an assertion about
conjugacy of arbitrary rational tori by rational points.

Over an algebraic closure, the automorphism group of an enhanced object
is N=N_H(T). It is smooth by the multiplicative-type transporter theorem
(Conrad, Proposition2.1.2). Its identity component is T. Furthermore,

    1→W(H^0)→pi_0(N)→pi_0(H)→1                         (2)

is exact. To see surjectivity on the right, any component represented by
h in H sends T to another maximal torus of H^0. Conjugacy by an element
of H^0 adjusts h into N. The kernel is N_{H^0}(T)/T, the Weyl group.
The latter is finite étale, by Conrad Proposition3.2.8. Thus (1) makes
the finite component group in (2) prime to p, and C^Tor satisfies turn 4's
general torus-by-tame-finite gerbe lemma.

Given x in X(K), let xi be its gerbe object. Aut(xi)^0 is a connected
reductive K-group, and it has a geometrically maximal torus defined over
K by Grothendieck's theorem (Conrad TheoremA.1.1). Thus xi lifts to an
enhanced object of C^Tor(K). After passing to L, turn 4's lemma descends
this full enhanced object to k, up to an L-isomorphism. Forgetting the
torus gives a k-object eta of C whose L-base change is isomorphic to xi_L.
Its underlying G-torsor becomes trivial over L. Constant-torsor injectivity
from turn 3 makes it trivial over k. A trivialization supplies x_0 in
X(k); the retained isomorphism supplies the G(L)-orbit relation. This
proves the theorem.

No nonabelian H2 classification or neutrality shortcut is substituted for
the full enhanced-object descent. The prime-to-p finite-component condition
is used exactly at turn 4's rigidification step.

## 2. Why full Puiseux extension is not acyclic for general reductive groups

One might try to drop (1) by declaring that every constant reductive group
has all its L-torsors descended from k. That assertion is false. We now
construct an explicit nonconstant PGL_p-torsor over L.

Take

    k=F_p(a,b),      K=k((t)),

with a,b algebraically independent. Define the cyclic degree-p algebra D
by generators x,y and relations

    x^p−x=a/t,       y^p=b,       y x y^−1=x+1.            (3)

This fixes the cyclic-generator convention; it may be the opposite of
another p-symbol convention. The Artin–Schreier polynomial in (3) is
irreducible over K: a hypothetical root with a pole would have its
p-th-power term of valuation divisible by p, incompatible with the pole
of order1. It defines a cyclic degree-p field, and the usual cyclic algebra
construction gives a central simple algebra of degree p, with basis
x^i y^j for 0≤i,j<p. See Gille–Szamuely, *Central Simple Algebras and
Galois Cohomology*, §2.5, especially Corollary2.5.5; the sign of the chosen
cyclic generator does not affect central simplicity.

We prove that D remains a division algebra over every finite Puiseux stage
and that its class over L cannot come from Br(k).

### A complete order with purely inseparable residue field

Fix any stage K_n=k((s)), t=s^n, and pass further if needed so that p divides
n. Write n=pq with q≥1 and put w=s^q x. The defining relations become

    w^p−s^{q(p−1)}w=a,
    y^p=b,
    y w y^−1=w+s^q.                                     (4)

Let O be the k[[s]]-submodule of D_{K_n} with basis w^i y^j, 0≤i,j<p.
The relations (4) show that it is a subring, containing y^−1=b^−1 y^{p−1}.
It is finite free, hence s-adically complete. Reducing (4) gives

    O/sO = k[w_bar,y_bar]/(w_bar^p−a,y_bar^p−b)
          = k(a^(1/p),b^(1/p)).                          (5)

This is a field of degree p² over k, by p-independence of a and b. In
particular no nilpotent or smaller residue quotient has been substituted.

Every element of O with nonzero reduction is invertible: lift an inverse
modulo s and use the convergent geometric series for 1+s z on both sides.
Every nonzero element of D_{K_n} can be written s^m u with u in O having
nonzero reduction, by taking the least valuation of its basis coefficients.
It is therefore invertible. Thus D_{K_n} is a division algebra. The least-
coefficient valuation is multiplicative, because the residue ring (5) is a
field. Its value group is Z and its residue division ring is the purely
inseparable commutative field (5).

This argument also proves nonsplitting over stages whose n is not divisible
by p: a split algebra at such a stage would remain split after a further
p-power root of the parameter, contrary to the preceding proof. Consequently
D_L is a division algebra too, since a splitting over the union would be
defined at a finite stage.

### The division algebra is not a constant one

For a central division algebra A_0 over k, the Laurent algebra A_0((s))
is a division algebra, by its leading-coefficient valuation. Its residue
ring is A_0. Therefore the index of a constant central simple algebra is
unchanged under a Laurent extension.

Suppose the Brauer class of D_L came from k. Equality is detected at a
finite stage; using the preceding index fact, the division representative
A_0 over k would have degree p. After a further stage with p dividing n,
we would have an isomorphism

    D_{K_n} ≅ A_0((s))                                  (6)

of central division K_n-algebras.

The valuations just used are intrinsic to the algebra in this situation.
For an element z=s^m u of either algebra, left multiplication on its
finite free order has determinant of valuation m p²: a unit u acts
invertibly modulo s. The general reduced-norm identity

    det(left multiplication by z)=Nrd(z)^p

therefore gives v(z)=v_{K_n}(Nrd(z))/p. An algebra isomorphism preserves
the reduced norm and hence the valuation and residue ring. The residue
ring on the left of (6) is the commutative field in (5); the one on the
right is A_0, a noncommutative central division algebra of degree p>1.
They cannot be isomorphic. This contradicts (6).

Thus

    [D_L] is not in the image of Br(k)→Br(L),
    H1(k,PGL_p)→H1(L,PGL_p) is not surjective.             (7)

For completeness, the norm identity used above can be checked after a
splitting field: left multiplication on Mat_p is the direct sum of p
copies of the defining p-dimensional matrix action. Hence its determinant
is the p-th power of the matrix determinant, which is the reduced norm.
This also works in characteristic p. The residue argument did not assume
perfection or invoke a defectless-division-algebra theorem.

## 3. Interpretation of the obstruction and final gap

The Weyl group of PGL_p is S_p, whose order is divisible by p. Thus (7)
occurs exactly outside the prime-to-p Weyl hypothesis of §1 and proves
that the blanket reductive object-surjectivity shortcut cannot replace it.
It does not prove that the Weyl hypothesis is necessary for the original
homogeneous-space implication.

Most importantly, D is an algebra defined over k((t)), not an algebra over
k that splits over k((t)). It gives an auxiliary nonconstant torsor and is
NOT a counterexample to the original descent problem. The constant-group
torsor theorem remains valid and was used throughout the packet.

After five genuine turns, the remaining gap includes arbitrary wild
noncommutative stabilizers, reductive stabilizers with p dividing the relevant
Weyl/component order, general unipotent isotropy, and any broader non-smooth
acting-group scope of the original formulation not covered by the explicitly
smooth partial theorems. The positive classes do not imply the unrestricted
statement, and no original counterexample has been constructed. The proposed
final disposition is **unsolved, 5/5**, subject to full independent source and
proof review of every partial claim.

No additional author proof search is undertaken after freezing this turn.

## Exact primary dependencies

- Conrad, already bound in SOURCE_ADDITION_T4: Proposition2.1.2
  (smooth normalizers), Theorem3.2.6 (maximal-torus scheme and étale-local
  conjugacy), Proposition3.2.8 (finite étale Weyl group), TheoremA.1.1
  (maximal torus over the actual field). These results were read at their
  full hypotheses; rational conjugacy is not assumed.
- The AOV normal-inertia rigidification theorem and its version qualification
  remain as in turn 4.
- Gille–Szamuely, primary book PDF,
  https://www.math.ens.psl.eu/~benoist/refs/Gille-Szamuely.pdf , §§2.5–2.6:
  cyclic algebra construction and reduced norm. The explicit order and
  residue-field obstruction in this turn are proved above.
