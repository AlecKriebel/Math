# Research log: third-color gate cycles

## 2026-07-28 00:35--01:15 PDT

- Read the accepted response-2SAT, physicalization, odd-connector, and
  original-edge incidence notes.
- Reparameterized every exact two-list port by its omitted color and a
  binary cyclic chirality.
- Proved that a tight virtual-rainbow gate is chirality equality and that
  a same-type connector contributes its path-length parity.
- Derived the type-word holonomy rule: ordinary cyclic type walks have an
  even number of reversal connectors, while a
  literal-to-complement closure reverses one connector sign and has odd
  holonomy.
- Built an exact one-guard SAT probe for the smallest two-gate return.
  The one-edge odd return was immediately UNSAT.  Its 11-clause core
  exposed a direct two-cap response fork.
- Generalized the core by hand.  The even-distance path-state lemma and
  one attack at the penultimate path vertex exclude every odd subdivision,
  yielding Theorem 4.4 and Corollary 4.5 in `NOTE.md`.
- Tested the overstrong claim that two tight gates sharing one physical
  port are always impossible.  It is false.
- Froze the exact equality control `MEXrtIdmdjLQqztC?` (canonical
  `MGEFK~cfJLBi]f]Z?`).  A standalone ordinary-set verifier checks
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3)\), its 172-state
  greatest eternal family, 1,892 attack obligations, both gates, and its
  two compatible chiral colorings.
- Removed transient SAT instances, models, and proof logs after the
  human theorem superseded the bounded UNSAT experiments.  The reusable
  discovery generator remains as `probe.py`.
- Exact remaining boundary: odd holonomy distributed across separated
  physical ports or several connector components need not contain the
  shared-port fork of Corollary 4.5.  No arbitrary-bicycle or universal
  \(k=3\) claim is made.
