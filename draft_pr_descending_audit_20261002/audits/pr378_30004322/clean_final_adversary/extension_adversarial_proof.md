# Fresh adversarial proof of the stronger auxiliary optimum

2026-10-03 04:56 UTC checkpoint; 90% of the assigned audit complete. This reconstruction was written after the clean initial seal and after the extension's exact statement was disclosed. It is independent verification of candidate-derived analysis, not an independent discovery, priority claim, sixth author turn, or unrestricted-conjecture solution.

## Claim and hypotheses

For q a positive integer, n=5q, take a primitive complex n-th root zeta and retain the Fermat lines A_a:x=zeta^a y, B_b:y=zeta^b z, C_c:z=zeta^c x exactly when their indices modulo5 belong to {0,2,3}. Let Z be the entire reduced singular locus. The claim is that the least total fractional weight of all projective lines covering Z is 11/3 at q=1 and 4q for q>=2. This is distinct from the component-only optimum4q, already in Turn5. The independently certified Seshadri value remains1/(4q+1).

## Universal all-line geometry, independent of any LP inference

The full Fermat singular grid is G={(u:v:1):u^n=v^n=1}. Its vertices are E={(1:0:0),(0:1:0),(0:0:1)}. Every retained pair intersection belongs to G or E, and a grid point is singular exactly when at least two of its three incident indices a,b,c with a+b+c=0 are retained. Thus point types are q^2 of000,6q^2 of023,6q^2 double221/334, and the three vertices. Distinct roots give distinct grid points and distinct components; each center retains3q>=3 components.

For a projective line alpha*x+beta*y+gamma*z=0 with all coefficients nonzero, its grid points satisfy alpha*u+beta*v+gamma=0. Since conjugate(u)=1/u and conjugate(v)=1/v, elimination gives

    alpha*conjugate(gamma)*u^2
    + (|alpha|^2+|gamma|^2-|beta|^2)*u
    + conjugate(alpha)*gamma = 0.

The leading coefficient is nonzero, so there are at most two u values; each determines exactly one v. Such a line contains no vertex. This bounds every abc-nonzero projective line before any cover or dual is constructed, so it cannot be circular.

For exactly one zero coefficient, the line fixes a nonzero coordinate ratio. If the ratio is an n-th root it is one of the3n full Fermat components; otherwise it contains no grid point and exactly one vertex. With two zero coefficients it is a coordinate axis, containing exactly two vertices and no grid point. These cases exhaust all lines, including lines with zero or one point of Z.

A retained residue0 component has3q grid points and its vertex; other retained components have4q grid points and their vertex. A deleted component of residue1 can meet singular grid points only when the other residues are2,2; residue4 requires3,3. For a fixed deleted index there are q lifts, not q^2, since choosing one other index uniquely determines the last. Each deleted component therefore contains exactly q double points and one vertex. No singular grid triple contains a deleted component.

It follows independently that K=4q+1, and the auxiliary maximum is q+1: deleted components attain it. For q>=2, precisely deleted components attain that auxiliary maximum since every other auxiliary class has at most2 points. At q=1, other two-point lines also attain2. None of these conclusions relies on the LP optimum or numerical tests.

## q>=2 certificate

Primal: every retained residue0 line gets1/3, every retained residue2/3 line gets1/2. Coverages are1 at000,4/3 at023,1 atdouble,4q/3 atvertices. Total cost4q.

Dual: weight1/q at000,1/(2q) atdouble, zero elsewhere. Total isq^2/q+6q^2/(2q)=4q. Retained residue0 lines contain q000 points and no doubles, load1. Retained residue2/3 lines contain2q doubles and no000, load1. A deleted component load isq/(2q)=1/2. Coordinate axes and nonroot ratio lines have zero load. Every remaining line contains at most two grid points, each of weight at most1/q, and therefore has load at most2/q<=1. The dual is feasible on every projective line. Weak duality gives equality of unrestricted optimum and4q. Singleton and empty line supports cannot defeat this certificate, since all individual dual weights are<=1.

## q=1 falsifier and replacement

At q=1, the000 type is a single point H=(1:1:1). There are six double points D and six023 points T. A double point's indices are221 or334, so none equals an index of H. A line joining H to a double point cannot be a full Fermat component. It therefore belongs to the three-nonzero-coefficient case and contains exactly H and that double point, with no vertex. The six such lines are distinct; if two coincided that line would contain at least three grid points. The component dual gives this line load1+1/2=3/2, a concrete failure of unrestricted feasibility.

Replacement primal: three residue0 components at1/9, six residue2/3 components at4/9, six H–D lines at1/9. At H coverage3/9+6/9=1; at each double8/9+1/9=1; at each T and each vertex1/9+8/9=1. Cost(3+24+6)/9=11/3. These are actual projective lines; auxiliary incidence is not an unsupported abstract covering column.

Replacement dual: H has2/3, each double1/3, each T1/6, vertices0. Cost2/3+6/3+6/6=11/3. Retained residue0 line load2/3+2/6=1. Retained residue2/3 line load2/3+2/6=1. Deleted line load1/3, axes and nonroot ratio lines0. A remaining line contains at most two grid points. If one is H, the other has weight<=1/3, so total<=1. If H is absent the total<=2/3. The fact that H is unique is required; a careless bound twice the largest point weight would fail. Thus this replacement is globally feasible and exactly optimal.

The cover bounds any nonlinear curve's ratio below by3/11 at q=1. Its support exceptions are lines, and the six retained five-point lines still compute1/5. No assertion of attainment of the nonlinear bound is made.

## Exact falsifiable controls and result

The newly written `new_extension_controls.py` imports none of the candidate or sibling arithmetic. It uses SymPy's exact algebraic-number field constructed from independently supplied cyclotomic polynomials, which are checked irreducible. At q=1,2,4 it reconstructs every retained-component pair intersection and compares with the actual point catalog. It groups every marked point pair by its exact projective joining line, yielding complete supports for all possible lines with>=2 marked points. It checks all primal and dual constraints, retained and deleted line counts, and the non-Fermat<=2 classification. q=4 adds a control beyond the sibling q=1,2,3 scan. Full support records and representative pairs are retained under `streams/new_q*_all_line_incidence.json`.

Observed: q1 has16points,9components,51pair-lines, optimum11/3; q2 has55points,18components,921pair-lines, optimum8; q4 has211points,36components,17775pair-lines, optimum16. All coordinate/constraint checks pass. Deliberate negative controls reject the q1 old component dual (max load3/2) and reject the replacement primal with its auxiliary weights removed (H coverage1/3). Replayed sibling extension outputs also match their sealed bytes exactly. The all-q conclusion rests on the preceding proof, not these finite observations.

Adversarial verdict: PASS within the exact positive-integer-q complex reduced-arrangement scope. No mandatory mathematical correction found in the stronger statement. q=0, nonprimitive roots, omitted singular points, replacing complex geometry by a finite field, or treating the component dual as globally feasible at q1 would change or invalidate the assumptions. Historical novelty and the general source conjecture remain unverified/unresolved.
