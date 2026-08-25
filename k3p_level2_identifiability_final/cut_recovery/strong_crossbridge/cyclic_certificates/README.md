# Cyclic six-minor K3P certificates

This package gives exact certificates for target directions

`107, 111, 117, 119, 177, 183, 189, 190, 191, 192`

in the graph-derived one-active wrong-split universe.  It recompiles each K3P
map from the frozen graph certificate.  No four-port collision classification
is imported.

For each target and each sector `s` in `{C,G,T}`, the bundle selects two
flattening minors `F_s,H_s`, one spectrum `x_s` of a common distinguished edge,
the other spectra `y_s,z_s`, an inheritance parameter `lambda_s`, and a
strictly positive monomial `Q_s`.  Exact sparse integer arithmetic proves

```text
y_s*z_s*(oriented F_s) + x_s*(oriented H_s)
  = Q_s*lambda_s*(1-lambda_s)
      *(y_s-x_s*z_s)*(x_s*y_s-z_s).
```

If the wrong-split flattening had rank at most four, all six selected minors
would vanish.  The identity would force `x_s=y_s/z_s` or `x_s=z_s/y_s` for
every sector.  With `U_s=-log(x_s)>0`, this says each of the three `U_s` is the
absolute difference of the other two.  Taking the largest `U_s` is an
immediate contradiction.  The proof uses only that every edge spectrum and
inheritance lies in `(0,1)`, so it applies throughout the strict principal K3P
domain (and the strict continuous-time subdomain).

The producer searches exact coefficient dictionaries.  The verifier does not
import the producer: it independently rebuilds the descriptors, minors,
monomial factors, and both sides of all 30 identities.  It also cross-checks
the three target-117 identities field by field against the pre-existing
independent record-39 audit.  Its adversarial mode rejects 40 mutations, one
identity mutation for every sector of every target plus ten structural/input
mutations.

From the project root, replay with:

```bash
.venv/bin/python cut_recovery/strong_crossbridge/cyclic_certificates/generate_cyclic_certificates.py
.venv/bin/python cut_recovery/strong_crossbridge/cyclic_certificates/verify_cyclic_certificates.py --mutations
.venv/bin/python -O cut_recovery/strong_crossbridge/cyclic_certificates/verify_cyclic_certificates.py --mutations --report cut_recovery/strong_crossbridge/cyclic_certificates/OPTIMIZED_VERIFICATION_REPORT.json
.venv/bin/python cut_recovery/strong_crossbridge/cyclic_certificates/build_manifest.py
```

The first command is deterministic discovery/production.  The second and
third are the promoted exact replay gates.  The last command binds the package
after a successful replay.
