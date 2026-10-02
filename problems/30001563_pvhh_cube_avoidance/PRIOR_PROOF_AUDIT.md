# Credited prior proof and independent reconstruction

Problem30001563 / OWR-4425-020. No new avoidance theorem or priority claim.
Proposed disposition: already_solved, 0/5 new author turns, subject to separate review.

## Exact theorem

Let phi(0)=03, phi(1)=43, phi(3)=1, phi(4)=01. The infinite fixed point beginning0 contains no three consecutive nonempty blocks of equal length and equal integer letter sum. This is precisely Shallit's Conjecture48, printed2236 in OWR37/2010; the definition of PVHH powers is on2235. The complete contribution2230–2236 was read and the question page visually checked. It is not an additive-square or abelian-cube assertion.

Cassaigne, Currie, Schaeffer and Shallit prove this exact theorem in *Avoiding Three Consecutive Blocks of the Same Size and Same Sum*, arXiv1106.5204v3, Theorem18, manuscriptp20; the morphism is fixed onp3. The authors' primary publication pages identify the final publication as JACM61(2)(2014),Paper10, DOI10.1145/2590775. Direct ACM retrieval was unavailable. The full inspected proof is the identified arXiv manuscript, not a claimed inspection of final journal pages. Its mathematical proof and computational mechanism receive full credit.

## Published computation: material reproducibility qualifications

The preprint uses normalized eigenvectors of the incidence matrix and prints a complex-coordinate bound2.1758, a503-vector set U and135572 reachable states. Its footnote explicitly uses floating-point approximations. Direct re-evaluation of the displayed diameter-plus-tail formula gives approximately2.175815390211514; 2.1758 is rounded downward and must not be used as a rigorous upper bound for that formula.

The reconstruction here uses outward bounds C1=1.9032, C2=2.9819, C3=C4=2.176 and independently certifies them. It obtains497 vectors, not503. The503 count is not reproduced or explained as a source-code fact. The old linked supplementary site could not be retrieved, so no comparison with original code or original vector list is claimed.

The exact source graph definition includes u,v,u+v in U. It yields78340 reachable states in this reconstruction. If only the extra u+v filter is omitted, the larger graph yields exactly135572 reachable states and no accepting state. This explains the numerical reachability difference by an explicitly tested admissibility choice; it is evidence of how the printed count can arise, not proof of what unpublished original code did. Both graphs are exhausted without a depth or state cap. Most importantly, the larger graph contains every ancestral path required by the proof, so exclusion there does not rest on pruning by u+v.

Thus the published theorem is credited, the printed503-vector count remains unreproduced, and a separately certified outward-rounded reconstruction of its proof is supplied. No claim that every published computational detail was reproduced is made.

## Complete analytic reduction being verified

Use alphabet order(0,1,3,4) and incidence matrix

    M = [[1,0,0,1],[0,0,1,1],[1,1,0,0],[0,1,0,0]].

Its characteristic polynomial is p(z)=z^4−z^3−2z²+2z−1. Each prefix endpoint has a unique parent position. If an edge has proper-prefix label a in {empty,0,4}, the prefix Parikh vector obeys sigma(child)=M sigma(parent)+psi(a). Parent positions strictly decrease except at0. The labelled alphabet graph has an edge for each occurrence in an image word. Its paths lift uniquely from a specified starting position.

For each root z of p use right vector
R(z)=(1,z(z−1),(1+z(z−1))/z,z−1)
and left vector
L(z)=(1,z(z−1),z−1,(1+z(z−1))/z).
Reduction modulo p verifies M R=z R and L M=z L. The normalized right eigenvector is R/||R||, with first coordinate positive real. The corresponding inverse eigenvector row is tau_z=||R|| L/(L·R), where the dot product is bilinear. Distinct eigenvalues give the inverse relationship. Conjugate roots give conjugate rows.

The two real roots are isolated by rational sign-change brackets[1.69,1.7] and[−1.51,−1.5], refined by180 rational bisections. The remaining pair has real part(1−a−b)/2 and modulus squared−1/(ab); the computed imaginary-part interval is strictly positive. The roots are therefore distinct, with two expanding real roots and a contracting complex pair. The checker evaluates the displayed normalized rows with directed interval arithmetic, then encloses each real/imaginary coefficient in rational intervals of width at most a few10^−18. Subsequent integer-vector tests use only exact integer endpoints.

For an arbitrary block, prefix expansion gives its contracting coordinate as a difference of two finite/infinite prefix sums. All length9 labelled paths give301 distinct vectors D9. The exact coefficient boxes bound every squared coordinate difference in D9, as well as every proper-prefix-label difference. Their geometric tail gives a rigorously outward-enclosed block-pair bound strictly below2.176. The certificate retains the interval, not only a decimal estimate.

If two blocks have equal length and sum, their difference belongs to Lattice=ker(1,1,1,1) intersect ker(0,1,3,4). Its integer basis is e=(1,−2,2,−1), f=(1,−1,−1,1). The coefficient change from the evident free-coordinate basis has determinant1. The imaginary determinant of tau(e),tau(f) proves lower bounds1.49|m| and2.16|n| for tau(me+nf); these are certified outward lower bounds. Consequently m,n lie in{−1,0,1}; exact interval tests of the nine possibilities leave only0,e,−e. Those three satisfy the expanding-coordinate bounds.

Moving to ancestors, expanding coordinates obey the inverse recurrence. The largest prefix-error coordinates are |tau1(e4)| and |tau2(e0−e4)|; all alternatives are interval-checked. Thus induction gives C1 andC2 from2*error/(|lambda|−1), strictly below the outward constants above. This applies to every ancestor of an equal-length/equal-sum block pair, not just the final pair.

Every possible ancestor difference is therefore in U={integer x:|tau_i(x)|≤C_i}. Since all four columns of the eigenvector matrix have norm1, its operator norm is at most its Frobenius norm2. Hence ||x||²≤4 sum C_i²<89. This avoids the preprint's rounded singular-value/norm estimate. Exhaustively enumerating all38249 integer vectors with squared norm≤88 and checking the rational coefficient boxes gives497 members and zero uncertain classifications. U_CERTIFIED.csv retains every vector.

For four endpoints, put u=sigma(p3)−2sigma(p2)+sigma(p1), v=sigma(p4)−2sigma(p3)+sigma(p2), and retain their four letters. An edge labelled(a1,a2,a3,a4) sends

    u to M u + psi(a3)−2psi(a2)+psi(a1),
    v to M v + psi(a4)−2psi(a3)+psi(a2).

Every nonempty triple-block ancestral chain reaches a last nonempty outer block whose parent is empty. Since proper prefixes are empty,0,4, all possibilities are represented by the nine ordered endpoint tuples
(0,0,0,1),(0,0,1,1),(0,1,1,1),
(3,3,3,4),(3,3,4,4),(3,4,4,4),
(5,5,5,6),(5,5,6,6).
The initial prefix0314301 supplies all three image contexts. The checker constructs these states from that prefix and verifies their U admissibility. No symmetry quotient is used.

An additive cube would give a forward path from one of those states to a state with u andv in the equal-length/equal-sum lattice. Every preceding state has both differences in U, by the ancestor bound. The exact finite closure with u,v in U alone contains135572 states and checks1129490 outgoing edges; none has both differences in the lattice. This necessary-path exclusion suffices for avoidance; no converse involving potentially reordered equal endpoints is required. Adding the safe u+v filter gives78340 states and650384 edge checks, also with no accepting state. There is no finite-word-length limitation.

## Computation and scope

Run certify_eigen_bounds.py first (mpmath interval arithmetic,60 decimal digits; inspected installed mpmath version is recorded separately), then replay_certified_graph.py with and without --omit-sum-filter. Graph replay is standard-library, exact integer arithmetic, bound to the retained U hash. Both sorted reachable streams are hashed but not retained; they are reproducible by the scripts. Raw source PDFs and imported records are excluded from public artifacts.

The work is verification and a qualified reconstruction of a credited prior theorem. It supplies no new author proof turn, no separate resolution of duplicate imported30001564, and no claim about arbitrary morphisms, additive squares or historical priority.
