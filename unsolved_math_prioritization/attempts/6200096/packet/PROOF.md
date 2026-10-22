# A published obstruction to homotopy Nielsen realization

Target: UnsolvedMath 6200096, AMR-061-0096, Kapovich Problem 96.

Status: **already_solved**, in the negative for the unrestricted question.
This is an exposition and verification of an existing counterexample family,
not a claim of a new mathematical result.

## 1. Scope and source correction

The homotopy Nielsen question asks whether a prescribed discrete subgroup of
the group of **unbased homotopy classes** of simple self-equivalences of a
compact polyhedron can be represented, compatibly with a homotopy equivalence,
by homeomorphisms of a compact replacement space.

Compatibility means: for a homotopy equivalence e:X→Y and prescribed classes
ρ(g), the homeomorphisms h_g of Y satisfy [h_g e]=[e]ρ(g), with all group laws
holding exactly for the h_g. Neither a fixed basepoint nor a free action is
required. Merely asking for an unrelated action of the abstract group on Y
would be a different question. Likewise, a strict group of actual continuous
maps with actual continuous inverses is already a group of homeomorphisms.

Kapovich's author-hosted version, dated October 24, 2007, places this question
at Problem 96, page 24. Its immediately following Remark 32 attributes negative
examples to Cooke. The catalogue's standalone statement and prior short report
omit this decisive context. The earlier AIM-hosted version numbers the question
94 and the associated remark 33; numbering alone must not identify the target.

For an explicit modern primary reference, see Jaka Smrekar, *Rational
Reidemeister trace of an outer automorphism of finite order*, Journal of Pure
and Applied Algebra 227 (2023), article 107350, Example 1, page 5:
https://doi.org/10.1016/j.jpaa.2023.107350 . The construction below specializes
that published family to p=2, A=(-1), and central twist 1. We give an elementary
extension obstruction and an explicit simple representative, so neither the
Bass conjecture nor a Whitehead-group vanishing theorem is needed.

## 2. The algebraic homotopy action

Let H=⟨c⟩×F(a,b,d), with c of infinite order and F(a,b,d) free of rank three.
Define an automorphism φ by

    φ(c)=c^(-1),   φ(a)=ca,   φ(b)=d,   φ(d)=a^(-1)ba.

These assignments preserve the commutation relations for c. An inverse is

    φ^(-1)(c)=c^(-1),   φ^(-1)(a)=ca,
    φ^(-1)(b)=ada^(-1), φ^(-1)(d)=b.

Evaluation on the four generators gives

    φ²(h)=a^(-1)ha  for every h∈H.

On abelianization, φ sends c to -c and swaps the b and d coordinates, so φ is
not inner. Consequently its class [φ] has order exactly two in Out(H).

## 3. A compact polyhedron with a simple representative

We specify a graph Γ with vertices u,v, oriented edges
e:u→v and f:v→u, and loops B at u and D at v. Its rank is three. Subdivide
the edges and loops if necessary to obtain a finite simplicial complex.
Let δ exchange u with v, e with f (preserving the indicated parametrizations),
and B with D. Then δ is a piecewise-linear involution.

Use basepoint u and the following free basis for π₁(Γ,u):

    a=ef,   b=B,   d=f^(-1)Df.

Define κ:Γ→R/Z to run once positively around R/Z along e and to be zero on
f,B,D. Both endpoints of e map to zero, so κ is well-defined, continuous and
piecewise linear. On the compact two-dimensional polyhedron

    X=(R/Z)×Γ

define

    F(s,x)=(-s+κ(x), δ(x)),

where the first coordinate is taken modulo 1. Its inverse is

    F^(-1)(s,x)=(-s+κ(δ(x)), δ(x)).

The formulas are integral-affine on each product cell after finite subdivision
at the wrap lines in R/Z. Thus F is a PL homeomorphism. A PL homeomorphism
between compact polyhedra is a simple homotopy equivalence: after subdivision
it is a simplicial isomorphism, and finite subdivisions preserve simple type.
This explicitly verifies the target's simple-homotopy hypothesis.

The map F moves (0,u) to (0,v). Change the basepoint back along
p=(0,f^(-1)), a path from (0,u) to (0,v). The resulting based automorphism
sends a loop ℓ to p·F(ℓ)·p^(-1). Its values are exactly φ above:

* the circle generator c is reversed;
* a=ef has κ-degree 1 and graph image f e; conjugating its basepoint by
  f^(-1) changes that graph image back to ef, giving ca;
* B maps to D and hence b maps to f^(-1)Df=d;
* f^(-1)Df maps in the graph to e^(-1)Be, giving a^(-1)ba.

The universal cover of X is R times a tree, hence contractible. For connected
CW complexes of type K(H,1), unbased homotopy classes of self-equivalences
correspond to Out(H). Therefore [F]²=1 and [F]≠1. We obtain a faithful
homomorphism C₂→E_s(X) taking the nonidentity element to [F], where E_s(X)
denotes the group of unbased homotopy classes of simple self-equivalences.
It is a homotopy involution; F itself is not asserted to have order two.

## 4. A necessary extension for any realizing action

For completeness, no local regularity or universal-cover hypothesis on a
replacement space is needed here. If a discrete group K acts by homeomorphisms
on a path-connected space Y, fix y∈Y and form E from pairs

    (g,[γ]),  g∈K,  γ a path from y to g(y),

where paths are taken up to endpoint-fixed homotopy. Multiplication is

    (g,[γ]) (h,[η]) = (gh,[γ * g(η)]).

Concatenation is associative up to endpoint-fixed homotopy; constant paths
give the identity and reversed transported paths give inverses. Projection
to g is surjective by path-connectedness. Its kernel consists of loops at y,
and hence there is an exact sequence

    1 → π₁(Y,y) → E → K → 1.

The outer action of K on the kernel is exactly that induced by the action on
Y: conjugation by (g,[γ]) sends [ℓ] to [γ*g(ℓ)*γ^(-1)]. This construction is
also the fundamental-group extension of the Borel construction.

Suppose now that Y is homotopy equivalent to X and carries a C₂-action
realizing the prescribed homotopy action. Since X is path-connected, so is Y.
Using the homotopy equivalence to identify π₁(Y) with H, the above extension
has outer action [φ]. This conclusion applies to an arbitrary compact space
Y and even to arbitrary noncompact Y with the required homotopy type.

## 5. The impossible parity equation

Assume such an extension 1→H→E→C₂→1 exists. Choose a lift t of the generator
of C₂. Its conjugation on H represents [φ]. Multiplying t by an element of H
changes that representative by an inner automorphism, so choose t with

    tht^(-1)=φ(h)  for all h∈H.

Since t²∈H and φ² is conjugation by a^(-1), we have

    t²=c^n a^(-1)  for some n∈Z.

Indeed, two elements inducing the same conjugation differ by an element of
Z(H)=⟨c⟩; the center of a nonabelian free group is trivial.
But t commutes with its square. Consequently φ(t²)=t², whereas

    φ(c^n a^(-1))=c^(-n-1)a^(-1).

Equality forces n=-n-1, or 2n=-1. No integer n satisfies this equation.
This contradiction proves that the homotopy C₂-action has no topological
realization on any space homotopy equivalent to X. In particular, it has
no compact realization. All target hypotheses are satisfied.

## 6. Controls and boundaries of the conclusion

The obstruction is the lack of a **group-compatible** choice of representatives,
not the absence of individual homeomorphism representatives: our F is already
a PL homeomorphism. Enlarging X by a contractible compact factor cannot remove
the fundamental-group extension obstruction.

For an integral twist k, replace φ(a)=ca by φ_k(a)=c^k a. The same computation
gives 2n=-k. Odd k are obstructed. For k=0, the explicit PL map
F₀(s,x)=(-s,δ(x)) is an actual involution, giving a positive control. We do not
deduce a general sufficiency theorem merely from even k passing this necessary
test. Allowing a rational central exponent would solve 2n=-1 with n=-1/2,
which confirms exactly where integrality enters; it changes the group.

The file verify.py checks reduced-word identities, the displayed inverse,
the graph basepoint formulas, and parity controls using exact arithmetic.
Finite tests are error-detection controls; the arguments in Sections 2–5,
not finite enumeration, prove the statements for all elements and all models.

No claim is made here about torsion-free acting groups, surface-only models,
or restricted subclasses. The unrestricted selected target is already
negative by published work. Five new search routes are unnecessary once this
prior resolution is verified.
