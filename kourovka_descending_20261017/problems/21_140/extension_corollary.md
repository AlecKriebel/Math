# A further obstruction to removing F by taking extensions

2026-10-17 UTC. Candidate partial deduction, pending fresh adversarial
review. No novelty claim and no full answer to Kourovka 21.140.
Discovery estimate for the full problem remains 5%.

Assume the central-extension proposition proved in
approach_central_extensions.md: every central extension of a group
containing Thompson F contains F.

**Corollary.** In an exact sequence of abstract groups

    1 -> N -> E -> Q -> 1,

if Q contains a copy of F and Out(N) contains no copy of F, then E
contains a copy of F. No finiteness or torsion hypothesis on N is needed.

**Proof.** Restrict to the preimage of a chosen F subgroup of Q. Conjugation
gives a well-defined outer-action homomorphism F -> Out(N). The subgroup
F' is simple, and contains an isomorphic copy of F supported on a proper
dyadic interval. An injective map F' -> Out(N) would therefore embed F
there. The hypothesis rules this out, so simplicity forces the outer
action of F' to be trivial.

Let P be the preimage of F' in E, and put C=C_E(N) intersect P. For every
f in F' and every lift e in P, the automorphism induced by e on N is
inner. Choose n in N inducing the same inner automorphism. Then n^-1 e
centralizes N and still maps to f. Hence C maps onto F'. Its kernel is
C intersect N=Z(N). This kernel is central in C because every element
of C centralizes all of N.

Choose a subgroup F_0 isomorphic to F inside F'. The preimage of F_0
under C -> F' is thus a central extension of F_0 by Z(N). The central
extension proposition supplies a copy of F in that preimage, hence in E.
QED.

Equivalently, any extension that destroys all F copies from a quotient
which contains F must have Out(N) containing F. This is a necessary
condition for a proposed construction, not a proof that every quotient
embedding lifts directly. The new F copy can project onto a different
embedded subcopy of the originally chosen F.

For a finite kernel, Out(N) is finite and the condition holds. For a
finitely generated abelian kernel, the outer automorphism group equals
Aut(N), which is residually finite. No residually finite group contains F:
otherwise residual finiteness would separate a nonidentity element of
its infinite simple subgroup F', contradicting the absence of nontrivial
finite quotients of F'. For completeness, Aut(N) is residually finite
because any nonidentity automorphism moves an element of finitely
generated abelian N, and some characteristic finite-index subgroup
mN separates that displacement; the induced action on N/mN is finite.
One may choose m divisible by the exponent of the finite torsion part,
and then arbitrarily high multiples to separate any nontorsion
displacement. Thus these two common kernel families cannot remove F.

The sole new dependency is the central-extension proposition, whose
integral homology and arbitrary-coefficient steps are undergoing fresh
review. Standard structural inputs concerning F' are recorded in
approach_structure.md. No publication gate is opened by this corollary.
