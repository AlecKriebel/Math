# Author turn 2: finite wild isotropy for H1-trivial groups, and a failed extension

Status: partial, 2/5 substantive author turns. This turn admits wild finite
étale stabilizers in one substantial acting-group class and gives an exact
obstruction to extending the same argument to arbitrary groups. It does not
supply a counterexample to the original question.

## 1. Neutrality descends for every finite étale gerbe

Let k be any field and K=k((t)). The restriction homomorphism

    rho:Gal(K)→Gal(k)

has a continuous section. This holds also when k is imperfect. A precise
primary reference is Brosnan–Reichstein–Vistoli, *Essential dimension of
moduli of curves and other algebraic stacks*, Proposition5.6 and its proof,
pp.13–14 in the inspected author PDF. It first splits the tame sequence
using compatible roots of a uniformizer, then lifts the section across
wild pro-p inertia using cd_p(Gal(k))≤1. No compatible choice across all
field extensions is asserted; their Remark5.8 distinguishes that issue.

For a finite étale gerbe C over k, use the credited extension description

    1→F→E→Gal(k)→1

from the same source, Proposition5.5. A K-object is a lift s:Gal(K)→E.
Composing s with a section of rho gives a section Gal(k)→E, hence a
k-object. Thus

    C(K) nonempty implies C(k) nonempty                    (1)

without any prime-to-characteristic bound on |F|. Unlike turn 1's statement
over its particular tame Puiseux extension, (1) is only an existence claim;
it does not say that every K-object is the base change of a k-object.
The Artin–Schreier example in turn 1 already forbids such a claim in the
wild case.

## 2. Positive result for an H1-trivial acting group

**Theorem.** Let G be a smooth affine k-group with H1(k,G)={1}. Let X
be a smooth homogeneous k-variety whose geometric stabilizer is finite
étale, with no restriction on its order. Then

    X(k((t))) nonempty implies X(k) nonempty.              (2)

Indeed C=[X/G] is a finite étale gerbe. A K-point of X gives a K-object
of C; (1) gives a k-object. That object is a G-torsor E over k equipped
with an equivariant map E→X. The hypothesis H1(k,G)={1} makes E trivial,
and any point of E(k) maps to X(k). This proves (2).

The hypothesis is required only at the particular field k, not at all
extensions. Standard examples valid over arbitrary fields are GL_n, SL_n
and Sp_{2n}: Hilbert90 proves the GL_n assertion; the determinant sequence
and surjectivity GL_n(k)→k^* give SL_n; classification of nondegenerate
alternating forms gives Sp_{2n}, including characteristic2. This does not
assert the same for all split reductive groups.

The group-extension input is credited prior work; the source-level problem
still concerns arbitrary affine acting groups and arbitrary stabilizers.
No priority is claimed for this partial corollary.

## 3. Why the section-fixed-field argument does not finish the general case

Over a perfect field Florence passes to the fixed field of a Galois section
and proves that constant torsors inject there. This is an essential input,
not a consequence of having a section. We exhibit a failure of that input
for a suitable section over an imperfect field.

Fix any prime p and put k=F_p(a,b), with a,b algebraically independent.
Consider the smooth connected unipotent group and its torsor

    U: y^p−a x^p−x=0,
    P: y^p−a x^p−x=b.                                    (3)

The group operation is coordinatewise addition. The additive polynomial
map Ga²→Ga defining (3) is smooth and surjective (its x-derivative is −1),
so every fiber is a torsor under U. Over k(d), d^p=a, the substitution
z=y−d x yields z^p−x=0 for U, and z^p−x=b for P. Thus U is geometrically
Ga, and P is a smooth geometrically integral affine curve.

**P(k) is empty.** Use the valuation at the pole of b, normalized by
v(b)=−1; its residue field is F_p(a). If x and y both have nonnegative
valuation, the left side of (3) does also, which is impossible. Otherwise
let m=min(v(x),v(y))<0. The leading p-th-power terms cannot cancel: if
both have valuation m, cancellation would force a to be a p-th power in
F_p(a); if the valuations differ, there is only one leading term. The
left-hand side consequently has valuation p m, since v(x)≥m>p m. It
cannot equal −1. This proves P(k)=empty.

The same leading-degree argument shows that U is k-wound: a nonconstant
polynomial map A1→U would force equality of the degrees of x and y and
then force a to be a p-th power in k. If x is constant, y is constant too.
Thus no subgroup Ga exists; a unipotent group has no subgroup Gm.
This terminology is supplementary; nontriviality of P was proved directly.

Now set K=k((t)) and define

    R=k[[t]][v]/(v^p−t v−a),       L=Frac(R).              (4)

The reduction of the displayed monic polynomial modulo t is irreducible
over k. The ring R is therefore a complete local domain, finite free of
rank p over k[[t]], with maximal ideal (t) and residue field k(d), d^p=a.
It is a discrete valuation ring with uniformizer t. The polynomial's
derivative over K is −t, so L/K is finite separable of degree p. Its
ramification index is1, but its residue extension is purely inseparable
of degree p. This is the imperfect-residue phenomenon excluded in the
perfect-field argument.

**P(L) is nonempty, explicitly.** In R put

    c=(−b)^p t v,
    delta=sum_{j≥0} (−a)^((p^j−1)/(p−1)) c^(p^j).

The series converges t-adically because v_t(c)=1. Frobenius and cancellation
of consecutive terms give delta+a delta^p=c. Then

    x=−b+delta,      y=−b v

satisfy (3), using v^p=a+t v. Thus a constant smooth torsor that has no
k-point becomes trivial over the separable extension L of K.

Finally apply the section theorem to the henselian valued field L. Since
its residue field k(d) is purely inseparable over k, Gal(k(d)) identifies
canonically with Gal(k). The homomorphism Gal(L)→Gal(k(d)) agrees, under
that identification, with restriction to constants: finite separable
constant extensions of k give the corresponding unramified extensions of
L, whose residues are their composites with k(d). A section therefore
composes with Gal(L)⊂Gal(K) to give a section sigma:Gal(k)→Gal(K).
Its fixed field M=(K^sep)^(sigma(Gal(k))) contains L. Consequently

    P(k)=empty,      P(M) nonempty.                        (5)

In particular H1(k,U)→H1(M,U) is not injective for this choice of section.
This is a counterexample to an auxiliary extension of the perfect-field
method, not to Laurent descent: P(k((t))) is still empty by the credited
torsor theorem (and is not claimed otherwise).

## 4. Precise gap and next route

For arbitrary G, (1) produces a G-torsor mapping to X but does not prove
it trivial. Composing a Galois lift with a section cannot fix that gap:
(5) shows why triviality after passing to a section-fixed field need not
reflect to k. Turn 1 avoided this by its tame Puiseux union, every finite
stage of which is k-isomorphic to a Laurent field; wild residue extensions
need not have that property as k-fields.

The unresolved classes include non-H1-trivial acting groups with wild
finite stabilizers, and general positive-dimensional or infinitesimal
stabilizers. The next substantive route will investigate reductions that
use the geometry of a particular embedding of the stabilizer, rather than
only the abstract Galois group of the ambient field.
