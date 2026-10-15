# Substantive turn 4: a finite-quotient obstruction with nontrivial twist actions

**Partial, unreviewed; no counterexample or full lifting theorem is claimed.** Date: 2026-10-01. This turn replaces the pointwise-invariant quotient restriction from turns 2–3 by an ordered finite-quotient test that retains nontrivial monodromy actions and all smooth local choices.

## 1. Exact global input required

Start with an actual positive identity factorization and its associated sphere-base Lefschetz fibration. Cut the sphere into its critical disk and a trivial disk. In a fixed boundary mapping-torus identification, the section of the trivial cap determines a based fiber class alpha. This class is part of the geometric input; it may not be chosen arbitrarily.

Use the conventions of [Hillman–Pedrotti, arXiv:2604.10943v1](https://arxiv.org/pdf/2604.10943v1), Theorem 3.19: the critical-disk monodromy is tau_Vn composed with ... composed with tau_V1. Put psi_i=(tau_Vi)_*^(-1), and write v_i for the correctly based oriented vanishing-cycle element. Define

    Psi_0 = identity,
    Psi_i = psi_1 composed with ... composed with psi_i.

A smooth extension requires, and at the full surface-group level is characterized by, an expression

    alpha = product_(i=1)^n Psi_(i-1)(
                x_i v_i^(epsilon_i) psi_i(x_i^(-1))),
    x_i in pi_1(S,p),  epsilon_i in {0,1}.                (1)

Products are in the displayed order. The two exponents are the two allowed smooth local types, including the two separating-side choices. The quantified x_i include every twisted-conjugate alternative; the test does not fix one arbitrary representative of a curve lift. If the local orientation convention is reversed, the corresponding oriented v_i and exponent representatives must be changed coherently.

## 2. Finite obstruction theorem

Let rho:pi_1(S,p) -> G be a surjection onto a finite group. Require that each psi_i preserve ker(rho), so it induces a **verified** automorphism sigma_i of G. Write z_i=rho(v_i), a=rho(alpha), and Sigma_i=sigma_1 composed with ... composed with sigma_i. Compute

    D_i = { x z_i^epsilon sigma_i(x^(-1)) :
            x in G, epsilon in {0,1} },
    R_0 = {identity},
    R_i = { r Sigma_(i-1)(d) : r in R_(i-1), d in D_i }.  (2)

**Claim. If a is not in R_n, the original positive factorization has no allowed one-puncture identity lift.**

Proof: A lift would give a smooth section and hence an expression (1). Applying rho to every factor gives (2). The image after i factors belongs to R_i by induction, so a belongs to R_n. Contraposition proves the claim. No restriction to pointwise-invariant quotient actions was used. No permissible smooth alternative was omitted. QED.

This theorem is an elementary finite-quotient consequence of the preprint's exact extension criterion, not a newly discovered characterization of sections. It supplies a checkable *obstruction certificate* only. If a is in R_n, the result is inconclusive: a solution in a finite quotient need not lift to the surface group. Even testing many finite quotients without an exclusion would not prove existence of a smooth section.

For a concrete certificate one must supply:

1. Exact based words for the surface presentation, vanishing cycles, twist automorphisms, and actual cap class
2. A finite group and the images of the surface generators, satisfying the surface relator and generating G
3. Automorphisms sigma_i, with the intertwining identities rho psi_i = sigma_i rho verified on every surface generator
4. The complete finite sets in (2), and an excluded target a

The homology table of a monodromy factorization does not provide items 1 or 3.

## 3. Why local obstructions can disappear after adding positive factors

The relative example from turn 2 has one separating vanishing cycle v and boundary class v^2. A *different* critical-disk fibration with two identical positive vanishing cycles v,v has total monodromy tau_v^2. In the corresponding compatible identification, select epsilon_1=epsilon_2=1 and x_1=x_2=1. Since psi_1(v)=v, formula (1) gives alpha=v^2. That boundary class now has a smooth extension.

This is an explicit failure of persistence under adding a positive singularity. It explains why a relative obstruction alone cannot be treated as a global positive-relation counterexample. The new total monodromy is still not the identity, so this observation also does not settle the original question.

## 4. Additional global constraint from the killed-cycle quotient

Let Q be the quotient of the surface group by the normal closure of all vanishing cycles. Each twist acts trivially on Q: its modification of any transverse loop inserts conjugates of its vanishing cycle. If the product of chosen pointed twist lifts is Push(w), the product action on the surface group is conjugation by w, up to the fixed point-pushing convention. It follows that the image of w is central in Q.

Thus a nontrivial image in Q can be a global obstruction, but it must lie in the center. If Q is centerless, this particular killed-cycle obstruction vanishes automatically. That still does not establish a section: membership in a normal closure is weaker than the ordered smooth expression (1). The distinction is already visible in turn 2, where the relevant cycle becomes trivial after it is killed but smooth extension fails.

## 5. Actual genus-nine candidate and limitation

Baykur–Hamada's equation (14) supplies an actual point-pushing insertion and therefore an actual global residual after cyclically shifting the positive word, as recorded in turn 3. However, the complete based words for the 48 vanishing cycles and their actions have not yet been certified from Figures 22–24. No such words have been guessed from the homology table. Consequently (2) has not produced an exclusion for that fibration, and no general nonsection assertion follows from it.

The exact checker `turn_4_check.py` verifies the finite-set recursion in the Heisenberg group of order 27, including nontrivial automorphisms, against direct enumeration. It also verifies the single-factor versus two-factor central local example. These are algebraic controls of the algorithm, not a monodromy certificate for a positive identity relation on a closed surface.

## Checkpoint

Substantive author turns: **4/5**. Estimated completion toward the full target: **6%**. This turn gives a rigorous finite obstruction criterion that handles nontrivial quotient actions and all local smooth choices, and an explicit reason the relative obstruction need not survive added positive factors. The missing step is an actual positive identity relation with a fully certified global input and an excluded finite image, or a proof that every such global input satisfies the infinite-group criterion. Separate review of the partial results remains required.
