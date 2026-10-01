# Turn 2: a relative filling criterion and its exact coverage gap

**Scoped partial result; original Problem 12.11 remains unresolved after two substantive author turns.** This route repairs the closed-versus-cusped mismatch from turn 1 and investigates whether puncturing short-slope regions supplies the required alternating coverage. It gives a valid relative criterion, but that coverage step fails without additional topology.

The hyperbolic inputs below are credited to Costantino–Thurston, Ishikawa–Koda and Futer–Kalfagianni–Purcell. The deductions and bookkeeping are supplied to specify their exact applicability, not to claim a new volume theorem.

## 1. A precise relative shadow class

Start with a branched special shadow P of a closed orientable 3-manifold, with connected singular graph and V>=1 true vertices. The regions R_1,...,R_r are disks. Let k_i count vertex incidences on the boundary of R_i, with multiplicity; let g_i be its permitted integer or half-integer gleam.

Take a small neighborhood of the singular graph. Its reconstructed boundary piece, denoted N_P, is the drilled manifold of Costantino–Thurston Proposition 3.33. It is a complete finite-volume hyperbolic manifold with r torus cusps and

    vol(N_P)=2 v_oct V.                                   (1)

For each region, the reconstruction has a specified primitive filling slope s_i. Ishikawa–Koda Lemma 5.3 identifies its length, in a simultaneous disjoint cusp system, as

    length(s_i)^2 = 4g_i^2+k_i^2.                         (2)

In particular this is a length in the prescribed cusp scale, not a normalized length obtained by dividing by the square root of cusp area.

Choose any subset I of the regions to fill and leave U={1,...,r}\I unfilled. Let

    M_I=N_P(s_i : i in I).                               (3)

This has an entirely combinatorial relative-shadow description: puncture one disk in each R_j with j in U, label the new boundary circle external, and retain the numerical gleams on the unpunctured regions. Costantino–Thurston Definitions 3.10–3.11 identify external boundary with drilling. Equivalently, in the reconstruction of the regular neighborhood of the singular graph, attach only the disk-region handles indexed by I. The local solid-torus attachments of Ishikawa–Koda's proof then fill exactly the corresponding cusps; the annular regions with external boundary leave the other cusps open. This justifies (3), rather than treating every relative shadow as automatically satisfying a closed-shadow theorem.

We require this special-shadow completion or the equivalent explicit block/filling description as part of the certificate. Arbitrary relative shadows can have more general regions and boundary vertices. Their inclusion is not asserted.

## 2. Relative long-gleam criterion

If I is nonempty, put

    Q=min_(i in I)(4g_i^2+k_i^2).

**Proposition.** If Q>=40, then M_I is hyperbolic and

    vol(M_I) >= 2 v_oct V (1-4pi^2/Q)^(3/2)
               >= 2 v_oct V (1-pi^2/10)^(3/2).            (4)

If I is empty, equation (1) gives the exact volume instead.

### Proof

The integers 2g_i and k_i make every expression in the minimum an integer. The classical rational bounds 223/71<pi<22/7 imply

    39 < 4pi^2 < 40.

Consequently Q>=40 is exactly the strict condition that every filled slope has length greater than 2pi. Futer–Kalfagianni–Purcell, arXiv:math/0612138v4, Theorem 1.1, expressly permits filling a subset of the cusps, using disjoint horoball neighborhoods of that subset. Apply it to N_P with the cusp system in (2). Its geometrization qualification is satisfied for these orientable three-manifolds; when at least one cusp is left unfilled, the cited theorem also discusses the Haken case. It supplies hyperbolicity and the first inequality in (4). The second follows because 1-4pi^2/Q increases with Q. QED.

For an entirely rational coefficient inside the exponent, pi<22/7 gives the slightly weaker but explicit bound

    vol(M_I) > 2 v_oct V (3/245)^(3/2).                  (5)

Indeed 1-(22/7)^2/10=3/245. Equation (5) is a lower bound on the actual M_I, not on an unverified further filling. No optimal constant is claimed.

If the boundary-marked reconstructed manifold M_I is certified to be the given knot exterior, (4) is the desired sort of shadow-combinatorial volume lower bound for that presentation. The certificate may be established by shadow moves that preserve the pair, but it must be established: merely having a cusped manifold with the right number of boundary components is not enough.

### Cusp-coordinate check

The parity lattice in Costantino–Thurston Proposition 3.34 has generators (2,0) and (epsilon_i,k_i), with epsilon_i in {0,1}. Since 2g_i has parity epsilon_i, the region slope has coordinates

    ((2g_i-epsilon_i)/2,1)

in this basis, and Euclidean vector (2g_i,k_i). It is primitive because its second basis coordinate is 1. This verifies both the half-integer case and the absence of a missing factor of two in (2). The needed metric formula is supplied by the cited geometric reconstruction, not by this arithmetic check alone.

## 3. A constraint for collapsible disk/annulus presentations

The relative formulation leaves room for shadow moves, so the planar Euler obstruction from turn 1 must not be applied indiscriminately after such moves. There is, however, a new conditional incidence constraint for a useful subclass.

Suppose the punctured P_I has only f disk regions to be filled and u>=1 annular regions, each with one external boundary circle. Its singular graph is connected and four-valent, with V>=1 true vertices and no singular boundary vertices. Suppose also that P_I is collapsible, as for a certified relative shadow in the four-ball, and that the filled regions retain the additional corner bound

    |2g_i|<=k_i.                                        (6)

Then the long-gleam criterion Q>=40 requires

    V>=5+u.                                             (7)

In particular, such a one-boundary-component presentation with V<=5 cannot meet that criterion.

### Proof

The singular graph has 2V edges, so Euler characteristic -V. Attaching f disks along boundary walks adds f to Euler characteristic; attaching the u annular regions along one boundary circle adds zero. Thus chi(P_I)=f-V. Collapsibility implies chi(P_I)=1, whence f=V+1.

At a true vertex there are six region corners, so the sum of all region incidence counts is 6V. Every annulus has at least one such incidence under the stated connected-singular-graph hypotheses. For a filled region, (6) gives 4g_i^2+k_i^2<=2k_i^2. The condition Q>=40 therefore forces k_i>=5. Hence

    6V >= 5f+u = 5(V+1)+u,

which is equivalent to (7). QED.

The extra bound (6) is not assumed to survive arbitrary shadow moves. Likewise a general relative shadow need not have only disk and annular regions. These hypotheses are part of this precise obstruction; dropping them invalidates the inference.

## 4. Why leaving short slopes unfilled does not establish alternating coverage

Turn 1 finds short formal slopes in the unchanged canonical planar model. One might try to put each offending region in U and apply (4) to the remaining slopes. This is legitimate for the newly drilled manifold M_I. It is not a solution for the original knot exterior unless that exterior is actually M_I.

Removing an additional disk and declaring its boundary external ordinarily drills an additional core curve and creates an additional torus boundary. Restoring the original object requires the omitted filling. If that filling is short, Theorem 1.1 gives no lower-volume transfer for it. Hyperbolic Dehn filling decreases volume: a lower bound for the drilled manifold cannot be read as a lower bound for its filled descendant.

Nor can the unchanged canonical-shadow corner counts be transported across a collapse by assertion. Costantino–Thurston Example 3.15 explicitly collapses the outside region of a figure-eight diagram and removes three of its four vertices, producing a one-vertex shadow of the exterior. This demonstrates a real change in the region/vertex data. A valid proof for moved shadows must recompute those data and the marked boundary identification.

The known long-twist link theorem in Futer–Kalfagianni–Purcell requires at least seven crossings in every twist region of a prime, twist-reduced diagram. That is another genuine sufficient condition, but general alternating knots do not come with that hypothesis. Adding twists usually changes the link, so it is not a universal conversion of the source examples.

## 5. Exact remaining gap and checkpoint

The relative criterion (4) closes the domain issue for an explicitly certified special-shadow filling presentation, and the integer threshold gives a uniform positive coefficient. The unproved step is a construction that puts every alternating-knot shadow into an appropriate presentation while preserving the knot exterior and verifying the long-slope criterion, or a different lower-bound mechanism that handles its short fillings. Neither is supplied by puncturing the bad regions or by a volume-monotonicity argument.

Thus no full answer to Problem 12.11 is claimed. The next route must address the genuinely topological short-filling/alternating-coverage issue, rather than repeat the long-slope corollary. All cited volume results are credited prior work, and no historical novelty is asserted for these scoped consequences.
