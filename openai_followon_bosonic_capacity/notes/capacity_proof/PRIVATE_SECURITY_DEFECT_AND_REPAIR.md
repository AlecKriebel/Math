# Private dynamic source: literal security defect and a repaired converse

Checkpoint: 2026-10-06 21:33 Pacific (2026-10-07 04:33 UTC).

This note records a substantive operational issue detected independently during the source audit. It **changes the qualification of the earlier conditional derivation**: the private region cannot be quoted as correct under the source paper's literal predecoded joint secrecy condition. The repair below applies to the conventional condition in which only **generated private information and generated key** must remain secret, while consumed private communication and consumed key may acquire correlations during use. The distinction must be explicit in any manuscript or target statement.

## 1. The printed condition and the zero-channel counterexample

The primary source is Wilde–Hsieh, arXiv:1005.3818v3, Section 5, directly between Eqs. (13) and (14). Its secrecy condition requires

\[
\tag{LIT}
\left\|\omega^{M K E^n T_A L J S_B}
-\pi^{M T_A J S_B}\otimes\sigma^{K L E^n}\right\|_1\le\epsilon.
\]

Here \(M\) is the generated private message, \(T_A\) the generated key share, \(J\) the **consumed** private-communication register, and \(S_B\) Bob's share of the **consumed** key. The paper then uses small \(I(MJ S_B T_A;E^nKL)\) in its converse. This is not a harmless notation or partial-trace artifact: the displayed state is before Bob decodes, and \(S_B\) is explicitly retained in it.

Take a uniform one-bit message \(M\), an independent uniform one-bit key \(S_B\), and the ordinary one-time-pad public ciphertext \(L=M\oplus S_B\). The message alone is perfectly independent of \(L\); however,

\[
I(MS_B;L)=1.
\]

For \(n\) independent bits this mutual information is \(n\). Thus the one-time-pad resource triple \((R,P,S)=(-1,1,-1)\), which the paper explicitly uses in its achievability cone, fails (LIT).

This is more than failure of that particular construction. At zero noisy-channel input energy, every noisy output is vacuum. For any catalytic protocol obeying (LIT), initial \(M\) and \(S_B\) are independent and remain so marginally, because an Alice-local trace-preserving encoder cannot change their joint marginal. Taking suitable marginals of (LIT) gives \(M S_B\) asymptotically independent of the public transcript \(L\). Hence

\[
I(M;LS_B)=o(n).
\]

Bob can obtain private-message information only from \(L,J,S_B\) (and vacuum). Therefore reliability and data processing imply

\[
n\bar P\le I(M;LJS_B)+o(n)
\le\log|J|+I(M;LS_B)+o(n)
=n\widetilde P+o(n).
\]

Consequently the net private rate satisfies \(P=\bar P-\widetilde P\le0\) under (LIT). But the target's zero-energy inequalities admit \((-1,1,-1)\). **The target private region is false under the literal printed condition.** Allowing additional catalytic private communication does not evade the net inequality above.

The \(o(n)\) estimates use finite resource rates and entropy continuity on the finite classical private registers; they do not rely on Eve being finite dimensional. The consumed key is not a reference system that can be traced away while retaining the printed security promise.

## 2. Correct conventional generated-resource security

Let overbars denote generated rates and tildes consumed rates. Define

\[
W=(M,T_A),\quad X=(K,L),\quad V=(J,S_B),\quad Y=(W,V).
\]

The conventional predecoded secrecy condition is

\[
\tag{GEN}
\left\|\omega^{W X E^n}-\pi^W\otimes\sigma^{X E^n}\right\|_1\to0,
\]

with \(\pi^W\) uniform on the generated message/key registers. It promises secrecy of the generated output resources and includes all public information and Eve's channel outputs. It does not promise residual secrecy of resources that the protocol consumes. It allows the one-time pad. Together with correctness, it gives

\[
I(W;E^n X)=o(n),
\]

and the usual \(o(n)\) bounds for reliably shared classical output resources. Trace-norm vanishing alone implies sublinear leakage, sufficient for a rate converse; an assertion of absolute leakage tending to zero requires a stronger decay or separate criterion. This remains a uniform-source security condition, without a semantic-security claim.

## 3. A repaired full converse under (GEN)

The following argument derives the same general one-block private dynamic inequalities without ever assuming joint secrecy of \(W,V\). All registers other than the channel outputs are classical and finite dimensional. All terms are defined for finite-energy bosonic outputs.

### Bound on public plus private communication

Correctness and data processing give

\[
n(\bar R+\bar P)\le I(KM;B^nLJS_B)+o(n).
\]

Initially \(KM\) is independent of \(S_B\), and their marginal stays unchanged. The chain rule gives

\[
\begin{aligned}
I(KM;B^nLJ S_B)
&=I(KM;B^nLJ|S_B)\\
&=I(KM;LJ|S_B)+I(KMLJS_B;B^n)-I(LJS_B;B^n)\\
&\le \log|L|+\log|J|+I(XY;B^n).
\end{aligned}
\]

Adding \(T_A\) to the first mutual-information argument only increases it. Subtracting consumed \(\widetilde R,\widetilde P\) gives

\[
\tag{A} n(R+P)\le I(XY;B^n)+o(n).
\]

### Bound on private communication plus secret key

Correctness, giving the public register \(K\) to Bob for the converse, and (GEN) give

\[
n(\bar P+\bar S)
\le I(W;B^nXV)-I(W;E^nX)+o(n)
=I(W;B^nV|X)-I(W;E^n|X)+o(n).
\]

The exact chain-rule identity is

\[
\begin{aligned}
I(W;B^nV|X)-I(W;E^n|X)
={}&I(WV;B^n|X)-I(WV;E^n|X)\\
&+I(W;V|X)-I(V;B^n|X)+I(V;E^n|WX).
\end{aligned}
\]

Since \(V\) is classical,

\[
I(W;V|X)+I(V;E^n|WX)
\le H(V|X)-H(V|WX)+H(V|WX)=H(V|X),
\]

and \(I(V;B^n|X)\ge0\). The remainder is therefore at most \(H(V|X)\le\log|V|=n(\widetilde P+\widetilde S)\). Subtracting the consumed rates yields

\[
\tag{B}n(P+S)\le I(Y;B^n|X)-I(Y;E^n|X)+o(n).
\]

### Bound on the sum of all three resources

Correctness and (GEN) give

\[
n(\bar R+\bar P+\bar S)
\le I(KW;B^nLV)-I(W;E^nX)+o(n).
\]

Expand the right side as

\[
I(XY;B^n)-I(Y;E^n|X)+T,
\]

where

\[
T=I(KW;LV)-I(LV;B^n)+I(V;E^n|WX)-I(W;X).
\]

Another exact identity is

\[
I(KW;LV)-I(W;KL)
=I(K;L)-I(W;K)+H(V|L)-H(V|KWL).
\]

Now use \(I(V;E^n|WX)\le H(V|WX)=H(V|KWL)\), and drop the two nonpositive terms \(-I(W;K)\), \(-I(LV;B^n)\). This gives

\[
T\le H(L)+H(V|L)\le\log|L|+\log|V|
=n(\widetilde R+\widetilde P+\widetilde S).
\]

Subtracting the consumed rates gives

\[
\tag{C} n(R+P+S)\le I(XY;B^n)-I(Y;E^n|X)+o(n).
\]

(A)–(C) are precisely the general mixed-ensemble private dynamic bounds. Conditional on the classical finite \(X,Y\) registers, the physical \(n\)-mode input is a density operator \(\rho_{xy}\); its average is exactly the actual code input, so the energy constraint is preserved. For a degradable channel, the coordinatewise pure refinement in CONDITIONAL_DERIVATION.md then applies, followed by its conditional entropy argument. Thus the **conventional** private region still follows from (VE), but it now rests on the repaired converse just given rather than the source's excessively strong joint secrecy assumption.

## 4. Achievability qualification and priority

The publicly enhanced private father plus one-time-pad, key-distribution, and private-to-public protocols naturally match (GEN). Their composition consumes key/private resources, so it should not be assessed by (LIT). A complete unconditional capacity theorem under (GEN) still needs its direct-coding energy audit and its appropriate secrecy guarantee, as recorded in the earlier derivation. This note is a new independent repair derivation, not a priority claim: search existing corrections, later books and resource-theory formulations before claiming novelty.

If the user strictly requires the literal printed (LIT) convention, the original requested formula is refuted at \(N=0\). If the intended target is the standard net-resource operational region with consumed resources allowed to be used, the repair makes the operational convention precise and removes this defect. A manuscript must display this distinction; it must not silently redefine the original source theorem.
