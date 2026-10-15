# The degeneracy gap in Kirby Problem 3.51

**Outcome: unresolved.** One proof route was examined. The known Morse–Bott argument does not extend merely from the set-theoretic absence of irreducible representations. This note gives an explicit circle-invariant local diagnostic, and checks a recent stronger Alexander-polynomial assertion against trefoil surgery. Neither diagnostic is a counterexample to the original instanton L-space question. The old review is dated history; both current independent original-head audits required this route correction. NEW whole-current review is PENDING; no discovery or priority claim is made.

## 1 Exact target and known theorem

For a closed oriented rational homology 3-sphere $Y$, suppose every homomorphism $\pi_1(Y)\to SU(2)$ has abelian image. The question is whether
\[
\dim_{\mathbb C} I^\#(Y;\mathbb C)=|H_1(Y;\mathbb Z)|.
\]
No irreducibility, surgery presentation, cyclic-homology condition, or nondegeneracy assumption is part of the target. The source is K3 Problem 3.51, printed pages 167–168, proposed and scribed by J. Baldwin; both rendered pages were inspected. [Original source](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf)

Baldwin–Sivek, *Stein fillings and SU(2) representations*, Geometry & Topology 22 (2018), §4.1, Propositions 4.4–4.5 and Theorem 4.6, proves the conclusion under cyclic finiteness. Under the reducible-only hypothesis this is equivalent to the Morse–Bott condition, and to vanishing of $H^1(Y;\operatorname{ad}\rho)$ for every representation. Central representations are automatically nondegenerate. Cyclically finite here refers to the covers determined by $\ker(\operatorname{ad}\rho)$, not an unrestricted claim about all finite covers. The published proof, pages 4350–4357, was read. [Published paper](https://msp.org/gt/2018/22-7/gt-v22-n7-p13-p.pdf)

## 2 What the representation set establishes

Put $A=H_1(Y;\mathbb Z)$, a finite abelian group, and let $\widehat A=\operatorname{Hom}(A,U(1))$. Every representation under consideration can be conjugated to
\[
\rho_\chi(g)=\operatorname{diag}(\chi(g),\chi(g)^{-1}).
\]
Two such representations are conjugate exactly when the characters agree or are inverses. If $\chi^2=1$, the orbit is one point. Otherwise its centralizer is $U(1)$, and its orbit is $SU(2)/U(1)\cong S^2$. There are finitely many orbits. Each is closed, and these are the connected components of the representation set.

Writing $c=|\{\chi:\chi^2=1\}|$, its ordinary homology therefore has total complex dimension
\[
c+2\frac{|A|-c}{2}=|A|.
\]
This is the elementary orbit count in Baldwin–Sivek's proof. It describes the critical set's topology, not the kernel of the Hessian transverse to it.

Indeed, the infinitesimal deformation quotient is $H^1(Y;\operatorname{ad}\rho_\chi)$. The adjoint local system splits as a trivial real line and the realification of the complex rank-one local system $\mathbb C_{\chi^2}$. Consequently
\[
\dim_{\mathbb R}H^1(Y;\operatorname{ad}\rho_\chi)
=2\dim_{\mathbb C}H^1(Y;\mathbb C_{\chi^2}),
\]
since $H^1(Y;\mathbb R)=0$. The square is essential. Absence of a curve of actual nonabelian representations does not, without another theorem, say that all first-order normal solutions vanish: those solutions may be obstructed at higher order.

If every character squares to one, all representations are central and the known theorem applies. More generally, when the displayed cohomology vanishes for all characters, the known Morse–Bott spectral sequence gives the rank upper bound, and the Euler characteristic gives the matching lower bound. These are credited special cases, not a removal of the hypothesis.

## 3 An explicit diagnostic for the proposed extension

Consider the real analytic function on $\mathbb C^2$
\[
f(z_1,z_2)=(|z_1|^2-|z_2|^2)(|z_1|^2-2|z_2|^2).
\]
It is invariant under scalar circle multiplication, including the weight-two action $z\mapsto e^{2i\theta}z$ occurring in a noncentral reducible normal representation.

**Claim.** The origin is its only critical point, the Hessian there is zero, and its local critical groups over $\mathbb C$ have total dimension three despite Euler characteristic one.

**Proof.** Set $x=|z_1|^2$, $y=|z_2|^2$. The two complex-coordinate gradient equations, up to a nonzero common real factor, are
\[
z_1(2x-3y)=0,\qquad z_2(-3x+4y)=0.
\]
If both coordinates are nonzero, the coefficient matrix has determinant $-1$, forcing $x=y=0$, a contradiction. If one is zero, the other equation forces the remaining coordinate to vanish. The Hessian at zero vanishes because $f$ is homogeneous of degree four.

On the unit 3-sphere, $x+y=1$, so the nonpositive lower link is
\[
L=\{f\le0\}\cap S^3
=\{1/2\le |z_1|^2\le2/3\}\cong T^2\times[1/2,2/3].
\]
Both coordinates stay nonzero; their two arguments and the first squared modulus give the indicated product homeomorphism. For a small closed ball $B$, the set $X=\{f\le0\}\cap B$ is a cone on $L$. Hence $X$ is contractible and $X\setminus\{0\}$ deformation retracts onto $L$. The relative homology groups defining the local critical groups satisfy
\[
H_k(X,X\setminus\{0\};\mathbb C)\cong\widetilde H_{k-1}(T^2;\mathbb C).
\]
They are $\mathbb C^2$ in degree 2 and $\mathbb C$ in degree 3, and vanish in other degrees. Their total dimension is three and their Euler characteristic is $2-1=1$. ∎

Thus even analyticity, circle symmetry, an isolated actual critical set, and the expected Euler characteristic do not justify replacing a degenerate local contribution by the homology of one point. This example is **not asserted to be a Chern–Simons local model of a 3-manifold**. Its role is to falsify that abstract inference, not KP-3.51. A proof for the actual gauge-theoretic functional must use additional structure.

## 4 A precise current-source check

Bascapè's *Some knots with no SU(2)-abelian surgeries*, arXiv:2608.20551v1, August 20, 2026, Definition 5.3, page 9, defines SU(2)-clean using every integer surgery coefficient $r$ with SU(2)-abelian filling and **unsquared** $r$-th Alexander roots. There is no exclusion of reducible fillings in that definition. Section 2, page 3, uses the usual meridian–null-longitude slope $r\mu+\lambda$. Corollary 5.4, on the same rendered page 9, says “The following knots are SU(2)-clean” and includes “torus knots $T(p,q)$.” [Versioned preprint](https://arxiv.org/abs/2608.20551v1)

The right-handed trefoil with $r=6$ checks this assertion directly.

**Surgery calculation.** The standard annular van Kampen decomposition of the trefoil exterior gives
\[
\pi_1(E(T_{2,3}))=\langle a,b\mid a^2=b^3\rangle.
\]
The common element $h=a^2=b^3$ is the regular fiber. In the peripheral torus it is $\mu^6\lambda$: a parallel of a $(2,3)$-torus knot in its containing torus has linking number $2\cdot3=6$, while $\lambda$ is the zero-linking longitude. Equivalently one may choose $\mu=a^{-1}b^2$ and $\lambda=h\mu^{-6}$. Filling at slope6 kills $h$, so van Kampen gives
\[
\pi_1(S^3_6(T_{2,3}))
=\langle a,b\mid a^2=b^3=1\rangle=C_2*C_3.
\]
Its abelianization is $C_2\oplus C_3\cong C_6$. The filling is a closed oriented rational homology sphere. This calculation is also explicitly recorded by Sivek–Zentner, *Surgery obstructions and character varieties*, Proposition4.3, page 14: it is $L(2,3)\#L(3,2)$, equivalently $\mathbb{RP}^3\#L(3,2)$. [Primary paper](https://spiral.imperial.ac.uk/server/api/core/bitstreams/31fba2ba-24ed-45cb-9374-dad47877adcc/content)

**Representation calculation.** If $A\in SU(2)$ satisfies $A^2=I$, its eigenvalues are reciprocal unit complex numbers whose squares equal one. Hence $A=I$ or $-I$. Every representation of $C_2*C_3$ therefore sends the first generator to a central matrix; its image is generated by that matrix and the image of the second generator, so it is abelian. This proves the required property for every representation, not just a selected family.

**Alexander calculation.** The usual torus-knot formula gives
\[
\Delta_{T_{2,3}}(t)
=\frac{(t^6-1)(t-1)}{(t^2-1)(t^3-1)}=t^2-t+1=\Phi_6(t).
\]
It vanishes at $e^{\pi i/3}$, which is a sixth root of unity. Thus the trefoil does not satisfy Definition 5.3 as printed. The preprint's own Theorem 3.5 on page 5 includes the slope $2p$ for $T_{p,2}$; the Corollary 5.4 proof on page 9 omits this family when reducing integral slopes to $pq\pm1$. This is a specific inconsistency in that auxiliary claim, not a statement about the paper's other results.

There is no counterexample here to Baldwin–Sivek's test or to KP-3.51. If $\zeta^6=1$, then $\zeta^2$ has order dividing 3, and $\Phi_6(\zeta^2)\ne0$. Equivalently,
\[
\gcd(\Delta(t),t^6-1)=\Phi_6(t),\qquad
\gcd(\Delta(t^2),t^6-1)=1.
\]
The squared test succeeds, so the known cyclic-finiteness theorem says this very filling is an instanton L-space. The example only prevents silently strengthening that test by deleting the square.

## 5 Other current sources and the remaining gap

Li–Ye, arXiv:2511.17877v1, Lemma 7.1 on page 32, treats SU(2)-abelian knot surgeries whose numerator is a prime power or twice a prime power; its proof explicitly uses squared roots. It does not remove the general degeneracy hypothesis for arbitrary rational homology spheres. [Primary preprint](https://arxiv.org/abs/2511.17877v1)

Bascapè, arXiv:2408.16635v2, Theorem 1.5, proves a **Heegaard Floer** L-space conclusion for a specified two-piece graph-manifold family. That cannot be substituted for the instanton statement without an additional theorem. Its introductory attribution of an “if and only if” instanton criterion is not established by the cited Baldwin–Sivek Theorem 4.6, which supplies the sufficient direction. No necessity claim is used here. [Primary preprint](https://arxiv.org/abs/2408.16635v2)

The universal route of proving that every target-premise reducible has vanishing normal deformation cohomology is **false**, not an available unproved lemma. Known SU(2)-abelian rational spheres already realize degenerate reducibles: Sivek–Zentner, *A menagerie of SU(2)-cyclic 3-manifolds*, Proposition6.1, includes Y=S²((3,1),(3,1),(3,2)). It has H1=C3⊕C12 of order36, all SU(2) images abelian, a squared-character complex H1 of dimension1 and real adjoint H1 of dimension2; its relevant regular3-fold adjoint-kernel cover has b1=2. [Primary known-result credit](https://zentner.app.uni-regensburg.de/menagerie.pdf). REALIZED_DEGENERACY_PROOF.md gives a first-party reconstruction and the two independent audits verify it. Its I# rank is not computed here, so it does not refute KP-3.51. A general solution must control actual degenerate Chern–Simons local Floer contributions and differentials, or use another mechanism giving the rank equality. The abstract quartic remains unrealized and supplies no such Floer control. The universal normal-vanishing/cyclic-finiteness route is closed under the original hypotheses.

The exact checks in `verify.py` certify polynomial identities, circle symmetry, elementary lower-link homology arithmetic, and finite-character counts. All 114 assertions pass. They do not compute instanton homology or realize the local model by a manifold. The original target remains unresolved; no full-solution PR should be created from this package.

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
