# Statement overlap, literature, and provenance

For R=aI+E+W, put N=n(n-1)/2. Then ||R_I||^2=Na^2 and scal=n(n-1)a. For d>0,

\[
\overline{\{\operatorname{scal}>d\|W\|\}}
 =\{a\ge0,\ \|W\|^2\le cNa^2\},\qquad
 c=\frac{2n(n-1)}{d^2}.
\]

The identity includes the complete traceless-Ricci subspace at a=W=0. The central d(n)^2=2(n-2)(n-1) maps exactly to c=n/(n-2).

The [2008 primary report](https://ems.press/content/serial-article-files/46179), Böhm with Wilking, pp. 1941–1942, defines a strict cone but puts overbars in its preservation theorem and necessity conjecture. Page 1942 was visually inspected. It gives high-dimensional PDE sufficiency, asks whether its listed parameters are necessary, and asks for threshold 12. The 2007 report's closed-cone ODE classification and the new record therefore share all algebraic work, but their stated PDE/ODE scopes differ. The parity repair in the 2007 source remains inferred, not an official erratum.

The existing rank-815 artifact contains five approaches, with an independent audit accepting the scoped partial results and separately correcting the 2008 closure description. Its archive hashes are in PUBLIC_METADATA.json. Those approaches are not repeated or counted as new here. The sole new approach is a specific local-to-compact geometric realization proof, submitted for audit in APPROACH_1_PDE_REALIZATION.md.

## Sources inspected

- [Richard and Seshadri, Noncoercive Ricci flow invariant curvature cones](https://arxiv.org/pdf/1308.1190), Definition 1.5, Theorem 1.7, Remark 1.8: their definition is ODE tangency; they distinguish it from literal preservation by geometric Ricci flow. This is a warning against assuming the converse maximum principle. Their noncoercive-cone restrictions do not evaluate the extrema needed here.
- [Xu, On some new Ricci flow invariant curvature conditions, preprint v1](https://arxiv.org/html/2412.13633v1), Conjecture 1 and Theorem 1.1: the broader n>=12 family remains conjectural in the inspected preprint. Its proved parameter range at n=12 starts at 35/12, while the target endpoint is zero. [Published metadata](https://link.springer.com/article/10.1007/s12220-025-02158-2) records publication on 20 August 2025; the version-of-record body was not inspected. No full resolution was found in these bounded checks.
- [Branca, Catino, Dameno and Mastrolia, Rigidity of Einstein manifolds with positive Yamabe invariant](https://link.springer.com/article/10.1007/s10455-025-09996-x), equations (2.9)–(2.11): the scalar-minus-Weyl-norm conformal covariance used in the new argument is standard modified-scalar-curvature calculus. We do not attribute the new compact-extension argument to this paper.
- [Tataru course, notes by Ning Tang](https://math.berkeley.edu/~ning_tang/files/notes/graduate/Math222B_Spring2023.pdf), Theorem 13.10: local analytic Cauchy solvability on a non-characteristic hypersurface. The application here is the linear equation (3), with positive normal principal coefficient.

The live aggregator page could not be read by the web tool; an ordinary HTTPS request returned 403. The full supplied record and report map were inspected instead. The report is absent, represented by {}, not null. Default sorted JSON of [record, {}] is 4,187 bytes and matches the catalog review hash. All three complete corpus files were hashed and parsed. No record contents or copied source text are distributed.

Fresh exact-ID and exact-problem-number repository searches found no matching PR, and exact-ID code and commit searches found no matches. These bounded searches do not clear all branches or private work. The supplied rank-815 authored artifacts are concrete prior work and are the basis for avoiding repetition.

No novelty, complete literature clearance, formal proof-assistant certification, or human peer review is claimed. The n0=12 question remains unsolved here.
