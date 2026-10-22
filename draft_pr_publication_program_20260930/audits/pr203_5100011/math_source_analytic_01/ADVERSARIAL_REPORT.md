# PR203 independent source and analytic audit

Original HEAD: 8edca9d773c085adb4ed0611357a7a2957e3395d. Problem5100011/k203,a. This addresses mathematical validity and primary-source dependence only. Historical priority, novelty, publication readiness and any other PR are outside this audit.

## Finding

**The explicit primitive-period theorem in original PROOF.md survives this independent audit.** No mathematical dependency gap or missing star/sign case was found. An independent analytic proof was reconstructed before candidate intake. The candidate's shared-author pole mechanism has now been independently proved rather than accepted on attribution. The needed confocal specialization of the published even-area identity is also proved independently below.

**The source needs an explicit interpretation.** Both actual RGK tables print N congruent0mod4, all M, with signed areas; neither literally prints "least period." The candidate expressly requires least period. A displayed-list-length interpretation is false: repeating a primitive6 family twice gives12 entries but a nonconstant product. This is not a candidate counterexample. It proves why the primitive clause must remain visible.

## Independence and custody

Plan frozen2026-10-16T07:31:45.469794+00:00, before source PDF reading and original proof intake. Independent proof saved before candidate read; checkpoint2026-10-16T07:36:16.389492+00:00. Subsequently all283 original PROOF.md lines and all80 SOURCES.md lines were read. No favorable old report/verdict or sibling checkpoint was read. Custody metadata was read after derivation/intake; proof and sources hashes match the original custody receipt.

Workflow exception: initial authoring omitted workdir and created the two new plan/log files in inherited Math cwd. They were moved intact into this audit folder immediately upon noticing; no pre-existing file was overwritten. The log records this. All subsequent authored files are here. No Git/index/ref/branch/PR/UI/publication/tracker mutation, outside-person communication, installation/copying of packages, source-package modification or other-PR review occurred. Two ephemeral table PNGs were inspected and deleted. ENOSPC delayed final text writes; no successful broad suite was repeated.

## Primary-source findings

- RGK arXiv2004.12497v11 actual PDF: signed equation(1) printedp3; §3.3 p4; Table3 p6. Row k203,a is A Am, N congruent0mod4, M all, value?, proven?. Table visually inspected. Feet are to N-periodic sides. Full side-line projection is the pedal convention necessary for arbitrary exterior M.
- Distinct RGK journal actual PDF, DOI10.1007/s40598-021-00174-y: signed equation(1) p343, §3.3 p344, Table3 p346. Independently rendered/inspected; agrees on target. It is bibliographically distinct from expanded arXivv11.
- Stachel actual journal PDF, DOI10.1007/s40879-021-00524-2, Theorem4.3/(4.9), pp1614-1615: canonical parametrization, coprime turning number, caustic modulus and axes relations exactly match the needed input. Printedp1613 dn(u+2jK)=(-1)^j dn(u) is a typo: correct real period2K. Candidate SOURCES25-26 explicitly discloses and avoids it. Software parameter is m=k².
- Chavez-Caliz actual journal PDF, DOI10.1007/s40598-020-00154-8: signed area p93, transverse-intersection/general-position definition p94, Theorems3(p93)/6(proofp104). The theorem concerns original area times area of the polygon made by OUTER boundary tangents; it is not a pedal theorem. Candidate supplies the needed fixed linear polarity transfer.
- NIST DLMF22.4 and22.8 opened independently for period/divisor/addition checks: https://dlmf.nist.gov/22.4 and https://dlmf.nist.gov/22.8 . Needed formulas were also derived from the Jacobi ODE in INDEPENDENT_DERIVATION.md, not inferred from numerics.

## Independent dependency closure

INDEPENDENT_DERIVATION.md proves the exact frozen hypothesis directly. Set alpha²=a²-lambda,beta²=b²-lambda,k=sqrt(a²-b²)/alpha,k'=beta/alpha,0<lambda<b². Choose h in(0,K) by cn h=beta/b. Then P(u)=(-a sn u,b cn u), delta=2h=4K tau/N. Addition formulas prove that the actual chord with midpoint argument v has line n(v).X=1, n=(-sn v/alpha,cn v/beta). Its exact foot is M+(1-n.M)n/(n.n), with n.n=dn²v/beta²>0 for real v.

The confocal reflection law can be proved without assuming Stachel's theorem. For a unit chord direction e and its perpendicular e_perp, caustic tangency gives (e_perp.P)²=alpha² e_perp,x²+beta² e_perp,y². Using P on the outer ellipse yields
lambda=a²e_y²+b²e_x²-(-e_y x+e_x y)²
      =a²b²(x e_x/a²+y e_y/b²)².
The two tangent directions thus have equal outer-normal velocity magnitude and opposite inward/outward signs, proving specular reflection.

The radial identity is B_M=B_0+|M|² C, where
C=(1/4)sum det(n_i,n_next)(n_i.n_next)/[(n_i.n_i)(n_next.n_next)].
For N=4n,tau odd,T=4K/N, the cyclic traces have periods T,4iK'. On that compact torus A has at most simple poles at iK',3iK' and zeros at T/2+iK',T/2+3iK'. B_0,C have at most simple poles at the latter points and zeros at the former. Their apparent double poles cancel because the singular vertex is even about a dn zero and multiplies an O(epsilon) difference of regular neighbors. Products A B_0,A C are holomorphic and constant. No division by A or B_M is used.

A separate derivation verifies the published identity actually needed in candidate §7. For arbitrary U,V:
area[(-U sn(u+j delta),V cn(u+j delta))]
=UV sn h cn h/dn h * S(u), S(u)=sum_j dn(u+j delta).
The edge determinant is2UV sn h cn h dn(x)/(1-k²sn²x sn²h); the addition identity dn(x-h)+dn(x+h)=2dn(x)dn h/(1-k²sn²x sn²h) gives the formula by summation. Hence A(P)=c1 S(u), A(P'')=c2 S(u+h). S has exactly two simple poles iK',3iK' (residue-2i at the former), and S(2iK'-u)=-S(u) forces zeros at T/2+iK',T/2+3iK'. Since h=tau T/2 is an odd half-period, S(u)S(u+h) has no poles and is constant. This proves the needed confocal even-area identity independently of accepting Chavez's theorem. Polarity then gives the outer-area version. No proof of Chavez's unnecessary more general nonconfocal theorem is claimed.

Divisor exhaustion can also be checked algebraically: c0²+s²=1,d²+k²s²=1 completes to a smooth intersection of two quadrics in P3 for0<k<1. Its only four points at infinity are [1:±i:±ik:0], giving exactly four common simple poles on the common4K by4iK' torus. Setting d=0 gives four simple zeros because d'=-k²s c0≠0 there. The ODE/shift formulas locate exactly the pole/zero grids used above. No additional hidden pole class or generic-parameter assumption remains.

## Full original PROOF.md audit

Ranges cover every substantive line; intervening blanks have no claim. "Verified" uses definitions, actual primary text or the independent derivation.

|Lines|Audit|
|---|---|
|1-3|Target title correct; author-turn/review status historical, not evidence.|
|5-15|Exact assumptions, signed areas and actual side-line pedal match frozen hypothesis. Least period explicit.|
|17-23|Parameter dependence harmless; stronger phase-independent pedal/contact proportionality independently verified. Zero/negative coefficient allowed.|
|25-31|Both editions/row locations verified. Primitivity is explicit interpretive narrowing, not source quotation. Exact repeated-list control below establishes necessity. Stars covered; hyperbolic/degenerate cases excluded.|
|33-42|Orthogonal projection q_i+T_i M and opposite-line linear cancellation exact.|
|43-54|Trig identity sign and1/8 shoelace factor correct; anisotropic sum telescopes. Independently rederived with unit normals.|
|56-59|No convexity needed. Radiality gives M/reflection equality for the same polygon; correctly not yet called phase invariance.|
|61-74|Stachel4.3 uses caustic modulus and coprime tau, step2v; axes/chord/contact phase independently reproved. Opposite traversal handled later.|
|75-80|N4n implies tau odd; half/quarter congruences and central symmetry correct.|
|81-99|Universal signed-area formula, midpoint determinant, dn identity and contact phase S(w+v) all correct; checked analytically and at65 digits.|
|101-102|Scalar and real S positive; signed formula valid for stars.|
|104-122|Normalized tangent, bilinear norm, foot and cyclic area correct; required pedal is T_M(w+v). Bilinear transpose correctly avoids conjugation.|
|124-128|Only possible foot poles at dn zeros, order<=2. Common Jacobi poles removable. Inventory complete.|
|130-140|Quarter-shift formulas, parity signs and arbitrary-M evenness correct; no complex square-root branch used.|
|142-154|Two incident edges combine with correct sign. Singular factor even order<=2; neighbor difference odd O(epsilon), so resulting pole<=1.|
|156-160|Nonadjacent simultaneous singularities grouped without double counting. Adjacent poles would require delta multiple2K. N4 covered.|
|162-174|Real/imaginary foot symmetries correct. Real radial lemma extends meromorphically, giving2K period and2iK' anti-period.|
|176-184|Bezout yields h=4K/N from delta and2K. The local h differs from earlier half-step v but is explicitly redefined. Compact lattice and two pole classes correct.|
|186-191|F=S(u+K) has exactly the same two simple poles, nonzero residue: exactly two dn trace terms contribute at a representative, with equal real-period residue; other terms regular. Imaginary residue has opposite sign.|
|193-202|Cancel first residue; anti-period cancels second. Holomorphic torus difference constant, anti-period forces zero. Includes identically-zero pedal and real coefficient.|
|204-207|K is a cyclic period of S by n delta=K tau, tau odd. Combining exact phases and positive normalization proves(2).|
|209-225|Chavez exact statement checked. Common-point x²=a²alpha²/c²,y²=-b²beta²/c² correct; four finite transverse intersections. Determinant=lambda c²/(a²b²alpha²beta²)>0; no common infinity point. Needed identity independently reproved above.|
|227-240|Outer polarity pole is intersection of consecutive boundary tangents. D_C B_i=D_E R_i and determinant transfer correct with ordered indices. Real antipodal chord cannot support proper centered caustic, so outer vertices finite.|
|242-243|Proved proportionality times proved area product proves target with all signs.|
|245-256|Attributions not evidence. Sibling checkpoint unread; every needed shared mechanism independently proved. Historical reuse/method attribution outside this audit.|
|257-260|Circle excluded. Separate circular extension follows from rigid rotation and radiality, without degenerate complex modulus.|
|261-264|Reversal, cyclic relabeling and admissible repetition scaling correct. Repetition does not change primitive hypothesis.|
|265-270|Diagnostics correctly labeled aids. Literature/review-status assertions not independently validated; no novelty inference.|
|272-283|RGK/Stachel/DLMF/Chavez references match checked inputs. AST is historical-method attribution, not a logical dependency; no AST theorem is needed for verdict.|

## Full original SOURCES.md audit

|Lines|Audit|
|---|---|
|1-15|Target, source row/page/area/pedal conventions checked. Fixed M correct. Primitive/star clauses explicit in candidate, not literal table. Sibling described only for scope and not reviewed.|
|17-32|Exact editions/statements checked independently. Original author's reading/rendering history not independent evidence. dn typo disclosure accurate.|
|34-35|Manifest/copy history metadata only; actual PDFs and candidate files independently hashed here.|
|37-46|Shared-author checkpoint and hash disclosed. Checkpoint untrusted/unread; mathematical mechanism independently reconstructed, so no unsupported gap transferred to it.|
|48-54|Credited Chavez theorem and polarity correct; no private communication mathematically required. Campaign/reviewer history outside proof audit.|
|56-70|Prior-attempt/search/history/no-contact assertions not verified here; none supports mathematical clearance or novelty. Deep priority gate not performed.|
|72-80|Budget/queue/runtime history not mathematical evidence. Substantive description of radial then meromorphic argument accurate; metadata neither checked nor mutated.|

## Exact repeated-list boundary

Let E:x²/4+y²=1 and C:x²/(32/9)+y²/(5/9)=1, alpha=4sqrt2/3,beta=sqrt5/3,lambda4/9. Two phases of its primitive6 family:
P_R=[(2,0),(4/3,beta),(-4/3,beta),(-2,0),(-4/3,-beta),(4/3,-beta)],
P_T=[(0,1),(-alpha,1/3),(-alpha,-1/3),(0,-1),(alpha,-1/3),(alpha,1/3)].
All vertices lie on E; all sides tangent to C exactly by n^T diag(alpha²,beta²)n=1. Six distinct vertices show least period6. Reflection follows from the confocal identity above. At M=O,
A_R=20sqrt5/9,B_R=140sqrt5/81;
A_T=32sqrt2/9,B_T=224sqrt2/81.
Repeat both lists twice:12-entry products56000/729 vs57344/729, difference448/243. Therefore the printed N cannot consistently mean arbitrary displayed length. exact_repeated_lists.py and exact_repeated_results.json preserve the exact independent Sympy1.14 computation.

## Reproduction, boundary cases and final scope

reproduce.py used existing mpmath1.3,65 digits, Python3.14.6 -B:156 phase cases across k=.15,.6,.92,.999; N4/8/12/16/20; every coprime tau in(0,N/2); centered/interior/far M. Max normalized product spread5.071e-64, pedal/contact ratio1.243e-63, line incidence6.766e-64, radial residual6.074e-64. Universal area sum and reversal pass. Complex N4/8/12 checks confirm residue and linear zero behavior. These are high-precision diagnostics, not interval-certified computations.

N8,tau3,k=.6 has zero-pedal radius about3.03423188732: positive centered B, numerical zero there, negative B at twice that radius across phases. The proof handles every sign exactly. All real foot denominators positive for0<k<1. No generic assumptions or unproved continuity from generic data are used. Excluded circle/degenerate endpoints are not silently inserted into the complex proof.

Strongest verified result: original explicit theorem and stronger B_M/contact proportionality hold for every proper nondegenerate confocal elliptical caustic, a>b>0, least N divisible4, all coprime stars/reversals and fixed finite real M, with signed areas on actual side lines. No mathematical gap remains in that scope.

Remaining limitations: least-period interpretation must remain explicit; arbitrary repeated-list-length assertion is false. Historical metadata, priority and novelty remain unassessed. This is source/mathematical clearance only; no publication action or novelty claim.
