# PR19 / 30006390: independent probability-family adversarial audit

Target head: `f1053196b6405623d5f5d8611289939765918d72`. Exact-head baseline SHA-256: `9e0a930e61d849799c4395024c85d4f9c75b63ae2172321ef78ebf643f283c82`.

**Disposition: PASS for the probability/concentration/alteration/reduction claims as unresolved partial analysis. No mathematical must-fix found in this family.** Neither the divergent lower factor nor a logarithmic lower factor is proved. The baseline lower factor tends to one. The weighted counting route is blocked at a substantive enumeration statement, not completed by its reduction.

This report was reconstructed independently before reading historical reviews or scripts; `INDEPENDENT_SEAL.md` preserves that checkpoint. Subsequent replay and historical comparisons corroborate the independently derived claims. No sibling mathematical conclusions were used. All writes are confined to this audit family. No Git actions, canonical mutations, installations, outreach, release, DOI, or publication occurred, and the original substantive-attempt ledger remains 2/5.

## Exact scope and strongest verified result

For any projective plane of order q, let n=q²+q+1 and retain each point independently with probability 1/2. Let tau(R) be the minimum size of a subset of R meeting every nonempty line section. With natural logarithms,

\[
q+\sqrt q+1\le\tau(R)\le(1+o(1))q\ln q
\]

with probability tending to one. The bounds and their error terms below are uniform over all planes at a given order, including non-Desarguesian ones. Limits run through unbounded orders for which the requisite planes exist. The original source specifically states prime-power orders; the baseline's incidence-only argument legitimately has broader scope. Integer lower sizes mean at least the ceiling of the real-valued lower bound.

The strongest directly checkable quantitative version in this family is: for every q≥4096 and every plane of that order, put

\[
t_q=\sqrt{3(q+1)\ln q},\quad s_q=\sqrt{3n\ln q},\quad
U_q=\frac{(n/2+s_q)\ln(q+1)}{(q+1)/2-t_q}+\frac n{q+1}.
\]

Then

\[
\Pr\{q+\sqrt q+1\le\tau(R)\le U_q\}
\ge 1-2n2^{-(q+1)}-2(n+1)q^{-6},\qquad
\frac{U_q}{q\ln q}\longrightarrow1.
\]

The value 4096 is a convenient explicit sufficient threshold, not an optimized threshold. Numerical evaluations in the fresh controls are diagnostics of this formula; the universal proof below supplies the asymptotic conclusion.

## Concentration: a self-contained universal certificate

For X distributed as Binomial(N,1/2),

\[
\mathbb E e^{\lambda(X-N/2)}=\cosh(\lambda/2)^N
\le e^{N\lambda^2/8}.
\]

To verify the inequality, for u≥0 use tanh(u)≤u, since tanh(0)=0 and its derivative is at most one. Integrating yields ln(cosh(u))≤u²/2; symmetry covers negative u. Markov's inequality and λ=4a/N give

\[
\Pr\{|X-N/2|\ge a\}\le2e^{-2a^2/N}.
\]

This proof works also for deviations larger than the support, when the actual tail is zero; it does not require a hidden small-deviation restriction. Each individual line cardinality has N=q+1 independent summands, and |R| has N=n independent summands. Taking a=t_q or s_q and union bounding gives simultaneous two-sided line and global-size control with failure at most 2(n+1)q^-6. Distinct line sums are correlated; none of this reasoning multiplies their probabilities.

On that event, m=min_L |L∩R| is at least (q+1)/2-t_q, and |R|≤n/2+s_q. Both have the asymptotics used in the baseline, uniformly over the plane. For q≥4096, ln(q)≤sqrt(q) and 48sqrt(q)≤q imply 48ln(q)≤q+1, so t_q≤(q+1)/4. Also ln(q+1)≤sqrt(q+1)<(q+1)/4. Therefore m>ln(q+1)>0 and rho=ln(q+1)/m lies strictly between zero and one.

I read all 19 pages of the original [Hoeffding paper](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf), including its cover, after locally extracting OCR in ignored temporary storage, and visually checked Theorem 1 (2.3), Theorem 2 (2.6), and the proof's (4.15)–(4.16). Its concentration exponent agrees with this independent derivation. OCR errors were not used to settle the formulas.

## Alteration: conditioning, repairs, expectation, and endpoints

Fix a good realization R. Thin its points independently at rho. A line with r retained points is missed with probability (1-rho)^r, regardless of what happens on other lines. For every missed line add one point from its nonempty R-section. The union of T and these repairs is contained in R and meets all lines. Repairs can coincide; the cardinality is bounded above by |T| plus the number of initially missed lines. Thus

\[
\mathbb E|B|\le\rho|R|+\sum_L(1-\rho)^{|L\cap R|}
\le\frac{|R|\ln(q+1)}m+\frac n{q+1}\le U_q.
\]

The miss-event sum uses linearity of expectation, not independence. At least one outcome has cardinality at most the expectation. This is an existential construction for each good R, and combining it with the probability of good R proves the asserted high-probability upper bound. It does not claim every random thinning outcome has small size. Dividing U_q by q ln(q), using t_q/(q+1)→0, s_q/n→0, n/(q+1)=q+1/(q+1), and ln(q+1)/ln(q)→1 proves its leading constant one.

The division by m is intentionally restricted to the good event; for R empty, m=0 while tau(R)=0 under the nonempty-section convention. Small-q negative deviation lower bounds are not asserted to give usable rho. The underlying repair-and-expectation argument remains valid at rho=0 or rho=1 whenever every section to repair is nonempty. Exact fresh controls include these endpoints, identical sections, sections sharing a center, singleton sections, cycles, and no sections. They check actual repaired-set sizes and duplicate repairs with rational probabilities; they do not assume that abstract controls are projective planes.

## Lower-bound exception and shared-point controls

Let p=2^(-(q+1)). Empty-line and whole-retained-line events each have probability at most np. In fact these global events are disjoint: a full line meets every other line and thereby prevents every empty line. Complementation of R gives equal probabilities. The first two Bonferroni terms and the shared-point pair probability give the fresh universal control

\[
2np-2n(n-1)p^2
\le\Pr\{\text{some empty or full line}\}\le2np.
\]

The lower-to-upper ratio is 1-(n-1)p→1; no classification or coordinates enter. Outside these exceptions, a section-transversal is an ordinary blocker containing no whole line. The baseline's incidence counting then proves Bruen's bound: for k=q+a+1, each line occupancy r_L is at most a+1, and summing r_L(r_L-1)≤(a+1)(r_L-1) gives q(a²-q)≥0. This lower factor is 1+q^-1/2+q^-1, so it does not diverge.

For distinct lines, both empty has probability 2p², so covariance of their empty indicators is p². For a stronger universal dependence control, fix a point x. Its q+1 incident lines partition P minus x into q+1 disjoint q-point petals. If K is the number of empty lines through x, its probability-generating function is

\[
\mathbb E z^K=\tfrac12+\tfrac12(1-2^{-q}+2^{-q}z)^{q+1}.
\]

If x is retained K=0; otherwise the petals are independent and K is binomial with parameters q+1 and 2^-q. Consequently its second factorial moment is (q+1)q·2p², and its probability of at least one empty line is [1-(1-2^-q)^(q+1)]/2. The fresh script verifies this distribution exactly, with direct enumeration of 128, 8192, and 2,097,152 local pencil states for q=2,3,4. This is a control of an analytically proved all-plane identity, not a finite-order conjecture trend. The q=4 pencil is an abstract local partition; no prime-field arithmetic is falsely used to construct PG(2,4).

In alteration, if two R-sections of sizes r,s share a retained point, their joint miss probability is (1-rho)^(r+s-1), and covariance is rho(1-rho)^(r+s-1). If their common point is absent from R, the sections are disjoint and their miss events are independent. Both cases support the use of expectation but rule out a blanket independence assertion.

## Why the independent-incidence proof cannot transfer

I independently read the complete seven-page [Alon author paper](https://web.math.princeton.edu/~nalon/PDFS/remark191.pdf) and the entire Alon contribution, pp. 2249–2251, in the [OWR report](https://ems.press/content/serial-article-files/52246?nt=1). Conjecture 5 uses one independent random choice per point. The partial-design proof instead independently samples points separately on each line and explicitly treats the line subsets independently. Its Claim 2.2 multiplies those independent failure probabilities. The source uses base-2 logarithms in that proof; the baseline declares natural logarithms, and only constant-insensitive conjectural rate comparisons transfer.

For any fixed ordinary blocker B, the exact shared-point probability that B is contained in R is 2^-|B|, and conditional on its containment every line is already hit. There are no additional independent line failures to charge. A completely explicit negative control takes B to be a whole line. Its shared-point containment probability is 2^(-(q+1)); in the independent-incidence model its probability of hitting all independently sampled sections is

\[
2^{-(n-1)}(1-2^{-(q+1)}).
\]

The ratio of these different event probabilities is 2^(q²-1)/(1-2^(-(q+1))). The line candidate belongs to the baseline's explicitly excluded whole-line event, so this comparison is not a counterexample to its lower bound. It is an exact obstruction to importing the other sampling model's product proof.

The candidate B must also be fixed before using probability 2^-|B|. Choosing the first retained point, or point zero if R is empty, gives an adaptively chosen singleton of fixed cardinality one whose containment probability is 1-2^-n, rather than 1/2. The weighted enumeration argument avoids this error by ranging over a deterministic family of all eligible witnesses.

## First moment: exact reduction and a fresh minimality control

On the no-empty-line event, tau(R)≤k if and only if some inclusion-minimal ordinary blocker of size at most floor(k) lies in R. Every finite blocker contains such a minimal blocker, and its size cannot increase on deletion. This is inclusion-minimality, not the stronger and unnecessary requirement of having globally minimum cardinality. For each deterministic B the containment probability is 2^-|B|; therefore the weighted union bound in the baseline is valid. The whole-line blockers contribute n2^(-(q+1)), which already tends to zero. The unsolved part concerns the full family of nontrivial minimal blockers of linear size.

Fresh control: minimality does not make a vanishing first moment necessary. Take an abstract hypergraph on a core S of t vertices and a disjoint optional set U of 4t vertices. Its edges are all singleton core vertices and all (3t+1)-subsets of U. Its minimal blockers are exactly S union A for A a t-subset of U. A random half-set contains one with probability

\[
2^{-t}\Pr\{\operatorname{Bin}(4t,1/2)\ge t\}\le2^{-t}\to0,
\]

but their expected number is W_t=binomial(4t,t)2^(-2t), which grows. This is a family of minimal blockers and an antichain, not an overcount caused merely by nonminimal supersets. It is deliberately not a projective-plane construction.

For every t≥3, the ratio W_(t+1)/W_t is at least two. After clearing positive denominators, the required difference is

\[
40t^4-8t^3-136t^2-112t-24.
\]

Putting t=u+3 gives 40u⁴+472u³+1952u²+3176u+1440, whose coefficients are all positive. This is a universal algebraic certificate, independently checked by the script. Finite exact hypergraph enumeration at t=1,2 additionally verifies the minimal-witness description. Therefore the baseline is right to label its first-moment requirement sufficient, not necessary. No claim is made that this generic counterexample occurs among projective blockers.

## Fixed-C versus a growing function

Write X_(q,Pi)=tau(R)/q. To obtain a single growing function for all planes, sufficient first-moment estimates should mean

\[
\sup_{\Pi\text{ of order }q}W_{q,\Pi}(\lfloor Cq\rfloor)\to0
\quad\text{for every fixed }C>0.
\]

For a single prescribed sequence of planes, the corresponding pointwise statement suffices and the diagonal function may depend on that sequence. Convergence along every possible plane sequence is equivalent to the uniform formulation: failure of uniformity permits choosing a bad plane along a subsequence. The baseline's proven error terms are already uniform, so there is no all-plane gap in its elementary bounds.

For clarity, suppose the uniform probabilities delta(q,j)=sup_Pi P(X_(q,Pi)≤j) tend to zero for every positive integer j. Choose strictly increasing Q_j with Q_j≥j such that delta(q,j)≤1/j for all admissible q≥Q_j. Let f(q) be the largest j≤q with Q_j≤q, using any fixed initial value before Q_1. Then f(q)→infinity and P(X_(q,Pi)≤f(q))≤1/f(q), uniformly. This checks the strict target X>f(q), including rounding. It does not produce a logarithmic rate: even the deterministic sequence X_q=sqrt(ln(q)) diverges while X_q/ln(q)→0.

None of the required fixed-C estimates is established in this package. For k=floor(Cq), naive subset enumeration has log[binomial(n,k)2^-k]=Cq ln(q)+O(q), a growing and useless union bound; the family of sizes at most k is no smaller for this purpose. No hidden counting theorem follows from incidence regularity, Bruen's inequality, or minimality. The route remains blocked at the exact enumeration/exclusion claim.

## Reproducibility, source fidelity, and limitations

Both original scripts were first read only after the seal, copied byte-for-byte into separate ignored temporary directories, and run with Python 3.14.6. The author output matched the snapshot's `check_results.json` byte-for-byte, and the historical independent reviewer output matched `review/independent_checks.json` byte-for-byte. Their assertion and finite-plane diagnostics corroborate the baseline but do not prove its asymptotic statements; those were reconstructed analytically here.

The new `fresh_probability_controls.py` imports no author/reviewer code, uses only the standard library, and passes 4,958 checks. It uses distinct mechanisms: universal pencil mixtures, exact correlated repair expectations, event-disjointness/Bonferroni controls, model-transfer and adaptive-witness negative controls, a minimal-blocker hypergraph family, and a polynomial positivity certificate. Its displayed decimal values are evaluations, not interval certificates; no conclusion relies on their finite sampling or precision.

The 13 source snapshot files are checked unchanged before and after this audit. Hashes, runtime version, replay comparisons, and primary-source evidence are recorded in `replay_comparison.json` and `hash_manifest.json`. Downloaded foreign PDF/OCR, copied scripts, and raw replay outputs remain under ignored `tmp/`; persistent deliverables contain first-party audit material only.

This family does not independently certify container theorem hypotheses, their epsilon-net applications, novelty, exhaustive current literature status, a human peer review, or a formal proof certificate. Those issues are outside its assigned probability mechanism. Its verdict is sufficient only for the stated probability baseline and precise unresolved-gap classification.
