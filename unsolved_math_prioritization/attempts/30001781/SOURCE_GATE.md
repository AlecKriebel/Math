# Exact source gate and corrected target

Problem30001781 / OWR-5152-008, checked2026-10-01 before substantive author turn1.

The primary source is Alexander E. Litvak's contribution, joint with Adamczak, Latała, Pajor and Tomczak-Jaegermann, OWR24/2011, printed pp.1343–1344. The complete contribution and adjacent relevant Latała contribution pp.1323–1325 were read. The target pages were visually inspected.

## Important extraction correction

The actual sharp scale is

    Lambda_(k,m)=sqrt(m)*log(3N/m)+sqrt(k)*log(3n/k).

The logarithms are **outside** the square roots. The pinned dataset incorrectly displays sqrt(m log(3N/m))+sqrt(k log(3n/k)), despite its source-verification label. That stronger expression is already false for independent variance-one symmetric exponential entries. For n=N=d and k=m=1, the maximum entry has distribution

    P(A_(1,1)<=u)=(1-exp(-sqrt(2)*u))^(d^2), u>=0.

At u=2C sqrt(log(3d)) this tends to zero for every fixed C. This calibrates the transcription; it does not refute the original logarithms-outside-radicals conjecture or resolve the campaign target.

## Exact hypotheses and unresolved question

The source has independent rows X_1,...,X_n in R^N, each centered, covariance identity, log-concave, and initially invariant under every coordinate sign change. Identical distribution is not required. A_(k,m) is the largest Euclidean operator norm over all exactly k rows and m columns. Equivalently it is the supremum of the associated bilinear form over k-sparse and m-sparse unit vectors; allowing supports of size at most k,m gives the same value by padding.

The conjecture asks to remove coordinatewise unconditionality while retaining independent isotropic log-concave rows. Central symmetry alone is not unconditionality. The report says 'with high probability' without a complete quantitative tail formula. The final Studia Mathematica2012 Theorem4.2 gives, under unconditionality, both the expected bound C Lambda and

    P(A_(k,m)>C Lambda+t)<=exp(-c min(t,t^2)), t>0.

This provides a useful precise benchmark. We distinguish proving the order bound with a specified tail from proving this entire tail formula under the weaker assumptions.

The report separately explains that its general Chevet inequality and the arbitrary-norm exponential comparison fail without unconditionality. Those counterexamples do not automatically refute the special Euclidean maximal-submatrix conjecture. Conversely, an argument that merely reuses that false general comparison does not prove the conjecture.

## Later literature actually checked

The final2012 Chevet paper retains unconditionality in the sharp theorem. The full author version of the2014 PLMS paper *Tail estimates for norms of sums of log-concave random vectors* (originally associated with the2011 announcement) gives the general-row estimate in Theorem5.1, with an additional sqrt(log log(3m)) on the column-complexity term, max(N,n) inside that logarithm, and a weaker tail denominator sqrt(log(3m)). The full formulas, not only the abstract, were read.

Latała–Strzelecka's final EJP2024 paper extends Chevet and maximal-submatrix estimates for Weibull and unconditional log-concave settings. It does not remove the relevant unconditionality assumption and explicitly keeps related arbitrary-log-concave comparisons open. Current targeted primary searches did not locate a resolution of the exact corrected original. This is a limited literature check, not a certification that no later paper exists.

## Prior campaign gate

Exact ID/source-code PR searches and remote branch search were empty; both main attempt-directory histories and the local all-ref target history were empty; no related-target group was found. The full pinned upstream record was read. No matching separate upstream OWR research report is available. Its generated literature summary is not a prior Alec campaign attempt.

Next substantive route: test the corrected conjecture for a genuinely non-unconditional class obtained by one common isometric quotient/rotation of unconditional latent rows, using the actual Chevet theorem in latent coordinates. Success in that class would be a partial theorem, not a general resolution. No source lookup, correction or audit is counted as a proof turn.
