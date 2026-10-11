# Independent written audit: primitive-set saturation game (EP872 / 2355)

This is an AI-assisted, unrefereed authored mathematical audit edition. Acceptance means an independent internal AI audit of the precisely scoped written arguments and explicitly retained classical dependencies. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete seven-section mathematical reconstruction and exact rational certificate proof are retained, including all corrections, analytic formulas, rational endpoints, necessary finite examples, assumptions and limitations. Executable code, raw calculation outputs or coefficient arrays, datasets, copied source documents or text, source images and private coordination material are not distributed. Hashes authenticate bytes; they do not prove mathematical correctness.

Retrieval, inspection and numerical-execution statements describe the original audit of October 11, 2026 UTC and its authenticated earlier source inspection. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. References to code, receipts and their execution describe historical private verification; those artifacts are not distributed in this edition.

## Result and scope

For the game on {2,...,n} with Prolonger moving first, this audit accepts the following previously claimed asymptotic bounds, after the explicit proof clarifications below:

- Silva and GPT 5.5 Pro: liminf L(n)/(n log log n/log n) >= 1/2.
- Buddhdev: limsup L(n)/n <= W4/2, where the density and four integrals defining W4 are given below.
- A new, independently authored exact-arithmetic audit certificate proves W4/2 < 0.189741239716434 < 0.19. Thus L(n) < 0.19n for all sufficiently large n. This verifies the strict threshold without relying on the author's numerical program or its FFT error model.
- Buddhdev's earlier 1/8 lower constant is also supported by its complete written proof. It is superseded, for the same Prolonger-first convention, by the 1/2 result.

The stronger lower scale n(log log n)^2/log n remains conditional on the restricted safe-edge hypothesis. Neither these inequalities nor this audit settles whether L(n) is linear or sublinear. In particular an upper bound by a fixed positive fraction of n is not an o(n) upper bound, and the accepted lower bound is itself o(n).

The tighter manuscript decimal W4/2 <= 0.1897123371 and the four narrow numerical intervals stated in its Proposition B.1 were not independently certified here. They are consistent with the wider independent intervals, but overlap is not verification of the narrower intervals.

These are mathematical audit conclusions from written arguments and an independently derived certificate, not claims of journal acceptance, author-artifact replay, end-to-end Lean verification, novelty, or an exhaustive current literature search. No public repository, branch, pull request, or QUEUE file was changed.

## Source identity and inspection

Historical byte-authentication checked all 43 listed source-collection members against their recorded sizes and hashes before the audit. This establishes byte identity, not theorem correctness. The relevant public sources and their inspected PDF identities follow; the PDFs remain outside this publication edition.

1. P. Erdos, *Some of my forgotten problems in number theory*, Hardy-Ramanujan Journal 15 (1992), 34-50. Publisher: https://hrj.episciences.org/125 ; PDF: https://hrj.episciences.org/125/pdf . 4,630,109 bytes, SHA-256 51faf4558eacab8e188efbcb028937f75dcb10d37865ab71ef1522df33361c72. The applicable original game statement is printed page 47, PDF page 14; that passage was read, with an authenticated earlier visual inspection of that passage recorded in SOURCES.json.
2. Om Buddhdev, *Improved Bounds for the Primitive-Set Saturation Game (Erdos Problem 872)*, manuscript dated April 21, 2026. https://sensho.xyz/papers/erdos-872.pdf and https://www.sensho.xyz/papers/erdos-872.pdf . 389,707 bytes, SHA-256 3f00eef40e1d775a818c893bc4257075ea059b85e991a2d88628d9302fdd59ed; 51 pages. PDF metadata records creation April 23, which does not replace the manuscript's stated date. Complete extracted text, including all proof-bearing sections and appendices, was read. The applicable lower, upper, conditional, numerical and formalization proofs were reconstructed; unrelated auxiliary results were read but are not comprehensively accepted by this report.
3. Jonas Silva and GPT 5.5 Pro, *A Dyadic Semiprime Lower Bound for the Primitive-Set Saturation Game*. https://github.com/jonaslsaa/maths/blob/main/872.pdf ; raw source https://raw.githubusercontent.com/jonaslsaa/maths/main/872.pdf . 87,433 bytes, SHA-256 0d837350fe0253e92a23ad6589e7c3414ded758e19a422a7ab43a0fc500d4385; five pages. All five pages and the complete argument were read. PDF metadata gives April 29, 2026; the bibliography also records an April 29 access date. Neither is an independently verified publication/acceptance date.

Fresh web access found the www.sensho.xyz PDF and the GitHub listing; the non-www endpoint and raw GitHub PDF did not open through the web reader in this pass. The hash-pinned complete local PDFs remained available. No byte identity between the fresh web-reader rendering and the pinned local PDF is assumed. No source-code, Lean artifact, or numerical certificate from the authors was executed or transplanted. The public artifact repository was not needed for acceptance.

Visual spot checks in this pass: Buddhdev pages 29 and 46; Silva pages 2 and 4. Additional pages were rendered but not all renders were visually inspected. Complete-text reading does not mean all 56 PDF pages were visually inspected. A PDF-text extraction ordering problem in the reciprocal inequality on Buddhdev page 29 was resolved against the rendered page; the PDF has the correct inequality.

## 1. Exact game and starting-player boundary

A move chooses a distinct, previously unchosen integer in {2,...,n}. The combined set of both players' choices is an antichain for divisibility. A move is legal exactly when it is incomparable with every previously chosen integer. Play ends at a maximal primitive set, not necessarily a maximum primitive set. Total moves equal the terminal set's cardinality. Prolonger maximizes this total and Shortener minimizes it.

Erdos's original passage does not identify the starting player. Both modern manuscripts define L(n) with Prolonger first. Denote this value L_P(n), and the other convention L_S(n). The accepted lower bound in this report is for L_P. We do not assert L_P=L_S or transfer a first-move strategy without checking it. The upper-bound proof below actually has no difficulty with Shortener first: before her jth move there are at most j Prolonger moves, and all its estimates use this upper bound. Thus the same upper strategy and asymptotic upper bound extend to L_S by the explicit count observation. This does not establish equality of values or a 1/2 lower constant for L_S.

A useful turn-independent baseline: every terminal antichain contains a multiple of each prime p>sqrt(n), by maximality. Distinct such primes cannot divide the same board integer, so every terminal set has at least pi(n)-pi(sqrt(n)) ~ n/log n members. This also guarantees that o(n/log n)-length activation phases below cannot exhaust the game.

All asymptotic statements concern sufficiently large n. No explicit finite threshold is furnished by the PNT-based proofs or by this audit. The integral certificate's finite exactness does not create an effective game threshold.

## 2. Reconstruction of Buddhdev's 1/8 lower bound

Fix 0<delta<1/2 and Y=n^delta. Let A consist of the odd primes at most Y. For a in A put J_a=(n/(2a),n/a] intersected with the primes. All targets ab with b in J_a lie in (n/2,n], and b>Y for large n.

### Activation

At every Prolonger activation turn, take the smallest currently legal prime a in A and play a legal target ab. This is possible: there are uniformly at least c_delta n^(1-delta)/log n candidate b, while only O(pi(Y)) prior moves have occurred. Because a is legal and ab lies in the upper half, a previous chosen integer can obstruct ab only by being b or ab. Each prior move excludes at most one candidate, and delta<1/2 makes the candidate count larger.

Stop once no prime in A is legal. Include Shortener's next reply if the last activation turn was Prolonger's. Divide A into A0, whose singleton was made unavailable by a chosen proper multiple, and D, whose singleton Shortener chose. Prolonger never chooses such a singleton. Pair each singleton chosen by Shortener with the immediately preceding activation prime. Those pairs are distinct, and the activated prime is no larger than the lost singleton, because it was the smallest legal one. Therefore sum_{D}1/a <= sum_{A0}1/a. Mertens gives sum_{A0}1/a >= (1/2-o(1))log log n.

### Fan size and activation damage

Make an edge (a,b) for each a in A0 and b in J_a. The fixed-ratio PNT, uniformly for a<=Y, gives |J_a| >= (1/2-o(1))n/(a log n). Thus the raw graph has at least (1/4-o(1))n log log n/log n edges.

The singleton a was not chosen. An earlier move can obstruct an upper-half squarefree target ab only by being b or ab. Delete a whole b-star for an already chosen b and a single edge for an already chosen target. There are O(pi(Y)) previous moves; a star has at most pi(Y) edges. Total damage is O(pi(Y)^2)=o(n log log n/log n), since 2delta<1. The surviving graph has the same leading edge lower bound.

### Capture and charging to actual moves

Prolonger chooses a right vertex of maximum current degree and plays one incident upper-half target a0b. It is legal: a0 is unavailable but unchosen, b has not been chosen, and the exact target is still available; those exhaust relevant divisors, and it has no proper board multiple.

After this move, b itself can never be chosen. For every other edge (a,b) in that star, a was already unavailable and unchosen. Therefore the target ab can no longer be obstructed by a divisor, and terminal maximality forces its eventual selection. Distinct target edges give distinct actual moves.

Delete the captured star from the live graph. A subsequent Shortener move can delete at most one current right star, one exact edge, or nothing. If d_i is Prolonger's captured degree, the immediately following deleted star has degree <=d_i. Let C=sum d_i and X count individual exact-edge deletions by Shortener. Partitioning the original edges gives |E0|<=2C+X<=2(C+X). Captured edges and individually selected exact targets are disjoint actual moves. Hence L_P(n)>=|E0|/2>=(1/8-o(1))n log log n/log n.

No unproved finite capture hypothesis or numerical input occurs in this argument. Its analytic inputs are the standard PNT and prime reciprocal Mertens estimate. The published paper describes it as prose-only, without a formal artifact.

## 3. Reconstruction of the 1/2 dyadic improvement

Fix an integer H>=0 before sending n to infinity. Set Y=n^(1/3), M=2^(-H)n^(1/2), and let C_m be the set of board integers with odd part m. Prolonger opens with 2^B, the largest power of two at most n. For large n, B>H, so all board moves 2^b with 1<=b<=H are unavailable and unchosen; 1 is never a board move.

### 3.1 Activation invariant and legal blocks

Initially the odd primes p<=Y are live. A prime is H-secured if p,2p,...,2^H p are all unavailable and none was chosen. Remove a prime when it becomes secured or is declared lost. After each Shortener move:

- If it is 2^b p for a live p and 0<=b<=H, declare p lost.
- Otherwise, if it contains at least two current live primes, declare one of them lost.
- Otherwise declare no loss.

Thus there is at most one bookkeeping loss per Shortener turn. On each activation turn take the longest initial segment of the currently live primes whose product d is at most M; if all fit, take all. Since every live prime is <=Y<M for large n, the block is nonempty. Choose a fresh prime r in (n/(2^(H+1)d), n/(2^H d)] which divides no previously chosen number, and play u=2^H dr.

Uniformly over these blocks, the interval has lower endpoint at least sqrt(n)/2 and fixed endpoint ratio 2. The PNT supplies at least c_H sqrt(n)/log n primes. There are O(pi(Y)) prior moves, each with at most log n/log 2 distinct prime factors, so only O(Y) primes are forbidden. Since sqrt(n)/log n >> Y=n^(1/3), a fresh r exists. It is greater than Y, different from the block primes, and u lies in (n/2,n].

For rigor, separate earlier Prolonger and Shortener moves in the legality proof. Earlier Prolonger activations also lie in the upper half; they cannot be proper divisors or multiples of u. Equality is excluded because r divides no earlier chosen integer. The opening 2^B does not divide u, whose 2-adic exponent is H<B. If an earlier Shortener choice a divided u, freshness of r would force a=2^b times a squarefree product of current block primes, with b<=H. No odd factor outside the current live set is then present, so the set of live factors at the earlier choice equals its current set. If there are no odd factors, a is a forbidden power of two (or 1). If there is exactly one, rule 1 removed it; if at least two, rule 2 removed one. All cases are impossible. No proper multiple of u is on the board. Thus u is legal, and every prime in d becomes H-secured.

This explicit separation repairs a small omission in the published Lemma 1: its bookkeeping argument is worded for an arbitrary earlier chosen integer, although the bookkeeping rules apply only after Shortener's turns. No change to the strategy or theorem is necessary.

### 3.2 Lost reciprocal mass is bounded

Let D(X) count lost primes at most X<=Y. There can be one unpaired loss immediately after the opening. Every subsequent lost p<=X is paired with the preceding activation block. Because p remained live after that block, the first omitted live prime is <=X; by maximality, d>M/X. Every prime in that initial block is also <=X. Distinct blocks use disjoint primes.

Consequently (D(X)-1)(log n/6-H log 2) <= theta(X). Chebyshev's elementary bound theta(X)<=C X yields D(X)<=1+C_H X/log n for all sufficiently large n. This estimate is uniform for 2<=X<=Y. Partial summation gives

sum_{p in D}1/p = D(Y)/Y + integral_2^Y D(t)/t^2 dt = O_H(1).

The integral of 1/t^2 is bounded, and that of 1/(t log n) is log(Y)/log n=1/3. Every initial live prime eventually is secured or lost. Thus the secured set P* has sum_{P*}1/p=log log n+O_H(1), losing only bounded reciprocal mass, compared with the factor 1/2 loss in the earlier strategy. The O(pi(Y)) activation moves cannot end the game by the baseline above. Include the final Shortener reply before starting the next phase.

### 3.3 Dyadic targets and surviving edge count

For p in P*, use every prime q in (n/(2^(H+1)p),n/p]. Such q is >=c_H n^(2/3)>Y. Every odd product pq has a unique lift T(p,q)=2^a pq in (n/2,n] with 0<=a<=H. Represent its entire chain C_pq by the edge (p,q).

The PNT gives uniformly

|J_p| >= (1-2^(-H-1)-o_H(1)) n/(p log n).

Indeed, apply the fixed-ratio estimate at x=n/p>=n^(2/3); then 1/log x>=1/log n. Summing over P* gives at least (1-2^(-H-1)-o_H(1))n log log n/log n raw edges.

Remove every right prime q dividing any previous selected integer. Each such integer contains at most one candidate q because two primes >=c_H n^(2/3) have product >n eventually. Each removed star has at most pi(Y) edges. With O(pi(Y)) prior moves, damage is O_H(pi(Y)^2)=O_H(n^(2/3)/log^2 n)=o(n log log n/log n). Denote the surviving graph G0.

### 3.4 Star capture forces distinct chains

Choose a current right prime q of maximum degree, and its smallest neighbor p0; play T(p0,q). No earlier selected integer is divisible by q. A proper divisor of this upper-half target is a power of two, 2^b p0, 2^b q, or 2^b p0q. Powers of two and small-prime lifts are unavailable and unchosen; any divisor containing q was not previously chosen. Hence the move is legal.

For another current neighbor p>=p0, the lift exponent satisfies a(p,q)<=a(p0,q). The capture move therefore makes all 2^b q with b<=a(p,q) unavailable and unchosen. Likewise all 2^b p needed for that target were already secured, and the relevant powers of two are blocked. If no element of C_pq were selected by the end, then the upper-half target T(p,q) would have no selected proper divisor and no proper board multiple. It would still be legal, contradicting terminal maximality. Thus every captured edge forces a move in its own 2-adic chain.

Edges encode different chains: p<=Y<q, so uniqueness of prime factorization gives unique ordered (small,large) factor pairs. Distinct odd parts have disjoint chains, and primitiveness permits at most one member of each chain. This proves actual move distinctness even when the selected chain member is a lower lift rather than the upper target.

After capture remove its q-star. After Shortener's reply remove the star of the unique current candidate q dividing that chosen number, if any. This can pessimistically discard edges not actually killed, which only strengthens the bookkeeping opponent. No move contains two such q. Every surviving right prime still divides no previous selection, maintaining the legality invariant. The reply's deleted degree is at most the preceding maximum d_i. Hence |E(G0)|<=2 sum d_i. The graph cannot be nonempty when the real game ends, because its indicated capture move would then still be legal.

Therefore for every fixed H,

L_P(n) >= [ (1/2)(1-2^(-H-1))-o_H(1) ] n log log n/log n.

To obtain the 1/2 statement, for each epsilon>0 choose a finite H with 2^(-H-2)<epsilon/2 and then n large enough for the fixed-H error <epsilon/2. No uniform PNT or error bound with H growing arbitrarily fast is needed. The theorem means a liminf of at least 1/2; it does not assert the strategy is optimal.

## 4. Reconstruction of the upper bound

Define rho(u)=1/((floor(1/u)+1)u) on 0<u<=1, and

J_r=(1/r!) integral_{u_i>0, sum u_i<=1} product rho(u_i) du_1...du_r,

for r=1,2,3,4. Then W4=1-J1+J2-J3+J4. Values assigned on reciprocal-integer breakpoint sets do not affect these integrals. Everywhere 0<rho<=1.

### 4.1 A long legal-prime prefix and local lower profile

Fix 0<epsilon<1. Shortener plays the smallest legal odd prime for K=floor((1-epsilon)n/(2 log n)) turns. This prefix exists: every previous integer disables at most one prime above sqrt(n), and before turn j there are at most 2j-1 previous moves. The PNT gives pi(n)-pi(sqrt(n))>2K eventually. The chosen primes q1<...<qK are strictly increasing because legality only decreases.

If Y^(h+1)>n, each Prolonger move has at most h prime factors in (Y,X]. At the time Shortener's next prime exceeds X, with S(X) prime selections so far, at most S(X)+1 Prolonger moves occurred. All primes in (Y,X] are now selected or divide an earlier Prolonger choice. Hence pi(X)-pi(Y)<= (h+1)S(X)+O_h(1).

For fixed H, put tau=1/(8H^2), alpha_h=1/(h+1)+tau, beta_h=1/h-tau, 1<=h<=H-1. Use X=n^u and Y=n^(u-tau/2) for u in [alpha_h,beta_h]. All such X are <=n^(1-tau), so their prime sets exhaust before the Kth turn. Uniform fixed-power PNT gives

S_K(n^u) >= (1-xi_H(n)) n^u/((h+1)u log n), with xi_H(n)->0.

### 4.2 Monotone envelope and moment limits

On each genuine interval define A_h(u)=(1-xi_H(n))n^u/((h+1)u log n). This is increasing for sufficiently large n. Its integer floors form the local cumulative envelope. Set the envelope to zero below the first interval, extend it constantly across gaps using the preceding right endpoint, and set its value to K at X=n. Adjacent endpoint levels increase because the next interval begins a factor n^(2tau) farther out. The upper genuine endpoint contributes o(K). The resulting right-continuous integer-valued envelope C(X) is everywhere <=S_K(X).

Define b_j=inf{X:C(X)>=j}. Right continuity and included endpoints ensure C(b_j)>=j, so q_j<=b_j. The b_j consist of genuine inverse points and repeated endpoint fillers. The total reciprocal mass of every filler block is O_H(1/log n), including the top atom b=n with multiplicity <=K.

Let mu=sum b_j^(-1) delta_{log_n b_j}. On a genuine block, Stieltjes summation with floor(A_h) and integration by parts has an error bounded by O_H(n^(-alpha_h)log n), which tends to zero. Its limiting density is rho(u) on G_H=union [alpha_h,beta_h]. Total mass is O_H(1), and the maximum atom weight is <=n^(-alpha_{H-1})->0. Repeated-index tuples therefore have total weight at most binom(r,2) max_j(1/b_j) mu([0,1])^(r-1)=o_H(1).

Tensor measure convergence and the zero measure of the boundary sum u_i=1 then give

T_r^(b)(n):=sum_{j1<...<jr, product b_j<=n} 1/product b_j -> J_r^(H).

The removed portion of (0,1] has length <=5/(4H). Since rho<=1, |J_r-J_r^(H)|<=5r/(4H r!). These are finite-H statements first; a slow diagonal subsequently sends H to infinity.

### 4.3 Why genuine increasing primes are needed, and how rounding works

Sieve monotonicity is established for primes, not arbitrary real cutoffs. Also the top atom contains order n/log n repeated values n and cannot be rounded to distinct primes in [n,(1+o(1))n]. The argument correctly uses a separate top block and a queued initial part of each genuine block.

Fix a>1. For a genuine block [A,B], divide it into source bins [Aa^k,Aa^(k+1)), allowing a truncated final bin. Its inverse demand density is at most (1+o(1))/((h+1)log X)<= (1+o(1))/(2 log X). Prime supply has density (1+o(1))/log X. Release the endpoint atom in bin 0 and source-bin-k demands only at prime bin k+1, guaranteeing p>=b.

Choose eta small with 2a(1-eta)/(1+eta)>1, and choose a fixed integer s so (1-eta)(a^(s+1)-1)>(1+eta)a^s/2. The endpoint atom plus the first s source bins then fit into prime bins 0,...,s. For every suffix, supply exceeds the demands with release at or after that suffix. These nested-neighborhood Hall inequalities ensure a matching. A precise implementation is to allocate demands in reverse release order to the latest available allowed primes, then sort the selected primes against the increasing demands; equivalently oldest-released-first processing meets the final deadline. This explains the compressed greedy wording of Lemma 7.16 without requiring every early bin to clear the whole queue.

All later source bins fit in the immediately following prime bin because their demand is at most half-density. The final truncated bin also fits by the same derivative bound. The largest assigned prime is <a^2 B. Distinct genuine blocks do not overlap because their separation is n^(2tau), and the highest genuine block ends at o(n). Assign the top atom to increasing primes in [n,2n], where PNT supply ~n/log n exceeds its demand <=n/(2 log n).

This yields strictly increasing odd primes p_j>=b_j>=q_j. Exceptions (endpoint atoms, finitely many initial bins and the top block) have reciprocal mass O_H,a(1/log n). Outside these exceptions, b_j<=p_j<=a^2 b_j. Set lambda>=a^2. Each fixed-ratio cell has total b-reciprocal mass O_H(1/log n). Tuples with product in (n/C,Cn] occupy O((log n)^(r-1)) cell patterns, each of mass O((log n)^(-r)), so their total is O(1/log n). Thus cutoff crossings caused by rounding are negligible. Shared tuples change reciprocals by O_H,r(lambda-1). Consequently

T_r^(p)=T_r^(b)+O_H,r(lambda-1)+o_H,lambda(1).

Choose H_m first, then lambda_m close enough to 1, then n thresholds large enough for every fixed-parameter estimate, interblock separation and top supply. Increase thresholds strictly to infinity. The resulting diagonal has T_r^(p)->J_r simultaneously for r<=4. This supplies the full prose input; no short-interval prime theorem, unquantified growing-parameter PNT, or formal artifact is used.

### 4.4 Sieve monotonicity, floor errors, and endgame

The odd-part map x -> x/2^v2(x) is injective on every primitive set. Other than the K selected primes themselves, terminal odd parts avoid all q_j. Thus L(n)<=N(q_1,...,q_K)+K, where N counts odd integers <=n avoiding the listed primes.

If one prime q is replaced by a larger prime p, both outside the remaining prime set R, then N(R union {q})=A_R(n)-A_R(n/q), where A_R counts odd R-free integers. Monotonicity of A_R implies replacement can only increase N. Replacing indices in descending order maintains distinctness. Therefore N(q)<=N(p).

Fourth-order Bonferroni gives

N(p) <= (n/2)[1-T_1^(p)+T_2^(p)-T_3^(p)+T_4^(p)] + O(1+D_1+...+D_4),

where D_r counts r-subsets of distinct p_j whose product is <=n. Unique factorization injects these into squarefree integers with r prime factors. Standard fixed-r almost-prime bounds give D_r=O_r(n(log log n)^(r-1)/log n)=o(n). This controls the number of O(1) intersection-floor errors; one must not substitute the much larger unrestricted K^r tuple count. Since K=o(n) and the four moments converge, limsup L(n)/n<=W4/2.

The independently certified strict gap below 0.19 in the next section absorbs the unspecified o(1) error eventually. The same argument also gives an unconditional contradiction of a near-n/2 asymptotic expectation for this convention, but not a resolution of linear versus sublinear growth.

## 5. Numerical audit and exact replacement certificate

The manuscript's Appendix B outlines N=100000 cell masses, logarithmic antiderivatives, a truncated h-tail, and interval convolutions. It states an FFT l1 rounding allowance of 256 epsilon_machine(ceil(log2 L)+1)^2 ||a||_1||b||_1 and says there is no separately archived stdout. The final arithmetic combining its printed endpoints is correct, but the detailed computation and its FFT error implementation were not reproduced. Merely reading that algorithm or its asserted error allowance is not independent certification of its reported narrow intervals.

The audit instead derived its own certificate from the displayed definition of rho. The full authored certificate reasoning is in PROOF.md. An independent implementation was executed during the original audit; its byte identity and bounded execution scope are recorded in VERIFICATION.json. The code and raw receipts are not distributed here. In brief:

- N=8192, rational cells ((i-1)/N,i/N].
- On the first cell use 1/(N+1)<=integral rho<=1/N, covering infinitely many breakpoints without an infinite computation.
- Split all other cells at exact rational reciprocal-integer breakpoints. Each integral is log(b/a)/(h+1).
- Enclose each logarithm by an 18-term positive rational atanh series plus its explicit positive remainder bound.
- Round masses to lower and upper integer multiples of 10^-15.
- Use exact integer polynomial multiplication with 256-bit coefficient limbs. A proof that each coefficient is smaller than its limb base excludes all carries. No FFT or floating-point operation enters the proof calculation.
- Sum coefficients inside and outside the simplex to enclose each J_r.

The certified intervals, rounded outward here for readability, are:

J1 in [0.788530554733311, 0.788530569640845]
J2 in [0.1868016129073984, 0.1868750780855074]
J3 in [0.0200861139910561, 0.0201056464556379]
J4 in [0.0012218774654126, 0.0012240700717266]

The exact rational endpoint calculation gives

0.1896936371381641 < W4/2 < 0.189741239716434.

The rigorous margin 0.19 minus the exact upper endpoint exceeds 0.000258760283566. The historical private machine-readable receipt contains all exact endpoint numerators and denominators; decimal display strings were not used to prove the inequality. Historical runs under normal Python, -O and -OO agreed byte for byte. Runtime checks used explicit exceptions rather than optimizable assert statements. PROOF.md retains the exact rational upper endpoint and its comparison with 19/100; VERIFICATION.json records the historical execution scope. The receipt and implementation are not distributed here.

This computation is not a game simulation or a finite-n theorem check. It certifies one analytic constant; the strategy and asymptotic limiting arguments still require the written proof above.

## 6. Conditional squared-log lower bound

The conditional construction uses targets acb in (n/2,n], where a<c are odd primes <=Y=n^delta, 0<delta<1/4, and b is prime in (n/(2ac),n/(ac)]. PNT and Mertens give total initial target mass W0 of order at least n(log log n)^2/log n.

An activation graph has vertices the small primes, an edge for each pair (a,c), and weight equal to its still-live b-token count. Choosing a target secures that pair and makes a,c,ac unavailable. The potential assigns coefficients 1/8,1/4,1/2 to unclaimed pairs with zero, one, two captured endpoints, full weight to secured pairs, and adds actual activation score. The desired guarantee that a move exists whose gain dominates every modeled reply is precisely an assumption, not an established general greedy lemma.

Off-model replies are accounted for per token, not per move. There are O(Y^2/log^2 Y) activation rounds. A large-prime singleton can delete O(Y^2/log^2 Y) tokens, a lateral semiprime O(Y/log Y), and an exact target one. Hence total off-model damage is O(Y^4/log^4 Y)=o(n(log log n)^2/log n). Under the activation safe-edge hypothesis, terminal secured mass is at least W0/8 minus this error and the negligible activation score.

For a residual target acb, securing acb0 with b0!=b blocks a,c,ac. Its only remaining harmful proper divisors are b,ab,cb. Distinct upper-half targets are incomparable. Encode these three slots as a rank-three hyperedge. A chosen target captures/scores it; a chosen slot deletes incident live targets. The scaled potential is Q=8S+sum_live 2^(number of captured slots) times edge weight. Under the restricted safe-edge hypothesis for every reached pre-Maker state, complete rounds do not decrease Q. Initially Q=M and terminally Q=8S, so at least M/8 target score follows. This proves the claimed larger scale only under both reached-state hypotheses.

The unrestricted hypothesis is demonstrably false. In the written weighted example, the unique maximum-gain move has gain 135 and admits a reply losing 144. In the arithmetic K4 fiber built from small primes 13,17,19,23, a large prime q in (n/442,n/437] supports all six pair targets. A reachable abstract slot-game state has two live edges with all three slots captured. Either Maker move scores weight one while removing potential eight, net zero; deleting the other edge without scoring loses eight. Thus every Maker choice admits a potential-decreasing reply.

The wording after Proposition A.3 that the only nontrivial issue is vertex deletion must not be read as dismissing unscored edge deletions: the proposition's hypothesis explicitly includes them, and its preceding counterexample uses one. Keeping every permitted reply in the restricted hypothesis repairs that misleading explanatory sentence. The conditional conclusion is a valid implication with this full hypothesis; no evidence here proves that the particular strategy-generated states satisfy it.

## 7. Formalization, publication, and acceptance limits

Buddhdev's Appendix C distinguishes finite core artifacts from complete analytic theorems. It reports zero-sorry finite shield/cover/compression cores. It calls the fan lower bound prose-only. The 5/16 artifact retains a bundled prime-prefix and game-tree placeholder. The sub-0.19 artifact named eventually_strict_lt_point19_of_componentwise_close establishes an endgame implication from close moment values; it does not by itself supply local density, envelope inversion, measure convergence, queued prime rounding, all analytic inputs, or the entire game strategy. We did not inspect or run those artifacts and do not independently certify their reported status. No Lean status is offered for the Silva note.

The author-hosted manuscript and GitHub note are primary written sources, sufficient to audit their arguments, but neither hosting location establishes peer review. The manuscript refers to a submission and an artifact tag; this audit did not establish a journal acceptance, arXiv accession, or independent end-to-end formal replay. AI-assistance disclosures neither prove nor disprove correctness; acceptance here rests on the reconstructed mathematics and bounded exact calculation.

This publication edition distributes the complete authored mathematical audit and certificate proof, acceptance reports, and permitted public-source and verification metadata. Source texts/PDFs, images, executable code and raw numerical records remain private verification materials and are excluded. No mathematical program or proof assistant was rerun during editorial preparation.

## Acceptance ledger

- Original convention: ACCEPTED as a statement of the original problem, with starting player unspecified.
- Earlier 1/8 lower bound, Prolonger first: ACCEPTED by written reconstruction using standard PNT/Mertens.
- Improved 1/2 lower bound, Prolonger first: ACCEPTED after the explicit previous-Prolonger-move clarification; no numerical or conjectural dependency.
- Integral upper theorem limsup L_P/n<=W4/2: ACCEPTED by the written analytic/combinatorial reconstruction and precise queue clarification.
- Eventual strict L_P(n)<0.19n: ACCEPTED with the independent exact certificate; upper also extends to Shortener first by the explicitly checked turn count.
- Printed tighter 0.1897123371 and its narrow component intervals: NOT independently certified; no need to accept them for the strict threshold.
- Squared-log lower scale: CONDITIONAL ONLY on both strategy-generated safe-edge assumptions, retaining unscored deletion replies.
- End-to-end Lean proof / peer-reviewed acceptance / exact asymptotic order / L_P=L_S / global novelty: NOT claimed.
