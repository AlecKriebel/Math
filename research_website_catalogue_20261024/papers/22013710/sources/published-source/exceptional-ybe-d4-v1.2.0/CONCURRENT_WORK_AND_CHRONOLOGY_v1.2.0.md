# Concurrent work and public chronology — version 1.2.0

This record accompanies the public version-1.2.0 archival release. It
distinguishes verifiable public chronology from reported private chronology
and does not ask the reader, an editor, or a repository to adjudicate private
discovery priority.

## Publicly documented chronology

1. The GitHub release
   [`exceptional-ybe-d4-v1.1.0`](https://github.com/AlecKriebel/Math/releases/tag/exceptional-ybe-d4-v1.1.0)
   was published at **2026-07-28T04:10:58Z**. Its annotated tag currently
   peels to the content-addressed artifact commit
   `e2669c5b2f99338c79381dc42bdbc61ee8b963c3` (tree
   `0437907ddb593f478958e001d4c0e5e619abe97f`). GitHub reports the release
   itself as `immutable: false`, and the tag is unsigned, so this record calls
   it publicly timestamped and content-addressed rather than formally
   immutable.
2. A later repository-wide GitHub/Zenodo snapshot, Zenodo record
   [10.5281/zenodo.21753405](https://doi.org/10.5281/zenodo.21753405), was
   created at **2026-08-02T02:10:07.456855Z**. Its 455,860,954-byte repository
   ZIP (`md5:cb299903423d30c58f0eb9e807cfaeae`) contains the paths
   `exceptional_ybe_d4/main.tex`, the paper PDF, `verify_exact.py`, and
   `SHA256SUMS`. This unrelated repository-wide software record is only
   secondary corroboration; it is not the paper's citation record and must not
   be used as its DOI.
3. Galindo and Rowell's
   [arXiv:2608.16865v1](https://arxiv.org/abs/2608.16865v1), *Unitary
   Yang–Baxter Operators: Towards a Classification*, was submitted at
   **2026-08-17T17:47:15Z**. Their v1 source is SHA-256
   `b7bc3fb2d1906140247e7643d82fda2bb02ee6cc53e6367956a087fa96d814ab`.
4. The dedicated version-1.1.3 paper record is
   [10.5281/zenodo.21971507](https://doi.org/10.5281/zenodo.21971507), under
   concept DOI `10.5281/zenodo.21971506`. It remains an archived historical
   version. Version 1.2.0 is archived as a new version of the dedicated record
   under version DOI
   [10.5281/zenodo.22013710](https://doi.org/10.5281/zenodo.22013710); it does
   not overwrite or reuse the v1.1.3 version DOI.

The v1.1.0 public release predates Galindo–Rowell arXiv v1 by 20 days,
13 hours, 36 minutes, and 17 seconds. This establishes earlier documented
public disclosure, not private discovery priority.

## What the July release already contained

Direct inspection of the tagged source, its released PDF, and a fresh run of
the tagged verifiers confirms that v1.1.0 already contained:

1. the explicit class `[e^{iπ/3}, 1/2, 4]`;
2. the five-word Pauli–Clifford operator;
3. the `(M,E)` decomposition;
4. the reflection circle and complete 18-word certificate;
5. unitarity, the Hecke polynomial, and the Yang–Baxter equation;
6. rank eight and both scalar partial traces;
7. faithful localization of `H_n(3,6)` for every `n`;
8. minimum local dimension four;
9. the `4m`-dimensional amplifications; and
10. the `(3,2)`-generalized normal form.

The July exposition was terser about the reverse kernel inclusion, the tower
commuting square, the dimension-three trace calculation, and the distinction
between generalized tensor placements. Later versions expanded those points,
but the headline theorem and explicit construction were already public in
v1.1.0.

## Historical release hashes

- v1.1.0 PDF:
  `af4ff57c4b8c5cd37f47f8a6da880b4f93b9c22d6e2908a3ef1f6ebf5fb1d049`
- v1.1.0 source archive:
  `099995bdfd446169caab2e458e74b9808d0b02134708486bded4e3623459f45d`
- v1.1.0 checksum asset:
  `5f33ddb374327e980bef4f20e5c9df0cff67a827fdbfd9c2a265e105b48d8308`
- v1.1.3 PDF:
  `f119f7a33285f37017ed4c76a964ae6d6d17415e03c7503e9bc079f7a96a93bb`
- v1.1.3 source ZIP:
  `35ce31b52897cc623729aa787357a520deed04a01791c88dca019eccee54237a`

The live v1.1.3 Zenodo PDF and source ZIP match the repository artifacts. The
uploaded v1.1.3 `SHA256SUMS` has one harmless leading ASCII space not present
in the repository copy; its two checksum entries still validate. This
historical upload-byte quirk is recorded rather than altered.

## Independent concurrent work

Galindo and Rowell independently prove the same existence and strict
localization conclusion, with dimension four smallest in Lechner's exceptional
family, through a quaternionic twisted-group-algebra construction. Their
Section 13 literally uses

```text
P_Z = (I tensor Z) tensor (Z tensor I),
P_X = (X tensor I) tensor (X tensor X),
U = i P_Z,
V = i P_X,
R_GR = (i zeta / 2)(I + U + V + UV),  zeta = exp(pi i / 6).
```

Version 1.2.0 cites that paper prominently and proves an exact comparison with
the Pauli–Clifford representative after reversal of the two four-dimensional
sites and a common local basis change. It does not call the two formulas
inequivalent or claim that the reversal is necessary. Tensor-site reversal and
Garside conjugation extend the local identity to a same-word all-strand
unitary equivalence. It separately retains the older comparison with the
8-by-8 GHR Equation (5.2) generalized operator
`K_GHR^gen`.

Galindo and Rowell report having obtained and privately circulated their
construction earlier in 2026, including communication to colleagues in late
July. That statement is based on a separately preserved private record; it is
not stated in arXiv:2608.16865v1. No email contents or causal inference is
published here.

## Scope of the chronology claim

The public record supports the phrase **earlier documented public disclosure**.
It does not support an inference about private discovery or causation. The
revised paper treats the works as independent and concurrent and emphasizes
their different proof architectures.
