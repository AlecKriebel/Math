# Metropolis chains on Cayley graphs: scoped partial answers

**Status: independently reviewed partial; full source record unresolved.**
Two of five substantive attempts have been used. Historical novelty is
unconfirmed.

The [separate adversarial review](review/REVIEW.md) passed without mandatory
corrections. All 992 independent exact checks reproduce. The frozen partial
retains its historical pending-review sentence so the reviewed bytes remain
unchanged. Human peer review has not occurred.

[PARTIAL.md](PARTIAL.md) gives the exact complete-graph spectrum, disproves
nonincreasing relaxation, rules out a universal comparison with the uniform
endpoint, and proves the decreasing upper bound (d(N-1)/p) for every
finite connected simple regular graph under the stated conventions.

The original page defines (0<p<1) and a uniform endpoint at zero but asks
about an undefined (\tau(\infty)). That comparison is explicitly held
unresolved. The proven comparison with (\tau(0)) is labelled as a
conditional interpretation, not silently attributed to the source.

Run `python verify.py` and compare stdout with
[verification.json](verification.json). All 14,121 exact rational controls
pass, including 63 complete flow decompositions. These checks support the
written proofs and do not replace them. The frozen `PARTIAL.md` must remain
beside the verifier because its hash is checked.

[SOURCE_AUDIT.md](SOURCE_AUDIT.md) records source definitions and the
endpoint limitation. No full-resolution, first-discovery, or human
peer-review claim is made.
