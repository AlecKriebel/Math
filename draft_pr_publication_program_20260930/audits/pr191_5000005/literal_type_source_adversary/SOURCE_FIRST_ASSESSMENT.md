# Sealed source-first assessment

UTC: 2026-10-15T04:17:08.337826+00:00

This assessment precedes any reading of the candidate, code, original review, gate files, or sibling opinions. It is an independent preliminary assessment, not a verdict on the candidate.

## Source and read depth

Primary: Dmitry Fuchs, Billiard Trajectories in Regular Polygons and Geodesics on Regular Polyhedra, Arnold Mathematical Journal (2021), DOI 10.1007/s40598-020-00170-8. PDF SHA-256 9550009b3a903727a89abba863c520def9bf900b6bec779b63ef6cc82d43f01d.

Fully read extracted text pp. 501-503 and 510-512. Visually inspected COMPLETE printed pp. 502, 503, 504, 505, 510, 511, 512 at 1500px (including both type tables, Figure 8 terminal pi-beta, Figure 9, and the Conjecture 2.6 tables). Read sections 1.1-1.2 text on pp. 494-495, including the angular parallelism definition; p. 495 extraction includes art noise. Did not yet fully read pp. 506-509 or the rest of the paper. Physical zero-based page is printed page minus 493. Private source extracts and images are excluded from public deliverables.

## Exact target reconstructed

For a regular n-gon (n>=3), with O=(0,0), one edge on positive x-axis and polygon above it, write gamma=(n-2)pi/n. Short trajectories start at O, finish at their FIRST subsequent vertex, and may reflect at edge interiors. Section 1.2 includes vertex-to-vertex short trajectories; Figure 9 explicitly includes sides and direct diagonals.

Type index k is a residue modulo n-2, represented 0<=k<=n-3. For a trajectory of initial slope angle alpha in [0,gamma] and type A_k, an existing parallel short trajectory FROM THE SAME O with LITERAL slope alpha'=ell*pi/n+epsilon*alpha, epsilon=+1 or -1, is claimed to have type A_(epsilon*k-ell). If n is even, ell must be even. Alpha' must be a geometrically admissible outgoing ray; the displayed angle expression is not automatically reduced modulo pi or 2pi. Section 2.5 first enumerates generic directions from an open fundamental interval, (0,pi/(2n)) for odd n, (0,pi/n) for even n; the conjecture wording itself does not explicitly exclude symmetry directions or sides. Those boundary cases must be addressed rather than silently dropped.

## Model, terminal convention, and parity

Figure 8 labels the terminal geometric interior angle as pi-beta, NOT beta. Thus departure alpha lies in [0,gamma], whereas beta lies in [2pi/n,pi]. The oriented polygon side at departure is positive x-axis. For an N-segment trajectory, the paragraph before Definition 2.1 states: use beta-alpha in (2pi/n)Z when N is even; beta+alpha in (2pi/n)Z when N is odd. The four type branches must be checked together with this physical segment parity to agree with Figure 9.

The four printed branches in Definition 2.1 are not literally disjoint on exceptional rays: at a square diagonal alpha=pi/4, beta=3pi/4, both the A_0 difference branch and A_1 sum branch hold. Figure 9 assigns that diagonal A_1. The N=1 odd sum branch restores that intended label. This is a genuine source-level under-specification if 'one of the following triples' is read as an unqualified disjunction. It is not a demonstrated failure of the parity-aware intended conjecture.

For a regular pentagon direct diagonal X_0 X_2, alpha=2pi/5 and beta=4pi/5. The printed raw triples assign BOTH A_0 (difference) and A_1 (sum), while Figure 9 explicitly chooses A_1. Under literal raw triples alone, Conjecture 2.6 even has a counterexample: choose k=0, epsilon=-1, ell=4. Then alpha'=alpha but claimed type is A_2, which none of those raw triples gives. Under the physical N=1 odd selection, k=1 and the self-map gives A_1 correctly. The repair must be explicit; no refutation of the coherent intended conjecture follows from this typographical ambiguity alone.

## Independent deductions and falsification targets

For a direct diagonal X_0 X_j, 1<=j<=n-1, its slope is alpha_j=(n-1-j)pi/n and Figure 9 type is k=j-1 modulo n-2. Therefore every admissible literal transformation between direct diagonals satisfies k'=epsilon*k-ell modulo n-2 by substitution. This proves the direct-diagonal law (including side endpoints) for all n, independent of the unresolved general reflected trajectory case. It also checks the choice of epsilon and ell signs against primary geometry.

For nonboundary rays the elementary dihedral symmetry through the vertex angle bisector gives alpha'=gamma-alpha and k'=-k (mod n-2), corresponding to ell=n-2, epsilon=-1; its proof should check terminal angle beta'=2pi/n+pi-beta and the printed branches. This alone does not establish the other ell transforms. A general proof must relate potentially different FIRST-hit saddle connections from O, not merely rotate the same vector or carry a terminal vertex beyond an earlier vertex. Periodicity and affinely reducing a direction are possible approaches but require actual central lemmas, endpoint conventions, and source-compatible sector labeling.

Provisional status: intended all-trajectory conjecture unresolved by this source-only audit; literal raw definition is ambiguous and, unqualified, incompatible with its own diagonal example. No positive-solution assumption is made. Completion estimate toward this audit: 25%; toward a new general theorem: unknown.
