# Centered unit-norm tight-frame endpoint experiments

This directory studies the additional hypothetical endpoint conditions
\[
\sum_{i=1}^{41}x_i=0,\qquad
\sum_{i=1}^{41}x_ix_i^{\mathsf T}=(41/5)I_5.
\]
Nothing here assumes that an arbitrary maximum kissing configuration must
obey either condition.

## Certified artifacts

- `circulant_triangle_psd_countermodel.json` and
  `verify_countermodel.py`: an exact order-41 matrix passing centered row
  moments, all ordinary harmonic row sums, and every principal Gram test
  through order three, but having a negative order-four principal minor.
- `centered_tight_bv_pseudodistribution.json` and
  `verify_centered_tight_bv.py`: an exact rational pair/triple
  pseudodistribution passing the centered/tight trace endpoint, every
  ordinary pair harmonic, every full-radial Bachoc--Vallentin block, the
  low-degree frame matrices, and 27 centered-skew rank cuts.  It is not a
  code.  It fails exactly four corrected exact-stratum common-pair
  capacity inequalities; the verifier audits and reports those failures.

Both verifiers use only Python's standard library and exact
`fractions.Fraction` arithmetic:

```sh
python3 experiments/centered_tight_frame_endpoint/verify_countermodel.py
python3 experiments/centered_tight_frame_endpoint/verify_centered_tight_bv.py
```

Current certificate SHA-256 values are

```text
ef9644c2ac645d6fa10b77e86bdf2f95743e0bab3612b4c93128ce66f603ba07  circulant_triangle_psd_countermodel.json
77f74f86eb0991a4abb96ec00512cdbe715437818b5fc2508bd719930912761f  centered_tight_bv_pseudodistribution.json
```

## Discovery-only artifacts

`search_centered_untf.py` performs floating-point projected optimization.
Its 16 recorded starts found a best maximum inner product of approximately
`0.537812703692`, not a kissing configuration.  Files under `results/`
are numerical solver checkpoints and are not imported by either verifier.

The mathematical interpretation and exact formulas are in
`proofs/centered_tight_frame_endpoint/README.md`.
