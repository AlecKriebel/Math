# A null-recurrent renewal law admitting no deterministic nondegenerate scale

**Target 9900002 / AMR-098-0002, Thorisson Problem 1.2. Substantive author turn 1 of 5. Complete negative candidate, pending independent review.**

## 1. Claim and source boundary

There is a strictly positive, non-lattice, infinite-mean interarrival distribution for which **no deterministic positive function** phi(t), even without monotonicity, makes the current total life D_t/phi(t) converge in distribution to a finite nondegenerate random variable as t tends to infinity. The suggested choice phi(t)=E[min(X_1,t)] fails for the same law. These are the two questions of the exact source, not merely its regularly varying special case.

We take zero delay S_0=0, which is allowed by the source. Let X_1,X_2,... be independent with the law below, S_k=sum_{j=1}^k X_j, N(t)=min{k≥1:S_k>t}, and D_t=X_{N(t)}. The half-open renewal interval convention is [S_{k-1},S_k). All limits below are ordinary weak limits on the real line. An infinite constant is not a proper nondegenerate random variable. The elementary argument does not depend on any infinite-mean renewal theorem.

## 2. The interarrival law

For n≥1 put

\[
p_n=2^{-2^n},\qquad a_n=2^{4^n},\qquad
p_0=1-\sum_{n\ge1}p_n.
\tag{1}
\]

With probability p_0, X is uniform on [1,2], and with probability p_n it equals a_n, for each n≥1. These probabilities define a law: p_{n+1}=p_n^2, and

\[
\sum_{n\ge1}p_n=\sum_{j\ge0}(1/4)^{2^j}
\le\sum_{j\ge0}(1/4)^{j+1}=1/3.
\tag{2}
\]

In particular p_0≥2/3. Thus X≥1 almost surely. The positive absolutely continuous component implies P(X∈dZ)<1 for every d>0; the distribution is non-lattice. Its mean is infinite, since

\[
\mathbb E X=\tfrac32p_0+\sum_{n\ge1}p_na_n,
\qquad p_na_n=2^{4^n-2^n}\longrightarrow\infty.
\tag{3}
\]

Every interarrival is nevertheless finite almost surely. Since S_k≥k, N(t) is finite for each finite t and the process is well-defined.

## 3. A first-large-interval estimate

Fix n≥2, and write

\[
q_n=\mathbb P(X\ge a_n)=\sum_{k\ge n}p_k,
\quad M_n=\mathbb E[X\mathbf1_{\{X<a_n\}}],
\quad K_n=\min\{k\ge1:X_k\ge a_n\},
\quad T_n=S_{K_n-1}.
\tag{4}
\]

K_n is geometric with success probability q_n>0, hence finite almost surely. Summing the nonnegative expectations of the successive small intervals gives

\[
\begin{aligned}
\mathbb E T_n
&=\sum_{j\ge1}\mathbb E[X_j\mathbf1_{\{K_n>j\}}]\\
&=\sum_{j\ge1}(1-q_n)^{j-1}M_n
=\frac{M_n}{q_n}.
\end{aligned}
\tag{5}
\]

No independence between T_n and X_{K_n} is needed below. Independently summing over the possible value of K_n gives

\[
\mathbb P(X_{K_n}=a_n)=\sum_{j\ge1}(1-q_n)^{j-1}p_n
=\frac{p_n}{q_n}.
\tag{6}
\]

Put t_n=a_n/2. If T_n≤t_n and X_{K_n}=a_n, then S_{K_n}=T_n+a_n>t_n. Consequently t_n lies in this very interval, including the allowed case T_n=t_n, and D_{t_n}=a_n. Markov's inequality and the union bound give

\[
\mathbb P(D_{t_n}\ne a_n)
\le\frac{q_n-p_n}{q_n}+\frac{2M_n}{q_na_n}.
\tag{7}
\]

All small interarrivals are at most a_{n-1}, since n≥2 and the base component is supported on [1,2]. Thus M_n≤a_{n-1}. Also q_n≥p_n. Since p_{n+j}=p_n^{2^j} and 2^j≥j+1,

\[
q_n-p_n\le\frac{p_n^2}{1-p_n},\qquad
q_n\le\frac{p_n}{1-p_n}.
\tag{8}
\]

Substitution in (7) yields the explicit error bound

\[
\boxed{\quad
\mathbb P(D_{t_n}=a_n)\ge1-\varepsilon_n,\qquad
\varepsilon_n=\frac{p_n}{1-p_n}
+2^{1+4^{n-1}+2^n-4^n}\longrightarrow0.
\quad}
\tag{9}
\]

The last exponent is 1+2^n-3·4^{n-1}, which tends to minus infinity. The times t_n tend to infinity. This is concentration at deterministic lengths along deterministic inspection times, despite the interarrival law's infinite mean and non-lattice component.

## 4. Exclusion of every deterministic scaling

We use the following elementary fact.

**Lemma.** Suppose real random variables Y_n and real constants c_n satisfy P(Y_n=c_n)→1. If Y_n converges weakly to a probability law nu on the real line, then nu is a point mass.

**Proof.** For every bounded measurable f,

\[
|\mathbb E f(Y_n)-f(c_n)|\le2\|f\|_\infty\mathbb P(Y_n\ne c_n).
\tag{10}
\]

Weak convergence of Y_n implies tightness. The probability concentration at c_n then forces the deterministic sequence c_n to be bounded eventually: choose a compact interval with P(Y_n in that interval)>3/4 for all sufficiently large n, and use P(Y_n=c_n)>3/4. Their intersection is nonempty, so c_n belongs to that interval. Choose a convergent subsequence c_{n_j}→c. Equation (10), for bounded continuous f, identifies the same subsequential weak limit as delta_c. Uniqueness of the weak limit gives nu=delta_c. ∎

Now let phi be any deterministic positive function defined at all sufficiently large times. If D_t/phi(t) had a proper nondegenerate weak limit as t→infinity, the sequence

\[
Y_n=\frac{D_{t_n}}{\phi(t_n)},\qquad
c_n=\frac{a_n}{\phi(t_n)}
\tag{11}
\]

would have the same weak limit. But (9) gives P(Y_n=c_n)≥1−epsilon_n→1. The lemma makes that limit degenerate, a contradiction. In particular every positive nondecreasing normalizer is excluded. In fact the lemma excludes arbitrary eventually nonzero real-valued deterministic normalizers too; positivity is simply the usual scaling convention.

The proof does not assert that no degenerate normalization exists. A normalizer producing convergence to zero would not answer the source's nondegenerate-limit question.

## 5. The proposed truncated-mean normalizer

Let m(t)=E[min(X,t)]. It is finite, strictly positive and nondecreasing for t≥1. At t_n all interarrivals smaller than a_n are at most a_{n-1}<t_n, while all others are at least a_n>t_n. Therefore exactly

\[
m(t_n)=M_n+t_nq_n.
\tag{12}
\]

Hence

\[
0<\frac{m(t_n)}{a_n}
\le\frac{a_{n-1}}{a_n}+\frac{q_n}{2}
\le2^{4^{n-1}-4^n}+\frac{p_n}{2(1-p_n)}
\longrightarrow0.
\tag{13}
\]

On the event in (9), D_{t_n}/m(t_n)=a_n/m(t_n)→infinity. Thus, for each fixed real L,

\[
\mathbb P\!\left(\frac{D_{t_n}}{m(t_n)}>L\right)\longrightarrow1.
\tag{14}
\]

This supplies a direct failure of even proper tightness along these inspection times for the source's specific proposed normalizer.

## 6. Scope, provenance, and verification

The construction answers both universal questions in Problem 1.2 negatively, conditional on independent verification of the complete source/proof correspondence. It does not classify which distributions do possess scaling limits. It does not challenge the classical regularly varying limit theorems. It gives no result about Thorisson's separate path-space coupling problems. The universal affirmative premise of the adjacent joint-limit question cannot hold for this example; its conditional formulations are not classified here.

The techniques are elementary mixture construction, geometric stopping, Markov's inequality, and weak-limit tightness. No historical-priority claim is made. SOURCE_GATE.md records the checked primary sources, faulty imported triage statements, and the inability to obtain a full binary/visual copy of Thorisson's original PDF.

The accompanying standalone checker verifies the exact exponent/tail estimates and finite renewal identities used in the argument. It uses exact rational arithmetic; no simulation, floating-point limit inference, or finite test is substituted for the infinite-quantifier proof above. This is AI-assisted research, not human peer review or machine-checked formal proof.
