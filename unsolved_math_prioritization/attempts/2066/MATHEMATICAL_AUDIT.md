# Audit of the deletion classification for Erdős Problem 348

## Publication edition and historical evidence

This AI-assisted, unrefereed publication edition preserves the complete substantive
mathematical audit and credits the existing Geneson theorem. No mathematical
correction is required. Acceptance is bounded to eventual completeness and deletion
of indexed occurrences. No novelty, human review, journal acceptance or formal
proof-assistant verification is claimed.

Source retrievals, visual inspections and finite diagnostics described below are
historical records of the accepted audit on 10 October 2026. Edition preparation
performed no new scholarly-source retrieval or inspection and no new mathematical
test execution. This is a prose-only edition: diagnostic programs and raw results
are omitted. The general theorem rests on the complete written argument, not on
finite samples. Public source identities and recorded inspection limits are in
`PUBLIC_SOURCES.json`; public status history and retrieval metadata are in
`FORMAL_HISTORY.json` and `RETRIEVAL_HISTORY.json`.

## Verdict and scope

**Bounded acceptance of the prior theorem.** Theorem 1 of Jesse Geneson, *Deletion thresholds and exponential examples for complete sequences*, arXiv:2609.25107v1, gives the exact classification for the stated problem: for integers $0\leq m<n$, such a nondecreasing integer sequence exists precisely when $m\leq1$. The argument in Sections 2–4, including the entire central-interval proof ending on PDF page 11, withstands this audit. No mathematical correction is required by the checks below.

This document reconstructs and checks an existing result. It is not a new-solution claim, a journal-refereeing claim, a claim of human review, or a formal proof certificate. The acceptance applies to the specified version and definitions. Results about Problems 349 and 354 in later sections are outside this verdict.

Primary source: [Geneson, version 1](https://arxiv.org/pdf/2609.25107v1), submitted 20 September 2026. The inspected PDF has 14 pages, 423,382 bytes, and SHA-256 `9060ebcc3812b9a33bf08cc8dbdf6b5c8714acda2f54ed4ecfca7c152cb8dcc2`. A fresh version-pinned download matched the supplied copy exactly. The current arXiv record establishes a preprint, not journal publication.

## Exact question and quantifiers

Let $A=(a_i)_{i\geq1}$ be a nondecreasing sequence of integers. Write

$$
\operatorname{FS}(A)=\left\{\sum_{i\in I}a_i:I\subset\mathbb N_{>0}\text{ is finite}\right\}.
$$

Thus each index may be selected once; equal values at different indices remain separately available. The empty selection gives zero. Completeness means that some integer $T$ satisfies $[T,\infty)\cap\mathbb Z\subset\operatorname{FS}(A)$.

For a finite set $D$ of indices, $A\setminus D$ means deletion of those occurrences, followed, if desired, by order-preserving reindexing. The question asks for

$$
\begin{aligned}
C(m)&:\quad \forall D\ (|D|=m\Longrightarrow A\setminus D\text{ is complete}),\\
N(n)&:\quad \forall E\ (|E|=n\Longrightarrow A\setminus E\text{ is incomplete}).
\end{aligned}
$$

The threshold in $C(m)$ is allowed to depend on $D$: the order is “for every deletion, there exists a threshold.” Incompleteness means missing integers occur arbitrarily far out. It is not enough to exhibit one small missing integer. Both deletion clauses are universal. The contradiction to $N(n)$ requires only one successful deletion of size $n$.

The original conventions are explicit in [Erdős–Graham (1980)](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf), printed pages 54 and 57 (PDF pages 50 and 53). The earlier [Graham (1971)](https://mathweb.ucsd.edu/~ronspubs/71_08_integer_sums.pdf), printed page 24 and Question 3 on page 34 (PDF pages 3 and 13), independently fixes finite indexed sums, eventual completeness, and deletion of entries. Both questions give the Fibonacci sequence with two initial ones. These scanned pages were visually inspected. The modern target explicitly requires nondecreasing integer sequences.

The stronger convention of representing every positive integer is a different statement. A result only under that convention does not settle this question. Also, “strongly complete” in these sources refers to surviving all finite deletions, not to representing every positive integer without exceptions.

## The two existence constructions

### Zero deletion tolerance

Take $a_i=2^{i-1}$. Binary expansion represents every nonnegative integer. If the occurrence $2^j$ is deleted, smaller terms have combined sum $2^j-1$, while every larger term is divisible by $2^{j+1}$. Consequently the residue class $2^j\pmod {2^{j+1}}$ is absent. This is an infinite family of missing integers. Any nonempty deletion contains a one-term deletion, and deleting additional occurrences cannot create subset sums. Hence this witness gives every $(0,n)$, $n\geq1$.

### One deletion tolerance

Let $F_1=F_2=1$ and $F_{s+2}=F_{s+1}+F_s$. The prefix identity is

$$
\sum_{r=1}^{k}F_r=F_{k+2}-1.
$$

The elementary interval induction says that a positive nondecreasing sequence beginning with 1 represents every integer from zero to each prefix total if every following term is at most one plus the preceding total. Indeed, the old interval $[0,S]$ and its translate $[c,c+S]$ cover $[0,S+c]$ when $c\leq S+1$.

Delete any indexed occurrence $F_j$. One initial 1 remains. For $s>j$, the retained total before $F_s$ is $F_{s+1}-1-F_j$. The required inequality is $F_s\leq F_{s+1}-F_j$, equivalent to $F_{s-1}\geq F_j$, valid because $s-1\geq j$. Earlier inequalities remain valid. This proves completeness after every single deletion, including either of the two initial ones.

For two deleted occurrences $F_i,F_j$ with $i<j$, choose $1\leq d\leq F_i$, and define

$$
x_t=F_{j+2t+1}-d\qquad(t\geq0).
$$

For $t=0$, $x_0<F_{j+1}$, while all available terms before $F_{j+1}$ total $F_{j+1}-1-F_i<x_0$. For $t>0$, put $s=j+2t$. A representation of $x_t<F_{s+1}$ cannot use terms later than $F_s$. If it omits $F_s$, its maximum possible sum is $F_{s+1}-1-F_i-F_j<x_t$. It must therefore use $F_s$, leaving a representation of $F_{s-1}-d=x_{t-1}$, which the induction excludes. These missing numbers tend to infinity. Thus every pair deletion is incomplete; so is every deletion containing a pair. This gives all $(1,n)$, $n\geq2$.

The arguments above are contained in the prior manuscript. [Graham (1964)](https://www.fq.math.ca/Scanned/2-1/graham.pdf), pages 1–2, states the one- and two-deletion facts and proves the latter; the one-deletion result is credited there to Brown. No unretrieved external theorem is needed for the checks just given.

## Reduction of the obstruction to central intervals

For a positive nondecreasing sequence $B=(b_i)$, set

$$
S_j=\sum_{i\leq j}b_i,\quad P_j=\operatorname{FS}(b_1,\ldots,b_j),\quad
\delta_j=S_j-b_{j+1}.
$$

Complementing an indexed subset proves $P_j=S_j-P_j$. Repetitions cause no problem.

### Slack after deletion

Suppose a positive nondecreasing sequence $A$ tolerates every single deletion. If bounded, it is eventually a positive constant and its slack tends to infinity. Otherwise fix an occurrence $a_i$. Completeness after deleting it implies, for all sufficiently large $k\geq i$,

$$
a_{k+1}\leq S_k-a_i+1.
$$

If this failed for infinitely many $k$, the number $S_k-a_i+1$ would be too large for the retained first $k$ terms and too small for any later term. Those absent numbers tend to infinity. Hence $\delta_k\geq a_i-1$ eventually. Choosing $i$ with arbitrarily large $a_i$ proves $\delta_k\to\infty$. No threshold uniform in $i$ is asserted.

For a fixed deletion $D$ of $d$ occurrences and total value $C$, once the original prefix contains all of $D$, the new slack at index $k-d$ is exactly $\delta_k-C$. Thus any fixed finite deletion preserves divergent slack. This is a statement about slack, not a claim that every such deletion preserves completeness.

### Long gaps from a deletion-minimal sequence

Call $B$ deletion-minimal if it is complete and every one-occurrence deletion is incomplete. Suppose, additionally, some fixed $T\geq1$ gives $[T,S_k-T]\subset P_k$ for all sufficiently large $k$.

For each prescribed $C\geq0$, the following constructs one pair whose deletion has intervals of more than $C$ missing integers arbitrarily far out. First $B$ is unbounded: a bounded nondecreasing sequence has an infinite constant tail, and deletion of one tail occurrence preserves its whole subset-sum set. Choose $i$ with $b_i>2T+C$, then a sufficiently large $k\geq i$ with the central interval property and $S_k\geq2T$. Fix one $j>k$. Let $Q$ be the subset sums of the tail beyond $k$, with the occurrence $j$ removed.

The unbounded set $Q\subset\mathbb N_0$ has arbitrarily late consecutive elements $q<q'$ with $q'-q>S_k-2T+1$. Otherwise the intervals $[q+T,q+S_k-T]$ would eventually meet or be adjacent and would make $P_k+Q$ complete, contradicting deletion-minimality at $j$.

After removing $i$ as well, the retained prefix sums lie in $[0,S_k-b_i]$. Thus

$$
[q+S_k-b_i+1,q'-1]
$$

is missed. Its number of integers is $(q'-q)-(S_k-b_i)-1\geq b_i-2T+1>C$. The same fixed pair $\{i,j\}$ works for arbitrarily late gaps. The pair may depend on $C$; a single pair with unbounded gap lengths is neither used nor established.

### Extending one successful deletion

Assume $A$ tolerates every two-occurrence deletion, and let $D$ be any finite deletion leaving a complete sequence $B=A\setminus D$. Tolerance of every single deletion follows by extending to a pair and restoring one occurrence. The slack result therefore applies to $B$. The central-interval theorem, proved below, gives its fixed end margin $T$.

If no one-occurrence enlargement of $D$ succeeds, $B$ is deletion-minimal. Apply the preceding gap argument with $C=\sum_{i\in D}a_i$. It produces a pair $E\subset B$ whose deleted subset-sum set $R$ has arbitrarily late missing intervals $[u,u+\ell-1]$, with $\ell>C$. Restoring $D$ adds an element of $\operatorname{FS}(D)\subset[0,C]$. Every integer in $[u+C,u+\ell-1]$ remains missing from $R+\operatorname{FS}(D)$, since subtracting any such addend stays inside the old gap. These nonempty gaps show $A\setminus E$ is incomplete, contradicting pair tolerance.

Therefore each successful finite deletion has at least one successful one-term extension. Starting from the empty deletion gives a successful deletion of each prescribed finite size. This is the existential conclusion needed for the obstruction. It is not universal finite-deletion tolerance.

## Audit of the central interval theorem

The theorem assumes $B$ positive and nondecreasing, $[T,\infty)\subset P=\operatorname{FS}(B)$, and $\delta_j\to\infty$. It concludes $[T,S_N-T]\subset P_N$ for all sufficiently large $N$, retaining the originally fixed $T$.

### Locate a missing sum near a cut

If $x\in[T,S_N-T]\setminus P_N$, choose the least $i\leq N$ with $S_i\geq x+T$. Such an $i$ exists. Put $y=S_i-x$, so $T\leq y<b_i+T$. If $y<b_i$, global completeness represents $y$ using only terms before $i$; positivity and monotonicity exclude every later term. Complementation in the first $i$ indices would represent $x$, a contradiction. Therefore $y\geq b_i$, and

$$
x\leq S_{i-1}<x+T.
$$

Thus $x=S_j-u$ for a cut $j=i-1<N$ and $0\leq u<T$. The argument does not use divergent slack.

### Bounded sequences and globally missing labels

If $B$ is bounded, write its fixed initial prefix total as $C$ and its constant tail value as $a>0$. A prefix with $v$ tail copies represents every globally representable $x\leq va$: in a representation $x=u+ra$, the initial-prefix sum $u\geq0$ forces $r\leq v$. Reflection in total $C+va$ also represents every central $x\geq C$. When $va\geq C$, the ranges $x\leq va$ and $x\geq C$ cover the central interval. This settles every sufficiently long prefix in the bounded case.

Now assume $b_j\to\infty$. A globally represented central $x$ absent from $P_N$ must use an occurrence beyond $N$, so $x\geq b_{N+1}$. In the cut representation above, $S_j=x+u\geq b_{N+1}$. Hence cut indices tend to infinity along any family of missing central sums with $N\to\infty$.

All globally representable integers below $T$ have representations in one common finite prefix. For sufficiently large cuts, complementing such a representation would rule out its label $u$. Consequently the relevant labels belong to

$$
H=\mathbb N_0\setminus P\subset\{1,\ldots,T-1\}.
$$

If $H$ is empty, the contradiction is already complete. Otherwise put $h=\max H$, $q=|H|$. These are fixed finite positive integers.

### States and normalization of repetitions

A state $(j,N,E)$ consists of $j<N$, a nonempty $E\subset H$, and missing sums $S_j-E\subset\mathbb Z\setminus P_N$. Terms $j+1,\ldots,N$ are its available occurrences. A state is constant if their values are all equal, and distinct otherwise.

For a constant state with available value $a$, if $j=0$ or $b_j<a$, it is normalized. If $b_j=a$, let $p$ precede the entire block of value $a$. Replace the state by $(p,p+1,E)$. If $S_p-e$ had a representation in $P_{p+1}$, appending the $j-p$ distinct occurrences at positions $p+2,\ldots,j+1$ would represent $S_j-e$ inside $P_N$. Thus the new state is valid. The labels are unchanged.

This is the essential repeated-value check: the proof moves occurrences and never collapses their values into a set. When original cuts tend to infinity, their available values tend to infinity, and the first occurrence of each such value also tends to infinity. Normalization therefore preserves divergence of cut indices. Eventual arguments can discard the $j=0$ case.

### The next distinct value is close

At any sufficiently large state, let $a=b_{j+1}\geq T$, and let $b>a$ be the next strictly larger value in the entire sequence. Unboundedness ensures it exists, even if its index exceeds $N$. Then

$$
1\leq b-a\leq\min E\leq h.
$$

For if $b>a+e$ for some $e\in E$, completeness represents $a+e\geq T$. No term can exceed $a$. Nor can an occurrence of $a$ be used: removing that occurrence would represent the globally missing $e$. All used terms are therefore smaller than $a$, hence before the cut. Complement them in the first $j$ occurrences and add the available occurrence $a$ at $j+1$. This represents $S_j-e$, contradicting the state. The occurrence at $j+1$ is disjoint from the complemented prefix.

### Bounded diameter forces one common earlier cut

Consider nonempty sets $R_j\subset\mathbb Z\setminus P_j$ with

$$
\min R_j\to\infty,\qquad \max R_j\leq S_j-T,\qquad
\max R_j-\min R_j\leq2h.
$$

Choose $J$ large enough to represent every globally represented integer below $T$ and to have $b_{J+1}>3h$. For large $j$, every $x\in R_j$ exceeds both $T$ and $S_J$. The cut argument writes $x=S_{\ell_x}-u_x$, with $\ell_x<j$ and $0\leq u_x<T$. Necessarily $\ell_x>J$; otherwise $S_{\ell_x}\geq x>S_J$ is impossible. Complementation now forces $u_x\in H$.

For $x,y\in R_j$, the two cut totals differ by at most $2h+h=3h$. Distinct cuts beyond $J$ differ by at least one term greater than $3h$. Hence all cuts coincide at some $\ell<j$, giving $R_j=S_\ell-E'$ for nonempty $E'\subset H$. Because $S_\ell\geq\min R_j\to\infty$, the output cuts also tend to infinity. This last point is needed for subsequent transitions.

### Transition from a distinct state

Let $a=b_{j+1}$, and let $b>a$ be the first larger available value. Monotonicity makes it the next globally distinct value, so $1\leq b-a\leq h$. Subtract these two available occurrences, separately, from all missing sums:

$$
R_j=(S_j-a-E)\cup(S_j-b-E).
$$

Every resulting integer is missing from $P_j$, because adding back its subtracted occurrence would give a forbidden representation in $P_N$. Also

$$
\min R_j\geq\delta_j-2h\to\infty,\quad
\operatorname{diam}(R_j)\leq2h,\quad
\max R_j\leq S_j-T
$$

eventually. The common-cut result gives a state $(\ell,j,E')$ with $\ell\to\infty$. The second translated set contains a point strictly below the minimum of the first, so $|E'|=|R_j|>|E|$. Normalizing a constant output preserves this increase and divergence.

### Transition from a constant state

For a normalized constant state at large $j$, write $a=b_{j+1}>b_j$. Now use only

$$
R_j=S_j-a-E=\delta_j-E.
$$

Its minimum tends to infinity, diameter is at most $h$, and maximum is eventually at most $S_j-T$. Again the output is a state $(\ell,j,E')$, with $\ell\to\infty$, and now $|E'|=|E|$.

If that state is distinct, stop this transition. If constant, its $r=j-\ell\geq1$ available occurrences all have value $b=b_j$, giving

$$
E'=E+(a-rb).
$$

The next strictly larger value after the new cut is $a$. Applying the preceding close-value bound at the new cut, which tends to infinity, yields

$$
a-b\leq\min E'=\min E+a-rb,
\quad\text{so}\quad(r-1)b\leq\min E\leq h.
$$

Eventually $b>h$, forcing $r=1$. Thus $\min E'=\min E+(a-b)>\min E$. Subsequent normalization preserves the labels and divergent cuts. Using the larger value $a$, which lies just outside the new certifying prefix $P_j$, is valid because the close-value lemma explicitly allows it.

### A bounded potential gives the contradiction

For a normalized state define

$$
\Phi=\begin{cases}
(h+1)|E|+\min E,&\text{constant},\\
(h+1)(|E|+1),&\text{distinct}.
\end{cases}
$$

This is a positive integer no larger than $(h+1)(q+1)$. Each eventual transition increases it strictly: a constant-to-constant step raises the minimum label; a constant-to-distinct step increases it by $h+1-\min E\geq1$; a distinct step gains at least one label and thus at least one unit of potential regardless of its output type.

The proof does not require one fixed starting state to admit infinitely many backward steps. Suppose instead there are missing central sums for arbitrarily large $N$. They give normalized states with cuts tending to infinity. Among finitely many potential values, take the largest $p$ realized at arbitrarily large cuts. Apply one transition to a sequence of such states. All sufficiently late outputs remain normalized, have divergent cuts, and have potential greater than $p$. Some one of the finitely many larger values recurs infinitely often, contradicting maximality of $p$. This establishes the eventual central interval conclusion.

All asymptotic bounds are applied to diverging families of cuts, including after normalization. There is no unjustified claim that an indefinitely iterated decreasing index stays large.

## Completion of the integer valued classification

If $m\geq2$ and $C(m)$ holds, every pair deletion is complete: extend the pair to $m$ indices, then restore the extras. For positive sequences, the extension result yields one complete deletion of size $n$, contradicting $N(n)$.

For a bounded nondecreasing integer sequence, integrality forces eventual constancy. Completeness forces its tail value to be positive. Deleting $n$ sufficiently late copies of this value leaves infinitely many identical copies and preserves the full subset-sum set. Such a sequence cannot satisfy $N(n)$.

For an unbounded nondecreasing integer sequence there are only finitely many nonpositive occurrences. Discard its zeros, replace each negative $-c$ by $c$, preserve occurrence identities, and sort to obtain a positive nondecreasing sequence $A^+$. Sorting is possible because only finitely many occurrences lie below any fixed bound. For any finite deletion $D$ among these nonzero occurrences, let $C_D$ be the sum of the absolute values of the surviving negative terms. The identity of two-element contribution sets $\{0,c\}=c+\{0,-c\}$ gives

$$
\operatorname{FS}(A^+\setminus D)=C_D+\operatorname{FS}(A\setminus D).
$$

Translation by the fixed $C_D$ preserves eventual completeness in both directions. Thus pair tolerance and universal failure at size $n$ transfer to $A^+$, where the positive argument contradicts them. Only deletions of nonzero occurrences are needed for this contradiction; removing zeros does not need to preserve the cardinalities of every original deletion pattern.

Together with the two constructions, this proves the advertised iff for every finite $0\leq m<n$.

## Natural valued and zero indexed formulations

The same classification holds for monotone $a:\mathbb N\to\mathbb N$. Exclusion follows from the integer theorem; the witnesses are already positive. With zero-based indexing use $a(k)=2^k$ or $a(k)=F_{k+1}$, where $F_1=F_2=1$. Using $F_k$ with the conventional $F_0=0$ would incorrectly introduce an extra zero occurrence: deleting that zero and one positive Fibonacci occurrence leaves a complete sequence, so it fails $N(2)$. No initial zero is part of the witness.

Replacing deleted indices by zero has exactly the same finite subset sums as deleting them. A sum using the updated sequence can drop all indices in the deletion set without changing its value, and every retained-index sum is still available. This remains true with repeated values and preexisting zeros. The updated sequence itself need not be monotone; its subset sums equal those of the ordered retained subsequence, to which the theorem applies.

The [Formal Conjectures statement at commit 97a729a](https://github.com/google-deepmind/formal-conjectures/blob/97a729a35de6de358570f9b5d820d6effb11bd43/FormalConjectures/ErdosProblems/348.lean) uses precisely an indexed-sum predicate and zero updates. Its [predicate definitions at that commit](https://github.com/google-deepmind/formal-conjectures/blob/97a729a35de6de358570f9b5d820d6effb11bd43/FormalConjecturesForMathlib/NumberTheory/AdditivelyComplete.lean) quantify finite sets of indices and eventual membership in their sumset. It records the answer and cites Geneson, but its theorem body still contains `sorry`. It supplies no formal verification of the classification.

## Limits and attribution

The infinite argument above is the basis of acceptance. Historically recorded finite diagnostics checked examples, signs, occurrence handling, and indexing; they cannot prove eventual completeness or replace the central-interval proof.

This verdict does not establish that the theorem is the first result of its kind, that it has been peer reviewed, that any mathematical database is fully current, or that the manuscript's separate exponential-sequence results have been audited. It attributes the accepted classification to the inspected Geneson preprint, with the binary and Fibonacci examples retaining their earlier attribution.
