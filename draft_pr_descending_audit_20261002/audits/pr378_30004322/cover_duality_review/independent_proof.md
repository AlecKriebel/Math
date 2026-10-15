# Independent curve-cover and incidence-duality derivation

Prepared independently before candidate, previous-audit, root-output, or sibling-output exposure. The assignment itself named the cover/duality mechanism and requested a possible 9q-line family. Those task labels are the sole pre-source exposure. This is a family result, not a proof of the general conjecture or a novelty claim.

## Source gate and exact target

At 2026-10-03 04:25 UTC, literally first opened https://ems.press/content/serial-article-files/46833, the primary Oberwolfach Report 53/2019, and read/rendered/viewed printed pages 3295, 3296, 3297 (PDF pages 25, 26, 27). The conjecture at printed 3297 concerns the singular set of a line arrangement and the maximum number of its points on **any projective line**. Printed page 3272 also defines the multipoint invariant by reduced irreducible curves meeting the point set. This gate preceded all candidate and prior-output reads.

Precise working claim: over C, let A be a finite collection of distinct projective lines, regarded as a reduced divisor, and let Z be its nonempty finite set of points incident with at least two components. Set K=max over projective lines M of |M intersection Z|. Is epsilon(P2,O(1);Z)=1/K? Here epsilon is the infimum of deg C / sum over p in Z of mult_p C, over reduced irreducible curves with positive denominator. Distinctness and reduction exclude repeated-line singular-locus pathologies; one or zero components have empty Z and the formula is undefined. Concurrent arrangements are permitted. No statement in this audit extends the claim to positive characteristic.

Allowing reduced reducible curves does not change the infimum: degrees and multiplicities add, and the quotient is a denominator-weighted average of the quotients of components with positive denominator, with an additional nonnegative degree contribution from components missing Z. The same observation handles effective nonreduced divisors, although they are outside the defining infimum.

## Fractional-cover lemma, including exceptional support curves

Let F={M_1,...,M_s} be any finite collection of projective lines, and choose nonnegative real weights w_j with sum over j containing p of w_j >=1 at every p in Z. Write T=sum w_j. For every reduced irreducible C different from every M_j with w_j>0, local intersection multiplicity I_p(C,M_j)>=mult_p C, and Bezout gives

    sum_p mult_p C <= sum_j w_j sum_{p in M_j intersection Z} mult_p C
                      <= sum_j w_j deg C = T deg C.

If C equals a supported line, its quotient is 1/|C intersection Z| >=1/K. Hence epsilon >=min(1/T,1/K). A line attaining K has quotient exactly 1/K. Consequently **a cover of total weight at most K proves the desired equality**. A cover of weight greater than K merely gives a weaker lower bound; it is neither a counterexample nor evidence that no stronger geometric argument exists.

If arbitrary curves are used as cover objects, one must require no common component and use their degrees as costs. The above line-only certificate avoids that extra bookkeeping. It does not replace the unknown curve C with an incidence vector unsupported by multiplicity bounds.

## Exact finite primal and dual

For a chosen finite line set F, put B[p,j]=1 if p lies on M_j and 0 otherwise. The covering primal and its dual are

    min 1^T w,  B w >=1, w>=0;
    max 1^T y,  B^T y <=1, y>=0.

Weak duality follows from 1^T y <= y^T B w <=1^T w. Thus rational feasible weights with equal total prove the exact optimum without any numerical LP solver. Standard finite LP duality supplies existence of optimum certificates when the set covers Z, but none of the equality results below requires invoking it.

There are two different domains: tau_comp uses only arrangement components; tau_all permits arbitrary auxiliary lines. They satisfy tau_all<=tau_comp. For |Z|>=2, tau_all is a finite LP over distinct pair-lines of points in Z. Every line containing at least two points is a pair-line; a line containing one point has its singleton column dominated by a pair-line through that point and any other point, so its weight can be transferred without increased cost. Empty columns are dispensable. For |Z|=1, one line suffices. The all-line dual must therefore be checked on **every distinct pair-line**, rather than only arrangement components. The uniform dual y_p=1/K shows tau_all>=|Z|/K.

## Exact infinite 9q-line family

For each integer q>=1, set n=3q and let mu_n be the complex nth roots of unity. Take the 3n=9q distinct lines

    x=a y,  y=b z,  x=c z,  a,b,c in mu_n.

Distinctness follows from their coefficient patterns and distinct roots. Their singular set consists exactly of the n^2 grid points G={[u:v:1]:u,v in mu_n} and the three coordinate vertices V={(1:0:0),(0:1:0),(0:0:1)}. Each grid point lies on exactly three components, one per family; each vertex lies on exactly n components of one family. Pairing components within one family gives its vertex, while components in different families give a grid point. This classifies every pair intersection and excludes omitted or additional singular points. Grid and vertices are disjoint. Each component contains n grid points and one vertex.

**Classification of all auxiliary lines.** A line ax+by+cz=0 with three nonzero coefficients contains no coordinate vertex. At a grid point it gives a u+b v=-c, with |u|=|v|=1. Eliminating v restricts u to the intersection of the circles |u|=1 and |a u+c|=|b|. These circles have distinct centers because a,c are nonzero, so they meet in at most two points. To avoid a diagram-only argument: on |u|=1, expanding the squared modulus gives Re(a conjugate(c) u)=(|b|^2-|a|^2-|c|^2)/2. A nonconstant real affine functional on a circle has at most two level-set points. This is an exact equation over C, not a floating-point test.

If exactly one coefficient vanishes, the line fixes a nonzero coordinate ratio. Either that ratio belongs to mu_n, in which case the line is an arrangement component with exactly n grid points and one vertex, or it contains no grid point and at most one vertex. If two coefficients vanish, it is a coordinate axis with exactly two vertices and no grid point. These cases classify all lines. Since n>=3, K=n+1, attained exactly by components; every auxiliary line contains at most two points of Z.

**Primal:** weight 1/3 on every component. Grid coverage is 1; vertex coverage is n/3=q>=1; total weight is n. **All-line dual:** y=1/n on G and y=0 on V. A component has sum 1, any auxiliary line has sum at most 2/n<=1. The dual total is n. Thus tau_comp=tau_all=n exactly. The cover lemma gives epsilon=1/(n+1)=1/(3q+1). This is an independently checked infinite family, and an equality witness for the cover primal/dual optima. It is not an equality case for tau=K, and no such claim is made.

## Small n and q boundaries

q=0 gives no arrangement and empty Z: neither K nor the stated expression applies. All positive integer q are collision-free by the classification above. The broader Fermat construction has instructive exceptional n=1,2 cases:

* n=1: three distinct concurrent lines; Z is just (1:1:1). Coordinate vertices are not singular because a pencil has only one component. K=tau_comp=tau_all=1 and epsilon=1. Thus extending the n^2+3 formula to n=1 is false.
* n=2: Z has four grid points and three vertices. K=3. The component primal puts weight 1/2 on each of six lines, total 3. The component dual puts weight 1 on each vertex and zero on the grid; every component contains one vertex, proving tau_comp=3. That dual fails on coordinate axes, which each contain two vertices. For tau_all, put weight 1/3 on each component and 1/6 on each coordinate axis, total 5/2; grid coverage is 1 and vertex coverage is 2/3+1/3=1. Put y=1/4 on each grid point and y=1/2 on each vertex, total 5/2. The all-line classification gives component sum 2/4+1/2=1, coordinate-axis sum 1, and every other line sum at most 1/2, so tau_all=5/2. The cover lemma yields epsilon=1/3. This exact example proves component-only and arbitrary-line optima need not agree.

## Verified result and remaining gap

The global target is not resolved. The verified theorem is the cover criterion plus exact all-line certificates for the stated infinite 9q-line family, with complete all-line collinearity classification and explicit boundary controls. General arrangements require either a cover of weight at most their actual K, or a separate multiplicity argument. Substituting component maximality for all-line maximality or checking a dual only on components transfers a genuine missing condition into an assumption.

Independent route completion estimate: 100% for this family/certificate derivation; 0% claimed toward a general proof beyond this conditional criterion. Candidate-audit estimate at this checkpoint: 20% (source fixed and independent reference theorem established, candidate not yet read).
