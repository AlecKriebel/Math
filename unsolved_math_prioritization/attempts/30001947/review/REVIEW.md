# Independent source review of the oriented Witt pairing question

**Verdict: PASS. The correct disposition is already solved in the literature.** The requested nontrivial bilinear Witt pairing does not occur in dimension \(4j+2\), for every \(j\ge0\), under the original integral-orientation and mod-two Witt-space conventions. Credit belongs to the cited prior literature; this is a source-status correction, not a new discovery.

**Target:** 30001947 / OWR-11454-005.  
**Reviewed document:** `SOURCE_STATUS.md`.  
**SHA-256:** `8393f0abbdd96e0abb5a3ed64875864e25168bbf437b0da5106752c5fa413d61`.  
**Date:** 30 September 2026. **Reviewer model:** gpt-6-astra, xhigh.

This was a targeted independent AI source audit, not a new proof search, formal verification, or human peer review.

## Exact original question

I checked Friedman's question in the author-hosted [OWR 56/2011 report](https://www.mathi.uni-heidelberg.de/~banagl/pdfdocs/OWR_2011_56.pdf), local pp. 63–64. The coefficient field is \(\mathbb F_2\), but the space is required to be integrally oriented. The sought invariant is the Witt class of its nonsingular middle-dimensional bilinear pairing. The note preserves these hypotheses. The question's surrounding discussion explicitly distinguishes the unoriented real-projective-space examples.

The [2012 characteristic-two paper](https://faculty.tcu.edu/gfriedman/papers/2-Witt3.pdf), Theorem 1(4), indeed leaves an ambiguity in positive dimensions congruent to two modulo four. It separately settles dimension two. That older source cannot by itself justify a current open-status claim.

## Original theorem and convention match

In [Goresky–Pardon, Wu numbers of singular spaces](https://www.math.ias.edu/~goresky/pdf/Wu.jour.pdf), §2.1 defines orientability using the regular stratum. Section 8.1 defines local orientability through orientability of links; the corollary in §8.3 states that orientability implies local orientability. Section 10.1 uses the mod-two lower-middle-perversity link condition required here. Thus no coherent orientation of a family of link bundles is an extra hypothesis.

The corollary in §10.2 gives the vanishing odd middle Steenrod operation, and §10.5, Theorem A, with its proof in §10.7, gives vanishing oriented Witt bordism in dimensions \(4j+2\). I inspected the original printed formula on p. 339 and the relevant surrounding text. The operation belongs to intersection homology; the note has not substituted an ordinary-cohomology argument.

There is one convention worth making explicit when reading the old paper: §2.4 generally works with normal connected pseudomanifolds and records its normalization reduction. The later sources below explicitly identify the resulting computation with the conventional oriented Witt bordism groups, so the status conclusion does not depend on silently extending a theorem from normal spaces.

## The proposer's later correction is decisive

I checked §5.2.1 and the complete footnote 14 on manuscript p. 28 of Friedman's [Stratified and unstratified bordism of pseudomanifolds](https://faculty.tcu.edu/gfriedman/papers/stratwitt.pdf), dated 11 May 2015. The main text attributes oriented mod-two Witt bordism to Goresky–Pardon §10.5. The footnote expressly identifies the earlier correction's unresolved \(4k+2\) case and acknowledges that its solution and the complete computation already appeared in Goresky–Pardon. The adjacent discussion again states that oriented spaces are locally orientable and identifies the bordism theories. I also visually inspected that footnote.

This resolves the apparent conflict between the older open statement and the earlier theorem through the original proposer's own explicit acknowledgment.

## Later corroboration and implication for the pairing

The author-hosted [Singular Intersection Homology manuscript](https://faculty.tcu.edu/gfriedman/ihbook.pdf), printed p. 676, states the full oriented coefficient groups as \(\mathbb Z\) in degree zero, \(\mathbb Z_2\) in positive degrees divisible by four, and zero otherwise, with attribution to Goresky–Pardon. I independently retrieved the PDF and checked that exact printed page and formula.

The middle pairing defines a bordism-invariant bilinear Witt class, as described in the original problem and the characteristic-two correction. Since the source bordism group in dimension \(4j+2\) vanishes, every such class is zero. The direct odd-square argument in the status note is consistent: zero self-pairings make the nonsingular form alternating, and a nonsingular alternating bilinear form over \(\mathbb F_2\) is hyperbolic. No quadratic refinement or Arf-invariant assertion is needed.

## Disposition

The reviewed source-status note is suitable for a draft PR marked **already_solved**, with the historical attribution and orientation qualifications retained. No required correction was found. The upstream open label has been superseded by the proposer's later clarification, and this project should not count the answer as a new mathematical resolution.
