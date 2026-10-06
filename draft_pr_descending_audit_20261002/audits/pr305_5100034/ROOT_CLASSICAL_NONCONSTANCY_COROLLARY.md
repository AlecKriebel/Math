# Classical implication for focal-ratio nonconstancy

This is an explicit derivation from old primary results, verified during the
PR305 priority audit. It is not a claim that those authors explicitly discussed
the later focal-ratio conjecture. It does not settle historical priority of E/M.

Querret, *Démonstration du théorème de géométrie élémentaire énoncé à la page28
du présent volume*, Annales de Mathématiques pures et appliquées14
(1823–1824),280–285, gives the signed pedal triangle formula in the derivation
on printed pp.282–284. For an oriented nondegenerate triangle of signed area
T, circumcenter O and circumradius R, the pedal area at X is

    p(X) = T (R² − |X−O|²)/(4R²).

ROOT read the complete extracted article and visually checked printed283 and284;
the displayed formulas missing from OCR were checked in the renders. Primary:
[Numdam article](https://www.numdam.org/item/AMPA_1823-1824__14__280_0/).
Fetched PDF441232 bytes, SHA256
`66d10fc03b3559a93241f519beabb353c269d148680a02af585216fc0b798560`.
Querret notes the possibility of either area sign; the formula here uses
consistent side order and signed determinants. A new exact symbolic projection
calculation proves the formula for arbitrary real triangle
(0,0),(r,0),(z,t), r*t nonzero, and arbitrary real X=(x,y). Euclidean motions
put any nondegenerate real triangle in this form. Its equality residual is
identically zero as a rational function, not a finite sample.

Corentin Fierobe, *On the circumcenters of triangular orbits in elliptic
billiard*, [arXiv1807.11903v5](https://arxiv.org/abs/1807.11903v5),
22July2019, Lemma4.1, printed p.9, states that the two real axial triangular
orbits of a noncircular ellipse have distinct circumcenters on the focal axis.
ROOT read the relevant setup, lemma and its complete proof and visually checked
the theorem page. Exact PDF158650 bytes, SHA256
`002006227b9e8d361e5f9a4d7c48148c718e18acce98ce55a2c6e2584617d3f1`.
The direct versioned-URL fetch initially failed with TLS exit35; the subsequent
unversioned PDF fetch succeeded, matches these authenticated bytes, and its
first page identifies v5. Both native retrieval histories remain intact. No
TLS verification was disabled. The2019 preprint date is not the2021 journal
publication date and is not retroactively assigned to uninspected v1 contents.

Put the outer ellipse center at zero and F±=(±c,0), c>0. The axial triangle
T1 is centrally inverted to the second axial triangle T2. Their circumcenters
are O1=(x0,0), O2=(−x0,0), and their circumradii agree. Distinctness in
Lemma4.1 therefore gives x0 nonzero. Define U=R²−c²−|O1|². The shared
nondegenerate confocal ellipse caustic contains both foci strictly; its tangent
triangle contains the caustic. Thus both foci lie strictly inside the triangle
and its circumdisk, so U±2cx0 are positive. Querret's formula gives

    p(F+)/p(F−) = (U+2cx0)/(U−2cx0).

This ratio is positive and unequal to1. Central inversion preserves orientation
and the confocal billiard family, exchanges the focus labels, and replaces the
ratio by its reciprocal. The two values differ. Consequently phase constancy
is false for the triangular billiard family of every noncircular ellipse in
this domain. The accepted E theorem makes the outer focal ratio share this
nonconstancy; that last assertion uses E, not an attribution to Fierobe.

The exact PR305 witness gives an explicit instance:

    O=(1/√21,0), R²=400/21, T=128√21/25,
    U=14, c=√5,
    p(F±)=84(7√21±√5)/625.

The fresh symbolic checker verifies its circumcircle at all three vertices,
the two powers, the classical areas, and independently projected feet. The
ratio minus its reciprocal is exactly7√105/256, which is nonzero. This agrees
with the original mathematical acceptance and explains the counterexample as
a classical implication. It should not be presented as an independently novel
negative theorem or an old explicit focal-ratio claim.

Native corrected execution:2026-10-04T23:54:51.663116–23:54:52.433385Z,
exit0, empty stderr, complete918-byte stdout SHA256
`f89ad4bc4cb890f3644ea25ca5f186a41f81208f59bd2d379d9c7421f39d7157`.
The initial vector-determinant API error is a retained failed harness attempt;
it occurred before any symbolic verdict and is not silently overwritten.

This strengthens the priority qualifications for C. The independent historical
routes remain active and E/M still require final comparison/adjudication.
Checkpoint estimates: mathematics100%; bounded priority45%; workflow35%.
No merge, preprint-ready or publication clearance is implied.
