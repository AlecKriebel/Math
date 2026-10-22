# Function Theory 5.50: an existing affirmative solution

## Exact question and answer

For an annular holomorphic function on the unit disk, put

\[
S(f)=\{a\in\mathbb C:Z'(f-a)\ne\mathbb T\},
\]

where \(Z'\) is the boundary accumulation set of the indicated zeros. The question is whether \(|S(f)|=\aleph_0\) can occur.

**Yes. This is an existing theorem of F. W. Carroll (1979), not a new result.**

Carroll's Theorem 2 establishes a strongly annular example with countably infinite \(S(f)\). His definition on p. 330 is exactly the displayed definition: “singular” refers to an exceptional value for boundary accumulation of its preimages. It does not mean a critical or asymptotic value of an inverse function. [C]

If \(r_n\uparrow1\) witnesses strong annularity, then the circles \(J_n=\{|z|=r_n\}\) are nested Jordan curves tending to the unit circle. Their minimum moduli tend to infinity. Thus strong annularity supplies every condition in the question. The boundary preimage accumulation sets agree, so Carroll's theorem answers the exact question.

## Checking the limiting argument

Here is a detailed check of the passage from the published construction to its conclusion. Carroll's Theorem 1 supplies distinct increasing real values \(a_j\), boundary caps \(G_j\) having nonempty open circular arcs, radii \(r_k\uparrow1\), and holomorphic \(f_k\) such that

\[
\sup_{|z|\le r_{k-1}}|f_k-f_{k-1}|<2^{-k},\qquad
\min_{|z|=r_k}|f_k|>2^k,
\]

and \(f_k-a_j\) is zero-free in \(G_j\) whenever \(k\ge j+1\) (and \(k\ge2\)). [C]

On each compact subdisk, the differences are bounded by the tail of a convergent geometric series. Consequently \(f_k\) converges locally uniformly to a holomorphic function \(f\). For fixed \(k\ge2\), all subsequent difference estimates hold throughout \(|z|\le r_k\), giving

\[
\sup_{|z|\le r_k}|f-f_k|\le\sum_{m=k+1}^{\infty}2^{-m}=2^{-k}.
\]

Therefore

\[
\min_{|z|=r_k}|f(z)|>2^k-2^{-k}\longrightarrow\infty.
\]

In particular \(f\) is nonconstant. Fix \(j\). Hurwitz's theorem applied to the tail of \(f_k-a_j\) on the connected cap \(G_j\) says that \(f-a_j\) is zero-free or identically zero there. The latter would force \(f\equiv a_j\) throughout the disk by the identity theorem, contradicting the preceding lower bounds. Hence \(f\) omits \(a_j\) throughout \(G_j\). Each interior point of the cap's circular boundary arc has a disk-relative neighborhood contained in \(G_j\). That arc contains no limit point of \(f^{-1}(a_j)\), so \(a_j\in S(f)\). Distinctness gives infinitely many such values.

To bound the cardinality above, use the classical annular-function fact stated on p. 491 of Osada [O]: for \(a\ne b\), the open sets

\[
U_a=\mathbb T\setminus Z'(f-a),\qquad U_b=\mathbb T\setminus Z'(f-b)
\]

are disjoint. Osada credits the Koebe–Gross theorem for this implication. Choose a fixed countable dense subset of \(\mathbb T\). Every nonempty \(U_a\) contains a member of this subset; choosing its first member in an enumeration injects \(S(f)\) into \(\mathbb N\). Combining both bounds proves \(|S(f)|=\aleph_0\).

## Dependency and verification boundary

The existence of the approximating functions is the credited content of Carroll's Theorem 1. Its published proof, including the Runge approximation step and Lemma A using Arakelian approximation, was read in full (pp. 330–334). The argument above checks the implication of those construction properties, including the otherwise implicit nonconstant alternative in Hurwitz's theorem. It is not a replacement proof of the approximation theorems or of Koebe–Gross.

The accompanying program verifies finite exact identities relevant to the construction and limiting estimates. It does not construct the infinite function, prove an approximation theorem, or formally verify the analytic proof. The affirmative classification rests on the published theorem and the exact definition match, not on numerical evidence.

## References

- [C] F. W. Carroll, *A strongly annular function with countably many singular values*, Mathematica Scandinavica **44** (1979), 330–334. [DOI](https://doi.org/10.7146/math.scand.a-11814). [Publisher PDF](https://journals.msp.org/mscand/article/download/1834/1833).
- [O] A. Osada, *On the distribution of a-points of a strongly annular function*, Pacific Journal of Mathematics **68** (1977), 491–496. [Publisher PDF](https://msp.org/pjm/1977/68-2/pjm-v68-n2-p17-s.pdf).
- [H] W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)*, 2018, Problem and Update 5.50, printed p. 104, reference [145]. [arXiv](https://arxiv.org/abs/1809.07200).
