# PR37 original partial: independently checked mechanism and exact gap

2026-10-02 07:52 UTC. Original1/5; new substantive attempts0. Proposed
disposition remains unsolved, with a credited low-dimensional consequence.
This is root audit evidence, not a completed new-current-package gate.

The complete K3 Problem5.2 on printed pp302–303 asks about all dimensions,
homeomorphisms or diffeomorphisms of Rn with one common bound on the diameters
of all full orbits and compact-open recurrence, and a boundary-fixed closed
ball special case. It discusses local/manifold and stronger smooth variants.
The global Rn hypothesis is not the same as merely individual orbit bounds
or a finite numerical bound on an arbitrary open subset. None of these wider
versions is silently settled by this partial.

For all x and all integers k, a common full-orbit diameter bound D is
equivalent to |h^k(x)−x|≤D: one direction compares with the zeroth orbit
point; the other applies the displacement inequality at h^ell(x) with
exponent k−ell. If D=0, h is identity. For D>0 the homotopy
H_t(x)=x+t(h(x)−x) is uniformly proper, since |H_t(x)|≥|x|−D. Its joint
extension over infinity is continuous, so the compactified sphere map has
degree+1 and the plane homeomorphism preserves orientation. Intermediate
H_t are not asserted to be homeomorphisms.

In stereographic chordal distance q(x,y)=2|x−y|/sqrt((1+|x|²)(1+|y|²)),
for |x|≥R>D every iterate satisfies
q(h^k(x),x)≤2D/sqrt((1+R²)(1+(R−D)²)). This tends to0 uniformly in k as
R→infinity. On each fixed compact disk, the selected positive return
iterates converge uniformly in Euclidean distance, hence in q. Infinity
is fixed. The two estimates prove uniform spherical recurrence; they do
not prove uniform Euclidean recurrence or equicontinuity of all powers.

In dimension2, for each center a, the invariant open set
U_a=union over all integers k of h^k(B(a,2D)) is connected: each image ball
contains h^k(a), which lies in the original ball, so every member intersects
one common connected member. It contains B(a,2D), lies in B(a,3D), and is
invariant because the index set is all integers. Its closure C_a is compact,
connected and invariant. Fill every bounded component of its complement.
The resulting K_a is compact and connected, has connected complement, and
lies in the closed3D disk: every point outside the disk belongs to the
unique unbounded complementary component. Each filled component has a
boundary meeting C_a, which supplies the connectedness of the fill.
Properness of h fixes infinity and preserves the unique unbounded
component, so h(K_a)=K_a. The set is nondegenerate since it contains a ball.

The established Cartwright–Littlewood theorem gives a fixed point in K_a.
Choose two centers more than6D apart: their closed3D disks are disjoint,
providing two distinct finite fixed points. Adding infinity gives three
fixed points of a recurrent orientation-preserving S² homeomorphism.
The established Kolev–Pérouème Theorem1.1 forces this map to be identity.
All hypotheses are satisfied; the sphere fixed-point restriction is not
being asserted in higher dimensions.

On the line, the global displacement bound excludes a decreasing surjection.
For an increasing map, h(x)>x implies h^m(x)≥h(x)>x for every positive m,
contradicting recurrence at x; h(x)<x is analogous. Thus h is identity.
The boundary-fixed interval proof uses the same increasing-map argument.
A boundary-fixed closed-disk homeomorphism extends by exterior identity to
a plane homeomorphism with full-orbit diameter at most2. Uniform returns
on the compact disk imply compact-open returns of the extension, proving
the disk case. No smooth gluing is asserted: matching boundary values of
a diffeomorphism need not match exterior derivatives.

Root read the exact K3 target/remarks and primary Boroński v1 TheoremA,
definitions and Section3 covering-space argument, and Kolev–Pérouème v3
recurrence definition, prime-end preliminaries/lemma proof and entire
operative Section3 proof of Theorem1.1. Established topological imports
remain imports; the finite diagnostics do not certify them. Root's actual
fresh primary hashes equal the original three provenance hashes. The
versioned KPv3 PDF endpoint returned406; the unversioned endpoint supplied
the exact v3 hash and displayed version header. Failure remains preserved.

The explicit disk corollary was directly read in the accessible2009 v3 of
the paper first published in1998. Root has not directly checked the printed
1998 passage. Current source/priority wording must preserve this distinction
if the printed edition remains inaccessible. Brown1977 direct access was
not claimed by the original; an independent family has recovered the
alternative Hamilton1954 proof, which awaits root reading here.

Root actually replayed both unchanged original programs under
/usr/bin/python3 with SymPy1.14.0. Generated complete31 and8462 receipts
are BYTE/fullJSON identical. The independent program prints metadata only,
so its actual stdout was compared with the exact metadata serialization
of the saved full receipt, not falsely equated with the full8462-check file.
All original13 Git files/modes/blobs and complete14-path diff are bound;
the full149,266,659-byte raw corpus and readonly15458-record SQL join agree.
There is no separate KP-5.2 research report: native importer{} is a
qualified fallback, while full dated literature triage is in the problem.
The original1/5 response ledger remains byte-exact; no native historical
readiness or proof event is reconstructed from its manually edited queue.

No higher-dimensional fixed-continuum theorem or sphere classification
needed for this argument is supplied. Recurrence does not supply the compact
or locally compact cyclic closure required to invoke the Hilbert–Smith
setting; the known periodic theorem does not turn recurrence into
periodicity. No conclusion is proved for the bundled dimensions≥3,
arbitrary local/manifold variants or stronger smooth recurrence there.
This is a precise unresolved gap, not a counterexample to those targets.
Current workflow remains pending independent-family closure, corrected
current administration, and a NEW whole-package adversarial gate. No paper,
new DOI, tracker row, external human review or outside outreach is claimed.

## ROOT_FINAL_CURRENT_ADDENDUM — 2026-10-02T08:24:04.068101+00:00

Root has now read the complete three-page primary Hamilton1954 proof, printed pp522–524, PDF SHA256d5078dc430f11464abea5bee8e3b72a1b50958b9fd1aee185dbabc7c461a2fbd. The earlier dated statement that this reading awaited completion is preserved as historical evidence. The fixed-point argument imports the stated planar/Jordan foundations; this audit does not claim to recertify all their underlying theory. Root also independently read the complete operative Kolev–Pérouème2009v3 theorem/proof and applicable Boroński argument. The1998 journal printed corollary passage remains unverified, so current wording must identify the directly inspected2009v3 source precisely. These are source-verification clarifications, with zero new substantive proof attempts.
