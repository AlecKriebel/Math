# Attempt 5: Generalized decomposition numbers and cancellation

A recent primary-source result offers a more precise place to look for the missing top conductor. Linckelmann, arXiv:2604.01351v1 (1 April 2026), Theorem 1.1, proves for every generalized character χ that c(χ)_p is the conductor of its generalized decomposition numbers. Because these lie in p-power cyclotomic fields, some such number attains the top conductor.

For a p-element u and a commuting p′-element s, the decomposition formula is

χ(us)=Σ_(φ∈IBr(C_G(u))) d^u_(χ,φ) φ(s).

At s=1 it becomes

χ(u)=Σ_φ d^u_(χ,φ) φ(1).

The theorem controls the separate d-coordinates. The original question instead concerns these degree-weighted sums. A coordinate of conductor p^a does not force a sum of conductor p^a. The missing assertion is a noncancellation theorem using global irreducibility and p′-degree.

## Explicit cancellation, with all hypotheses honestly tracked

The ordinary reducible character Ψ of Attempt 3 gives an exact model. For G=C_(p^2)×C_q and u=x, the Brauer characters of C_G(x)=G are μ^j, inflated from C_q. The relevant generalized decomposition numbers are

- d_(Ψ,1)^x=1+ζ_(p^2),
- d_(Ψ,μ^j)^x=ζ_(p^2)^(1+pj) for 1≤j≤p−1,
- all other coordinates are zero.

Each coefficient for j≥1 has conductor p^2. Their degree-weighted sum is nevertheless Ψ(x)=1, since the p primitive-root terms cancel. At u=x^(pt) the sum belongs to Q_p. Thus Linckelmann's conductor theorem is consistent with a loss of the entire top level upon restricting a p′-degree ordinary character to P. The obstruction is real, but the example is reducible and does not disprove the actual conjecture.

## A limited conditional gain

For odd p, if one can choose a conductor-detecting p-element u such that C_G(u) is a p-group, then IBr(C_G(u)) consists only of the trivial Brauer character. There is a single decomposition coordinate and d^u_(χ,1)=χ(u). It follows that c(χ(u))=p^a. Since Q(χ(u))⊆Q(χ_P)⊆Q_(p^a), the cyclic Galois criterion from Attempt 1 proves the desired prime-to-p index. This condition is sufficient, not known here to hold in general.

For p=2, even a conductor-detecting scalar sum does not by itself force Q_(2^a): the real field Q(√2) warning from Attempt 3 still applies. An additional field-generation argument is required.

## Verification and stopping point

The exact verifier does not approximate roots of unity. It uses linear-character exponent multiplicities to calculate the Galois stabilizers, conductors, and extension indices. It checks the reducible cancellation examples, the binary conductor-only warning, the degree<p proposition on modest finite cyclic test sets, and the proper-subgroup induction congruence on cyclic p-groups. These are sanity checks for stated finite instances, not proof of the general irreducible case or an exhaustive character-table search.

The latest sources inspected still formulate the general statement as a conjecture. The newer conductor theorem does not remove the cancellation obstacle. After five substantive approaches, neither a complete proof nor an irreducible counterexample has been obtained.

Final status: UNSOLVED, 5/5. Public claims should be limited to the source correction, known-case recovery, fully proved limited propositions, exact reducible obstruction examples, and the explicit unresolved step. No new-resolution or priority claim.
