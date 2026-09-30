# AND layers and average maximal sensitivity: a scoped obstruction package

**Original target unresolved after two approaches.** The calculations below
prove elementary restricted bounds and identify a false proof shortcut. They
supply neither a proof nor a counterexample to Rossman's conjecture, including
its weaker subpolynomial version. No novelty is claimed. Separate adversarial
review is pending.

## 1. Exact statement and conventions

The complete source is Benjamin Rossman's contribution, pp.2825–2826 of
[Oberwolfach Report 52/2009](https://ems.press/journals/owr/articles/4135),
*The k-Clique Problem on Random Graphs & New Conjectures on AC⁰*.
For functions on the uniformly distributed n-dimensional Boolean cube, write

\[
 s(f,x)=\#\{t\in[n]:f(x)\ne f(x\oplus e_t)\},\qquad
 \operatorname{ams}(f_1,\ldots,f_m)
   =2^{-n}\sum_x\max_{j\le m}s(f_j,x).
\]

The maximum is **inside** the expectation. It is neither the mean of the
worst-case sensitivities nor the maximum of their means. Both 0-inputs and
1-inputs contribute, and no monotonicity assumption is imposed.

The precise proposed induction step concerns n functions f₁,…,fₙ on n bits,
and n functions

\[
 g_i=\bigwedge_{j\in S_i}f_j,\qquad S_i\subseteq[n].
\]

For fixed d, does \(\operatorname{ams}(f)=O((\log n)^d)\) imply
\(\operatorname{ams}(g)=O((\log n)^{d+1})\)? The source also asks the weaker
question with both bounds replaced by \(n^{o(1)}\). These are assertions about
families as n grows; any finite truth-table computation is only a control.

The preceding AC⁰ sensitivity estimate is already known through the Switching
Lemma. Its truth does not establish the proposed induction step for arbitrary
input functions. The source's second conjecture about balanced graph properties
is a different question and is not the target here.

## 2. Approach 1: exact boundary accounting

Put \(M_f(x)=\max_j s(f_j,x)\). If \(g=\bigwedge_{j\in S}f_j\) and g(x)=0,
choose any j∈S with fⱼ(x)=0. Every edge changing g from zero to one also changes
that particular fⱼ. Consequently

\[
 1_{\{g(x)=0\}}s(g,x)\le M_f(x). \tag{1}
\]

This includes the case of several zero factors. When g(x)=1, a changing edge
must change at least one factor; the sensitive-coordinate set of g is the union
of the factors' sensitive-coordinate sets. Thus

\[
 s(g,x)\le\sum_{j\in S}s(f_j,x)\le |S|M_f(x). \tag{2}
\]

The empty conjunction is constant one and has sensitivity zero, so it causes
no exception. If every Sᵢ has size at most K, (1)–(2) give the pointwise and
averaged bounds

\[
 \max_i s(g_i,x)\le K M_f(x),\qquad
 \operatorname{ams}(g)\le K\operatorname{ams}(f). \tag{3}
\]

In particular **fan-in O(log n)** proves the desired implication for that
restricted class. The source places no such fan-in restriction.

For a *single* conjunction there is a second useful bound, independent of its
fan-in. Every boundary edge has exactly one zero endpoint and one one endpoint,
so uniform counting gives

\[
 \mathbb E[1_{\{g=0\}}s(g)]
 =\mathbb E[1_{\{g=1\}}s(g)]
 =\tfrac12\mathbb E[s(g)].
\]

Combining with (1),

\[
 \mathbb E[s(g)]\le2\operatorname{ams}(f). \tag{4}
\]

One cannot commute this edge-balance identity with a maximum over many output
functions. Summing (4) over m outputs gives only
\(\operatorname{ams}(g_1,\ldots,g_m)\le2m\operatorname{ams}(f)\), not the desired
logarithmic loss. Duplicating a function in either family leaves its pointwise
maximum unchanged, so repetition alone cannot exploit a hidden arithmetic mean.

### A logarithmic loss can genuinely occur

Use the elementary disjoint-conjunction construction: let k≥1, m=2ᵏ and
n=km. Take fⱼ(x)=xⱼ for all n coordinates. Then M_f(x)=1 everywhere. Partition
the coordinates into m disjoint k-bit blocks and let hᵢ be the AND of block i.
Use h₁,…,hₘ as outputs and repeat h₁ to pad the list to exactly n outputs.
This padding changes neither the maximum nor its expectation.

A block-AND has sensitivity k when all its bits are one, sensitivity one when
exactly one bit is zero, and sensitivity zero otherwise. Independence of the
blocks therefore gives the exact formula

\[
 \operatorname{ams}(h_1,\ldots,h_m)
 = k-(k-1)(1-2^{-k})^m-(1-(k+1)2^{-k})^m. \tag{5}
\]

Indeed the maximum equals k if at least one block is all one. If no block is
all one, it equals one precisely when at least one block has exactly one zero.
These two disjoint events yield (5).

For m=2ᵏ, the all-one-block event has probability
\(1-(1-1/m)^m\ge1-e^{-1}>1/2\). Hence

\[
 k/2\le\operatorname{ams}(h)\le k.
\]

Since \(\log_2 n=k+\log_2 k\in[k,2k]\), this is Θ(log n), while the input ams
is exactly one. This shows that a uniform constant-factor bound would be false.
It is fully consistent with the logarithmic factor in the proposed induction;
it is not a counterexample. The disjoint-AND pattern is standard, and no novelty
is asserted for this calculation.

**Gap after approach 1.** A single-output cut identity is too weak after taking
the maximum. No estimate controlling arbitrarily large, overlapping Sᵢ by a
single logarithmic factor has been established.

## 3. Approach 2: a false one-sided transfer principle

Define the zero-side maximal sensitivity of an output family by

\[
 Z_g(x)=\max_i[1_{\{g_i(x)=0\}}s(g_i,x)].
\]

Equation (1) shows \(Z_g(x)\le M_f(x)\) for every conjunction family. It is
therefore tempting to try the universal inequality

\[
 \mathbb E\max_i s(g_i,x)
 \stackrel{?}{\le}C\log n\;\mathbb E Z_g(x). \tag{6}
\]

If true for every n-function family on n bits, (6) would give the desired
induction immediately. **It is false.** The following standard Hamming-syndrome
construction gives an exact obstruction to (6), while not refuting the source.

### The classical syndrome construction

Fix r≥2 and let n=2ʳ−1. Index the n coordinates by the nonzero vectors
v∈F₂ʳ. For x∈{0,1}ⁿ define

\[
 T(x)=\sum_{v\ne0}x_vv\in\mathbb F_2^r.
\]

This is the parity-check map of the classical binary Hamming code, whose
construction goes back to [Hamming (1950)](https://doi.org/10.1002/j.1538-7305.1950.tb00463.x).
No coding-theoretic theorem is required below: all properties used follow
straight from the displayed linear map.

For each nonzero a∈F₂ʳ set
\(h_a(x)=1_{\{T(x)=a\}}\). There are exactly n functions. Flipping coordinate v
changes T(x) to T(x)+v, and the n nonzero v enumerate each other syndrome
exactly once. Thus

\[
 s(h_a,x)=\begin{cases}n,&T(x)=a,\\1,&T(x)\ne a.\end{cases} \tag{7}
\]

Every x has a zero-valued hₐ, and its zero-side sensitivity is one. Therefore
\(Z_h(x)=1\) at every x. The map T is surjective because its columns contain the
r standard basis vectors. Every fiber has size 2ⁿ⁻ʳ, so its syndrome is uniform.
At syndrome zero the full maximum is one; at any of the n nonzero syndromes it
is n. Consequently

\[
 \mathbb E Z_h=1,\qquad
 \operatorname{ams}(h)=\frac{n^2+1}{n+1}
                      =n-1+\frac2{n+1}. \tag{8}
\]

This contradicts (6) for every fixed C once r is sufficiently large. It also
rules out a universal subpolynomial one-sided transfer bound of that form.

### Why this is not a counterexample to Rossman's implication

The original question demands a conjunction representation whose **input**
family has small full ams. Equation (8) by itself supplies no such input family.
In the natural representation, include both parity literals

\[
 f_{b,\epsilon}(x)=1_{\{T(x)_b=\epsilon\}},
 \quad b\in[r],\quad\epsilon\in\{0,1\}.
\]

For r≥3, 2r≤n, so repeat one literal to obtain exactly n input functions. A
parity literal changes under exactly the 2ʳ⁻¹ coordinates whose column has
b-th bit one, independently of x. Thus

\[
 \operatorname{ams}(f)=2^{r-1}=(n+1)/2. \tag{9}
\]

Every hₐ is indeed the conjunction of its r matching parity literals. But (9)
is linear, not polylogarithmic or subpolynomial, and the output in (8) is at most
twice (9). This realization therefore does not satisfy the source hypothesis.
No claim is made that every possible alternative representation has linear input
ams; excluding or finding a better representation would itself require work.

**Gap after approach 2.** A proof cannot retain only the one-sided statistic Z_g.
It must exploit more information about the common factors fⱼ and their
conjunction incidence sets. The classical syndrome controls defeat the proposed
shortcut, not the original factorization-sensitive assertion.

## 4. Relation to established sensitivity results

[Rossman's later formula theorem](https://arxiv.org/abs/1508.07677v1) bounds
ordinary average sensitivity of bounded-depth formulas and explicitly uses a
random-restriction process based on the Switching Lemma. Its circuit/formula
hypotheses and its statistic differ from an arbitrary input family specified
only by ams. Applying that theorem requires an additional structural hypothesis
not supplied by the current question.

[Huang's sensitivity theorem](https://arxiv.org/abs/1907.00847v2) settles the
worst-case sensitivity/degree problem. A small expectation of the pointwise
family maximum does not give the worst-case bound needed to substitute that
result here. This package obtains no such substitution and does not confuse the
already-solved classical Sensitivity Conjecture with Rossman's different
conjunction question.

The limited source and current-literature audit is in [SOURCES.md](SOURCES.md).
Neither an exact resolution nor historical novelty for these elementary
observations has been established.

## 5. Checks and disposition

The standard-library [verifier](verify_controls.py) checks all pairs of Boolean
functions on the two-dimensional cube against (1)–(4), exact small disjoint-block
truth tables against (5), the Hamming syndrome arithmetic against (7)–(9), and
actual cube truth tables for r=2,3. These are bounded controls. The parameterized
proofs above, not finite tests, justify the stated infinite control families.
Run `python3 verify_controls.py` and compare with [verification.json](verification.json).

**Full-target status: unsolved.** Two substantive approaches used. The exact
missing result is a universal factorization-sensitive estimate strong enough
for the polylogarithmic or subpolynomial implication, or a family of explicit
conjunctions violating that implication while meeting its input ams hypothesis.
Neither has been produced. Stop at that gap rather than treating (8) as a
manufactured counterexample.
