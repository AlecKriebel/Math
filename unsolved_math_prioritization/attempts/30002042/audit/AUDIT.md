# Independent audit: stringy E-polynomial degree and finiteness

Problem 30002042 / OWR-11783-009, rank 837. Audit date: 2026-10-06.

## Decision

**Accept the sealed author packet as a correctly scoped partial result and source correction.** No author-file correction is required. This acceptance does not certify a solution of the compound problem, a new theorem of general finiteness, an infinite realized counterexample, or the entire proof of the September 2026 degree manuscript. The five-approach status remains `unsolved_by_this_attempt`, 5/5.

The exact accepted author ZIP is 13,660 bytes with SHA-256
`3e77fa2a11514444ea34bbee9ebd9096cbf313749d22dd4c7afc21060ef4218b`.
Its external manifest has SHA-256
`7ed84eb3615eba0c2a413e3a7653e7a826312171aff1f61666c67d614b06503f`;
its separately trusted bootstrap has SHA-256
`303c8a3f91db4cafd7a73504357ac1c90170bdee17635f8222498462fb3f2d7c`.
These originals were not modified. There is no derivative proof patch to substitute.

## 1. Target and source verification

The complete problem record, including nested fields, was taken from the full supplied corpus, rather than reconstructed from the short statement. Exactly one problem and one catalog entry matched the identifier. The report lookup was empty. Default Python `json.dumps([complete_problem, reports.get(problem_number,{})], sort_keys=True).encode()` produced 4,104 bytes and SHA-256 `77c0d0843392c742e6a65cfc507d39ac3569df4b835f26e46a40c3b478d631a4`. The 249-byte statement hash was `fde972335adb681663341ef1fb412fc75fff869dcbcfeae849e95486022f98a7`. Both agree with the catalog and author binding. The author's privately retained comparison bytes are equal to this independent serialization. Only hashes, counts, and match results are included here; no corpus records are included.

All seven referenced PDFs were independently retrieved again from their public URLs. All seven sizes and SHA-256 hashes exactly matched the author metadata. See `SOURCE_BYTE_CHECKS.json`. The two OWR distributions have different bytes and are not represented as identical documents.

Printed OWR pages 1292–1293 were read as extracted text and as newly rendered images of the freshly retrieved EMS PDF. The notation really is `E_st(P,t)` beside a formula involving both `u` and `v`, with no indicated substitution for `t`. The following degree sentence uses `dim(P)+1−2r`. That is an ambiguity in the workshop account; the audit does not supply an undocumented specialization. The actual two-variable formulation and scalar-class question are fixed by Nill–Schepers, Conjecture 3.3(2), and Batyrev–Nill, Question 4.21. The live curated problem page could not be opened with the web tool, so this is not a claim of live-page equality.

Primary target: [Nill's contribution in Toric Geometry, OWR 21/2012](https://ems.press/content/serial-article-files/46392?nt=1), printed pp. 1292–1294. Finiteness formulation: [Batyrev–Nill, Combinatorial aspects of mirror symmetry](https://arxiv.org/pdf/math/0703456), Question 4.21 and Remark 4.22.

### Established inputs and their hypotheses

- [Nill–Schepers](https://arxiv.org/pdf/1005.5158): Definition 3.1 is the precise face formula; Proposition 3.2 supplies symmetry and duality; Corollary 3.7 supplies polynomiality and vanishing for negative CY-dimension. Proposition 4.15 requires a Z-join, equivalently the integral free join used here. Remark 4.10 also supplies the sometimes implicit converse: a Z-join is Gorenstein precisely when its factors are Gorenstein. Example 4.16 rules out unrestricted multiplicativity for broader joins. Conjecture 3.3(2) is total degree `2n` or zero. Its boundary and derivative clauses agree with the identities checked in the author packet. Lemma 6.1 supports the conditional application in the 2026 manuscript.
- [Lorenz–Nill, On smooth Gorenstein polytopes](https://www.jstage.jst.go.jp/article/tmj/67/4/67_513/_pdf/-char/en): Theorem 4.1 assumes smoothness and `n≥0`; when `d>3n+3`, it gives a smooth representative with the same E-polynomial and dimension at most `3n+1`. The author's reduction preserves these hypotheses. The paper is by Lorenz and Nill, not Schepers and Nill.
- [Borisov–Li, On complete intersections with trivial canonical class](https://sites.math.rutgers.edu/~borisov/pubs/pdf/BoundCICY.pdf): Theorems 5.1–5.2 and Corollary 5.3 concern geometric complete intersections in the stated base-point-free big Fano setting, and hence the Batyrev–Borisov construction. The connected-component qualification is material. Section 6 explicitly separates the general reflexive-Gorenstein-cone construction. The author correctly refrains from using this theorem for arbitrary Gorenstein polytopes.

### September 2026 manuscript

[Knupfer–Nill, arXiv:2609.18873v1](https://arxiv.org/html/2609.18873v1), Theorem 1.5 states vanishing exactly for thin polytopes, and total degree `2n` otherwise, without a smoothness or nef-partition restriction. Its statement, Theorems 2.17–2.18, and the application proof of Theorem 1.5 were inspected. Conditional on the decomposition result and cited local-polynomial results, the application is consistent: thinness forces a negative-CY free-join factor; non-thinness gives a contribution to the constant coefficient through Nill–Schepers Lemma 6.1; duality gives the upper corner.

The full decomposition proof in Sections 3–4 and every dependency were **not independently accepted in this audit**. The inspected arXiv record lists submission on 16 September 2026, one version, and no journal reference. These are manuscript-status observations, not a peer-review certificate. None of the accepted partial proofs below needs this new degree theorem.

## 2. Independent mathematical review of every retained result

### 2.1 Coefficient-corner criterion

For a polynomial satisfying `E(u,v)=(uv)^n E(u^−1,v^−1)`, the map of exponent pairs `(p,q)→(n−p,n−q)` is injective. A negative exponent on the right cannot cancel with a different monomial. Thus every nonzero term has `0≤p,q≤n`; a nonzero polynomial is impossible when `n<0`. The only possible term of total degree `2n` is `u^n v^n`, whose coefficient equals the constant coefficient. This proves the author's criterion in both directions, including `n=0`. The example `u^n+v^n` confirms that separate degrees alone do not force the corner for `n>0`.

### 2.2 Reflexive triangle

The stated dual vertices satisfy the three facet inequalities and each lies on two supporting lines. Both triangles contain the origin in their interiors. Independently counting lattice points in homogenized half-open fundamental parallelepipeds gives `h*_T=1+t+t²` and `h*_(T-dual)=1+7t+t²`. Fully open boxes give `t+t²` for both local polynomials. This method is independent of the author's dilate-count and edge-subtraction routine.

All eight faces of the triangle were included in a separate face-sum implementation. Vertices have zero local polynomial; edges of T are primitive and also contribute zero. The empty and full terms give `1−u−v+uv`. Consequently total degree and diagonal degree are 2, each variable degree is 1, and substitution `v=1` gives zero. The author uses this to separate conventions, not to refute the properly qualified two-variable conjecture.

### 2.3 Zero examples in every nonnegative CY-dimension

For each `n≥0`, take `D=n+2` and the reflexive simplex `R=conv(e_1,…,e_D,−1)`. It has primitive integral facet normals `−1` and the vectors having one coordinate D and all other coordinates −1. Its lattice pyramid P has dimension `D+1`. Explicitly, `2P−(0,1)` has base inequality `z≥−1` and side inequalities `a·x−z≥−1` for those facet normals a. Hence P is Gorenstein of index 2, and its CY-dimension is D−2=n. Equivalently P is the integral free join of R with a point. The point has index 1, CY-dimension −1, and E-polynomial zero. Free-join multiplicativity proves `E_P=0`. No degree is assigned to zero. Direct facet diagnostics corroborated n=0 through 12; the displayed construction proves every n.

### 2.4 Finiteness ranges

Negative n permits only zero; at n=0 all nonzero polynomials are constants and thus constitute one scalar class. If `r≤R`, the relation `d=n+2r−1` bounds dimension. Fix a dimension d and index r, and write `rP−m=Q`. Choose one representative of each of the finitely many reflexive Q up to unimodular equivalence. With Q fixed, replacing m by an element of the same class modulo `rM` only translates P integrally. There are at most `r^d` such classes; those that fail integrality or the Gorenstein condition are simply discarded. For the additional assertion of finiteness in fixed dimension without fixing r, use the standard codegree bound `1≤r≤d+1` (also recalled in the cited sources). This makes explicit a standard fact left implicit in the author prose; it does not require a correction to its bounded-index argument.

The smooth-class conclusion follows from the precise Lorenz–Nill theorem above plus fixed-dimensional finiteness. The geometric Borisov–Li conclusion is correctly kept separate. Neither eliminates the unrestricted-index gap for arbitrary polytopes.

### 2.5 Scalar-growth family

For `I=[−1,1]`, the local polynomial is t; including all four faces in an independent computation gives `E_I=2`. For k integral free-join factors, dimensions add with k−1 extra dimensions and indices add. Thus `d=2k−1`, `r=k`, `n=0`, and `E=2^k`. A fixed Q then gives `2^k E_Q` at unchanged n. When `E_Q≠0`, these are distinct polynomials but the same scalar class. Independent Ehrhart-series convolution also checks `h*=(1+t)^k` for small joins. This correctly exposes why exact equality cannot replace scalar equivalence.

### 2.6 Reduction to positive-CY free-join-indecomposables

Successive nontrivial integral free-join decompositions terminate because every nonempty proper factor has smaller dimension. The factors stay Gorenstein by Nill–Schepers Remark 4.10. Nonzero E for the original implies nonzero E for every final factor. Each factor therefore has nonnegative CY-dimension. Additivity then bounds the number of positive-CY factors by n. Zero-CY factors only multiply E by nonzero constants. A finite set of positive-CY scalar classes in each of the finitely many dimensions `1,…,N` has only finitely many products of length at most N. The reverse implication is restriction. This proves precisely the author's equivalence, without decomposition uniqueness and without silently changing Z-join indecomposability to the broader irreducibility notion.

### 2.7 Formal infinite polynomial family

For `Q_m=(1−u³)(1−v³)+m uv(1−u)(1−v)`, expand the two summands. The corner coefficients are 1, the `(3,0)` and `(0,3)` coefficients are −1, and the four middle coefficients have magnitudes m with the required alternating signs. Thus for every integer `m≥0` the signed Hodge coefficients are nonnegative, the total degree is 6, and each separate degree is 3.

Each summand is invariant under swapping u and v and under simultaneous exponent reversal around `(3/2,3/2)`. Each satisfies the negative single-variable reversal, proving the self-mirror identity. Setting v=0 leaves `1−u³`; setting v=1 gives zero identically. The latter yields both derivative identities at `(1,1)` with n=3 because both sides are zero. Finally, scalar proportionality forces the scalar to equal 1 by constant coefficients, and then forces m to agree by the uv coefficient. This is an infinite family of formal scalar classes. There is no proof of its realization by polytopes, and none is asserted. It is therefore not a counterexample to the original finiteness question.

## 3. Code, integrity, and execution boundary

Every author code file encountered was read before execution: the 179-line `checks.py`, the external bootstrap, the freezing script, and the author control script. Only the independently pinned bootstrap and its authenticated embedded check bytes were executed; the author's freezing/control scripts were not rerun against the originals. The check file imports only JSON and `math.gcd`, makes no filesystem or network changes, and uses explicit failures rather than optimization-sensitive assertions.

The external bootstrap checks `-I -S` before filesystem-dependent imports, pins the ZIP and manifest, enforces the exact eight-member inventory and regular-file modes, rejects duplicate JSON keys, checks exact member sizes and hashes, and executes only authenticated code bytes in a fresh isolated `-c` child. Optimization is propagated. It does not execute an extracted sibling `checks.py` or resolve a package entrypoint.

Independent runs, recorded in `REPLAY_NORMAL.json` and `REPLAY_OPTIMIZED.json`, each contain:

- 6 positive author executions: both child optimization modes under original paths, relocation with spaces and hostile siblings, and a hostile working root/PYTHONPATH/source/bytecode-cache environment.
- 36 negative executions: missing isolation flags; changed prose/source; unexpected root module, entrypoint, cache, traversal, absolute, directory, missing, duplicate, or symlink members; malformed or changed manifests; and symlink input files. Every case was rejected and no poison sentinel was created.
- 14 additional structural/member-layer probes. These explicitly used test-local replacement top-level pins to reach the untouched deeper validation logic. They all rejected. Those replacement pins were never used to accept a packet or persisted as deployment trust anchors.

All six positives in each reviewer mode reproduced the author's 230 exact checks and 10 shortcut labels. Those labels are sanity assertions, several elementary tautologies, and should not be represented as independent adversarial mathematical proofs. They do not establish general finiteness.

The separate `independent_math.py` makes no use of author functions. It passed 4,795 exact checks in each of normal and optimized mode, with byte-identical output. It enumerates fundamental boxes and all triangle faces, checks interval joins and explicit pyramid facets, and checks the formal family at m=0,…,64. The all-parameter arguments are the mathematical proofs above and the author's symbolic calculation over Z[m], not the finite sample count.

This is not an OS sandbox against a malicious trusted interpreter, standard library, bootstrap, or concurrently replaced trusted runtime. The standalone bootstrap still needs its own independently authenticated hash. Integrity controls establish which code ran; they do not make that code a formal proof checker.

## 4. Acceptance limits and packaging

Accepted: the coefficient criterion, triangle, universal zero-pyramid construction, bounded-index and n≤0 cases, smooth/geometric source boundaries, scalar-growth family, free-join reduction, formal-identity obstruction, and faithful statement/status reporting of the 2026 manuscript.

Not accepted as proved: general finiteness or infinitude of realized scalar classes; the complete 2026 decomposition theorem; novelty; exhaustive current openness; or publication/CI success. The bibliography metadata in `PUBLICATION_METADATA.json` distinguishes online and print dates when available and reports the failed OWR Crossref lookup together with independently retrieved EMS publisher metadata confirming the report title, DOI, volume, pages, and publication date 20 February 2013.

The audit archive contains only authored audit prose, acceptance data, authored verification code, computed diagnostics, and public-source/corpus hash metadata. It contains no source PDF, extracted source text, rendered source image, corpus record, or private coordination material. No repository publication was performed. The sealed author package remains separately available at the exact hash above.
