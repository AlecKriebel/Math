# Independent mathematical acceptance report

Date: 14 October 2026 UTC.

Subject: *A direct all-assignment certificate for the four-ray drawings of K(3,n) and K(4,n)*, `PROOF.md`.

Reviewed version: `6ec0d8fbf2e583e02fd775e24be762144d09ae3e8de9a835a80856e27527746e` (SHA-256; 15940 bytes).

## 1. Verdict and exact scope

**ACCEPTED.** The proof establishes Székely's exact universal set-system inequality for the specified integer-coordinate four-ray drawings of K(3,n) and K(4,n), for every integer n >= 3. The respective crossing counts are

    q(n) = floor(n/2) floor((n-1)/2),
    2 q(n).

The argument is uniform in n, covers every simultaneous choice of all sets A_e, and does not use a small-instance calculation or an ordinary-crossing lower bound as a substitute for the required criterion. No mathematical gap was found.

This accepts a nonplanar structured-family certificate. It does not establish the corresponding assertion for arbitrary K(m,n), a classification of every graph admitting a certificate, a certificate for arbitrary drawings, or a priority claim. The bare existential wording of the original source already has previously known nonplanar positive cases.

## 2. Independent checks of the mathematical argument

### 2.1 The indexed objects and the target inequality

An unordered independent edge pair in K(m,n) consists of two distinct X-endpoints, two distinct Y-endpoints, and one of the two matchings between these endpoint sets. Therefore the full index set has exactly

    2 binom(m,2) binom(n,2)

members. This gives six eligible independent pairs for each Y-pair when m=3 and twelve when m=4. Adjacent edge pairs are never included.

For each indexed pair, the proof defines b = c xor p, where c is the crossing indicator of the specified drawing and p is the full endpoint-set parity from the question. If N_ij counts pairs with c=i and p=j, then

    wt(b) - wt(c) = N_01 - N_11.

Thus the proved Hamming-weight inequality is exactly the requested inequality, with the correct direction and without a factor-of-two ambiguity.

### 2.2 Explicit geometry and every niceness condition

The X-coordinates are the nonzero integers on the horizontal axis split into floor(m/2) negative and ceil(m/2) positive positions. The Y-coordinates are similarly split on the vertical axis. Vertices are distinct; the origin is not a vertex. Every segment interior lies in an open quadrant, avoiding all vertices and the axes.

Pairs of interiors in different quadrants are disjoint. For vertices (u,0), (U,0), (0,v), (0,V) in a single reflected quadrant, with 0 < u < U and 0 < v < V, the intersecting matching has intersection

    x = u U (V-v)/(U V-u v),
    y = v V (U-u)/(U V-u v).

The denominator is positive. Direct subtraction gives x < u and y < v, while both coordinates are positive. The point lies in both relevant segment interiors. The other matching is disjoint by comparison with the outer line x/U+y/V=1. These observations prove both directions of the asserted crossing-pair characterization.

Distinct edges have distinct supporting lines whenever their interiors could meet. Two adjacent segments therefore have no common interior point, and two independent segments meet at most once. Any interior intersection of distinct straight lines is transverse.

The no-triple-crossing argument uses the special scope m=3,4 in an essential and valid way. A triple interior intersection would lie in a single quadrant. Its three edges could not share any X-endpoint, because adjacent edges have disjoint interiors. It would therefore require three X-vertices on that quadrant's horizontal ray. There are at most two. This contradiction proves that these exact integer coordinates already give nice drawings; an unstated generic perturbation is unnecessary.

Consequently the drawing has exactly

    [binom(floor(m/2),2)+binom(ceil(m/2),2)]
    [binom(floor(n/2),2)+binom(ceil(n/2),2)]

crossing pairs and the same number of geometric crossing points. For m=3,4 the first factor is respectively 1,2, and the second equals q(n). The count is positive at every n >= 3 and unbounded over the family.

### 2.3 Simultaneous-assignment parity on each K(3,3)

Every three chosen X-vertices occupy the two rays in a 1+2 split, including every left triple of K(4,n). A right triple occupies its two rays with r and 3-r vertices. Its baseline crossing count is

    binom(r,2)+binom(3-r,2),

which is either 1 or 3. The baseline sum over all unordered independent edge pairs in this K(3,3) is therefore odd.

Now regard every allowed incidence z_e(v), expressing v in A_e, as an independent Boolean variable. In the sum of p over an induced K(3,3), a variable with e or v outside the subgraph has coefficient zero. For e inside and v a nonendpoint vertex inside, its coefficient equals the number of independent partner edges f incident with v. If v is on the X-side, its partner endpoint can be either of the two Y-vertices other than e's Y-endpoint. If v is on the Y-side, the same count holds with the sides exchanged. The coefficient is exactly two in both cases.

All coefficients thus vanish modulo 2. This is a polynomial identity in all incidence variables, so overlapping or cancelling effects of different choices introduce no missing compatibility condition. It is not merely a verification of one switch at a time. Combining it with the baseline parity gives an odd sum of b on every such K(3,3), for every global assignment.

This step proves precisely the parity property the subsequent lower bound needs. It does not assume an independent-odd optimum or a restriction on competing topological drawings.

### 2.4 The K(3,n) lower bound

Group the b-bits by their unordered Y-endpoint pair and let w_yz be the resulting nonnegative integer weight. Every independent pair enters exactly one group, so their sum is wt(b).

For every right triple {y,z,t}, the preceding parity identity becomes

    w_yz + w_yt + w_zt = 1 modulo 2.

Hence at least one of these weights is positive. The support graph of the positive weights meets every triple; its complement F is triangle-free. Since each supported pair contributes at least one to wt(b),

    wt(b) >= binom(n,2) - |E(F)|.

The included proof of Mantel's bound is correct. For every edge uv of F, the open neighborhoods of u and v are disjoint, so d_u+d_v <= n. Summing over edges gives sum d_v^2 <= n|E(F)|. The square-sum inequality then gives 4|E(F)|^2 <= n^2|E(F)|. The zero-edge case is treated separately before division, and integrality gives |E(F)| <= floor(n^2/4). Therefore

    wt(b) >= binom(n,2)-floor(n^2/4) = q(n) = wt(c).

The arithmetic identity holds for both n=2k and n=2k+1. This argument establishes the desired bound for every n >= 3; no finite enumeration is needed.

The optional algebraic verification also checks independently. Writing r_yz=w_yz modulo 2, the triangle identities imply r_yz=1+t_y+t_z for a suitable Boolean vertex labeling. Therefore all pairs within either label class have odd, hence positive, weight. If the class sizes are s and n-s, this gives wt(b) >= binom(s,2)+binom(n-s,2), minimized at a balanced split. Its minimum is q(n). The definitions also verify the formula for pairs containing the chosen reference vertex.

### 2.5 The K(4,n) restriction and exact multiplicity

For each of the four three-element subsets T of X, restricting A_e to the vertices of K(T,Y) preserves p on every independent edge pair of that subgraph: all endpoints contributing to p already lie in that vertex set. Its crossing bits are exactly the restriction of the original drawing. The K(3,n) argument remains applicable because it uses the 1+2 ray split and order, not the particular consecutive X-radii.

Each restriction has weight at least q(n). An independent pair in K(4,n) has two X-endpoints and belongs to precisely two left triples, one for each choice of a third vertex among the two remaining X-vertices. Thus

    2 wt(b) = sum over the four left triples of their restricted weights
            >= 4 q(n).

No independence among the four restricted assignments is assumed or needed. The conclusion wt(b) >= 2q(n) matches the exact drawing count and proves the universal criterion.

## 3. Published-theorem interface

Székely's Theorem 1 in *An Optimality Criterion for the Crossing Number* explicitly quantifies over all edge-to-vertex-set assignments and sums over unordered nonadjacent edge pairs. It equates this criterion for a normal drawing with independent-odd crossing optimality, and adds ordinary crossing optimality for a nice drawing. The definitions and theorem were independently checked in the primary paper, printed pp. 32–34.

The proof meets these hypotheses. Its drawing is nice, and it proves the universal inequality directly. It is therefore justified to conclude

    iocr(K(3,n)) = cr(K(3,n)) = q(n),
    iocr(K(4,n)) = cr(K(4,n)) = 2q(n).

The unrestricted class of normal comparator drawings, including possible adjacent or repeated crossings, is handled by the cited equivalence. The proof never silently replaces that class by straight-line or nice comparator drawings.

Primary reference: [Székely, AMC 1 (2008), 32–37](https://amc-journal.eu/index.php/amc/article/download/43/30), [DOI](https://doi.org/10.26493/1855-3974.43.506).

## 4. Source scope and attribution

The original Oberwolfach question asks for theoretically verifiable graph examples and suggests the Zarankiewicz drawing; it does not require an all-K(m,n) theorem or a complete classification. The exact wording and neighboring section boundary were checked in the source's printed p. 983. A verified infinite family therefore answers that existential scope, provided the narrower scope and prior positive cases are disclosed. [Oberwolfach Report 17/2005](https://ems.press/content/serial-article-files/45990?nt=1).

The criterion itself, the four-ray construction, the numerical crossing counts, and Mantel's bound are credited as existing mathematics. Eppstein's primary paper was checked at Lemma 1 and its surrounding discussion, printed pp. 466–468. It describes the classical axes construction and credits Zarankiewicz and Kleitman for its related pair-crossing argument. The present proof correctly distinguishes that pair-crossing result from the stronger all-assignment verification. [Eppstein, *The Effect of Planarization on Width*](https://jgaa.info/index.php/jgaa/article/download/paper468/2483/2290).

Known nonplanar existential examples are explicit in Sections 1 and 9 of the accepted version. Pelsmajer, Schaefer and Štefankovič's *Removing Even Crossings*, Theorem 1.2 and Remark 1, records iocr(K5)=iocr(K3,3)=1 and credits Székely's earlier algebraic treatment. Those passages were independently checked in the author manuscript. Combining these known values with one-crossing nice drawings and Székely's criterion already supplies nonplanar existential positives. [Author manuscript](https://ovid.cs.depaul.edu/documents/tutte.pdf), [published article DOI](https://doi.org/10.1016/j.jctb.2006.08.001).

No priority conclusion is inferred from a bounded literature search. No unreviewed general ordinary-crossing manuscript is used as an input. The accepted result is the direct, family-specific certificate presented here.

## 5. Acceptance gates and verification limits

- Exact family, drawings and full parameter range: passed.
- All normality and niceness conditions, including triple intersections: passed.
- Exact independent-pair indexing and crossing count: passed.
- Every simultaneous A_e assignment: passed.
- Correct invariant and unrestricted-comparator interface: passed.
- Uniform theoretical argument, without exhaustive checking: passed.
- Noncircular lower bound: passed.
- Prior credit and explicit known existential positives: passed in the final bound version.
- Scoped conclusion without all-K(m,n), classification or novelty claims: passed.

This report accepts the mathematical text identified by its final SHA-256. Any supplemental numerical checks are corroborative only and are not necessary premises of this acceptance. A later substantive mathematical edit requires a new version comparison; the hash identifies bytes and does not itself establish correctness.

## 6. Final version binding

The complete final proof was read again after the attribution additions. Sections 1 and 9 now explicitly disclose the known K5 and K(3,3) positive cases and their source. The mathematical argument remains valid. The final frozen file has 15940 bytes and SHA-256 `6ec0d8fbf2e583e02fd775e24be762144d09ae3e8de9a835a80856e27527746e`. All acceptance gates listed above pass for those bytes. No outstanding mathematical or acceptance-scope issue remains.
