# Independent source and proof scope audit for the coarse Schottky problem

**Target:** 11000048 / AMR-109-0048, rank 449, Farb Problem 4.11.

**Date:** 2026-10-03 UTC.

**Verdict: PASS** for the frozen certificate's credited prior-resolution classification, `already_solved`, with `0/5` substantive author proof-attempt turns. No mandatory mathematical or attribution repair was found. This verdict concerns exactly the ambient coarse-cone question. It does not certify an intrinsic metric statement, settle either adjacent problem, authorize publication, or claim a new proof.

## Frozen material and checks

The reviewed input is `../package/MANIFEST.json`, SHA-256
`64e196175fbbc17bfb46dc6efb2f880d228d3ebe1ced7dcc6a3d7939aeb96878`.
All seven bound files were read and independently checked against its digest map. The package was not modified.

The two downloaded primary PDFs match the digests recorded in `source_record.json`:

- Farb author-hosted volume: `f37c6a1dbc875105c2b294196de1a03a88595b75e8705e6077e9d48f066e402a`.
- Ji–Leuzinger 2008 preprint: `8e49953e13124e51c00bc8861e2c544636fb5d30b2751c601300a2041ca639e6`.

Fresh `pdftotext -layout` extraction of both PDFs agreed byte-for-byte with the supplied local text files. I read Farb's definition (10), Section 4.4 and the neighboring problem headings; Ji–Leuzinger's introduction, Section 2, the separating-node construction and Corollary 3.2 in Section 3, Lemma 4.1, Section 4.1 and its dependencies as stated there. I inspected the supplied rendered images of Farb PDF page 42 and Ji–Leuzinger preprint page 4.

`python3 ../package/verify.py` passed and reported exactly 80 scaling diagnostics and all seven manifest files verified. The script's scope is accurately disclosed: metadata, digests, package exclusions and finite exact arithmetic. It does not test reduction theory, period matrices, existence of smoothings, all genera or an infinite limiting assertion.

## Original question and identity

The original is Benson Farb, “Some problems on mapping class groups and moduli space,” Chapter 2 of *Problems on Mapping Class Groups and Related Topics* (2006), Section 4.4, printed page 35, PDF page 42. Problem 4.11 asks for the portion of the g-dimensional Euclidean sector Cone(A_g) represented by the Schottky locus. The preceding paragraph specifies the locally symmetric Riemannian orbifold metric on A_g; definition (10), printed page 32, specifies pointed Gromov–Hausdorff rescaling. [Original volume](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf#page=42).

The period locus is the image of the Jacobian map on smooth compact Riemann surfaces. The ambient space is the moduli of complex principally polarized abelian varieties, A_g = Sp(2g,Z)\Sp(2g,R)/U(g). The preprint writes Sp(g,R) for the group of 2g-by-2g symplectic matrices, so this notation change introduces no change of dimension or target.

The supplied pinned catalogue statement contains the numbered Problem 4.11 plus following prose that transitions to distortion. The original page gives algorithmic recognition its own heading, Problem 4.10, and ambient-versus-path metric distortion its own heading, Problem 4.12. Thus treating those as excluded is an exact source distinction, not a weakening of Problem 4.11. The pinned catalogue identity and rank agree with the package and local records. Current live catalogue content and status were not independently retrieved in this audit; the certificate correctly leaves them unverified.

## Attribution and theorem versions

The directly checked mathematical source is Lizhen Ji and Enrico Leuzinger, *The asymptotic Schottky problem*, arXiv:0811.4059v1, dated 25 November 2008. Theorem 1.1 on preprint page 4 gives both the whole-cone conclusion and a finite genus-dependent coarse-density constant. The nearby text explicitly attributes the target to Farb Problem 4.11 and distinguishes Problem 4.12. [Version-pinned preprint](https://arxiv.org/abs/0811.4059v1).

The publisher independently confirms authorship, title, *Geometric and Functional Analysis* 19 (2010), 1693–1712, publication on 6 February 2010, and DOI 10.1007/s00039-010-0049-8. Its abstract confirms coarse density and the resulting equality with the whole ambient cone. [Publisher record](https://link.springer.com/article/10.1007/s00039-010-0049-8).

Ji's 2019 article, Theorem 1.3 on page 2213, restates the coarse-density result and attributes it to the joint paper's Theorem 1.2; its reference [17] identifies the 2010 journal article. Remark 1.7 on page 2215 assigns its correction to the speculative distortion argument in Section 8 of that paper. It does not withdraw the coarse-density result. [Later primary article](https://cdn.sciengine.com/doi/pdf/9D3C71BECF314AF3ABFCA33F0E461337).

The package's version distinction is therefore accurate: preprint Theorem 1.1 is directly verified, and published Theorem 1.2 is the numbering reported by the later primary source. The journal PDF itself could not be fetched through the direct publisher PDF endpoint in this audit; I do not claim a line-by-line comparison of preprint and journal proofs. The later article was inspected as extracted PDF text; attempts to retrieve screenshots of its pages failed. These limitations do not undermine the directly checked preprint statement, matching publisher abstract and later explicit reaffirmation.

## Imported proof and applicability

The relevant proof has two substantive imported inputs and a short metric conclusion.

1. **A genus-dependent chamber net.** Preprint Proposition 2.2, page 7, states that a sufficiently deep positive Weyl chamber projects isometrically to A_g and that its image N_g is a net in A_g. In particular, there is a finite C_g with d(x,N_g) <= C_g for all x in A_g. The preprint identifies its sources as Leuzinger, *Tits Geometry, Arithmetic Groups, and the Proof of a Conjecture of Siegel*, Theorem 4.1 and Corollary 4.2, and Ji–MacPherson, Lemma 5.10. Proposition 2.3 identifies the ambient asymptotic cone. For the surjectivity conclusion under audit, the net property is sufficient once the ambient cone is known; no metric control inside the Jacobian locus is required.

2. **Arbitrary diagonal periods lie in the closure.** Corollary 3.2, page 9, gives block-diagonal convergence of periods under separating-node plumbing. For arbitrary elliptic periods z_1,...,z_g in the upper half-plane, take the corresponding elliptic curves and join them in a chain at distinct chosen points. For g >= 2 this is a stable compact-type curve of arithmetic genus g: its dual graph is a tree, and its components have genus one. Its nodes are separating. Smoothing its nodes and applying the stated period convergence produces smooth genus-g Jacobians approaching diag(z_1,...,z_g). This is the construction used in Section 4.1, pages 11–12. It also explains why the elliptic periods may be chosen freely rather than being restricted by a previously fixed smooth curve.

For every such diagonal target, its imaginary part is positive definite, so it lies inside Siegel space. Convergence of its period matrices is ordinary interior convergence and hence convergence in the locally symmetric Riemannian distance; the quotient projection is continuous and distance nonincreasing. Thus the diagonal locus's image, including N_g, lies in the ambient metric closure of the smooth Jacobian locus J_g.

Only pointwise approximation is needed. Given any fixed positive tolerance and any chamber point, choose sufficiently small plumbing parameters for that point. The quantifiers are “for every chamber point, there exist suitable parameters.” There is no exchange requiring one parameter choice to work on the entire noncompact chamber. In a sequence of increasingly distant chamber points, the parameters may depend on the sequence index.

Combining the two inputs, for any x in A_g and eta > 0 choose p in N_g with d(x,p) < C_g + eta/2, and then q in J_g with d(p,q) < eta/2. Hence d(x,J_g) <= C_g after taking the infimum and eta down to zero. If actual point witnesses are desired, a bound C_g + 1 suffices. This justifies the certificate's treatment of the potentially nonclosed locus. No nearest-point projection or attained infimum is assumed.

The preprint's shorthand referring to “real, positive diagonal matrices” in Section 4.1 is understood through its Section 2 group coordinates: acting on iI gives positive-imaginary diagonal period matrices. The certificate correctly refers to diagonal period matrices and does not rely on real matrices being elements of Siegel space.

These checks establish that the cited theorem's objects and assumptions apply to this target. They are not an independent derivation of the specialist reduction-theoretic results or Fay's plumbing expansions. I checked the roles, statements and sufficiency of these inputs and the deductions made from them. I did not reconstruct every upstream reference or formally verify the imported geometry.

## Rescaling and all cone points

Fix a positive integer genus g and the ambient locally symmetric metric normalization. Write X = A_g and S = J_g, and take a finite delta_g with d(x,S) <= delta_g for every x in X. Given any cone point represented by ambient points x_n and scales r_n tending to infinity, choose s_n in S with d(x_n,s_n) < delta_g + 1. Then

    d(x_n,s_n)/r_n <= (delta_g + 1)/r_n -> 0.

The triangle inequality gives

    d(o,s_n)/r_n <= d(o,x_n)/r_n + (delta_g + 1)/r_n,

so s_n remains an admissible bounded-rescaled-distance sequence whenever x_n is admissible. Under the pointed Gromov–Hausdorff approximations used for the ambient cone, the two sequences have the same limit. Thus every ambient cone point is represented by smooth Jacobians. The reverse inclusion holds because S is a subset of X. This covers the vertex and every chamber face, with no generic-direction restriction. The source's r_n = n scaling is included; the argument also works for other diverging scales whenever the indicated ambient limit is considered.

The delta_g + 1 choice is intentional: a nonclosed subset need not contain a nearest point. It removes the attainment issue without changing the limit. If a basepoint in S is preferred, replacing the ambient fixed basepoint by any fixed Jacobian changes rescaled distances by a quantity tending to zero.

The quantifier order is “for each fixed g, there exists a finite constant, valid for every ambient point.” Genus does not vary with n. There is no genus-uniform or effective constant claim. Changing the invariant metric by a fixed positive scaling merely rescales the constant. Genus one is immediate because every principally polarized elliptic curve is its own Jacobian; the plumbing discussion is needed only for g >= 2.

The distances above are ambient distances restricted to points of S. They do not bound path lengths of curves constrained to S. Accordingly this audit does not assert equality with a cone constructed from the intrinsic path metric, any distortion estimate, any algorithm, or equality of compactification boundaries.

## Accounting and gate limits

The imported local research record records title reading and unfinished statement retrieval. The local assessment proposes a mechanism and calls for a literature check. The package's event log records source-audit work, not a substantive new mathematical attack. On the material reviewed, `0/5` is consistent; the elementary explanation of a cited theorem does not establish new mathematical priority.

The package's extensive repository-history and duplicate checks were read as reported gate evidence. This audit does not independently replay all repository API searches, tree enumerations, remote historical records, or the author's correction/retraction search. No assertion of exhaustive off-repository history or literature coverage is made. The source/proof-scope PASS rests on the direct match and sufficient prior theorem, not on search silence.

## Repairs and disposition

**Mandatory repairs: none.** Retain the explicit fixed-genus, ambient-metric, nonclosed-locus and version-number qualifications already present. Retain credit to Ji and Leuzinger and the `already_solved` disposition; do not relabel this certificate as a new solution or charge it as a fresh proof attempt.

Optional reproducibility improvement for a later package revision: pin the preprint links to `0811.4059v1` and preserve a dated local copy or retrieval record of the 2019 reaffirmation outside the publication package. This is not required for acceptance because the existing record already names v1 and binds the directly checked main preprint bytes.

HOLD any expanded claim about Problem 4.10, Problem 4.12, an intrinsic metric, genus-uniform estimates, effective constants, live catalogue changes, publication or novelty unless separately reviewed and authorized. This audit makes no remote writes and changes no frozen source file.
