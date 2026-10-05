# Kirby Problem 3.72 / catalog 2870

**Unresolved after five substantive approaches. Both parts remain open in this investigation.**

The target is the kernel of the smooth integral-to-rational homology-cobordism
map. It asks for a countable infinite-rank free subgroup, and then a direct
summand. This is the modern K3 problem; Bowditch's answer to a differently
numbered 1997 convergence-group problem is unrelated.

- `PROOF.md`: complete authored reductions, conditional criteria, and precise gaps.
- `APPROACH_LOG.md`: five mechanisms and their stopping points.
- `SOURCE_GATE.md` and `sources.json`: primary-source scope, versions, inspection
  limits, and public verification metadata.
- `check_controls.py` and `controls.json`: standard-library exact controls.
- `STATUS.json`: explicit disposition and exclusions.

A useful checked obstruction is that the standard Dai--Hom--Stoffregen--Truong
infinite-rank direct summand has zero intersection with this kernel, by applying
the credited filtered-instanton independence criterion. It cannot be recycled
into a solution. Other partials explain the necessary 1- and 3-handles, paired
finite homology, rational-invariant blindness, and the extra requirements for
splitting. These are credited deductions and elementary reductions, with no
historical novelty claim.

Reproduce from this directory:

    python3 check_controls.py > /tmp/kirby2870_controls.json
    cmp controls.json /tmp/kirby2870_controls.json
    sha256sum -c SHA256SUMS

The 9,495 assertions are finite algebra diagnostics. They do not prove the
infinite topology or the external Floer-theory theorems. The full target is not
settled, and the packet is pending independent mathematical audit. No source
PDF, source extraction, dataset contents or private coordination material is
included in this author packet.
