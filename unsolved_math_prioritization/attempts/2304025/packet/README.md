# Fuchs's weighted integer-polynomial infimum: exact initial ranges and an arithmetic reduction

Problem 2304025 / AMR-022-4025, Hayman–Lingham Problem 4.25.

**Partial result only. The original question for every real parameter remains unresolved by this packet.** These are unrefereed AI-assisted mathematical notes. No novelty or first-resolution claim is made.

Write

\[
F(\lambda)=\inf_{P\in\mathbb Z[z]\ \mathrm{monic}}
 \frac1{2\pi}\int_{-\pi}^{\pi}|1-e^{i\theta}|^{2\lambda}|P(e^{i\theta})|^2\,d\theta,
\qquad C(\alpha)=\frac{\Gamma(2\alpha+1)}{\Gamma(\alpha+1)^2}.
\]

The integral in the original question has infimum **\(2\pi F(\lambda)\)**.

The packet proves:

- \(F(\lambda)=C(\lambda)\) for \(0<\lambda\le1\).
- \(F(\lambda)=2C(\lambda-1)\) for \(1\le\lambda\le2\). For \(1<\lambda<2\), no polynomial attains the infimum; geometric sums approach it.
- \(F(m)=2m\) for integers \(1\le m\le6\), with explicit witnesses.
- For every positive integer \(m\), \(F(m)\) is an attained even integer, at least \(2m\). Equality holds exactly when there is a disjoint pair of distinct-element integer sets, each of size \(m\), whose power sums agree through exponent \(m-1\).
- Explicit higher-parameter bounds, including
  \[
  \frac{4C(\alpha)}{\alpha+1}\le F(2+\alpha)
  \le\frac{2(\alpha+2)C(\alpha)}{\alpha+1},\qquad0<\alpha<1.
  \]
  These bounds do not coincide. Their sharpness is not claimed.

The remaining task is a determination for arbitrary \(\lambda>2\), including an unrestricted treatment of the integer arithmetic minima. The packet does not assert that every individual parameter above 2 is open in the literature.

## Files and replay

- `PROOF.md`: complete proofs and exact remaining gap.
- `ATTEMPTS.md`: five substantive mathematical approaches and their outcomes.
- `SOURCES.md`: statement, source/priority boundaries, and classical attribution.
- `verify.py`: standard-library exact rational and integer sanity checks.
- `verification.json`: recorded deterministic output.

Run `python3 verify.py` from this directory. The program writes `verification.json`. It checks encoded finite identities, witnesses and bounded controls; the analytical proofs, infinite limits and universal inequalities are in `PROOF.md` and are not established by finite sampling.
