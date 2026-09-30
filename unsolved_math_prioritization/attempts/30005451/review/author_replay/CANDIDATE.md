# Affine Bernoulli attachment and Poisson-outdegree attachment have the same local limit

**Problem 30005451 / OWR-12697708-004.** Candidate affine comparison theorem, independently unreviewed. One substantive approach. Priority is unestablished; no novelty or human-peer-review claim is made.

## 1. Source correction and precise models

The actual question in Maria Deijfen and Remco van der Hofstad's contribution on preferential attachment in [OWR, pp. 649–650] concerns the relation between the Bernoulli model and an **adapted random-outdegree model**. The proposed adaptation uses indegree weights and an **i.i.d. Poisson number of outgoing edges**. The dataset's statement instead compares fixed outdegree with Poisson outdegree. Those are different questions. The theorem below concerns the source's proposed affine Poisson comparison, with both standard no-self-loop updating conventions specified explicitly.

Fix

$$
 0\le a<1,\qquad 0<b\le1,\qquad
 f(k)=ak+b,\qquad \lambda=\frac b{1-a}. \tag{1}
$$

All edges point from a new vertex to an older vertex. Distance and radius-$r$ balls are taken in the underlying undirected graph, retaining edge multiplicities when present. A root is sampled uniformly from the $n$ vertices, independently of the graph. The initial graph in each basic model is vertex 1 with no edges.

- **Bernoulli model $B_n$.** Given $B_n$, add vertex $n+1$ and, independently for every $v\le n$, add one edge $(n+1)\to v$ with probability
  $$p_v=\frac{a d^{\mathrm{in}}_{B_n}(v)+b}{n}.$$
  This is the exact Bernoulli rule of [OWR] and [DM]. It is well defined: $d^{\mathrm{in}}(v)\le n-1$, and $a(n-1)+b\le n$. The bound on $b$ is the initial-step admissibility condition supplied by [DM], which the abbreviated report leaves implicit.
- **Frozen-weight Poisson model $P_n^{\mathrm F}$.** Independently at each arrival, sample $M_{n+1}\sim\operatorname{Poisson}(\lambda)$. Given the old graph, each of these $M_{n+1}$ edges independently selects $v\le n$ with probability $f(d^{\mathrm{in}}(v))/S_n$, where $S_n=\sum_{u\le n}f(d^{\mathrm{in}}(u))$. Weights stay fixed while this row is attached.
- **Sequential Poisson model $P_n^{\mathrm S}$.** Use the same i.i.d. Poisson outdegree law, but update the old target's indegree after each edge. If its initial weight is $w_v$, and it has received $h_v$ of the first $j$ edges in the new row, its next selection probability is $(w_v+a h_v)/(S_n+aj)$.

Parallel edges are allowed in both Poisson models. The new vertex is ineligible as a target during its own row, so there are no new self-loops. Zero outgoing edges are allowed. These definitions are the indegree-based adaptations of the independent and sequential conventions called (E) and (D) in [GHHR]; they are not applications of that paper's total-degree theorem. The proof also allows either Poisson model to start from any fixed finite directed multigraph instead; see Section 5.

## 2. The comparison theorem

**Theorem.** For each choice in (1) and either $P^{\mathrm F}$ or $P^{\mathrm S}$, there is a coupling with $B$ on the same vertex labels such that, writing $D_n$ for the sum of absolute differences of directed edge multiplicities,

$$
 \mathbb E D_n=o(n). \tag{2}
$$

For every fixed nonnegative integer $r$, let $Z_{n,r}$ be the number of labels whose induced rooted radius-$r$ balls differ in the coupled graphs. The comparison retains orientations, multiplicities and any identical deterministic vertex marks, such as $v/n$. Then

$$
 \mathbb E Z_{n,r}=o(n). \tag{3}
$$

Consequently the total variation distance between their empirical radius-$r$ rooted-ball distributions tends to zero in $L^1$. After forgetting orientations and marks, both Poisson models converge locally in probability, in the sense defined in [OWR, p. 648], to the Bernoulli model's idealized neighborhood tree of [DM]. Its explicit affine description is given in Section 8.

The theorem covers every source-admissible affine rule (1), including $a=0$. It does not claim a comparison for arbitrary nonlinear concave rules, a model forbidding parallel edges, or a deterministic-outdegree model. It asserts no uniformity as $a\uparrow1$.

## 3. Moment estimates for the Bernoulli graph

Let $T_n$ be the number of edges of $B_n$, and put

$$
 w_v(n)=a d^{\mathrm{in}}_{B_n}(v)+b,\quad
 S_n=\sum_{v\le n}w_v(n)=aT_n+bn,\quad
 F_n=\sum_{v\le n}w_v(n)^2.
$$

Constants below depend only on the fixed parameters. If $L_{n+1}=T_{n+1}-T_n$, then, conditionally on $B_n$, this is a sum of independent Bernoulli variables, so

$$
 \mathbb E[L_{n+1}\mid B_n]=S_n/n,
 \qquad \operatorname{Var}(L_{n+1}\mid B_n)\le S_n/n. \tag{4}
$$

In particular $\mathbb ET_{n+1}=(1+a/n)\mathbb ET_n+b$. Induction from $T_1=0$ and $(1-a)\lambda=b$ gives

$$
 \mathbb ET_n\le\lambda n,
 \qquad \mathbb ES_n\le\lambda n. \tag{5}
$$

Each old weight increases by $a$ with probability $w_v/n$, and the new weight is $b$. Therefore

$$
 \mathbb EF_{n+1}
 =(1+2a/n)\mathbb EF_n+(a^2/n)\mathbb ES_n+b^2.
$$

Iterating this scalar recursion using (5) yields

$$
 \mathbb EF_n=
 \begin{cases}
 O(n),&2a<1,\\
 O(n\log(n+1)),&2a=1,\\
 O(n^{2a}),&2a>1.
 \end{cases}
 \qquad\text{In particular }\mathbb EF_n/n^2\longrightarrow0. \tag{6}
$$

For example these bounds follow by multiplying through by the reciprocal of $\prod_{j=1}^{n-1}(1+2a/j)$, which is bounded above and below by positive constants times $n^{2a}$ when $a>0$; the case $a=0$ is immediate. This product estimate follows directly by summing $\log(1+2a/j)=2a/j+O(j^{-2})$.

We also need a degree moment strictly above one. First, (4) implies

$$
 \mathbb ET_{n+1}^2
 \le (1+a/n)^2\mathbb ET_n^2
  +[2b(1+a/n)+a/n]\mathbb ET_n+b^2+b.
$$

By (5) the additive term is $O(n)$. Induction, comparing $(n+1)^2$ with $(n+a)^2$ and using $a<1$, proves $\mathbb ET_n^2=O(n^2)$. Thus $\mathbb E(S_n/n)^2=O(1)$ and, by (4),

$$
 \sup_n\mathbb E L_{n+1}^2<\infty. \tag{7}
$$

Assume first $a>0$, and choose $q\in(1,2]$ with $aq<1$. Since $w\ge b>0$, Taylor's theorem gives, uniformly for $w\ge b$,

$$
 (w+a)^q-w^q\le qa w^{q-1}+C.
$$

Writing $U_n=\sum_{v\le n}w_v(n)^q$, the same one-step calculation gives

$$
 \mathbb EU_{n+1}\le(1+aq/n)\mathbb EU_n+(C/n)\mathbb ES_n+b^q.
$$

Equations (5) and $aq<1$ imply $\mathbb EU_n=O(n)$. Because $d^{\mathrm{in}}\le w/a$, the averaged $q$th indegree moment is bounded. Each vertex's outdegree is its single birth-row count, so (7) bounds the averaged $q$th outdegree moment as well.

When $a=0$, use $q=2$. Here $\mathbb ET_n=b(n-1)$ and

$$
 \mathbb E\sum_v d^{\mathrm{in}}_{B_{n+1}}(v)^2
 =\mathbb E\sum_v d^{\mathrm{in}}_{B_n}(v)^2
   +(2b/n)\mathbb ET_n+b,
$$

which is $O(n)$. The outdegree bound (7) still applies. In all cases, for the total undirected degree $\deg_{B_n}$, there are $q>1$ and $C<\infty$ such that

$$
 \frac1n\mathbb E\sum_{v\le n}\deg_{B_n}(v)^q\le C
 \quad\text{for every }n. \tag{8}
$$

## 4. Row coupling and sublinear discrepancy

We first record an elementary count coupling. For $0\le p\le1$, a Bernoulli($p$) variable and a Poisson($p$) variable can be coupled with expected absolute difference

$$
 2(p-1+e^{-p})\le p^2. \tag{9}
$$

Indeed, draw $N\sim\operatorname{Poisson}(p)$, put $X=1$ whenever $N\ge1$, and on $N=0$ set $X=1$ with probability $(p-1+e^{-p})/e^{-p}$. This lies in $[0,1]$ and gives the asserted Bernoulli marginal and cost. The inequality follows from $e^{-p}\le1-p+p^2/2$. Poisson variables of means $p$ and $z$ can be coupled by adding an independent Poisson variable of mean $|p-z|$, with expected discrepancy $|p-z|$. Combining these couplings gives

$$
 \mathbb E|\operatorname{Bernoulli}(p)-\operatorname{Poisson}(z)|
 \le p^2+|p-z|. \tag{10}
$$

Suppose the old coupled graphs have $n$ vertices. In the Poisson graph write $w'_v=a d^{\mathrm{in}}_P(v)+b$ and $S'_n=\sum_vw'_v$. The frozen-weight row is exactly a vector of independent Poisson variables with means

$$z_v=\lambda w'_v/S'_n,$$

by Poisson splitting. Its total is Poisson($\lambda$), independently of the past, and conditional on the total its targets are independent with probabilities $w'_v/S'_n$. Apply (10) independently across targets to preserve both row marginals. Since
$\sum_v|d^{\mathrm{in}}_B(v)-d^{\mathrm{in}}_P(v)|\le D_n$,

$$
 \sum_{v\le n}|p_v-z_v|
 \le \frac{aD_n}{n}+\left|\frac{S'_n}{n}-\lambda\right|. \tag{11}
$$

The Poisson graph has $T'_n=\sum_{i=2}^nM_i$ edges, a Poisson variable of mean $\lambda(n-1)$. Hence

$$
 S'_n=aT'_n+bn,\qquad
 \mathbb E\left|S'_n/n-\lambda\right|=O(n^{-1/2}). \tag{12}
$$

This is the important affine normalization step: the error is controlled by the **Poisson graph's own edge count**, rather than by an unproved concentration assertion about a general weight sum.

Old edges never change, so new row discrepancies add to $D_n$. For the frozen-weight model, (6), (10)–(12) give

$$
 d_{n+1}\le(1+a/n)d_n+r_n,\qquad
 d_n:=\mathbb ED_n,\qquad
 r_n:=\mathbb EF_n/n^2+O(n^{-1/2})\longrightarrow0. \tag{13}
$$

Since $a<1$, (13) implies $d_n=o(n)$. To see this without a rate assumption, fix $\varepsilon>0$ and choose $N$ with $r_n\le\varepsilon$ for $n\ge N$. Comparison with the recursion having constant forcing $\varepsilon$ gives
$d_n\le C_N n^a+\varepsilon n/(1-a)$; divide by $n$, let $n\to\infty$, and then let $\varepsilon\downarrow0$.

### Sequential updating

Given a past Poisson graph and a birth count $M=m$, compare independent frozen targets with sequentially updated targets. After $j$ sequential choices, its next distribution is

$$
 \frac{w'_v+a h_v}{S'_n+aj}
 =\frac{S'_n}{S'_n+aj}\frac{w'_v}{S'_n}
   +\frac{aj}{S'_n+aj}\frac{h_v}{j},
$$

with the second summand omitted when $j=0$. Its total variation distance from the frozen target law is at most $aj/(S'_n+aj)\le aj/(bn)$. Couple the next frozen draw to this law while preserving its fixed conditional distribution given the entire previous history. Thus the frozen draws are still independent. Each disagreeing target changes the row multiplicity vector by at most 2 in $\ell^1$. Summing over $j=0,\ldots,m-1$ and averaging gives expected row discrepancy at most

$$
 \frac{a\mathbb E[M(M-1)]}{bn}
 =\frac{a\lambda^2}{bn}. \tag{14}
$$

Glue this coupling to the Bernoulli/frozen-row coupling (conditional on the intermediate row, using a uniformly random ordering of its Poisson targets). The triangle inequality for the expected $\ell^1$ cost adds only (14) to $r_n$. The sequential model also has exactly the i.i.d. Poisson birth counts, so (12) is unchanged. Equation (2) follows for both conventions.

## 5. From edge discrepancy to local comparison

Let $H_n$ be the union multigraph of the two coupled graphs, and let $W_{n,0}$ be the set of endpoints of discrepant edges. Then $|W_{n,0}|\le2D_n$. Define $W_{n,r+1}$ by adjoining all $H_n$-neighbors of $W_{n,r}$. At each vertex,

$$
 \deg_{H_n}(v)\le2\deg_{B_n}(v)+\Delta_v,
 \qquad \sum_v\Delta_v\le2D_n,
$$

where $\Delta_v=|\deg_{P_n}(v)-\deg_{B_n}(v)|$ suffices. For any random vertex set $W$, Hölder's inequality on the product of the probability space and counting measure, followed by (8), gives

$$
 \frac1n\mathbb E\sum_{v\in W}\deg_{B_n}(v)
 \le C^{1/q}\left(\frac{\mathbb E|W|}{n}\right)^{1-1/q}. \tag{15}
$$

Writing $x_{n,r}=\mathbb E|W_{n,r}|/n$, we obtain

$$
 x_{n,r+1}\le x_{n,r}+2C^{1/q}x_{n,r}^{1-1/q}+2d_n/n.
$$

Equation (2) and induction on fixed $r$ give $x_{n,r}\to0$. A root outside $W_{n,r}$ has identical induced radius-$r$ balls in the two graphs, via the identity on labels: no edge with an endpoint in its union-graph radius-$r$ ball is discrepant. This proves (3), including boundary edges, directions, multiplicities and identical marks.

Pairing the same uniformly chosen root proves the total variation bound for rooted-ball laws. Pairing the same labels in the two empirical measures bounds their total variation distance by $Z_{n,r}/n$, proving the stronger empirical assertion.

A different fixed finite initial graph for either Poisson model only changes $D_{n_0}$ by a finite amount and changes $T'_n$ from $\operatorname{Poisson}(\lambda(n-1))$ to a fixed constant plus $\operatorname{Poisson}(\lambda(n-n_0))$. Equation (12) remains valid, with an additional $O(1/n)$ term. The proof from time $n_0$ onward is identical. This justifies the seed qualification without presuming seed universality.

## 6. Concentration of Bernoulli local statistics

For completeness, the following argument upgrades the credited annealed Bernoulli local limit to the local-in-probability formulation used in [OWR]. It avoids assuming that a one-root limit automatically gives concentration.

In $B_n$, the entire column of incoming indicators at vertex $v$ depends only on its own independent uniforms: its transition probability depends on its own indegree and deterministic time. Different incoming columns are therefore independent. Fix a bounded radius-$r$ rooted-graph function $h$.

Construct a pruned graph $J_{n,K}$ in two steps. First, erase an entire incoming column if it contains more than $K$ edges, obtaining $H_{n,K}$. Second, erase all edges incident to any vertex whose degree in $H_{n,K}$ exceeds $K$. The resulting graph has maximum degree at most $K$.

Every edge removed at either step is incident to a vertex whose original degree in $B_n$ exceeds $K$. Hence the expected number of removed edges is at most

$$
 2\mathbb E\sum_v\deg_{B_n}(v)\mathbf1_{\{\deg_{B_n}(v)>K\}}
 \le 2CnK^{1-q}. \tag{16}
$$

The same neighborhood-expansion estimate (15), now using that $J_{n,K}\subset B_n$, shows that the expected fraction of roots with different radius-$r$ balls in $B_n$ and $J_{n,K}$ is at most $\varepsilon_{K,r}$, where $\varepsilon_{K,r}\to0$ as $K\to\infty$, uniformly in $n$. Explicitly, start with at most twice the normalized bound (16) for the endpoints, and iterate the continuous function $x\mapsto x+C^{1/q}x^{1-1/q}$ a fixed number of times.

Resampling one original incoming column changes $H_{n,K}$ by at most $2K$ edges. Only endpoints of those edges can change their degree-threshold status in the second pruning. If a vertex crosses the threshold $K$, its degree in either intermediate graph is at most $3K$. Therefore at most $C_K$ edges differ between the two final pruned graphs, for a deterministic constant $C_K$ depending only on $K$. Their union has maximum degree at most $2K$, so at most $C_{K,r}$ roots have different radius-$r$ balls.

It follows that the empirical mean of $h$ on $J_{n,K}$ changes by at most $2\|h\|_\infty C_{K,r}/n$ upon resampling one independent column. Reveal the independent columns one at a time. The resulting conditional-expectation martingale has increments bounded by the same constant times $1/n$, since replacing one coordinate changes the function by that amount. Orthogonality of its increments gives variance $O_{K,r,h}(1/n)$. The $L^1$ difference between the empirical means on $B_n$ and $J_{n,K}$ is at most $2\|h\|_\infty\varepsilon_{K,r}$. Taking first $n\to\infty$ and then $K\to\infty$ proves concentration of the original empirical mean around its expectation, in $L^1$.

Thus the annealed rooted local limit of $B_n$ supplied by [DM] is also its local-in-probability limit. Section 5 transfers it to both Poisson models.

## 7. Credited Bernoulli limit

[DM, Section 1.3, especially pp. 7–9 of the arXiv full text] constructs the idealized neighborhood tree and explicitly identifies it as the weak local limit. Sections 5–6 couple neighborhood explorations, retaining the tree structure, although the displayed propositions summarize the consequence for truncated component sizes. We use this known Bernoulli limit, not the distinct total-degree Pólya-point-tree theorem of [GHHR].

The underlying pure-birth process $Z_t$, started at zero, has rate $f(Z_t)$. A particle at logarithmic age-position $x<0$ has older children at relative positions $s<0$ forming a Poisson process with intensity $e^s\mathbb E f(Z_{-s})\,ds$. Younger children arise from its birth process to the right. If its parent is younger, this birth process is Palm-conditioned to have the prescribed parent birth and that point is removed. Particles beyond position zero are killed. The root starts at $-E$ with $E\sim\operatorname{Exp}(1)$. These are the source's idealized-neighborhood conventions.

## 8. Explicit common affine tree

For $a>0$, the common unmarked limit can be generated with auxiliary ages and strengths as follows. The root has age $U\sim\operatorname{Uniform}(0,1)$. A vertex of age $u$ draws a strength

$$
 \Gamma\sim\begin{cases}
 \operatorname{Gamma}(b/a,1),&\text{root, or its parent is older},\\
 \operatorname{Gamma}(b/a+1,1),&\text{its parent is younger},
 \end{cases} \tag{17}
$$

where the second parameter is the rate. Independently of $\Gamma$, its additional older children form a Poisson process on $(0,u)$ with intensity

$$ b u^{a-1}v^{-a}\,dv. \tag{18}$$

Conditionally on $\Gamma$, its additional younger children form a Poisson process on $(u,1)$ with intensity

$$ a\Gamma u^{-a}v^{a-1}\,dv. \tag{19}$$

The parent itself is omitted from these offspring lists. Offspring mechanisms at distinct vertices are conditionally independent given their ages and parent-relative types. All edges are oriented from younger to older. The integral in (18) is $b/(1-a)=\lambda$; the integral in (19) is $\Gamma(u^{-a}-1)$, finite almost surely. Thus every finite generation is finite almost surely.

Here is the verification from [DM]'s construction. The affine pure-birth process is a Cox process with random intensity $a\Gamma e^{at}\,dt$ and $\Gamma\sim\operatorname{Gamma}(b/a,1)$. Conditional on $Z_t=k$, Gamma–Poisson conjugacy gives posterior shape $b/a+k$ and rate $e^{at}$, so its next-event intensity is exactly $ak+b$. Also $\mathbb E f(Z_t)=be^{at}$. The transformation $v=ue^s$ gives (18), and $v=ue^t$ gives (19). Palm-conditioning a Cox process on a point at a prescribed time size-biases $\Gamma$ once, replacing its shape by $b/a+1$; after removing that point, the remaining process has the same conditional Poisson law. This gives precisely (17), with no conditioning on an ordinary positive-probability point event. Finally $e^{-E}$ is uniform.

For $a=0$, use no Gamma variable. Both offspring lists are independent Poisson processes, with older intensity $(b/u)\,dv$ on $(0,u)$ and younger intensity $(b/v)\,dv$ on $(u,1)$. The homogeneous rate-$b$ birth process has the same Palm remainder as itself, so the parent-relative type no longer changes its law. This also agrees with the limit of the affine formulas as $a\downarrow0$.

This explicit construction clarifies the relation requested in the report. It also gives a simple unmarked diagnostic for the dataset's fixed-outdegree substitution. Given root age $u$, its probability of having no older children is $e^{-\lambda}$, and its probability of having no younger children is $u^b$: for $a>0$, use the Gamma Laplace transform at $u^{-a}-1$, and for $a=0$ use the Poisson mean $b\log(1/u)$. These mechanisms are independent. Therefore

$$\mathbb P(\deg(\text{root})=0)=\frac{e^{-\lambda}}{1+b}>0. \tag{20}$$

A model with a fixed positive outdegree $m$ has total degree at least $m$ at every non-seed vertex. Its uniformly rooted local limit cannot have an isolated root. Thus even the unmarked limits cannot satisfy the dataset's fixed-outdegree equality. This diagnostic does not replace the corrected Poisson comparison proved above.

## 9. Scope, provenance and remaining distinctions

The affine comparison is proved for the exact Bernoulli rule and the two expressly defined indegree-based Poisson adaptations. It uses a uniform root and undirected graph distance, as in the original local-convergence definition; the finite-graph coupling additionally preserves directed/marked balls. General nonlinear concave attachment, arbitrary interpretations of “appropriately adapt,” and a no-parallel-edge convention are not asserted. If the original open-ended question is read as requesting all nonlinear rules as well, that larger request remains unresolved here.

The source's Poisson mean is identified by (1), not assumed to be the fixed outdegree of an unrelated model. Finite checks support the algebra and local edit bounds, but the limit and coupling assertions require the written infinite-graph-sequence proof. The Bernoulli idealized neighborhood limit is credited to Dereich–Mörters; the explicit affine description is its Gamma–Poisson reformulation. No claim that this comparison has not appeared elsewhere is made.

### References

- **[OWR]** *MATRIX–MFO Tandem Workshop: Stochastic Reinforcement Processes and Graphs*, Oberwolfach Report 12/2023, pp. 639–679. Preferential-attachment contribution and local convergence on pp. 646–651; question (b), pp. 649–650. [Full report](https://ems.press/content/serial-article-files/47008), [DOI](https://doi.org/10.4171/OWR/2023/12).
- **[DM]** S. Dereich and P. Mörters, *Random networks with sublinear preferential attachment: the giant component*, Ann. Probab. **41** (2013), 329–384. [Full primary paper](https://arxiv.org/pdf/1007.0899), [DOI](https://doi.org/10.1214/11-AOP697). The earlier degree-evolution paper is [arXiv:0807.4904](https://arxiv.org/abs/0807.4904), EJP **14** (2009), 1222–1267.
- **[GHHR]** A. Garavaglia, R. S. Hazra, R. van der Hofstad and R. Ray, *Universality of the local limit of preferential attachment models*, [arXiv:2212.05551v4](https://arxiv.org/abs/2212.05551v4), revised 2 March 2026. Models (D) and (E), pp. 4–5; Bernoulli extension discussion, p. 13. Its theorems use total-degree weights; their conclusions are not assumed for the adaptations proved here.
