# Root reconstruction notes: Grassmann section and affine SOS obstruction

13 October 2026 UTC. Exact submitted head
f6570e093267a7f910faf9cdd60dfbc1c12f5681. Provisional mathematical audit notes;
independent families and priority are pending. No acceptance follows from the
submitted PASS labels.

## Independent deductions

The complexification convention maps the standard complex coordinate a to its
correct underlying real vector: adding its +i component and conjugate, with
the stated square-root factors, yields Re(a)e+Im(a)f. In the projector wedge
identity the two factors -i give a minus sign and interchanging the intervening
degree-one factors gives a second minus sign. The resulting complex orientation
is positive. The (2,2) exterior-type basis has complex dimension15²=225; on
Hermitian matrices conjugate transposition and commuting degree-two factors
make the image real. Independence of that basis makes the map injective as a
real map, not merely a nonlinear parametrization of rank-one generators.

Compression of orthogonal J to a real four-plane has singular values at most
one. Pfaffian equality +1 forces both to have magnitude one, so every Jv has
zero perpendicular component and the plane is complex. Exactly its complex
orientation is positive. Equality at the exposed calibration face passes to
every positive-weight summand of a finite convex expression. Thus the face
really is the image of the convex hull of complex decomposable unit-bivector
projectors. Its additional pure-block trace is nonnegative on this face;
no global nonnegativity of that functional on the whole orbitope is assumed.

Trace zero forces each decomposable generator to have zero pure U/Z component.
The projections of its spanning complex two-plane to U and Z then each have
rank one. Neither can have rank zero, because a nonzero mixed wedge would
otherwise lie entirely in a pure exterior summand. With spanning vectors x,y,
the wedge is a nonzero scalar multiple of x wedge y. Orthogonality gives the
product norm, so unit generators exactly match unit complex product tensors.
This proves equality of convex sets with Sep(3,3), rather than a support-only
PSD inclusion. The section is imposed simultaneously with the exposed face.

Finite spectrahedral images are preserved under affine section and a real
linear inverse extended from the image subspace. Fresh primary inspection of
the published Fawzi paper confirms its normalized trace-one Sep definition
and arbitrary projected Hermitian LMI notion. Its Theorem1 explicitly excludes
Sep(3,3), not merely one relaxation hierarchy. Real-symmetric lifts would be a
subclass. Fawzi's established theorem is an external dependency, not reproved
by the submitted coordinate script.

For the sphere moment construction, M00=1 and the sphere relation give trace2,
so the PSD feasible set and its projection are compact. This avoids an
unsupported closure of a spectrahedral shadow. Every affine-square certificate
is evaluated nonnegatively by every feasible M because the discrepancy has
degree at most two and lies in the full real vanishing ideal. All certified
supporting halfspaces would force the projected relaxation to equal the
compact hull, supplying a finite lift in contradiction to the section.

Strict containment then provides a point and a strictly separating linear
functional. On unit generators the support function is Lipschitz in coefficient
norm; the separating gap remains positive in a neighborhood, which contains
rational coefficients. Hence rational existence is valid, although no explicit
coefficient list or exact comass is computed. Symmetry and spanning by signed
coordinate wedges ensure positive support of every nonzero functional. Comass
normalization need not preserve rational coefficients and is not claimed to.

The Harvey–Lawson pointwise completion identity implies an affine SOS by
half the square of (1-phi) plus half the completion squares. Conversely, an
affine square vector a+Bp gives B^T a=-phi/2 by comparing p and -p. At a
maximizer Bp=-a and the opposite orientation yields ||a||²=1/2. Projecting B
perpendicularly to a and multiplying by sqrt2 gives the homogeneous completion
1-phi². Homogeneity extends the identity to all decomposable vectors. A constant
four-form is closed. None of this locates a least failing dimension or settles
the cases n<=7.

## Checks and exact remaining gap

Root reproduced three complete submitted symbolic-check baselines and45
deliberately damaged-certificate rejections across normal/-O/-OO, with all
stdout/stderr/exit bytes equal to fixed references. All495 quartic exterior
coordinate identities in24 independent real variables are checked coefficient
by coefficient; these support an algebraic bridge beyond finite sampling.
The original checker/certificate bytes remain unchanged. Only the inspected
pure certificate-mutation function and literal references were AST-extracted
from the old runner; its UID1000 environmental harness was not imported,
executed or simulated. See root_reproduction/FINITE_REPRODUCTION.json.

Root read the original OWR2015 contribution pp708–709. It states the degree-one
conjecture for all Grassmann orbitopes after n<=7 experiments, rather than
restricting its assertion to those dimensions. The counterexample at(4,12)
would refute that universal clause. Independent source/degree conventions and
complete geometry/SOS families remain pending before mathematical promotion.
No priority search, preprint package, publication, tracker or PR action has
occurred for this candidate.

Primary sources inspected by root:
[Sanyal, OWR13/2015](https://ems.press/content/serial-article-files/46561),
[Fawzi, published CMP2021](https://www.repository.cam.ac.uk/bitstreams/e6e52df9-b317-4616-9462-c79a3cb4844b/download).
