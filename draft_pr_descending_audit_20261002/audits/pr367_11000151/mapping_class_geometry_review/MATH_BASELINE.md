# Independent mathematical checkpoint (before candidate programs/results/history)

This phase read only the mathematical narrative ranges listed in MATH_SEAL.json. No candidate checker, output, state, final statement, source-gate triage, history, or prior review was opened. Notation here keeps c0=a1a2a3a4, C=c0^5, H=a5a4a3a2a1^2a2a3a4a5, Z=(a1a2a3a4a5)^6, Q=B6/<<CH^-1>>.

## Geometry and the length ceiling

An odd chain of five curves has regular neighborhood genus2 with two boundary components (Euler characteristic -4). Removing an endpoint curve leaves a four-chain regular neighborhood genus2 with one boundary (Euler characteristic -3). The complement in the five-chain neighborhood is a pair of pants; capping either one of the outer boundaries makes that complement an annulus. Thus each four-chain neighborhood boundary becomes parallel to the single retained boundary. This establishes the candidate's boundary-parallel assertion without conflating closed and bounded surfaces.

The four-chain relation is C^2=t_delta after this capping; the five-chain relation is Z=t_delta. My independent B6 free-group-action control verifies Z=CH as a braid identity. It follows geometrically that image(C)=image(H). Hence B6->Mod(Sigma2^1) descends to Q and every genuine positive Q representative of C^2 produces exactly the same number of NONSEPARATING positive twists of t_delta. Theorem A of Baykur–Monden–Van Horn-Morris applies with (g,n)=(2,1) and gives 40. Neither injectivity of Q->Mod nor a classification of all geometric factorizations is required for this implication. A faithful four-chain subgroup map is needed later for the forty-letter conclusion, and Wajnryb's Theorem2.1 supplies exactly that A4 regular-neighborhood case. Attaching an annulus to the boundary does not change the surface or its boundary-fixing mapping-class group.

All generators have one abelianization class, the new relation is 20x=10x, and the homomorphism sending each generator to 1 mod10 proves Q_ab=Z/10. Positive representatives therefore have length 0,10,20,30,40 after applying the geometric ceiling. Three representatives are exhibited by C^2=Z=H^2 in Q.

## Linking inequalities reconstructed

Pure braid P6 has additive labelled-pair linking numbers, half its signed crossing counts. Conjugation by arbitrary B6 permutes coordinates. The quotient relation is pure, so a representative is pure in B6. Each conjugate of CH^-1 contributes the vector R_k, with (R_k)_ij=1-2*1_{k in {i,j}}. Writing the target vector beta as 2 on pairs among1,...,5 and0 on pairs with6 gives L_ij=beta_ij+T-2(t_i+t_j), integer t_i with sum T=m/10-4. Positivity forces L_ij>=0.

For m=0 or10, summing internal inequalities yields s=sum_{i<=5}t_i<=-3, while summing external inequalities yields s>=ceil((5T+10)/4), namely -2 or -1. Both impossible.

At m20, T=-2 and -1<=s<=0. If s=-1, cross inequalities force first coordinates<=0 and exactly one=-1, t6=-1. If s=0, t6=-2; any positive coordinate M forces others<=-M and yields a negative sum, contradiction. These yield exactly six star vectors with L=2 on incident pairs.

At m30, T=-1, internal/external sums force s=0, t6=-1, first coordinates<=0, hence all zero. All fifteen linking numbers are1.

At m40, T=0. The cross sum gives t6<=0, so s>=0. If maximum first coordinate M>=1, pair bounds give s<=4-3M<=1; if no positive coordinate, s<=0. For s0 all first coordinates are0. For s1, t6=-1, at most one first coordinate is1 and the others must be0. Thus exactly the six possible isolated-vertex clique vectors occur.

Positivity makes an isolated strand untouched. An interior isolated strand separates two sets whose required pair crossings are positive, contradiction. The only possible isolates are1 or6. Each residual five-strand positive braid is in an injective A4 geometric subgroup and maps to its full twist. Positive braid monoid embedding then relates every word to the standard word by commutation and braid relations. For xyx=yxy, the two inverse Hurwitz moves written in TURN2 are valid by y^-1xy=xyx^-1. For the two standard tuples the S6 factor-subgroups are respectively the S5 fixing6 and the S5 fixing1, giving a strict Hurwitz obstruction. Simultaneous conjugation by a1a2a3a4a5 connects them. This obstruction relies on subgroup preservation, not merely product equality.

## Twenty letters reconstructed and independently computed

At length20 the five noncentral strands do not cross each other, hence maintain their relative order. The star strand executes a nearest-neighbor walk among six positions; each edge encounters the same fixed noncentral label and is crossed four times. Returning to start restores all labels. Independent enumeration from those definitions yields counts81,162,162,162,162,81 and810 words.

I re-entered the Aut(F4) tuples from narrative and wrote my own free-reduction and right-composition implementation. Every inverse, adjacent braid, distant commute, and quotient relation check passed. The four exact target images coincide for precisely the ten literal rotations of H^2. A negative action comparison safely excludes Q equality without faithfulness. Every survivor has a positive Q certificate: Z=C^2=H^2 is central, and a cyclic rotation conjugates a central product to itself. Strict Hurwitz moves also implement each cyclic rotation with unchanged last factor because the total product is central. Thus this is an exhaustive necessity-and-sufficiency reduction, not acceptance solely by a finite target. Reproduction of candidate programs remains outstanding.

## Thirty letters: mathematical coverage with one computational gap

If all pair linking numbers are1, every pair crosses exactly twice. The narrative's DAG includes exactly the possible prefixes: counts in{0,1,2}, adjacent swaps updating their actual labelled pair, depth equal to sum counts. The permutation is uniquely determined by pair parities. Merging count states therefore preserves every permitted continuation, but does NOT establish braid equality.

A prefix c is coaccessible precisely when f-c is reachable: reverse a positive suffix's adjacent swaps to obtain the complement-count path, and reverse a reachable complement path to obtain a suffix. Both rely on positive count addition, not inverse braids. A canonical prefix of any coaccessible state is also coaccessible. If exact faithful Artin-action equality holds on EVERY edge in this coaccessible DAG, induction proves equality along every complete path. Comparing the terminal action with Z then proves the six-strand theorem. Positive braid relations yield strict Hurwitz equivalence for length30.

This inductive argument is valid, but before reading/running candidate programs I have not yet independently certified its stated graph sizes or all edge-action equalities. That is the precise remaining verification gap at this seal. It cannot be replaced by count-vector merging alone.

## Independent geometry falsifiers already executed

geometry_controls.py verifies all chain braid relations on integral H1, C and H=-I4, their squares=I4, the closed torus (AB)^6=I2, the braid splitting Z=CH via free-group action, and the S6 quotient relation. The integral homology action kills boundary data. The word C^2 a1^6 has the same S6 and Sp4(F3) images as C^2 but length46, hence is unequal in Q by abelianization. This explicit finite collision is a control against an overbroad finite-quotient sufficiency claim; it is not a counterexample to the candidate, which uses the geometric bound and explicit positive certificates instead.

## Qualified scope

An affirmative statement up to Hurwitz plus simultaneous conjugation can follow from the three classified slices. Under strict Hurwitz alone there are four classes: one at20, one at30, two at40. Wajnryb points to Auroux where Hurwitz and simultaneous conjugation are separately defined; reporting both is appropriate. None of this classifies every genus-two boundary-twist factorization along arbitrary curves, nor answers all higher-genus Smith questions, nor establishes worldwide openness/novelty.
