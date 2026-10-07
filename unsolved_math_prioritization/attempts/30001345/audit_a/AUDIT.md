# Independent mathematical audit: multibranch rough-M counterexample

## Verdict and exact target

**ACCEPT for the explicitly stated, unrestricted reduced multibranch scope.** No mathematical correction is required for the frozen proof. Its family is flat and reduced, has a finite simultaneous normalization, retains all singularities inside one fixed transverse-boundary representative, and is total-delta-constant. The summed invariant defined by `K·(K+D)` increases from 7 on the central fiber to 12 on each sufficiently small noncentral fiber.

This is **not** acceptance of a resolution of the unibranched parametric conjecture, a sectionwise delta-constant assertion, a general fine-M conjecture, or a novelty claim. Those exclusions are essential to the verdict and agree with the proof's own exclusions.

Audited object: problem 30001345, frozen version 2.

- `PROOF.md`: 16,696 bytes; SHA-256 `561b189c2091eaeccccf89fdd933b2300ec676a871d7229ebfaf8c806962fe8b`
- `FROZEN_MANIFEST.json`: SHA-256 `199dc44fdb8de8f37024d170e6246281e1a7b6b5b7e1cdd94a21f4a1b195e478`
- All five files listed in that manifest were checked against their recorded lengths and hashes.
- Audit date: 2026-10-07 UTC.

The audit was conducted independently, without reading another review or acceptance report and without using helpers. The primary mathematical construction and a separate exact checker were worked through before reading the frozen written proof. The frozen proof was subsequently read in full. No files were published.

## 1. Arrangement, affine chart and exact equation

Set `w^2+w+1=0`. The nine projective linear forms are

- `X-qY`,
- `Y-qZ`,
- `Z-qX`,

with `q` ranging over the three cube roots of unity.

Each group is a pencil of three distinct lines whose common point is a coordinate vertex. The vertices do not lie on the other six lines. An intersection between the first and second groups is `[w^(i+j):w^j:1]`. It lies on exactly the line `Z-w^(-i-j)X=0` in the third group. These nine points are distinct, have nonzero coordinates and are separate from the three vertices. This enumerates all intergroup pairs. The twelve triple points account for `12·3=36` pairs, exactly the number of pairs of nine lines. There is no additional double point, higher-multiplicity point or isolated singularity away from these intersections.

The linear form `L=X+2Y+4Z` is nonzero at all twelve points. At the vertices it has the respective values 1, 2 and 4. At each mixed point its absolute value is at least `4-2-1=1`. The chart `L=1` consequently contains every intersection. No pair of its affine lines is parallel: otherwise its projective intersection would lie on `L=0`.

Substituting `4Z=t-x-2y` gives the displayed family

`F=(x^3-y^3)(64y^3-(t-x-2y)^3)((t-x-2y)^3-64x^3)`.

The three sets of factors are exactly

- `x-qy`,
- `qx+(4+2q)y-qt`,
- `-(1+4q)x-2y+t`.

For nonzero t this is the affine chart arrangement scaled by t. At zero it is the union of nine lines through the origin with pairwise different directions. Therefore all fibers are reduced; the central fiber has exactly one singularity, an ordinary ninefold point; and each noncentral fiber has exactly twelve ordinary triple points in the full affine plane.

The independent standard-library checker reconstructs the incidence set, all 36 nonzero spatial-direction determinants, the chart points and the complete polynomial factorization over the exact number field `Q[w]/(w^2+w+1)`. It does not read the author's checker or its results. Its checks also verify that the cubic initial part at each noncentral singularity is a nonzero scalar times three distinct linear forms.

## 2. Flatness

The x-degree of F is nine and its leading coefficient is the constant -65. Thus `-F/65` is monic in x. The quotient `C[x,y,t]/(F)` is free of rank nine over `C[y,t]`, with basis `1,x,...,x^8`, and consequently flat over `C[t]`.

This polynomial argument is not being used to skip the analytic issue. At an arbitrary point of the total family over `t=t0`, work in the ambient convergent-power-series local ring. It is factorial. The local equation is, up to a unit, a product of some of the distinct linear plane equations. None is a multiple of `t-t0`, because every component projects nontrivially and smoothly to t. If `(t-t0)h` is divisible by that product, each factor must divide h, so their product divides h. Thus `t-t0` is a nonzerodivisor in the local quotient. The quotient is torsion-free over the one-dimensional regular local base `C{t-t0}` and is therefore flat. This applies after restriction to the open ball.

The total space is also reduced, since its nine defining linear factors are distinct. The description as a reduced flat family is justified scheme-theoretically and analytically, not merely by counting visible points.

## 3. Finite simultaneous normalization

The total space has nine irreducible plane components. Each defining form has a nonzero x-coefficient: the coefficients are 1, q and `-(1+4q)`, respectively. The last cannot vanish since `|q|=1`. Each plane is therefore isomorphic to `A^2` with coordinates `(y,t)` and projects smoothly to the base.

Let R be the coordinate ring of the total family and let S be the product of the coordinate rings of those nine planes. S is a finite R-module, being the direct sum of nine cyclic quotient modules. The map `R -> S` is injective: the intersection of the nine distinct principal prime ideals is their product. R and S have the same total ring of fractions, namely the product of the nine component fields. S is normal. It is integral over R, and an element of the common total ring integral over R is also integral over S; it therefore belongs to S. This proves that S is precisely the integral closure of R.

Specializing to any parameter leaves nine distinct line factors, including at zero. The specialized normalization map is the disjoint union of the smooth line components, which is exactly the normalization of the fiber. Thus the stronger simultaneous-normalization assertion holds. It is not merely a normalization of the total space that might behave incorrectly upon specialization.

Finiteness and the local normalization description persist on the analytic restriction and on the inverse image of the open ball. No holomorphic product assertion for the closed Euclidean disks is necessary. The normalized total space over the open parameter disk is smooth over that disk, and each normalized restricted fiber consists of nine disks.

## 4. Fixed representative and boundary

The proof specifies the unit ball and `|t|<1/4`; those constants are valid.

The three vertex coordinates in the affine chart are `(1,0)`, `(0,1/2)` and `(0,0)`. At each of the nine other points the sum of squared moduli of the chart coordinates is at most 2. Thus every scaled intersection has norm at most `sqrt(2)|t|<sqrt(2)/4<1/2`. Every singularity is retained in the representative. No pair intersection occurs near its boundary.

For a line `ax+by+ct=0`, its distance from the origin is `|ct|/sqrt(|a|^2+|b|^2)`. For the three kinds of factors this distance is, respectively, zero, at most `|t|/sqrt(5)`, and at most `|t|/sqrt(13)`. In particular all nine distances are less than 1 throughout the parameter disk.

Write a point on one line as `p(t)+u v`, where p(t) is its closest point to zero and v is a fixed unit complex direction vector. The orthogonality gives squared norm `||p(t)||^2+|u|^2`. Its intersection with the closed unit ball is a genuine disk, and the radius function has no critical point on its boundary circle. This proves transversality to the sphere. The circles are pairwise disjoint because all line intersections are in the ball of radius 1/2. Therefore the entire reduced fiber is smooth and transverse along its boundary.

The closest point depends smoothly on t as two real variables, and the circle radius is `sqrt(1-||p(t)||^2)>0`. The nine circle embeddings thus vary smoothly without intersections. Restriction to any parameter path gives an isotopy of boundary links. The central curve is homogeneous and has no singularity other than the origin, so radial scaling identifies its unit-sphere intersection with its link on any smaller sphere. A smaller representative of radius rho is obtained by scaling x, y and t together, with parameter bound `|t|<rho/4`.

This establishes the locality and boundary conditions directly. Merely observing affine scaling would not have established them, but the frozen proof supplies the needed argument.

## 5. Delta and the precise rough invariant

For an ordinary r-fold point, each branch is smooth, and each distinct pair has intersection multiplicity one. The normalization-length identity for a reduced product gives

`delta = r(r-1)/2`.

The exact sequence written in the proof has the correct kernel and cokernel: the map from `O/(f) + O/(g)` to `O/(f,g)` is the difference map; the kernel is the image of `O/(fg)` because `(f) intersect (g)=(fg)`. Comparison with the separate branch normalizations yields the stated additive delta formula.

For r at least three, a single blowup is the minimal embedded resolution. Its unique exceptional curve E has square -1, and the strict transform C' has intersection r with E. The local canonical class supported on E is K=E, since `(K+E)·E=-2`. Hence, with the precise convention `D=C'+E`,

`K·(K+D)=E·(C'+2E)=r-2`.

There is no missing multiplicity coefficient in D and no branch-count shift in this computation. For r=3 the value is 1, and for r=9 it is 7. Both are directly obtained from the minimal embedded resolution required by the sources.

It follows that the central delta is 36, while the nearby sum is `12·3=36`. The central rough invariant is 7, while the nearby sum is `12·1=12`. Upper semicontinuity of the sum would require the latter to be at most the former, so the strict failure has excess 5.

The relevant delta-constant condition is the total over the representative. Along the distinguished origin section alone, the nearby singularity is a triple point with delta 3, so a sectionwise delta-constant assertion would be false for this example. The proof explicitly uses the summed convention and does not make that assertion.

## 6. Primary-source interpretation

The following scope checks were made on primary publications, including visual inspection of the relevant rendered pages rather than reliance on OCR alone.

**Oberwolfach:** Borodzik's contribution, printed p. 2446, defines the rough invariant through `K(K+D)` and formulates Questions 2 and 3 without an irreducibility or unibranched qualification. Question 3 adds delta constancy. Printed p. 2447 separately sets up multiple nearby singular points in a fixed ball and compares their summed invariants; its signature estimates then impose additional restrictions. Thus the frozen proof's unrestricted, summed reading is supported, while no inference about an unstated intended restriction is warranted. The contribution's signature theorem does not apply to the present ordinary triple-point fibers. [Official report](https://ems.press/content/serial-article-files/46242?nt=1)

**Published paper:** Definition 2.1, printed p. 575, makes parametric deformations both rational and unibranched. Definition 3.3, p. 576, uses the displayed rough invariant for potentially multibranch singularities. Remark 3.4, p. 577, warns of a different branch-dependent normalization, and Definition 3.5 distinguishes the fine invariant. Conjecture 3.8, also p. 577, explicitly assumes a parametric deformation. The present central fiber has nine branches and consequently fails that hypothesis. These facts require the scoped verdict above; the frozen proof states them correctly. [Published article](https://ir.library.osaka-u.ac.jp/repo/ouka/all/50809/ojm51_03_573.pdf)

The classical dual Hesse attribution is also consistent with Proposition 3.1 of Roulleau and Urzua's paper. The proof does not depend on trusting that attribution: its incidence calculation is complete. [Publisher record](https://annals.math.princeton.edu/2015/182-1/p06)

No present-day literature-completeness or global novelty conclusion is part of this audit.

## 7. Optional all-n extension

The extension in the frozen proof is mathematically sound for every integer n at least 3. Within each of the three groups there is one n-fold coordinate vertex. Between groups there are exactly n squared distinct ordinary triple points, indexed by two exponents modulo n. The incidence rule forces exactly one line from each group, and enumerates every pair. The same triangle inequality excludes every intersection from the chosen line at infinity. Scaling therefore produces an ordinary `3n`-fold central point, with the same normalization and fixed-ball arguments.

The delta identity is

`3·n(n-1)/2 + 3n^2 = (3n)(3n-1)/2`,

and the rough-invariant excess is

`[3(n-2)+n^2]-(3n-2)=n^2-4`.

This is an algebraic all-n argument. The author's finite checks through n=100 are additional testing and are not substituted for that argument.

## 8. Reproducibility, source bytes and limits

Companion files contain authored verification code or public metadata only, not third-party source text, source PDFs or dataset contents.

Run the independent checks with ordinary Python:

`python independent_checks.py`

Expected result: the JSON in `INDEPENDENT_CHECK_RESULTS.json`, including nine lines, 36 line pairs, twelve triple points, 36 nonzero direction determinants, the exact factorization, x-leading coefficient -65, deltas 36 and 36, rough invariants 7 and 12, and all assertions passing. This independent script uses Python assertions and must not be run with `-O`.

Separately, the frozen author's `checks.py` was executed both with normal Python and with `python -O`. Both runs succeeded. Both outputs were byte-identical to the frozen `CHECK_RESULTS.json`; the reproduced output records 1,515,405 checks and four intentional-error controls. The checker was read, including its explicit `require` implementation, which remains active under optimization. These calculations are supplemental; the analytic and source-scope claims were audited above as mathematics and source interpretation.

Fresh primary-source retrievals were also performed independently:

- The OWR PDF was 619,685 bytes and matched the retained file exactly, SHA-256 `4815ac5af6a174f097404021b2133c0da742f6764681bac0bedb94f8d595d06f`.
- The published Osaka PDF was 379,471 bytes. The fresh copy had SHA-256 `7dc99c902dff69080671285f7008a088dc9964a635f17029ff513e064a53502d`, while the retained copy had SHA-256 `63fb56a9b7ed10321313a535fd3049c2ba442fbbad1cad7598f9c0cdf62bbf6e`. The 30 differing bytes were confined to the second PDF trailer ID, within zero-based offsets 379410 through 379441. Extracted layout text was byte-identical. Inspection of both trailers confirms the content-independent ID difference. This is not reported as raw-file identity. The author's separately recorded retrieval had a different trailer ID as well, which is consistent with this observation.

Full retrieval metadata is in `INDEPENDENT_SOURCE_RETRIEVAL.json`. Neither metadata nor arithmetic tests certify the theorem by themselves. Acceptance rests on the complete algebraic, analytic and interpretive checks in this report.

**Final assessment:** the frozen v2 packet contains a valid, self-contained counterexample within its stated multibranch scope, with no blocking defect found. Preserve that scope in any acceptance summary or subsequent publication.
