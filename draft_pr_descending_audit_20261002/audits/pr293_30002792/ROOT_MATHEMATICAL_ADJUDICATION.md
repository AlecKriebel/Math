# PR293: integrated mathematical adjudication

This is a mathematical acceptance of the exact original proof, conditional only on the explicitly cited established algebraic geometry and commutative algebra theorems. It is not a novelty finding, preprint acceptance, formal proof certificate or human peer review. AI tools were used extensively in the proof and these independent reviews.

Original submission: PR293, head `6e717193f93c8a321cce1ce35a00eed1ecfb56e7`, QUEUE status `claimed_solved`, author budget2/5. The operative proof is the preserved `PUBLIC_TURN_2.md`, SHA256 `56d7aee2dbb567f1574952bfe905b5407c0f0b06ec60e4b53b72acda48c245e1`. Earlier author reviews do not establish its validity and were not substituted for the current families.

## Exact target and disposition

Let k be algebraically closed, of arbitrary characteristic. Let L be a nonempty finite reduced union of distinct projective lines in P3, with radical homogeneous ideal I. If alpha(I^(2))=alpha(I)+1, then L is coplanar or consists of all pair-intersection lines of d=alpha(I)+1 distinct planes, no three containing a line. Its homogeneous coordinate ring is Cohen–Macaulay. Hence a non-ACM configuration satisfying this equality does not exist.

This answers precisely Janssen Question3.1, not Question3.2 about arbitrary reduced curves. The original paper explicitly allows arbitrary characteristic. The original Oberwolfach question has the same line scope. Empty unions cannot satisfy the initial-degree premise; nonreduced schemes and nonperfect fields are outside the stated claim. A single line is included. Four or more planes through one point are permitted; three through a line are excluded by the argument, not silently by a stronger general-position convention.

## The central geometric input

On a smooth integral projective surface X, let H be nef with H²=e>=2 and contain an integral Cartier curve C. If pg>0, multiplication by the square of the defining section of C gives a nonzero section of omega_X(2H). If pg=0, duality gives H²(O_X)=0, so the Picard scheme is smooth by the line-bundle lifting obstruction. Therefore q=h¹(O_X)=dim Alb(X) in this branch. No unconditional Picard reducedness is asserted in positive characteristic.

The normalized curve generates Alb(X). Otherwise the quotient Albanese map is constant on C, and the pullback N of an ample bundle on the quotient is nef with N.H=0. Algebraic Hodge index for positive-square H and N²>=0 makes N numerically trivial. A nonconstant projective morphism has a curve with positive pullback degree, including in the inseparable case, a contradiction. The Jacobian of the normalized curve thus surjects onto the Albanese, so q<=g(C_normalized)<=pa(C). This uses dimensions of abelian varieties, not an injection of tangent spaces.

Arithmetic adjunction and Riemann–Roch give K.H=2pa(C)-2-e and

chi(omega_X(2H))=e+2pa(C)-1-q>=e+pa(C)-1>=1.

Duality gives h²(omega_X(2H))=h⁰(-2H)=0 by nef intersection, including exclusion of a nowhere-vanishing section. Hence h⁰>=1. The arithmetic division by2 in RR never divides by2 in k. The lower bound e>=2 is necessary: P2 with H a line fails it.

For an integral degree-e surface S in P3, normalize and projectively resolve in dimension two, preserving the regular locus. H=f*O_S(1) is nef and globally generated with H²=e. A general plane section E is integral, generically in S_reg, and avoids the finitely many images of contracted curves. Its Cartier pullback has no contracted component; generic isomorphism gives exactly one component of multiplicity one. Cartier Cohen–Macaulayness removes embedded structure, so the pullback is integral. Smooth Bertini on the pullback system is neither invoked nor required.

Canonical sections on the resolution inject into the reflexive canonical sheaf of the normalization. Finite Cohen–Macaulay duality gives nu_*omega_Y=Hom_S(nu_*O_Y,omega_S)=c tensor omega_S, where c is the conductor and omega_S=O_S(e-4). The preceding nonzero section injects into c(e-2). At a singular-curve generic point, a normal one-dimensional local domain would be a regular DVR; the actual nonregular local ring is nonnormal, and its conductor is a proper ideal. Thus the section vanishes on every reduced singular curve. The hypersurface sequence and H¹(P3,O(-2))=0 lift it to a nonzero degree-(e-2) polynomial.

Independent surface and characteristic families separately checked this complete chain. They tested nonreduced Picard schemes, purely inseparable conductor maps, nef contracted curves, special nonreduced sections, the e=1 threshold, and canonical inclusion versus equality. No surviving defect was found. The explicit ruled surfaces x^p z-y^p w and the cuspidal cubic cone illustrate the mechanisms; their finite computations are not proofs of the universal input.

## Algebraic reduction and ACM conclusion

For each line prime P, P² is P-primary and I^(2) is the intersection of these actual squares. Choose a nonzero degree-d form F in I^(2). Its radical has degree at least d-1. The only possible repeated factor is therefore F=P²G with P linear, G squarefree and coprime to P. Unless all lines are coplanar, a nonzero partial of G gives a forbidden degree-(d-2) form P DG. In characteristic p, a squarefree nonconstant G has a nonzero partial because vanishing of all partials over perfect k would make G a pth power. No Euler division is used.

A nonlinear irreducible factor Q of degree e>=2 has the degree-(e-2) adjoint polynomial above. Every target line contained solely in Q is in its reduced singular-curve locus, since symbolic order two forces every first partial of Q to vanish along that line. Multiplying the adjoint by F/Q gives a nonzero degree-(d-2) form through all target lines, a contradiction. Thus F is a product of distinct planes.

Every target line is in at least two planes. For each pair, the quotient F/(Pi Pj) has forbidden degree d-2. It establishes simultaneously that their pair line is present and belongs to no third plane. All target lines are these pair lines.

For J=(F/P1,...,F/Pd), reduce a relation sum ai(F/Pi)=0 modulo Pi. The domain S/(Pi) gives Pi|ai; writing ai=Pi bi yields sum bi=0. Thus the full syzygy module is freely generated by Pi ei-Pd ed, giving

0 -> S(-d)^(d-1) -> S(-(d-1))^d -> S -> S/J -> 0.

The support has height two. Auslander–Buchsbaum at associated primes excludes embedded primes. At each pair-line minimal prime every other plane is a unit, so J localizes to that prime and is generically reduced. Unmixedness plus generic reducedness makes J radical; hence J=I(L), and its quotient is Cohen–Macaulay. This direct resolution independently checks the author's Hilbert–Burch argument in every characteristic. Coplanar reduced unions are complete intersections.

## Reproduction and evidence limits

ROOT authenticated all three completed family domains, their source/scope records and complete native streams. ROOT separately reproduced the author's exact3,888-control JSON and the independent algebra family's full60,182-check result: all7,175 unions of up to three F2-rational lines and all15,488 plane multisets of degrees2–5. Both complete enumeration digests match. ROOT also replayed the current geometric example controls with asserts enabled and an exact prelaunch body/PID record. These bounded results supplement, and do not replace, the written proof.

Source reading is precisely scoped. Whole PDF byte custody is not a claim to have semantically read every page. The characteristic-family wrapper lacked contemporaneous child PID/program pins; ROOT does not invent those historical records, and its new replay supplies an independent current binding. The earlier finite program body survives only as an explicitly disclosed reconstruction. Eight surface download failures and two independent Chiarli–Greco access failures remain preserved. No mathematical theorem is inferred from an unavailable article. The surface family supplies precise Kleiman, Liedtke, Milne, Stacks and Kollár dependencies; Kollár is the author, with Dao's appendix.

The additional low-degree singular-line bound and cone route in sectionD were separately checked by the characteristic family: general-plane delta bounds, elementary coefficient dimensions, and curve conductor/RR. They are optional deductions, not gaps transferred into the central proof.

Mathematical review estimate:100% for the stated theorem under established inputs. Priority estimate:0%. Workflow estimate:30%. Exact next gap: extensive primary-source priority audit, including earlier resolutions, characteristic restrictions and classical adjoint-effectivity results. A fresh whole-theorem adversary will also challenge this combined deduction before it is promoted to a preprint. No paper, DOI, tracker row, merge or close is authorized by this mathematical record.
