# Substantive turn 5: the actual genus-nine test case and surviving obstruction gap

**Final author checkpoint: original question unresolved after 5/5 substantive turns. All partial claims await independent review.** Date: 2026-10-01. This turn tests the actual global candidate against the available algebraic obstructions rather than selecting arbitrary relative boundary data.

## 1. Exact integral cancellation for the actual point-pushing class

Use the explicit positive genus-nine relation of [Baykur–Hamada](https://doi.org/10.4171/JEMS/1326), Theorem 14 and equations (14)–(15). The accessed publisher online-first PDF has its own pagination; the relevant homology table is on pp. 34–36. Those pages, including all signs used below, were rendered and visually checked.

Write alpha_1,...,alpha_9,beta_1,...,beta_9 for the surface homology basis in their Figure 24. The abelianized point-pushing insertion has class

    s = alpha_2 + alpha_8 + beta_4 - beta_5
          + beta_6 - beta_7 - beta_9.                    (1)

Using the author's named vanishing-cycle classes, a short integral certificate is

    s = 2[a_3] + 2[a_3'] - 4[w_3] - [z_2] - [b_3]
          + [b_4'] - [b_4].                              (2)

For verification, set u=alpha_2+alpha_8 and v=alpha_4+alpha_6. The table gives

    [a_3]-[w_3] = u-beta_9,
    [a_3']-[w_3] = v-beta_9,
    [b_3] = u+v+beta_7-2 beta_9,
    [z_2] = v-beta_4+beta_5-beta_6,
    [b_4']-[b_4] = beta_9.

Substituting these five identities proves (2) in the integral lattice, not merely after tensoring with Q or reducing modulo a prime. The exact 18-coordinate data and coefficients are in `turn_5_homology_data.json`; `turn_5_check.py` verifies them.

The source's pointed relation is U Push(alpha) V=1. For the cyclically shifted positive word VU the chosen pointed product is Push(alpha)^(-1), so its residual has abelian class -s. The sign does not affect membership in the vanishing-cycle lattice.

By turn 1's correction formula, the genuine twist lifts can therefore be changed by independent point-pushing conjugations until their product lies in the commutator subgroup of the point-pushing surface group. Hence **no abelian quotient of this residual problem can exclude every allowed lift**: there is already one simultaneous choice killing its complete integral abelianization. In particular, using the Z/4 or Z/2 torsion in the total-space homology does not rescue this first-stage strategy.

This is an explicit certificate of the homological vanishing already established by Baykur–Hamada's longer calculation. Their Proposition 8 identifies this vanishing with primitive fiber class/pseudosection; it does not identify it with a genuine section. Equation (2) is not a newly discovered solution to their example.

## 2. The spin/intersection-form shortcut also gives no obstruction

The same source proves the total space is spin and its fiber class F has an integral algebraic dual D. Thus

    F^2=0,       D dot F=1,       D^2 is even.

Define the integral class

    S = D - (D^2/2 + 1) F.

Then S dot F=1 and S^2=-2. Therefore the even intersection form and primitivity of F do not forbid the algebraic numerical data of a negative-square section. Minimality of a spin symplectic manifold forbids exceptional (-1)-spheres, not every possible negative-square section.

No embedded sphere representing S has been constructed. An algebraic dual or pseudosection can have positive genus, and a homology class with these intersection numbers need not be represented by a section. This calculation rejects a numerical shortcut; it is not a geometric existence theorem.

## 3. Why the finite nonabelian test has not yet settled this example

The actual monodromy has 48 explicitly drawn vanishing cycles and a pictured point-pushing loop. To run the turn-4 finite obstruction test correctly, one still needs based fundamental-group words for those curves and the induced automorphisms, consistent with the cap identification. Their homology vectors do not specify their actions on a nonabelian quotient. In particular, replacing the true actions on a two-step nilpotent quotient by arbitrary symplectic linear lifts would discard precisely the central correction data being tested.

No such 48-factor nonabelian certificate has been completed here. No finite quotient exclusion of the actual cap class is claimed. Conversely, disappearance of the abelian obstruction, or membership in a finite quotient's allowed set, does not prove the infinite surface-group equation has a solution.

The narrow September 2026 seminar announcement remains insufficient to fill this gap. The complete April 2026 preprint supplies the exact local and disk extension criterion, but not a universal theorem solving every positive sphere-base factorization.

## 4. Five-turn outcome

The strongest retained, unreviewed partial work is:

1. Exact abelian correction coset under point-pushing conjugation, with full curve-lift coverage for nonseparating factors
2. A genus-two relative disk boundary condition with continuous but no smooth extension, certified by an integral Heisenberg quotient and including both separating-side choices
3. A no-go theorem for preserving that particular pointwise-invariant quotient through an essential positive genus-two identity completion
4. An ordered finite-quotient obstruction criterion allowing nontrivial twist actions and all smooth local alternatives; a proof that a local obstruction can disappear after adding a positive singularity
5. The concrete integral cancellation (2) and algebraic (-2)-dual calculation for the actual genus-nine global candidate

The main question is still unresolved: either exhibit a positive identity factorization whose *actual* cap class fails the smooth ordered criterion for every permitted individual curve lift, or prove that all positive identity factorizations satisfy that criterion. The relative disk example does not provide such a factorization. The restricted completion obstruction does not prove universal impossibility.

The OWR statement does not state a genus restriction; Korkmaz's earlier full version specifies genus at least two. Low-genus cases are standard and do not remove the higher-genus gap. Inessential curves yield trivial twists in both the closed and once-punctured mapping class groups and do not supply a counterexample. Nothing here concerns a boundary component fixed pointwise or a universal splitting of the Birman sequence.

**Proposed overall disposition: unsolved, 5/5.** Estimated full-target completion remains 6%. No sixth author proof-search turn is taken. Any public partial-result PR must wait for independent adversarial review of the frozen package, with prior theorem/preprint attribution and no novelty claim.
