# Beurling transform annihilator witnesses

Problem 2307072 / AMR0227072; Hayman–Lingham Problem 7.72.

This AI-assisted proof and audit give explicit negative answers under the printed bilinear pairing and Beurling-kernel conventions. No novelty or historical priority is claimed. The packet has no external human review, peer review, or formal proof certification.

## Result

Let \(D\) be the unit disc and let \(N\) be the bounded functions annihilating every holomorphic area-integrable test function under \(\int_D v\phi\,dA\), with no conjugation on \(\phi\). Inputs are extended by zero outside \(D\), and the Beurling kernel has coefficient \(-1/\pi\).

For each integer \(m\ge1\), the polynomial

\[
v_m(z)=z^2\sum_{j=0}^{m-1}(1-|z|^2)^j
\]

belongs to \(N\) and has \(\|v_m\|_\infty=1\), while

\[
\|Bv_m\|_\infty=H_m=\sum_{k=1}^m\frac1k\longrightarrow\infty.
\]

Thus no uniform bound holds even on the polynomial subspace. Each individual polynomial in this family still has a bounded transform.

Separately, \(v(z)=z/\bar z\) for \(z\ne0\), with \(v(0)=0\), belongs to \(N\), has norm one, and satisfies

\[
Bv(z)=1+\log|z|^2\qquad(0<|z|<1).
\]

This transform is essentially unbounded, so the Beurling transform does not map all of \(N\) into \(L^\infty\). Its principal value at zero is not finite; the single exceptional point is immaterial to the almost-everywhere statement. Positive-area level sets establish essential unboundedness. Both calculated transforms vanish almost everywhere outside \(D\).

The proof handles all analytic \(L^1\) test functions, principal values, the zero-extension boundary, and the absence of boundary or origin point masses. The Cauchy transform is calculated directly, avoiding an unproved inversion ambiguity. The exact polynomial essential norm uses continuity and positive-area neighborhoods rather than an isolated point value.

## Historical and source limits

The [2018 arXiv manuscript](https://arxiv.org/abs/1809.07200v2), Problem 7.72, printed p.183 / PDF p.184, provides the definitions. Its statement that no progress was known is historical and is not evidence of present-day openness.

A secondary transcription of the later book reports credit to Volberg. That attribution remains primary-unverified. The publisher-hosted 2019 bibliography verifies that reference 52 is the Bañuelos–Janakiraman paper and is indexed to Problem 7.72; it does not verify the Volberg credit sentence or identify these particular witnesses. The chapter's full text was inaccessible. The inspected author-hosted Bañuelos–Janakiraman text discusses finite-p estimates and contains no explicit discussion of Problem 7.72 or these witnesses. The final AMS PDF returned HTTP 403 and was not inspected. No attribution to Volberg or to Bañuelos–Janakiraman of these particular formulas is made.

## Contents and integrity

- [PROOF.md](PROOF.md) is the complete standalone mathematical argument, byte-identical to the audited proof: 10,718 bytes, SHA-256 `e9d43de1562948d62264be2ddb40a68019dedcfd38406671a32608a47e05059b`.
- [AUDIT.md](AUDIT.md) records the mathematical checks and source limitations. Its mathematical-check section is preserved verbatim.
- [SOURCE_VERIFICATION.json](SOURCE_VERIFICATION.json) records public source URLs, exact PDF hashes and sizes, and the audit's inspection and access limits.
- [EDITORIAL_MAP.json](EDITORIAL_MAP.json) records exact editorial transformations without exposing removed text.
- [PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json) enumerates this closed six-file packet. It hashes the other five files; its own exact bytes are separately sealed during preparation.

The recorded 512 exact-rational checks for m = 1 through 64 passed in normal, `-O`, and `-OO` modes. They are ancillary finite checks, not formal certification of the all-m or analytic proof. Packet preparation rechecked artifact and PDF identities without repeating those checks or source inspections.

Only authored mathematics and public verification metadata are included. Copied source PDFs, extracted source text, source images, dataset contents, code, raw check tables, and private coordination material are excluded. A cryptographic match establishes byte identity, not mathematical correctness, historical attribution, or peer review.
