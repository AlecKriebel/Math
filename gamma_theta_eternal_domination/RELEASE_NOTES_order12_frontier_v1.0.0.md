# Gamma-theta conjecture: certified order-12 frontier v1.0.0

This release publishes one current paper and its exact reproducibility
archive:

> Alec Kriebel, *A Certified Order-Twelve Extension of the
> gamma-theta Frontier in One-Guard Eternal Domination* (17 pages,
> 26 July 2026).

## Result and exact boundary

Assume MacGillivray, Mynhardt, and Virgile's published exhaustive result that
there is no counterexample through order 11.  Then no finite simple graph of
order at most 12 satisfies

```text
gamma(G) = gamma-infinity(G) < theta(G).
```

Equivalently, every counterexample, if one exists, has order at least 13.
Here `theta` is the clique-cover number, equivalently the chromatic number of
the complement, and `gamma-infinity` is the standard one-guard-moves eternal
domination number.

This is a finite frontier result.  It is not a universal proof, a
counterexample, a lower bound of 14, or an independent re-enumeration of all
graphs at orders 10 and 11.  The universal conjecture remains open.

## Proof architecture

- Common parameter 3 is excluded by a complete odd-hole template split and
  independently replayed proof certificates.
- Common parameter 4 is excluded for connected order-12 graphs by an exact
  18,381-variable graph-to-CNF theorem and a checked 228,381,671-byte LRAT
  refutation.
- Common parameter 5 is excluded analytically by a simplicial
  closed-neighborhood reduction and the McCuaig-Shepherd domination bound.
- Classical parameter and component reductions prove that these are the only
  possible order-12 cases.

## Reproduce

From `gamma_theta_eternal_domination/`, verify all theorem bindings and replay
the decisive LRAT proof without invoking a SAT solver:

```text
python3 -I -B repro/c050/replay.py --full
```

Expected verdict:

```text
VERIFIED_ORDER12_FRONTIER_BINDINGS_AND_EXACT_LRAT
```

The accepted order-13 complement-`C9` template exclusion is separately
replayable with:

```text
python3 -I -B -W error repro/c057/replay.py
```

That second claim is included as current campaign context; it is not part of
the order-12 theorem and does not complete order 13.

## Release hashes

```text
b35d4bd795ddfbfa61be18bdd60ddb6d23492b0a63a7449e2ec0190170e6e9d2  paper/order12_frontier/main.pdf
e3b093085bafd124c228a29ef98c86341a45316dc02e11b565a138afe983d57a  results/order12_frontier_acceptance.json
14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7  instances/order12_k4_connected_doublelex/instance.cnf
edc0f6b76bc96b2b26677f399566ae437cc47a6fc0cc921eaff81d77b72a50da  certificates/order12_k4_doublelex_seed0_lrat_publication/proof.converted.lrat.zst
```

## Authorship and verification status

Alec Kriebel is the author.  The research, programs, certificate design,
audits, manuscript, and publication materials were developed with heavy
assistance from ChatGPT 5.6 Sol under his direction.  No outside individual
was contacted, and the result has not been peer reviewed.  Exact certificate
checking is evidence about the encoded finite statements, not independent
expert validation or proof of worldwide priority.

Public pages:

- <https://aleckriebel.github.io/Math/research/gamma-theta-conjecture/>
- <https://aleckriebel.github.io/Math/papers/gamma-theta-order-12-frontier/>
