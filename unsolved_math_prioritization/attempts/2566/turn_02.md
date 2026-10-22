# Attempt 2/5: quotient lifting and the smallest counterexample

Date: 2026-10-03 UTC. Objective: force a minimal counterexample to disappear by removing solvable normal layers. Outcome: a proved radical-free, faithful-action reduction; the nonsolvable layer remains.

Throughout pi is a set of odd primes, G=HN, H is pi-maximal in G, N is normal in G, and A=H∩N. The first turn justifies these reductions. A counterexample means A is not pi-maximal in N.

## 1. A quotient lemma, proved directly

Let R be solvable and normal in G, with R≤N. Write q:G→G/R.

First H is pi-Hall in HR. Indeed HR is solvable (its normal subgroup R and quotient HR/R≅H/(H∩R) are solvable), so Hall's embedding theorem supplies a pi-Hall subgroup of HR containing H. Maximality of H forces it to equal H. Consequently H∩R=A∩R is pi-Hall in R.

Next q(H) is pi-maximal in G/R. Suppose q(H)≤Kbar≤G/R with Kbar a pi-group. The preimage E=q^{-1}(Kbar) is solvable: R is solvable and Kbar has odd order. A pi-Hall subgroup L of E can be chosen to contain H. Its image q(L) is all of Kbar because [Kbar:q(L)] divides both the pi'-number [E:L] and the pi-number |Kbar|. Maximality in G gives L=H, hence Kbar=q(H).

Finally,

A is pi-maximal in N if and only if q(A) is pi-maximal in N/R.

For the forward direction, suppose q(A)<Bbar is a pi-subgroup of N/R. Its preimage E_N in N is solvable. A pi-Hall subgroup B of E_N can be chosen to contain A. The same index argument gives q(B)=Bbar, so B>A, contradicting maximality of A.

For the reverse direction, let A≤B≤N be a pi-subgroup and suppose q(A) is maximal. Then q(B)=q(A), so B≤AR. As A∩R is pi-Hall in R,

[AR:A]=[R:A∩R]

is a pi'-number. Since [B:A] is a pi-number dividing it, B=A.

Also q(H)∩(N/R)=q(A), because R≤N. Thus the quotient configuration is a counterexample precisely when the original one is. This is a genuine equivalence, not just preservation of a weak submaximal property.

## 2. Remove the solvable radical of N

Choose a counterexample with |G| least. The solvable radical R=Rad(N) is characteristic in N and therefore normal in G. If R≠1, the quotient lemma yields a smaller counterexample. Hence

Rad(N)=1.

In particular Z(N)=1, and N is nonsolvable by turn 1. This rejects searches in soluble kernels and their extensions before expensive subgroup enumeration.

## 3. Remove the solvable radical of G

Let T=Rad(G). Since T∩N is solvable and normal in N, it is trivial. The image of T in G/N is therefore injective. Since G/N is a pi-group, T is a pi-group. Normality makes HT a pi-subgroup (an extension of T by H/(H∩T)), and maximality gives T≤H.

If T≠1, pass to G/T. A pi-subgroup containing H/T lifts to a pi-subgroup containing H, so H/T is pi-maximal. Also N maps isomorphically onto NT/T, and

(H/T)∩(NT/T)=AT/T.

For the last identity, if h∈H and h=nt with n∈N,t∈T≤H, then n=ht^{-1}∈H∩N=A. Any pi-overgroup of A in N survives isomorphically in NT/T, giving a smaller counterexample. Therefore Rad(G)=1 as well.

## 4. The action on N is faithful

C=C_G(N) is normal in G and C∩N=Z(N)=1. Thus C embeds into the odd pi-group G/N, so C is solvable. Rad(G)=1 forces C=1. Conjugation consequently embeds G into Aut(N), with N identified with Inn(N) because Z(N)=1.

Every hypothetical minimal counterexample can therefore be taken to have:

- G=HN and G/N a pi-group;
- Rad(G)=Rad(N)=1;
- N≤G≤Aut(N) in the conjugation embedding;
- H odd, solvable, and pi-maximal;
- A=H∩N properly contained in some pi-subgroup of N.

## 5. Why this does not finish the proof

Radical-free is not the same as simple or almost simple. The socle of N can be a product of simple factors, and N itself may have a nontrivial outer-action quotient. More importantly, quotienting by a nonsolvable minimal normal subgroup does not satisfy the solvable lifting lemma: a preimage of a pi-group need not be solvable and Hall's embedding theorem cannot be invoked.

Thus an induction that silently replaces an arbitrary normal layer by its quotient would beg the central question. The reduction isolates the difficulty but does not eliminate it.

## Result after this turn

Counterexamples, if any, persist after stripping all solvable normal layers and can be chosen with faithful ambient action on a radical-free normal subgroup. No universal proof or counterexample. Budget used: 2/5 substantive attempts.
