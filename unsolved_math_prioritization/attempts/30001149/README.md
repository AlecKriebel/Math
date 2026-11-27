# Weak almost-rational automorphisms: accepted order-four bridge and partial reductions

Problem 30001149, source alias OWR-3388-008, rank 1233. First substantive attempt, 1 of 5. The original all-primes, all-orders classification remains unresolved by this work.

## Accepted scope

Over an algebraically closed field k of characteristic two, let sigma be a k-automorphism of k[[t]] of exact order four. If sigma(t) lies in a degree-two Artin–Schreier extension E0/k(t) inside k((t)), then

    k(t,sigma(t),sigma^2(t),sigma^3(t)) = k(t,sigma(t)) = E0,
    [E0:k(t)] = 2.

This proves the weak-to-strong bridge only in that exact-order-four setting. The familiar resulting conjugacy class is the known Bleher–Chinburg–Poonen–Symonds class, not a new class or formula.

Two additional accepted partial theorems remain useful outside that restricted case:

- In characteristic two, every weak example of order 2^n with n>=2 has initial lower breaks (1,3) or (1,5).
- For every prime p, the full orbit field is Galois of degree p^r over each coordinate field. The complete interval-degree, fixed-group, pair-genus, orbit-genus and final-break bounds are retained. These reductions alone do not force r=1.

Orders 2^n with n>=3 and odd-characteristic orders p^n with n>=2 remain unresolved. No full classification or original-problem counterexample is claimed.

## Reading order and dependencies

1. [ORBIT_TOWER_PARTIAL.md](ORBIT_TOWER_PARTIAL.md): all-primes orbit/Galois/genus reductions.
2. [RAMIFICATION_PARTIAL.md](RAMIFICATION_PARTIAL.md): characteristic-two initial-break restriction.
3. [AUDIT_RAMIFICATION_TOWER.md](AUDIT_RAMIFICATION_TOWER.md): full independent audit, including quotient-length and expanded ramification arguments.
4. [ORDER4_R3_EXCLUSION.md](ORDER4_R3_EXCLUSION.md): standalone exclusion of orbit degree eight; it does not itself exclude degree four.
5. [ORDER4_WEAK_BRIDGE.md](ORDER4_WEAK_BRIDGE.md): exclusion of orbit degree four, using the orbit theorem and the separate r=3 proposition.
6. [AUDIT_ORDER4_BRIDGE.md](AUDIT_ORDER4_BRIDGE.md): full independent audit, including elliptic substitutions and the local Kummer argument.

The r=3 proof defines A_i using triple fields. The r=2 proof defines A_i using neighboring pair fields. These definitions are distinct and must not be identified. The ramification partial is not a dependency of the order-four bridge.

[SOURCE_LEDGER.md](SOURCE_LEDGER.md) gives public bibliographic identities and inspection history; [PROVENANCE.md](PROVENANCE.md), [STATUS.json](STATUS.json) and [MANIFEST.json](MANIFEST.json) describe this edition.

All proof and audit material is AI-assisted and unrefereed. Scoped mathematical acceptance is not external human peer review, formal proof-assistant certification, or historical novelty/priority certification. No new source inspection or exhaustive literature search is claimed for edition preparation. No queue or historical approach accounting is changed by this edition.
