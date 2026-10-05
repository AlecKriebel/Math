# Independent adversarial audit: root-of-unity blowups

## Verdict

**PASS, scoped to the frozen partial-results packet. No mandatory correction identified.**

Problem 30004334 / OWR-17296-019; assessed 2026-10-05. The five documented approaches are substantive. The general question for a fixed complex order m >= 4 remains unresolved by this packet. This is not a solved-status finding, a novelty claim, or a claim that a literature search proves global openness.

Author manifest SHA-256:

`465c3840c518ad8b5abe6bc229e306f2059a211f64cdeb48f5cb0005d2b88ecb`

All eight payload files and the manifest were read. The author directory was preserved byte-for-byte. No remote writes were made. This audit contains authored analysis, programs, numerical verification metadata, and public-source metadata only. It includes no source PDF, extracted source text, external dataset contents, or private coordination material.

## Target and conventions

The requested object is the blowup of the complex projective plane at the m^2 distinct torus points with affine coordinates (epsilon^a, epsilon^b). The three coordinate vertices are absent. Curves are reduced and irreducible, and the requested signed optimal bound is the infimum of their squares. The parameter m is fixed before bounding curves.

The target and sign convention agree with the [Oberwolfach report, printed pp. 3308–3310](https://ems.press/content/serial-article-files/46833). The field is supplied by context rather than repeated in its final problem paragraph; the [original authors’ arXiv record](https://arxiv.org/abs/1909.05899) explicitly identifies complex projective geometry. The author packet acknowledges this distinction correctly.

The distinction between integral and reduced curves is material for optimal constants. The example on X_3 checks: two different-family arrangement lines intersect at a blown-up grid point, so their strict transforms are disjoint and their reduced union has square -4. Boundedness itself transfers from integral curves to reduced divisors by Zariski decomposition, since the negative part has boundedly many components and coefficients at most one. Nonreduced multiples of an exceptional curve immediately destroy boundedness.

## Geometric proof review

### 1. Blowup and pencil

The forms defining the pencil have independent differentials at every grid point in characteristic zero. One blowup at each point resolves all base points. Each exceptional divisor maps isomorphically to the pencil base, so it is a section, never a vertical component. The fiber class is nef, has square zero, and intersects each exceptional divisor once. The adjunction identity in Section 1 has the correct signs and arithmetic genus. For a horizontal integral curve the fiber intersection is the degree of the map from its normalization.

### 2. Complete vertical classification and lines

For m >= 2, a pencil member with all three diagonal coefficients nonzero is smooth by its partial derivatives. Smooth plane curves of positive degree are irreducible: two different components would intersect. The other three parameter values give precisely the three reduced unions of m distinct lines. Blowing up smooth grid points does not create additional fiber components. The only vertical integral curves are therefore the listed line transforms and complete smooth fibers.

A non-arrangement line has at most two grid points: its affine equation and unit-modulus coordinates reduce incidence to intersection of a circle and a genuine real line. The zero-coefficient cases are exactly arrangement lines or lines missing the grid. Arrangement lines have square 1-m. Thus the impossibility of an m-independent bound is valid and does not imply failure on a fixed surface.

### 3. Small orders and anticanonical obstruction

For m=1, plane multiplicity is at most degree and only the exceptional curve is needed to attain -1. For m=2 and degree at least two, an integral curve is not an arrangement line. Summing Bezout over one complete family gives total multiplicity at most 2d; adjunction gives square at least d-2. Lines and exceptional curves give the remaining bound -1. For m=3, K=-F and adjunction gives square at least -2, attained by arrangement lines. No unsupported classification of (-1)-curves enters these arguments.

For m>3, the intersection of -K with the nef fiber is negative. This excludes the entire pseudoeffective cone, hence every effective positive multiple of -K. The scope and strict threshold are correct.

### 4. Symmetry and numerical feasibility

Constant multiplicity r gives d >= mr by nefness, and hence nonnegative square. Transitive group invariance implies constant local multiplicity, but the converse is not required. Averaging increases square by the multiplicity variance; it cannot justify discarding nonsymmetric curves.

The explicit X_4 family has nonnegative integral multiplicities, fiber intersection 4, square 1-8k^2, and arithmetic genus zero. Its arrangement-line slack is 1. For all other lines, the bound reduces to the nonnegative polynomial (2k-1)^2. These conclusions hold for every integer k>=1, not merely the author verifier’s finite sample. No effectivity or irreducibility follows from these tests.

### 5. Nonrealizability for every parameter

[Hao’s manuscript](https://arxiv.org/pdf/1708.09463) was inspected at Lemma 2.2.1, Theorem 2.2.7, and the singular-curve reduction. Its two cases exhaust integral curves when h^0(-K)=0; smoothness of the curve is not an unstated requirement. Substitution for these rational blowups gives 2-4m^2-2g. On X_4 the genus-zero bound is -62, while the numerical family has square at most -71 for k>=3. Arithmetic genus zero forces geometric genus zero if an integral representative exists. The independent full-rank certificates below exclude k=1,2 even for arbitrary nonzero plane forms. The entire family is therefore excluded, with no gap between parameter ranges.

### 6. Characteristic-zero power images

The restriction of the coordinate-power map to x_0+x_1+x_2=0 is generically one-to-one: each nontrivial root-of-unity pair can identify at most one affine parameter. Thus the image has degree d, and the line is its normalization. The power map is etale on the torus over C, so normalization branches meeting the grid are smooth.

After normalizing one coordinate, two unit complex numbers summing to -1 must be the two primitive cube roots. The two normalization points exist exactly when 3 divides dm. Their images coincide precisely when 3 divides d, and then their tangent directions differ. Counting the squared image multiplicities gives exactly the three cases in formula (4). Other singularities of the image do not affect the blowup square, because those points are not blown up. Only d=1 with 3 dividing m is negative.

The [Cheng–van Dobben de Bruyn theorem](https://chngr.github.io/assets/negcurves.pdf) requires positive characteristic, m invertible, and dm=p^e-1. These hypotheses ensure d is also invertible and yield infinitely many admissible exponents for fixed m prime to p. Its negative-square formula is correctly kept separate. The complex m=4,d=6 value is 32; the characteristic-five construction gives -7. There is no transfer to C.

### 7. Divisibility and covers

The inclusion of center sets when m divides n gives a further blowup X_n -> X_m, with the claimed decrease in a strict transform’s square. Every integral curve on X_m has a strict transform, including exceptional curves. This proves the stated downward boundedness and upward unboundedness implications.

For the different coordinate-power construction, the map on the plane is finite flat of degree a^2; on affine charts its coordinate ring is free with basis x^i y^j for 0<=i,j<a. The center preimage is precisely the larger grid and is etale there. Flat base change therefore gives the stated finite map on blowups, without new exceptional ramification. For a>1 the branch curves are the coordinate-line transforms; for a=1 the map is the identity. Away from branch curves a pulled-back integral divisor is reduced. The projection formula, component count, and nonnegative pairwise intersections give (5) with the correct degree a^2. Rearranging it to bound one component requires subtracting uncontrolled cross-intersections. The packet does not make the invalid upward inference.

## Independent computations

`independent_verify.py` does not import the author verifier. It reconstructs the arithmetic by different representations and algorithms:

- Exact Gaussian-integer affine line equations, identified by their incident sets, give 60 lines: 12 with four points and 48 with two points. Their pair coverage is exactly 120, with no repetition.
- Formal polynomial arithmetic in k verifies the numerical-family intersection identities and all-parameter line and genus thresholds.
- Jets are generated by repeated polynomial multiplication of (center+T)^n, rather than the author’s binomial/power expression. Columns are ordered by total degree. Reverse elimination with column pivoting reconstructs the selected minors.
- The 60-by-55 matrix has selected-minor determinant 23 mod 101; the 624-by-595 matrix has determinant 57 mod 101. The column-permutation signs are both +1. These determinants are nonzero over the residue field, hence the Gaussian-integer minors are nonzero in characteristic zero. Rank remains full after extending scalars to C.
- Exact rational-polynomial gcds for 1<=N<=60 independently check the cube-root-only normalization intersections. Four thousand branch-image cases match the square formula. These finite controls supplement, rather than replace, the all-parameter unit-circle argument.

The selected rows are the author’s witnesses; the regenerated entries, basis ordering, determinant algorithm, and line reconstruction are independent. No floating-point rank or numerical tolerance is used.

## Replays and integrity

`REPLAY_RESULTS.json` records eight successful full replays: author and independent verifiers, each in normal and optimized Python, each in original and relocated directories. Relocation uses spaces in paths and an unrelated working directory. Outputs agree exactly across the corresponding runs. Seven author mathematical negative controls remain active under optimization.

Thirty integrity checks reject changed, missing, or unlisted payloads; a changed or duplicated manifest; payload symlinks; and a payload whose changed checksum was coherently inserted into an unpinned replacement manifest. The independent verifier also rejects a manifest symlink. Every mutation is made in a disposable copy. The original freeze is unchanged.

Nonblocking hardening note: the author integrity function accepts a manifest-only symlink to the exact pinned manifest bytes. Its payload symlink rejection and hash binding remain effective, so this does not change the mathematics or verdict. The independent verifier rejects all symlinks. No mandatory correction is needed for the claimed byte-integrity contract.

## Source and scope limits

All eight public-source PDF copies were hash- and size-compared with the author metadata. Relevant primary passages were independently inspected; the source-specific record is `SOURCE_AUDIT.json`. The revised and published problem numbers are distinguished. Later degree/genus-dependent results and results about Fermat hypersurfaces do not resolve this torus-grid target.

The audit does not re-certify historical private or repository searches, tracking rank, or claims of search exhaustiveness. None is used as mathematical evidence. Source inspection checks applicability; it is not a new proof of every imported theorem. No general boundedness theorem or complex counterexample is certified.

## Reproduce

Run from any working directory, substituting the actual packet locations:

`python3 verify_audit.py --author /path/to/root_unity_30004334 --expected-audit-manifest AUDIT_MANIFEST_SHA256`

Repeat with `python3 -O` for optimized mode. To repeat the more extensive temporary-copy and mutation suite:

`python3 replay_checks.py --author /path/to/root_unity_30004334`

The audit manifest binds this report and all audit payloads; its externally supplied hash pins the audit freeze. The independent verifier pins the author manifest internally. Source PDFs are unnecessary for arithmetic replay and are deliberately not distributed here.
