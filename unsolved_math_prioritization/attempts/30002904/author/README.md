# Generic infinite index subgroups of integral special linear groups

Problem OWR-13687-003, public problem 30002904. Research date: 2026-10-06.

**Status: partial result only. The ordinary operator-norm-ball question for every fixed n >= 3 is not solved here. No novelty claim is made.**

The exact target is the probability that two independent uniformly selected matrices in

\[
B_X=\{g\in\mathrm{SL}_n(\mathbb Z):\|g\|_{\mathrm{op}}\leq X\},\qquad
\|g\|_{\mathrm{op}}=\sqrt{\lambda_{\max}(g^t g)},
\]

generate an infinite-index subgroup, for fixed n >= 2 as X tends to infinity. The primary source is Elena Fuchs's contribution to Oberwolfach Report 30/2015, printed p. 1709. Two generators, product counting measure, and this particular norm are retained. No random-walk law or inverse-bounded sampling law is substituted. The report concerns a June 2015 workshop and was published in 2016.

This package contains:

- `proof.md`: a model-correct proof of the known dimension-two conclusion using a modern counting input; an exact continuous SL3 singular-gap calculation; and explicit barriers to several attempted extensions.
- `status.json`: claims, nonclaims, and the five approaches examined.
- `checks.md`: author checks and computational diagnostics, with their limitations.
- `sources.json`: public references, retrieval information, byte counts, and hashes. Source documents themselves are not included.
- `manifest.json`: SHA-256 hashes and byte counts of the other package files.

The SL3 calculation corrects the numerical upper bound printed in Fuchs--Rivin, Theorem 3.4, under the intended interpretation as a limit of normalized Haar measures. It does not establish any discrete lattice-point asymptotic. Independent mathematical review remains required before relying on that correction publicly.

The rank-two conclusion is established here as an explicit consequence of Bulinski--Ostafe--Shparlinski, Lemma 3.6, plus the elementary argument supplied in `proof.md`. Their paper also documents a different defect in Fuchs--Rivin, Lemma 2.5. The present calculation and their documented correction should not be conflated.

The literature search was bounded. Failure to locate a higher-rank solution is not evidence of novelty, nor a certification that no such result exists.

Primary references: [OWR report](https://ems.press/content/serial-article-files/46576), [Fuchs--Rivin](https://academic.oup.com/imrn/article/2017/17/5385/3056825), [Bulinski--Ostafe--Shparlinski](https://arxiv.org/abs/2304.10980), [Aoun](https://arxiv.org/abs/1005.3445).
