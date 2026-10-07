# Dependency ledger (initial)

| Input | Exact needed scope | Validation basis | Status / gap |
|---|---|---|---|
| Family142 main theorem | Complete factoring over F_p, uniform polynomial in (n+1)log p; multiplicities, binary p | Actual source at pinned adc7f124, hash manifest; independent proof audit underway | Uncertified: nontrivial odd-degree geometric division and analytic dependence |
| Family029 Theorem1.2 | Uniform zero-free half-plane for finite-order Hecke L-functions over arbitrary varying number fields | Actual statement and proof audit underway | Uncertified; family003 restricted field theorem insufficient |
| Family003 | Dirichlet and finite-order Hecke over Q(sqrt(-3)); potential optional nonresidue consequences | Source and actual Lean scope under examination | Does not directly supply family142 varying-field requirement |
| Berlekamp fixed algebra / trace pairing | B=ker(Frob_q-I) is K^r for squarefree f; trace coordinates separate K component values | Direct proof and feasible code underway | Conditional on prime factoring oracle |
| Shoup Theorem3.1 | Deterministic prescribed-degree irreducible construction reduced to prime-field factoring | Primary paper exact proof under independent audit | Scope/parameter dependence pending |
