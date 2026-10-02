# Turn 3: explicit name-dependent finite-choice coding into intervals

**Scoped constructive result; the full planar WKL question remains unresolved.** The extensional obstruction in Turn 2 is not a bound on ordinary Weihrauch preprocessing power. This turn constructs, for every fixed n, a strong reduction of choice on the known n-point discrete space to choice on a nondegenerate interval. The finite-choice upper-bound phenomenon is known; compare compact discrete choice in Proposition7.39 of the [Brattka–Gherardi–Pauly survey](https://arxiv.org/abs/1707.03202). The purpose here is an explicit name-dependent construction and its exact boundary, not a novelty claim.

## 1. A finite tree of exclusion histories

Fix labels S_0={0,...,n-1}. A valid input is an enumeration of excluded labels, promised to leave a nonempty set A. Repetitions are ignored. A history h is a finite sequence of distinct excluded labels; let S_h be the remaining labels. Consider every history of length at most n-1, not merely the eventual history of one input.

Assign a nondegenerate rational closed interval I_h to each history. Start with I_empty=[0,1]. Suppose I_h=[l,l+L] and S_h has k>=2 elements, listed i_0<...<i_(k-1). Define

    I_(h i_j) = [l+L(3j+1)/(3k+1),
                   l+L(3j+2)/(3k+1)].            (1)

These child intervals are strictly inside I_h, have positive pairwise gaps, and each has length L/(3k+1). At k=1 there are no children. Every interval in the finite tree has length at least

    product_(k=2,...,n) 1/(3k+1) > 0,           (2)

with empty product1 when n=1. The coordinates depend only on the finite history, not on the times at which exclusions arrived.

## 2. A fixed computable decoder for the whole finite tree

Give both endpoints of I_h the label min(S_h). All endpoints belonging to distinct nested or sibling intervals are distinct, since children are strictly interior and separated. Sort this finite set of rational mesh points. At a mesh point labeled i assign the unit vector e_i in the n-dimensional probability simplex. Between consecutive mesh points interpolate linearly. This defines computable continuous piecewise-linear functions

    w_0,...,w_(n-1):[0,1]->[0,1],   sum_i w_i(x)=1.

For every history h and every x in I_h,

    w_i(x)>0 implies i in S_h.                  (3)

Indeed the mesh points inside I_h are its endpoints and endpoints of descendant intervals. Every such label belongs to S_h. The two endpoints of any mesh segment lying in I_h therefore have labels in S_h, and linear interpolation introduces no other nonzero coordinate. Endpoints of I_h are included in the argument.

Given any Cauchy name of x, simultaneously semidecide w_i(x)>0 for all i and output the first successful label. At least one test succeeds because the weights sum to one. Strict positivity of a computable real is semidecidable; no test for zero or equality with a mesh point is needed. By (3), every possible returned label is allowed at the current history. The decoder is fixed for this n and sees no source input.

## 3. Computable negative-name preprocessing

While reading the exclusion enumeration, maintain h and its surviving set S_h. Upon a newly excluded label i in S_h, descend from I_h to I_(h i); repeated exclusions cause no change. The nonempty-domain promise prevents an exclusion of the last surviving label. At each stage enumerate the open complement of the current rational closed interval, dovetailing these enumerations as stages proceed.

The intervals decrease, so this is consistent negative information. At most n-1 proper descents occur. Every label outside the final A is eventually excluded, so there is a finite last history h_* with S_(h_*)=A. We do not need to recognize when that history has become final. The resulting negative name describes exactly I_(h_*), a nonempty nondegenerate rational closed interval.

An interval-choice oracle must return a point x of this final interval, not a point of an earlier approximation. The decoder from Section2 then outputs a label in S_(h_*)=A. This proves, at the level of all allowed output Cauchy names,

    C_n reducible_sW CC_1 reducible_sW PWCC_2.    (4)

The second reduction embeds the interval as I x {0} and projects the first coordinate. Here C_n means choice on a fixed known discrete n-point space. It must not be confused with choosing from an arbitrary closed set of at most n unknown points in a continuum, or with unrestricted closed choice on N.

## 4. Why name dependence is real

Already for n=3, the two valid histories (0,1) and (1,0) both leave A={2}. Their final intervals lie in distinct first-level child intervals and are therefore disjoint. Thus the target set depends on exclusion order, even though the underlying source set is identical. This directly violates extensionality as used in Turn 2, while remaining a valid computable function on negative input names.

The construction does not contradict the four-choice planar extensional limit. It even handles five finite choices in a one-dimensional target, precisely by abandoning target-set extensionality. In a K5 obstruction argument there would be no single target vertex region B({i}) common to all relevant pair histories.

The result also gives no automatic reduction of WKL. For each fixed n the history tree, mesh and simplex decoder are finite, and the number of genuine exclusions is bounded. WKL must handle infinitely many coordinated bits. Taking a limit of these finite constructions does not supply a common continuous decoder, a preserved path-connected limit, or a uniform negative-name construction meeting all those demands. Those are the unresolved infinite requirements.

## 5. Exact checks and route status

`verify_turn3.py` constructs every exclusion history for n<=5 and checks exact rational interval nesting, sibling separation, the length bound, all mesh labels and midpoint decoder supports, and the explicit same-set/different-history witness. The proof works for every finite n; these finite checks only audit the stated construction.

The extensional barrier is now sharply delimited: it excludes a large natural class of static geometric encodings, while a concrete name-dependent method gets past every fixed finite-choice obstruction. A successful infinite planar coding still has to maintain topological path connectedness and strong name-level decoding simultaneously. No such coding is proved here.

Estimated completion toward the original strong-equivalence target:15%, low confidence. Three of five genuine turns used; two remain. No full solution or novelty claim; independent review pending.
