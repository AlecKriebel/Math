# Finite holonomy compatibility for a fixed taut carrier

## Result and scope

This report concerns 10300018 / AMR-102-0018, Calegari's Question 7.3 attributed to Dunfield. The unrestricted boundary-slope algorithm is not obtained.

The proved result is an exact decision and certificate theorem for **finite point constraints on shared increasing interval homeomorphisms**. In particular, a supplied finite regular boundary itinerary can be checked without replacing its unmeasured holonomy by transverse weights. A feasible instance has rational piecewise-linear witnesses. The same theorem gives a terminating finite search at each specified itinerary bound.

These are algebraic compatibility certificates. They do not, by themselves, certify an essential lamination or the complete boundary behavior required by a chosen definition of carried slope. Section 7 states the geometric bridge conditionally and separates its hypotheses. Section 6 proves why finite periodic-orbit samples cannot impose the stronger all-boundary-leaves-closed condition.

A further primary-source check found a genuine convention issue. Calegari's short formulation does not define the boundary condition or an output language. Lackenby's paper, explicitly cited in that setup, uses a fully carried lamination whose entire boundary intersection consists of closed curves of the prescribed slope. Zung uses the slope of a possibly nonlinear boundary foliation. We do not identify these conditions or silently choose one of them.

## 1 The target and the source conventions

Let T be the fixed taut ideal triangulation and B its cooriented branched two-skeleton. The task concerns essential laminations carried by this particular B, not a replacement triangulation, only measured laminations, only compact surfaces, or only a canonical veering lamination.

Calegari [C, Question 7.3 and its surrounding paragraph, PDF p.13] works in the torus-cusp setting and explicitly warns about half-sink disks. His two-line question does not say that the desired output is a finite list, an interval decomposition, a decision procedure on rational inputs, or an effective description of a set of real slopes. It also says carried, rather than explicitly fully carried.

Lackenby [L, section 4(2), manuscript p.26] uses a one-torus boundary and a stronger, explicit condition: a fully carried lamination meets the boundary only in simple closed curves of the specified slope. Such a slope is rational in any integral peripheral basis. The paper asks whether the resulting set is open and notes that knot meridians are excluded, because the associated filling would have a taut foliation transverse to the surgery core. Openness here cannot be used as a proved interval theorem.

Zung [Z, section 1, p.2] instead allows a nonlinear boundary foliation of a given slope in the canonical veering setting. His section 2.3 supplies interval-homeomorphism coordinates. This is useful prior input for a finite compatibility problem, not a general solution to [C].

Consequently there are at least three different tasks to distinguish:

1. Compatibility of finitely many prescribed boundary trajectory segments.
2. Realization of a boundary foliation having a specified asymptotic/rotation slope.
3. Realization with the entire boundary lamination consisting of closed curves of a prescribed rational slope.

Our theorem solves the first task. No equivalence with the second or third is proved. The target's exact boundary/output convention must be fixed before promoting geometric claims. No irrational slopes are added to, or removed from, the original target by this attempt.

## 2 Finite point constraints

Let E be a finite set. For each e in E, fix positive rational lengths L_e and R_e. The unknown object f_e is an increasing homeomorphism

f_e : [0,L_e] -> [0,R_e].

There is **one** map for each e. Distinct occurrences of e, including the two cusp ends of the same ideal edge, use this same map.

Let t=(t_1,...,t_d) be real variables. An affine form means c+sum a_i t_i with rational coefficients. The input consists of:

- a finite conjunction C(t) of rational affine equalities and strict or weak inequalities;
- finitely many requests f_e(X_i(t))=Y_i(t), with rational affine X_i,Y_i.

A request involving the inverse is normalized: f_e^{-1}(Y)=X means exactly f_e(X)=Y. A reversed coordinate at an edge end is converted to the chosen canonical coordinate by its prescribed affine reflection. It is never assigned an independent inverse or endpoint map.

The input is feasible if some t and increasing homeomorphisms f_e satisfy all requests and C. In particular all X_i and Y_i must lie in their respective map domains and ranges.

### Theorem 1

Finite point-constraint feasibility is decidable. If feasible, there is a rational solution t and, for every e, an increasing piecewise-linear homeomorphism f_e whose breakpoints and breakpoint values are rational. The algorithm outputs this finite certificate.

### Proof

For each e, adjoin two permanent requests (0,0) and (L_e,R_e). They fix both endpoints. Separately impose 0<=X_i<=L_e and 0<=Y_i<=R_e for every request. Anchors alone would not exclude an additional sample beyond both right endpoints or before both left endpoints.

Consider all sample occurrences for this e, including repeated ones. Enumerate all ordered partitions of these occurrences. Each block represents equal input values and equal output values. If block A precedes block B, impose X_i<X_j and Y_i<Y_j for all i in A and j in B. Within a block impose X_i=X_j and Y_i=Y_j. There are finitely many such partitions.

Do this independently for each map label, but use the same global variables t. For each resulting collection of partitions append all these conditions to C. This is a finite rational linear system, possibly with strict inequalities. Its feasibility is decidable, as shown below. If every system is infeasible, return NO.

For soundness, take a feasible system. Its rational solution t gives, after removing duplicate points, ordered pairs

0=x_0 < x_1 < ... < x_k=L_e,
0=y_0 < y_1 < ... < y_k=R_e.

Define f_e on [x_j,x_{j+1}] by linear interpolation between (x_j,y_j) and (x_{j+1},y_{j+1}). Every slope is positive. The pieces agree at their endpoints. Thus f_e is continuous, strictly increasing and onto [0,R_e]; its inverse is continuous. It satisfies every sample request and has rational breakpoints and values.

For completeness, suppose real homeomorphisms and a real t solve the input. For each e sort the sampled X values and group equal values. Since f_e is increasing and injective, the Y values have exactly the same strict order and exactly the same equality classes. This ordered partition occurs in our finite enumeration, so its linear system has a real solution and will be accepted. The rational-feasibility argument below replaces it by a rational one without changing any requested order or equality. This proves both directions and termination. QED.

### Exact rational linear feasibility

Write each inequality as a.x<=b, marking it strict when appropriate. Replace an equality by two weak inequalities. Eliminate one variable z. A positive z coefficient supplies an upper bound; a negative coefficient supplies a lower bound. Every lower-upper pair gives the condition that its lower bound does not exceed its upper bound; this condition is strict if either bound is strict. Bounds with zero z coefficient are retained. This is Fourier-Motzkin elimination over the rationals.

The projection is exact. Necessity follows by substitution. For sufficiency, finitely many lower bounds have a largest value and finitely many upper bounds have a smallest value. The pair inequalities guarantee either a nonempty interval, or a singleton at which both bounding conditions are weak. If one kind of bound is absent, there is a one-sided unbounded interval. Choose a rational point: the midpoint for a bounded nonsingleton interval, the endpoint for an allowed singleton, or a rational point one unit beyond a finite one-sided bound. Reverse the eliminations. At dimension zero the only possible contradictions are 0<=b with b<0, or 0<b with b<=0. Every step is finite and exact.

This also proves that every nonempty finite mixed strict/weak rational polyhedron has a rational point. No floating-point feasibility tolerance is needed.

## 3 Encoding a regular finite boundary itinerary

The following is an explicit input format, not an assertion that every target lamination has such a certificate.

For each ideal edge e, its two ordered fans have n_e and m_e face incidences. The interval coordinates are [0,n_e] and [0,m_e]. A face incidence is a unit subinterval; after choosing canonical directions, a port coordinate has the form a+t or a+1-t for an integer a.

A finite regular itinerary diagram specifies:

- a finite collection of nonempty cyclic words in the actual boundary branches and transition ports;
- a transverse height variable for each marked branch occurrence;
- its chosen unit sector and the strict bounds 0<t<1;
- affine coordinate transport along each branch;
- every transition as one canonical graph request f_e(X)=Y;
- the equalities closing each cyclic word, including the final height;
- any required identifications or distinctness of marked occurrences.

Regular here explicitly excludes trajectories through fan subdivision points, sector endpoints, limiting cusp separatrices, and infinitely many transitions in a finite itinerary. Such phenomena are not discarded from the original question. They are outside this finite input class.

For a prescribed simple boundary circle, require distinct heights at distinct visits to the same physical boundary branch. More generally, impose any needed no-collision conditions on repeated ports. A condition t_i!=t_j is handled by the two finite alternatives t_i<t_j and t_j<t_i. An itinerary that intentionally repeats a smaller closed orbit must instead be quotient-recorded; one cannot label its unreduced multiple as a simple curve.

### Corollary 2

For a supplied regular finite diagram, compatibility with shared increasing edge maps is decidable, with rational piecewise-linear witnesses when feasible.

### Proof

Each transport, sector condition and closure condition is a rational affine condition. Every transition is a request of Theorem 1. Resolve any finitely many disequalities into finitely many strict-order cases. Apply Theorem 1 to each case. It handles all cusp components simultaneously because occurrences with the same global e have the same map. QED.

A solution exactly preserves the selected finite diagram. It does not say that every unmarked orbit is periodic, that all boundary components share the desired global behavior, or that a topological lamination has already been supplied.

## 4 A bounded finite output

Fix finite boundary incidence data, verified peripheral integral cocycles, and a nonnegative integer N. There are finitely many nonempty cyclic transition words of total length at most N and finitely many associated choices of ports and strand ordering requirements. Enumerate them and apply Corollary 2. For each accepted word, its homology pair is the sum of the cocycle evaluations along the word; transitions within a contractible port neighborhood contribute no additional ambiguity once the incidence model is fixed.

Thus the algorithm returns exactly the finite set of peripheral homology tuples admitting **regular finite compatible diagrams of that bound**. A nonzero homology pair may be reduced to a primitive unoriented pair (p,q), identifying (p,q) and (-p,-q). Zero homology is not called a slope. No meridian or longitude is guessed when the input has not specified a basis.

This is a finite output theorem for the finite class, not a finite-output theorem for all carried slopes. Letting N increase recursively enumerates all such finite compatible diagrams and their rational homology labels. It does not halt on the nonexistence of a diagram of arbitrary length, does not decide the original slope-membership problem, and does not describe irrational boundary behavior.

## 5 Shared cusp constraints give actual obstructions

Consider one unknown increasing f:[0,2]->[0,2]. Suppose one requested transition has x in (0,1), y in (1,2), and another has x' in (1,2), y' in (0,1). Each request alone extends to an increasing homeomorphism fixing the endpoints. Together they cannot: x<x' forces f(x)<f(x'), whereas y>y'.

This obstruction is not captured by allowing an independent map at each cusp end. The same issue occurs if two requests have the same input and different outputs, or the same output and different inputs. Both equality directions are necessary.

This is a local compatibility obstruction, not a constructed counterexample triangulation and not a counterexample to Question 7.3. Zung's use of repeated edge maps in section 5 is relevant prior motivation. We make no novelty claim for monotonicity or interpolation.

## 6 Why pointwise closure is weaker than all leaves closed

### Proposition 3

No finite set of point evaluations agreeing with the identity can, in the unrestricted class of increasing circle homeomorphisms, certify that the suspension consists entirely of compact leaves.

### Proof

Let A be the finite set of sampled points on a circle. Choose a closed arc [a,b] in its complement and a point c in its interior. Choose d with c<d<b in an oriented coordinate on the arc. Let g be the piecewise-linear increasing map which fixes a and b, sends c to d, is linear on [a,c] and [c,b], and is the identity outside this arc.

The map is an orientation-preserving circle homeomorphism and agrees with the identity on A. On the interior of [a,b], g(x)>x. Hence all positive iterates of such x strictly increase within [a,b]; none is periodic. Outside that interior, every point is fixed.

In the suspension, a leaf is compact exactly when the corresponding point has a finite orbit. The identity suspension has only compact leaves. The suspension of g has compact leaves through all sampled points but noncompact leaves through every point in the open modified arc. Therefore the finite evaluations cannot distinguish the required global property. QED.

When A is rational, a,b,c,d may all be chosen rational, so the counterexample already occurs among rational piecewise-linear maps. This does not say that a complete finite PL map cannot be checked for a functional identity: it can. It says that the interpolation theorem, which only preserves finitely many marked orbits, does not impose that identity on unsampled points.

### A global certificate that can be checked once supplied

The previous obstruction concerns incomplete point samples. A full return map supports a stronger exact check.

### Theorem 4

Suppose a boundary foliation has been independently identified with the suspension of an orientation-preserving circle homeomorphism with a supplied rational piecewise-linear lift F:R->R satisfying F(x+1)=F(x)+1. Fix relatively prime integers p,q with q>0, in the basis determined by the supplied suspension section. Whether every boundary leaf is closed of slope (p,q) is decidable from F: the necessary and sufficient condition is

F^q(x)=x+p for every real x.

This theorem assumes the global suspension section, its peripheral basis, and the chosen lift; it does not produce them from an arbitrary triangulation. Here q counts positive section crossings and p is the corresponding lift displacement. A class with q=0 is outside this global-section model. Replacing F by F+k for an integer k changes p to p+kq. A negative result concerns the supplied map, not existence of a different map realizing the class.

### Proof

In the suspension, the leaf through a point is closed exactly when its orbit under the circle return map is periodic. Following a closed leaf through q successive returns to the section with lifted displacement p gives its peripheral homology pair (p,q). Thus the displayed identity implies that every orbit closes with this pair. Its minimal return period cannot be smaller than q, since p/q is reduced. Conversely, if every leaf is a closed curve of primitive slope (p,q), the return orbit of each point closes after q steps with lifted displacement p, giving the identity pointwise.

It remains to decide the identity. Represent F on [0,1] by its finite rational graph. The composite of two rational PL degree-one lifts is rational PL on [0,1]. Its possible breakpoints are the inner map's breakpoints together with preimages, under the inner map, of the finitely many relevant integer translates of outer breakpoints. Monotonicity gives unique rational preimages by linear interpolation. Only finitely many translates lie in the compact image of [0,1]. Induction constructs F^q exactly. The difference F^q(x)-x-p is affine between consecutive resulting breakpoints. It vanishes identically if and only if it vanishes at every breakpoint. This is a finite rational comparison. Periodicity extends the conclusion from [0,1] to R. QED.

This provides a checkable way to certify the all-closed boundary condition for a **supplied** rational PL global return map. There is no claim that every all-closed realization on a fixed taut carrier admits such a rational PL certificate, that a compatible set of edge maps with this return identity can be found, or that the other geometric hypotheses have been checked.

## 7 The separate geometric bridge

The finite compatibility theorem itself needs no three-manifold theorem. To use one of its outputs as an essential-lamination witness, the following must additionally be established for the chosen geometric model:

1. Its interval maps actually glue all sector products into a globally embedded, properly carried lamination in the original fixed carrier.
2. That lamination is fully carried by a carrier satisfying the relevant incompressibility, irreducibility, no-monogon, no-Reeb-component and no-disk-of-contact conditions, including the required boundary formulation.
3. Its boundary behavior satisfies the chosen definition of realization of a slope.

There is a standard sufficient theorem for step 2. The Gabai-Oertel criterion, stated in [Li, Proposition 1.1(b)] and [AL, Theorem 2.3(2)], makes a fully carried lamination essential when the specified carrier conditions hold. Lackenby identifies the taut carrier with an incompressible Reebless homology branched surface [L, manuscript p.6], and his Proposition 10 establishes incompressible torus boundary. These are important prior tools, rather than consequences of Theorem 1.

Zung gives the complete sector-gluing recipe in [Z, section 2.3] for his canonical veering setting. Locally it uses ordered fans, the absence of triple points, and product face sectors. This motivates the same finite encoding for a taut carrier. No result in this attempt promotes every arbitrary finite diagram to a checked essential-lamination boundary certificate on every taut ideal triangulation.

Even if steps 1 and 2 are supplied by the standard full interval-gluing construction and the cited carrier criterion, step 3 remains independent. A compact marked boundary orbit does not imply that the entire boundary lamination consists of closed curves. Proposition 3 is a direct proof of this gap. The half-sink-disk warning in [C] is retained: the absence of interior sink disks is not permission to apply a boundary extension/splitting theorem without checking its extra hypotheses.

This separation avoids claiming either that taut carriers never support essential laminations or that their essentiality automatically supplies prescribed peripheral behavior.

## 8 The source example checks the peripheral basis

The discrepancy between the two boundary conditions is not merely terminology. In [Z, section 5, pp.14-15], the example is the complement of the knot 10_145. Figure 8(c) is identified there as a meridian, with picture slope 0, and Lemma 5.1 asserts the corresponding holonomy realization. On p.15 the paper supplies the actual peripheral vectors in that picture:

lambda=(6,-1), mu=(-1,0).

Thus the picture slope 0 is geometrically the meridian mu. It is not standard 0-surgery (the longitude lambda). Under the usual coefficient convention lambda+s*mu, that meridian corresponds to the infinite surgery coefficient. Lackenby's exclusion in [L, section 4(2)] is the geometric meridian and does not depend on a numerical basis.

These inspected source claims do not establish a contradiction. Zung's stated witness is a holonomy solution with the indicated boundary curve, whereas Lackenby's definition imposes the stronger whole-boundary condition. In addition, this comparison does not identify every full-carrying, precise-carrier and global-essentiality hypothesis between the displayed holonomy witness and Lackenby's filling conclusion. No complete geometric identification of the two constructions is asserted. The boundary-condition difference already prevents the proposed transfer, but it is not claimed to be the only difference between all relevant hypotheses. We do not claim that Zung's meridional solution extends across meridional filling as a taut foliation. His own Lemma 5.2 uses the impossibility of the relevant taut foliation on S^3 as an obstruction to a different, positive holonomy solution.

This basis check rules out a misleading numerical explanation. Independently, Proposition 3 proves why the finite periodic-orbit theorem cannot be advertised as enumerating a subset of Lackenby's carried slopes.

## 9 Other attempted routes and the remaining obstruction

**Measured branch weights.** Nonnegative solutions of linear switch equations encode invariant transverse measures. They can test a strictly narrower problem. No theorem here turns an arbitrary unmeasured lamination into a measured one preserving boundary slopes. The finite holonomy formulation retains the actual repeated-map order constraints instead.

**Agol-Li existence detection.** [AL] supplies algorithms and semialgorithms for full carrying and laminar-manifold detection under its stated hypotheses. Its positive and negative procedures do not themselves impose a specified peripheral holonomy or the requirement that the original fixed carrier and every boundary circle condition survive. Dehn filling or doubling is not used to erase these relative requirements. No boundary-preserving reduction or termination theorem was obtained.

**Veering polynomials and flow results.** [LMT1] studies the polynomial and carried-surface homology/Thurston face. [LMT2] studies associated flows and growth. Neither is an all-lamination boundary algorithm. The authors are Landry, Minsky and Taylor. [Z] is not a veering A-polynomial paper and its canonical-flow criterion is not silently generalized.

**The exact residual.** A solution to the full target still needs a specified boundary convention and effective output language; a global realization/completeness theorem for all laminations carried by the fixed B, including non-full and nongeneric cases if they are admitted; and a terminating treatment of unbounded or infinite holonomy and global peripheral constraints. Under the closed-boundary convention, the missing constraint is genuinely functional, not just a finite set of point equalities. Under a real-slope convention, a representation theorem for the full slope set and effective endpoint/infinite-orbit control are additionally absent.

The finite theorem is therefore a useful exact compatibility layer and a rigorous obstruction to an invalid shortcut. It is not a claimed algorithm or counterexample for Question 7.3. The first attempt remains unresolved, with these partial results.

## Review status

The [mathematical audit](MATHEMATICAL_AUDIT.md) accepts the finite shared-map compatibility theorem, the bounded regular-diagram conclusion, the finite-sampling obstruction and the supplied global PL return-identity theorem at their stated scope. All geometric realization, essentiality and boundary-convention hypotheses remain separate. This AI-assisted, unrefereed proof-and-audit edition is not external human peer review, journal acceptance or formal proof-assistant certification. No historical novelty or current-openness certification is made; the original universal boundary-slope algorithm remains unresolved by this work.

## References

[C] Danny Calegari, Problems in foliations and laminations of 3-manifolds (2002), Question 7.3, PDF p.13. https://arxiv.org/abs/math/0209081

[L] Marc Lackenby, Taut ideal triangulations of 3-manifolds, Geometry & Topology 4 (2000), 369-395. Author manuscript pp.2,5-6,21,26; DOI 10.2140/gt.2000.4.369. https://people.maths.ox.ac.uk/lackenby/tit-gt.pdf

[Li] Tao Li, Laminar Branched Surfaces in 3-manifolds, Geometry & Topology 6 (2002), 153-194, Proposition 1.1 and boundary-scope note in section 1. https://arxiv.org/abs/math/0204012

[AL] Ian Agol and Tao Li, An algorithm to detect laminar 3-manifolds, Geometry & Topology 7 (2003), 287-309, Theorems 2.3,2.8,3.5,3.6 and section 4. https://arxiv.org/abs/math/0201310

[Z] Jonathan Zung, Veering triangulations and transverse foliations, arXiv:2411.00227v1 (2024), sections 1,2.3,5. The version inspected is a preprint. https://arxiv.org/abs/2411.00227

[LMT1] Michael Landry, Yair Minsky and Samuel Taylor, A polynomial invariant for veering triangulations, arXiv:2008.04836. https://arxiv.org/abs/2008.04836

[LMT2] Michael Landry, Yair Minsky and Samuel Taylor, Flows, growth rates, and the veering polynomial, arXiv:2107.04066. https://arxiv.org/abs/2107.04066
