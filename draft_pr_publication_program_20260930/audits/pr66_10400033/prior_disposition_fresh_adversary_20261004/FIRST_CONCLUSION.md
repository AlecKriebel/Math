# FIRST_CONCLUSION — independent source-first mathematical disposition

Sealed at 2026-10-04T17:08:40.426035+00:00 before reading ROOT/sibling reports, historical dispositions, or the proposed attribution packet. No new proof search and no promotion authority.

## Exact claim and inputs

Authentic candidate: 9121 bytes, SHA256 fc2be9794873073e6482e8dfe93ccfd6c5d6f8674c2058ba0a8fc900d906d698. Authentic source record: 3676 bytes, SHA256 075059240df7ba3bfac89aaf96f8f9fb176b12b61e6e7f7fdd1f8e1d93a8d4bc. The supplied PR head is 78f4a7fadac0fd24e147a617956cb409eb6a579e; this phase does not independently inspect the remote head.

The real Ohtsuki primary target, printed 403 and 405 / PDF 31 and 33, specifies a primitive degree-three invariant, mirror odd, right trefoil 1, integral on classical knots. For any classical knot having an n-crossing diagram, the requested inequality is |v3(K)| <= floor(n(n^2-1)/24). No positivity or crossing minimality restriction occurs.

## Decisive primary relation

I read Fiedler–Stoimenow, New knot and link invariants, the actual author PDF bytes 268871, SHA256 193dfd4c993f2337ba17b48f524d8c71333f8717d520ba299f7b76a8cbd324b7, text and rendered pixels printed 4–8. Section 2 supplies ordinary classical Gauss diagrams; the page 5 paragraph explicitly counts distinct unordered crossing choices, taking one matching permutation where a configuration has automorphisms. Formula (1) has two disjoint three-crossing configuration families (the all-linked triangle and a specified two-linked configuration), plus a two-crossing linked-pair term whose weight is (wp+wq)/2. Each crossing writhe is +/-1, so each triple contributes absolute weight at most 1; each pair term has absolute weight at most 1. Disjoint triple families are bounded by one binomial(n,3), rather than two. The pair family is bounded by binomial(n,2).

The first display of section 3.2, printed 7, bounds |vt3| by binomial(n,2)+binomial(n,3). This is stated for a diagram with n crossings. Definitions of positive/reduced diagrams on page 6 concern Theorem 3.1, not this separate bound.

Remark 3.1, printed 6, gives vt3=4v3=-(V''(1))/3-(V'''(1))/9 and identifies v3 with the Polyak–Viro formula. Independently downloaded Polyak–Viro's original primary PDF, Theorem 2, printed 448 / PDF 4, explicitly normalizes v3 to right trefoil +1, left trefoil -1 and unknot 0. This resolves the factor and sign convention in favor of the exact target normalization. The sign could not affect the absolute bound in any event; an unchecked scale factor would.

Consequently, for every classical n-crossing diagram,

    |v3| <= [binomial(n,2)+binomial(n,3)]/4
         = [n(n-1)/2+n(n-1)(n-2)/6]/4
         = n(n-1)(n+1)/24.

Because the target v3 is integral, this gives precisely the floor in the target. At n=0,1,2 the bound and integrality force v3=0 (with the empty-diagram case also the unknot). This deduction covers all small cases without needing the stronger page 8 statement.

## Stronger claim, candidate relation, and boundary

The final paragraph before section 4 on printed 8 asserts that the standard T(2,2r-1) diagram maximizes v3 through crossing count 2r. Mirroring extends its maximum statement to |v3| for ordinary diagrams. Using the target's stated torus value, for even n=2r this gives |v3| <= n(n-1)(n-2)/24. It is stronger than the candidate's even bound n(n^2-4)/24 by n(n-2)/8 for n>=4. I do not independently certify the source's diagram uniqueness assertion or reconstruct its omitted stronger argument; neither is required for the exact-target implication from page 7.

The candidate P/T table agrees with printed source equation (3) after converting under-to-over to the candidate's over-to-under arrows and applying cyclic rotations. The graph correspondence and tournament square identity in the candidate are correct as algebraic deductions, conditional on the imported subset-counting formula. Polyak–Viro's wording about representations alone can be read ambiguously concerning automorphisms, but the decisive Fiedler–Stoimenow page 5 counting paragraph explicitly supplies the subset convention. My own finite program confirms the cyclic conversion, directed path/cycle correspondence, and arithmetic for n=0..12; that finite evidence is not the universal proof.

The candidate therefore supplies an alternate derivation of an already established target inequality. Neither estimate novelty nor proof novelty is established; no new theorem or earliest-priority claim follows from the candidate or from this review. An attributed prior-result resolution of this one target is mathematically supported. The current author file labels its version February 1, 2002 and its first version December 9, 1996, and says it is a minor update of the printed version. I have not obtained or read the exact 2000 printed chapter body. Those facts do not certify that this exact bound occurred in 1996 or 2000, and do not certify earliest priority. Attribution must distinguish the verified 2002 author-version body from bibliographic printed-chapter dates.

No other individual was contacted; sources were retrieved/read only. Copyright PDFs, extracted source text, and source page images are private outside Git. No original PR, Git/index/ref, editor, tracker, DOI, release, or upload mutation occurred.
