# A missing hypothesis, not a resolution of the published conjecture

## Two different statements

The current public dataset record for ID 30002003 / OWR-11580-009 asks, without any completeness or closed-orbit restriction, whether equality of stringy and ordinary Euler characteristics detects smoothness for every locally factorial spherical variety. Its full statement was recovered by an exact-ID filter, with a unique result and no truncated cells. The 126-byte UTF-8 statement's SHA-256 is 6e964d979f65113b1582de96738094b9042e96d116451d2b5a7f5c54955074c6, exactly matching the existing descriptor. The problem webpage itself remained inaccessible.

Batyrev–Moreau Conjecture 6.7 adds that every closed G-orbit is projective, and also proposes the inequality e_st>=e. The original short OWR discussion suppresses this condition in its concluding conjectural sentence, after explicitly using it for the horospherical theorem. The fully written paper is therefore essential to interpret the intended mathematical conjecture.

## Literal-statement counterexample

Let C be the affine hypersurface x1*x2+x3*x4+x5^2=0 in A^5, and put X=C x C*. Take G=SO(5,C) x C*.

- C is a four-dimensional normal UFD with an isolated singularity at its vertex. The explicit normality and Nagata-localization proof appears in PROOFS.md, Approach 4.
- X is a five-dimensional normal locally factorial variety, since its coordinate ring is the Laurent-polynomial extension of that UFD.
- Its dense orbit is horospherical and therefore spherical. The action is by the specified connected reductive group over C.
- C and X are Gorenstein and log terminal. Blowing up the cone vertex has the single discrepancy 2; taking the product with C* preserves it.
- X is singular along {0} x C*.
- The ordinary Euler number of C* is zero. The product resolution gives e_st(X)=e_st(C)e(C*)=0 and e(X)=e(C)e(C*)=0.

Thus equality does not detect smoothness in the class literally stated by the dataset. No numerical experiment is needed for this conclusion.

## Why this does not disprove the published conjecture

The unique closed G-orbit of X is {0} x C*, which is not projective. It fails precisely the omitted hypothesis. The affine cone C itself has a projective closed orbit (a point) and satisfies e_st(C)=4/3>1=e(C), in agreement with the published conjecture.

Recommended mathematical label: **literal-source statement disproved; missing-hypothesis correction; qualified conjecture unresolved**. Avoid labels such as “Batyrev–Moreau conjecture solved,” “new counterexample to the spherical smoothness conjecture,” or “general criterion disproved.” This source correction is not presented as an original geometric discovery.

The result must pass a fresh independent audit before any publication or queue promotion. This packet makes no remote changes.
