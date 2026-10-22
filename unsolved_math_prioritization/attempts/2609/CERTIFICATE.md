# A credited counterexample to Kourovka 21.100

## Result and attribution

Eric Hou's preprint *Coprime Actions and Characters Non-vanishing on the Fixed-point Subgroup*, [arXiv:2609.16227v1](https://arxiv.org/abs/2609.16227v1), supplies a negative answer to the exact question catalogued as UnsolvedMath 2609 / Kourovka 21.100. This document reconstructs that existing construction. It is not a discovery or first-priority claim. No original proof-attempt turn was spent: the result was found during the source gate. The verified disposition is `already_solved`, with `0/5` original turns.

The original target is a universal counting assertion: if a finite group A acts on a finite group G with coprime orders, and C consists of the elements fixed by every operator, are exactly |C/C'| of the A-invariant irreducible complex characters nonzero at every element of C?

The counterexample below has |A|=21, |G|=2^135, C elementary abelian of order 4096, and an A-invariant irreducible character vanishing at an element of C. There are exactly 4096 invariant irreducible characters in total. Thus the requested number is strictly less than 4096. This strict inequality alone resolves the original problem negatively; the optional exact enumeration further gives 1728.

## 1. Explicit group and action

Use F4=F2[r]/(r^2+r+1) and F8=F2[s]/(s^3+s+1). Both displayed polynomials are irreducible over F2: the quadratic has no root, and a cubic without a root is irreducible. The nonzero elements r and s have orders 3 and 7, respectively. Set

    V = F4 ⊕ F4 ⊕ F8,
    T(x,y,z) = (rx,ry,sz),
    A = <T> ≅ C21.

Then V is a seven-dimensional F2-space. The order of T is lcm(3,7)=21 and its fixed space is zero, since none of r-1 and s-1 vanish. The action is faithful.

Let B be the additive group of all functions V→F2. For t∈V put (τ_t f)(x)=f(x+t), and define

    G = B ⋊ V,
    (f,t)(g,u) = (f + τ_t g, t+u).

There are 2^128 functions in B and 128 elements of V, so |G|=2^135. Extend T by

    T·(f,t) = (f∘T^(-1), Tt).

The identity (τ_t g)∘T^(-1)=τ_(Tt)(g∘T^(-1)) verifies multiplicativity. Consequently A acts by automorphisms and its order is coprime to |G|.

## 2. Fixed subgroup and its exact order

An A-fixed pair (f,t) has t=0, because V^A=0. Its function f must be constant on every A-orbit of V. Therefore

    C = C_G(A) = B^A.

In particular C is elementary abelian, so C'=1. To count its dimension, write U=F4² and W=F8. The five one-dimensional F4-subspaces L of U divide U\{0} into five sets of size 3. The orbits on V are:

- the singleton {(0,0)};
- five sets (L\{0})×{0}, each of size 3;
- {0}×(W\{0}), of size 7;
- five sets (L\{0})×(W\{0}), each of size 21.

The last sets really are single orbits: the exponents of r and s vary independently by the Chinese remainder theorem for 3 and 7. This lists 12 disjoint orbits with sizes summing to 128. Hence C≅C2^12 and |C/C'|=4096.

## 3. One invariant irreducible character with a fixed-subgroup zero

Let λ:B→{±1} be evaluation at zero followed by the sign map:

    λ(f)=(-1)^(f(0)),  χ=Ind_B^G λ.

The conjugates of λ under translations are the 128 distinct evaluation characters f↦(-1)^(f(t)). Distinctness follows by testing the function supported at a single point. As B is normal, Mackey's inner-product formula shows

    <Ind_B^G λ, Ind_B^G λ>_G
       = Σ_(t∈V) <λ,λ^t>_B = 1.

Thus χ is irreducible and χ(1)=128. The operator group fixes zero, so it fixes λ and hence fixes χ. For c∈B, the induced-character formula is particularly simple:

    χ(c)=Σ_(t∈V) (-1)^(c(t))=128-2|supp(c)|.

Choose any three of the five F4-lines in U, and let S consist of zero together with the three corresponding size-21 orbits. This is A-stable and |S|=1+3·21=64. Its indicator c=1_S belongs to C, and χ(c)=128-2·64=0.

This part does not require a full character table, a Glauberman-correspondent computation, or the longer zero-classification argument of Hou's paper.

## 4. Exactly 4096 invariant irreducible characters

The classical Glauberman correspondence already gives |Irr_A(G)|=|Irr(C)|=4096, since A is solvable and acts coprimely. For completeness, the following elementary argument reconstructs the count directly and supports the optional checker without using that correspondence.

For a function u∈B define

    λ_u(f)=(-1)^(Σ_x u(x)f(x)),
    V_u={t∈V:τ_t u=u},   I_u=B⋊V_u.

Every linear character μ of V_u gives a linear character θ_(u,μ) of I_u by θ_(u,μ)(f,t)=λ_u(f)μ(t). The invariance defining V_u makes this multiplicative. The induced characters Ind_(I_u)^G θ_(u,μ), taking one u per translation orbit, are irreducible and pairwise distinct. Indeed, I_u is normal, and every coset outside I_u changes the B-weight λ_u, while the identity coset distinguishes the different μ. Mackey's formula gives these assertions. They are exhaustive: the contribution to the sum of squared degrees from an orbit O=V·u is

    |V_u| [V:V_u]^2 = |V| |O|;

summing over all translation orbits in B gives |V||B|=|G|.

It remains to determine which of these characters are A-invariant. An A-invariant character must have an A-stable translation orbit of weights. Every such orbit contains exactly one A-fixed function. Here is a direct proof.

If a·u=τ_(z_a)u, then V_u is A-stable and z_a is well-defined modulo V_u. The classes z_a satisfy z_(ab)=z_a+a z_b in V/V_u. Since |A| is odd, summing over b shows, with w=Σ_b z_b, that z_a=w+a w. Therefore τ_w u is fixed by every a. By Maschke's theorem, V/V_u is isomorphic to an A-stable complement of V_u in V, and consequently (V/V_u)^A=0. If both u and τ_tu are fixed, t+V_u is fixed, so t∈V_u and the two functions coincide. This proves existence and uniqueness.

Fix this unique u∈B^A. The extension θ_(u,1) is A-invariant, and the character parameters are equivariant and injective. Therefore the induced character associated to μ is A-invariant exactly when μ is. But (V_u^*)^A=0: Maschke's theorem and V_u^A=0 imply that V_u has no trivial quotient as well as no trivial submodule. Thus only μ=1 is invariant. We have obtained a bijection

    B^A → Irr_A(G),  u↦χ_u=Ind_(I_u)^G θ_(u,1).

It follows that |Irr_A(G)|=|B^A|=4096, as claimed.

## 5. Conclusion for the precise original question

Among exactly 4096 invariant irreducible characters, the character in §3 has a zero on C. Thus at most 4095 can be nowhere zero there, whereas |C/C'|=4096. This disproves the universal equality. Because C is abelian, every character in Irr(C) is linear, so the proposed stronger characterization by linearity of the Glauberman–Isaacs correspondent also fails for this example.

The independent supplemental calculation gives the sharper values

    #{χ∈Irr_A(G): χ|_C nowhere zero}=1728,
    #{χ∈Irr_A(G): χ|_C has a zero}=2368.

The original negative answer follows without these supplemental numbers. The packet does not assert verification of Hou's minimality, infinite-family, Carter-subgroup, or head-character results, nor does it settle restrictions such as prime-power A. Its mathematical attribution is to Hou throughout.

## 6. Verification level

This is a human-readable proof reconstruction with independent exact finite checks. It is not a formal proof-assistant certificate or evidence of journal/editor acceptance. The source was an arXiv preprint as inspected on 3 October 2026; the October Kourovka Notebook still had no solution marker at 21.100. These status facts are recorded separately from the mathematical verification.
