# Truth-table reduction and a simulation obstruction for K-trivial depth

**30004669 / OWR-7155442-002. The original question remains unsolved, 2/5 approaches. Independent review pending.**

The results below are elementary deductions from credited theorems about K-triviality and relativized depth. They reduce the universal equality question to computably enumerable oracles and identify a precise obstruction to a uniform simulation approach. They do not exhibit a noncomputable oracle with either outcome, decide the general classification, or assert novelty.

## 1. Exact definitions and the known direction

Fix the universal prefix-free oracle machine and computable simulation-overhead convention used in Bienvenu–Delle Rose–Merkle [BDRM, Section 2]. A time bound is an **ordinary total computable nondecreasing** function of the output length. It is not allowed to be merely A-computable. Write

\[
\mathcal D^A=\{X\in2^{\mathbb N}:\ \forall t\ \lim_{n\to\infty}
[K^{A,t}(X\upharpoonright n)-K^A(X\upharpoonright n)]=+\infty\},
\qquad \mathcal D=\mathcal D^{\varnothing}.
\]

Negating this definition gives the exact shallowness quantifiers:

\[
X\notin\mathcal D^A\quad\Longleftrightarrow\quad
\exists t\ \exists b\ \exists^\infty n\quad
K^{A,t}(X\upharpoonright n)\le K^A(X\upharpoonright n)+b. \tag{1}
\]

An oracle A is K-trivial if K(A restricted to n)≤K(n)+O(1) for all n. Nies's lowness theorem, with Hirschfeldt, implies

\[
K^A(\sigma)=K(\sigma)+O(1) \qquad\text{uniformly in finite strings }\sigma. \tag{2}
\]

The constants may depend on A and the machines. This is an unbounded-complexity statement.

BDRM Theorem 6.3 proves

\[
\mathcal D^A\subseteq\mathcal D \qquad(A\text{ K-trivial}). \tag{3}
\]

For completeness, if X is ordinarily shallow, choose t,b witnessing (1) without an oracle. Ignoring A simulates the fast plain descriptions with constant description overhead and an ordinary computable enlarged time bound s. Thus, infinitely often,

\[
K^{A,s}(X\upharpoonright n)
 \le K^t(X\upharpoonright n)+c
 \le K(X\upharpoonright n)+b+c
 \le K^A(X\upharpoonright n)+b+c+d_A.
\]

Hence X is A-shallow. The explicit enlargement from t to s avoids identifying different universal-machine running times. If A is computable, simulating its answers also gives the converse, so equality holds. The source's unresolved alternatives concern **noncomputable** K-trivial A: equality or proper containment in (3), and which possibilities occur.

## 2. A reduction to c.e. K-trivial oracles

### Transfer lemma

Suppose A≤tt B and K^A(σ)≤K^B(σ)+d for all σ, with a fixed d. Then

\[
\mathcal D^B\subseteq\mathcal D^A. \tag{4}
\]

**Proof.** A truth-table reduction is a total oracle procedure with an ordinary computable running-time bound, uniformly over oracle answers. For each ordinary computable t, simulating the A-queries in an A-t-fast description therefore gives an ordinary computable s and a constant c with

\[
K^{B,s}(\sigma)\le K^{A,t}(\sigma)+c\quad\text{for every }\sigma. \tag{5}
\]

This is BDRM Lemma 2.2(ii), with its computable time enlargement. If X is A-shallow, (1), (5), and the assumed unbounded comparison imply infinitely often

\[
K^{B,s}(X\upharpoonright n)
 \le K^{A,t}(X\upharpoonright n)+c
 \le K^A(X\upharpoonright n)+b+c
 \le K^B(X\upharpoonright n)+b+c+d.
\]

So X is B-shallow. Contraposition proves (4). ∎

This uses the same simulation mechanism as BDRM Theorem 3.4. Their Turing-equivalence hypothesis is one sufficient way to obtain the unbounded comparison; equation (2) is another.

In particular, if **both A and B are K-trivial**, then A≤tt B implies

\[
\mathcal D^B\subseteq\mathcal D^A\subseteq\mathcal D. \tag{6}
\]

Consequently equality with ordinary depth passes downward under truth-table reducibility inside the K-trivial class. Strict containment passes upward: the same ordinarily deep, A-shallow X is B-shallow. No arbitrary Turing-reducibility version or Turing-degree invariance is asserted.

### C.e. covering corollary

Nies [N, Theorem 7.4, printed p.301] proves that every K-trivial A is truth-table reducible to a **c.e. K-trivial** B. This is the strong covering theorem, not merely a Turing cover. Applying (6) gives:

1. Equality holds for every K-trivial oracle **if and only if** it holds for every c.e. K-trivial oracle.
2. Some K-trivial oracle has a strict subclass of ordinary deep sets **if and only if** some c.e. K-trivial oracle does.
3. If a particular A admits a strictness witness, that same witness works for every K-trivial truth-table upper bound of A, including the c.e. cover supplied by Nies.

For (1), the nontrivial direction follows from D^B=D and D^B⊆D^A⊆D. For (2), transfer a witness from A to a cover B; the converse is immediate because c.e. K-trivials are K-trivial. A cover of a noncomputable A cannot be computable.

These are reductions of the remaining question. They do **not** prove equality for c.e. oracles, produce a strictness witness, or show that all noncomputable oracles have the same outcome. In particular, they do not transfer an equality example upward.

The later elementary Solovay-function proof in [S, Section 4.4, Corollary 4.13] gives a Turing cover and explicitly distinguishes Nies's stronger truth-table result. That weaker conclusion alone would not justify (5).

## 3. What a successful simulation would need

A sufficient additional condition for the missing inclusion D⊆D^A is

\[
\forall t\ \exists\text{ ordinary computable }s\ \exists c\ \forall\sigma,
\qquad K^s(\sigma)\le K^{A,t}(\sigma)+c. \tag{7}
\]

Indeed, an A-shallowness witness and (7) give infinitely often

\[
K^s(X\upharpoonright n)
 \le K^{A,t}(X\upharpoonright n)+c
 \le K^A(X\upharpoonright n)+b+c
 \le K(X\upharpoonright n)+b+c+e,
\]

where the last inequality holds by ignoring the oracle, without requiring K-triviality. Thus X is ordinarily shallow. Together with (3), condition (7) would give equality for K-trivial A.

No proof of (7) for a noncomputable K-trivial A is supplied. Nor is (7) asserted necessary for equality of the deep classes: it asks for a comparison on **all finite strings**, whereas equality of deep classes is an asymptotic statement along infinite paths.

Lowness (2) only supplies short ordinary descriptions whose decoding times may be unbounded by any chosen computable function. Replacing a short oracle-prefix description by a short plain description therefore does not supply s in (7). Enumerating approximations and waiting for the correct oracle answers likewise needs an effective stopping guarantee that is absent here.

### Uniform-compilation obstruction

There is a fixed ordinary computable time bound t_0 and a computable family of oracle programs p_n such that

\[
U^A(p_n)=A\upharpoonright n
\quad\text{within }t_0(n)\text{ steps, for every oracle A.} \tag{8}
\]

To construct them, use a prefix-free code such as 1^n0 for n, then an oracle machine that asks for bits 0 through n−1 and prints them. Its running time is computably bounded in n, uniformly over all answers. Compile this fixed machine into U and absorb the computable overhead into a nondecreasing t_0. The programs need not be optimal descriptions.

**Proposition.** If A is noncomputable, there is no partial computable function T, defined on all p_n, such that U(T(p_n)) halts and outputs U^A(p_n) for every n.

**Proof.** To compute A(j), compute p_(j+1), run T on it, run the resulting ordinary program, and read bit j. Both computations halt by hypothesis, so this computes A, a contradiction. ∎

In particular, no computable compiler can preserve the outputs of *all* A-programs halting within t_0 of their output lengths, even without a bound on the compiler's overhead or the resulting program lengths. This is stronger than the naive proposed compiler's requirement and rules out that approach for every noncomputable oracle.

It does **not** refute (7). An inequality between the minimum lengths of descriptions does not furnish a computable output-preserving map from oracle programs to ordinary programs. The proposition also says nothing about compilers defined only on a noncomputably selected family of near-optimal descriptions. Failure of this stronger uniform mechanism is not a counterexample to the depth question.

A related obstruction applies to an approximation (A_s). If u and g are ordinary computable, u is unbounded, and A_(g(n)) restricted to u(n) equals A restricted to u(n) for every n, then A is computable: for bit j, search for an n with u(n)>j and inspect the computable finite approximation A_(g(n)). Thus a uniform correct-stage simulation on unbounded prefixes is also unavailable for noncomputable A. No claim is made that a depth-preservation proof must use such a simulation.

## 4. A restriction on possible strictness witnesses

A witness to strictness must satisfy

\[
X\in\mathcal D\setminus\mathcal D^A,
\qquad X\not\le_T A. \tag{9}
\]

For if X≤T A and A is K-trivial, then X is K-trivial by Nies's downward-closure theorem [N, Theorem 6.1]. Moser–Stephan [MS, Theorem 4.6] prove that every K-trivial sequence is shallow, contradicting X∈D. Thus taking X=A, or any sequence computable from A, cannot give a strictness witness. An A-shallow sequence need not itself be computable from A: its near-optimal descriptions in (1) are existentially chosen, not uniformly supplied by A.

This is a credited consequence of those prior theorems, not a new nonexistence theorem for all potential witnesses.

## 5. Exact remaining gap and verification limits

The two approaches stop at distinct precise points:

- Oracle elimination: the available K-trivial lowness controls unbounded description lengths; no finite-string comparison such as (7), or weaker pathwise replacement sufficient for depth, has been proved. A uniform output-preserving compiler would be impossible, but that does not settle the nonuniform comparison.
- C.e. reduction: Nies's truth-table cover transfers the question to c.e. K-trivial oracles. There is still no proof of preservation for all such oracles and no ordinarily deep sequence rendered shallow by one.

The bounded checker verifies the finite change-record/parity mechanism behind a truth-table cover, finite truth-table compositions, class-inclusion directions and the additive inequalities used above. It does not compute genuine Kolmogorov complexity, decide depth of an infinite sequence, construct a noncomputable K-trivial oracle, or prove Nies's cost-function theorem. The universal assertions rely on the written proofs and explicitly credited source theorems.

A bounded primary-literature search found the question explicitly open in the published 2023 paper and in a 2024 author lecture. The 2026 paper *Bridging Computational Notions of Depth* concerns other comparisons and supplies no classification of these oracles. This is not a certification that no later resolution exists. The original target remains **unsolved, 2/5**. No third approach is continued without a new mechanism.

## References

- [Original OWR21/2021 contribution](https://ems.press/content/serial-article-files/46899), printed pp.1162–1164.
- [BDRM: Bienvenu, Delle Rose and Merkle, *Relativized depth*](https://iris.uniroma1.it/bitstream/11573/1713789/1/relativized-depth.pdf), Theoretical Computer Science 949 (2023), 113694; Definitions 2.10 and 3.1, Lemma 2.2, Theorems 3.4 and 6.3.
- [N: Nies, *Lowness properties and randomness*](https://www.cs.auckland.ac.nz/~nies/papers_till_09/Nies_LownessPropertiesRandomness.pdf), Advances in Mathematics 197 (2005), 274–305; Theorems 6.1, 6.2 and 7.4.
- [S: Bienvenu et al., *Solovay functions and their applications in algorithmic randomness*](https://arxiv.org/abs/1603.08351), Journal of Computer and System Sciences 81 (2015), 1575–1591; Section 4.4.
- [MS: Moser and Stephan, *Depth, highness and DNR degrees*](https://dmtcs.episciences.org/4012), Discrete Mathematics & Theoretical Computer Science 19(4) (2017).
- [Bienvenu and Porter, *Bridging Computational Notions of Depth*](https://arxiv.org/abs/2403.04045), primary preprint; published Information and Computation 309 (2026), 105420.
