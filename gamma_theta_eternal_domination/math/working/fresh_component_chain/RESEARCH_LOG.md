# Research log: fresh-component chain

## 2026-07-28 (PDT)

- Read the accepted C-069 response-2-CNF construction, C-079 physical odd
  fan and side-purity theorem, C-103 boundary parity theorem, C-120
  exact-two free-component theorem, C-124
  singleton-component polarization, C-129 first-clause theorem, C-133
  anchor-only bridge theorem, and C-140 bridge propagation gate.
- Checked the tempting global statement that C-140 makes the component
  propagation graph acyclic.  The sound conclusion is narrower.  The
  positive terminal \(t\) exposes one selected bridge \(z\) to every
  \(u\)-omitting component, so that one physical hub is side-pure
  everywhere.  C-079 does not synchronize the side choices made by
  distinct hubs.
- Proved that the C-140 turning ridge is disjoint from every free
  \(u\)-component: its defining \(H\)-edge to anchor \(w\) puts a singleton
  member in the fixed component, while an exact two-list member includes
  \(u\) and is absent from the projection.
- Wrote the exact shortest-trace normalization and audited both terminal
  color directions.  A return to a \(u\)-component can force the opposite
  orientation either through a \(\{u,w\}\)-source assigned \(w\) on the
  \(w\)-side or a \(\{u,v\}\)-source assigned \(v\) on the \(v\)-side.
  This prevented an incorrect same-type-only formulation.
- Applied C-103 to a return through a second \(\{u,w\}\)-vertex of the
  original C-133 bridge.  The source path \(z-t-y\) has even length in
  \(W_v\), while the target return path has odd length in \(W_u\).
  Therefore the two terminal boundary states cannot both be absent; if
  either is absent, the other is retained.
- Checked the equality graph `HEhbtjK` as the strict scope control for
  cross-hub coherence.  Same-list sources 3 and 8 are each exposed for
  frozen color 0 and see opposite sides 5 and 6 of one component.  Their
  own complement edge forces opposite source colors, so this refutes raw
  side synchronization under full equality without realizing an active
  same-color return.
- Reused the graph `HFzvvn{` with a newly restricted no-full family.
  Greatest fixed-point deletion after the exact direct-swap bans gives 52
  states and exact lists
  \(0,01,0,01,12,12\).  The two source ports are separately exposed and
  side-pure but hit opposite sides of the target component, producing a
  literal separated-port lollipop.  The standalone checker verifies all
  312 attacks and
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3)\).
- Ran the discovery-only cycle scanner over the 261,080 connected
  unlabeled order-nine graphs.  Among 1,380 eternal-equality graphs and
  16,122 independent references, 92 references had free singleton units
  and six had cross clauses, but none had both.  This was retained only as
  `OBSERVED`; it has no independent coverage audit and is not a promoted
  finite result.

## Frozen boundary

The proved result is local.  It excludes opposite-side return through the
same physical bridge and forces a retained boundary for a return through a
second original bridge vertex.  It does not exclude a terminal source in a
fresh component, does not turn the retained boundary into a contradiction,
and does not prove complete \(k=3\) or the universal conjecture.

Reproduction:

```text
python3 -I -B -W error \
  math/working/fresh_component_chain/verify_boundary.py

python3 -I -B -W error \
  math/working/fresh_component_chain/verify_equality_control.py
```

## 2026-07-28 — hostile-review scope correction

- Restricted the first-return normal form to traces that actually
  re-enter a previously visited component.  A two-unit contradiction can
  instead hit a separately pinned component without repeating a trace
  variable.
- Restricted the two displayed terminal color directions to binary cross
  clauses between exact-two-list endpoints.  Singleton sources can force
  the same target rows and are not covered by that classification.
- Corrected three internal equation references and the positive-marker
  wording.  The downstream bridge-to-bridge theorem already assumes an
  exact \(\{u,w\}\)-source and is unchanged.
