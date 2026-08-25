# Independent K3P cut-recovery audit

## Verdict

Primary item 6 cannot honestly pass. Its status is **BLOCKED**.

The exact missing JC certificate was recovered byte-for-byte and all 177
endpoint records, 453 single-blob records, 598 strict sign records, seven
partial Bernstein certificates, and 547 distinct factor expansions replay
exactly. The JC two-active elimination identities also pass.

The obstruction is the model-transfer step, not the recovered file. The
order-two K3P-to-CFN identity is exact only on Fourier coordinates supported
in $H=\{0,C\}$. The frozen JC proof uses the all-distinct coordinate
$P(C,G,T)$, which is outside $H$, in both its endpoint invariant and three
of its four decisive two-active minors. Those formulas do not become
$c$-only K3P formulas.

## Independent exact falsification of the projection route

The verifier reconstructs a literal frozen endpoint descendant-mask tensor:

```text
((0,0,0,4), (0,0,4,0), (0,0,4,4), (1,1,1,1),
 (1,1,1,5), (1,1,5,5), (2,2,2,2), (4,4,0,0),
 (4,4,4,4), (5,5,5,5))
```

With inheritance parameters $(1/6,1/2)$ and normalized edge parameters

```text
(3/4, 9/10, 2/3, 1/3, 3/4, 1/10, 1/2, 5/6, 1, 1/2),
```

the exact CFN endpoint values are

\[
(a,b,c)=\left(\frac1{160},\frac{25}{288},\frac{427}{3840}\right),
\qquad a-bc=-\frac{3763}{1105920}.
\]

Two identical endpoints and effective bridge
$z=6912/10675$ give wrong-split block determinants $(0,0)$ and total CFN
Fourier rank 2. This is realized with all physical parameters strict by using
endpoint central scales $9/10$ and actual bridge $1024/1281$.

Therefore an order-two projection of a noncut K3P configuration need not have
binary rank above the binary cut threshold. The claimed inference to K3P rank
at least five is invalid.

## What is and is not established

- PASS: exact dependency recovery and SHA-256 binding.
- PASS: internal exact replay of the frozen JC classification certificate.
- PASS: JC two-active polynomial identities.
- PASS: K3P-to-CFN polynomial-map identity on $H$-supported coordinates.
- FAIL: transporting the full JC endpoint/two-active proof through that identity.
- BLOCKED: pointwise K3P cut recovery throughout $\mathcal D_{3,+}$.

This audit does not disprove the full K3P cut theorem. A K3P-specific argument
could still show that the remaining $G,T$ character blocks force total rank
above four. No such exact certificate is present in the supplied chain.

## Replay

From `k3p_level2_identifiability_final/cut_recovery/` run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_cut_recovery.py --report verification_report.json
```

The program uses only Python's standard library and exits successfully after
reproducing the audit. Add `--require-primary-pass` for a fail-closed gate; it
exits nonzero while item 6 remains blocked.
