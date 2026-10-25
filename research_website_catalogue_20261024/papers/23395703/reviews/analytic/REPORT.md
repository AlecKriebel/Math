# Independent analytic review — Zenodo23395703

**Complete: the full stated seven-hyperplane counterexample is supported. No substantive mathematical defect or central proof-dependency/applicability gap was identified.** The conclusion holds over every characteristic-zero field with the specified degree-reverse-lexicographic convention. Historical priority, independent discovery and smallest hyperplane count remain unestablished. This is an independent mathematical assessment, not conventional peer review or formal proof certification.

The actual six-page manuscript is *A seven-hyperplane counterexample to a generic-initial degree bound*,dated15October2026. The authenticated PDF is82,753bytes,SHA256 `4cdc4d5810d0ffe09c23242aeea9560bd9dffcdacdc9c09f9b2133562d3d5180`. The separate controlling TeX is18,436bytes,396lines,SHA256 `c824a6b0327044714027f80d5067488a1f5875a2007f1555b2c038d595a2e43d`, identical to its embedded copy. I read every actual PDF page's text, every TeX line and all six actual rendered pages. The API has no version field; the package README's internal version language is not an official record version assertion. All88frozen source bindings were checked unchanged at completion.

## Independence and literal claim

The full manuscript was read and a substantial ten-family analytic ledger sealed at2026-10-25T07:28:12.462321Z before primary bodies, certificates, source historical assessments or current sibling/root derivations. Ledger SHA256 `4a1f9df01af26982525ef4dbdb83d7d2177df9d5c97873b8cedc49804dc7727e`; INITIAL_SEAL SHA256 `face785ba6840becbf77d939872c579ce6ea97cde15fe3cb4e5d1e8ef7d8cf9a`. Only then were raw primary paths requested. No sibling/root mathematical derivation or historical report body was read. The source README's authored status/credit/reproduction descriptions were read afterward and are not adopted as proof or priority evidence.

Let S=K[x,y,z,w],charK=0,

    Q=xy(x−y)(x−2y)zw(x+z+w), J=(Q_x,Q_y,Q_z,Q_w),
    B=gin_DegRevLex(J), x1>x2>x3>x4.

The theorem asserts that the least p withx2^p∈B is8 and that B has a degree7minimal generator supported in the first three variables and divisible byx3. Its largest variable is consequentlyx3 and its degree is belowp. No full gin, particular exponent vector, positive-characteristic extension, smallest example or first-discovery claim is needed or made.

## Universal proof reconstruction

DERIVATIONS.md gives the detailed checkable reconstruction. The central algebra survives the following checks.

On a binary or ternary linear section keep **all four ambient polars**, differentiating before restricting. Pairwise nonproportional nonzero restricted factors make the quotient modulo each factor a domain with all other factor images nonzero. Reducing a linear syzygy forces each ambient scalar contraction to be a constant multiple of that factor. The converse is exact when the seven constants sum to zero. Constant syzygies vanish because the coordinate-factor rows span the ambient dual space. Thus there are four minimal degree6generators.

The four-factor pencil forces one common scalar a. With the other three scalars b,c,d, the full system is

    u=(aX,aY,bZ,cW),
    (a−d)X+(b−d)Z+(c−d)W=0, 4a+b+c+d=0.

Ternary independence ofX,Z,W forcesa=b=c=d, then7a=0. Thus there are no linear ternary syzygies and H3(5,6,7)=(21,24,24). Binary rank2 gives a one-dimensional relation amongX,Z,W; the trace cuts its two parameters by a rank-one equation. The parameter-to-syzygy map is injective because all coordinate restrictions andX+Z+W are nonzero. There is exactly one independent linear binary syzygy.

Restricted Euler and the pairwise distinct binary factors rule out any common projective zero of the four binary polars, even after algebraic closure. The binary quotient is Artinian. Hilbert–Burch gives three minimal syzygy shifts6+e_i; finite colength impliesΣe_i=6. Exactly onee_i=1 and the others≥2 force(1,2,3), yielding H2(6,7,8)=(3,1,0).

The explicit compatible flag has determinant1, all21binary pair determinants nonzero and the required ternary rank. These conditions are polynomial nonvanishings. The entire scalar/Hilbert argument holds on that nonempty open set of flags. Intersecting its lift toGL4 with the generic-initial open set is legitimate; the finite intersection of K-defined opens has K-rational points over the infinite characteristic-zero field. No assertion that the one displayed coordinate system itself gives the gin is used.

Conca's revlex section identity then identifies these dimensions with the first-variable truncations ofB. Strong stability converts H2(7)=1,H2(8)=0 into p=8. The kernel dimension of multiplication byx3 is H3(k−1)−H3(k)+H2(k): zero at k=6 and one at k=7. SinceB has no elements below degree6, the first kernel excludes degree6generators involvingx3. A killed standard degree6monomial gives a degree7minimal divisor involvingx3. That divisor remains minimal in the fullB because an x4-containing monomial cannot divide a monomial supported in the first three variables. This last argument explicitly avoids extending a third-section statement to arbitrary generators involving later variables.

## Independent exact evidence and a second generic-rank route

The own-folder SymPy program was written and run before reading supplied certificate contents. Its five independently assembled rational multiplication matrices have ranks4,12,4,7,9 at(section variables,total degree)=(3,6),(3,7),(2,6),(2,7),(2,8). It records nonzero minors and their row/column indices and verifies complete left-kernel bases. Independently recovered minimal binary syzygies have coefficient degrees1,2,3; all signed maximal minors of the recovered4×3matrix are exactly70000times the four binary ambient polars. The displayed manuscript syzygy was also independently derived from the relationρ=(1,−11,3).

The binary degree8matrix has a9×9minor equal to40555206945792000000. Its determinant is a polynomial in the flag coordinates and is nonzero at the displayed flag overQ. Thus it is nonzero on a nonempty open set over every characteristic-zeroK, forcing maximal rank9there. Together with the scalar bounds for the other four ranks and intersection with the gin open, this gives an independent proof of exactly the generic dimensions needed for the counterexample. This is an exact nonvanishing/open-set argument; it does not identify a sampled initial ideal with the gin. It provides a second route alongside the paper's valid Hilbert–Burch classification.

Boundary controls confirm why the stated hypotheses matter. RestrictingQ first and then differentiating gives only2binary or3ternary independent degree6polars, rather than4. In characteristic7 the ternary degree7rank drops from12to11, consistently with the Euler relation. In characteristic2 factors merge. The selected flag has determinant bad primes2,3,5,7,11,17; these are flag failures, not a classification of positive-characteristic behavior. The theorem claims no such extension.

The final own run completed in0.691seconds under a25-second watchdog and finally cleaned its process group, including descendants; exit0,empty stderr. A prior successful version with an unused expression was retained in ignored cache and rerun after cleanup; a final35-triple factor-rank census checked the newly inspected prior-family hypothesis. The supplied whole package, its21Buchberger-pair checks,12additional flags, coordinate-specific partial initial ideals and historical example-comparison suites were not freshly executed in this analytic lane. Their core rank/syzygy/Hilbert–Burch existence assertions were independently reproduced. No authored PASS wrapper establishes genericity, full-gin structure or priority here.

## Actual primary interfaces and credit

[BPT, actual arXiv1801.09868v1 body](https://arxiv.org/pdf/1801.09868),Definition3.1/Remark3.2,Theorems4.4/6.2 and Conjecture5.7, matches the ideal, characteristic, order, section and threshold conventions. Its d0 is p−1. Euler's identity permits omittingQ from the generators here. This is the actual arXiv body, not an asserted byte-identical journal copy.

The actual published [OWR2021/5 body](https://ems.press/content/serial-article-files/46883),Conjecture7,p234, independently prints the second-variable exponent bound with unshifted threshold. Both Hokkaido author-manuscript bodies of PT2020/PT2022 also state it as Conjecture7.9. Thus the first-variable transcription mentioned by the note is a genuine source normalization, not the conjecture being refuted or a mathematical contribution.

[Conca, Lemma1.2 and its complete proof](https://arxiv.org/pdf/math/0210064),p2, explicitly identifies generic linear sections with quotienting the revlex gin by the last variables. BPTTheorem4.4 supplies the exact characteristic-zero strongly stable generic-initial statement. Original Galligo1974 was not directly obtained. The original Burch1968 body was also not obtained; the classical Hilbert–Burch interface was checked in Bruns–Vetter's author-hosted *Determinantal Rings*,§16F,p217,including its polynomial-ring/grade2/Cohen–Macaulay application paragraph. The manuscript's Artinian binary ideal satisfies those hypotheses. Its generic conclusion is also independently supported by the exact-minor route above.

The actual published [MPT2026 body](https://ems.press/content/serial-article-files/52275?nt=1),Conjecture4.6/Theorem4.7,p14, proves the bound for arrangements inK3. Its ideal is the Jacobian of that three-variable arrangement. Four restricted ambient polars in the present proof are a different ideal. No contradiction or hidden exception to that valid theorem is being asserted.

Falk–Proudfootv2,§4/Theorem4.1, explicitly constructs parallel connections by identifying common coordinates; the stated U2,4/U3,4arrangement description fits. Tohaneanuv2,§2.1, explicitly credits Orlik–Terao4.29(3) for the classical linear logarithmic mechanism; the current scalar proof is an application, not a new general derivation theorem. Orlik–Terao's original book passage was not directly read.

Migliore–Nagelv1,§8.2,Theorem8.11/Corollary8.12, applies: there is one multiplicity4codimension-two flat, the hypothesis about two such flats in one hyperplane is vacuous, and s=3. Substitution gives precisely S(−7)^3⊕S(−9)→S(−6)^5→J^top. Their§3 distinguishes the two restriction operations. This is substantive prior family information about the five-generated unmixed ideal, rather than the four-generatedJ studied here. The current manuscript gives this credit explicitly; that distinction alone proves no priority claim.

## Verdict and remaining limits

The strongest verified result is the entire original characteristic-zero theorem, with a proof that refutes the actual general-dimensional second-variable conjecture. No mathematical defect, hidden genericity/field restriction, wrong-order interface or unsupported central certificate-to-gin inference was found. Classical imported facts were checked at the precise interfaces; they were not rederived from foundations or proof-assistant formalized.

Historical priority remains unknown. The full Ilardi2018 article was not acquired; publisher/institutional403facts were supplied as acquisition facts only. Its abstract cannot exclude overlap. This review did not reproduce the author's dated36-record/120-query audit,19specific earlier-example exclusions, all parameter families, historical code or first-public-disclosure investigation. Those are explicit limits, not an obstruction to checking that the displayed example is a counterexample. No firstness, independent discovery, continued openness, smallest size, full gin or positive-characteristic result is certified.

All actual read ranges, primary versions, execution limits,88unchanged original bindings and independent artifacts are recorded in READ_LEDGER.json,PRIMARY_LIMITS.md,SOURCE_CUSTODY.json and the immutable manifest/seal. Previous sealed packets,sources,editorial/shared files,site/core,UI,Sheet,Git,deployment and outreach were untouched. Root must read the actual manuscript and full final report before any promotion.
