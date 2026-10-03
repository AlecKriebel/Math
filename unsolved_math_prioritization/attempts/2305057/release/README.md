# A known negative answer to Baernstein's Plessner question

**Catalogue:** 2305057 / AMR-022-5057  
**Original title:** Research Problems in Function Theory — Problem 5.57  
**Checked:** 3 October 2026  
**Result:** Negative, by Oleg Ivrii's preprint of 16 September 2026. This packet verifies and attributes an existing result; it claims no new resolution.

## The question

For every holomorphic function on the unit disc, must almost every boundary point either admit an angular limit or have every Stolz-angle image omit only a set of zero logarithmic capacity?

## Answer and attribution

Ivrii's [Theorem 1.1](https://arxiv.org/html/2609.18785v1) supplies counterexamples of the form

\[
f(z)=\sum_{k\ge1}\frac{\xi_k}{\sqrt{k}}z^{2^k},
\]

where the coefficients are independent standard complex Gaussians. Almost surely there is a full-measure set of boundary points where radial values have modulus liminf zero and limsup infinity, while every Stolz-angle image has planar density zero at infinity. The latter image therefore has a complement of positive area, hence positive logarithmic capacity. The angular-limit alternative also fails.

The relevant reference is Oleg Ivrii, *Non-tangential ranges of holomorphic functions at Plessner points*, [arXiv:2609.18785v1](https://arxiv.org/abs/2609.18785v1), submitted 16 September 2026. Only the preprint status is asserted; no journal acceptance or peer-review claim is made.

## Verification material

- [Source, history, and attribution checks](SOURCE_GATE.md)
- [Complete counterexample verification](COUNTEREXAMPLE_VERIFICATION.md)
- [Single substantive attempt](turn_01.md)
- [Research log](RESEARCH_LOG.md)

The verification reconstructs the required counterexample from standard Brownian-motion facts. It supplies an elementary occupation-time proof of the small-radius sausage bound needed in the argument, instead of relying on a sharp sausage asymptotic. Neither that proof variant nor its constants are claimed novel.

No numerical sample or finite truncation is presented as a counterexample certificate. The construction is a rigorous almost-sure existence argument. The broad invitation to seek other improvements of Plessner's theorem is not an assertion that every possible strengthening is classified here.
