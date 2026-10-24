# Centralizer obstruction to transplanting the known lift examples

Draft for independent adversarial review; 2026-10-24 UTC. No original-result claim.

## Claim

For every subgroup H of a right-angled Artin group A and every 1 != z in Z(H), no nonzero power z^m belongs to [H,H]. In particular a group possessing a nontrivial central element with torsion image in its abelianization cannot embed in any RAAG.

Proof using the Servatius centralizer theorem: conjugate z to a cyclically reduced element. Write its block-root decomposition z=r_1^{e_1} ... r_k^{e_k}, where k>=1, all e_i are nonzero integers, distinct blocks commute, and the centralizer is <r_1> x ... x <r_k> x A(link supp(z)). Projection onto the first cyclic factor is a homomorphism lambda:C_A(z)->Z with lambda(z)=e_1 != 0. Because H<=C_A(z), lambda kills [H,H] but lambda(z^m)=m e_1 !=0. For infinite defining graphs it suffices to restrict to the finite induced subgraph containing the finitely many letters in z and any asserted finite commutator expression; this finite RAAG is a retract.

Finite index persistence (general H, with z of infinite order): if z^m in [H,H] for an integer m != 0, then for every finite-index subgroup K<=H some positive power z^d lies in Z(K). Transfer H_1(H;Q)->H_1(K;Q) sends the zero class of z^m to [H:K]/d times the class of z^{md}, because z is central. Thus the class of z^d vanishes in H_1(K;Q), so some positive power of z^d lies in [K,K]. Therefore no finite-index subgroup K embeds in a RAAG either. An alternative proof uses rational homological transfer by passing to the normal core and summing lifts.

## Application to golden-ratio Thompson lift

Fournier-Facio--Lodha, arXiv:2110.06286v2, Lemma 3.15: for the full lift G of T_tau, G'=H is the full lift of T_tau', and [G:G']=2. The central unit translation z lies in the kernel Z of H->T_tau', hence z is a nontrivial central element of G'. It follows directly that z in [G,G], and G cannot embed in a RAAG. The finite-index argument excludes virtual embedding as well. This is an obstruction to transplanting this particular irrational-scl group; it is not a proof that all subgroups or all potential irrational-scl examples fail.

## Application to Zhuang lifts

For integer independent p,q, A=Z[1/p,1/q] includes 1/p^n. The circle rotation by 1/p^n belongs to T(1,A,<p,q>); its lift is translation x->x+1/p^n. Thus the central unit translation has p^n-th roots for every n. Under an embedding in a finite RAAG, its nontrivial image g would have arbitrarily deep roots. Servatius' root-block decomposition of a fixed g bounds root exponents by gcd(|e_1|,...,|e_k|); contradiction. This already excludes direct embeddings of the full lifted group. For any finite-index subgroup, its intersection with the subgroup of p-power translations is still p-divisible, hence nontrivial roots persist: the finite quotient of Z[1/p] by the intersection has order coprime to p, so multiplication by p is an automorphism and the intersection remains p-divisible. Verify this finite-index assertion adversarially before use.

## Scope

Only a transplant barrier. It does not exclude suitable subgroups of these lift groups whose irrational element survives, does not show scl preservation under any embedding, and does not answer Kourovka 21.127.
