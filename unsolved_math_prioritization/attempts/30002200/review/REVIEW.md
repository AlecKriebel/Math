# Independent review: sharp syzygy bounds for torus actions

PASS: the exact requested sharpness has a credited prior positive answer for every rank r>=5. Recommended disposition is already_solved, 0/5 author turns. This packet reconstructs Matthias Franz's published construction; it does not claim a new solution, minimal dimension, integral coefficients or positive-characteristic result.

The frozen author packet is bound by FINAL_SOURCE_MANIFEST SHA256 2b15a00aeb0addb5650793dc8ce1783d4e1416b9181d99bea7fe9edaa96af324, backed up at 5ba83eccde1e5a5655d199fc3abb47a277f82b31.

## Source match

The original OWR pages 2955–2956 were visually inspected together with the surrounding rank and rational-coefficient setup. The question asks whether the nonfree bound is sharp for torus ranks at least five. The report's undeclared n is correctly interpreted using the primary Allday–Franz–Puppe Corollary 1.4 and Proposition 5.12, which explicitly say r/2. It is not a manifold-dimension parameter.

Franz's corrected 2023 version of Big polygon spaces states Proposition 5.1 for odd equilateral rank and Corollary 5.3 for arbitrary rank with zero-length sphere factors. Its coefficient convention is every characteristic-zero field, so Q is directly covered. The 2020 Franz–Huang general theorem and its own characteristic-zero convention were checked as corroboration, not used to replace the needed proof with a broader unreviewed classification.

## Geometric realization

For the equilateral odd rank, the sum map on the product of three-spheres is a submersion on its zero set. A nonzero z coordinate permits arbitrary complex u variation; when all z vanish, a nonzero annihilating real functional would force an odd number of signed collinear unit vectors to sum to zero, impossible. Compactness, smoothness and orientability follow. The pathwise scaling argument proves connectedness without asserting a continuous global choice of phases or a deformation retraction.

The point with all u zero and all z equal to one has trivial stabilizer, so the action has the requested effective torus rank. Stabilizers are coordinate subtori; orbit skeletons are semialgebraic and satisfy the stated finiteness and local topological hypotheses. The even-rank example is precisely an extra S3 factor times the odd example. Its zero length is generic and permitted; a small positive replacement lies in the same chamber if desired. No additional almost-free or dimension restriction is inserted.

## Relevant published proof chain

I read the equilateral portions of Lemmas 3.1–3.2, the geometric cycle definitions, Lemmas 4.2, 4.4–4.5, Proposition 4.6, the Koszul calculation, corrected Proposition 5.1, Lemma 5.2 and Corollary 5.3. The source's literal sign/minimum wording is not inherited blindly: the displayed local quadratic form independently has exactly 3|J| negative directions and a one-dimensional critical-circle kernel. The angular form splits into the common direction and its signed-orthogonal hyperplane, giving the claimed signature. The character argument then distinguishes the negative-bundle orientations at distinct critical strata and kills the Morse boundary maps over Q. This verification is restricted to the equilateral case and makes no unsupported use of the unweighted function for general lengths.

The equivariant inclusion map has the stated Euler-class coefficients and shuffle signs. Its kernel and cokernel are the required Koszul syzygies plus free summands, and equivariant duality gives the short exact sequence. The corrected a=b=1 shifts are 3m and 3m+3. The potentially exceptional free extension at r=5 has shift differences 1 and 4, not 2, agreeing with AFP Lemma 2.4.

The exact-order conclusion also follows without any grading-sensitive splitting: at the homogeneous maximal ideal the left nonfree summand has depth m and the right has depth at least m+2. The depth lemma and the localized syzygy criterion give order exactly m and nonfreeness. The Koszul indices used for r>=5 are strictly below the free terminal index. Standard equivariant duality, regular-sequence/Koszul exactness and localized depth criteria remain explicit credited foundations, not re-proved topology from finite tests.

For the extra circle acting on S3, the Borel sphere bundle of 1 plus the universal complex line has zero Euler class and a free two-summand equivariant cohomology module. Equivariant Künneth and faithful polynomial extension preserve the exact order. Failure of the next regular sequence is retained; one does not incorrectly infer the order solely from depth at the larger full maximal ideal. Thus every odd and even requested rank is covered.

## Reproduction and conclusion

All frozen file bindings and four primary PDF hashes verify. The 358,064 author controls replay byte-exact. An independent SymPy checker adds 983 exact controls for angular-Hessian characteristic polynomials, Koszul signs, parity and corrected shifts. These supplement the reviewed all-rank construction and published theorem; they do not prove topology by finite enumeration.

The answer to the original sharpness question is yes, already supplied by Franz's big polygon spaces. Publish as a credited prior resolution at zero author turns, with the narrow source cautions and correction history retained. No unresolved mathematical gap remains within this exact existence/sharpness request.
