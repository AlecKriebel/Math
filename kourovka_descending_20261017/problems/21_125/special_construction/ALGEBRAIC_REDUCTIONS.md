# Algebraic constructive routes for ordinary Hydra groups

Author investigation: October 24, 2026 UTC. These are supporting deductions and route obstructions, not a resolution of Kourovka 21.125(b). No originality claim is made for the elementary reductions or the rederivation of a known small rank.

Use the canonical square presentation
\[
H_r=\langle s,u_1,\ldots,u_r\mid [s,u_1]=1,
 u_i^{-1}s u_i=u_{i-1}\ (2\le i\le r)\rangle.
\]
As established in Dison–Riley, *Hydra groups*, CMH88(2013), pp.510–511, this is the ordinary Hydra group. The top letter is the original free generator a_r, and s is the inverse of the original stable letter. Each H_(r+1) is a cyclic HNN extension of H_r identifying <s> with <u_r>. The base injects by Britton's lemma.

## Route 1: a sufficient marked HNN embedding criterion

**Lemma.** Suppose B embeds in a group A, p,q are nontrivial elements of B, and v in A satisfies v^-1 p v=q. Then
\[
\langle B,t\mid t^{-1}pt=q\rangle
\hookrightarrow
\langle A,z\mid z^{-1}pz=p\rangle,
\qquad t\longmapsto zv.
\]

**Proof.** The relation is respected. In a reduced HNN word, a subword t^-1 b t could acquire a pinch in the target only when b belongs to <p>; this is already a forbidden pinch in the source. A subword t b t^-1 becomes z(v b v^-1)z^-1 and could acquire a pinch only when v b v^-1 belongs to <p>, equivalently b belongs to <q>; again it was a source pinch. The outer factors v or v^-1 do not change this analysis of successive opposite stable letters. Thus a source word containing stable letters remains Britton-reduced in the target. Words in B remain nontrivial by the initial embedding. This proves injectivity.

If A is a RAAG and p is conjugate to an individual standard vertex generator or its inverse, the target is a RAAG: change the centralizing letter by the same conjugator and append one new vertex adjacent just to that vertex. Thus the lemma yields a genuine algebraic construction, provided one already has the required marked embedding and conjugacy.

That final proviso is substantial. Given only a virtual embedding of B in some RAAG, its two edge elements need not become conjugate, much less conjugate to a standard vertex generator.

## An explicit successful small-rank construction

For H_2=<s,u,a | [s,u], a^-1 s a=u>, take the index-two subgroup K defined by a-exponent modulo2. Reidemeister–Schreier gives
\[
K=\langle x,y,w,r\mid[x,y]=[y,w]=1,
 r^{-1}xr=w\rangle,
\quad x=asa^{-1},\ y=s,\ w=u,\ r=a^2.
\]
The base group B=<x,y,w | [x,y],[y,w]> is F(x,w)×<y>.

Let A=<p,b,c | [p,b],[b,c]>=F(p,c)×<b>. Map
\[
x\mapsto p,\qquad y\mapsto b,\qquad w\mapsto c^{-1}pc.
\]
The two elements p and c^-1pc freely generate a free group: an alternating reduced product of their nonzero powers expands to a nonempty reduced word in p,c (the c transitions separating the two conjugate cyclic subgroups cannot disappear). Consequently this embeds B in A. The lemma now sends r to zc in
\[
A'=\langle p,b,c,z\mid[p,b],[b,c],[p,z]\rangle=A(P_4).
\]
This is an explicit injection of the index-two subgroup K into a RAAG.

This rederives a previously known small rank and is not a new answer to the target r≥5. It also exposes a concrete induction difficulty: s maps to b, while a^2 maps to zc. In the further subgroup with equal edge orders2, s^2 and a^2 map to b^2 and zc; their abelianizations in this A(P4) are different, so they are not conjugate there. Conjugating the entire embedding, or applying a common automorphism of A(P4), cannot repair that inequality. This statement concerns this particular embedding, not every possible re-embedding in a different RAAG. A new marked construction is required.

## Route 2: finite covers can impose the entire preceding virtual subgroup

**Balancing/extension lemma.** For every finite-index subgroup L≤H_r there is a finite-index normal subgroup J≤H_(r+1) such that J∩H_r≤L. Its Bass–Serre graph of groups has all vertex groups conjugate to J∩H_r and all edge groups infinite cyclic. In particular, if L is (compact) special, every vertex group can be made (compact) special in a finite cover of H_(r+1).

**Proof.** Replace L by its normal core and take a finite quotient π:H_r→Q0 with kernel contained in L. Let the orders of π(s),π(u_r) be d,e, and choose a positive integer N divisible by both. The abelianization of H_r is free abelian on s,u_r, since all lower u_i become s. Hence there is a map χ:H_r→(Z/N)^2 taking s to (1,0) and u_r to (0,1). Let Q be the image of (π,χ). Both images p,q of s,u_r in Q have exact order N, and ker(H_r→Q)≤L.

Embed Q faithfully in Sym(Q) by its regular action. The permutations representing p and q each consist of |Q|/N cycles of length N, so they are conjugate in Sym(Q). Choose a permutation v taking p to q in the convention v^-1 p v=q. The HNN relation therefore extends the map H_r→Sym(Q) to H_(r+1) by u_(r+1)→v. Its kernel J is finite-index normal and intersects H_r in precisely ker(H_r→Q). All other vertex stabilizers are its conjugates. Each cyclic edge group intersects J in the subgroup generated by the corresponding Nth power. This proves the assertion. Finite-index subgroups of a special group are special by taking covers; finite covers preserve compactness.

This is not a special-combination theorem. A finite graph of special groups with cyclic edge groups need not be promoted to special without additional hypotheses. The lemma removes only a finite-cover compatibility difficulty; it does not provide a RAAG embedding of the resulting graph of groups.

## Why a direct malnormal hierarchy does not complete the induction

For r≥2 the top cyclic subgroup <a_r>=<u_r> is malnormal in H_r. Write H_r=F_r⋊<t>, with t^-1 a_i t=a_i a_(i-1). If g a_r^k g^-1=a_r^l with k,l nonzero, abelianization in H_r forces k=l. Write g=w t^n. Then φ^-n(a_r) is conjugate to a_r in F_r, using unique roots in the free group. Its coefficient on a_(r-1) in free abelianization is -n, while a_r has coefficient0, so n=0. Now w centralizes a_r^k in a free group, and w belongs to <a_r>. This proves malnormality.

The other edge subgroup <s>=<t> is not malnormal. In fact its centralizer contains
\[
\langle a_1,a_2a_1a_2^{-1}\rangle\times\langle t\rangle\cong F_2\times\mathbb Z,
\]
since both displayed free words are fixed by φ. Their free independence follows, for example, by reduced free-word normal forms. This persists as a noncyclic centralizer in every finite-index subgroup, after taking suitable powers of the displayed elements. Thus passing to a finite cover does not make this cyclic edge subgroup malnormal.

A combination theorem demanding malnormality of every incident cyclic edge group therefore cannot be applied directly. One-sided malnormality is useful structure, but no theorem or construction that fills this missing combination step has been proved here. Treat that route as blocked until a materially new mechanism is supplied.
