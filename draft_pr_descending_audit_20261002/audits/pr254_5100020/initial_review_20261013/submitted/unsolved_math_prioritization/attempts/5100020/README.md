# k403,a — origin-pedal/antipedal signed-area product

**Full first-turn candidate, independent review pending.** PROOF.md gives the odd least-period theorem for a strict confocal ellipse pair, including primitive stars and the circular case. Both areas belong to the original orbit. Every real antipedal intersection is finite; zero signed areas are permitted in the product.

The proof uses a rational support-line area identity and a two-pole meromorphic characterization. It accounts separately for coincident and opposite complex chord endpoints; the latter's pole class coincides with the vertex pole class only for odd period. An exact convex four-periodic negative control gives products225/4 and289/4 in the same family, so no even-period extrapolation is hidden.

Run:

```sh
python check_exact.py
python check_numerical.py
```

The first command uses SymPy1.14.0 and reproduces14,940 exact finite algebra/geometry/lattice controls. The second uses mpmath at95decimal digits and reproduces19,296 explicitly numerical diagnostics over72 primitive families; these are not interval certificates or a proof. The pole/divisor arguments are in the written theorem.

Classical Stachel/DLMF inputs and the prior reviewed campaign origin-pedal mechanism (5100012/PR204) are credited and restated self-contained. No historical novelty, proposer acceptance or human peer review is claimed. Earlier TURN_1_CHECKPOINT.md is preserved as a provisional checkpoint; this proof and the frozen manifest define the review version.
