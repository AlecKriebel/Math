# A lift-sensitive enhancement for Ohtsuki Problem 5.9

**Candidate, author turn 1 of 5. Independent review pending.**

This is an explicit construction from standard extension theory and the published generalized cocycle invariant of Carter, Elhamdadi, Graña and Saito (CEGS, 2005). No novelty or priority is asserted. The result answers the construction request, not the neighboring request to compute every generalized cohomology group. In particular, it does not assert that the scalar CEGS invariant alone detects every obstruction.

## 1. Exact data and scope

Let X be a quandle, A an abelian group, and R_x an automorphism of A for each x in X, satisfying

    R_(x*y) = R_y^(-1) R_x R_y.

Use normalized cochains: C¹ consists of all maps X → A and C² consists of maps φ:X² → A with φ(x,x)=0. In the convention on Ohtsuki's printed p.464,

    (d f)(x,y) = R_y^(-1)(f(x)+(R_x-I)f(y)) - f(x*y),

and the 2-cocycle condition is

    R_z^(-1) φ(x,y) + φ(x*y,z)
      = R_(y*z)^(-1) φ(x,z)
        + R_(y*z)^(-1)(R_(x*z)-I) φ(y,z)
        + φ(x*z,y*z).                                      (1)

Fix α=[φ]. Its extension is Y_φ=A×X with

    (a,x)*(b,y) = (R_y^(-1)(a+(R_x-I)b)+φ(x,y), x*y).         (2)

K is an oriented classical knot, Q=Q(K) its fundamental quandle. The finite state-sum statements below assume finite X, so Hom(Q,X) is finite because a finite knot diagram gives finitely many generators. A need not be finite. For arbitrary X the indexed collection described below is the invariant; no unsupported infinite sum in a group ring is taken. Neither connectedness, faithfulness, nor a field structure is imposed.

## 2. Complete intrinsic obstruction and all lifts

For each coloring C:Q→X, make A into a Q-module by R^C_q=R_(C(q)). Pullback of cochains commutes with d by substitution in the displayed formulas. Define

    o_α(C) = C*α in H²_Q(Q; A_C).

**Lifting criterion.** C lifts to a quandle homomorphism Q→Y_φ over X if and only if o_α(C)=0. When nonempty, the set of lifts is a torsor for Z¹_Q(Q;A_C)=ker(d:C¹→C²).

Proof. Every map over C is uniquely q↦(a(q),C(q)). It is a homomorphism exactly when, for every p,q,

    a(p*q) = R_(C(q))^(-1)(a(p)+(R_(C(p))-I)a(q))
               + φ(C(p),C(q)),

that is, d_C a = -C*φ. Solvability is exactly vanishing of its cohomology class. Differences of two solutions lie in ker d_C, and adding any element of ker d_C to one solution gives every other solution, freely and transitively. This is an equation in all cochains; it does not require a chosen presentation or a decision procedure.

If φ'=φ+d f, the explicit isomorphism over X

    Y_φ → Y_φ',   (a,x) ↦ (a-f(x),x)                       (3)

follows by inserting the formula for d f into (2). Thus liftability and the lift torsor depend only on α. An isomorphism of fundamental quandles induced by oriented knot equivalence bijects colorings and lifts and transports the pulled-back classes and their coefficient modules. The colored family of obstruction classes, coefficient modules, and lift torsors is therefore intrinsic, up to that transport, including when X is infinite.

## 3. A finite exact test, rather than only a definition by lifts

Take the usual over-arc presentation of an oriented diagram. At each crossing use the relation q_t=q_s*q_o, with s and t chosen by the normal to the over-arc; this convention handles either crossing sign without changing (2). For a coloring C, form the group homomorphism

    L_C:A^(arcs) → A^(crossings),
    (L_C a)_r = a_t - R_y^(-1)a_s - R_y^(-1)(R_x-I)a_o,

where x=C(q_s), y=C(q_o), and put b_C(r)=φ(x,y). Then

    Lift_φ(C) = {a : L_C a=b_C}.                            (4)

Indeed the diagram is a presentation of Q, so assignments satisfying all its crossing relations extend uniquely to quandle homomorphisms. Consequently

    C lifts ⇔ [b_C]=0 in coker L_C.

This last cokernel is only used as a presentation-dependent test; no unproved claim that the entire cokernel is diagram invariant is needed. The solution set and its kernel torsor are the intrinsic ones in §2. If A is finite, enumerate A^(arcs), or solve the finite abelian-group linear system, obtaining exactly 0 or |ker L_C| lifts. If A is a finitely generated abelian group with explicitly given automorphisms, (4) is an integer linear system with its group relations and is decidable by Smith normal form. For arbitrary A this remains a precise solvability criterion, without an algorithm claim. The crossing-free unknot has one free arc variable, no equations, and |A| lifts for each base color (cardinally when A is infinite).

Equation (3) acts on (4) by a↦a-f∘C, since L_C(f∘C)=-(d f)∘(C,C). This checks the sign and α-independence explicitly.

## 4. Translation to the published generalized cocycle invariant

CEGS use the enveloping-group convention e_(x*y)=e_y e_x e_y^(-1), and the group-action quandle module

    η'_(x,y)=t_y,   τ'_(x,y)=I-t_(x*y).

The source convention is not the same formula. Set

    t_x=R_x^(-1),   T_x=R_x^(-1),
    κ(x,y)=T_(x*y) φ(x,y).

The assignment e_x↦t_x is a representation of the CEGS enveloping group. The fiberwise bijection (a,x)↦(T_x a,x) transforms (2) into

    (u,x)*(v,y) = (t_y u+(I-t_(x*y))v+κ(x,y), x*y),          (5)

because

    T_(x*y) R_y^(-1) T_x^(-1) = R_y^(-1),
    T_(x*y) R_y^(-1)(R_x-I) T_y^(-1) = I-T_(x*y).

Thus κ is a normalized generalized cocycle in exactly the group-action setting of CEGS §6. This can also be checked by multiplying (1) by T_((x*y)*z). Normalization is preserved. If φ changes by d f, put λ(x)=T_x f(x); then κ changes by

    t_y λ(x)+(I-t_(x*y))λ(y)-λ(x*y),

the CEGS coboundary up to their harmless global sign convention.

For a diagram coloring C let w_α(C)∈A be the CEGS weight (Definition 6.1/6.3, pp.521–522): at each crossing evaluate ±κ(x,y), transport it by the ordered t-actions of colors crossed by a path from the unbounded region to the crossing's target region, and sum the transported values. The path exponent is +1 against the arc normal and -1 with it; the overall sign is the oriented crossing sign, exactly as in their Definition 6.1.

The published Lemma 6.2, Theorem 6.4 and Lemma 6.5 (pp.522–523) show path independence, invariance under corresponding colored Reidemeister moves, and invariance under a cocycle coboundary. These are local, per-color statements: R1 uses κ(x,x)=0, R2 cancels inverse contributions, R3 is the generalized cocycle identity, and coboundaries telescope on arcs. Their proofs therefore apply to individual colorings also when X is infinite; only the finite sum requires finite X. We invoke these published results, not a claim of a newly discovered scalar invariant.

CEGS Theorem 6.10 (p.525) proves the implication

    C lifts ⇒ w_α(C)=0.                                   (6)

It does not assert the reverse implication. We do not use that reverse implication, their group-extension Proposition 6.6, or the discussion of group cohomology in Remark 6.11.

## 5. The requested lift-sensitive state sum

For finite X define ε_α(C)=0 if o_α(C)=0, and ε_α(C)=1 otherwise. With [a] denoting the basis element of the integral group ring Z[A], define

    Ψ_α(K;v) = Σ_(C∈Hom(Q(K),X)) [w_α(C)] v^(ε_α(C))
               in Z[A][v].                               (7)

For arbitrary X retain the corresponding indexed family (w_α(C),o_α(C),Lift_φ(C)), up to the transport in §2, rather than (7).

**Theorem.** The construction is an oriented knot invariant associated with α. It extends the ordinary quandle cocycle invariant and records exactly which colorings lift. For finite X, the constant coefficient in v of (7) is

    #{C : C lifts} [0],

and the augmentation of its coefficient of v is #{C : C does not lift}. Setting v=1 recovers the published generalized cocycle state sum. When the action R is trivial, this specialization is exactly the ordinary quandle cocycle invariant in Ohtsuki §5.4.

Proof. Sections 2–4 give a bijection of colorings preserving both entries (w,ε) under an oriented knot equivalence, and independence of the representative of α. This proves (7) invariant. Equation (6) identifies its constant coefficient. When R_x=I, the gauge T is the identity and κ=φ, all transport actions disappear, and w is the usual signed sum of local cocycle values. Hence v=1 gives precisely the ordinary state sum, with no normalization by |A|.

There is a stronger consistency check in this trivial-action case. Going once around the single knot component, the first coordinate in (2) changes by the signed sum w(C), independently of all over-arc lift coordinates. Starting with any a∈A returns consistently exactly when w(C)=0. Thus every such coloring has either |A| lifts or none, and ε(C)=1_(w(C)≠0). For general actions the exact test is (4), not this scalar shortcut.

If A is finite, a further lift-number enhancement is obtained by recording |Lift_φ(C)| along with (w,ε), or by forming Σ_C [w_α(C)] u^(|Lift_φ(C)|). The identity

    Σ_C |Lift_φ(C)| = |Hom(Q(K),Y_φ)|

is just the partition into fibers of the induced map on colorings. Neither this identity nor (7) assumes that all nonempty fibers have a common size in the nontrivial-action case.

## 6. Meaning of the conclusion

The original target asks for a construction, not for a universal numerical closed formula, classification of cohomology, or a complete knot invariant. Formula (7), its intrinsic obstruction, and the finite affine procedure provide the requested construction. It deliberately retains a complete lifting test in addition to the established scalar invariant, so it does not strengthen Theorem 6.10 without proof. This is a credited standard-theory construction; the current search has not established that this precise packaging is historically new, and no such assertion is made.
