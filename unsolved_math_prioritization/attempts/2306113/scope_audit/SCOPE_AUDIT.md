# Independent mathematical and source-scope audit

Problem 2306113 / AMR-022-6113, associated with Hayman–Lingham Problems 6.112–6.113.
Date: 2026-10-08 UTC.

## Verdict

**Accept the mathematics for each of the two explicitly displayed neighborhood definitions, subject to successful replay of its finite exact certificate. Historical source identification remains unresolved.** No mathematical correction is required in the reviewed proof or supplement.

The witness disproves the proposed universal inclusion for the symmetric definition, and also for the separately specified inner-absolute-value definition. In both cases its center is z, its positive parameter is rho=1/1000, its test point is 999/1000, its polynomial has degree 10, and the comparison function is globally normalized and univalent. This is a genuine interior convolution zero, not a boundary limiting obstruction.

The inspected arXiv rendering contains a malformed definition. Consequently this audit does **not** certify an unconditional resolution of the literal historical problem or identify the proposers' intended correction. Certifying two repairs does not establish that all possible source interpretations have been exhausted. No novelty, comprehensive literature, human peer-review, or proof-assistant verification claim is made.

This audit independently reconstructs the required Taylor coefficients by a different exact formal-series method. It reviews the mathematics and reads both candidate verifiers completely. Bulk all-circle, adaptive-cover, malformed-input, hostile-environment, and optimization-mode replays belong to the separate reproducibility review; the independently executed computation here is described precisely below.

## 1. Reviewed version and trust anchors

Both mathematical documents were read completely. The change from the initial proof to the reviewed version only clarifies the reference to the alternative-definition supplement. The mathematical witness and verifiers did not change.

Reviewed byte identities:

- MANIFEST.json: 2f315877db00b3776fe55ab0e576012874078fd8e2df0fc61fec94ff7ac98c28
- PROOF.md: 71fb7cad064a4e1dd9fa0760f96ad2ff66aecac4cff1c7f156b1c06d536ea640
- ALTERNATIVE_REPAIR.md: 3aeb1fc5c84a8d757cdf96099218c56e51e357c23749fff5b4a51e598467d77f
- COUNTEREXAMPLE.json: 65ddace3d1b7718fee4195027432b440c6f7ba0f12e33d899c0d9839df6eafd7
- verify_counterexample.py: aff03b041039d7cbcddab95d2af02d64df361d4d7911e2f87aa0986b682fa675
- verify_alternative.py: d6195d9189972b3f3aca70cf7c41ea1e59828c4c1e3af98b35290def5a7f09f1

These hashes were independently recomputed from the reviewed files. A published copy must be checked against an independently supplied pin, rather than being trusted merely because it carries its own manifest.

## 2. Source identity and exact quantifiers

The primary compilation's Problems 6.112–6.113 distinguish the Hadamard dual of the normalized univalent class from the class of starlike functions. The target parameter constraint is |x|<=rho<=1, with gamma=(1+rho)^(-2). The choice x=0, rho=1/1000 is therefore admissible. Problem 6.112 supplies the center-case question. The adjacent update reports the editors' historical knowledge, not a verified 2026 literature status. [Hayman–Lingham, arXiv v2](https://arxiv.org/html/1809.07200v2).

The definition in that HTML and the rendered PDF page has an unmatched delimiter in its second summand. I independently inspected both the HTML formula and the relevant PDF page images. This is not merely an OCR ambiguity. The mathematical statements reviewed here explicitly replace that malformed string by the following well-defined alternatives, writing H=g-f:

1. Symmetric: (|H'-H/z|+|H'+H/z|)/2 < delta throughout the disk.
2. Inner-absolute-value: (|H'-H/z|+|H'+|H|/z|)/2 < delta for 0<|z|<1, with continuous extension at zero.

The [publisher record for Sheil-Small and Silvia's 1989 article](https://link.springer.com/article/10.1007/BF02820479) confirms the article identity and displays subscription access. Its full text was not obtained, and this audit attributes no corrected definition to an uninspected article page.

The later [published 2019 chapter](https://link.springer.com/chapter/10.1007/978-3-030-25165-9_6) was also located, but its relevant text was not available through the publisher's accessible page. The legitimate [Google Books preview](https://books.google.com/books?id=lxCuDwAAQBAJ&printsec=frontcover) did not expose the needed formula in the inspection performed; a subsequent book-search request returned HTTP 429, after which that route was stopped. Unverified search snippets and third-party transcriptions are not accepted as resolving the source defect.

The earlier [Janowski partial-result proof](https://github.com/AlecKriebel/Math/blob/1f302bc62c5492ef45a3b5278fec6dfbd01ed0c3/unsolved_math_prioritization/attempts/2306111/submission/FULL_PROOF.md) was inspected through the supplied exact-commit retrieval. Its problem is a coefficient neighborhood with a starlikeness target. It neither supplies the missing definition nor contradicts this Hadamard-dual counterexample. This comparison is a scope check, not a comprehensive duplication search.

## 3. Global univalence and inverse branches

Let K_u(z)=z/(1+uz)^2, with |u|=1. Its denominator is nonzero on the open unit disk. Clearing denominators in K_u(z)=K_u(w) gives

    (z-w)(1-u^2 zw)=0.

The second factor cannot vanish for z,w in the disk. Thus K_u is injective there.

For the proposed inverse, set s=sqrt(1-4uy), using the principal square root. On the complement of the ray {t/u:t>=1/4}, its argument avoids the nonpositive real axis, and Re(s)>0. Hence

    J_u(y)=(1-s)/(u(1+s))

is holomorphic, has modulus below one, and has nonzero denominator. Direct substitution gives K_u(J_u(y))=y. Conversely (1-uz)/(1+uz) lies in the right half-plane for |z|<1, so it is exactly the principal square root appearing in J_u(K_u(z)). This verifies the inverse identity without a branch-sign assumption. Therefore the claimed slit image is exact.

For 0<q<1 the scaled slit domain q Omega_u excludes the larger ray starting at q/(4u). Thus q Omega_u is a subset of Omega_u. The inclusion direction in the proof is correct: multiplying the image by q moves the slit endpoint toward zero and removes more points. Consequently J_u(qK_u(z)) is defined everywhere on the disk, maps into the disk, and is injective. Its derivative at zero is q.

The three displayed parameters have modulus one exactly, and the two q parameters are strictly between zero and one. Each successive input therefore lies in the domain required by the next map. Composing the two disk self-maps and K_u3 gives an injective holomorphic function; dividing by the nonzero number q1 q2 preserves injectivity and normalizes its derivative to one. This establishes F in S globally. It does not infer univalence from a coefficient list, a sampled image, or a numerical differential equation.

## 4. Taylor coefficients, complex normalization, and an independent reconstruction

The inverse relation K_u(Y)=W is equivalently

    Y=W(1+uY)^2,  Y(0)=0.

Lagrange inversion gives the coefficient of W^n as

    (1/n) binom(2n,n-1) u^(n-1)
      = (1/(n+1)) binom(2n,n) u^(n-1).

Thus the Catalan indexing in the candidate is correct, beginning with 1,2,5. All coefficients through degree 10 are Gaussian rational. Compositions may be truncated modulo z^11 because every inner series has constant term zero.

To avoid relying solely on that same coefficient formula, the accompanying verify_independent_algebra.py performs a different reconstruction. It implements rational-function power series using a reciprocal recurrence. It solves Y=W(1+uY)^2 by ten formal fixed-point updates: multiplication by W, whose constant term is zero, improves the coefficient agreement by at least one order per update. It then verifies the exact fixed-point identity and K_u(Y)=W modulo z^11. The second slit is solved after substitution of the first one, and the final K map is evaluated as a rational-function series. No candidate code is imported and no Catalan formula is used by this independent program.

The independently executed result is PASS. It reproduces the complete degree-10 coefficient-array SHA-256

    6e7dec6a524075e5626c60ef1adcc3e6655362e324825ea57d84a606117185f8.

It also reproduces exactly the stated real part of L, verifies Re(L)>2517/2500, and computes its nonzero imaginary part. The full rational values are in INDEPENDENT_ALGEBRA_RESULT.json. In particular L is not silently replaced by its real part, absolute value, or complex conjugate.

With H=-h/L, exact multiplication gives (H*F)(r)=-r. Therefore (g*F)(r)=0 exactly when g=z+H. Only coefficients through degree 10 occur because h is a polynomial. There is no uncontrolled analytic tail in this identity. Since Re(L)>0, division by L is legitimate; since r=999/1000, the zero lies strictly within the forbidden punctured disk. The independent code verifies this cancellation directly using the full complex scalar.

## 5. Symmetric all-circle certificate

For P=h'+h/z and M=h'-h/z, the angular frequencies are n-1 and their coefficients are respectively (n+1)c_n and (n-1)c_n. The reverse triangle inequality therefore gives the half-sum an angular Lipschitz bound

    (1/2) sum ((n+1)(n-1)+(n-1)^2)|c_n|
      = sum n(n-1)|c_n|.

Replacing each modulus by |Re(c_n)|+|Im(c_n)| is conservative. Independent rational arithmetic reproduces 6004273/500000 for the resulting bound.

The rational parametrization v(t)=(1-t^2+2it)/(1+t^2), -1<=t<=1, traces exactly a semicircle. The angular derivative is 2/(1+t^2), at most 2. For a uniform t-grid of spacing 1/8192, choosing a nearest grid point gives t-distance at most 1/(2*8192), hence angular distance at most 1/8192. Its negatives cover the other semicircle. The endpoints overlap and introduce no gap. The count 32770 includes harmless repetitions.

The modulus enclosure implemented by the candidate is valid. If k initially is the integer square root of floor(s^2 X), then either k/s already bounds sqrt(X), or incrementing k once does. Checking k^2/s^2>=X certifies the upper bound. The increment never needs to exceed one, and the enclosure error is below 1/s. Evaluating real and imaginary parts and their squared norm rationally avoids cancellation or floating-point rounding errors.

The code's polynomial arrays have exponents n-1, including their zero constant terms. Thus they evaluate P and M, rather than accidentally evaluating h or zP. Combining the recorded rational grid maximum with the proved covering radius yields

    500679451/500000000 + (6004273/500000)/8192
      = 513446291949/512000000000 < 251/250.

The arithmetic identity and strict comparison were independently executed here; the 32770-point extremum traversal is left to the separate full replay.

The passage from the circle to the disk is valid. For any fixed z, phases alpha,beta of modulus one can align P(z) and M(z), giving

    |P(z)|+|M(z)| = max |alpha P(z)+beta M(z)|.

For each fixed pair of phases the expression inside the modulus is an analytic polynomial. Its maximum on the closed disk is bounded by its boundary maximum. Taking the maximum over the phases preserves the bound; the phases need not vary analytically with z.

Finally symmetric homogeneity gives s_H=s_h/|L|. Since |L|>=Re(L),

    s_H < 2510/2517 < 1000000/1002001.

The exact difference between these last two fractions is 1977490/2522036517>0. This is a uniform strict margin, stronger than the required pointwise open-disk inequality.

## 6. Alternative repair: direct post-scaling disk verification

The alternative expression is not assumed to be subharmonic or invariant under multiplication of H by a unit scalar. Both distinctions matter. Its certificate correctly operates on the already normalized complex polynomial H=-h/L, rather than dividing the unscaled alternative expression by |L|.

Writing q=H/z and z=r exp(i theta), the identity

    |H(z)|/z = exp(-i theta)|q(z)|

is exact for r>0. At r=0, H'=q=0; all terms tend to zero uniformly in theta. This justifies the continuous extension used in the cover.

For one coefficient d_n, the first term H'-q has radial derivative bound (n-1)^2 |d_n| r^(n-2). The second term has radial derivative bound [n(n-1)+(n-1)]|d_n| r^(n-2). Halving the sum gives n(n-1)|d_n| r^(n-2), precisely the proposed B_r.

For the angular bound, the first term contributes (n-1)^2 |d_n| r^(n-1); H' contributes n(n-1)|d_n| r^(n-1); and exp(-i theta)|q| contributes at most [1+(n-1)]|d_n| r^(n-1). Halving the total gives (n^2-n+1/2)|d_n| r^(n-1), precisely B_theta. Reverse triangle inequalities supply these estimates even where an absolute-value argument vanishes. The proof does not require differentiability of a modulus at zero.

Replacing |d_n| by the rational l1 upper bound is again conservative. Replacing angular coordinates by t multiplies the bound by at most two. On a rectangle, changing r and then t from its midpoint gives the stated sum of radial and angular half-width errors; using the maximum radius r1 makes both constants valid along the entire path.

At a rational midpoint, the unit vector and its conjugate are exact Gaussian rationals. The upward enclosure Q for |q| differs from it by at most 10^(-10). Multiplying that discrepancy by the conjugate unit vector changes the second outer modulus by at most the same amount. Adding half that error to half the two upward modulus bounds is the correct safe direction.

The initial two closed rectangles parameterize the entire closed disk. Bisection replaces a rectangle by two closed children whose union is the parent. Every node is either split or accepted with a strict bound, and a budget failure rejects instead of accepting. Therefore an exhausted stack of certified leaves proves universal coverage, including the origin, rectangle edges, and duplicated semicircle endpoints. No boundary-only maximum principle is used for this nonanalytic expression.

The reported 4050 visited rectangles, 2026 leaves, and depth 21 are consistent with two full binary trees: visited=2*leaves-2. The positive recorded minimum margin is a rational certificate datum; the separate replay must reproduce these values. Once that traversal passes, the alternative inequality holds with the same strict gamma threshold everywhere, and the already verified convolution zero proves the alternative counterexample.

## 7. Center equivalence and separation from earlier questions

Under the symmetric definition, the full parameterized universal assertion is indeed equivalent to the center assertion. One direction uses x=rho=0.

For the other, assume the center assertion and take a normalized difference h with s_h<1. For F in S define A(w)=(h*F)(w)/w, analytically extended with A(0)=0. If |A(w0)|>1, the complex scalar lambda=-1/A(w0) has modulus below one, so z+lambda h remains in the center neighborhood, while its convolution with F vanishes at w0. This contradiction proves |A|<=1. Schwarz's lemma then gives |A(w)|<=|w|. Analyticity is legitimate because Hadamard products of two series analytic in the unit disk are analytic there.

For the general perturbation scale gamma, apply that conclusion to h/gamma. The center contribution is F(xw)/(xw), interpreted as 1 at x=0. The classical normalized-univalent growth theorem bounds its modulus below by (1+|xw|)^(-2), which is at least gamma. The perturbation contribution has modulus at most gamma|w|<gamma. Thus no cancellation is possible. The growth theorem is a correct imported dependency of this auxiliary equivalence, not a dependency of the explicit counterexample.

This balanced-scaling argument is not automatically transferable to the alternative definition; the supplement neither needs nor claims that transfer. The explicitly certified alternative witness already lies in the radius-gamma center neighborhood and therefore also in the radius-one center neighborhood.

Finally, starlikeness and membership in the Hadamard dual are different conclusions. The counterexample can be starlike and still have a vanishing convolution with a member of S. Replacing this dual target by a starlikeness target, replacing the pointwise Sigma neighborhood by a weighted coefficient neighborhood, or replacing the whole class S by a Koebe/close-to-convex test family would change the question. None of those substitutions is used in the accepted counterexample.

## 8. Acceptance conditions and remaining gap

The explicit mathematical constructions and analytic error bounds pass this adversarial review. The independent algebra reconstruction also passes. Final computational acceptance requires the separate finite-certificate replay to succeed on the pinned version; this audit does not claim that its algebra-only execution reproduced the grid or rectangle traversals.

The outstanding historical gap is precise: obtain an authorized primary definition, an inspected authoritative correction, or a reliable primary reproduction identifying which neighborhood was intended. Until then the accurate public mathematical description is a counterexample for two explicitly stated repairs of the malformed definition. The witness is valuable as proved mathematics without converting that conditional identification into an unconditional historical resolution.

No source documents, copied source passages, source datasets, personal information, or private coordination material are included in this audit or its independent algebra artifacts.
