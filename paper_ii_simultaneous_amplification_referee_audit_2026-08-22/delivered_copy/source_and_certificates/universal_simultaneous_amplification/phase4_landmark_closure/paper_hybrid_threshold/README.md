# A fitness-independent family of simultaneous amplifiers beyond relative fitness 3/2

This folder contains the manuscript, paper-level exact audit, deterministic
release tooling, and human submission handoff for Paper II of the universal-
amplification workstream.

Let

\[
P(R)=R^6-8R^5+22R^4-30R^3+21R^2-6R+1
\]

and let `R_hyb=1.5028569127905696...` be its unique root in
`(3/2,151/100)`.  The paper constructs one fitness-independent family of
finite connected loopless undirected weighted graphs that eventually
amplifies every fixed `1<r<R_hyb` under both Birth--death and death--Birth
updating.  Consequently,

\[
R_{\rm sim}\ge R_{\rm hyb}>3/2.
\]

The endpoint is exact only among fixed positive response parameters in the
paper's displayed first-order dilute pair--pendant model.  The unrestricted
value of `R_sim`, and even a finite universal upper bound, remain open.

From this folder run:

```sh
./replay.sh
./build.sh
./release_bundle.sh
```

`all.sh` performs the exact replay and PDF build.  The deterministic PDF is
written to
`output/pdf/simultaneous_amplification_beyond_three_halves.pdf`.  The release
script creates
`output/release/simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz`.

The exact replay audits labelled finite-state lumping, the pair and pendant
response algebra, rational endpoint margins, and the sextic optimization.
The analytic weak-cut, establishment, cleanup, reciprocal-invasion, and sweep
estimates are proved in the manuscript; they are not machine-verified by
these finite certificates.  No sampled numerical calculation carries a
theorem quantifier.

For a fresh archive extraction, the single canonical bootstrap is
`bootstrap_replay.sh`.  It pins Python 3.14.6, SymPy 1.14.0, and SymPy's
numerical dependency mpmath 1.3.0.

DOI `10.5281/zenodo.21852072` is the public v1 source/software archive for an
earlier manuscript version in this same workstream.  This package is a major
superseding manuscript version and does not yet have a new DOI, bioRxiv DOI,
or journal publication.  No submission or external contact has occurred.
