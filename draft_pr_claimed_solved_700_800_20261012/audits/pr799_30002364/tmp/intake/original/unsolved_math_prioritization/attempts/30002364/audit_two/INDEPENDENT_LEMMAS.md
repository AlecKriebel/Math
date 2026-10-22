# Independent mathematical review: CM reduction, problem 30002364

Date: 6 October 2026. This review uses the immutable author packet with SHA-256 `32f5ec9f310f62566906cf6b0ff4a1e8cef5a6e9442ecb995c91525a1fb9879e`. The finite checker was independently written using permutations of the four roots and actual prime cosets. It does not import the author's checker. No first-audit report was read before the mathematical assessment.

## 1. Realization and primitivity

The roots of the Eisenstein polynomial X^4-6X^2+3 are ±a, ±b, where a^2=3+sqrt(6), b^2=3-sqrt(6), and ab=sqrt(3). If sqrt(3) belonged to Q(a), the latter would be Q(sqrt(6),sqrt(3)). Writing a=u+v sqrt(3) over Q(sqrt(6)) forces uv=0. The resulting proposed squares have norms 3 or 1/3, neither a square in Q. Thus the real splitting field L has degree eight. Its displayed automorphisms act on (a,b,-a,-b) as r=(0123) and s=(13), generating D4. Since L is totally real, adjoining i gives the degree-sixteen Galois CM field E=L(i), with group D4×C2 and central conjugation c.

Every choice of one embedding from each conjugate pair is a realizable CM type: the analytic construction on an O_E-lattice is polarizable. For example, a purely imaginary element with the required signs exists by real approximation in L; clearing denominators makes the trace alternating form integral on the lattice. CM descent then places the variety and its endomorphisms over a number field. These existence and descent steps agree with Milne's CM notes, Propositions 3.12 and 7.9. They impose no ordinarity hypothesis.

The matrix of all conjugates of the centered type has rank eight. Consequently its Mumford–Tate torus has dimension nine and equals the torus with x_h x_ch independent of h. Its sixteen coordinate characters are pairwise distinct. The centralizer on H^1 is exactly E, and Hodge endomorphism comparison gives End^0(A)=E. The field contains no nontrivial idempotents, so A is simple. This proves primitivity rather than presupposing it. Independently, the checker finds both left and right stabilizers of the type trivial; the reflex field is E.

## 2. Every power has only Lefschetz Hodge classes

Over a coefficient splitting field, H^1(A^n) contains n copies of each embedding character. A monomial with multiplicity difference d_h=m_h-m_ch has centered weight M d. Since det M=256, vanishing against all rational Hodge cocharacters forces d=0. Equal numbers from each conjugate pair can be matched into degree-two wedges, including matches between different copies of A. These degree-two invariant spaces are scalar extensions of rational (1,1) classes; the Lefschetz (1,1) theorem identifies them with divisors. Taking invariant subspaces and multiplication-map images commutes with coefficient extension, so the spanning statement descends. This proves the required statement for every n, not merely for A.

## 3. The chosen local place and potential good reduction

Modulo 5 the polynomial factors as (X^2-4)(X^2-2), while i reduces to 2. Choose the prime with a reducing to 2. Then sqrt(6) reduces to 1, and b has degree two with fifth power -b. The polynomial discriminant 2^10 3^3 excludes ramification at 5. Thus the actual decomposition group is D={1,s}, not a conjugation-containing subgroup. There are eight primes of E over 5, all of local degree two.

After adjoining definitions of all E-endomorphisms, extend the number field to obtain good reduction above this prime. Milne's Proposition 7.12 supplies this potential-good-reduction step; it is legitimate for the original problem, which works at a prime of Qbar. The normalized slopes do not change on further finite extension. The maximal-order action descends and specializes faithfully.

## 4. Orientation of the formula

Fix P with stabilizer D. Primes tP are indexed by right cosets tD. For the embedding h and the prime tP, h(pi) has the same normalized valuation as pi at h^{-1}tP. The set of embeddings sigma carrying h^{-1}tP to P is exactly D t^{-1}h. Therefore

    slope(h(pi),tP) = #(Phi intersect D t^{-1}h)/|D|.

This is precisely the averaging formula from Milne 2001, Appendix A.8, using Phi on H^{1,0}; Milne's CM Theorem 8.1 applies because 5 is unramified and O_E acts. Conrad's primary lecture notes, Theorem 2.1 and Remark 2.2, independently give the same normalized formula and its finite-base-extension invariance:
https://math.stanford.edu/~conrad/vigregroup/vigre04/stformula.pdf

The independent checker forms the actual cosets and counts sigma^{-1}D=h^{-1}tD. It does not assume either the author's displayed N or a left/right averaging identity. Its centered slope matrix has rank four and sixteen distinct nonzero columns. The slopes are 0 six times, 1/2 four times, and 1 six times. In particular the example is not ordinary. Local degree times each slope is integral, so there is no hidden Honda–Tate division-algebra obstruction.

## 5. Geometric endomorphisms, including every extension

Because E acts with rank one on H^1, it is its own centralizer. Frobenius commutes with this action, so pi is an element of E; integrality gives pi in O_E. The Weil property gives pi c(pi)=q.

Suppose h(pi)^m=k(pi)^m for some m>0. Their quotient is a root of unity, so the corresponding columns of valuations agree. Distinctness of all sixteen columns forces h=k. It follows that pi^m has sixteen distinct conjugates and Q(pi^m)=E for every m. The centralizer of Frobenius^m on the sixteen-dimensional l-adic space is therefore E tensor Q_l. Tate's endomorphism theorem, followed by the fact that every geometric endomorphism descends to some finite extension, proves End^0(A_0)=E. Hence A_0 is geometrically simple. No implication from angle rank alone to simplicity has been used.

## 6. Tate classes and descent

A product of Frobenius eigenvalues of total weight zero is a root of unity exactly when its valuation is zero at all primes over 5: away from 5 the eigenvalues are units, and at every archimedean place the weight-zero product has absolute value one. The forward direction is immediate; the reverse is Kronecker's theorem for an algebraic unit.

For a two-element wedge, this criterion says that its centered columns must add to zero. The only such pairs are {h,ch}. Thus the divisor subspace after splitting coefficients consists exactly of these eight pair-wedges, using Tate's divisor theorem. Their products in degree four occupy exactly the 28 basis lines coming from two disjoint conjugate pairs.

The labels {r,r^3,crs,cr^3s} sum to zero as centered columns. They are four distinct labels and contain no conjugate pair. Their degree-four wedge is consequently Tate after finite base extension and cannot be a sum of divisor products. All required root-of-unity orders in a fixed degree can be killed by one finite extension. The fixed subspace and the multiplication image are both defined over Q_l, and formation of each commutes with a finite coefficient splitting extension. Thus a strict containment there proves a strict containment over Q_l. The argument does not claim that an individual split eigenline has a Q_l generator.

An exhaustive check of all 1,820 four-element subsets gives an additional quantitative result. In the author's indexing 0,...,7 for H and 8,...,15 for cH, the only four additional Tate lines are

    (0,2,12,14), (1,3,13,15), (4,6,8,10), (5,7,9,11).

Their set is stable under the full Galois permutation action. Hence, over Q_l for every l different from 5, the degree-four Tate space has dimension 32, its Lefschetz subspace has dimension 28, and the quotient has dimension four. This dimension count is supplementary; a single exceptional line already suffices for the counterexample. It concerns cohomological classes, not numerical equivalence or nonalgebraicity.

## 7. The published rank conflict

Angle ranks of abelian varieties, Remark 3.5, is stated in the context of absolute simplicity and excludes supersingularity. Inspection of the remark and surrounding setup finds no ordinary hypothesis, no trivial-decomposition hypothesis, and no specified distinguished lift. This example satisfies the actual stated setup. The CM field and Frobenius splitting field are both E, so the remark's switch of field letters cannot resolve the discrepancy.

The Shimura–Taniyama formula is compatible with the example. The unsupported inference is preservation of orbit-span dimension under local averaging. Here it changes the centered dimension from eight to four. Restoring the weight direction changes both ranks by one, producing nine and five; a rank convention cannot repair the claimed equality or the stated equivalence of Lefschetz properties.

There is a further explicit check against a proposed choice-of-lift repair. Exhausting all 256 types on E with the fixed oriented local slope function leaves exactly two:

    (-1,-1,-1,1,-1,1,1,-1),
    (-1,-1, 1,1,-1,1,-1,-1).

Both have centered Hodge rank eight. Accordingly, selecting a different type compatible with these same E-action and slope data does not restore rank four. This does not require any claim about canonical lift constructions.

The exact final CCO Proposition 2.1.4.2 and original Dodson publisher PDF were not acquired. Indexed older CCO text has different numbering and is not treated as the final proposition. Thus this review does not claim to have checked those original passages. The necessary formula and hypotheses are instead verified in the independent primary sources above. The mathematical conclusion is that the unrestricted equality in Remark 3.5 is contradicted by this construction; this is an authored correction claim, not evidence of an author-approved erratum, priority, or novelty.

## 8. The literal existential converse

The OWR question asks for a class of characteristic-zero CM varieties. The complete-splitting theorem naturally concerns pairs (A, a prime), and alone should not be advertised as a prime-independent class theorem.

CM elliptic curves supply a literal affirmative class, uniformly at every reduction: every power of such an elliptic curve already has its Hodge classes generated by divisors. To see this, split the two CM characters. A Hodge-invariant monomial on the nth power has equal multiplicities of the two characters and factors into degree-two wedges. The rational descent and divisor identification are the same as in Section 2. Therefore the requested implication holds at every prime because its consequent holds for every member of the class. This elementary answer is not a novel converse theorem.

The author's complete-splitting paragraph remains valuable as a stronger bidirectional statement for the specified pairs. The OWR reflex-field wording and the accessible Sugiyama preprint's Galois-closure wording remain distinct. No unsupported replacement of one hypothesis by the other is made.
