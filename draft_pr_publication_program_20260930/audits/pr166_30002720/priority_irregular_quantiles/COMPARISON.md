# Priority comparison and checkable derivations

Audit: PR166 / problem30002720; head efc3f35a72543ad9ae76fd31a860116f1ffd4a32. Family: general digital trees, irregular deterministic profiles, inverse-distribution moduli, and discontinuity neighborhoods. This document separates published statements from deductions assembled during this audit. It is a priority comparison, not a replacement mathematical validation of the submitted proof.

## 1. Exact dictionary

Let independent strings have stationary initial law (1/2,1/2) and transition matrix

\[
P=\begin{pmatrix}3/4&1/4\\1/4&3/4\end{pmatrix}.
\]

For a prefix w write π(w)=P(S starts with w), and set π(∅)=1. With Λ_{n,d}(s) the number of sample strings sharing the first d letters of s, the cost is

\[
Z_n(s)=\sum_{d\ge0}\Lambda_{n,d}(s)\mathbf1\{\Lambda_{n,d}(s)>1\},\qquad
Y_n(k)=Z_n(S_{(k)}).
\]

Thus the singleton bucket contributes zero. Define m(s)=Σ_{d≥0}π(s^d), the source CDF F in lexicographic order, its canonical inverse h, and g=m∘h. If U_i=F(S_i), then U_i are independent Uniform(0,1), S_i=h(U_i) almost surely, and

\[
Y_n(k)=Z_n(h(Q_n)),\qquad Q_n=U_{(k)}.
\]

The candidate fixes v with v_r=1 exactly when r=j², j≥2, takes t=F(v), and k_n=⌊nt⌋+1. Its conclusion is: for every deterministic real sequence c_n, the laws of (Y_n(k_n)−c_n)/√n are not tight. The rank is fixed as n varies; v has infinitely many zeros and ones, so it is not an eventually constant endpoint representation and t is a continuity rank.

The closest published process result uses exactly Z, Y, π, F, h, m and the same stopping rule. Its string-indexed theorem implies

\[
R_n:=\sup_s|Z_n(s)-nm(s)|/\sqrt n=O_P(1).
\tag{1}
\]

Consequently, even at a data-dependent selected string,

\[
Y_n(k_n)=n g(Q_n)+O_P(\sqrt n).
\tag{2}
\]

This is an inference from uniform convergence, not from a fixed-string central limit theorem. [Leckey–Neininger–Sulzbach, Theorem 1.2](https://www.math.uni-frankfurt.de/~neiningr/radix_journal.pdf).

## 2. What is required for the explicit continuity rank

Continuity of g at t yields only g(Q_n)−g(t)→0 in probability. It supplies no bound on √n[g(Q_n)−g(t)]. In particular, first-order convergence and fluctuation failure are compatible.

The candidate's additional geometry is as follows. Put q=3/4, W_j=v^{j²−1}, P_j=π(W_j), and let τ_j be the boundary between a_j=W_j0 1∞ and b_j=W_j1 0∞. The explicit calculation in the allowed candidate gives

\[
P_j=\tfrac12(\tfrac14)^{2j-4}q^{j²-2j+2},\qquad
m(a_j)-m(b_j)=P_j,
\]

\[
0<t-\tau_j<P_jq^{2j}/12.
\tag{3}
\]

Take w_j=P_jq^j, K_j=⌊j/2⌋ and n_j=⌈w_j^{-2}⌉. The two local profile bands on (τ_j−w_j,τ_j) and (τ_j,τ_j+w_j) differ by P_j, with error at most P_jq^{K_j} in either band. Thus

\[
(t-\tau_j)/w_j\to0,\quad \sqrt{n_j}w_j\to1,\quad
\sqrt{n_j}P_j\ge q^{-j}\to\infty.
\tag{4}
\]

The ordinary uniform-order-statistic central limit theorem gives

\[
\sqrt n(Q_n-t)\Rightarrow N(0,t(1-t)).
\]

It follows that both bands have limiting probability

\[
\rho=\Phi(1/\sqrt{t(1-t)})-\tfrac12>0.
\]

Equation (1) makes the cost remainder negligible relative to n_jP_j, since √n_j/(n_jP_j)→0. The cost therefore has two probability bands separated by a quantity of order n_jP_j≫√n_j. For every fixed M, every interval of radius M√n_j can meet at most one band for large j. Hence

\[
\limsup_j\sup_{a\in\mathbb R}
P(|Y_{n_j}(k_{n_j})-a|\le M\sqrt{n_j})\le1-\rho.
\tag{5}
\]

Equation (5) is sufficient for failure under every deterministic center. This reconstructs the candidate's mechanism using a published, sharper uniform remainder estimate. Equations (3)–(4) and the local band lemma are candidate-specific inputs: the prior theorem does not supply them. This is a supported deduction once those new lemmas are available; it is not containment in an earlier theorem.

## 3. Post-seal Baire deduction: existence without square geometry

The following argument was assembled during this audit after the first assessment was sealed. The parent supplied a scientific question proposing this route, not a verdict or sibling assessment. No earlier radix application of this argument was located in the inspected primary sources. It establishes existence, and a residual set, rather than identifying v.

Let D be the countable set of all cylinder endpoints, and let B⊆D be the dense set at which g has a nonzero jump. The density of B is part of the published boundary argument for the present nonmemoryless source. For this particular matrix it can also be checked directly: if W is a nonempty prefix ending in i, and C=Σ_{d≤|W|}π(W^d), then

\[
m(W0 1^\infty)=C+2\pi(W)p_{i0},\qquad
m(W1 0^\infty)=C+2\pi(W)p_{i1}.
\]

The left-minus-right jump is +π(W) for i=0 and −π(W) for i=1. The root midpoint has zero jump, which does not affect density. Cylinder lengths tend to zero and any interval contains a finer cylinder, so the nonzero-jump endpoints are dense.

At any fixed b∈B, the number of U_i below b is Binomial(n,b). The rank ⌊nb⌋+1 lies to either side with probabilities tending to 1/2. Q_n→b, and the one-sided profile limits and first-order cost control therefore give

\[
Y_n(\lfloor nb\rfloor+1)/n
\Rightarrow \tfrac12\delta_{g(b-)}+\tfrac12\delta_{g(b)}.
\tag{6}
\]

This is a deduction from the published proof, whose stated non-tightness uses specified centers. [LNS, Proposition 2.9 and its proof](https://www.math.uni-frankfurt.de/~neiningr/radix_journal.pdf).

A general elementary consequence of weak convergence is useful here: if V_n⇒V and r_n→0, then

\[
\limsup_n\sup_aP(|V_n-a|\le r_n)\le\sup_aP(V=a).
\tag{7}
\]

Proof: choose near-maximizing a_n along a subsequence. Tightness gives probability tending to zero if |a_n|→∞. Otherwise extract a_n→a; for every δ>0, the shrinking intervals eventually lie inside [a−δ,a+δ]. The closed-set bound for weak convergence, followed by δ↓0, gives (7). Applying (7) to (6), with r_n=M/√n, yields

\[
\limsup_n C_n(b,M)\le\tfrac12,
\quad C_n(t,M):=\sup_aP(|Y_n(\lfloor nt\rfloor+1)-a|\le M\sqrt n).
\tag{8}
\]

Now let X=(0,1)\(D∪Q). This is a dense Gδ subset of R, hence completely metrizable and Baire. The ordinary Euclidean metric on X is not complete; complete metrizability is the needed statement. A direct check removes any dependence on that metric restriction: enumerate D∪Q∪{0,1} as (d_j), and use

\[
d_*(x,y)=|x-y|+\sum_{j\ge1}2^{-j}\min\{1,|\,|x-d_j|^{-1}-|y-d_j|^{-1}|\}.
\]

Finite-coordinate continuity and the bounded series tail give the same topology on X. A d_*-Cauchy sequence is Euclidean Cauchy in [0,1]; each reciprocal-distance coordinate is Cauchy and hence bounded. Its limit cannot be any d_j, including 0 and 1, so it belongs to X, and convergence in d_* follows by the same bounded-tail argument. This proves completeness. For each fixed n,M, C_n(·,M) is locally constant on X, because k_n(t)=⌊nt⌋+1 is constant off its rational breakpoints. Thus, for positive integers M,N,

\[
E_{M,N}:=\{t\in X:C_n(t,M)\ge3/4\text{ for every }n\ge N\}
\]

is closed in X.

To prove empty interior, take any nonempty relative open interval I∩X. Choose b∈B in the interior of I. For sufficiently large n≥N, equation (8) gives C_n(b,M)<3/4. The rank cell containing b has a nonempty right-hand portion inside I. This remains true if b is exactly a grid breakpoint: k_n(b) uses the right-hand rank. Removing the countable D∪Q leaves a nonempty relative open subset of that portion, on which the distribution and C_n are the same as at b. This subset is disjoint from E_{M,N}. Therefore every E_{M,N} is nowhere dense.

By Baire,

\[
\mathcal R=X\setminus\bigcup_{M,N\ge1}E_{M,N}
\]

is dense Gδ in X (and in (0,1)). Every t∈𝓡 satisfies

\[
\forall M,N\in\mathbb N\ \exists n\ge N:\ C_n(t,M)<3/4.
\tag{9}
\]

For any deterministic centers c_n, equation (9) gives arbitrarily large n with P(|Y_n(k_n)−c_n|>M√n)>1/4, for every integer M. Thus the centered laws are not tight. These are fixed nonboundary continuity ranks.

The mathematical bridge to an existential result is therefore supported and needs no square-word geometry. It is a newly assembled application of old machinery, not evidence that an earlier author stated it, and not evidence that the candidate's named rank lies in R. Classical linear uniform boundedness is inapplicable directly: t↦C_n(t,M) is not a family of bounded linear maps on a Banach space. Baire itself suffices. The complete relevant proofs were read in [Müger, Theorem 3.3.1, Proposition 3.4.18, Theorem 3.4.20](https://www.math.ru.nl/~mueger/topology.pdf); the text's linear Theorem G.5.7 was also checked and is not the applied theorem.

## 4. General-source and inverse-modulus exclusions

| Source inspected | Exact random object and hypotheses | Dictionary result / exact gap |
|---|---|---|
| Mahmoud–Flajolet–Jacquet–Régnier, INRIA RR3399 (1998), §2.2, Theorem 2 and proof | Same singleton-stopped bucket cost, uniform independent digits, independent uniform target rank | Uniform-source grand average has center Bn/(B−1) and root-n Gaussian limit. Neither persistent Markov dependence nor the fixed rank is covered. An average over ranks cannot imply all fixed-rank behavior. |
| Clément–Flajolet–Vallée, RR3645 (1999), Theorems 5–6 and proofs; Markov Corollary 2 | Dynamical sources including Markov; aggregate trie size, total path length and height | The source dictionary can match. The cost sums over all prefixes or counts path depth, rather than bucket populations along one selected order-statistic path. No exact cost identity bridges these objects. |
| Devroye (1992), Lemma D1, Theorem D2 and proof | Independent numeric keys with Lebesgue density; unweighted insertion/branch depth | The binary numeric distribution here is singular. Markov flip frequency is almost surely 1/4, whereas Lebesgue binary flip frequency is 1/2. The depth statistic also differs from Y. |
| Cesaratto–Vallée (2015), Definition 3; Theorem 2.5 and proof; Theorem 3.5 and §3.7 | Uniformly selected branch depth, with analytic strong-tameness conditions on Λ(s,v) | Global random-branch depth has logarithmic mean/variance. A fixed lexicographic quantile and weighted bucket cost are absent. The text distinguishes good simple sources and possible slow remainders; “Markov” alone is not a license to invoke every rate. |
| Knight (1998), A1–A3, Theorem 1, Corollary 2 and complete proof | Convex L1-regression objective; iid errors with continuous median CDF and convergent local scaled integrals | The intercept case gives nonregular sample medians. The profile g is not an inverse CDF: every interval contains both upward and downward jumps, using prefixes ending in 0 and 1. The required monotonicity/convex local dictionary is missing. |

Primary manuscripts: [RR3399](https://algo.inria.fr/flajolet/Publications/MaFlJaRe98.ps), [RR3645](https://algo.inria.fr/flajolet/Publications/RR-3645.pdf), [Devroye](https://luc.devroye.org/devroye_1992_a_study_of_trie_like_structures_under_the_density_model.pdf), [Cesaratto–Vallée](https://ri.conicet.gov.ar/bitstream/11336/38329/2/CONICET_Digital_Nro.90d6d091-5ac8-45ad-a5cd-f44e4469a5d9_A.pdf), [Knight](https://www.math.pku.edu.cn/teachers/xirb/Courses/QR2013/Kight%28Annals1998%29.pdf).

The inverse-CDF objection does not assert that all nonregular quantile theorems are irrelevant. It states the exact missing dictionary for the theorem actually checked. Non-differentiability alone never proves non-tightness: a locally constant profile yields zero profile fluctuation. A valid general profile theorem must control this signed, discontinuous modulus at the fixed t.

## 5. Typical-rank scope and historical limitations

The inspected 2014 rank theorem is first order, at every nonboundary t. The 2015 thesis expressly asks how marginal limits depend on continuity of the profile. The 2019 manuscript supplies boundary obstructions, random-profile centering, and deterministic-centering process limits for the binary memoryless family. None supplies a deterministic-centered, root-n theorem for almost every fixed rank of this persistent source. Grand averages, uniformly chosen branches, and data-dependent centers do not answer that question.

The new Baire deduction is topological. It makes no Lebesgue-almost-everywhere assertion and neither establishes nor contradicts a possible measure-theoretic typical-rank theorem. The candidate's one explicit rank is therefore not proven to be merely an exceptional departure from known typical deterministic-rank Gaussian behavior.

The accepted manuscript was read through its institutional web parser and compared on the relevant theorem pages. Its binary download returned 403; the independently retained author manuscript is the theorem/proof source. Final publisher typesetting was not certified. The Cesaratto–Vallée file is an institutional author proof with line numbers. Recent Quickselect work was screened on its actual random-pivot, comparison-cost and random-limit centering definitions; no assertion is made about a theorem proof not fully inspected. Smirnov was only a bibliographic lead, with no original theorem relied upon.

Conclusion: substantial published mechanism overlap; a fully supported new existential deduction; no exact earlier theorem/application located for the named square-position rank. This bounded audit does not establish novelty.
