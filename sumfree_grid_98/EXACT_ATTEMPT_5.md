# Exact finite-grid attempt 5: upper-bound routes and non-shell trades

Date: 2026-10-20. This attempt seeks a matching upper theorem for the stronger boundary-completed construction B_t, rather than another restatement of its lower bound.

## Candidate finite formula and precise unproved step

Attempt 4 gives the exact lower bound

C_d(N)=N^d−(N−1)^d+max_t[H_{d,N−1}(2t−d−1)−H_{d,N−1}(t−1)].

The bracket is the cardinality of a zero-based cube slice after setting a=t−d and translating only the count. This suggests the possible formula f_d(N)=C_d(N), but **no general proof is supplied**. An even broader identity with the maximum unrestricted zero-based sum-free subset replacing the maximum slice is also unproved. Neither a counting translation nor matching small cases establishes either identity.

The exact shell recurrence shows precisely what a matching upper argument must establish: for every sum-free F⊆[N−1]^d,

|F|−|(F+F)∩T| ≤ max_t[H_{d,N−1}(2t−d−1)−H_{d,N−1}(t−1)],

where T=[N]^d\[N−1]^d. We have not proved this inequality or found a counterexample.

## Why two tempting induction routes fail

### Scalar extremal size loses necessary information

In [4], the sum-free sets F_1={2,3} and F_2={3,4} both have maximum size 2. On adjoining the shell {5}, F_1 forbids 5=2+3, so its optimal extension still has size 2. F_2 forbids no shell point and extends to {3,4,5}, of size 3. Thus even knowing that F is an extremizer, and knowing f_1(4), does not determine its extension score. An induction needs a sumset boundary profile, not just f_d(N−1).

### Boolean upward compression does not generalize naively

The positive set {1,3,5}⊆[5] is sum-free. Move every member up by one when its successor is absent and still in [5]. The resulting set is {2,4,5}, which is not sum-free because 2+2=4. Therefore the successful N=3 Boolean disjoint-union compression from attempt 2 cannot simply be applied as integer-coordinate upward compression for larger alphabets. The failure explicitly involves repeated summands and is not removed by the intended convention.

## Exhaustive local trade test

For a selected best B_t, we tested whether deleting one selected vertex and adding two omitted vertices improves cardinality. This is a complete test of this local move class, not a heuristic walk.

For each omitted point w, enumerate every forbidden edge containing w and otherwise contained in B_t. These are:

- the repeated relation w+w=z, if z∈B_t;
- w+x=z with x,z∈B_t;
- x+y=w with x,y∈B_t, allowing x=y.

Deleting one v∈B_t makes w individually admissible exactly when v belongs to the intersection of all these blocking sets. For every eligible deletion, test all candidate pairs of additions against each other and the remaining B_t, including all repeated-summand relations. Any found improvement is rechecked against all ordered pairs in the resulting set.

`search_boundary_trades.py`, executed under python -OO, found no such improvement for:

(d,N)=(2,8), (3,5),(3,6),(3,7),(3,8),(3,9),(3,10),(3,11), (4,4),(4,5), (5,4),(6,3).

In fact every omitted point in each of these instances has blocking sets with empty common intersection, so it cannot be added after only one deletion. Thus these B_t are stable against even a one-for-one exchange involving an omitted point. This is a rigorous local obstruction only. It says nothing about deleting two or more points or replacing a large fraction of the set. Results are in `BOUNDARY_TRADE_RESULTS.jsonl`.

## Final status after five substantive attempts

The exact arbitrary-(d,N) maximum remains unresolved by this work. The attempts did produce:

1. Exact slice-count formulas, elementary exact families, and independently replayed small-grid certificates.
2. A Boolean reduction for N=3, exact f_6(3)=706 by two independent exhaustive methods, and an exact formula in infinitely many dimensions using a primary partition-free-family theorem with its actual dimension restrictions preserved.
3. A counterexample to exact plain-slice extremality already on [11]^3, plus eventual failure for every fixed d≥3.
4. A stronger explicit boundary completion that beats isolated completion, an exact count, an exact profile recurrence, and a correctly qualified inclusion-maximality proof.
5. Identified failures of scalar induction and naive compression, and a complete local-trade test that did not close the global upper gap.

These results must not be relabeled as a full exact solution of Green's unrestricted finite question. Separately, the all-dimensional asymptotic theorem has its own source/proof audit. No material from this work has been remotely published.
