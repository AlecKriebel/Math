# Stability and clustering relaxations: an exact LP diagnostic and a robust certificate

**Original target unresolved; two scoped approaches; independent review pending.** Record2800904 / Bandeira Open Problem9.4. No general stability threshold or k-means SDP characterization is claimed.

## 1. Exact source and distinct stability notions

The complete [Bandeira lecture notes](https://people.math.ethz.ch/~abandeira/TenLecturesFortyTwoProblems.pdf), pp.128–129, give the facility-assignment k-median LP and the Peng–Wei-style k-means SDP. Problem9.4 asks for integrality conditions based on stability-like structure. Its immediate motivation is a large improvement from k−1 to k clusters followed by little improvement from k to k+1. It does **not** specify a numerical perturbation-resilience parameter, ratio threshold, or random model for this question. The preceding stochastic-ball discussion and the separate random-unplanted Problem9.3 must not be substituted for it.

[Chekuri–Gupta(2018)](https://arxiv.org/abs/1806.04202) proves LP integrality for perturbation-resilient k-center variants; its Question3 explicitly distinguishes the corresponding k-median/k-means LP question. [Makarychev–Makarychev(2016)](https://arxiv.org/abs/1607.06442) gives an exact clustering algorithm under metric perturbation resilience; that does not by itself prove this particular LP or SDP integral. These are distinctions among theorem statements, not an exhaustive current-openness certificate.

We study the finite-metric k-median LP
\[
\min\sum_{i,j}d_{ij}x_{ij},\quad
\sum_i x_{ij}=1,\quad0\le x_{ij}\le y_i\le1,\quad\sum_i y_i=k.
\tag{1}
\]
Facilities and clients are the same finite set. Integral solutions choose k centers and assign each point to one. The counterexample below is a finite metric, not asserted to be a Euclidean point configuration, and says nothing about the k-means SDP.

## 2. A unique, weakly perturbation-resilient metric optimum need not make this LP tight

Take k=2 on vertices0,…,7 with symmetric distance matrix
\[
D=\begin{pmatrix}
0&1050&1998&1954&1006&1934&1966&1063\\
1050&0&1052&1939&1962&1046&1975&1928\\
1998&1052&0&1065&1918&1937&1018&1997\\
1954&1939&1065&0&1013&1980&1933&1069\\
1006&1962&1918&1013&0&1091&1978&1919\\
1934&1046&1937&1980&1091&0&1040&1913\\
1966&1975&1018&1933&1978&1040&0&1094\\
1063&1928&1997&1069&1919&1913&1094&0
\end{pmatrix}.
\]
All off-diagonal distances lie in[1006,1998], and1998<2·1006. Thus every triangle inequality holds, including those with repeated vertices.

Enumerating all28 pairs of centers and their256 assignments gives a unique optimum of7099, at centers{2,4}. The assignment, indexed by client0,…,7, is
\[
(4,2,2,4,4,4,2,4).
\]
The next cheapest distinct center/assignment solution costs7110. The supplied exhaustive integer verifier is a finite proof certificate for these claims.

For any entrywise perturbation with
\[
d_{ij}\le d'_{ij}\le\frac{1001}{1000}d_{ij},
\tag{2}
\]
the displayed solution costs at most7099·1001/1000=7106.099, while every other integral solution costs at least7110. It therefore stays uniquely optimal. This proves 1.001-perturbation resilience even without requiring the perturbed costs to remain a metric, and hence also with that requirement. Equivalent uniformly rescaled shrinking conventions give the same conclusion. The argument includes alternative assignments for the same centers, not merely alternative center sets.

Nevertheless(1) has a strictly cheaper fractional feasible point. Let E be the edges of the eight-cycle together with its four opposite chords:
\[
E=\{\{i,i+1\bmod8\}:0\le i<8\}\cup\{\{i,i+4\}:0\le i<4\}.
\]
Set y_i=1/4 for every i and x_{ij}=1/4 when i=j or{i,j}∈E, zero otherwise. Each vertex has three graph neighbors, so each client receives total assignment one; every assignment respects its facility variable, and Σy_i=2. Its cost is
\[
\frac12\sum_{\{i,j\}\in E}d_{ij}=\frac{12607}{2}=6303.5<7099.
\]
Thus the LP is not tight on this explicitly weakly resilient instance. We do not claim6303.5 is the fractional optimum; a feasible upper bound already proves nonintegrality.

For context, exact integer optima at k=1,2,3 are10887,7099,5171. These numbers do not establish a large-gap/plateau counterexample of the kind motivating the original source. This example only rules out “unique optimum” or “some multiplicative resilience greater than one” as sufficient by themselves. It does not rule out a stronger universal resilience threshold or useful objective-gap conditions. This elementary construction has no novelty claim.

## 3. A checkable strict-margin certificate for k-median

This is a standard LP-duality mechanism, proved here to specify its exact content. It is not a new stability characterization.

Choose k distinct candidate centers S and a partition into nonempty clusters C_c, c∈S, with each center assigned to itself. Let c(j) denote client j's center. Choose t>0 and define
\[
\alpha_j=d_{c(j),j}+\frac{t}{|C_{c(j)}|},\qquad
\beta_{ij}=(\alpha_j-d_{ij})_+.
\]
Suppose
\[
\alpha_j<d_{c,j}\quad(c\in S\setminus\{c(j)\}),
\tag{3}
\]
and
\[
\sum_j\beta_{ij}<t\quad(i\notin S).
\tag{4}
\]
Then the specified integral point is the **unique** optimum of(1).

**Proof.** For each selected center c, condition(3) removes all off-cluster contributions, while its own-cluster contributions sum to t. Hence Σ_jβ_{cj}=t for c∈S, and Σ_jβ_{ij}≤t for every facility. The inequalities α_j−β_{ij}≤d_{ij} hold by definition. For any feasible point,
\[
\sum_{i,j}d_{ij}x_{ij}
\ge\sum_j\alpha_j-\sum_{i,j}\beta_{ij}x_{ij}
\ge\sum_j\alpha_j-\sum_i y_i\sum_j\beta_{ij}
\ge\sum_j\alpha_j-kt.
\]
The last expression equals the proposed integral cost because Σ_j(α_j−d_{c(j),j})=kt. Thus it is optimal. Equality and strict(4) force y_i=0 outside S. There are k selected facilities, each y_i≤1, and their sum is k, so each has y_i=1. For a wrong selected center c, condition(3) makes its first inequality strict whenever x_{cj}>0. Consequently every client is assigned only to c(j), proving uniqueness. □

### Quantified robustness of this certificate

Let γ be the minimum of d_{c,j}−α_j over the inequalities(3), and η the minimum of t−Σ_jβ_{ij} over i∉S. If one of the corresponding index sets is empty, omit its restriction. Otherwise γ,η>0. If the cost matrix changes to d' with |d'_{ij}−d_{ij}|≤ε, rebuild α'_j=d'_{c(j),j}+t/|C_{c(j)}|. Each difference α'_j−d'_{ij} changes by at most2ε. The positive-part map is1-Lipschitz. Hence conditions(3)–(4) remain strict whenever
\[
2\varepsilon<\gamma,\qquad2n\varepsilon<\eta.
\tag{5}
\]
The same clustering is then the unique LP optimum. The proof requires no random sampling or metric property. It certifies a neighborhood of tightness from explicit dual margins.

This condition is stronger information than merely asserting perturbation stability of the integral optimum. It requires verifying every off-center inequality(4); it does not derive those inequalities from the source's k−1/k/k+1 objective gaps. The preceding counterexample shows why a general weak-stability shortcut would fail.

## 4. Remaining gap and controls

Approach1 is the exact resilient-but-fractional metric example. Approach2 is the strict dual-margin sufficient condition and its perturbation bound. The verifier checks every integer solution in the finite example, the fractional constraints/cost, all triangle inequalities, and exact margins on a separate separated-cluster positive control. Those tests support the two deductions but do not constitute a general stability characterization.

Original status: **unsolved,2/5**. Missing is a justified implication from a specified meaningful source-style stability condition to LP or SDP integrality, or a counterexample to such a precise proposed implication. No k-means SDP result, optimal threshold, random-model theorem, novelty or human peer review is claimed. Actual model metadata: inherited runtime; exact model identifier not exposed; no model/reasoning switch made.
