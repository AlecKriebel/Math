# Turn 1: countable tail fusion for promised avoidance

Substantive author turn **1/5**. Let A=wFindHS_{Pi^0_1} in the exact source convention: the input is an open P⊆[N]^N with no homogeneous solution landing in P; every output h avoids P, meaning [h]^N∩P=∅. Ordinary and strong Weihrauch reducibility are distinguished throughout.

This turn tests whether many independent refinements can supply the missing path information. It proves a countable fusion statement, but does not eliminate adaptive dependence and does not resolve either source reduction.

## Theorem

Let hat(A) be countable parallelization, whose input is a uniformly named sequence (P_i)_{i∈N} of valid A-instances and whose output is a sequence of solutions. Then

                         hat(A) equivalent_sW A.                   (1)

Marcone–Valenti Proposition4.10 already gives finite-product idempotence. The proof below supplies the countable shifted-union argument explicitly. No claim of historical novelty is made.

## 1. Why the ordinary union fails

For each i let P_i={f∈[N]^N:f(0)=i}. No infinite sequence can land homogeneously in P_i, since a tail beginning after its possible occurrence of i lies outside. Thus every P_i is a valid promised input. Yet their countable union is the entire space, which has no avoiding solution and is outside the domain of A. Finite-union closure alone cannot be iterated by simply taking a countable union.

## 2. Shift the i-th constraint by i places

Write s_i(f)(n)=f(n+i). From the uniformly open names of the P_i compute

                         Q=⋃_{i∈N} s_i^{-1}(P_i).                  (2)

This is an open set with a computable name. Explicitly, for every cylinder [τ] enumerated into P_i, enumerate [α followed by τ] for every increasing string α of length i whose last element is smaller than the first element of τ. If τ is empty, its inverse image is the whole space. Dovetail all i, all enumeration stages and all finite α. This describes a genuine open-name transformation; the preprocessor does not compute any Ramsey solution.

We show Q is a valid A-instance. Fix an arbitrary infinite X⊆N, viewed increasingly. By the open Ramsey theorem and the promise on P_0, X has an infinite subset R_0 avoiding P_0. Pick h(0)∈R_0. Inductively, after R_i and h(i) have been chosen, restrict R_i to its elements above h(i). The open Ramsey theorem and the promise on P_{i+1} yield an infinite subset R_{i+1} of that tail which avoids P_{i+1}; choose h(i+1)∈R_{i+1}.

This is an existence argument verifying the domain promise, not a computable construction performed by the reduction. The resulting increasing h is a subsequence of X, and for each i,

                         ran(s_i(h))⊆R_i.                         (3)

For every g∈[h]^N, its i-th and later terms occur at indices at least i in h, so ran(s_i(g))⊆R_i as well. Therefore s_i(g)∉P_i for every i. Thus every g∈[h]^N is outside Q: h avoids Q.

Because every infinite X has such a subsequence h, no infinite X can land homogeneously in Q. This proves Q∈dom(A), using only the individual promises and classical open Ramsey existence.

## 3. Decode every allowed solution

Let h be any output of A(Q). For each i return s_i(h). To see that it avoids P_i, take an arbitrary f∈[s_i(h)]^N. Prepend the first i elements h(0),...,h(i−1) to f. The resulting g is an infinite subsequence of h and s_i(g)=f. If f∈P_i, then g∈Q by (2), contradicting that h avoids Q. Hence every returned tail is a valid output for its corresponding P_i.

The map h↦(s_i(h))_i is computable and uses no input name. It works for every allowed h, proving hat(A)<=_sW A. Conversely, send one P to the constant sequence P_i=P, and return the first component of any solution sequence. This proves the reverse strong reduction and (1).

For the singleton-first-coordinate example in §1, (2) becomes Q={f:∃i f(i)=i}. Since f is strictly increasing and starts in N={0,1,...}, this is exactly {f:f(0)=0}. Every avoiding h has h(i)>=i+1, so its i-th tail indeed avoids P_i. This directly contrasts the valid shifted union with the invalid ordinary union.

## 4. Consequence and remaining adaptive gap

Any uniformly supplied countable family of independent valid avoidance instances can be replaced by a single avoidance call. This includes a nonadaptive search that prepares countably many refinements in advance, provided every instance satisfies the required promise. It does not justify listing speculative instances whose validity depends on an unknown first answer.

The known factorization C_{N^N} equivalent_W C_{2^N} star A (Marcone–Valenti Proposition4.9) has an additional compact-choice instance obtained **after** an A-answer. The fusion above does not provide that missing choice, nor show that A is closed under sequential composition. A family's countability does not erase its dependence on an entire as-yet-unseen oracle output. The original two ordinary reductions remain unresolved after this first author turn.
