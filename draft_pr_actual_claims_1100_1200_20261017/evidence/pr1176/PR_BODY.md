## Variable-base universal extension refuted; fixed base 2 unresolved

This prose-only edition retains the complete substantive proof and independent
mathematical audit. No mathematical correction was required. The combined
problem is not declared solved.

Let P(X)=X^4-X^3-X^2-X-1, let gamma be its unique positive root, and define
c=1/((gamma-1)P'(gamma)), alpha=2c gamma^20, and beta=gamma alpha.
Then 1.92<gamma<1.93 and alpha/beta=1/gamma is irrational. Every indexed
term floor(alpha gamma^n) and floor(beta gamma^n), for n>=0, is even.
Every positive odd integer is omitted from finite sums of distinct positions.
Equal values at different positions remain usable separately and cannot
remove this parity obstruction.

The explicit trace recurrence has residue 1/3. Exact root/coefficient bounds
imply |E_m|<3(5/6)^m<1/6 for every m>=20, giving strict floor endpoints.
The shift 20 covers both exponent-zero terms. The historical independent
check also isolates the unshifted m=3 floor as the odd integer 1, emphasizing
why an unproved eventual-to-all-positions step would be invalid.

The original hypotheses permit beta=gamma alpha for irrational gamma.
At gamma=2 the corresponding ratio is rational and inadmissible. Therefore
this counterexample addresses the universal extension to 1<gamma<2;
it does not resolve the original fixed-base-2 question or classify all bases.
Original formulations and indexed-sum definitions were historically checked in
[Graham (1971), question 12, printed page 36](https://mathweb.ucsd.edu/~ronspubs/71_08_integer_sums.pdf)
and [Erdős–Graham (1980), printed page 58](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf).
Complete PDF retrieval is not asserted to mean cover-to-cover reading.

The positive multiplier and fractional-part mechanism are prior work of
[Dubickas, On the limit points of the fractional parts of powers of Pisot numbers (2006)](https://dml.cz/handle/10338.dmlcz/107991),
Theorem 4 and its proof. The all-even mechanism is in
[Dubickas, Even and odd integral parts of powers of a real number (2006)](https://doi.org/10.1017/S0017089506003090),
Theorem 1(iv); printed page 332 explicitly includes the exact quartic family
at d=5. No novelty or priority of this application, exhaustive literature
review, current authoritative open-status certification, or full solution
of the combined problem is claimed.

“Accepted” means an independent internal AI audit of the specified
counterexample. The AI-assisted work is unrefereed; no external human peer
review, journal acceptance, or formal proof-assistant certification is claimed.

Historical independent exact arithmetic passed 1,573 checks, including 1,024
trace values and 512 consecutive floor values, with byte-identical normal,
-O and -OO outputs. The checker used explicit exceptions and recorded
failure controls. These finite checks supplement the written all-future proof.
Four complete public source PDFs were independently re-retrieved and matched
by SHA-256 to inspected copies during the original audit.

The edition contains authored proof, audit, acceptance, public citations and
verification metadata only. Executable code, raw datasets, detailed receipts,
full computational certificates, copied PDFs/source text/images, and private
coordination material are excluded. It is not an executable reproduction
package. Preparation performed byte-integrity and publication-structure checks
without new mathematical tests or new scholarly-source retrieval/inspection.
The original candidate and audit remain unchanged.

Exactly eight files are additions under attempts/2070. QUEUE.md and all
unrelated paths are unchanged.

## Exact public-file identities

- `ACCEPTANCE.json`: 2,071 bytes; SHA-256 `50597310b03a4cf12b4ad15f9c09e98281a02ad2ebcaecbd386b6eedf54793a5`.
- `ACCEPTANCE.md`: 3,956 bytes; SHA-256 `ec7d3a4ad8bdf043e804d2865301c810a7f9f98f4e58bc9e5d6075eff9590955`.
- `AUDIT.md`: 12,889 bytes; SHA-256 `d92bf24c643a88a57984c4ffa93f57dac06aba0120e5235a41a1a61b17fea917`.
- `MANIFEST.json`: 1,700 bytes; SHA-256 `589983fc342b411f8d4997b5d3d2d3d5cd0b1c45471dc78625603d59111c0a24`.
- `PROOF.md`: 9,813 bytes; SHA-256 `d1763e7b4b40f59f69c00f18e75f283a0692db29fb9835f1af66ab5197554207`.
- `README.md`: 3,790 bytes; SHA-256 `1d8a2274ef7be44bbcef761c6eb5aceac09bc151e296d14224d2a2c487be5549`.
- `SOURCES.json`: 9,718 bytes; SHA-256 `9a43e899dbffe7c957faaaf67f4d2dcb40173b12f334892423428106a14c726e`.
- `VERIFICATION.json`: 2,663 bytes; SHA-256 `b6f5bfe5e428648fff3104fe4e138a352c5d8a8d1c35bb7492b8bd6c3175254e`.

MANIFEST.json lists all eight members and hashes the other seven; this body independently pins its digest.

