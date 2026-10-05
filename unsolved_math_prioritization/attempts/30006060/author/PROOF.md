# Five scoped approaches to OWR-14298592-014

## Scope and conventions

The question concerns smooth, oriented knot concordance in S^3 x [0,1]. Both braid generators are positive, and both closures have the natural coherent braid orientation. There is no mirror in either input. Write -J for the concordance inverse, namely the mirror with orientation reversed, and D = K # -J. An annulus between K and J is equivalent to a smooth slice disk for D. The standard signature convention here assigns -2 to the positive trefoil.

The primary source is Paula Truöl's contribution, “Notions of braid positivity and knot concordance,” in [Oberwolfach Report 43/2024](https://ems.press/content/serial-article-files/50050?nt=1), pp. 2543–2546, with the pair on p. 2545. The report was published in 2025 and describes a September 2024 workshop. Its affirmative-concordance question is not an assertion of concordance. No minimal-crossing-number claim is made merely from the 18-crossing diagrams.

Put a = sigma1 and b = sigma2. We use four-block words a^p b^q a^r b^s, with exponent tuples (3,3,6,6) and (3,5,3,7). Both induced permutations are three-cycles, hence the closures are knots. Their disk-and-band surfaces have three disks and 18 bands, so Euler characteristic -15 and genus 8.

## Approach 1: Alexander polynomial and Fox–Milnor

Use the reduced Burau matrices

A = [[-t,1],[0,1]], B = [[1,0],[t,-t]].

For a three-braid knot, the Alexander polynomial, up to a Laurent unit, is det(I - rho(beta))/(1+t+t^2). Exact multiplication gives for both inputs

P(t) = 1 - t - t^2 + 6t^3 - 13t^4 + 21t^5 - 29t^6 + 35t^7 - 37t^8
       + 35t^9 - 29t^10 + 21t^11 - 13t^12 + 6t^13 - t^14 - t^15 + t^16.

It is reciprocal, P(1)=1 and P(-1)=-243. Thus Delta_K(t)=Delta_J(t)=t^(-8)P(t) in symmetric normalization. Its degree span is 16, giving g(K),g(J)>=8; the explicit surfaces give equality. The determinant is 243, and both Arf invariants are 1 because the determinant is 3 modulo 8.

For D, Delta_D(t)=Delta_K(t)Delta_J(t)=Delta_K(t)Delta_K(t^(-1)). This is already a Fox–Milnor norm. This necessary sliceness condition therefore gives no obstruction. Equal Alexander polynomials do not assert algebraic concordance or smooth concordance. The verifier computes Burau products independently of the tree calculations below; matching polynomials supply a second calculation of P.

## Geometric matrix certificate used in approaches 2 and 3

Take one homology curve for every consecutive pair of occurrences of a, followed by the analogous curves for b. Set n=p+r-1 and m=q+s-1. There are n+m=16 curves. Denote the a curves by A_1,...,A_n and the b curves by B_1,...,B_m.

The local disk-and-band calculation gives a Seifert matrix V with:

- V_ii=-1;
- V_(A_(i+1),A_i)=1 and V_(B_(i+1),B_i)=1;
- V_(A_p,B_q)=1;
- all other off-diagonal entries zero.

For completeness, consecutive same-column bricks share one positive band, giving a single lower-triangular linking entry. The sole interleaving of different-column brick intervals is A_p with B_q: the last a of block one, last b of block two, first a of block three, first b of block four occur in that order. They give the displayed upper-triangular entry. All other cross-column intervals are disjoint or nested and give zero. This is the positive specialization of Julia Collins's corrected [Seifert-matrix algorithm](https://webhomes.maths.ed.ac.uk/~v1ranick/julia/SeifertMatrix.pdf), Sections 3.1–3.3. The local rectangle rule is also described in Baader's [Positive braids of maximal signature](https://ems.press/content/serial-article-files/44257?nt=1), Section 2. The written local rule, rather than polynomial agreement alone, identifies V with the actual knot.

Let T be the graph with two paths A_1--...--A_n and B_1--...--B_m joined by A_p--B_q. It is a tree. If C is its adjacency matrix, then V+V^T=-2I+C, and write S=2I-C=-(V+V^T). All complete matrices are in results.json. The verifier checks det(V-V^T)=1, as required for a one-boundary-component surface.

## Approach 2: the full Levine–Tristram functions

Lemma. Suppose a Seifert matrix has diagonal -1, and for each edge of a tree exactly one of V_ij,V_ji is +1 or -1, with all other off-diagonal entries zero. Put d=|1-omega| for omega on the unit circle with omega != 1. Its Hermitian matrix

H(omega)=(1-omega)V+(1-conjugate(omega))V^T

is unitarily conjugate to d(C-dI), after choosing a sign gauge for the underlying tree. Consequently its signature and nullity depend only on the adjacency spectrum of the tree.

Proof. The diagonal is -d^2. Each edge entry has modulus d, and opposite entries are conjugates. Starting at a root, choose a unit complex phase at each child so the corresponding conjugated edge entry is positive real d. There is no compatibility cycle because the graph is a tree. This proves the displayed conjugacy. It works even when H is singular. At omega=1 the matrix is zero for both inputs. QED.

For the two trees, exact characteristic-polynomial calculation gives the same polynomial:

C_T(x) = (x-1)^2 (x+1)^2
  (x^6-x^5-6x^4+4x^3+9x^2-3x-1)
  (x^6+x^5-6x^4-4x^3+9x^2+3x-1).

The computation has a short exact combinatorial certificate. If m_k is the number of k-edge matchings of a forest on 16 vertices, then det(xI-C)=sum_k (-1)^k m_k x^(16-2k). Only fixed points and edge-transpositions can appear in a nonzero determinant term. The verifier obtains m_k by the recurrence: either a chosen vertex is unmatched, or is matched to one of its neighbors. It checks identical complete matching-count lists for the two explicit trees, and separately the factorization above can be expanded against the displayed coefficient list.

Likewise det(V-tV^T)=sum_k m_k t^k(1-t)^(16-2k); a matched edge contributes t after including the permutation sign. This formula is independent of the edge orientation and supplies the second Alexander check.

It follows that the signatures and nullities agree at every omega, including Alexander roots. Exact rational LDL decomposition gives inertia(S)=(15,1,0), hence the standard ordinary signatures are both -14.

Concordance caveat: the raw value of a Levine–Tristram signature or nullity at an arbitrary Alexander root need not itself be a concordance invariant. The averaged signature is a concordance invariant, and raw signatures at admissible parameters, in particular prime-power roots of unity, give the usual obstructions. Our stronger equality of the raw functions implies equality of these legitimate concordance obstructions; it is not a claim of universal raw-value invariance. See Conway's [survey](https://arxiv.org/abs/1903.04477), Section 2.4. No numerical signature sampling is used in the proof.

## Approach 3: double-cover linking form

The double branched-cover homology is presented by V+V^T, hence equally by S. The linking form is represented, up to the same global orientation sign, by S^(-1) modulo Z. Replacing both pairings by their negatives does not change the metabolicity conclusion.

Use zero-based matrix indices in this paragraph, and let e_i be the ith coordinate vector. For K take x=e_0 and y=e_8-20e_0. For J take x'=e_0 and y'=e_3-29e_0. Exact rational inversion gives the following orthogonal decompositions:

H_1(Sigma_2(K)) = <x> + <y> = Z/27 + Z/9,
  lambda_K(x,x)=16/27, lambda_K(y,y)=5/9, lambda_K(x,y)=0 modulo Z;

H_1(Sigma_2(J)) = <x'> + <y'> = Z/81 + Z/3,
  lambda_J(x',x')=50/81, lambda_J(y',y')=1/3, lambda_J(x',y')=0 modulo Z.

Here the order of the class of z is exactly the least common multiple of the denominators of S^(-1)z. The orthogonal self-pairings have unit numerators, so the two cyclic factors are independent. Their order product is 243=|det S|, proving they generate the full group. The replay also enumerates all 243 classes in each presentation.

These groups are nonisomorphic (their exponents are 27 and 81). Isotopy would induce a homeomorphism of the double covers, so K and J are non-isotopic, independently confirming the primary report's assertion. But branched-cover homology is not itself a knot concordance invariant.

Indeed the difference form on G=Z/27 + Z/9 + Z/81 + Z/3 is diagonal with entries

16/27, 5/9, -50/81, -1/3.

The subgroup M generated by

(3,0,0,1), (0,3,0,0), (0,0,9,0)

is isotropic. Its three self-pairings are 5, 5, -50, and mutual pairings are zero. Its generators have orders 9,3,9 and are independent by their coordinate supports, so |M|=243=sqrt(|G|). The pairing is nonsingular, hence M=M-perp: it is a metabolizer. Thus the elementary double-cover linking obstruction vanishes. This does not show the two covers are rationally homology cobordant, does not show D is algebraically slice, and does not dispose of Casson–Gordon or correction-term obstructions.

## Approach 4: smooth Floer-derived invariants

Positive braids are strongly quasipositive and fibered. The positive-braid equality gives

tau(K)=g_4(K)=g(K)=8, tau(J)=g_4(J)=g(J)=8,

and [Rasmussen, Theorem 4 and Section 5.2](https://arxiv.org/abs/math/0402131) gives s(K)=s(J)=18-3+1=16. These are smooth-category statements, not formulas for topological slice genus.

Both words are case (C) of Truöl's Garside normal form, with ell=0, two a/b block pairs, and every block exponent at least 3. [Truöl, Lemma 4.11](https://arxiv.org/abs/2108.03674v2) applies and gives

Upsilon_K(1)=Upsilon_J(1)=-(18)/2+2=-7.

Thus the minimal block-pair count in the report's corollary is g+Upsilon(1)+1=2 for each knot. Subtracting these values on D gives zero in all three concordance homomorphisms tau, s and Upsilon(1).

Two tempting reconstruction shortcuts provably do not apply. An L-space knot's Alexander polynomial has nonzero coefficients of magnitude one, whereas P has coefficient -37. Also for a quasi-alternating knot, Upsilon(t)=sigma*t/2 on [0,1]; its initial slope would be -7, contradicting the initial slope -tau=-8. So neither input is an L-space knot or quasi-alternating. The relevant restrictions are [Ozsváth–Stipsicz–Szabó](https://arxiv.org/abs/1407.1795v3), Theorem 1.14 and Section 2's L-space calculation.

The newer [Cheng–Hedden paper, v2, July 2026](https://arxiv.org/abs/2504.13005v2) determines a next-to-top Floer term for positive braids; this is not a determination of their full filtered knot complexes. No full Upsilon, V_i, epsilon, secondary-Upsilon, or involutive-Floer calculation is supplied here. A rank or isotopy invariant from an ordinary homology table cannot silently be promoted to a concordance obstruction. This is the exact remaining gap in this route.

## Approach 5: constructive cobordism and ribbon restriction

Deleting one positive braid letter is an oriented saddle move, namely the local oriented smoothing of that crossing. Reverse such a saddle to insert a letter. Perform the following six moves, written in exponent tuples:

(3,3,6,6) -> (3,3,5,6) -> (3,3,4,6) -> (3,3,3,6)
            -> (3,4,3,6) -> (3,5,3,6) -> (3,5,3,7).

This is an explicit movie through the common word a^3 b^3 a^3 b^6. Begin with the product cylinder on K and attach each of the six oriented one-handles in succession; isotopies put the next crossing into position if necessary. No births or deaths occur. Attaching a one-handle to a connected surface keeps that surface connected, even when the current level link splits. At the end the only boundary components are K and J. The Euler characteristic is -6, so 2-2g-2=-6 gives genus g=3. Therefore g_4(K # -J)<=3.

The verifier checks every word transition and the number of link components at each stage. It also exhausts common-subsequence comparisons under cyclic word rotations and generator interchange and finds maximum common length 15. Thus this restricted deletion/insertion scheme has no better bound. This is not an optimization over all braid equivalences, stabilizations, or smooth surfaces, and does not give any positive lower bound on concordance distance.

By [Baker, A note on the concordance of fibered knots](https://arxiv.org/abs/1409.7646), Lemma 2 and Theorem 3, two distinct tight fibered knots cannot be homotopy-ribbon concordant in either direction, and their difference cannot be ribbon. The hypotheses hold here, and distinctness was independently proved above. Hence D is not ribbon. The theorem does not assert that D is not slice. If an annulus exists, it yields a counterexample to Slice–Ribbon, exactly as noted in the source report.

## Final disposition

Five substantive approaches are complete at the stated scope. The original smooth-concordance problem remains unsolved. The exact retained conclusions are identical Alexander and full signature functions, equal listed smooth homomorphisms, different double-cover groups with metabolic difference linking form, a genus-three upper bound, and a ribbon obstruction. No combination of these proves or disproves a smooth annulus. No novelty, exhaustive literature coverage, or human peer-review claim is made.
