# Independent audit of the Whitney umbrella investigation

## Verdict

**Accept the elementary partial results, with one required scope clarification and one minor wording correction. Keep the full target unsolved in this investigation.** No complete arbitrary-group construction, counterexample group, or verified prior resolution has been established. The 2016 announcement discrepancy must remain visible.

This audit independently examines the frozen five-approach packet for problem 30002526 / OWR-12869-003, rank 625. It is verification of those approaches, not a sixth proof-search attempt. The frozen SHA256SUMS digest is `e468ff6825bd523f60483c9bb812a577a6724a03684b75205f70340e7ffc1c8f`. All seven listed files match. The author program replays byte-for-byte, with 506 assertions, including 481 bounded parity checks. The independent program adds 93 top-level assertions, using different checks and no author-module imports. Counts describe checks, not mathematical significance.

The audit's one required qualification is that the Bierstone–Milman obstruction concerns **proper** birational modifications preserving the normal-crossing locus. Unrestricted birational morphisms would include the open immersion obtained by deleting the pinch point. This correction does not invalidate the intended blowup-route obstruction. The second correction replaces the categorical wording that a covering changes the group by the precise statement that group preservation is not automatic.

## Exact target and source scope

The target is a reduced irreducible complex projective surface W with ordinary topological fundamental group equal to any prescribed finitely presented G, and only analytic normal-crossing singularities. For a surface the permitted local models are smooth, xy=0 in three coordinates, and xyz=0 in three coordinates. This agrees with the question following Theorem 0.7 on printed page 542 of the [2014 Oberwolfach report](https://ems.press/content/serial-article-files/46500). The source page was independently read and visually checked.

Global irreducibility is compatible with analytically reducible germs. Substituting simple normal crossings would materially change the target: the irreducible components of a simple-normal-crossing variety are smooth, so an irreducible such variety is smooth. This distinction is handled correctly in the packet.

[Kapovich's published Theorem 1.2](https://www.math.ucdavis.edu/~kapovich/EPR/tiling.pdf) admits Whitney umbrellas for general G; its NC-only clause has the compact hyperbolic 3-manifold hypothesis, with possibly empty convex boundary. [Kapovich–Kollár Theorem 2](https://www.math.ucdavis.edu/~kapovich/EPR/jams807.pdf) gives arbitrary G with a reducible projective SNC surface. Neither directly supplies the requested conjunction. The centerless-kernel assumption in Kapovich Proposition 4.13 is explicitly recorded in the author's source file; no unsupported general quotient comparison was used in the partial results.

The official [UC Davis announcement dated 19 April 2016](https://mass.math.ucdavis.edu/research/seminars?talk_id=4608) and [Vienna announcement dated 9 December 2016](https://mathematik.univie.ac.at/en/eventsnews/full-news-display/news/fundamental-groups-of-complex-projective-varieties/?cHash=ab87c7dd536220f1aefd91a80eca754d&no_cache=1) both announce arbitrary-group irreducible NC-only projective realization. Neither checked abstract supplies a proof or explicitly fixes dimension two. The author-hosted [research statement](https://www.math.ucdavis.edu/~kapovich/statement.pdf), dated 13 October 2019 on its first page, retains Whitney umbrellas in Theorem 15 for arbitrary G. Its later date is not evidence of a retraction. The bounded recheck did not locate a proof explaining the announcements; it does not prove the absence of one. `already_solved` is therefore unverified, while categorical current-literature openness is also unverified.

## Quotient algebra and stabilizer relations

The invariant computation is correct. An independent derivation works directly in A=C[x,y,z]/(xy), avoiding reliance on the author's Reynolds-operator presentation. A vector-space basis consists of z^k, x^i z^k and y^i z^k for i>=1. The involution sends z to -z and exchanges x and y. Its invariant basis consists of:

- z^(2j);
- (x^i+y^i) z^(2j), for i>=1;
- (x^i-y^i) z^(2j+1), for i>=1.

With s=x+y, b=z(x-y), and c=z^2, these are respectively c^j, s^i c^j and s^(i-1)b c^j, since mixed x,y monomials vanish. This proves generation in every degree. The relation is b^2=c s^2. There are no further relations: reduce powers of b to exponent 0 or 1; substituting s=u, b=ut, c=t^2 gives distinct monomials u^(i+epsilon)t^(2j+epsilon). The parity of the t exponent recovers epsilon, followed by i and j. Thus the quotient presentation is injective as well as surjective.

The exact prequotient identity is [z(x-y)]^2-z^2(x+y)^2=-4z^2xy. The independent control verifies it on a sufficient exact interpolation grid with coordinate-degree bounds (2,2,2), and checks a counterexample to the missing-factor version. The published formula in Lemma 4.12 is also correct: its displayed parentheses place the factor y3^2 outside the entire difference. PDF text extraction can obscure those parentheses. This audit does **not** allege a missing-factor error in the published paper.

The alternate involution fixing z has invariant ring C[s,z], and its reduced fixed locus contains the whole double curve. It is genuinely a different action. The author correctly leaves the global replacement unsupported.

The topology control R^3/{v~-v} is the cone on RP^2, whereas its punctured version retracts to RP^2. It correctly illustrates loss of an order-two relation. It is not a projective global counterexample. A torsion-free discrete action on H^3 has a manifold quotient with that acting group as fundamental group, so it cannot directly realize G=Z/2. This blocks the universal torsion-free shortcut without excluding Z/2 from the actual NC projective target.

The phrase that a covering changes the group should be weakened: a connected covering injects its fundamental group as a subgroup of the base group, but the two groups can be abstractly isomorphic. The double cover S^1 to S^1 already illustrates this. The intended need for a separate group-identification argument is valid.

## Point blowups and the conductor

For F=v^2-wu^2, the three point-blowup charts are as follows, after removing the exceptional square factor:

- u chart, v=ub and w=uc: b^2-uc=0;
- v chart, u=va and w=vc: 1-vca^2=0;
- w chart, u=wa and v=wb: b^2-wa^2=0.

The last chart reproduces the pinch point exactly. Thus repeatedly blowing up the surviving pinch cannot eliminate all non-NC germs. The other two charts are not silently discarded: the u chart contains a quadratic-cone singularity and the v chart is smooth, but neither changes the surviving pinch in the w chart. All three identities are independently checked.

The broader-center blowup of the ideal (u,v) has charts t^2-w=0 and 1-wr^2=0. The first is the affine plane with coordinates u,t. In the second chart r is invertible because wr^2=1, so this entire chart lies in the overlap with the first, with t=1/r. Consequently the intrinsic blowup is indeed the normalization, not merely a pair of unrelated smooth charts. Strict-transform computations agree with the intrinsic blowup because the chart rings are formed inside the common fraction field, removing the exceptional torsion.

For completeness, write B=C[u,t] and A=C[u,ut,t^2]. Then

    A = C[t^2] + u B.

Every monomial with positive u exponent belongs to A, while a monomial with u exponent zero belongs exactly when its t exponent is even. B is a finite A-module generated by 1,t and has the same fraction field, since t=v/u. Being integrally closed, B is the integral closure of A.

The conductor in B is uB. Indeed uB is an ideal of B contained in A. Conversely, for f in the conductor both f and tf lie in A. Reducing modulo u says that f(0,t) and t f(0,t) are even polynomials; hence f(0,t)=0. In A the same conductor is the ideal (u,v). The conductor map is C[w] to C[t], w=t^2, so its branch point is at zero. The independent BFS semigroup check confirms finite exponent controls; the displayed argument proves all degrees.

The monodromy of this conductor cover exchanges the two sheets over one circuit around w=0. [Bierstone–Milman, Question 1.2 and Example 1.7](https://arxiv.org/pdf/1107.5595) address proper birational repair preserving the NC locus. Properness must be explicit in the packet. Without it, X minus {0} is NC and its open inclusion into the pinch-point surface is birational and an isomorphism over X_NC, so the unrestricted assertion is false. With the qualifier, the source is used in its intended resolution setting. Blowing up the whole double curve falls outside the preservation hypothesis, exactly as the author says. None of this is a nonexistence theorem for other projective realizations.

## Square-root base change

After w=t^2 the two components v-ut=0 and v+ut=0 are individually smooth. Their normal rows are (-t,1,-u) and (t,1,u). The three two-by-two minors are -2t, 0 and 2u. Thus the sheets meet transversely precisely when (u,t) is nonzero. Their intersection has v=0 and ut=0; away from the origin its points are ordinary double crossings, but the origin is not NC. Equivalently, its quadratic tangent cone is the doubled plane v^2=0, whereas an ordinary double crossing has two distinct tangent planes. An analytic coordinate change cannot repair this tangent-cone defect.

The base-changed scheme is reduced, since its two distinct factors are coprime in the polynomial UFD, but its normalization is the disjoint union of the two smooth sheets. That loses local connectedness. The original conductor map is ramified; an étale neighborhood at a complex point cannot change its analytic local isomorphism type. The author makes neither a false étaleness assertion nor an unjustified descent claim.

## Nodal cubic and smoothing topology

The cubic C_0 is irreducible: x^2(x+1) is not a square in C(x), because the valuation of x+1 at x=-1 is odd. Its only affine singularity is (0,0), the quadratic part is y^2-x^2, and the point at infinity [0:1:0] is smooth. The parametrization by homogeneous cubics has no base points: T nonzero makes T^3 nonzero, and T=0 makes the middle coordinate S^3 nonzero. The equation is satisfied identically.

On T=1, x=s^2-1 and y=s(s^2-1). If x is nonzero then s=y/x; if x=0 then s=+1 or -1 and both map to the node. Infinity has one preimage. A nonconstant morphism of these projective integral curves is proper and quasi-finite, hence finite. It is birational, so it is the normalization. A continuous surjection from compact P^1(C) to Hausdorff C_0(C) realizes the latter as the quotient of S^2 identifying exactly two points.

The fundamental group claim is verified independently by a CW presentation. Use a tetrahedral sphere and identify vertices 0 and 1; retain all edges, including loop 01. Collapse the maximal tree with edges 02 and 03. The remaining generators a=01,b=12,c=13,d=23 satisfy

    ab=1, ac=1, d=1, bdc^(-1)=1.

The first three eliminate b=c=a^(-1), d=1, and the fourth is redundant. The result is the free group on a, namely Z. The independent cellular boundary matrices give Betti numbers (1,1,1), providing a separate homology control; homology is not being substituted for the presentation argument.

Products preserve the asserted facts: C_0 times P^1 is irreducible and projective of dimension two, and its singular germs are a node times a smooth curve. Its fundamental group is Z. The normalization P^1 times P^1 is simply connected. This verifies the failure of blanket pi_1 preservation by normalization in the required projective setting.

For C_e, a repeated affine root occurs only at x=0 or x=-2/3, giving e=0 or -4/27. Infinity remains smooth. For other e this is a smooth plane cubic, of genus one and fundamental group Z^2; multiplying by simply connected P^1 does not change that group. The homogeneous cubic family is projective and flat: it is a relative effective Cartier divisor of degree three in P^2 over the parameter line, with the same nonzero defining degree on every fiber. Thus the example is a genuine smoothing control, not just a comparison of unrelated curves. It refutes a general smoothing-invariance principle, not every selective pinch-point deformation.

Finally, even b1 for smooth complex projective varieties follows from Hodge symmetry in degree one. G=Z therefore blocks an attempt to make all realizations smooth. The author correctly avoids extending this obstruction to singular NC surfaces; its own example disproves that extension.

## Global gluing gap

No shortcut closes the principal gap. Connected smooth normalization is sufficient for irreducibility here, since irreducible components of a regular complex variety are disjoint; a connected one has only one component. But abstract connectedness or a desired dual presentation does not construct the algebraic quotient.

The missing data remain conductor divisors on that normalization, compatible identifications and relations, local NC completed rings including triple points, existence of the quotient, an ample descended line bundle, and an actual fundamental-group calculation. The reducible SNC theorem has a disconnected normalization and does not itself provide such self-gluing on one irreducible normalization. The packet explicitly stops before claiming any of these missing general steps. No hidden full solution was found in its controls or prose.

## Reproducibility and disposition

Run `python3 verify_audit.py` for independent checks alone. With the original packet available, run `python3 verify_audit.py --author-dir ../author` and compare the JSON output with `audit_control_results.json`. The latter also verifies the original manifest and the exact author replay. `author_control_replay.json` is the captured deterministic output, not a new proof certificate.

The recommended correction patch is un-applied; frozen originals remain untouched. The audit packet contains only authored review, bibliographic summaries and links, code, control output, and manifests. It contains no source PDFs, full source text, imported problem corpus, or private coordination inventories. No remote writes, external communications, additional helpers, or queue mutations occurred in this audit.

Disposition: retain five approaches and the conservative non-resolution status. Accept the checked partial results subject to the properness clarification; incorporate the covering wording correction when publishing a revised copy. Preserve the stronger-announcement caveat. The 5% full-target completion estimate remains an uncalibrated planning judgment, not a probability of success or a mathematical certificate.
