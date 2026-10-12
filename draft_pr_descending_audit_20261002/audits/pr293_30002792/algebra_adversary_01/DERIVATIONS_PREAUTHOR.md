# Independent algebraic derivation, before reading the submitted argument

Written 2026-10-05T15:44:30.408745+00:00. Algebra-family progress: 35%; the integral-surface adjoint assertion is an inherited, unverified obligation in this family.

Let k be algebraically closed, S=k[x0,x1,x2,x3], and I the radical homogeneous ideal of a nonempty finite reduced union of distinct projective lines. Assume a=alpha(I), alpha(I^(2))=a+1=d. Here I^(2) is the intersection of the squares of the height-two linear ideals of the component lines, rather than an ordinary square. Choose nonzero homogeneous F of degree d in this intersection.

## Conditional surface input

For each integral surface G of degree e>=2, assume there is a nonzero homogeneous A of degree e-2 vanishing on every reduced singular curve of G. This is the only inherited theorem used below. Its validity in positive characteristic and its exact hypotheses require an independent audit elsewhere. These pages do not certify that input.

## Eliminating nonlinear factors

If an irreducible homogeneous factor G of F has multiplicity at least two, F/G belongs to every component line ideal: either G is in that prime, and its remaining copy suffices, or G is a unit after localization at the prime, and F/G still has order at least two there. Membership in the prime also follows directly from primality. Thus d-deg(G)>=a=d-1, so deg(G)<=1.

If an irreducible factor G of degree e>=2 occurs just once, let A be its adjoint as assumed. At each component line L not contained in G, F/G is in its line ideal by primality. For a line contained in G, either G has generic normal order >=2 and L is a singular curve of G, so A vanishes on L; or G has generic normal order exactly one and F/G has order at least one in the regular local ring S_P, since the product has order at least two. A polynomial belonging to P S_P contracts to P. Consequently A(F/G) lies in I, has degree d-2, and is nonzero in the polynomial domain. This contradicts alpha(I)=d-1.

There is no assumption that an arbitrary first derivative is nonzero. Over an algebraically closed field, an irreducible positive-degree polynomial cannot be a p-th power. More importantly, order at a height-two linear prime and multiplicativity in its associated graded polynomial domain, rather than division by a characteristic-dependent integer, justify the argument. The equivalence between generic order >=2 and singularity along a line can be checked in normal coordinates: the constant and both linear normal coefficients vanish identically precisely when all partial derivatives vanish along that line. Tangential derivatives of a polynomial vanishing identically on the line are zero there in every characteristic.

## Repeated linear factors

Write F=product h_i^(m_i) for distinct linear forms, with r factors and sum m_i=d. Every component line is contained in at least one of the r planes, so the squarefree product of degree r belongs to I. Hence d-1<=r, and there is at most one excess multiplicity. If there is an excess, exactly one m_i=2 and all others equal one. If r=1, all lines are coplanar. If r>=2, divide F by the repeated h_i and by any other h_j. The remaining degree d-2 product vanishes on every component line: lines inside H_i retain a factor h_i; lines outside H_i must lie in at least two of the other distinct planes, and removal of h_j leaves one. This contradicts alpha(I)=d-1. Thus in the noncoplanar case F is squarefree.

## Completeness and exclusion of three planes through a line

Each component line now belongs to at least two distinct planes. For every i!=j, the quotient F/(h_i h_j), of degree d-2, cannot vanish on all component lines. A component on which it does not vanish must be contained in H_i and H_j and in no other H_t. It is necessarily the line H_i cap H_j. Thus every pair intersection occurs, and no third plane contains that intersection. In particular all pair-intersection lines are distinct. Intersections of four or more planes at a point are allowed; the argument only excludes a common line of three planes.

## Ideal, radicality, and ACM

For d distinct planes with no three containing a line, set P=product h_i and J=(P/h_i:1<=i<=d). A d by (d-1) matrix has column j (j=2,...,d) equal to h_1 in row 1, -h_j in row j, zero elsewhere. Its maximal minors are the generators P/h_i up to signs. The zero locus is precisely the union of the pair-intersection lines, so ht(J)=2. The Hilbert-Burch theorem then gives a length-one free resolution of J, hence a Cohen-Macaulay quotient of dimension two and no embedded associated primes. At a minimal prime (h_i,h_j), all other h_t are units and J localizes to that prime. Thus J is generically reduced and unmixed, hence radical and equal to the intersection of all pair-line primes. Signs cause no problem in characteristic two.

For d=2 this is simply J=(h_1,h_2), one line. Nonempty unions have a>=1, hence d>=2; a degree-one form cannot have order two on a line. A coplanar union of N distinct lines has ideal (h,product of the N distinct line equations in S/(h)), a complete intersection of degrees (1,N), including N=1. Both outcomes are ACM.

## Proposed falsifiable checks

1. Enumerate all unions of at most three F2-rational lines in P3(F2), computing homogeneous restriction and double-vanishing constraints directly in linear normal coordinates. Every equality case should be coplanar or the three pair intersections of three planes with no common line.
2. Enumerate plane multisets of small total degree in P3(F2); test the maximal reduced line locus on which the plane product has generic order at least two. Repetition and triple-line degeneracy should force a form of degree at most d-2 except the elementary coplanar boundary d=2.
3. Authenticate and execute the original supplemental controls only after this independent derivation is sealed. Computations are finite evidence for the reduction; they cannot validate the inherited surface input.
