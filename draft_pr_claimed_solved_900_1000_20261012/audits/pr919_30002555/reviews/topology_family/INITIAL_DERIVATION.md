# Independent reconstruction before submitted-proof comparison

Recorded 2026-10-15 05:11:20 UTC. Discovery/audit completion estimate: 25%.

Inputs read so far: parent `RESEARCH_CHARTER.md`, `TARGET_IDENTITY_PREFLIGHT.json`, `source_record_private.txt`, and `ORIGINAL_SNAPSHOT.json`; the file inventory but no original proof or reviewer verdict. The charter already supplies the proposed mechanism. The reconstruction below tests that mechanism without consulting its implementation.

## Exact target and topology convention

The target is universal existence for a prescribed *matrix* subgroup of GL+(2,R), not merely an abstract group. One admissible counterexample suffices. The candidate end space is the closed Cantor subset X={0,2/3,1}, so the relevant surface has exactly three ends. A translation surface is oriented; the topological lemma below concerns a connected second-countable surface without boundary, with finite n>=3 ambient ends. Infinite genus and the absence of planar ends are not needed for the topological lemma itself. Their role belongs to the later conformal step.

An important convention: if K is a compact subsurface, a component of the *open* complement S\K can acquire collar ends approaching the deleted boundary of K. Its intrinsic end space must not be identified with its subset of ambient ends without a qualification. Work instead with the Freudenthal end partition induced by a compact subset, or with components of S\int(K) retaining the compact boundary.

## Separator construction

For a connected surface, take an exhaustion by connected compact subsurfaces. Distinct ambient ends are separated by some stage of the exhaustion. Since there are finitely many ends, one stage simultaneously separates every pair. A compact subsurface has finitely many boundary circles and therefore finitely many complementary components. Fill each relatively compact complementary component into the core. Every remaining complementary component contains an ambient end: a noncompact bordered surface with compact boundary has an end escaping every ambient compact set. Consequently one obtains a connected compact subsurface K whose complementary components U_1,...,U_n induce precisely the singleton ambient-end sets {e_1},...,{e_n}.

This construction uses ordinary surface exhaustion and the definition of ends, not the classification of infinite-type surfaces. It does not require K to have genus zero, or each tail to meet K along only one circle.

## Nondisplaceability under every homeomorphism

Suppose a homeomorphism h:S->S has h(K) disjoint from K. Since h(K) is connected, it lies in one component U_i of S\K. Let W be the component of S\h(K) containing K. For j!=i the connected closed tail cl_S(U_j) is disjoint from h(K), intersects K, and therefore lies in W. Thus W carries at least the n-1 distinct ambient ends e_j (j!=i).

But homeomorphisms are proper and induce bijections of the ambient end space. The components of S\h(K) are images of the components of S\K and each carries exactly one ambient end. Therefore n-1<=1, contradicting n>=3. No assumption that h fixes individual ends, has finite order, preserves orientation, is affine, or respects genus is used.

Equivalent careful formulation: for an end e, its sufficiently far representatives lie in exactly one component of the complement of the compact set K; the set of such e is the component's ambient-end set. The proof counts those sets and never invokes the generally nonproper inclusion U_j->S to transport intrinsic end spaces.

## Bridge that would finish the obstruction

If a group H of self-homeomorphisms of S acts compact-set properly, meaning {h in H: h(C) intersects C} is finite for every compact C, nondisplaceability gives H finite by setting C=K. For a translation surface, every affine map whose derivative lies in SO(2) is locally z->az+b with |a|=1, hence holomorphic on the regular locus. At an included finite-angle cone point of angle 2*pi*m, the translation coordinate is locally w^m, and a rotational affine map extends holomorphically using the removable-singularity theorem (or the local conical chart). Excluded singularities, infinite-angle completion points, or boundary conventions require explicit source-model verification. If the full rotational affine preimage acts compact-set properly on the relevant Riemann surface, it is finite and its derivative image Gamma(S) intersect SO(2) is finite. It is essential to use the full preimage and not assume an arbitrary derivative splitting.

## Adversarial boundary controls

* n=1: the count gives zero other tails; no obstruction. A one-ended infinite-genus surface admits compact cores that can move away into its sole infinite-genus tail.
* n=2: the count gives one other tail; no contradiction. On a bi-infinite chain of handles, a translation of the chain displaces every chosen finite block core.
* n>=3 with extra planar ends: the *topological* obstruction still works if the total number of ends is finite and >=3. A later conformal argument must use actual infinite genus, not the assertion that every end is nonplanar.
* Infinitely many ends: this proof does not supply a singleton-tail compact separator and makes no claim.
* Finite-angle cone points included as ordinary points do not alter ends. Removing a closed discrete family of those points can add planar ends; it cannot be done silently while preserving the exact finite all-nonplanar target.
* Genuine topological boundary, if allowed, needs a separate conformal model. Compact boundary is not interchangeable with deleted punctures.
* Finite rotational groups cause no contradiction. The candidate needs an actually infinite subgroup of SO(2); finite numerical lists of powers cannot establish this.

Provisional conclusion: the finite-end nondisplaceability mechanism survives a direct adversarial reconstruction. The exact surface convention and compact-set conformal properness remain dependencies to compare against the submitted proof and primary sources. This is neither a priority audit nor a certification of current openness or novelty.
