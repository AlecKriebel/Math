# Exact reductions and baseline bounds for random projective plane transversals

**Target:** 30006390 / OWR-14299518-003. **Duplicate:** 30006391.
**Status:** verified partial analysis; original conjectured lower bounds remain unsolved. Current three-family validation passes; fresh full acceptance review pending.
**Date:** 30 September 2026. **Model:** gpt-6-astra, xhigh.

The original Conjecture5 restricts q to large prime powers and asks to hit all line sections, without an explicit exception for empty ones. This baseline extends the elementary estimates to every existing finite projective plane of order q>=2. The catalogue convention defines tau for every realization by hitting only nonempty sections; it differs from the literal source on finite realizations with an empty section, whose probability is at most n*2^(-(q+1))=o(1). Thus the two conventions give the same asymptotic target, rather than identical finite statements. Limits below run through unbounded existing plane orders, uniformly over planes at each order. Imported source_records.json is preserved as historical provenance; its literal typography-only verification claim is qualified in CURRENT_SOURCE_SCOPE.md.

Let \(\Pi_q\) be any projective plane of order \(q\), with point set \(P\), line family \(\mathcal L\), and \(n=q^2+q+1\). Retain each point independently with probability \(1/2\), obtaining \(R\). Write \(\tau(R)\) for the minimum cardinality of a subset of \(R\) meeting every nonempty section \(L\cap R\).

The elementary bounds established below are

\[
q+\sqrt q+1\le \tau(R)\le (1+o(1))q\log q
\qquad\text{with high probability},
\]

where logarithms are natural. These are baseline estimates, not a new resolution. In particular the lower bound divided by \(q\) tends to one. It does not give a function tending to infinity.

## Reduction to ordinary blocking sets

Each line has \(q+1\) points. The union bound gives

\[
\Pr(\exists L:L\cap R=\varnothing)\le n2^{-(q+1)},\qquad
\Pr(\exists L:L\subseteq R)\le n2^{-(q+1)}.
\]

Outside these two exceptional events, every section is nonempty, \(\tau(R)\) is the minimum size of an ordinary blocking set contained in \(R\), and every such blocking set contains no whole line. Thus the catalogue's convention about nonempty sections does not affect the asymptotic target.

## A self-contained classical lower bound

Let \(B\) meet every line but contain no line, and write \(k=|B|\). Counting incidences gives \(k(q+1)\ge n\), so \(k\ge q+1\). Put \(a=k-q-1\ge0\).

For any line \(L\), choose \(x\in L\setminus B\), possible because \(B\) contains no line. The \(q\) other lines through \(x\) each need a point of \(B\setminus L\), and those portions are pairwise disjoint. Therefore

\[
r_L:=|B\cap L|\le k-q=a+1.
\]

Since \(r_L\ge1\), we have \(r_L(r_L-1)\le(a+1)(r_L-1)\). Sum over the lines. Every ordered pair of distinct points lies on exactly one line, while every point lies on \(q+1\) lines, so

\[
k(k-1)\le(a+1)\bigl(k(q+1)-n\bigr).
\]

Substituting \(k=q+a+1\), the difference between the right and left sides is \(q(a^2-q)\). Hence \(a\ge\sqrt q\), proving

\[
|B|\ge q+\sqrt q+1.
\]

This is the classical Bruen bound, reproduced here to make the baseline independently checkable. Together with the previous union bounds it gives the asserted random-set lower bound. No classification of equality cases is used.

## An alteration upper bound

With high probability, simultaneously

\[
|R|=(1+o(1))n/2,\qquad
m:=\min_{L\in\mathcal L}|L\cap R|=(1+o(1))q/2.
\]

For example, the binomial Hoeffding bound with deviations \(\sqrt{3(q+1)\log q}\), followed by a union bound over \(n\) lines, proves the line assertion; ordinary binomial concentration proves the size assertion.

Fix any realization satisfying these statements. Choose a temporary subset \(T\subseteq R\) by retaining each point with probability

\[
\rho=\frac{\log(q+1)}{m}<1
\]

for sufficiently large \(q\). For every line missed by \(T\), add one point of its nonempty section in \(R\). The resulting set is a blocker contained in \(R\), and its expected size is at most

\[
\rho|R|+\sum_{L\in\mathcal L}(1-\rho)^{|L\cap R|}
\le \frac{|R|\log(q+1)}m+\frac{n}{q+1}
=(1+o(1))q\log q.
\]

At least one outcome has size no larger than this expectation. This is a standard alteration argument; it supplies an upper bound, while the conjecture asks for a growing lower bound.

## The exact counting obstacle

Let \(\mathcal M_q(k)\) denote the family of inclusion-minimal ordinary blocking sets of size at most \(k\). On the event that all line sections are nonempty,

\[
\tau(R)\le k
\quad\Longleftrightarrow\quad
\exists B\in\mathcal M_q(k):B\subseteq R.
\]

Every finite blocker contains an inclusion-minimal one, so this equivalence loses nothing. Consequently

\[
\Pr(\tau(R)\le k)
\le n2^{-(q+1)}+
\sum_{B\in\mathcal M_q(k)}2^{-|B|}.
\]

A bound making the displayed sum tend to zero for \(k=Cq\), for every fixed \(C\), would prove the first conjecture. It is a sufficient counting route, not an established estimate or a necessary condition. Counting all subsets gives at best \(\binom nk2^{-k}\), which grows exponentially in \(q\log q\) at \(k=Cq\). Counting all blockers also badly overcounts families sharing an entire line; minimality removes that particular redundancy but does not by itself supply a usable estimate for nontrivial blockers.

## Why independent incidence deletion does not prove the target

In the different partial-design model, one retains each incidence independently, so the random sections on distinct lines are independent. In the present model, for distinct lines \(L,M\),

\[
\Pr(L\cap R=M\cap R=\varnothing)=2^{-(2q+1)},
\]

whereas the product of the two marginal probabilities is \(2^{-(2q+2)}\). More decisively, for a fixed ordinary blocker \(B\), conditioning on \(B\subseteq R\) already guarantees that every section meets \(B\). There are no remaining independent per-line failure events to multiply. Transferring the source's independent-incidence proof would therefore use a false independence assumption.

The exact diagnostic script checks the incidence identities and enumerates only the 128 point subsets of \(\mathrm{PG}(2,2)\) and the 8192 point subsets of \(\mathrm{PG}(2,3)\). It confirms the reductions and dependence calculation. These finite examples do not establish an asymptotic trend.

## Direct container application fails its hypotheses

Consider the hypergraph whose vertices are all points and whose edges are all complete lines. Its independent sets are exactly complements of ordinary blocking sets. This is an \(s=q+1\)-uniform hypergraph on \(n=q^2+q+1\) vertices, with every vertex of degree \(q+1\).

The packaged [Balogh–Samotij container theorem](https://www.math.tau.ac.il/~samotij/papers/efficient-containers-revised.pdf), Theorem 1.6, requires parameters \(\alpha,\beta,\eta\in(0,1)\) satisfying \(\alpha\beta\eta n\ge 10^9s^7\). Here the parameter called \(q\) in that theorem has been renamed \(\eta\). Since the left side is smaller than \(n<(q+1)^2=s^2\), this requirement is impossible. This rules out that direct application, not every possible auxiliary hypergraph or container argument.

Even the stronger technical Theorem 2.1 does not apply directly. For this regular hypergraph its first degree measure is uniform, so \(\|\sigma_H^{(1)}\|^2=1/n\). The first summand in the theorem's hypothesis already requires

\[
\frac{300s^4}{n}\le\frac1{\delta n}\le\frac p{500}<\frac1{500},
\]

which would imply \(n>150000s^4\), again impossible. Replacing complete lines by shorter collinear subsets would change the independent-set condition: the complement of a genuine blocker may contain many such short subsets. A valid auxiliary construction would need an additional argument preserving the blocking problem.

The cited epsilon-net applications construct different point systems with different line sizes. Their existential bounds do not assert the required statement for the random half of every projective plane. No transfer to the present parameters has been established here.

## Remaining gap

Neither a suitable weighted enumeration of all small minimal blockers nor a different argument excluding them from a random half-set has been established here. In particular, the first-moment reduction transfers the central difficulty to an unproved structural counting statement. The source's growing lower bound and its proposed logarithmic strengthening both remain unresolved in this analysis.
