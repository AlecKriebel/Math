# Author turn 1: tame finite stabilizers over arbitrary imperfect fields

Status: partial, one of five substantive author turns. The unrestricted source
question remains unresolved. Perfect fields and all torsors are credited prior
results, not new conclusions of this turn. No novelty claim is made for the
following combination of standard gerbe and ramification facts.

## The positive class

Let k have characteristic p>0. Let G be a smooth affine k-group, and let X
be a smooth homogeneous k-variety whose geometric stabilizer is finite of
order prime to p. Then

    X(k((t))) nonempty  implies  X(k) nonempty.             (T)

No perfection assumption on k or connectedness assumption on G is required.
The finite prime-to-p group scheme is automatically étale. Homogeneity here
means the standard schematic/fppf homogeneous-space condition; mere orbit
transitivity on a selected set of rational points is not substituted for it.
This is a restricted affirmative theorem, not an answer for arbitrary
positive-dimensional or wild stabilizers.

We prove (T) by preserving an entire gerbe object, including its underlying
G-torsor. Proving only that the gerbe becomes neutral would be insufficient.

## 1. A tame Puiseux extension and its precise Galois kernel

Put K=k((t)). In a separable closure of K choose compatible n-th roots
s_n=t^(1/n) for every n prime to p, and set

    K_n=k((s_n)),       L=union_{(n,p)=1} K_n.              (1)

The union is directed by divisibility. The field K_n is also K(s_n), as
seen by grouping a Laurent series in s_n by its exponents modulo n. Thus
K_n/K is finite separable of degree n. All these fields retain k as a
coefficient field; replacing s_n by a formal variable is a k-isomorphism
K_n ≅ k((s)).

Let K^u and K^t denote the maximal unramified and maximal tame extensions.
The standard tame ramification theorem gives

    K^t=L K^u=L k^sep,
    Gal(K^sep/K^t) is pro-p.                              (2)

These assertions hold with imperfect residue field. References:
Temkin, *Tame distillation and desingularization by p-alterations*, Annals
of Mathematics186(2017), §2.2.3–2.2.6; and Brosnan–Reichstein–Vistoli,
*Essential dimension of moduli of curves and other algebraic stacks*,
§5.3, proof of Proposition5.6. In the latter proof K_ram is precisely the
union (1), and the subgroup fixing its compatible roots identifies with
Gal(k). Equivalently, the tame quotient is split by coefficient-field
automorphisms fixing the roots of t.

Consequently restriction to constants gives a continuous exact sequence

    1 → P → Gal(L) → Gal(k) → 1,       P pro-p.            (3)

Here a separable closure of K is also a separable closure of L. The quotient
Gal(K^t/L) is Gal(k), and its kernel in Gal(L) is the pro-p group in (2).
We do not assert that Gal(L) equals Gal(k): the wild kernel remains.

For application of the gerbe base-change statement, L/k is separable.
One elementary verification for K/k in characteristic p is coefficientwise:
any finite k^p-linearly independent family of constants remains linearly
independent over K^p,
since a relation between p-th powers of Laurent series yields a relation
between their coefficients at each exponent. This is the field-theoretic
criterion for separability; algebraic separability of L/K then finishes.
Also k is relatively algebraically closed in L. For a constant-algebraic
element of k((s)), its valuation is zero unless it is zero; subtracting its
constant coefficient gives an algebraic element of positive valuation, which
must be zero. Apply this in a finite K_n containing the element.

## 2. A finite-gerbe descent lemma with full object control

**Lemma.** Suppose L/k is separable, restriction Gal(L)→Gal(k) is surjective
with pro-p kernel, and C is a finite étale gerbe over k whose geometric
automorphism group F has order prime to p. Then

    C(k) → C(L) is an equivalence of groupoids.             (4)

We use the standard group-extension description of finite étale gerbes,
spelled out in Brosnan–Reichstein–Vistoli §5.2, especially Proposition5.5.
Choose a geometric object. Its descent data determine a profinite extension

    1 → F → E → Gal(k) → 1.

Objects over a separable extension M/k are continuous lifts
Gal(M)→E of restriction to Gal(k), and morphisms are the corresponding
conjugations by elements of F. This description includes nonneutral gerbes;
no k-object is presumed.

Given an object over L, its lift s:Gal(L)→E sends the pro-p kernel P into
F. Its finite image is a p-group, and hence trivial, because |F| is prime
to p. Thus s factors uniquely through a continuous section Gal(k)→E.
Continuity follows from the quotient topology of a continuous surjection
of profinite groups. The section is a k-object giving the original object
back after base change. Conjugation identities between two sections hold
over Gal(L) exactly when they hold over Gal(k), by surjectivity. This proves
both essential surjectivity and full faithfulness in (4).

This lemma is closely related to the credited tame-gerbe specialization
functors in the same primary source, Theorem5.10. The argument here uses
the particular union (1) to obtain an isomorphism with a constant object,
which will preserve its underlying torsor after extension to L.

## 3. Apply the lemma to the homogeneous-space gerbe

The quotient stack C=[X/G] is a gerbe over k, and geometrically is B F,
where F is the geometric stabilizer. Since F is finite étale, C is a finite
étale gerbe. These facts can also be read directly from an orbit presentation
after a separable extension admitting a point of X; smoothness supplies
such points and the finite étale stabilizer makes the orbit map a finite
étale torsor. Objects of C over a field M are G_M-torsors E with a
G-equivariant map E→X_M. In particular, a point x in X(K) defines an
object xi in C(K) whose underlying G-torsor is trivial.

Base-change xi to L. By (4), there is an object eta in C(k) and an
isomorphism

    eta_L ≅ xi_L   in C(L).                                (5)

Let E be the underlying G-torsor of eta. The forgetful map [X/G]→B G
sends (5) to an isomorphism with the trivial G_L-torsor. Therefore E(L)
is nonempty. Since E is of finite type, this point is defined over a finite
stage K_n in (1). The credited Florence–Gille torsor theorem, applied to
K_n≅k((s)) over the unchanged coefficient field k, gives E(k) nonempty.
The equivariant map E→X now sends any such point to X(k). This proves (T).

The use of a full object is important. Neutrality of C alone would only
produce a possibly nontrivial G-torsor mapping to X. The isomorphism (5)
proves that this specific constant torsor becomes trivial over L and hence
allows the existing torsor descent theorem to finish.

## 4. A sharp failure of the chosen object-descent mechanism in the wild case

The argument cannot drop the prime-to-p condition merely by replacing F
with a finite p-group. Over the same L from (1), consider the C_p-torsor

    z^p−z=t^(−1).                                        (6)

It is not isomorphic to the base change of any C_p-torsor over k. Indeed
such an isomorphism would mean

    t^(−1)−a=b^p−b,       a in k, b in L.

Choose a stage K_n=k((s)) containing b, with t=s^n and p not dividing n.
The left side has valuation −n. If b has nonnegative valuation then the
right side does also; if b has negative valuation then its right-side
valuation is p·v(b), divisible by p. Either case contradicts −n. Thus
B C_p(k)→B C_p(L) is not essentially surjective.

This is NOT a counterexample to the original homogeneous-space question:
(6) is a nonconstant torsor over L, not a k-defined space acquiring a point
over k((t)). It is an exact counterexample only to extending the object-
descent lemma to wild finite inertia. The pro-p kernel in (3) is precisely
the part that a wild stabilizer can detect.

## Remaining task

The unrestricted imperfect-field question remains open in this packet.
The next mechanism must address nontrivial wild inertia, infinitesimal
stabilizers or positive-dimensional isotropy; simply repeating tame gerbe
descent would not do so. Normal-stabilizer and proper-space reductions alone
would likewise not fill this gap. All known torsor/perfect-field inputs remain
credited, and historical novelty of the partial combination is unverified.
