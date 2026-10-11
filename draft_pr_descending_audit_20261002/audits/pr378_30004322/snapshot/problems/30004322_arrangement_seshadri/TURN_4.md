# Turn4: deletion resilience of the Fermat Seshadri value

Fourth substantive turn, general source unresolved. The full Fermat/CEVA value is a credited result of Pokora, Example3.4 following Proposition3.3 in https://arxiv.org/pdf/1711.09364v3 . This turn gives explicit sufficient deletion criteria retaining that value and exact incidence formulas. It does not claim a new value for the full arrangement or historical novelty for these deductions.

## 1. Full arrangement and its credited bound

Fixn≥3 and a primitive nth rootζ. Index the three pencils byG=Z/nZ:

    A_a: x=ζ^a y,     B_b: y=ζ^b z,     C_c: z=ζ^c x.

A grid point is incident to the triple(A_a,B_b,C_c) exactly whena+b+c=0. The singular setZ₀ consists ofn² grid points and three coordinate vertices. Each component has n grid points plus its pencil center, hence n+1 singular points.

For reference the full value has a short credited Bézout proof: the sum of all3n lines has multiplicity at least3 at everyZ₀ point. An integral curve not one of these lines therefore has ratio at least1/n. The components have ratio1/(n+1). Consequently

    epsilon(Z₀)=1/(n+1),        mpl(Z₀)=n+1.             (1)

The collinearity conclusion also follows directly: any line outside the3n components contains at mostn points by the same Bézout calculation.

Delete arbitrary index setsD_A,D_B,D_C, with sizesd_A,d_B,d_C, leaving a subarrangement and its full singular setZ. AlwaysZ⊂Z₀, so deleting point conditions gives

    epsilon(Z)≥epsilon(Z₀)=1/(n+1),                     (2)

providedZ is nonempty. No claim that line deletion necessarily changes every original singular point is made.

## 2. Exact lost-point convolutions

For a retained A_a define

    L_A(a)=#{b∈D_B : −a−b∈D_C}.                         (3)

Among its n original grid points, exactly those counted byL_A(a) cease to be singular in the subarrangement: A_a remains, so singularity fails precisely when both other incident lines were deleted. If the A pencil retains at leasttwo lines, its coordinate vertex also remains singular. Thus its exact singular-point count is

    n+1−L_A(a).                                         (4)

The analogous formulas hold cyclically. They involve finite cyclic convolution, not a generic-position model.

If the A pencil retains at leasttwo lines and there existsa∉D_A withL_A(a)=0, that component still containsn+1 points. Equations(1)–(2) then prove

    mpl(Z)=n+1,       epsilon(Z)=1/(n+1).                (5)

The lower bound on all other lines comes fromZ⊂Z₀; no unexamined auxiliary line is excluded by assumption.

A size-only sufficient condition is

    n−d_A≥2 and n−d_A>d_B d_C                           (6)

for at least one cyclic choice ofA. Indeed at mostd_Bd_C indices can lie in the set−D_B−D_C. A retained index outside that set has zero loss. The exact convolution test(3) may succeed even when(6) fails.

## 3. A uniform deletion budget

WriteD=d_A+d_B+d_C. If

    D≤n−2,            D²+3D<9n,                         (7)

then **every** way of deletingD lines retains the full value(5).

To prove this, D≤n−2 guarantees at leasttwo retained lines in each pencil. If(6) failed for allthree pencils, summing the failures would give

    3n−D≤d_Ad_B+d_Bd_C+d_Cd_A≤D²/3,

contradicting(7). The last inequality is equivalent to the sum of the squared pairwise differences of thed_i being nonnegative.

This allows an order-sqrt(n) number of arbitrary deletions, with leading sufficient budget3sqrt(n), rather than only deletion of a fixed number of lines. It is a sufficient guarantee, not a sharp threshold. For example the largestD certified by(7) is8 atn=10,28 atn=100, and298 atn=10000. The checker verifies these integer claims exactly.

A second immediate class is any subarrangement retaining one whole pencil and at leasttwo lines in another pencil. A retained line in that second pencil cannot lose a grid point, because one of its other incident families is whole. It has n+1 singular points, so(5) applies. This includes arbitrary choices in the third pencil. The degenerate case with at mostone line in each of the two other pencils is deliberately not swept into this statement.

## 4. Exact total point count when every pencil retains at leasttwo lines

LetT be the number of triples(a,b,c)∈D_A×D_B×D_C witha+b+c=0. A grid point is lost exactly when at leasttwo of its three incident lines are deleted. The sum

    P=d_Ad_B+d_Bd_C+d_Cd_A

counts a point with exactlytwo deleted lines once and a point with allthree deleted lines three times. Therefore the number lost isP−2T, and

    |Z|=n²−P+2T+3.                                      (8)

The final3 counts the retained pencil centers. This can feed the explicit degree bound of turn1; if a pencil retains fewer than two, the appropriate center is instead omitted.

## 5. Scope of the progress

The deletion criteria give genuine arrangements of arbitrarily large size, with the full inherited Seshadri value proved for all curves. They neither assert the general conjecture nor say that every Fermat subarrangement satisfies(5). Larger deletions can change the value; absence of a zero-loss line only means this particular inheritance argument no longer pins it down.

The next and final turn will test that boundary with an exact finite example and retain any remaining gap rather than perform a sixth author search. Original status unresolved4/5.
