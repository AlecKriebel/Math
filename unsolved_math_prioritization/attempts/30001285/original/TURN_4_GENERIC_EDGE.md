# Author approach 4: the generic element and the missing filtered comparison

Aim: reduce a natural equality to one geometric class, then determine which spectral-sequence data would compute that class.

## Generic detection

Fix A/F, let G=SL_1(A), and let K=F(G). The generic point eta∈G(K) defines [eta]∈SK_1(A_K). For a common target Q=Q_{1,r}, let f and g be natural group invariants, and put

    omega=(f_K-g_K)([eta]) in Q(K).

Merkurjev's generic-evaluation theorem for group invariants with values in a cycle module identifies an invariant with a multiplicative unramified class on G. It applies here to the bounded-torsion submodule containing the values: the source is killed by d, so the difference takes values in Q[d]. Kahn Theorem 10.7 explains the same torsion passage for the unquotiented target; Wouters §2.1 describes the quotient cycle modules.

Thus omega is unramified and primitive, meaning that on G×G its pullback along multiplication is the sum of its two projection pullbacks. More importantly,

    f=g as invariants over extensions of F  iff  omega=0.

The forward implication is evaluation. The reverse implication is injectivity of Merkurjev's generic-evaluation map, applied after precomposing with G→SK_1(A); that precomposition detects the invariant because G(L)→SK_1(A_L) is surjective. This is an application of a credited structural theorem, not a claim that values on arbitrary individual rational points determine all field-valued invariants.

For the central unresolved comparison, the single class is

    omega_A=beta_1,K([eta])-sigma_1^1,K([eta]) in Q_{1,1}(K).

Neither of its two terms has been independently computed here. In particular, vanishing of omega after a splitting extension is insufficient by approach 3.

## What the spectral sequence determines

Kahn–Levine §6.9 uses

    E_2^{p,q}=H_et^{p-q}(F,Z(-q)) => K_{-p-q}^et(A).

For SK_1 the relevant edge value is at (p,q)=(2,-3), namely H_et^5(F,Z(3)). Its d_2 incoming source is (0,-2), namely K_2^M(F). Proposition 6.9.1 computes d_2^A(1)=[A], and the module structure computes its image as [A] cup K_2^M(F). For SK_2 the relevant value is (2,-4); d_2 comes from (0,-3), and d_3 can come from (-1,-2), namely H_et^1(F,Z(2)). The algebraically closed-subfield hypothesis makes this last image zero in the cited construction.

These computations fix the quotient targets. They do not compute beta on [eta]. Equality of the target groups or of their first differential is not equality of the homomorphisms into those groups.

Here is a precise sufficient route. Construct a morphism between the filtered objects used for the étale K-theory edge construction and the generalized Severi–Brauer construction, such that:

1. on the relevant input it is the tautological-module map applied to [eta];
2. on the identified edge quotient it is the specified identity (including sign and coefficient normalization);
3. it respects the filtrations and their incoming indeterminacies.

Then the edge invariants agree. Proof: a morphism of filtered complexes or towers induces compatible morphisms of exact couples and hence of each page and the abutment filtration. The edge assignment is the composition of passage to that filtration quotient with its inclusion into the identified permanent-cycle subquotient. Naturality of these two operations makes the edge square commute. Conditions 1 and 2 make its two routes the two asserted invariants.

This is an exact criterion, not a supplied construction. In this packet no morphism satisfying these conditions has been produced. An unfiltered map of K-theory objects, or the isolated computation d_2^A(1)=[A], does not certify condition 3.

## Coefficient-map warning in the geometric literature

Kahn §7.F discusses a flag-variety comparison and its tautological K-theory difference. We do not import its degree-four discussion as a claim that the natural quotient projection identifies sigma_2^1 with sigma_1^1. Suslin's displayed comparison in Kahn Theorem 4 uses a coefficient reduction arrow, and approach 1 rules out that simple quotient identity. Any use of the flag diagram in a full proof must explicitly reconstruct the arrows and their normalization. The current packet does not resolve that normalization issue or allege a corrected general flag theorem.

## Outcome and gap

The comparison is reduced to one explicit unramified generic class, or to a concrete filtered naturality construction that would kill it. Neither is evaluated or constructed. The reduction prevents a proof from being replaced by a target-group identification.
