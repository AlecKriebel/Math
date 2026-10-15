# PR29 original-stage existence-family adversarial audit

**Verdict: PASS for the assigned corner-compatible characteristic existence and continuation mechanism.** No required mathematical correction was found in this family. This verdict does not independently certify the entire instability proof or solve the full source question. The original low-regularity nonlinear stability/instability problem remains unresolved/partial; no L2/H1 departure, global weak-continuation theorem, priority, or new DOI is certified.

Target 30004186 / OWR-17128-002. Original PR head `5ac4a57e08dd72a6f16768f2288b9c0349999431`. Frozen candidate SHA-256 `95458afe7f030f3f0aec3b9d5150857e7dedcb8688e6325c4a0407497feb1b6c`. Original dataset/turn record and review are preserved as historical evidence. No original or canonical file was edited.

## Independence and exact input

The independently derived existence proof was sealed at 2026-10-01T23:31:02Z before reading either old verifier, old review, old receipts, metadata, the original turn ledger, PR diff, or sibling mathematical results. Its immutable early file SHA-256 is `35fdc1acce661c275cfe31a49ebd5dce4e0bcf8b390416dc94763993b0627db0`; see EARLY_SEAL.json and EARLY_INDEPENDENT_RECONSTRUCTION.md. The literal OWR and author-posted 2019/2020 PDFs, together with the current theorem treated as a hypothesis, were the only mathematical inputs before that seal.

After the seal, all 16 original attempt files were read and independently compared, byte for byte, with read-only Git objects at the exact head. Every SHA-256, byte count, and Git blob SHA-1 matches the frozen manifest. The complete 17-path exact diff matches frozen `pr_input/diff.patch` byte for byte, SHA-256 `ac21cf5a637bb83a254d44b53b123c18c301807a3d84c0328e38a6cbbc193f2f`. Every new-file addition reconstructs its entire exact-head blob. The historical ledger is 1 used of 5, one substantive response, original outcome partial. Main was not used as the source candidate. There were no Git mutations or branch changes.

The original provenance's model `gpt-6-astra` and effort `xhigh` are historical metadata attestations, not independently verified service telemetry. The old readiness/source-audit statements about bounded queries are likewise historical attestations. This audit does not reconstruct their actual query telemetry or certify priority. The only new external reads were specified primary/history URLs; no individual was contacted.

## Exact lemma and falsifiable success criterion

The required lemma is local existence and uniqueness for mean-zero initial profiles in

    B={f in C1([0,L]): f(0)=f(L)}, L=2pi,

with a potentially nonzero difference of endpoint derivatives. It must give a common positive initial existence time for the narrow perturbations even though their second derivatives diverge. Reconstruction must give the actual zero-mean periodic primitive, an injective degree-one circle lift, the distributional Eulerian PDE, evolving one-sided slopes, persistence of the sole corner, continuous profiles in a chart moving with that corner, and finite-time continuation conditional only on bounded physical slope. It must also preserve the smoothness of the stated smooth-on-the-cut-interval data.

The audit deliberately sought failures from an unweighted primitive constant, wrong or missing mean subtraction, noninjective lift, forced matching endpoint derivatives, hidden C2 lifetime control, incorrect time continuity, or assuming existence through the desired logarithmic time. These are concrete falsifiers, not hypotheses taken for granted.

## Explicit Banach bounds and uniform local time

B is complete because endpoint equality is a closed linear condition in C1. Write X=id+Y and a=1+Y'. Then integral a=L. The positive-Jacobian subset is open in BxB. Endpoint derivatives are deliberately unrestricted, so X is a piecewise C1 bi-Lipschitz circle homeomorphism rather than a necessarily globally C1 circle diffeomorphism.

Let m=L^(-1) integral Va, K(xi)=integral_0^xi(V-m)a, d=L^(-1) integral Ka and H=K-d. The identity integral a=L gives K(0)=K(L)=0. Hence H belongs to B, H'=(V-m)a, and integral Ha=0. The weighted constant d is essential.

Here are explicit bounded-set Lipschitz estimates supplementing the sealed reconstruction. Use ||f||C1=||f||infinity+||f'||infinity and the maximum product norm. Suppose both input pairs have norms <=R; put S=1+R, B_R0=R(1+S)S, and C_R=2S^2+R(1+S). For a single input, |m|<=RS, ||K'||infinity<=B_R0, ||K||infinity<=LB_R0, and

    ||H||C1 <= [L(1+S)+1] B_R0.

For D=max(||Y1-Y2||C1,||V1-V2||C1), direct product differences give

    |m1-m2| <= (S+R)D,
    ||K1'-K2'||infinity <= C_R D,
    ||K1-K2||infinity <= L C_R D,
    |d1-d2| <= L(S C_R+B_R0)D,
    ||H1-H2||C1 <= [L((1+S)C_R+B_R0)+C_R]D.

Thus F(Y,V)=(V,H) is bounded and Lipschitz on every norm-bounded ball. This reasoning uses only C0 multiplication and integration C0->C1, plus differentiation C1->C0. No Y'' or V'' occurs. The map is polynomial even outside the positive-Jacobian set; positivity is needed only for Eulerian inversion.

If ||V0||C1<=R0 and Y0=0, fix r=1/4 and R=R0+1. Let B_F=max(R,[L(1+S)+1]B_R0) and L_F=max(1,L((1+S)C_R+B_R0)+C_R). The usual integral Picard map on trajectories within radius r of each initial state maps that ball into itself and contracts whenever

    T <= min(r/(2 B_F),1/(2 L_F)),

with a harmless arbitrary positive bound if B_F=0. Every such trajectory has a>=1-r>0. The same constants work for the entire bounded family of initial velocities. This explicitly proves a common positive initial lifespan independent of delta and its large C2 norm. Later continuation constants need only be finite for each fixed delta; no uniform logarithmic-time Ck bound is claimed.

## Mean, inverse map, and weak PDE

The ODE is Y_t=V, V_t=H. Differentiation in the label is valid as a bounded C1->C0 operation. The physical mean M=integral Va obeys

    M'=integral Ha+integral VV'=0,

because the first term is the weighted normalization and the second is [V^2/2]_0^L. Only endpoint values, not endpoint derivatives, are used. Therefore initial mean zero implies m=0 throughout.

On the positive-Jacobian interval, define u(t,X(t,xi))=V(t,xi). Change of variables proves that H is precisely (P u) composed with X: its physical derivative is u and its physical mean is zero. The increasing degree-one lift is globally injective modulo L, with a Lipschitz inverse on each compact time interval. Away from q(t)=X(t,0), u_x=(V'/a) composed with X^(-1) and u_t=H-u u_x.

The weak equation can be checked without assigning a derivative at the corner. For a smooth periodic spacetime test psi, differentiate I(t)=integral Va psi(t,X). The result is

    I'=integral Ha psi+integral Va psi_t
       +integral V^2 a psi_x+integral VV' psi.

Integrating the last term by parts in xi gives -1/2 integral V^2 a psi_x. Its boundary term vanishes because V has equal endpoint values and psi is periodic. Changing variables yields the weak conservative equation u_t+(u^2/2)_x=P u. Continuity of u and u^2/2 prevents a delta contribution at the moving corner. Thus the Eulerian equation holds distributionally everywhere, including the seam.

## Endpoint slopes, corner persistence, topology and regularity

For w=V'/a, the exact derivative equations are a_t=V'=wa and w_t=V-w^2. At the endpoints the forcing V is the same, so J=w_- -w_+ satisfies

    J'=-(w_-+w_+)J,
    J(t)=J(0) exp(-integral_0^t(w_-+w_+)).

The data have J(0)=2kappa+delta!=0. The sole corner persists at finite existing times; its trajectory is q'=V(0)=u(t,q), with no frozen crest speed. Interior C1 regularity excludes additional corners. The physical slope essential supremum equals max_[0,L]|w|, since one-sided endpoint values are limits from intervals of positive measure, not isolated point values. The slope norm is therefore continuous in time.

To describe continuity in the actual class, set A_t=X(t,.)-q(t), mapping [0,L] increasingly onto itself. If a>=alpha>0, its inverse is continuous in the C1 norm: the inverse values change by at most alpha^(-1)||A_t-A_s||infinity, and inverse derivatives follow from 1/(a composed with A_t^(-1)), using uniform continuity on the compact interval. Composition gives U(t,z)=V(t,A_t^(-1)(z)) continuous in C1([0,L]); combined with the Banach ODE it also supplies continuous data dependence in that chart.

This does not assert false strong continuity of translation in periodic W1,infinity. Indeed, for 0<x<theta, phi'(x)-phi'(x-theta+L)=-2kappa+theta/3, whose magnitude tends to 2kappa as theta decreases to zero. The aligned chart is the correct topology for these corner trajectories. Translation covariance is exact: adding a constant to X leaves a,H unchanged. An increasing endpoint-preserving relabeling r gives X_new=X composed with r and V_new=V composed with r; change of variables proves m,d unchanged and K_new=K composed with r, H_new=H composed with r. The vector field is natural under these choices.

The specified cutoffs make the initial data smooth on the closed cut interval for each fixed delta. In Bk={Ck functions with matching endpoint values}, the same vector field is locally Lipschitz with no derivative loss. Differentiating V_t'=Va gives, at derivative order n>=2,

    (D^n X)_t=D^n V,
    (D^n V)_t=V D^n X+terms with lower derivatives.

The highest pair is linear with bounded coefficients on a bounded-C1 interval. Induction and Gronwall bound every finite Ck norm, although bounds may depend on that datum's large initial derivatives. Uniqueness of the C1 system and Ck continuation therefore preserve smoothness before C1 breakdown. The instability proof only needs the C1 class and endpoint slopes.

## Noncircular finite-time continuation

Suppose the existing solution satisfies ||u_x||infinity<=M on [0,T), with T finite. Then a_t=wa and a(0)=1 imply exp(-MT)<=a<=exp(MT). The periodic primitive kernel k(x)=1/2-x/L has L1 norm L/4=pi/2, so

    ||V(t)||infinity <= ||V0||infinity exp(pi t/2).

Moreover ||V'||infinity<=M exp(MT), ||Y'||infinity<=exp(MT)+1, and ||Y||infinity<=integral_0^T||V||infinity. Thus both Banach coordinates are uniformly bounded. Because F is bounded on that bounded set, the trajectory is uniformly Lipschitz in time in BxB, and has a norm limit at T. This explicit time-Cauchy step is needed: a bounded set in an infinite-dimensional Banach space need not be compact. The limiting a remains >=exp(-MT)>0, so Picard at that limit extends the solution beyond T. Only the slope bound on the already existing interval was assumed. The desired logarithmic time was never assumed to lie in that interval.

## Adversarial controls and legacy reproduction

Fresh `existence_controls.py` passes **55 assertions: 32 exact/symbolic controls and 23 finite floating-point observations**. Formal identities are universal only within their explicitly displayed polynomial/rational families; numerical observations are finite and are not validated PDE simulations. The general theorem rests on the proof above and in the early sealed reconstruction.

The negative controls show concretely that the wrong unweighted label mean produces K(1)=-a*d/30, and an unweighted primitive constant produces physical mean -a*(a*d+7*b)/1260 in the coordinate family used. Omitting mean subtraction breaks periodicity. Matching endpoint values is essential for mean conservation. The degree-one lift X=x+2x(1-x) folds: X(1/2)=X(1)=1 and X'(1)=-1. Forcing matched endpoint derivatives excludes the peak and is not invariant under its flow. The cutoff proxy has a second derivative 135/(32 delta) at quarter width while its C1 scale is small, making a C2-based shared-lifetime argument fail. Relabeling, exact background characteristics, weak boundary cancellation, and the corner-jump identities also pass.

All three legacy scripts were executed byte-identically in ignored isolated folders using `/usr/bin/python3`, Python 3.9.6 and SymPy 1.14.0. Original `check_identities.py`: 20; old independent verifier: 135; copied old submitted verifier: 20. Their outputs reproduce the frozen receipts exactly (the submitted scripts' written receipts also match bytes). All16 original snapshot hashes remain unchanged before/after. Replay receipts record commands and hashes. No legacy script was run in the original folder where it could overwrite a frozen receipt.

After the early seal, the literal 2018 v1 Section 4 was checked. Its fixed translated peak plus smooth periodic perturbation class is not generally invariant: u0=phi+e sin(x) has J(0)=2kappa but J'(0)=-4kappa e!=0, whereas that representation would force the fixed jump J(t)=2kappa. V1_DOMAIN_CONTROL.md records this exact old-route obstruction. It is a domain-mechanism counterexample, not a disproof of weaker-norm instability and not a statement of the authors' motives. The current candidate lets the jump evolve and avoids it.

## Failure inventory, exact gap and disposition

No mathematical failure was found in the assigned existence family. The strongest verified conclusion is a locally unique, corner-compatible mean-zero Banach characteristic evolution, with common initial lifespan, correct weak Eulerian PDE, moving-chart continuity, evolving one-sided slopes, smoothness preservation, and bounded-slope continuation. It supports the scoped strong-norm proof. It supplies no fixed weaker-norm departure or global continuation/selection principle. The broad target must remain partial, and historical novelty unconfirmed.

One historical scope-reporting contradiction was found and reported immediately to the root audit: the frozen PR body says all changes are inside the attempt folder and denies any queue edit; provenance sets shared_queue_modified=false, and the old log also denies shared queue changes. The exact 17-file diff does edit QUEUE.md, preserving unsolved/partial status and advancing the ledger to 1/5. This contradiction requires current metadata reconciliation by the root, while preserving the frozen originals. It is not a candidate proof correction. No queue/canonical/PR/publication change was performed by this family.

All checks and derivations are confined to this dedicated family. Foreign primary PDFs/text and all legacy executable copies/streams are under ignoredtmp. The final self-excluding manifest records own artifacts; the source/replay ledgers retain hashes for ignored inputs. Completion: 100% of this assigned family audit, not 100% of the original nonlinear research question.
