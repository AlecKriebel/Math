# Reproducible checks and their limits

Run `python check_exact.py`. It uses only Python's standard library and
passes 3,439 exact Fraction assertions. It checks exponential-assembly
normalization by complete ordered-composition enumeration through n=10
for two rational weight families; factorial and marked factorial moments;
simplex monomial factors; the exact geometric prefactor ratio; the
rational Chernoff-exponent lower bound; and Euler/binomial identities.
The deterministic output is `exact_receipt.json`.

The optional `OPENBLAS_NUM_THREADS=1 python diagnose_model.py` uses the
already available NumPy/SciPy and evaluates ideal-model Beta marginals.
`numerical_diagnostics.json` records its output and package versions.
For g=101,1001,4001, the ideal expected count in the requested window is
approximately 0.37465, 0.35477, 0.35060, approaching the predicted
log(2)/2=0.34657. These are floating-point diagnostic values, not certified
enclosures, sampled geometric surfaces, or evidence replacing a proof.

Neither checker proves the asymptotic theorem or the external geometric
inputs. Those must be reviewed analytically in `CANDIDATE.md` and the
primary papers. Particular review points are the uniform whole-mixture
comparison, k-tail moment control, slowly diverging mesoscopic scales,
Gamma normalization, and the order of the N and g limits.
