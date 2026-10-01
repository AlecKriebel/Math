# Independent first-pass reconstruction

Sealed at 2026-10-01 18:18:48 UTC before historical review, proposer correction, or root/sibling conclusions. Primary source bodies read: Goresky-Pardon 1989 §§2.1/2.4/3.1/4.1/5.1/6/7/8.1-8.3/10.1-10.2 (including all of the proof on printed pp.339-340); Goresky 1984 §§2-3 (printed pp.486-496), §5.1-5.2; Goresky-MacPherson 1980 §4.1-4.2 including proof (printed pp.151-153). Visually checked Goresky-Pardon pp.330,335,339,340 and Goresky 1984 pp.485-487. No previous review material has been read.

## Result at the published theorem level

The exact negative answer follows from the printed Goresky-Pardon §10.2 corollary, after the adapters below. I found no hidden need for coherently oriented links, orientable singular strata, or a locally square-free hypothesis in that corollary. This supports the candidate's classification as a literature result. I do not yet certify every detail of the printed cochain proof: its unrestricted middle-perversity operation notation and integral lift deserve a separate qualification, described below.

## Checkable adapter

Let n=4j+2, r=2j+1, F=F2, m(c)=floor((c-2)/2), u(c)=floor((c-1)/2), t(c)=c-2. Then m+u=t and 2m<=t. Define V=I^mH_r(X;F). For a Witt space the comparison V -> I^uH_r(X;F) is an isomorphism. Complementary-perversity duality therefore makes the middle pairing B on all of V nonsingular. It is not merely an ordinary cohomology or an image pairing.

Under the compact mod-two identification I^mH_r(X;F)=IH_m^r(X;F), the diagonal operation is

    Sq^r: IH_m^r(X;F) -> IH_t^(2r)(X;F) -> F,
    B(x,x) = epsilon(Sq^r(x)).

One may enlarge the target perversity from 2m to t using the natural comparison. The diagonal-square property is established for the operations of Goresky 1984 §3.4, and is stated in Goresky-Pardon §4.1. The orientation corollary of §10.2 sets this odd-degree number to zero for every x. Thus B is alternating.

For an arbitrary finite-dimensional nonsingular alternating form over F, take e!=0. Nonsingularity supplies f with B(e,f)=1; alternation gives the matrix [[0,1],[1,0]] on span(e,f). This plane is nonsingular. For any x, x+B(x,f)e+B(x,e)f belongs to its orthogonal complement. Induction splits V as an orthogonal sum of such planes. The span of their e-vectors is a Lagrangian. The zero-dimensional case terminates immediately. Hence [B]=0 in W(F), without a classification theorem about W(F).

## Local orientation, arbitrary strata and normalization

In a distinguished chart R^s x cL, the regular portion is R^s x (0,1) x L_reg. Restrict the integral orientation there, fix an orientation of R^s and the radial interval, and cancel those oriented factors. This orients every component of L_reg. It proves each fiber link is orientable. A loop in a nonorientable singular stratum may reverse both the stratum orientation and the link-fiber orientation while preserving the ambient regular orientation. The proof needs no coherent fiber orientation over such a loop.

Goresky-Pardon assumes normal connected spaces globally in §2.4. Removing that restriction is not justified merely by citing its normalization cobordism statement. Instead, Goresky-MacPherson 1980 §4.2 gives an actual chain-complex isomorphism for every traditional perversity under normalization. Its proof uses the common regular part; coefficientwise it works over F2. Links of the normalization are normalizations of the corresponding local branches, so their middle groups are summands of the normalized link's middle group. The link Witt vanishing is preserved. The regular orientation lifts.

Pairing preservation also has an explicit check: if two middle chains are in stratified general position, their expected intersection dimension inside a codimension-c stratum is

    2(r-c+m(c))-(2r-c)=2m(c)-c <= -2.

Thus their zero-dimensional intersections lie entirely in the regular part, where normalization is a homeomorphism. Intersection multiplicities and augmentation agree. Applying the corollary on the normal components and taking their orthogonal sum establishes the assertion for nonnormal or disconnected X.

For j=0, r=1 and Sq^r=Sq^1; the orientation corollary still applies. Normal two-dimensional spaces have circle links and are surfaces, while the normalization argument covers nonnormal surfaces. No positive-degree division or surgery induction at j=0 occurs.

## Proof-level qualification found independently

The literal §10.2 lemma and its J_j/D_j maps are printed with middle perversity on both sides. This is broader than the general operations in §4.1, whose target perversity doubles. Goresky 1984 §3 explicitly warns that general squares need not stay in middle perversity. Goresky-Pardon §10.3 likewise warns that Sq^1 may not be an operation on middle intersection homology. Therefore the published corollary should be cited in its precise number-valued form; the audit must not turn the displayed lemma into a universal middle-to-middle Sq^1 or a full Steenrod algebra claim.

A second issue is the proof's step choosing an integral cochain lift c~ in IC_m(Z) with d c~=2y, y in IC_m(Z). The paper's own §6.3 gives a link-torsion criterion for a Bockstein preserving a perversity, and local orientability in §8.3 establishes it for t, not automatically for m. An orientable RP^3 link in even codimension four has H^2(RP^3;Z)=Z/2, which triggers the obstruction at m(4)+1=2 while its odd-codimension Witt restrictions are vacuous. This is a countercontrol against silently assuming coefficient reduction is surjective on every middle integral cochain model; it is not a counterexample to the number-valued corollary or target claim. I have not supplied a new replacement universal cochain argument.

Decision at this seal: **qualified pass for the exact claim as an adapter to a printed published corollary; do not label this a complete independent chain-level verification of every line in §10.2.** If the requested certification demands an independently reconstructed universal proof rather than theorem-level source verification, that subroute is blocked pending a precise resolution of these types/lifts. The remaining independent task is reconciliation with historical source discussion and exact algebraic probes.

Family audit completion estimate: 70%.
