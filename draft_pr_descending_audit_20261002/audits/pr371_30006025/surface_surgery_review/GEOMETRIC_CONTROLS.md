# New geometric adversarial controls

These independent constructions supplement the universal proofs in the immutable `MATHEMATICAL_VERDICT.md`. They do not repair the candidate, assert historical novelty, or infer universal geometry from a finite scan. The corresponding exact algebra is in `geometric_controls.py`; its complete output is `GEOMETRIC_CONTROL_RECEIPT.json`.

## A perimeter-preserving cone escape, and why smoothness matters

Fix any cubic one-face genus-g pairing, g>=12, and N=12g-6. Take the regular hyperbolic N-gon with side length

`l=12g/N=2g/(2g-1)`.

It exists: the regular N-gon side increases continuously from zero to infinity as its corner angle decreases from `(1-2/N)pi` to zero. For its actual corner angle alpha, the right-triangle identity gives

`sin(alpha/2)=cos(pi/N)/cosh(l/2)`.

The smooth 120-degree regular polygon would instead have `cosh(l_smooth/2)=2cos(pi/N)/sqrt(3)`. We prove l is smaller, hence alpha>2pi/3, for **all** g>=12. Since l/2=g/(2g-1) decreases and N increases,

`cosh(l/2)<=cosh(12/23)<=1+((12/23)^2/2)/(1-(12/23)^2/12)=589/517`.

The Taylor-series ratio after the quadratic term is at most x^2/12, proving the bound. Using pi<22/7, cos t>1-t^2/2 for t>0, and sqrt(3)<7/4,

`2cos(pi/N)/sqrt(3) > (8/7)*(1-(22/(7*138))^2/2)=1865828/1633023 >589/517`.

All comparisons after the classical pi bound are rational. Glue the N equal-length sides by the given pairing. It is a genuine compact hyperbolic cone surface of the specified genus; each vertex has angle 3alpha>2pi and negative defect `2pi-3alpha`. All edges keep their prescribed equal lengths, and the face perimeter is exactly 12g.

Its area is `(N-2)pi-N alpha`, and the closed cone Gauss-Bonnet identity is

`A=4pi(g-1)+V*(2pi-3alpha)`, `V=4g-2`.

The negative defects lower the area below the smooth value. The candidate's smooth-area substitution therefore cannot be applied. This is an explicit counterexample to the **broader** assertion obtained by omitting smoothness, and a check that the stated obstruction is appropriately restricted. It is not a WP surface or an answer to the original random-surface comparison. The algebraic-angle obstruction remains consistent: the equal prescribed sides are positive algebraic numbers, while the actual angle cosine must be transcendental.

## A genuine disk whose development overlaps

Take eight Euclidean quadrilateral panels. Panel j has vertices at radii 1 and 2 along directions j*pi/2 and (j+1)*pi/2. Glue neighboring radial sides of consecutive panels, but leave the radial sides at j=0 and j=8 unglued. Intrinsically this is a rectangle-shaped annular strip wound twice, with a disk topology. It has V=18, E=25 and F=8, hence Euler characteristic 1. It can also be parametrized topologically by radius and an angle in [0,4pi]. The first and last panel sides are distinct boundary copies even though their developed directions coincide.

There are no interior cone points: any point inside a panel is Euclidean, and any interior point of a glued radial side joins two half neighborhoods into a disk. All panel vertices lie on the boundary. Outer joined corner angles are pi/2, inner joined angles are 3pi/2. At the two unglued radial ends, outer angles are pi/4 and inner angles are 3pi/4. All are positive. The total boundary turning is 2pi.

Each panel has area 3/2, so A=12. The perimeter is `24sqrt(2)+2`, with geodesic sides. Its development sends panel 0 and panel 4 onto the identical quadrilateral, and likewise all other panels modulo 4. Thus the development is not injective while the intrinsic metric remains a disk with no interior singularity. The intrinsic Euclidean theorem applies; the exact perimeter-area inequality is easily verified. This control disproves the hidden implication “no interior cones means an embedded planar development.” It supports the candidate's decision to cite Izmestiev's intrinsic statement rather than a simple-polygon argument.

## Full turn, zero angle, and boundary curvature

Cut the unit square along a length-1/2 slit from the midpoint of its bottom side to its center. The cut object is a topological flat disk with area 1 and perimeter 5. The tip has intrinsic sector angle 2pi; the two copies of the slit have identical developed rays but remain separate boundary branches. The boundary angle list is six occurrences of pi/2 and one occurrence of 2pi. It gives

`sum_boundary(pi-alpha)=2pi`.

Using the interior formula 2pi-alpha at boundary points would instead give 9pi and fails Gauss-Bonnet. Reducing the full turn modulo 2pi would incorrectly replace a legitimate positive sector by an excluded zero sector. This is the precise leaf-tip case relevant to cutting graphs with bridges.

## Interior positive curvature: a polygonal counterexample

Glue four Euclidean isosceles triangles of radial side R and apex angle pi/4 cyclically. The disk apex has total angle pi and positive defect pi. The outer boundary is a genuine geodesic four-gon. Its area and perimeter satisfy

`A=2R^2 sin(pi/4)`, `P=8R sin(pi/8)`,

`P^2/(4pi A)=(4/pi)tan(pi/8)=(4/pi)(sqrt(2)-1)<2/3<1`.

Thus the Euclidean inequality fails when the negative-interior-cone hypothesis is dropped, even with the correct geodesic boundary class. The boundary defect sum is pi and the interior defect is pi, agreeing with disk Gauss-Bonnet.

One clarification to the sealed verdict's auxiliary examples is necessary: **radial round cone disks have circular boundary, so they are not literally Izmestiev's piecewise geodesic cone-boundary class.** They remain useful limiting constructions and can be approximated by geodesic cone polygons; the four-gon above supplies a valid example directly. This is a correction to this audit's exposition, not to the candidate theorem. Their polar area/perimeter formulas and the recorded curvature-sign algebra remain correct.

For the hyperbolic radial auxiliary example, put Theta=2pi*q and h=cosh R-1. Then `A=2pi*q*h`, `P^2=4pi^2*q^2*h*(h+2)`, so

`P^2-4pi A-A^2=8pi^2*q*(q-1)*h`.

The sign is exactly that of the negative cone defect; q=1 is smooth. The exact checker tests this algebra separately from boundary-class applicability. No numerical approximation to a theorem is used.

## Local sector surgery and continuum distance controls

Merging k smooth vertices while conserving their sectors gives glued angle 2pi*k and defect -2pi(k-1). Euler changes genus by (k-1)/2 for odd k. Conversely, dividing one smooth angle among k vertices cannot leave all k smooth. This is a precise obstruction to purely local sector-conserving smooth surgery; changing the face geometry or allowing cone defects removes that inference.

The one-skeleton of the unit square flat torus is a bouquet of two length-1 loops. Between edge midpoints (1/2,0) and (0,1/2), graph distance is 1, while the filled torus has a face-interior path of length sqrt(1/2). The word abAB is freely reduced and nontrivial in the graph's free fundamental group, but filling the square imposes that relation, making it null-homotopic. A periodic lattice graph has also already imposed relations relative to the graph's free universal covering tree. Hence graph cycles, lattice displacements and surface geodesics cannot be interchanged without proving what the quotient and filling do. This genus-1 flat example is an exact boundary control, not a hyperbolic genus-g model used in the candidate obstruction.

Finally, independent E=2/3 simplex maximum tails from inclusion-exclusion are compared with their exact Markov bounds, including t=1 and t<=1/E. These test a measurable necessary mass event. They do not treat it as the sufficient event of geometric realizability. Adaptive largest-coordinate choice exceeds a fixed small-coordinate choice; the candidate's top-k domination already accounts for this.
