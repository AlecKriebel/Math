# Independent exact special-arrangement derivations

These derivations precede candidate exposure. Mechanisms were suggested in the assignment (Hesse covers, supersolvable arrangements, Fermat deletions), so this is **not blind rediscovery**. No candidate theorem or code was used.

## 1. Cover lemma, with the complete line exception

Let Z be nonempty and finite, k=max_L #(L intersect Z), over all complex projective lines. Suppose finitely many projective lines L_j and nonnegative rational weights w_j satisfy a_p=sum_{j:p in L_j} w_j>=1 for every p in Z and W=sum w_j<=k. For an irreducible reduced curve C which is not a line, proper Bezout gives

    W deg C >= sum_{p in Z} a_p mult_p(C) >= sum_{p in Z} mult_p(C).

This also applies to a line distinct from all positively weighted L_j. For every line, including cover components and auxiliary lines, the direct definition gives sum mult_p(L)=#(L intersect Z)<=k. Thus epsilon(Z)=1/k. One must not apply proper Bezout when C is a component of the cover. A reduced or nonreduced curve decomposes into irreducible components and its degree and point multiplicities are additive; the same bound follows if each component is separately checked. The Seshadri definition needs only irreducible reduced curves.

The lemma is a sufficient certificate, not a necessary condition for the conjecture. Failure of the finite arrangement-component LP proves neither failure of the conjecture nor that no auxiliary-line certificate exists.

## 2. Hesse exact construction and obstruction to component-only covers

Work over Q(w), w^2+w+1=0, with H consisting of x=0, y=0, z=0 and x+w^i y+w^j z=0 for i,j=0,1,2. Independent cross products and exact incidence evaluation give 21 singular points, t_2=12 and t_4=9. Their pair joins are exactly 57 lines: 36 contain 2 points, 9 contain 4, and the 12 H components each contain 5. Hence k=5 for all projective lines: every line with two or more Z-points occurs among these pair joins, while all other lines contain at most one.

An exact cover of all 21 points is

    y=0,
    x+w^2 y+w z=0,
    x+y+w z=0,
    x+w y+w z=0,
    x-w z=0.

The last line is auxiliary. The first four meet at P=[1:0:-w^2], a quadruple point of H. Every other Z-point lies on exactly one selected line, and P lies on four. The product cover polynomial has degree 5 and curve multiplicity sum 24=20+4. The cover lemma gives for every curve distinct from its component lines

    sum_{p in Z} mult_p(C) <= 5 deg C - 3 mult_P(C).

Cover components themselves have at most 5 Z-points, including the auxiliary component, which has 4. This proves epsilon(Z)=1/5 for this concrete Hesse arrangement. No uniqueness/classification assertion is needed.

There is no component-only fractional line cover of cost <=5. Each H component contains exactly two double points, and each of the 12 double points lies on exactly two components. Summing the 12 required coverage inequalities gives 2 sum_j w_j>=12, hence cost>=6. This is a falsifier for promoting a component-only cover mechanism to all arrangements. The auxiliary line is what resolves this case.

The coordinates agree with the actual primary paper *Companion varieties for Hesse, Hesse union dual Hesse arrangements* (Pietro De Poi and Giovanna Ilardi, J. Commutative Algebra 15 (2023), 1--13), Example 3.1. The repository-hosted PDF's indexed source excerpt was read by web browse; local-byte download failed with TLS handshake and web opening timed out. This is therefore **excerpt-level** exposure, not a claimed full-PDF/fresh-byte read. Its coordinate description was independently recomputed. The additional locally downloaded actual primary dependency is Hanumanthu--Harbourne. No secondary site was used to justify the mathematics.

## 3. Supersolvable arrangements, and a broader small-extra-lines case

If P is a modular point incident with m component lines, every singular point other than P lies on one of those m lines. For a nonpencil arrangement choose a component L not through P. L intersects those m lines in m distinct singular points, so k>=m. The m pencil lines cover Z, so the cover lemma proves the conjectural value for **every** such supersolvable arrangement. Pencils were handled separately in source_scope.md.

More generally, take m>=2 distinct lines through P and r<=2 further distinct lines not through P. If r=0, it is a pencil. If r=1, k=m from the added line, and the m pencil lines cover Z. If r=2 and the two added lines meet at Q on a pencil line, all Z is covered by the pencil and k>=m. If Q is off every pencil line, the m pencil lines together with the auxiliary line PQ cover Z; either added line has m+1 distinct Z-points, so k>=m+1. This proves the conjectural value in both cases without presuming supersolvability in the last case.

The actual primary source Hanumanthu--Harbourne, *Real and complex supersolvable line arrangements in the projective plane*, arXiv:1907.07712v1, defines modularity as used here. The derivation above is elementary and does not need any classification claim from that paper.

## 4. Fermat one-family deletion theorem, including fully deleted family

For n>=2, let mu_n be the n-th roots of unity. The full Fermat arrangement has lines A_alpha:x-alpha y=0, B_beta:y-beta z=0, C_gamma:z-gamma x=0. Its singular set S consists of an n by n grid of points with all coordinates nonzero and the three coordinate vertices. Each original Fermat component contains n grid points and its pencil vertex, hence n+1 points.

For every arbitrary projective line L: if it is an original Fermat line its S-count is n+1; if it contains a coordinate vertex and is not an original Fermat line, it contains no grid point (each grid point is already on the unique corresponding Fermat pencil line through that vertex); if it contains no coordinate vertex, intersecting the degree-n union of any one pencil bounds its grid-point count by n. Coordinate lines contain two vertices and no grid points. Thus max_L #(L intersect S)=n+1, with the n=2 boundary included.

Delete **any subset of A-lines**, possibly all n, retaining all B- and C-lines. Every grid point remains singular because its B and C components remain. Both B and C vertices remain singular because n>=2. The A vertex remains iff at least two A-lines survive. A retained B-line contains all its n grid points and the B vertex, so k=n+1 still. All original n A-lines, now allowed as auxiliary lines when deleted, together with z=0 form a degree-(n+1) cover of the remaining singular set. Therefore epsilon=1/(n+1) for every one-family deletion, including n=2 and deleting all A-lines.

For deletions across multiple families, only Z subset S and k<=n+1 follow automatically. A surviving line can lose singular grid points if both other incident components are deleted. Neither the one-family upper-bound witness nor the exact value may be transferred without a fresh incidence check. The independent exact program exhausts all 1-, 2-, and 3-line deletions of F_3 as a checkable finite falsifier set; it does not infer an infinite-family claim from this enumeration.

Pokora, arXiv:1711.09364v3, Example 3.4 supplies the original CEVA/Fermat family and its undeleted Seshadri value, while Proposition 3.3 uses the absence of double points. After deletion that absence can fail; the replacement mechanism here is an auxiliary-line cover.

## 5. Multiplicity, genus, and numerical-only limitations

Arrangement multiplicity r_p counts component lines through p. Curve multiplicity m_p(C) is the local order of the curve equation and is generally unrelated. Bezout with the arrangement gives D deg C>=sum r_p m_p(C) only when C is distinct from every arrangement component. Incidence on one arrangement line gives sum_{p on L}(r_p-1)=D-1, whereas an auxiliary line merely has sum_{p on L} r_p<=D, because distinct arrangement intersections can be counted once per component. Replacing r_p by r_p-1 for arbitrary lines has no basis.

For irreducible plane C, the genus inequality is sum_p m_p(C)(m_p(C)-1)<=(d-1)(d-2). This holds for any chosen subset of points, but the corresponding vector feasibility test omits geometric realization. In particular, multiplicity-one points cost zero genus, so the genus bound alone cannot prove a linear total multiplicity bound: a formal degree-5 vector of 26 ones passes the genus inequality yet exceeds 5d. No existence of such a curve or arrangement is asserted.

An irreducible nodal cubic y^2 z-x^3-x^2 z was checked exactly on a rational arrangement. The local curve orders were computed by dehomogenization and exact Taylor expansion, independently of arrangement multiplicities. Irreducibility follows from y^2=x^2(x+1) over C(x), since x+1 is not a square. The node [0:0:1] has curve multiplicity 2, despite its arrangement multiplicity being 4 in the test arrangement. Full coordinates and results are retained in stdout.

## Exact remaining gap before candidate exposure

The verified results are concrete Hesse, all supersolvable arrangements, m-pencil plus <=2 extra lines, and every one-family deletion of Fermat n>=2. The general source conjecture requires a geometric argument or counterexample for arbitrary reduced complex arrangements. Neither a component-only covering LP nor numerical genus/incidence vector feasibility establishes that general result. No full-solution, novelty, global-current-open-status, or acceptance certificate is claimed.
