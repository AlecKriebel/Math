# Verification and historical supplement

Alec Kriebel. *Focal pedal area ratios of closed elliptic billiards*, version 1.0, October 4, 2026. ORCID https://orcid.org/0009-0001-9320-500X. This supplement is part of the extensively AI-assisted, unrefereed research package. No human peer-review or formal-verification claim is made.

## Exact scope and source fidelity

The original equality is E: A+/A−=B+/B− for original chord and outer boundary-tangent supporting-line pedals, using signed shoelace areas. The stronger proved result M is B±=C0A±, with the same positive phase-independent C0 at both foci. C, the proposed phase constancy of the common focal ratio, is false. The original invariant framing and explicit imported assertion both need this distinction; the correction cannot be blamed solely on the dataset.

The primitive domain is a noncircular boundary ellipse, a strictly nested nondegenerate confocal elliptical caustic, least period N>=3 and coprime turning number 0<tau<N/2, including stars. Reversals/repeated traversals are extensions by sign/scale. Hyperbolic/collapsed caustics, diameter walks, segment-clamped feet and unsigned lobe sums are excluded. The circle has coincident foci and a separate regular-star formula C0=sec²(pi*tau/N), with 0<tau<N/2.

The original observation is Reznik–Garcia–Koiller, arXiv:2004.12497v1 (26 April 2020), Table 5 p. 6 k605; v11 (29 October 2020), Table 7 p. 9 k606; published *Fifty New Invariants*, Arnold Math. J. 7 (2021), 341–355, Table 7 p. 349 k607, DOI 10.1007/s40598-021-00174-y. The signed convention is journal Eq. 1 p. 343. Primitive-even E already has their central-symmetry proof. An even-length repetition of an odd primitive orbit does not acquire that symmetry.

## An explicit deduction of triangular E/M from old results

This historical implication is independent of the main all-period proof. It is conditional on the older published geometric theorems identified below, not a claim that their full general vertex-CAS proofs were independently recertified.

Let X=a²>Y=b²>0, c²=X−Y, D=√(X²−XY+Y²), n=X−D>0, m=D−Y>0 and rho=r/R=2mn/(X−Y)². The original triangle has incenter I, circumcenter O and circumradius R. Reflection makes its outer tangents the external angle bisectors, hence the outer triangle is the excentral triangle. Its center is H=2O−I, radius 2R, and signed area 2[T]/rho.

Garcia–Reznik, *Discovering Poncelet Invariants in the Plane*, IMPA (2021), Theorem 2.1, printed pp. 13–15, gives the incenter-locus axes m/a,n/b; Theorem 2.3 gives rho. Helman–Laurain–Garcia–Reznik, arXiv:2102.09438v4 (16 April 2021), sections 3.4–3.5, pp. 6–8, gives circumcenter-locus axes n/(2a),m/(2b) and powers R²−|O|²=D and 4R²−|H|²=X+Y+2D. The supplied scalar side-parameter power reductions are reproduced in verify_historical_power.py.

Euler's relation |O−I|²=R²−2Rr and the powers imply

    |I|²+4rho|O|²=X+Y−4rhoD,
    4O·I−|I|²=X+Y−2D.

Writing u=O_x²,v=I_x², the two locus equations substitute into the first identity to yield

    alpha(v−4m²u/n²)=0,    alpha=1−Xn²/(Ym²)>0.

Indeed Ym²−Xn²=2(X−Y)[D(X+Y)−X²−Y²]>0, since D²(X+Y)²−(X²+Y²)²=XY(X−Y)²>0.

Phase synchronization needs more than locus shape. The two tangent branches from a boundary point P to the positive caustic vary analytically: after caustic normalization z=(P_x/a_c,P_y/b_c), the contact directions are (z±√(|z|²−1)Jz)/|z|², where J rotates by 90 degrees. Here |z|²−1>0. Their second boundary intersections are rational with positive quadratic denominators. On a chosen connected oriented phase circle, I and O are therefore real analytic. The product (I_x−2mO_x/n)(I_x+2mO_x/n) vanishes identically, so one analytic factor vanishes identically; it cannot change branch at a zero. At the symmetric phase containing (a,0), O_y=I_y=0. The original power and R²=(a−O_x)² yield O_x=n/(2a)>0. The second displayed metric identity fixes I_x=−m/a, hence globally

    I_x=−2mO_x/n,    H_x=(2+2m/n)O_x.

Put U=D−c²>0 and V=2(Y+D)>0. Algebra gives 2+2m/n=V/U. The classical signed triangle pedal formula, [T](R²−|F−O|²)/(4R²), then gives

    A±=[T](U±2cO_x)/(4R²),
    B±=[T](V±2cH_x)/(8rhoR²),
    B±=V/(2rhoU) A±.

In the independent parameter t=m/n>1, the identities become

    X/Y=t(t+2)/(2t+1), D/Y=(t²+t+1)/(2t+1),
    rho=2t/(t+1)², V/U=2(t+1), C0=(t+1)³/(2t),
    U²−c²n²/X=Y²(2t+1)/(t(t+2))>0.

The last inequality and |O_x|<=n/(2a) prove strict focal positivity. The circle limit C0=4 matches the equilateral case; the noncircle algebra itself divides by quantities that vanish at a=b and is not applied there. At eccentric degeneration C0 diverges; no finite endpoint multiplier is claimed. Reversal/repetition follow by signed area scaling.

The inspected triangular-orbits preprint arXiv:2001.08054v3 has a faulty printed isosceles example on p. 9, as well as ancillary reciprocal-Cayley/area-ratio text errors. At squared axes 21,16, its literal base fails the actual caustic tangency condition by 64512/625 and its claimed circle fails incidence. That example is not used here. The old scalar power statements agree with the independently reproduced center-power derivation, the IMPA statements, and actual constructed billiards. Generic old locus/rho vertex-CAS proofs were not fully reproduced. The inspected v3 header is 12 December 2021; its internal July 2020 date does not establish priority of every v3 line. No separate triangular novelty is claimed.

## Classical nonconstancy and bounded priority comparison

Querret, Annales 14 (1823–1824), 280–285, and Sturm, pp. 286–293, establish signed triangle pedal area in terms of circumcircle power. Fierobe, arXiv:1807.11903v5 (22 July 2019), Lemma 4.1 p. 9, distinguishes the two axial triangular billiard circumcenters. Together they give unequal reciprocal focal ratios under central inversion. Thus the main note's exact example is a present certificate of an old-results corollary, not a claim to a new negative theorem or earliest correction.

Two independently frozen literature routes checked general elliptic/Poncelet area and trace methods, and focal/classical/triangular geometry. A separate targeted adversary verified the conditional old N3 implication. No complete prior E/M theorem across the stated primitive convex/star domain was located in the primary sections examined. This is a bounded non-location finding, not absolute firstness. Known observations, even and triangular cases, canonical coordinates, and compact-torus/Jacobi principal-part methods are credited.

The 2026-10-01 preprints by Alper Ferudun were authenticated against public Zenodo files and deposit dates preceding the 2026-10-02 original submission. Focal Pedal-Antipedal Area Products, v1.0, DOI 10.5281/zenodo.23079799, treats original pedal times antipedal at least N divisible by 4. Steiner-Centroid Pedal Area Ratios, v1.0, DOI 10.5281/zenodo.23089778, treats original area / own-Steiner pedal for odd N. Outer-Pedal Area Products, v1.1, DOI 10.5281/zenodo.23088516, treats outer unpedalled area times outer pedal at least N=2 mod 4, with centered odd results. The first and third headline domains are incompatible, so combining them does not prove full E/M. The general even-M scalar-trace bridge was not independently closed, and no even-M priority claim is made. An original 2020 video title suggests original/outer focal ratios, but player content was not inspected; no independent new-discovery claim for M follows.

Six journal finals were unavailable: the inversive-triangle, pedal-like-curve, Steiner-Hat, triangular-orbit Monthly, center-power and spatial-integral papers. Specified primary preprints and relevant book sections were inspected without assuming identity to missing final texts. None of their inspected scopes supplied a concrete full-domain E/M theorem. That observation is an inference limited to the read editions; the missing editions remain coverage limits. Finite catalogs, search queries, citation graphs and old proof question marks cannot certify absence throughout all literature.

## Reproduction

Use Python 3 with SymPy 1.14.0 and mpmath 1.3.0. The requirements file records versions; no network is needed by any checker. Run from verification/:

    python verify_exact.py
    python verify_numeric.py
    python verify_triangle.py
    python verify_triangle_phases.py
    python verify_historical_power.py
    python verify_reflection.py

verify_exact supplies exact conic/projection identities, reflection/contact checks, two reciprocal triangle phases, and finite reduced-lattice incidence controls. verify_triangle proves the general signed triangle formula symbolically and independently verifies the rational parameter and actual excentral geometry. verify_historical_power reproduces the original scalar power proof modulo its declared square-root relation, with denominators displayed. The numerical scripts provide real/complex diagnostics, 54 actual triangle cases, and 18 independent direct-reflection configurations; they are finite NONINTERVAL evidence and do not certify universal analytic bounds. The universal proof is the note itself.

reflection_geometry.py is an original independent sampler. Its imported wrapper verify_reflection asserts all geometry/area/positivity/phase predicates. Running reflection_geometry.py directly performs a larger 117-configuration census and writes a results file in its own directory; its printed output alone is not a proof verdict.

Original source/dependency hashes and local programme provenance are recorded separately. The verification package redistributes no third-party source PDFs, extracted texts or facsimiles.
