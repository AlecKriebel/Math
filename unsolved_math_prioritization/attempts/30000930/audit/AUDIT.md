# Independent audit of the continued crossingless-matching release

## Verdict

**PASS for the stated k=2 ordinary graded Yoneda/arc-algebra comparison and the qualified supporting partial results.** No blocking mathematical error was found. The general weighted all-k target remains unresolved in this investigation, with the packet's unsolved-after-five-approaches disposition. The k=2 proof supplies a valid reconstruction of mixed products from one-sided module information and duality; it does not silently promote pairwise formality to collection compatibility.

This audit binds exactly `continued-unsolved5.zip`, 55,541 bytes, SHA256 `7d50dd95d9b3bb49b20b2218f2b865d1e75c0adad4c26a727c37ea572baf3846`. The original archive was not modified. The previous source correction and audit remain historical results, with their qualifications intact. No novelty or comprehensive current-literature status is certified.

## 1. Geometry, half-canonical twists, and the endpoint actions

The clean intersection geometry retained from the original packet is sufficient: A is P1 x P1, B is the Hirzebruch surface F2, and C is a P1 which is diagonal in A and the negative section in B. A and B are smooth projective Lagrangian surfaces in the smooth resolved Slodowy slice X of complex dimension four. These hypotheses meet the compact-Kahler and clean-intersection requirements even though X is noncompact.

The line-bundle calculation is worth making explicit. The chosen half-canonical bundle on A restricts to O_C(-2). On B, K_B/2=-s-2h restricts to degree -(-2)-2=0, hence O_C. Their product restricts to K_C=O_C(-2). Therefore the orientation line in the mixed Ext calculation is trivial. Equivalently, the two local Ext degree-one twists are respectively

- N_(C/B) tensor (K_A/2)|C dual tensor (K_B/2)|C, of degree -2+2+0=0;
- N_(C/A) tensor (K_B/2)|C dual tensor (K_A/2)|C, of degree 2+0-2=0.

There is no nontrivial order-two local system on P1. Thus the half-canonical twists are being used correctly. Replacing them by untwisted structure sheaves is not justified by this mixed calculation.

For the cohomology coordinates, p=h and q=-s-h satisfy p^2=q^2=0, pq=-hs, and both restrict to the positive class t on C. Both x and y likewise restrict to t. The diagonal graded dimensions are 1,2,1 in degrees 0,2,4; each mixed corner has dimension one in degrees 1 and 3.

The published Mladenov theorem applies precisely to these half-canonical objects: Theorem 0.1.12 gives the one-sided algebra/module pair comparison, and Remark 0.1.13(2) supplies its other-endpoint variant. Neither statement requires X compact. Its hypotheses and both endpoint statements were independently checked in the official article and its PDF, including visual inspection of PDF page 5. Theorem 0.1.8 and Stroppel-Webster Theorems 40 and 45 supply the stated single-object rings and pairwise graded spaces. [Mladenov 2024](https://doi.org/10.1007/s00029-023-00894-3), [Stroppel-Webster 2012](https://doi.org/10.4171/CMH/261).

There is no simultaneous-identification gap in the limited conclusion actually needed. In C[x,y]/(x^2,y^2), a degree-two element ax+by squares to 2ab xy. Thus the nonzero square-zero elements form exactly the two coordinate lines, and every graded algebra automorphism permutes and rescales those lines. Nonzero action on each line is therefore independent of which graded ring identification a one-sided theorem supplies. Each endpoint can be handled separately; the four actions on a fixed mixed degree-one generator are nonzero multiples of the same one-dimensional degree-three space. Independent rescaling of the four diagonal generators makes all four images equal. No canonical or collection-compatible quasi-isomorphism is required.

Analytification does not change the answer: local coherent Ext agrees under analytification, and its cohomology sheaves have proper support. Applying proper-support GAGA to the local-to-global comparison preserves both Ext groups and their natural Yoneda compositions. This is a comparison of the algebraic objects actually named in the claim.

## 2. Serre duality and signs

The proper-support duality argument is valid. The sheaves are perfect because X is smooth; their supports are proper. A smooth projective compactification can be chosen without changing X or the neighborhoods of their supports. Extension by zero remains coherent, and both the Ext groups and the canonical-bundle restriction relevant to duality are unchanged. Since K_X is trivial, duality gives nondegenerate degree-r/degree-(4-r) pairings in both directions. The degree-one and degree-three mixed spaces are one-dimensional, so the two compositions into Ext^4(E_A,E_A) used in the lemma are nonzero.

There is no sign in the associativity law for the Yoneda algebra. There is a graded sign in cyclicity of its Serre trace. This distinction matters. With the normalized arc table, one may choose

    tr_A(xy)=1,   tr_B(pq)=-1.

Then, for example, tr_A(uz)=-tr_B(zu) and tr_A(wv)=-tr_B(vw), as required for odd-degree pairs. The proposed table is therefore compatible with Calabi-Yau duality; requiring both normalized top classes to have trace +1 would introduce an artificial contradiction. In geometric cohomology coordinates pq=-hs already explains the opposite top-class orientation. The release correctly claims only an abstract graded algebra isomorphism, without a trace-preserving or canonical normalization.

The independent checker verifies all 144 graded-cyclic trace identities and nondegeneracy. Before normalizing alpha and beta, its full trace-pairing determinant is alpha^2 beta^2, hence nonzero under exactly the duality assumptions.

## 3. Rigidity lemma and independent symbolic verification

Every step of the elementary proof is valid over C. After the four forward actions have been normalized to w, write uv=c_x x+c_y y and vu=d_p p+d_q q. Associativity gives c_x=c_y=beta, all four reverse action coefficients beta/alpha, d_p=d_q=gamma, then 2 beta w=2 gamma w and delta=alpha. Only nonzero alpha, nonzero beta, and the invertibility of 2 are used. The final rescaling v -> beta^(-1)v and z -> alpha^(-1)z produces precisely the displayed arc multiplication. Blocks and degrees leave no unspecified additional products.

The independent script does not import or copy the author's verifier. It starts with the most general multiplication table permitted by the lemma after normalizing the four forward actions. It leaves ten remaining coefficients undetermined, with alpha and beta nonzero parameters. Expanding all 1,728 basis associativity conditions produces 14 distinct nonzero polynomial expressions. Exact Groebner reduction proves that the ten coefficients are forced to the values in the proof.

To rule out an accidental generic-parameter argument, a second calculation works over a polynomial ring with relations alpha*inv_alpha=1 and beta*inv_beta=1. It again forces all ten formulas. Thus there is no hidden exclusion such as alpha+beta != 0. The computations do not claim validity in characteristic two.

It then verifies:

- all 1,728 symbolic associativity triples in the resulting normal form;
- all 144 products under the stated basis normalization;
- corner and cohomological-degree compatibility;
- all 144 graded trace-cyclicity equations and a nonzero Gram determinant.

The normalized table is the usual two-object arc algebra: diagonal tensor squares of C[t]/(t^2), mixed copies shifted to degrees 1 and 3, and the usual merge/split operations. In the earlier convolution presentation, the B pushforward carries the opposite weight, with -s=p+q and -hs=pq. This agrees with the already-audited opposite-sign repair, not with ordinary complex-oriented f=1 convolution.

## 4. Local calculation and higher-rank limitations

The two affine Koszul complexes, the two closed degree-one maps, and their two zero compositions satisfy all six exact polynomial-matrix identities claimed. This is compatible with nonzero global mixed products: the local associated-graded product may vanish while the global product has higher filtration. For A=P1 x P1 and B=F2, the relevant self-Ext^2 contribution is H^1(Omega^1), while H^0(Omega^2) and H^2(O) vanish. No local-to-global vanishing inference is justified, and the release does not make one.

The higher-rank annihilator argument is also correct in its explicitly hypothetical simultaneous cohomology model. For a group of r_j square-zero variables, the quotient by their differences is C[t]/(t^2). Frobenius duality gives a two-dimensional annihilator with basis in degrees r_j-1 and r_j. Tensoring over the s groups yields the stated binomial coefficient in the required degree.

An independent implementation enumerates all perfect pairings and filters crossings, uses graph traversal for components, and constructs difference-multiplication matrices on subset monomials. Exact rational elimination verifies all 2,878 ordered triples for k=1 through 4. The counts agree: all triples have dimension one for k<=3; at k=4 there are 2,696 dimension-one and 48 dimension-two cases. The displayed k=4 triple indeed permits span(u,v). In the standard TQFT its six-point factor has a genus-one contribution, hence image 2u, while the shared last cup contributes the unit. Degree and balancing alone do not select that direction. This is neither a family of globally associative algebras nor a counterexample to the desired comparison.

## 5. Literature and the all-k boundary

The newer Mladenov preprint was independently retrieved at the specified v1 URL and matched the supplied bytes and hash. Its Theorem 1.1.1/5.4.9 states collection formality for the relevant orientable compact Kahler clean-intersection collections. Lemma 5.4.7 and Corollary 5.4.8 additionally state triviality of the relevant formal deformation of composition. This latter statement is understood through a formal change of coordinates; it is stronger than formality alone. Definition 5.3.1 and the following multiplication construction use Yoneda composition. The retained distinction is therefore accurate: these results do not by themselves calculate the concrete weighted arc-surgery product. Conjecture 1.5.3 remains a conjectural local Fukaya comparison in the inspected preprint. The present audit checks the quoted scope and dependencies, not the entire preprint's proof. [Mladenov 2026, v1](https://arxiv.org/abs/2604.06630v1).

The categorical-route cautions were spot-checked against the private primary-source files. Cautis-Kamnitzer's Section 7.2 uses projective 2-morphisms, and Theorem 8.2 identifies regraded link homologies. Mackaay-Webster Theorems 5.10 and 5.11 compare link invariants. These inspected statements alone do not provide the requested object-specific multiplication comparison. The corrected sl2 reference is arXiv:math/0701194; arXiv:0710.3216 is the sl(m) sequel. [Cautis-Kamnitzer](https://arxiv.org/abs/math/0701194), [Mackaay-Webster](https://arxiv.org/abs/1502.06011).

Anno's 2008 canonical/multiplication claim, the later Anno-Nandakumar Section 5.3 discussion, and the publisher-deposited final abstract were distinguished correctly. The final deposited abstract describes multiplication as conjectural. The inaccessible final AMS PDF was not inspected in this audit either; supplied metadata is not substituted for reading its proof. An in-preparation bibliography entry establishes no theorem. These sources do not justify an unqualified all-k resolution or global-open-status claim. [Anno 2008](https://arxiv.org/abs/0802.1070v1), [Anno-Nandakumar preprint](https://arxiv.org/abs/1602.00768v1), [final publication](https://doi.org/10.1090/tran/8765).

## 6. Frozen history and reproduction

The current archive contains exactly 24 members, including its manifest. All 23 listed payload files pass byte-count and hash verification. Its history binding passes for all seven entries. The embedded original author archive is byte-identical to the separately retained original. All six preserved audit files are byte-identical both to the original audit directory and to the six files in the original portable audit ZIP. Excluding a runtime bytecode cache is correct; that cache was not in the bound portable audit.

The author's new exact output matches CONTROL_RESULTS.json byte for byte. The complete historical replay passes, including the earlier independent 1,728 symbolic triples and 576 product comparisons. No old verdict is inherited as certification of the new result.

The original source-formulation correction remains necessary: the f=1 obstruction refers to ordinary complex-oriented Gysin maps, whose signs are not explicitly fixed in the original report. The inconsistent alpha labels in the final article do not determine our conventions. None of the continued claims overturns the original associator or the distinction between unweighted and weighted multiplication.

Run the new audit with Python 3 and SymPy (checked with 1.14.0):

    python3 replay_audit.py /path/to/continued-unsolved5.zip

The binding covers this audit's report, status, clarifications, source-inspection metadata, checker, results, and replay script. It records the exact input archive and member list. Original source PDFs, extracted source text, screenshots, private catalogues, and coordination material are excluded. No helper reviewer or remote write was used. Live repository/campaign duplicate checks, administrative accounting rules, and the full external theorem proofs were not independently certified.

## Publication wording

A suitable summary is: "Partial progress: the half-canonical Yoneda algebra for the two Springer components of the resolved (2,2) slice is abstractly isomorphic, as a cohomologically graded algebra, to the two-matching arc algebra. The argument uses published one-sided module comparisons, proper-support duality, and a two-object rigidity lemma. The general weighted all-k comparison remains unresolved in this investigation after five approaches."
