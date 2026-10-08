# Turn 3: build compatible Sylow models and test globalization

## Attempt

The global character obstruction suggests assembling actions from Sylow subgroups instead of from one global representation. Here is an explicit family of fusion-stable complex characters of common dimension 12. It exhibits the local success and the precise missing smooth gluing step.

Let P2=<c,s> with c=(1234), s=(13). On S4 fixing the fifth letter, take W=epsilon times the three-dimensional reduced permutation representation. This is the usual orientation-preserving octahedral representation: the reduced representation has determinant epsilon, and twisting a three-dimensional representation multiplies that determinant by epsilon^3, making the product trivial.

Restrict W to P2. It splits into a two-dimensional dihedral plane representation and a line on which c acts as +1 and s acts as -1. Its character values are 3 at the identity, -1 on every involution, and +1 on the four-cycles. In particular it is constant on each S5 conjugacy class that meets P2. Both types of Klein four subgroup in P2 have zero W-fixed subspace. Every nontrivial cyclic 2-subgroup in P2 fixes one line.

Use the following actual complex representations:

    V2 = 4(W tensor_R C),
    V3 = 6(chi + chi^2) on C3,
    V5 = 3(psi + psi^2 + psi^3 + psi^4) on C5,

where chi and psi are faithful complex one-dimensional characters of the indicated cyclic groups. Their common complex dimension is 12. The nonidentity character values on C3 and C5 are respectively -6 and -3; therefore they respect every automorphism induced by S5. V3 and V5 have no fixed vectors for their nontrivial subgroups. V2 has no fixed vectors for either Klein four type. Thus the representations give p-effective, fusion-stable local data for every prime dividing |S5|.

The underlying real V2 has dimension 24. Its sphere has dimension 23; the fixed sphere for any nontrivial cyclic 2-subgroup has dimension 7. These are consistent with Turn 2: 24=3(8). The underlying real V3 and V5 also have dimension 24 and free actions on their unit spheres.

## Globalization test

There is no global complex S5 representation restricting to V2: any such representation would have zero invariants for both E_A and E_B, contrary to Turn 1. In particular matching dimensions and fusion-stable characters do not suffice to glue the models linearly. The problem calls for genuinely nonlinear geometry.

Existing orbit-category results do glue suitable local data at the CW level. The finite-CW S5 theorem is credited to Hambleton–Pamuk–Yalçın, not proved anew here. The general later classification in Hambleton–Yalçın, *Group actions on spheres with rank one prime power isotropy* (2017), also remains in the finite-CW category. S5 has no odd-prime Qd(p) section simply because its order has p-part at most p for p=3,5, whereas Qd(p) has p-part p^3. That group-theoretic eligibility provides no smooth structure.

## Exact gap

The displayed representations do not specify smooth strata, their normal-bundle gluing, an equivariant normal map, or vanishing surgery obstructions. No smooth sphere has been produced. Even the dimension 23 here labels the explicit Sylow representation spheres; it is not a claim that a smooth S5 action in dimension 23 exists, nor that a general realization theorem preserves this initial dimension.
