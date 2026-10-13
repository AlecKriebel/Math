# Generated-secret-only catalytic converse with classical consumed registers

Checkpoint: 2026-10-06 21:25 America/Los_Angeles. The initial proof used degradability, explaining the retained filename. Coding_repair independently identified a general entropy argument; the argument below uses classical consumed registers instead and needs no channel degradability. It corrects the literal security assumption rather than silently identifying the models. It does not validate the strong consumed-resource criterion. This is an explicit derivation within this effort, subject to independent review and priority checks, with no claim that the elementary correction is historically new.

Let K,M be independent uniform generated public/private messages, S_B the initially independent consumed key, T_A the generated key, L the consumed public communication and J the consumed private communication. Write

\[
X=KL,\qquad W=MT_A,\qquad V=JS_B,\qquad Y=WV.
\]

Assume reliability and generated-secret-only security: the generated outputs approach the ideal product correlations, and W approaches a uniform product register independent of X and Eve's full final system. In the displayed converse inequalities E denotes the physical channel-complement output before Bob's decoding. Tracing full Eve security to this channel marginal supplies the required security bound, and the conditional input ensemble has the required channel-output form. Consumed registers V are not required to remain independent of W or public data. All message, key and consumed communication registers are classical and finite at each block length. The physical channel can be arbitrary, and its inputs can be entangled across all uses.

The finite-block bounds, with continuity/reliability remainder o(n), are

\[
\begin{aligned}
n(\bar R+\bar P)&\le I(XY;B)+\log|LJ|+o(n),\\
n(\bar P+\bar S)&\le I(Y;B|X)-I(Y;E|X)+\log|JS_B|+o(n),\\
n(\bar R+\bar P+\bar S)&\le I(XY;B)-I(Y;E|X)+\log|LJS_B|+o(n).
\end{aligned}
\]

Subtracting consumed rates gives the original regularized information converse under this explicitly repaired convention. The original first-bound argument does not invoke joint secrecy and applies unchanged: K,M remain jointly independent of S_B before public conditioning, and adding T_A to the classical input label increases I(label;B).

## Exact entropy identity for the second bound

Reliability and data processing give n(bar P+bar S)<=I(W;B V X)+o(n). Generated-secret-only security permits subtracting I(W;E X)=o(n). The resulting expression is

\[
F=I(W;BV|X)-I(W;E|X).
\]

Expanding by the chain rule,

\[
F=I(WV;B|X)-I(WV;E|X)
 +I(W;V|X)-I(V;B|X)+I(V;E|WX).
\]

Since V is classical, its conditional Holevo information is bounded by its conditional entropy, I(V;E|WX)<=H(V|WX). Therefore the remainder satisfies

\[
\begin{aligned}
I(W;V|X)-I(V;B|X)+I(V;E|WX)
&\le H(V|X)-I(V;B|X)\\
&=H(V|BX)\le H(V)\le\log|V|.
\end{aligned}
\]

This proves the claimed second bound without requiring secrecy of the consumed registers jointly with W.

## Exact entropy identity for the third bound

Reliability gives n(bar R+bar P+bar S)<=I(KW;B L V)+o(n). Generated-secret-only security gives I(W;E|KL)=o(n). Subtract this leakage. Expanding and subtracting the desired information expression gives exactly

\[
\begin{aligned}
&I(KW;BLV)-I(W;E|KL)\\
&\quad-[I(KL WV;B)-I(WV;E|KL)]\\
&=I(KW;LV)-I(LV;B)+I(V;E|WKL).
\end{aligned}
\]

The classical-register bound I(V;E|WKL)<=H(V|WKL) and the chain rule give

\[
\begin{aligned}
I(KW;LV)-I(LV;B)+I(V;E|WKL)
&\le I(KW;L)+H(V|L)-I(LV;B)\\
&\le H(L)+H(V)\\
&\le\log|L|+\log|JS_B|.
\end{aligned}
\]

This proves the third bound with the correct consumed-resource coefficient.

## Continuity and scope

For an unhalved trace-norm error epsilon, the event-error and conditional-entropy continuity bounds yield o(n) for fixed finite gross generation/consumption rates as epsilon tends to zero. This note does not establish arbitrary superlinear catalyst conventions. Leakage continuity can be bounded using only the dimension of the finite classical W register, even if E is infinite dimensional; no dimension bound on E is needed. In the intended finite-energy bosonic application, unconditional B/E entropies are finite and all classical message/resource registers are finite, so the displayed chain identities have no infinity-minus-infinity ambiguity. The ensemble of conditional n-mode input states has finite total average energy; individual positive-probability branches have finite energy because the number of finite registers is finite at each block length.

The lemma includes all pure-loss boundaries and all other channels under its finite classical-resource convention. It does not restore the false literal N=0 region: it proves a distinct, expressly corrected convention under which OTP is permitted. Achievability, energy approximation, sharp bosonic entropy input, full closure, and publication novelty still need separate verification.
