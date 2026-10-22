# Independent audit: finite fixed-diagonal projection paving

Date: 21 October 2026. Target: problem 20000566.

## Verdict

ACCEPT the exact complex and real 4-by-4 half-diagonal two-paving profile as an elementary consequence/synthesis of established structure. ACCEPT the finite complementary-frame matroid criterion below as a direct application of Edmonds's classical partition theorem. REQUIRE the scope and attribution corrections below. The subsequently developed theorem in Section 5 is also ACCEPTED: it answers the explicit finite universal epsilon_d formulation recovered from primary context, but not a uniform-gap-over-dimensions question. Novelty is unestablished. No GitHub or queue write was made in this audit.

The independently checked mathematical claims are stated and proved here; this is not an acceptance of every bibliographic or current-status claim in the recovered generated attempt.

## Conventions

P is a finite orthogonal projection over R or C, not an arbitrary idempotent. For 1<=r<=n, pi_r(P) is the minimum, over partitions of all n coordinates into r nonempty blocks S_j, of max_j ||P[S_j]||. This is direct compression of P. Strict means pi_r(P)<1. A uniform quantitative assertion over a class means one epsilon<1 bounds pi_r for every member of the entire class.

Allowing empty blocks gives the same minimum when n>=r: split non-singleton occupied blocks until there are r nonempty blocks, and use monotonicity of compression norms. The recovered claim that nonemptiness materially changes this optimum is incorrect.

## 1. Exact profile on the half-diagonal 4-by-4 fiber

Suppose diag(P)=(1/2,1/2,1/2,1/2). Trace gives rank(P)=2. Write x_ij=|p_ij|^2. The diagonal equations P^2=P give the four incident-edge sums x_ij+x_ik+x_il=1/4. Adding two of these equations and subtracting the other two yields

x_12=x_34, x_13=x_24, x_14=x_23.

Thus complementary off-diagonal magnitudes agree; no unproved assertion about complementary minors is needed.

Every 1+3 coordinate partition has norm 1: the three-dimensional coordinate subspace intersects the two-dimensional range of P nontrivially. A nonzero vector in that intersection is a compression eigenvector of eigenvalue 1. Positivity and contractivity give equality of the norm to 1.

For a 2+2 partition, each principal pair has eigenvalues 1/2 plus or minus its off-diagonal magnitude. The two blocks have the same magnitude by the preceding identities. There are exactly three such unordered partitions, and consequently

pi_2(P)=1/2+min(|p_12|,|p_13|,|p_14|).

The three squared magnitudes sum to 1/4. Their minimum is at most 1/(2 sqrt(3)), so in particular it is strictly less than 1/2. Hence an optimal partition really is balanced; this is a conclusion after checking all seven partitions, not an assumption restricting the optimization.

### Sharpness and full interval

For real x,y,z define the Hermitian matrix

A(x,y,z) = [[0,x,y,z], [x,0,-i*z,i*y], [y,i*z,0,-i*x], [z,-i*y,i*x,0]].

Direct multiplication gives A^2=(x^2+y^2+z^2)I. Therefore P=I/2+A is a projection whenever x^2+y^2+z^2=1/4. For

0<=s<=1/(2 sqrt(3)), x=s, y=z=sqrt((1/4-s^2)/2),

we have y=z>=s and pi_2(P)=1/2+s. This proves the full complex image

[1/2, 1/2+1/(2 sqrt(3))].

The minimum is achieved and the maximum is achieved. Thus the existential fiber minimum is 1/2 and the universal fiber maximum is 1/2+1/(2 sqrt(3)). In particular epsilon=3/4 separates two complex matrices with identical diagonals, but does not separate strict two-pavability: every member is strictly two-pavable.

### Real fiber

For real symmetric A=P-I/2, let its upper-triangular entries be a,b,c,d,e,f in row order. Three off-diagonal equations in A^2=I/4 are bd+ce=0, ad+cf=0, ae+bf=0. If all six entries were nonzero, dividing the first two gives b/a=e/f, while the third gives e/f=-b/a, a contradiction. At least one entry is zero. Complementary magnitude equality then makes one of p_12,p_13,p_14 zero. Therefore pi_2(P)=1/2 for every real member. The same division argument does not apply to complex Hermitian entries, whose conjugates alter the equations.

### Normalization audit

A=P-I/2 has norm 1/2, and B=2P-I=2A is a norm-one zero-diagonal Hermitian symmetry. On this fiber the absolute centered two-paving optimum is min(|p_12|,|p_13|,|p_14|). For balanced partitions this follows from the pair eigenvalues. For unbalanced partitions the centered triple block has norm 1/2: the direct triple compression has eigenvalue 1, so its centered compression has eigenvalue 1/2, and compression contractivity bounds its norm by 1/2. Thus

pi_2(P)=1/2+alpha_2(A)=1/2+(1/2)alpha_2(B).

The normalized centered parameter beta_2(A)=alpha_2(A)/||A|| ranges from 0 to 1/sqrt(3), not from 1/2 to 1/2+1/(2 sqrt(3)). The exact affine relation here must not be asserted for arbitrary diagonal projections without a separate proof.

## 2. Finite strict paving and the complementary frame

Let Q=I-P and f_i=Qe_i. For any S, the Gram matrix of (f_i)_{i in S} is Q[S], because Q^2=Q. Also P[S]=I_S-Q[S]. All its eigenvalues lie in [0,1]. Hence

||P[S]||<1 iff Q[S] is positive definite iff (f_i)_{i in S} are linearly independent.

Edmonds's finite matroid partition theorem states that a finite ground set can be partitioned into at most r independent sets exactly when every subset S has cardinality at most r times its matroid rank. Applying that theorem to the column vectors f_i, and refining independent sets when necessary, proves

pi_r(P)<1 iff |S|<=r rank(Q[S]) for every S subset of [n].

This is a matrix/frame criterion, not a criterion depending on the diagonal alone: rank(Q[S]) contains off-diagonal information.

If d_i=p_ii<=1-1/r for every i, then Q[S] is a positive contraction and

rank(Q[S]) >= trace(Q[S]) = sum_{i in S}(1-d_i) >= |S|/r.

Thus every such finite projection is strictly r-pavable. Conversely, applying the necessary condition to S=[n] yields n<=r(n-rank(P)). For constant diagonal alpha, rank(P)=n alpha, so the finite constant-diagonal answer is precisely

strict r-paving iff alpha<=1-1/r,

for admissible finite projections and n>=r. Equality is included.

This is also the sharp maximum-diagonal threshold for a universal *finite pointwise strict* guarantee across all dimensions: above 1-1/r choose a rational constant alpha below the proposed larger cutoff, realize it by a finite constant-diagonal projection (for example the appropriate Fourier projection over C), and the total-rank obstruction applies. It is not a necessary condition on an individual arbitrary diagonal. For example a rank-one projection with diagonal (0.9,0.1) has pi_2=0.9<1 despite max diagonal>1/2.

All these finite strict statements are classical theorem consequences, not claimed novel. They do not supply a common epsilon<1 independent of dimension. Positive definiteness may hold with arbitrarily small least eigenvalue. In infinite dimension algebraic independence likewise does not imply a Gram operator bounded below. The finite proof must not be carried over as an infinite-dimensional norm bound.

For a fixed finite diagonal d, the projection fiber is compact and pi_r is continuous (indeed 1-Lipschitz in operator norm). Therefore if every member of that one fiber is strictly r-pavable, its fiber maximum is strictly below 1. That gap may depend on d and n; it is not the dimension-independent gap demanded by a uniform paving question.

## 3. Prior art and corrections required

- Giol, Kovalev, Larson, Nguyen and Tener, *Projections and idempotents with fixed diagonal and the homotopy problem for unit tight frames*, arXiv:0906.0139v2, Section 3.2, printed pp.6-7, already give the explicit complex 4-by-4 parametrization, complementary-pair magnitudes, zero-entry strata and real all-nonzero obstruction. The profile is an elementary optimization over that established structure. The exact range statement was not verified verbatim there; no bibliographic priority is asserted. https://arxiv.org/pdf/0906.0139
- Weiss and Zarikian, *Paving small matrices and the Kadison-Singer extension problem*, Operators and Matrices 4 (2010), 301-352, Definition 1.2.3 and Proposition 6.2.2 (p.333), prove beta_2=1/sqrt(3) for all zero-diagonal Hermitian complex 4-by-4 matrices. Applying this to A=P-I/2 gives the direct upper endpoint by the triangle inequality. This is an established prior bound, not a newly obtained universal constant. https://files.ele-math.com/articles/oam-04-17.pdf
- Jack Edmonds, *Minimum Partition of a Matroid Into Independent Subsets*, Journal of Research NBS 69B (1965), 67-72, Theorem 1, Section 1.3, p.69, supplies exactly the finite partition criterion used above. The theorem and its finite scope were verified in the primary publication. https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn1-2p67_A1b.pdf
- The generated sentence presenting max diagonal<1/4 as the best general finite strict-two-paving condition must be changed to a verified sufficient condition for a dimension-independent quantitative gap from the cited analytic estimate. It is false if read as the best condition for individual finite strictness, as the <=1/2 matroid consequence shows.
- Do not identify existential and universal fiber extrema, or claim the diagonal completely determines a quantitative paving constant. Do not claim this 4-by-4 specialization solves the broadly worded AIM problem. Do not claim an unambiguously formulated current open conjecture merely because a bounded literature search found no exact general classification.

## 4. Exact computational checks

The adjacent exact_checks.py uses symbolic algebra, not floating-point tolerance. It verifies A^2=(x^2+y^2+z^2)I, all four triple characteristic polynomials, the linear equations forcing complementary squared magnitudes, and projectionhood of the full interpolating path. It records all six pair characteristic polynomials; theorem_checks.py supplies the explicit guards verifying those six pair identities. outputs/exact_checks.py.stdout records PASS with SymPy 1.14.0. The script supports the written proof; it is not a substitute for the general mathematical arguments.

The triple checks are for the displayed parametrized family; the universal triple norm conclusion is independently proved above by subspace intersection and contractivity. No numerical sampling is used to establish universality or attainability.

## 5. Additional exact universal-diagonal theorem (independently audited)

The following stronger theorem was submitted during the mathematical audit. It is mathematically valid; the proof below includes fractional, integer, boundary and scalar-field cases.

Let d in [0,1]^n be realizable, q_i=1-d_i and m=sum q_i an integer. Fix S and put a=sum_{i in S}q_i. Among all orthogonal projections Q with diagonal q,

min rank(Q[S]) = ceil(a).

The lower bound follows because Q[S] is a positive contraction of trace a. To attain it, write a=f+theta with f=floor(a).

If theta=0, construct separate projections on S and its complement with diagonals q restricted to those sets. Their integer sums are f and m-f, respectively; finite Schur-Horn gives these projections over both R and C. Their direct sum attains rank f on S. This covers a=0, S empty, S all coordinates, and complementary trace zero.

If 0<theta<1, the spectra to use on S and its complement are respectively

(1 repeated f times, theta, 0...),
(1 repeated m-f-1 times, 1-theta, 0...).

Both fit: f+1<=|S| since a<=|S|; m-f<=|S complement| since m-a<=|S complement|; and m-f-1>=0 since m-a>0. Construct a projection whose only cross-block coupling is the real rank-one matrix [[theta,sqrt(theta(1-theta))],[sqrt(theta(1-theta)),1-theta]] between the two fractional eigencoordinates; elsewhere use the indicated ones and zeros. Its total rank is m. Every vector of entries in [0,1] with sum f+theta is majorized by (1^f,theta,0...), since a partial sum is at most its number of terms and at most the total sum. The same holds on the complement. The real symmetric Schur-Horn theorem therefore supplies independent real orthogonal changes of basis in the two blocks producing the prescribed diagonals. Block orthogonal conjugation preserves global projectionhood and the compression ranks. This attains ceil(a)=f+1. The construction is real, so also works in the complex class.

Combining the minimum-rank result with the matroid criterion proves that EVERY P with diagonal d is strictly r-pavable if and only if

|S| <= r ceil(sum_{i in S}(1-d_i)) for every S.

There is no quantifier interchange error: sufficiency bounds the rank for every P and every S; if one S violates the inequality, its attaining projection is a single counterexample to the universal statement. A separate projection may be used for each proposed obstruction.

Order d decreasingly, so q is increasingly ordered. It suffices to test smallest-q prefixes because they minimize the trace for any given cardinality. Equivalently, for every integer j>=0 with rj+1<=n,

sum_{i=1}^{rj+1} d_i < (r-1)j+1.

Indeed the corresponding q-prefix condition is sum_{i<=rj+1}q_i>j. These imply all intervening cardinality conditions by nonnegativity of q: if rj+1<=k<=r(j+1), the prefix trace at k is greater than j and therefore has ceiling at least j+1>=k/r. Conversely the all-cardinality condition implies each displayed prefix inequality. If one fails, its trace a<=j and rank can be made at most j, whereas the subset has rj+1 entries.

The fixed-diagonal fiber is compact in both fields and pi_r is continuous. Therefore the universal pointwise strict condition is equivalent to existence of epsilon_d>0 such that EVERY P in that fiber has pi_r(P)<=1-epsilon_d. This is a finite fiber-uniform constant, not an effective value or a dimension-independent uniform gap across changing diagonals.

### Precise source match and scope revision

Casazza-Edidin, *Equivalents of the Kadison-Singer Problem*, Section 9, Problem 9.4 asks for this exact finite universal fixed-diagonal condition. Proposition 9.6 gives the displayed inequalities as sufficient, Problem 9.7 asks necessity, and Proposition 9.8 handles an equality obstruction. The fractional coupling above also supplies counterexamples when a prefix inequality is violated strictly, so it establishes the missing implication of that precise formulation. https://www.aimath.org/WWN/kadisonsinger/123.KS.pdf

The 2014 AIM participant contribution A.4 confirms the finite universal epsilon_d formulation; its subsequent moment-map sentence uses an existential intersection description inconsistent with that universal wording. The 2006 A.3 contribution unambiguously formulates fiber containment and records the then-unproved converse. These sources support treating the theorem as a complete answer to the explicit universal finite-fiber problem associated with Edidin's request, rather than merely a four-dimensional specialization. Neither the actual best epsilon_d, the geometry of worst-paved loci, nor any uniform bound across dimensions has been determined here. Source links: https://aimath.org/WWN/beyondks/beyondks.pdf and https://aimath.org/WWN/kadisonsinger/kadisonsinger.pdf . These workshop compilations bear a distribution restriction; no source text or PDF is reproduced in this authored audit.

This updates the narrower initial source gate: the four-dimensional generated profile alone remains insufficient, but the subsequently developed general theorem addresses the explicit finite universal target. Bibliographic novelty remains unestablished. The published or archived date of a question does not prove it is still open.

### Concrete real strict-versus-nonstrict separation

Let I=I_3 and J be the all-ones 3-by-3 matrix. Define

Q_bad = diag(J/3, I-J/3),
Q_good = [[I/3, sqrt(2)I/3],[sqrt(2)I/3, 2I/3]],
P_bad=I_6-Q_bad and P_good=I_6-Q_good.

Both Q matrices are real rank-three orthogonal projections with diagonal ((1/3)^3,(2/3)^3). Thus both P matrices have diagonal ((2/3)^3,(1/3)^3). The first three Q_bad columns span dimension one, so no two-partition can make both restricted families independent; pi_2(P_bad)=1. The first-three/last-three partition of P_good has compression norms 2/3 and 1/3, while max diagonal is 2/3; hence pi_2(P_good)=2/3. This explicitly closes the generated attempt's proposed strict-pavability-separation next step. No priority claim is made for this elementary witness.

strict_checks.py verifies both projections, their common diagonals and ranks, all 31 unordered nonempty two-partitions exactly, and the fractional coupling identity. outputs/strict_checks.py.stdout records PASS.

## 6. Bounded priority-search record

On 21 October 2026 an independent targeted web search used combinations of Casazza/Edidin, Problem 9.7, inequalities (9.2), fixed diagonal, paving, Schur-Horn, rank, necessary and sufficient. It recovered the primary old question and related projection/frame literature, but no verified later theorem proving the displayed converse. This is a bounded negative search only, not an assertion of novelty or present open status. Source identification, theorem correctness, and priority are separate conclusions.

## 7. Final manuscript review and acceptance

Independently read all five approaches in the accepted proof manuscript and its scope decision. The Bloch-frame calculation has the correct scaling |p_ij|^2=(1+n_i dot n_j)/8. The rank-one bin formula and lower bounds are sound. The CFMT reconstruction has D1^2+D2^2=2I, unit row norms, and a valid dimension-kernel vector proving pi_2>=m/(m+1); it does not falsely assert failure of strictness for a finite example. The cited Leake-Ravichandran formula is presented only as a sufficient bound and not as current optimal status. Independently verified the real-orthogonal Schur-Horn form in Carlen-Lieb arXiv:0904.0734v3, introduction and proof after Chan-Li: https://arxiv.org/pdf/0904.0734 .

Final mathematical decision: claimed_solved=true for the precise source-supported finite universal formulation: given admissible finite d and fixed r<=n, characterize whether EVERY orthogonal projection with diagonal d admits an r-paving with a common bound 1-epsilon_d<1. The prefix inequalities are necessary and sufficient, over R and C. This decision does NOT claim novelty and does NOT assert a solved prescribed-epsilon classification, optimal epsilon_d formula, uniform gap across dimensions, existential-only classification, infinite-dimensional norm theorem, or geometric classification of all worst-paved loci.

Both author check programs were independently rerun successfully. The quarter-grid comparison tests 28,092 admissible (q,r) cases of subset versus prefix conditions. Its finite scope is explicit and it is not the proof of the universal theorem. A requested audit patch removes floating-point ordering from the three exact symbolic sample extrema. The accepted input manuscript and audit hashes, and publication derivative changes, are recorded in DERIVATION.json.
