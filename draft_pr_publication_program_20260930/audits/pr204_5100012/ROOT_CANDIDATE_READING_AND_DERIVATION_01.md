# Root candidate reading and independent calculations

UTC checkpoint: 2026-10-16 09:56. Estimated case completion: 25%; mathematical gate remains pending the four fresh families and Root artifact acceptance. Priority, manuscript, whole-package reviews and all publication/integration gates remain undone.

## Reading and provenance

Root froze ROOT_SOURCE_FIRST_CONTRACT_01.md and ROOT_PRE_CANDIDATE_FLAG_ROUTE_01.md before reading the original candidate or favorable review. After that freeze Root read the complete original PROOF.md, SOURCES.md, TURN_1_CHECKPOINT.md, PUBLICATION_STATUS.md, both manifests, complete prior_imported_report.json, the original independent FINAL_REVIEW.md and both verifier programs. Original bytes remain unchanged. The shared two-pole checkpoint is substantive author collaboration with PR203, not an independent review or separate discovery. The old favorable review and reported counts are historical claims to recheck, not current acceptance.

The source table specifies k203,b, signed orbit area times origin-pedal signed area, with N not 2 modulo 4, in a proper confocal ellipse pair. It does not literally print a least-period convention. The physical least-period interpretation is necessary: repeating a primitive-six list twice yields a listed length twelve but does not make its nonconstant area product constant. Every current theorem statement must disclose this qualification. Absolute values of the signed shoelace areas also give constant product as a corollary; that observation does not identify shoelace area with an unweighted filled-in region of a star polygon. Projection is onto full sidelines.

## Direct checks of the canonical geometric input

For outer semiaxes a>b>0 and 0<lambda<b^2 set alpha^2=a^2-lambda and beta^2=b^2-lambda, k^2=(alpha^2-beta^2)/alpha^2 and k'=beta/alpha. Since cn decreases from 1 to 0 on (0,K), cn(v)=beta/b determines a unique v in (0,K). It gives sn(v)^2=lambda/b^2 and alpha^2 dn(v)^2/cn(v)^2=a^2. Thus the displayed outer ellipse is exactly the prescribed pair, with no generic-parameter omission. The addition identities put P(u-v), P(u+v) on the tangent with normal (-sn(u)/alpha,cn(u)/beta). Stachel Theorem4.3/equation4.9 supplies the physical billiard correspondence and coprime winding classification; the other family is also checking that correspondence directly. Primitive stars are retained.

Root freshly read Stachel printed1613-1616. The printed1613 dn sign under 2kK is erroneous for odd k; the proof's correct period2K is verified directly from NIST DLMF22.4, Table22.4.3, accessed2026-10-16. Its 2iK' shift is minus dn. Tables22.4.1-2 give the pole/zero sets and simple orders; DLMF22.8 gives the addition identities. This sign typo is not used as a premise.

## Pole argument checked

For delta=4K tau/N with gcd(N,tau)=1 and 0<tau<N/2, the residues j delta modulo2K have m=N elements for odd N and m=N/2 for even N. Every distinct class has multiplicity N/m. Consequently the cyclic dn sum has two noncancelling simple poles on the compact torus with real period ell=2K/m and imaginary period4iK'. Evenness and the imaginary antiperiod force exactly its two simple zeros, shifted by ell/2. The half-period product is constant by its zero divisor and compactness. This uses exact arithmetic of the physical step, not a numerical closure check.

The origin foot Q=(-alpha k'^2 sn/dn^2,beta cn/dn^2) is holomorphic at common sn/cn/dn poles. At r=K+iK', the shift formulas give Q(r+x)=(alpha/k)cn(x)/sn(x)^2*(dn(x),i), an even Laurent series with leading U/x^2, U=(alpha/k)(1,i). Neighboring pole indices cannot be adjacent because 0<delta<2K. Pairing the two incident determinants makes their neighbor difference odd and O(x), so the area sum has at most simple poles. N=4 has m=2; repeated pole indices share holomorphic neighbors and each term has at most one singular endpoint, so incident grouping does not double-count any singular term. The same argument works for odd N including3. The foot area sum has the dn sum's real period and imaginary antiperiod. One residue match therefore proves T(u)=C_T S(u+K), without a hidden additive constant.

## Explicit nonzero residue coefficient

Two fresh agents independently obtained a positive coefficient before Root's response. Root then independently checked the derivative algebra below. Put s=sn(delta), c=cn(delta), d=dn(delta), h=c/s^2. With residue dn(iK'+x)=-i, the N/m multiplicities cancel in the ratio of residues. The paired incident terms have residue det(U,Q'(r+delta)), with no extra factor2: the incident 1/2 cancels the derivative difference2. Hence

    C_T=alpha^2/k^2 * [h'(d-1)+h d']
       =alpha^2/s * (d-c^2)/(1+d)
       =alpha^2 s (d+k'^2)/(1+d)^2 > 0.

Here h'=-d(1+c^2)/s^3, d'=-k^2 s c, 1-d=k^2 s^2/(1+d), c^2=1-s^2. Since delta is strictly between0 and2K, s>0 and d>0. Thus the original allowance of a vanishing coefficient is harmless but unnecessarily weak. This explicit formula also shows excluded primitive N=2 modulo4 has genuinely nonconstant product, since its product is a positive constant times the square of a meromorphic function with poles. This is an exact obstruction, not merely the displayed finite samples.

## Route status and required repairs

The pre-candidate alternative flag route is still a proposed complementary pole/zero mechanism; this note does not promote its omitted incidence-curve chart and support-disjointness details to a second universal proof. The complete candidate Jacobi proof is the argument actually being audited. The independent Euclidean family has separately derived full low-period cases and states its general scalar cancellation gap explicitly.

Both original scripts use removable Python assert for correctness checks. Their unchanged ordinary output may reproduce exactly while optimized execution loses enforcement. Historical originals must remain intact, and any current executable verification kit must use explicit exceptions and genuine false-identity controls in ordinary and optimized modes, with exact code/output bindings. The fresh physical reproduction family owns unchanged runs and actual mutations; the source family has complementary small function controls. Counts are finite checks, numerical values are non-interval diagnostics, and neither is the universal proof.

No original PR/QUEUE/native content was changed by this checkpoint; no publication or priority conclusion is made here.
