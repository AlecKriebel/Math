# Required source and statement repairs after independent review

2026-10-03. This repairs the frozen five-turn packet at commit 9eca3cd5e2c2ae85bfc933e5f0b58758bef748b7. All 32 original files are retained byte-for-byte. This is correction of statements and source attribution, not a sixth proof attempt. The original general conjecture remains unresolved; the corrected packet awaits explicit re-review.

## R1. Source Loewner definition: disclose the normalization

Kapovich's author-hosted problem list, printed/PDF page 11, Definition 2, visibly prints an upper-bound sign in its modulus inequality, and uses phi in the display but psi in the following line. We independently re-rendered and inspected that page after the reviewer flagged it. The literal displayed convention is not the one used by our proofs.

This packet interprets those inconsistencies as apparent typographical errors and uses the standard analytic Loewner lower bound

  Mod_Q(Gamma(E,F)) >= Psi(Delta(E,F)),

where Psi is positive and decreasing and E,F are disjoint nondegenerate continua. Here Delta(E,F)=dist(E,F)/min{diam E,diam F}, and Gamma(E,F) is the family of connecting curves. Bonk–Kleiner, Geometry & Topology 9 (2005), printed page 227, equation (2.6), explicitly states this standard convention. Our analytic deductions additionally retain an Ahlfors Q-regular representative in the boundary's quasisymmetric gauge and Q>1.

Sources:
- https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf, printed/PDF pages 11 and 13.
- https://arxiv.org/pdf/math/0208135, printed page 227, equation (2.6).

We do not derive results from a literal upper-bound condition, redefine Heinonen's intended conjecture, or use the apparent typo to manufacture a counterexample. The exact target remains surjectivity of every quasisymmetric self-embedding of the intended Loewner boundary. The source wording must be read with this disclosed normalization. All Q>1 qualifications and the absence of a full solution remain unchanged.

## R2. Corrected Turn 5 geometric theorem

The following statement replaces the geometric-certificate theorem in TURN_5.md. Its graph counting lemma remains unchanged. The original theorem omitted a logical link: the cell selected around a point of Y was not explicitly required to have a reachable safe state arising from its label. No porosity conclusion is accepted from that original statement without this repair.

### Complete hypotheses

Let X be a compact metric space with D=diam X>0, and let Y be a nonempty closed subset. Fix:

1. A finite alphabet Sigma of cardinality b>=2; a nonempty finite safe-state set S; an initial state s0 in S; and a total deterministic transition map delta on (S union {bottom}) times Sigma, with bottom absorbing. Write delta-star for the word extension of delta. Let R be the states in S reachable from s0 by a word whose run stays safe. R is finite and nonempty.
2. A prefix-closed collection W of existing cell words, containing the empty word, with cells C_w subset X. If wa belongs to W, then C_wa subset C_w. Each cell's state is exactly s(w)=delta-star(s0,w), so descendant labels and state transitions are compatible. There are constants A>0 and 0<rho<1 with diam C_w<=A rho^|w| for every existing cell.
3. For every y in Y, a selected infinite word alpha_y such that every prefix w=alpha_y|k belongs to W, contains y in C_w, and has s(w) in S, for every k>=0. Thus every cell used to choose a scale around y has a state in R. These safe coding chains are a geometric hypothesis, not a conclusion of the automaton.
4. Every s in R can reach bottom. For each s choose one shortest escape word e_s; put l_s=|e_s| and N=max_{s in R} l_s. Then 1<=N<=|R|<=|S| by the graph argument below.
5. There is c0>0 such that for every prefix w of any selected chain in (3), the descendant cell C_(w e_s(w)) exists. It has a separately verified ambient-metric certificate: some z_w in X satisfies

   B_X(z_w,c0 rho^(|w|+l_s(w))) subset C_(w e_s(w)) subset C_w,

   and that ball is disjoint from Y.

The word in (5) is the actual chosen shortest escape word from (4). It is not enough to verify a ball for some unrelated rejected descendant. If geometry supplies different, possibly longer escape words, the same theorem holds with N their verified maximum length, but N<=|S| is then not asserted.

### Conclusion and proof

For every y in Y and every 0<r<=min{A,D}, there is an ambient ball in B_X(y,r)\Y of radius c r, where one may take

  c = min{1/4, c0 rho^(N+1)/(4A)} > 0.

Choose the least k>=0 such that A rho^k<=r/2. Because r<=A, k>=1. Minimality gives A rho^(k−1)>r/2, hence rho^k>rho r/(2A). Use the selected chain from (3) and its prefix w of length k. Its state s(w) is in R, so (4) supplies e_s(w), and (5) applies to this very cell and this very escape word.

The certified ball has radius

  R_w=c0 rho^(k+l_s(w)) >= c0 rho^(k+N)
      > [c0 rho^(N+1)/(2A)] r >= 2c r.

It is contained in C_w, which contains y and has diameter at most r/2. Thus the certified ball lies inside B_X(y,r), and is disjoint from Y. The smaller concentric ball B_X(z_w,c r) proves the claimed porosity. All scale choices are uniform in y. The large-scale adjustment in the Turn 1 clarification below gives uniform porosity for radii up to D as well.

### Why the graph bound is finite and nonvacuous

For each s in R, a shortest path to bottom cannot repeat a safe state: deletion of the intervening cycle would give a shorter path to the same target. Every safe state on this path is still reachable from s0, so at most |R| safe states occur before the terminal bottom. Therefore l_s<=|R|. Since s is safe, l_s>=1. Reverse breadth-first search computes these integers exactly.

At length N there is at least one rejected word from every reachable safe state, obtained by padding its shortest escape after bottom. Hence at most b^N−1 words survive from each such state, and the original block-count bound follows. This finite computation supplies a uniform symbolic escape length; it does not verify the infinite family of geometric ball inclusions.

The theorem is a conditional reduction, not a claim that an arbitrary self-image meets its hypotheses. Geometry must independently establish (2), (3), and (5), with uniform constants. The automaton only establishes (4) and the counting bound. In particular a rejected address may represent the same point as a safe address under a many-to-one coding, so rejection alone proves no missing metric ball. Conversely, the original vacuous-state counterexample Y=X is now excluded: (3) demands a reachable safe chain through every point, and (4) plus (5) would then give a nonempty ball disjoint from X, which is impossible. The proof does not infer safety from porosity or assume its conclusion.

For an attained-conformal-dimension boundary self-image, the corrected criterion and the separately credited porous-subset theorem exclude any construction satisfying all these hypotheses. They do not verify the hypotheses for a general quasisymmetric image. The original conjecture remains open in this packet.

## Recommended clarification of Turn 1 quantifiers

In the auxiliary hole-propagation criterion, fix a single r0 with 0<r0<=D, and require its stated homeomorphism and actual-hole hypotheses for every y in Y and every 0<r<=r0, with one fixed c>0. The cutoff cannot depend on y. The unused point z in the old wording is unnecessary.

For r<=r0 the original argument gives a hole of radius c r. For r0<r<=D use the hypothesis at radius r0/2; the resulting hole lies in B(y,r0/2) subset B(y,r), with radius c r0/2 >= [c r0/(2D)]r. Shrink the ball if necessary. Thus c'=min{c,c r0/(2D)} is a uniform all-scale porosity constant. Compactness provides the finite diameter D, not a missing uniform quantifier.

## Recommended clarification of Turn 3 hypotheses

In the quantitative orbit and measure arguments explicitly take U=B_X(a,s) with 0<s<=D and U subset X\f(X). A proper compact image supplies such an a,s. The general disjoint-layer observation still holds for every U subset X\f(X), but the estimate d(a,b)>=s uses this ball choice.

For every n use h_n=max{1,eta_n(D/s)}. Then

  d(f^n(a),f^m(a)) >= d_n/(2h_n),  m>n,
  d_n/h_n -> 0,

where d_n=diam f^n(X). Every associated packing denominator uses h_n. This restates the already mandatory ADDITIVE_T3_NORMALIZATION.md consistently, including degenerate triples. The measure-series statement assumes lambda_n>0 so the inverse is lambda_n^(-1)-Lipschitz. Its sum inequality, uniform-iterate point-attractor alternative and stated limitations remain unchanged.
