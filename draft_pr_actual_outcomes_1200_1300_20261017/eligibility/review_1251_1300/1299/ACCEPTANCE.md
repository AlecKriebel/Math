# Acceptance of the qualified degree normalization obstruction

## Decision

Accepted on 11 October 2026 for problem 30004270: the explicit modern-normalized valuation on the standard homogeneous coordinate ring of the projective line supplies a normalization-dependent obstruction to applying the unweighted LS semigroup formula with arbitrary-degree extremal functions.

This acceptance covers the complete proof in `PROOF.md`, the accompanying independent mathematical audit in `AUDIT_REPORT.md`, and the bounded source checks in `SOURCE_MANIFEST.json`. It is not an acceptance of an unconditional refutation of the historical 2019 conjecture.

## Accepted mathematical statement

Let the strata be the standard projective line and the point [0:1], with the full ordinary-graded ring C[x,y] and extremal functions x² and y². Both bonds in the modern cone construction are two, and the edgewise rational-root condition is witnessed by x/y. For a nonzero homogeneous polynomial of degree d whose least x exponent is i, the explicitly normalized valuation is (i/2,(d-i)/2). Its complete homogeneous semigroup is (1/2)Z²≥0. In particular, x has value (1/2,0), which fails the unweighted integer-total condition.

The proof also establishes the exact weighted description for this example and both degree-one controls. Replacing the extremal functions by x and y in C[x,y] gives the nonnegative integer lattice. Keeping x² and y² but changing to the quadratic-Veronese coordinate ring C[x²,xy,y²], regraded in degree one, gives precisely the half-integral points with integer coordinate total. The element x is absent from that latter ring.

## Required scope boundaries

The original 2019 Oberwolfach contribution announces a modified valuation without fully specifying its arbitrary-degree normalization. The inspected sources do not identify that announced convention in every arbitrary-degree case with the later extremal-function-normalized construction. The historical conjecture therefore remains unresolved by this report under any unspecified intended convention.

Neither the flag-variety claim nor the modern LS-type theory is refuted. Definition 2.9 in the cited 2025 arXiv revision explicitly requires degree-one extremal functions. No general repaired-conjecture proof, general weighted sufficiency theorem, novelty claim, or exhaustive literature conclusion is accepted here. The two repairs are proved only in the explicit projective-line example. The general weighted degree identity is used only as a necessary condition.

## Preparation and verification

The accepted frozen proof had SHA-256 `75939a20da6fa3eadd3ec1c0732590443ad96d830e4d09a0e6e5e745314033ed` and 11,292 bytes. The only changes to its text remove the stray comma from the lattice exponent at original lines 8 and 111. `TYPESETTING_EDITS.json` records both exact replacements, byte offsets, and original and corrected hashes. No mathematical sentence, conclusion, or qualification was changed. The audit report and source manifest remain byte-identical to their accepted versions; the audit manifest updates the corrected proof pin and records this provenance.

All four original public artifact pins, all five cited source-PDF pins, the recorded non-PDF retrieval response, the frozen candidate pin, and the upstream input pins were rechecked. The existing closed research-packet verifier passed in ordinary, -O, and -OO Python modes. The source record remains bounded to its stated versions and retrieval history. During this preparation the 2019 valuation announcement and semigroup/conjecture page, and the modern degree-one LS-type definition, were visually reinspected against the retained primary-source page images.

Fresh exact-arithmetic checks cover 3,272 nonzero homogeneous polynomials, 441 monomial exponent pairs, and 7,921 rational-coordinate pairs, including both degree-one controls. Their aggregate results appear in `CHECK_RESULTS.json`. These checks support the algebra; the complete proof is the symbolic derivation in `PROOF.md`, not finite enumeration.

## Publication boundary

This packet contains authored mathematical exposition, audit and acceptance reports, exact typesetting-change metadata, bibliography and source-verification metadata, and aggregate input/check metadata. It contains no source PDFs or copied source extracts, dataset contents, executable scripts, private sources, personal data, or private coordination records. `MANIFEST.json` gives the closed public file set and hashes. This preparation performed no repository publication or queue edit.
