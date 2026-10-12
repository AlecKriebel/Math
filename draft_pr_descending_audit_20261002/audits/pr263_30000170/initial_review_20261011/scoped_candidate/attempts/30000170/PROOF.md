# Nonunique nearest stable complex quadratics near z²

**Mathematically accepted complex projection result; direct credited note preparation GO; publication pending.** Root accepted the core theorem, whole-read the v1 candidate, and reproduced its 2005 rational controls. This framing revision has its own manifest and awaits final exact-version review. Author turns remain **1/5**. Original reviews certify only their original body; no firstness or present-openness claim is made.

## 1. Exact accepted claims

Identify monic complex quadratics p(z)=z²+az+b with C²=R⁴, in coordinate order (Re a,Im a,Re b,Im b). Let alpha(p) be the maximum real part of a root, and let S={p:alpha(p)≤0}. Distances use any **fixed positive-definite real coefficient inner product**.

**Theorem A.** S is not prox-regular at p0(z)=z². Every neighborhood of p0 contains an unstable polynomial with at least two distinct attained global nearest stable monic quadratics.

**Theorem B.** The same conclusions hold for full exact-degree complex quadratics lz²+az+b, l≠0, near (1,0,0), with every fixed positive-definite real coefficient inner product.

**Theorem C.** The abscissa epigraph is not prox-regular, as a set, at (p0,0), in either framework. Its obstructing limit is a horizontal normal vector in a coefficient/height product metric. In a metric mixing coefficient and height coordinates, the limit is a horizontal support covector; its representing normal vector may tilt.

These core claims concern complex coefficients and the whole epigraph. They make no negative finite-subgradient function claim. A separately accepted positive quadratic function lemma is compatible with them and is described in §8 without becoming a proof premise. The real-only general problem, general-degree function conjectures, all-degree failure, and an explicit nonunique input/minimizing pair remain excluded. Stability is the closed-half-plane convention ≤0. Firstness and present openness are not asserted.

## 2. Necessary fixed-normal support and projection criterion

A limit of proximal normals at converging points is a limiting normal. Set prox-regularity at x0 requires a uniform local nearest-point condition for each limiting normal n0∈N_C(x0). In particular it implies, with some finite rho,

    <n0,y-x0>≤(rho/2)||y-x0||²

for nearby y∈C. This follows by expanding the distances from x0+n0/rho to x0 and y. Therefore a limiting normal that is not proximal at the base disproves set prox-regularity. In finite dimension, local single-valued nearest projection onto a closed set is equivalent to set prox-regularity. [Poliquin–Rockafellar–Thibault (2000), Definition 1.1, Proposition 1.2, Theorem 1.3(a),(k), pp.5233–5234](https://sites.math.washington.edu/~rtr/papers/rtr170-LocalDiffDistance.pdf).

## 3. Stable path and actual ambient normals

For t>0, use

    p_t(z)=z²+t²z+t²+it³=(z+it)(z+t²-it).

Its roots are -it and -t²+it. The active root is simple and strictly dominates the other root locally at each fixed t. Implicit differentiation at lambda=-it gives

    d lambda=-(lambda da+db)/(t²-2it),
    grad alpha(p_t)=gamma n_t,
    gamma=2/[t(t²+4)]>0,
    n_t=(-t,-t²/2,-t/2,1).

All four real coefficient directions are included. To independently check the sign and stability boundary, write a=x+iy,b=u+iv and shift the root variable by -iy/2. The new polynomial is

    w²+xw+U+iV, U=u+y²/4, V=v-xy/2.

The quadratic formula gives exactly x≥0,U≥0,V²≤x²U for stability. For x>0,U>0 this is |V|≤x sqrt(U). At p_t the upper constraint is active; the lower one has slack 2t³. The gradient of v-xy/2-x sqrt(u+y²/4) is n_t, with outward sign. The closed chart also includes the edge restrictions x=0⇒V=0,U≥0 and U=0⇒V=0,x≥0.

At each fixed t, a smooth local sublevel Taylor bound gives <n_t,y-p_t>≤K_t||y-p_t||² for nearby stable y. Taking a sufficiently small positive normal displacement makes p_t nearer than every distinct nearby stable point. Taking the displacement also below half a chosen local ball's radius excludes remote competitors by the triangle inequality. Hence n_t is genuinely proximal. No uniform K_t or root gap is assumed.

Since p_t→p0 and n_t→n0=(0,0,0,1), the vector n0 belongs to the limiting normal cone at p0.

## 4. Cubic support versus quartic distance

Let w_t=p_t-p0=(t²,0,t²,t³). Then

    <n0,w_t>=t³,
    ||w_t||²=2t⁴+t⁶,
    <n0,w_t>/||w_t||²=1/[t(2+t²)]→+∞.

For every tau>0, the squared-distance difference from p0+tau n0 is

    ||w_t-tau n0||²-||tau n0||²
      =2t⁴+t⁶-2tau t³<0

for sufficiently small t. The competitors approach the base arbitrarily closely. Thus n0 is limiting but not proximal at p0, so the local prox-regularity condition fails already at that fixed normal.

An equivalent rational comparison uses n_t and the stable base: <n_t,p0-p_t>=t³/2 and ||p0-p_t||²=2t⁴+t⁶. The original sqrt(2) two-moving-point argument remains in the immutable original submission and its historical controls; the revised core does not need it.

## 5. All fixed positive-definite coefficient metrics

For any fixed SPD matrix G, the covector n_t represents the metric normal vector G⁻¹n_t. The preceding proximal-normal argument remains valid using the positive minimum eigenvalue of G. Its limit is G⁻¹n0 and

    <G⁻¹n0,w_t>_G=n0^T w_t=t³.

Write w_t=t²e+t³f, with e=(1,0,1,0),f=(0,0,0,1). Then

    ||w_t||_G²=t⁴[e^TGe+2t e^TGf+t² f^TGf],
    e^TGe>0.

The quotient therefore diverges for every fixed SPD G, including coupled coefficient metrics. This proves a metric support obstruction; mere equivalence of arbitrary norms is not used.

The monic abscissa is continuous, including at multiple roots, by

    alpha(a,b)=[-Re(a)+sqrt((|a²-4b|+Re(a²-4b))/2)]/2.

Thus S is nonempty and closed. Distance minima exist: a minimizing sequence is bounded using p0 as a finite-distance competitor, and a convergent subsequence attains its infimum. The projection criterion in the Hilbert metric G now supplies non-single-valued projections arbitrarily close to p0. Since minima exist, each such projection has at least two points. A stable input has only itself as its distance-zero projection, so the inputs are unstable. This proves Theorem A.

## 6. Full exact-degree normals and global localization

For lz²+az+b, direct differentiation at the same monic point gives

    d lambda=-(lambda² dl+lambda da+db)/(t²-2it),
    grad alpha(p_t)=gamma N_t,
    N_t=(t³/2,-t²,-t,-t²/2,-t/2,1).

The first two entries are leading-coefficient directions. These are genuine six-dimensional proximal normals locally, and N_t→N0=(0,0,0,0,0,1). The displacement has zero leading coordinates. Its support is again t³ and its squared metric distance has order t⁴ with a positive leading coefficient. For an arbitrary full coefficient SPD G, the normal vector is G⁻¹N_t. The proof uses the full ambient space, rather than inheriting a conclusion from a monic slice.

The full stable set is relatively closed where l≠0, since alpha(l,a,b)=alpha(a/l,b/l) is continuous there. Choose a closed metric ball C0 of radius R around (1,0,0) so small that l≠0 throughout. Its stable intersection C is nonempty and compact. Eventually the path lies in the interior, with its normals unchanged, and the same obstruction makes C non-prox-regular at the base.

If ||q-p0||_G<R/3, every stable s outside C0 obeys

    ||s-q||_G≥||s-p0||_G-||q-p0||_G
              >R-||q-p0||_G>2R/3.

The competitor p0 is less than R/3 away; boundary points of C0 also cannot minimize. Thus nearest points in compact C and in the entire full exact-degree stable set agree. The closed-set projection criterion supplies arbitrarily nearby nonunique minima which are attained global nearest full-degree stable quadratics. This proves Theorem B for every fixed SPD coefficient metric.

## 7. Whole-epigraph set obstruction

At (p_t,0), the epigraph is locally alpha(p)-r≤0. Its scaled outward normal covectors are

    v_t=(n_t,-1/gamma)=(n_t,-t(t²+4)/2)

and, in full degree, (N_t,-1/gamma). They are proximal at each smooth boundary point and converge to (n0,0) or (N0,0). The comparison points (p_t,0) have zero height displacement, so the limiting covector's support is t³ and the squared Euclidean displacement is 2t⁴+t⁶. It is nonproximal at the base, proving Theorem C.

For coefficient metric G and the ordinary height metric, the representing normal limit is (G⁻¹n0,0), which is horizontal. For a fixed SPD epigraph metric H mixing coordinates, the vector H⁻¹v_t still has the same covector support; the displacement retains a positive order-four squared-distance coefficient. Non-prox-regularity persists, although its representing limit vector may tilt. The monic epigraph is closed; full-degree local closedness is handled by clipping to a small closed ball within l≠0.

The unscaled coefficient gradients diverge because their imaginary-constant component is gamma. Function prox-regularity at a fixed finite subgradient localizes near that subgradient and corresponds to the epigraph normal (v,-1). This horizontal witness does not test that property. [Poliquin–Rockafellar (2010), Definition 1.1 and p.205](https://www.heldermann-verlag.de/jca/jca17/jca0849_b.pdf).

## 8. Current historical framing, classical credits, and exclusions

Lewis's *The Mathematics of Eigenvalue Optimization* (2003), **Section8, printed pp166–168**, explicitly formulates the stable-set question in complex Euclidean monic coefficient space. The core theorem gives a negative degree-two answer to that historical set question. [Primary author-posted paper](https://people.orie.cornell.edu/aslewis/publications/03-mathematics.pdf). This historical question does not establish present openness.

Printed OWR Question1 omits field, metric, and monicity; those omissions remain disclosed when it is cited. Its surrounding prose does not contain the imported “Equivalently.” The related Lewis epigraph definition is in *Eigenvalues and nonsmooth optimization*, **Section1.7,p15**; Section1.6 discusses partial smoothness. Current source notes correct that locator while preserving historical copied review bytes.

The real-quartic stability boundary is classical, as in [Bottema1956](https://onkirillov.narod.ru/1956-IM-Bottema-WhitneyUmbrella-ZieglerParadox.pdf), and its Whitney-umbrella presentation appears in [Kirillov–Overton2013](https://cs.nyu.edu/~overton/papers/pdffiles/swallowtail.pdf). The complex quadratic chart has this classical shape. Its nonlinear coordinate identification does not by itself transfer projection in a fixed metric; the direct ambient normal/support argument supplies the needed step. Prior Burke–Overton/Lewis root/abscissa calculus and PRT's local projection theorem are credited. Ordinary root differentiation and the cusp mechanism are not claimed novel.

Cross2010's full dissertation is recovered, and independent priority reviewers read complete chapter5, printed pp80–133. Its standard finite-subgradient definitions and restricted parameter examples are distinguished from the ambient coefficient projection theorem. Earlier unrecovered-thesis statements are only dated 2026-10-01 access records. The full 2009 talk body remains unknown.

Two later primary recoveries are now credited. [Moses–Liu1991](https://www.academia.edu/329556/Determining_the_Closest_Stable_Polynomial_to_An_Unstable_One) recognizes possible global nonuniqueness for real monic disk-stable coefficients with weighted Euclidean objectives; its complete public author-linked article OCR pp901–906 was read. The original typeset PDF and Figure1 were not recovered, so this is an OCR-body finding with a retained visual gap. Generic nonuniqueness is not claimed as a discovery here; no exact local complex theorem was located in the OCR read.

[Orban de Xivry2013, Nearest Stable System](https://research.dial.uclouvain.be/bitstreams/930fe0d3-f488-439c-bce1-37a8dc368917/download), is a recovered 214-page primary Open Access thesis. Relevant theory and complete polynomial Chapter4 were independently read; complex monic coefficient formulation is explicit at p144, and weighted objectives are discussed at pp175–180. No exact core A–C theorem was located in the audited chapters. The thesis is credited as prior complex polynomial projection/algorithm work, without asserting an exhaustive negative read of all 214 pages. Its Example22 has a displayed numerical distance inconsistency; neither it nor its matrix candidates is a premise or a verified global/local tie here.

Combettes–Trussell1992 and the separate Orban–Nesterov–Van Dooren2013 journal article remain genuinely unread full bodies. The recovered thesis is not assumed identical to the journal article. No absence inference or firstness/application-priority clearance follows.

A separate cold-reviewed auxiliary result establishes the **positive** finite-subgradient function property for the monic complex-quadratic abscissa at the origin in the real Euclidean coefficient metric. Constants depend on each fixed finite limiting subgradient; the root mathematical acceptance includes the strict-inequality repair r=M+1. This is compatible with the whole-epigraph set obstruction at a horizontal normal. The core proof above does not depend on it. Original reviews and the bounded priority decision do not certify auxiliary novelty or the final manuscript/package.

Root's bounded decision permits **direct credited proof-note preparation**. Unconditional novelty/application priority remains **HOLD**, and final root exact-version/publication review is pending. No firstness or present-openness claim is made. Real monic quadratics have the convex stability orthant a≥0,b≥0, so this complex construction is not a real-only general counterexample. General-degree function conjectures, all-degree failure, and an explicit input or nearest pair remain excluded.
