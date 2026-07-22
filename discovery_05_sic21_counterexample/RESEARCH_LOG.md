# Discovery 05 research log

All times are UTC on 22 July 2026 unless stated otherwise.

## Starting observation

The 13-variable stable model from Exploration 03 has the form

```text
Psi(X) = X + H2(X) + B K(X),
```

where `H2` is quadratic, `K` has eight independent cubic components, and
`B` is a 13-by-8 rational matrix. The candidate was to retain the eight
factor variables without the final homogenizing coordinate:

```text
g(X,U) = (H2(X) + B U, -K(X)).
```

## Proof development

The block determinant gives

```text
det(I+s Jg) = det(I+s JH2+s^2 B JK) = det JPsI(sX) = 1.
```

The three certified source collisions lift as `(X,K(X))`; all map under
`I+g` to `(Psi(X),0)`, and their first coordinates are `0,1,-1`.

The initial temptation was to quote Zhao's homogeneous Theorem 3.7 directly.
That would be invalid because `g` contains the linear block `BU`. The repair
was to formulate Abhyankar--Gurjar inversion in the scalar-parameter
filtration for `T_t=I+t g`. With `A=-xi.g`, coefficient extraction gives

```text
[t^m] p(T_t^{-1}(Z)) = E(p A^m)/m!.
```

Taking `p=1` proves `E(A^m)=0`; taking `p=Z_1` and using the collision proves
that `E(Z_1 A^m)` is nonzero infinitely often.

## Exact verification

- Primary SymPy reconstruction: 21 coordinate pairs, 72 terms, total degree
  four, exact block-matrix identity, exact three-point collision.
- Direct low-order operator checks: `E(A)=E(A^2)=0`, `E(bA) != 0`, and
  `E(bA^2)=3*x^2*y`.
- Dependency-free Python/Fraction checker: sparse reconstruction, exact
  collision, and 66 determinant-pencil specializations.
- Independent Node.js/BigInt checker: exact collision and 18 determinant
  specializations.
- Deterministic JSON SHA-256:
  `ed5a5a2069da28905403d2dd5b709951a22b863455608b5b4f8a5c9bdb784286`.

## Priority audit

At **02:42:05**, the audit snapshot covered 29 post-announcement GitHub
repositories, exact and variant web/code searches, current MathOverflow and
arXiv results, Zhang's consequence page, and the primary Zhao and
Derksen--van den Essen--Zhao papers.

The first draft overstated novelty by suggesting that no earlier explicit SIC
witness existed. A self-audit caught the error before commit: Exploration
03's 22-variable cubic homogeneous map already implies an explicit SIC(22)
witness by Zhao's theorem. Thompson's 24-variable and Harrison's 79-variable
maps imply larger witnesses as well.

The corrected claim is only that the present certificate reaches dimension
21, one below the immediately available dimension 22, and that its
nonhomogeneous linear block is handled by the scalar-parameter lemma. No
minimality or guaranteed worldwide priority is claimed.

## Artifact status

The five-page PDF was built with Tectonic, rendered to images with Poppler,
and every page was visually inspected. The TeX log contains no overfull or
underfull box warnings.

## Typesetting clarification

An external review reported that Equation (5) appeared to begin with `2g_1`.
Inspection of the TeX, Markdown, sparse JSON, and rendered page showed that
all four already contained the intended coefficient-one formula

```text
g_1 = U_1 + (1/2)*a_1*b_1 + (3/2)*a_1*y.
```

The apparent `2` was the page-2 footer concatenated with the first formula on
page 3 by a PDF text extractor. The PDF layout now places an explicit
normalization sentence at the top of page 3, and the primary verifier checks
the exact formula in both human-readable sources to prevent regression.
