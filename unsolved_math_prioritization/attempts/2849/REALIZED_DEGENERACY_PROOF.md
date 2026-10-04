# Attributed first-party proof copy from closed cover algebra family

# A realized target-premise degenerate rational sphere

This is an independently authored reconstruction of a known example, not a novelty claim. It verifies the false-route correction to the closing paragraph of the exact original PR47 `OBSTRUCTION.md`. The primary source is Sivek–Zentner, *A menagerie of SU(2)-cyclic 3-manifolds*, Theorem1.2, presentation(2.1), Proposition6.1 and Remark6.2, [author PDF](https://zentner.app.uni-regensburg.de/menagerie.pdf). That PDF was read temporarily and its SHA256 is `e3595453cbe70e44a6fa0f57137228218910c6c5d0223dfc9add2171e1a92f67` (461253 bytes); no foreign body is retained here.

Take the closed oriented Seifert manifold
\[
Y=S^2((3,1),(3,1),(3,2))
\]
in the source's convention. Its fundamental group has presentation
\[
G=\langle c_1,c_2,c_3,h\mid [h,c_i]=1,
c_1^3h=c_2^3h=c_3^3h^2=1,\ c_1c_2c_3=1\rangle.
\]

**Rational sphere.** The integral abelianization matrix, with columns \(c_1,c_2,c_3,h\), is
\[
M=\begin{pmatrix}3&0&0&1\\0&3&0&1\\0&0&3&2\\1&1&1&0\end{pmatrix}.
\]
Its determinant is \(-36\), and its determinantal divisors are \(1,1,3,36\). Hence
\(H_1(Y;\mathbb Z)\cong\mathbb Z/3\oplus\mathbb Z/12\), of order36. Closed orientability and Poincaré duality then imply \(Y\) is a rational homology3-sphere. The independently authored exact controls check every minor needed for these invariant factors, rather than assuming the answer from a determinant alone.

**Every SU(2) representation is abelian.** Identify SU(2) with unit quaternions. Write each noncentral element as \(\cos\theta+v\sin\theta\), with unit imaginary \(v\) and \(0<\theta<\pi\). For elements with angles \(\theta_1,\theta_2\),
\[
\operatorname{Re}(q_1q_2)=\cos\theta_1\cos\theta_2-
\langle v_1,v_2\rangle\sin\theta_1\sin\theta_2.
\]
Suppose a representation \(\rho:G\to SU(2)\) had nonabelian image. Since \(h\) is central in \(G\), \(\rho(h)\) commutes with every image element. The centralizer of a noncentral SU(2) element is a circle; if \(\rho(h)\) were noncentral, the entire image would lie in that circle. Therefore \(\rho(h)=\pm1\).

If \(\rho(h)=1\), each \(q_i=\rho(c_i)\) satisfies \(q_i^3=1\). Its angle is0 or \(2\pi/3\). If one \(q_i=1\), the product relation says the other two are inverses and they commute. Otherwise all angles are \(2\pi/3\), and \(q_1q_2=q_3^{-1}\) has real part \(-1/2\). Thus
\[
-\tfrac12=\tfrac14-\tfrac34\langle v_1,v_2\rangle,
\]
which forces \(v_1=v_2\). Then \(q_1,q_2\) commute and so does \(q_3=(q_1q_2)^{-1}\).

If \(\rho(h)=-1\), then \(q_1^3=q_2^3=-1\) and \(q_3^3=1\). A central \(q_1\) or \(q_2\) is \(-1\), and a central \(q_3\) is1; any of those cases makes all generators commute using the product relation. Otherwise the first two angles are \(\pi/3\) and the third angle is \(2\pi/3\). The identical real-part equation again forces \(v_1=v_2\). All cases contradict nonabelianity. Thus the target's universal representation premise holds, including its central and endpoint cases. This is a genuine manifold example, unlike the quartic germ.

**Nonzero normal deformation cohomology, directly.** Put \(\omega=e^{2\pi i/3}\), and choose \(\chi(c_1)=\chi(c_2)=\chi(c_3)=\omega\), \(\chi(h)=1\). This satisfies every relator and gives a noncentral abelian SU(2) representation \(\rho_\chi=\operatorname{diag}(\chi,\chi^{-1})\). For either \(a=\omega\) or \(a=\omega^2\), a rank-one cocycle has four values \((u_1,u_2,u_3,u_h)\). The commutator relations imply \((1-a)u_h=0\), so \(u_h=0\). The cube relations contribute no further restrictions because \(1+a+a^2=0\); the product relation is
\[
u_1+a u_2+a^2u_3=0.
\]
Thus the cocycle space has complex dimension2. Coboundaries span the nonzero vector \((a-1,a-1,a-1,0)\), which satisfies the relation. Hence
\[
\dim_\mathbb C H^1(Y;\mathbb C_{\chi^2})=1,
\qquad \dim_\mathbb R H^1(Y;\operatorname{ad}\rho_\chi)=2.
\]
Degree1 group cohomology equals the manifold's local-system cohomology, so no asphericity assumption is needed for this calculation. The two independent cocycle constraints and coboundary ranks are checked exactly in `exact_controls.py`.

**A relevant finite cyclic cover.** The quotient sending every \(c_i\) to1 in \(\mathbb Z/3\) and \(h\) to0 corresponds to the regular torus cover of the base orbifold \(S^2(3,3,3)\). It is exactly the kernel of \(\chi^2\), hence an adjoint-kernel cover permitted by the definition of cyclic finiteness. One construction is \(T^2=\mathbb C/(\mathbb Z+\mathbb Z\omega)\), on which multiplication by \(\omega\) has order3 and three fixed points; its quotient orbifold is \(S^2(3,3,3)\). Pulling back the Seifert fibration yields a regular3-fold manifold cover \(\widetilde Y\to Y\), a circle bundle over \(T^2\). The source's Euler-number convention gives \(e(Y)=-4/3\) and \(e(\widetilde Y)=-4\). The circle-bundle presentation has abelianization \(\mathbb Z^2\oplus\mathbb Z/4\), so \(b_1(\widetilde Y)=2\). This agrees with the two nontrivial rank-one eigensummands of dimension1 and zero invariant eigensummand.

Consequently, the general claim that every target-premise reducible has zero normal cohomology is **false**. The example establishes neither the value of \(I^\#(Y)\) nor a counterexample to KP3.51. It only makes the correct remaining route precise: any general proof must control actual degenerate reducible Floer data, or use other information that bypasses that control; it cannot first prove universal cyclic finiteness.

# Global current source qualifications

This is a SOURCE-only correction proposal for PR47 / 2849 / KP-3.51, original head 487327b2412c436ae69e8c52bf353a9a1fb7594e and base c6975ca76f9f667f1250ba403d0e6da2aafe14d0. The full framed-instanton rank question remains UNSOLVED. Source readiness does not certify ROOT reading, an actual current freeze, a new verdict, acceptance, native reconciliation or publication. All current ROOT approval/runtime/verdict fields remain false or null. NEW whole-current source-first review is PENDING even after a future administrative freeze.

The original §5 alternative of proving universal normal H1 vanishing under the target premises is FALSE. Known Y=S²((3,1),(3,1),(3,2)) has H1=C3⊕C12 (order36), all SU(2) representation images abelian, complex normal H1 dimension1, real adjoint H1 dimension2 and a relevant regular3-cover with b1=2. Credit Sivek–Zentner, A menagerie of SU(2)-cyclic 3-manifolds, Proposition6.1. A general solution must control actual degenerate reducible Floer contributions and differentials, or supply a mechanism bypassing that difficulty. The I# rank of this example is not computed in this packet and it is not a counterexample to KP-3.51. The universal-vanishing route stays blocked unless materially new premises change the claim.

The elementary finite-character orbit count, adjoint square weight and quartic lower-link proof remain valid. The quartic has local critical rank3 and Euler1 but has no asserted three-manifold/Chern–Simons realization or equivariant instanton interpretation. Trefoil6-surgery has C2*C3 and all abelian SU(2) images; the correct squared-root test succeeds and its known instanton rank is6. The trefoil calculation diagnoses only Definition5.3 / Corollary5.4's torus-knot clause in arXiv:2608.20551v1. It supplies no broader claim about that paper, its authors, other versions or the full target. No novelty, exhaustive literature absence, priority or full-solution claim is made.

The raw plain source_record.json is preserved byte-exactly, both operatively and in original_archive. Its historical AIM kirbylistrep.pdf attribution points to a workshop summary, not numbered K3 Problem3.51. SOURCE_PROVENANCE_CORRECTION.md explicitly identifies the Berkeley author K3 PDF at printed167–168. Neither the record nor the frozen old review is silently rewritten. Historical PDF hashes/access/render/model/reasoning/deadline/publication-state and old PASS assertions are dated attributions unless separately authenticated by genuine ROOT evidence. The older review is not the current verdict; both new independent families require the route and provenance repairs. No fresh foreign PDF/text/OCR/pixels/cache/SQLite bodies, HTTP headers or cookies are retained here.

Original turns.json is one JSON OBJECT, count1 / five allowed; no new substantive attempt or audit turn is charged. Original prior_report.json is literal null\n. The upstream KP-3.51 key was separately observed ABSENT, with saved SQLite/import fallback {}; null, absence and {} are distinct. These dated facts never turn the saved null into an actual report. Native selected state/history were ABSENT and queue/catalog remained queued0/5; mirror reconciliation is PENDING. Current proposed bookkeeping preserves state/history/inventory and changes only the selected queue's named Status, Turns and Findings; Chat, DOI, every other cell and every other row remain byte-exact.

Original preparation ownership is scoped301+self with55 relative directories and a separate5-member closure, totaling307 first-party files; it does not own this whole audit root. Cover family is143+self /23 relative directories; gauge is71+self /15 relative directories (16 including root). ROOT's actual closed-cover readback child12271 follows original closure child10880. No disk prelaunch/split-stream capture is invented for the original agent closure. Duplicate ROOT closer10982 failed permission on already closed family bytes and is preserved as a failure. Gauge ROOT read-only verification child10989 passed. The three A45 records have4 actual members and currently dated0644, while original separate closure has5/full0444. They are read-only dependencies outside this family's ownership.

Production builder/operator are TEXT ONLY at this stage. Actual own captures cover source inspection/authoring and private predicates only, retaining failures, prelaunch sources, real PID/times and complete streams. Private predicates do not validate a production run. Every eventual staged file and self-only manifest must have full S_IMODE0444; low nine bits are insufficient. Exact bytes plus recursive scalar-type-sensitive JSON equality, canonical safe paths, no duplicate/extra/special/symlink or empty directories, immutable dependencies, no optimized guards, main/fresh13 authority and macOS absent-only exclusive publication are required.

Execution chronology: original inner GIT_COMMANDS is written incrementally by the builder while alive; the frozen copy is an honestly labeled prepublication prefix. Only the actual outer CAPTURE is completed after child exit. The outer operator never writes inner commands. ROOT must personally read the ORIGINAL final inner full command records and full streams AFTER child exit, plus the completed outer capture at its original path, before promotion. Dated native4/currentHEAD evidence approves no future changed main. After the new whole-current adversary, ROOT must reconcile its complete closed report, final capture/inner evidence and newly fresh13/currentHEAD before acceptance.

No native/canonical/index/branch/Git/remote/outreach/paper/DOI/tracker/release write is authorized by this preparation. Source closure is self-only; its genuine outer capture is written separately by ROOT after that child exits.


## Distinct SOURCE V2 administrative repair

The operative preparation is current_preparation_family_v2. Closed SOURCE V1 manifest cc29dc830448d8ddf232f3fc080e457c6a8a015428104bba2d4fc15f62f56631 remains unchanged and unpromoted. The complete closed [ADVERSE SOURCE report](../../current_source_adversary_family/REPORT.md), manifest ed0aba6a7a42e752012399daed24d460e25108afd7b66c89ee1907473eb76a85, identifies one mandatory administrative defect at V1 builder line150. That source rejected all33 genuine read-only Git receipts because their source and source_unchanged fields are null. No old PASS is transferred.

V2 separates the three typed-source unchanged mathematical-helper receipts from the exact33 read-only Git receipts. Both classes retain the genuine pr47-root-literal-operation-capture/v1 schema, complete actual child records and full streams. Helper argv/source identities are exact; Git argv is the exact original16 show/16 ls-tree/one full-diff sequence with explicit null source fields. Invalid substitutions, malformed types, missing fields and changed argv must be rejected. Original16 archives, immutable operative helper/results/plain source/object ledger/literal null and every historical capture remain byte-exact. The closed V1 and ADVERSE bodies and separate actual ROOT closing/readback captures are fixed read-only dependencies.

This repairs an administrative evidence contract only. KP3.51 remains UNSOLVED at original1/5,new0,audit0. The known realized normal degeneracy still has no instanton rank computation here. Production builder/operator are text only, never imported, compiled or executed during preparation. All five ROOT prerequisite drafts remain false/null. A new different clean SOURCE audit, genuine ROOT prerequisites, actual current freeze, another whole-current audit, fresh13/currentHEAD reconciliation and native acceptance remain PENDING. No paper, DOI, tracker row, outside communication or Git/native/canonical mutation is supplied by SOURCE V2.
