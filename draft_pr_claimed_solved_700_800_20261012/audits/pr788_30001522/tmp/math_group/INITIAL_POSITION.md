# Independent initial position: compact-group family

Frozen UTC: 2026-10-16T13:56:38.528381+00:00
Completion estimate toward this validation family: 65% (primary definitions and independent candidate mechanism checked; arbitrary continuous-circle quotient category and submitted proof remain to be audited).

Independence boundary: before this document, read only intake SELECTED_PUBLIC_RECORD, ROOT_SOURCE_IDENTITY, ELIGIBILITY_GATE, RAM_WORKSPACE_RECEIPT and the original Hanke report. No author proof, historical audit, current peer/root mathematical conclusion was opened. Intake title supplied SU(3)/SO(3) as a candidate hint; the arguments below are reconstructed independently.

## Exact source target

Hanke, Oberwolfach Report 32/2010, printed p. 1912, PDF p. 28, defines both ranks by free actions on X itself. The displayed definitions do not replace X by another finite complex in its homotopy type or rational homotopy type, and do not say almost free. The report requires finite connected X, abelian fundamental group acting trivially on higher homotopy, and finite total rational homotopy dimension. The last paragraph asks for strict inequality at infinitely many primes. These hypotheses are reproduced by the curated target. Source read scope: printed 1912-1914; visual inspection of complete 1912. Primary body lives only in sibling scratch.

## Independent mechanism

Let W=SU(3)/SO(3), with SO(3) embedded by real matrices. It is a compact connected smooth 5-manifold, hence has a finite triangulation. The homotopy sequence gives pi_1(W)=0 and pi_2(W)=Z/2, since pi_1(SU(3))=pi_2(SU(3))=0 and pi_1(SO(3))=Z/2. Hurewicz gives H_2(W;Z)=Z/2. W is oriented because its isotropy group is connected. Poincare duality and the integral universal coefficient theorem give homology Z in degrees 0,5, Z/2 in degree 2, and zero otherwise. In particular, for every odd p, H*(W;F_p) is that of S^5. The simply connected rational homology 5-sphere is rationally equivalent to S^5 by rational Hurewicz and rational Whitehead, so its only rational homotopy is Q in degree 5. The source homotopy hypotheses hold, and -chi^pi(W)=1.

A left multiplication element g fixes h SO(3) iff h^-1 g h is in SO(3). Every element of SO(3) has complex eigenvalue 1. For odd prime p put zeta=exp(2 pi i/p) and g=diag(zeta,zeta,zeta^-2). Every nonidentity g^k has no eigenvalue 1: p does not divide k or 2k. Thus C_p acts freely for every odd p, including p=3 (where the generator is central). This is a universal congruence proof, not an inference from finitely many primes. For p=2 this generator has eigenvalue 1 and belongs to SO(3), so the construction fails at precisely the even prime.

For any arbitrary continuous free E=(Z/p)^r action on W with p odd, the top cohomology action is trivial because a p-group cannot map nontrivially to {+1,-1}; the two-row Borel spectral sequence has a possible d_6 only. The quotient has no cohomology in sufficiently high degrees, hence multiplication by the transgression class in degree 6 must eventually give isomorphisms H^n(BE;F_p) -> H^(n+6)(BE;F_p). But dim H^n(BE;F_p)=binomial(n+r-1,r-1), strictly increasing with n when r>=2. Therefore r<=1. This bounds all free actions, not merely left-translation subgroups, and proves rk_p(W)=1 for every odd p.

## Circle obstruction and category checkpoint

For a hypothetical free circle action, the principal bundle S^1 -> W -> B gives pi_1(B)=0. If B is an oriented integral Poincare duality space of formal dimension 4 (as for every smooth free action; for arbitrary continuous actions this follows if the orbit is an orientable integral cohomology 4-manifold with the required duality), then H_2(B;Z) is free and its intersection pairing is unimodular. Homotopy exactness says pi_2(W)=Z/2 injects into pi_2(B), since pi_2(S^1)=0. Hurewicz identifies pi_2(B)=H_2(B;Z), a contradiction. Equivalently, a rank-one primitive Euler-class argument via Gysin gives the same contradiction. Thus rk_T(W)=0 in the smooth category, with one explicit standard-theorem dependency to check for fully arbitrary continuous actions: integral PD for B. No claim that merely excluding a circle inside SU(3) excludes arbitrary circle actions.

The Borel p-rank argument also requires that a free finite-group quotient of compact W has bounded cohomological dimension. Here a free finite action makes W -> W/E a covering and W/E a compact topological 5-manifold, so this is secure.

At p=2 the strongest independently established fact so far is only that the particular diagonal involution is not free. A possible further obstruction uses the nonzero Stiefel-Whitney number <w_2 w_3,[W]> and preservation under a covering, but it must be proved rather than assumed. No p=2 value is needed for the infinite-prime target.

## Initial assessment

The exact fixed-space claim is strongly supported: all odd-prime free p-ranks equal 1; smooth free toral rank equals 0; rational homotopy hypotheses hold. The remaining gap for the original action category is the orbit-space PD theorem for arbitrary continuous free circle actions. This is validation work, not a new substantive proof-search turn. Novelty and current open status are outside this mathematical-family verdict.
