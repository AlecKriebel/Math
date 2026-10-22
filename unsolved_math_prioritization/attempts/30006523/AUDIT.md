# Audit of the Schubert support skew sum reduction

## Verdict

**Accept the restricted mathematical results in the frozen candidate. No correction is required.** The exact skew-sum support factorization, the equivalence of left-weak convexity with convexity of both factors, the skew-indecomposable minimal-counterexample reduction, the Boolean family, and the stated shortcut obstructions are valid. The general Schubert-support convexity conjecture is not proved or disproved by these materials. This acceptance makes no claim of novelty or of present-day openness.

The accepted original report has 15,445 bytes and SHA-256 `937ab7e160c9515590da7ab8938a3103dc50dc83b3bbca33bfc6bfc44f4c2f34`; its 33-member candidate manifest has 7,558 bytes and SHA-256 `065800329296eac09f826392cb44d3c44563bdbe7ca402954114c34add16b043`. The original independent audit has 17,469 bytes and SHA-256 `9ac59b1fd55643b9febd096394ea253c1125238a9e3fdb87810cd525414e9f0d`; its 12-member manifest has SHA-256 `42167dd888f7f2e7cd460da9b29cbe00ba26e7d54a10c240501d72772045a351`. These identify the accepted originals; ACCEPTANCE.json separately binds this edited public edition. No accepted input was changed.

This audit independently reconstructed all 873 expansions in S1 through S6, without reading candidate code as implementation source or executing/importing candidate or paper-author programs. The source PDFs and candidate certificates were read as evidence or data. Finite testing is supporting evidence; the universal theorem is accepted on its written proof.

This AI-assisted manuscript is unrefereed. Acceptance means an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The complete written universal proofs and displayed analytical identities are retained. This is not a computational reproduction package: raw expansion datasets, detailed computational certificate tables, executable code, copied source documents and images, and private coordination material are omitted. Historical finite checks support the work but are not premises of the universal theorem. The exhaustive finite checks cannot be reproduced from this edition alone.

The general Schubert-support left-weak convexity conjecture remains unresolved by this work. No novelty, priority, exhaustive literature survey, or current-openness claim is made.

## Target statement and source check

The target is Conjecture 3 in Anna Weigandt's contribution, joint with Judy (Hsin-Hui) Chiang, *On the Schubert Support of Grothendieck Polynomials*, printed pages 132-133 of *Enumerative Combinatorics*, Oberwolfach Report 2/2026, [DOI](https://doi.org/10.4171/owr/2026/2). The audited statement concerns the Schubert-basis support of an ordinary Grothendieck polynomial and intervals in **left weak order**. It does not concern convexity of monomial exponents, Bruhat convexity, or right weak order. Both contribution pages were freshly extracted from the authenticated retained PDF and read in full; both supplied page renderings were visually inspected. The DOI web open failed, so this audit does not claim a fresh online download of that PDF.

The paper *Changing Bases with Pipe Dream Combinatorics*, [arXiv:2506.07306v1](https://arxiv.org/abs/2506.07306v1), supplies the operator conventions, stability, an existing example, and a separate pipe-dream formula. The retained 54-page PDF has internal date June 10, 2025, while its arXiv v1 submission was June 8, 2025. The abstract page was independently opened online. The local PDF's relevant text and page 10 rendering were inspected. The sentence just before displayed equation (2.1) has the ascent inequality in the wrong direction. Equations (2.1)-(2.2), the longest-permutation initial value, and nilpotence/idempotence remove the ambiguity. The candidate explicitly notices this issue and uses the correct descent convention. No newer or dynamically substituted HTML version was used as mathematical authority.

Example 1.4 of this v1 paper already gives the displayed expansion of G2143. The candidate correctly attributes it. The Oberwolfach contribution claims its three conjectures in the Grassmannian and 1 times dominant cases; its inverse-fireworks statement covers only the first two conjectures. The audit verifies this distinction, without independently proving those source-reported families.

The independently opened [Chiang research page](https://sites.google.com/view/judy-chiang/research) lists the joint Schubert-support project as a paper in progress. This is only a public manuscript-status observation. It proves neither openness nor novelty.

## Conventions and ambient polynomial ring

Composition is (ab)(i)=a(b(i)). Right multiplication by s_i swaps adjacent positions i and i+1. Left multiplication swaps the two values i and i+1 wherever they occur. In particular, the indices for the differential operators are position indices, whereas increasing left-weak chains use value swaps.

Write Inv(w)={(r,s): r<s and w(r)>w(s)}. With this position-pair convention,

    a <=_L b  iff  length(b)=length(a)+length(b a^{-1})
              iff  Inv(a) is contained in Inv(b).

For clarity, one can see the inversion implication without switching conventions. An increasing adjacent-value swap adds exactly the inversion between the positions of those two values. Conversely, suppose Inv(a) is contained in Inv(b) and a differs from b. The sequence b(a^{-1}(1)),...,b(a^{-1}(n)) is not increasing. Choose an adjacent descent in this sequence, say at i. The positions of i and i+1 in a must occur in increasing order, since otherwise the assumed inversion inclusion would force the opposite inequality in b. Swapping those two values in a therefore adds one inversion present in b. Repeating reaches b. This proves the chain characterization. Right weak order instead uses inverse-permutation inversion sets, or length(a^{-1}b).

The operators are ordinary polynomial operators

    partial_i f=(f-s_i f)/(x_i-x_{i+1}),
    pi_i f=partial_i((1-x_{i+1})f)=f+(1-x_i)partial_i f.

They act by the usual right-descent recurrences on S_w and G_w. At the longest permutation in S_n both initial polynomials are x_1^(n-1)...x_(n-1). No reduction modulo symmetric polynomials is used anywhere.

The finite module M_n spanned by x^a with 0<=a_i<=n-i has n! monomials. The standard leading-monomial theorem for Schubert polynomials gives lexicographically least monomial x^code(w), with coefficient one. Lehmer codes biject S_n with these exponent vectors, so the S_w for w in S_n are an integral unitriangular basis of M_n. The triangular pipe-dream formula also directly places both S_w and G_w in M_n: row i has only n-i possible crossings. Thus the finite expansion is the unique stable Schubert expansion. As a separate source check, Theorem 1.1 in the v1 paper already expands G_w using n-pipe objects whose indices are in S_n. It independently supports the absence of missing larger-index terms.

Appending a fixed largest letter preserves both polynomial families, as explicitly stated after (2.2) in the v1 paper. If an upper endpoint belongs to S_n, inversion containment forbids an intermediate finite permutation from having a crossing inversion involving a position greater than n or an inversion within that tail. Its eventually fixed increasing tail must therefore be the identity tail. Accordingly, intervals with endpoints in S_n do not acquire extra elements in S_infinity. The candidate's finite and stable statements are consistent.

## Universal skew sum proof

Let a in S_p and b in S_q, and define a skew b=(q+a(1),...,q+a(p),b(1),...,b(q)). Put X=(x_1,...,x_p), Y=(x_(p+1),...,x_(p+q)), and R=(x_1...x_p)^q.

The longest permutation in S_(p+q) is the skew sum of the two longest block permutations. Its defining monomial is precisely R times the product of the two block defining monomials. Reduce the first and second block permutations separately from their longest permutations by right descents. These moves use positions i<p and p+j with j<q; they never use the boundary position p. Each remains a descent in the full skew sum.

For a first-block move, R is symmetric in the two relevant variables and the second block polynomial is independent of them. For a second-block move, R and the first block polynomial are independent of the two variables. Both partial_i and pi_i commute with multiplication by any polynomial symmetric in those two variables, directly from their definitions. Applying all chosen right-descent operators therefore proves the ordinary polynomial identity

    H_(a skew b)(X,Y)=R H_a(X) H_b(Y),  H=S or G.

There is no unsupported assumption about support in this proof, and no coinvariant multiplication. The two occurrences of the same rectangle monomial in the Schubert and Grothendieck factorizations are essential and correct.

Now let B_(p,q) be the permutations whose first p positions contain exactly the largest p values. In every such permutation, q+1 occurs before q, so left multiplication by s_q decreases length. All other left simple reflections preserve the two value blocks. An increasing left-weak chain starting in B_(p,q) remains there, proving that B_(p,q) is an upper ideal in S_(p+q).

Within this ideal, s_(q+i) acts on the first factor and s_j on the second. Also,

    length(a skew b)=pq+length(a)+length(b).

Every increasing step changes exactly one factor by an increasing left-weak step. Conversely, increasing factor chains can be interleaved. Hence the skew-sum map identifies the product order on S_p times S_q with this upper ideal, and every interval between two skew-sum endpoints is the product of the corresponding factor intervals.

If G_a=sum A_u S_u and G_b=sum B_v S_v, substitute in the G factorization and use the S factorization term by term:

    G_(a skew b)=sum_(u,v) A_u B_v S_(u skew v).

Distinct pairs have distinct skew sums. Since the coefficients are integers, A_u B_v is nonzero exactly when both factors are nonzero. Thus there is no cancellation between different pairs, and support is exactly the embedded Cartesian product. The interval formula proves that convex factors have convex product. For the converse, fix any supported second factor and test intervals with that factor held constant; convexity forces the first support to be convex. Interchanging the factors proves the other implication. Their supports are nonempty because each G has lowest homogeneous component S at its index.

This establishes the stated equivalence for every p,q>=1. If a counterexample of smallest permutation size were a nontrivial skew sum, at least one smaller factor would already be a counterexample, a contradiction. The minimal-counterexample reduction is therefore valid.

## Boolean family

The defining recurrence gives G132=x_1+x_2-x_1 x_2=S132-S231. The interval [132,231]_L consists of those two elements. Applying the skew theorem repeatedly makes the support of an r-fold skew sum of 132 the product of r two-element chains. It is an interval isomorphic to the Boolean lattice and contains exactly 2^r elements. The coefficient is (-1) to the number of 231 factors. For r=2 the index is 465132 and the four terms are exactly

    S465132 - S465231 - S564132 + S564231.

This is an unbounded proved family. It carries no novelty assertion.

## Exact shortcut obstructions

For the stronger example, S1243=e_1(x_1,x_2,x_3), S1342=e_2, and S2341=e_3. Hence

    G1243=S1243-S1342+S2341,
    F=S1243-S1342+2 S2341=G1243+x_1 x_2 x_3.

The support interval is the three-element chain 1243<1342<2341, with successive left generators s_2,s_1. Every term has right descent set {3}. The input has the same support, alternating coefficient signs, unique lowest-degree Schubert term, and descent restriction as G1243. Its monomial signs also alternate with degree.

Direct calculation gives pi_3 G1243=1 and pi_3(x_1 x_2 x_3)=x_1 x_2. Therefore

    pi_3 F=S1234+S2314.

The intermediate element 1324 of 1234<1324<2314 is absent. The input invariants cannot force convexity after pi_i without further coefficient information. F is not any G_v: its lowest homogeneous component is S1243, which would force v=1243, but its degree-three coefficient differs from G1243. Thus this is only an obstruction to the proposed general induction shortcut, never a counterexample to the target conjecture.

The earlier S3 control was independently confirmed as well: S132-S231+S321 maps under pi_2 to S123+S312, omitting 213 between the output endpoints.

The already published example

    G2143=S2143-S3142-S2341+S3241

has two left-weak minimal support elements, 2143 and 2341. The position inversion (1,2) belongs to 2143 and not to 2341. A support need not be one interval or lie above its original index. This support is nevertheless convex.

The complete ten-term expansion for G13254 in the candidate was reconstructed exactly, including the coefficients +2 at 23451 and -2 at 24351. Its terms 13452 and 34152 have nonzero coefficients, while 31452 does not. The right-position swaps s_1 then s_2 give increasing covers 13452<31452<34152 of lengths 3,4,5. This disproves right-weak convexity. The endpoints are left-incomparable, so it does not contradict the target statement.

Finally, if i is a right ascent of w, pi_i G_w=G_w. The polynomial identity for pi_i gives (1-x_i)partial_i G_w=0; the ordinary integral polynomial ring has no zero divisors, so partial_i G_w=0. In the Schubert expansion, partial_i kills right ascents and sends each right descent u to the distinct index u s_i. Linear independence therefore forces all such coefficients to vanish. This proves Des_R(u) is contained in Des_R(w) for every supported u. The stronger example satisfies this input restriction and still defeats the shortcut.

## Independent exact computation and limits

The independently authored historical checker uses Python's standard library and sparse integer polynomials. It was written without inspecting the candidate's implementation. It constructs polynomials downward from the longest element, choosing the last available right ascent in the recursive reverse step. Every computed divided difference is checked by multiplying back the denominator. A separate column-first triangular pipe-grid sweep, using the exact reading order in the primary source, aggregates all subset choices by right Demazure products. A selected descent contributes the negative excess-crossing sign; reduced-pipe transitions permit only ascents. This implementation differs from the candidate's described exhaustive row-first subset enumeration.

Schubert expansions are obtained by exact integral leading-monomial elimination. All candidate expansion certificates are consulted only after the corresponding entire group has been independently reconstructed. In S1 through S5, an additional right-descent operator word extracts every Schubert coefficient as a constant term. No candidate program is used for this secondary check.

All three final runs, ordinary Python, -O and -OO, pass and give identical substantive JSON after removing the optimization-mode field. Checks use explicit exceptions, never Python assert statements.

Final independent scope:

- 873 permutations: every element of S1 through S6.
- 1,746 complete recursive-versus-pipe polynomial matches.
- All 873 Schubert expansions independently reconstructed and compared with the candidate data.
- All 873 left-convexity checks pass; all supports satisfy the right-descent restriction.
- 533,417 ordered pairs checked by three equivalent left-order descriptions: increasing value-swap reachability, position-pair inversion containment, and the length formula.
- 8,332 operator identities across all right simple edges, covering both descent and ascent branches for S and G.
- 15,017 dual coefficient comparisons, covering every pair in S1 through S5 only.
- 306 polynomial stability checks, covering both families and all indices in S1 through S5 only.
- 930 exact skew polynomial factorizations and 465 exact skew coefficient factorizations, for all positive block sizes with p+q<=6.
- 5,447 upper-ideal members checked in those skew tests, together with both directions of the product-order formula.
- 83,859 exact divided-difference numerator checks in each final run.

The S6 dual-extraction suite and the candidate's S6-to-S7 stability checks were not rerun. This audit therefore does not adopt every count in the candidate's secondary-control report as independently reproduced. It independently reproduces all 873 expansions by a different polynomial construction and verifies the explicitly listed scope. It does not audit performance, prove correctness of the candidate's source code, or turn finite evidence into an unbounded proof.

Semantic negative controls detect substitution of partial_i for pi_i, alteration of the decisive coefficient magnitude, insertion of the omitted middle coefficient, deletion of a true interval's middle, the principal-upper-set shortcut, and use of right weak order. The examples are checked through exact polynomial identities, not numerical evaluation.

## Integrity, edition, and reproduction scope

The historical independent inventory checks authenticated exact candidate membership, safe paths, byte lengths, SHA-256 values, and absence of symlinks against an external manifest digest. Disposable-copy controls rejected a changed byte, missing or extra member, symlink substitution, altered manifest, and coordinated member-plus-manifest resealing. These checks passed under normal Python, -O, and -OO. Original candidate and audit inventories were separately reauthenticated during edition preparation without executing their mathematical programs.

This edition retains the accepted mathematical statements and complete universal proofs. The displayed G13254 identity remains an independently checked finite premise for the right-order convention example; its full recursive calculation and computational certificate are not distributed. Reproducing it requires application of the stated recurrences. The universal skew-sum theorem does not rely on it. The F calculation and Boolean-family derivation are written out in PROOF.md.

The complete written universal proofs and displayed analytical identities are retained. This is not a computational reproduction package: raw expansion datasets, detailed computational certificate tables, executable code, copied source documents and images, and private coordination material are omitted. Historical finite checks support the work but are not premises of the universal theorem. The exhaustive finite checks cannot be reproduced from this edition alone.

This AI-assisted manuscript is unrefereed. Acceptance means an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The general Schubert-support left-weak convexity conjecture remains unresolved by this work. No novelty, priority, exhaustive literature survey, or current-openness claim is made.

Editorial preparation performed no new mathematical execution, scholarly-source retrieval, source text extraction, visual source inspection, or current-literature survey. The eight public authored files exclude all executable code, raw expansion datasets, computational certificate tables, copied sources/images, and private coordination. Acceptance is limited to the restricted results and the historical independent scope stated above.
