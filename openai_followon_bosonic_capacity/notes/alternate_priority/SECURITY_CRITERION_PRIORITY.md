# Consumed-resource secrecy: exact counterexample and scoped priority search

Audit checkpoint: 2026-10-06 21:20 America/Los_Angeles. This note independently verifies the operational inconsistency identified in the lead task. It does not establish that its observation is historically new.

## Primary definitions actually inspected

[Wilde–Hsieh, arXiv:1005.3818v3](https://arxiv.org/html/1005.3818v3), submitted 2010-05-20, current version 2012-06-25, Section 5 immediately before Eq. (14), requires the predecoded state to approach

\[
\pi^{M T_A J S_B}\otimes\sigma^{K L E^n}
\]

in the unhalved trace norm. M is the generated private message, T_A generated secret key, J a register sent through a consumed private classical channel, S_B Bob's share of the consumed secret key, and KL public data. Thus the requirement imposes joint uniform independence of the generated and consumed private registers from all public data and Eve. The author-hosted [journal PDF](https://markwilde.com/publications/10.1007_s11128-011-0317-z.pdf), printed p. 1475, contains the same condition; this is not solely a converted-HTML error. Eq. (14)'s small mutual information for that whole joint register is used in the P+S and R+P+S converse steps.

[Hsieh–Wilde, arXiv:0903.3920v1](https://arxiv.org/html/0903.3920v1), first public 2009-03-23 (PRA 80, 022306, published 2009-08-05), already states in Eq. (4) a stronger joint condition on Eve and S_B for every fixed private message m. Section III explicitly uses one-time-pad resource conversion. Ordinary OTP fails the joint criterion conditional on m, because its public ciphertext then determines the consumed key. Its cited separate marginal mutual-information conditions (11)–(12) do not capture this joint leakage.

## Exact OTP certificate

Let d=2^n, with M and S independent uniform n-bit strings. Publish L=M xor S and let Bob recover M=L xor S. Eve sees only L; channel input can be vacuum, so this uses no energy. Both I(M;L)=0 and I(S;L)=0, but

\[
I(MS;L)=H(L)=n\quad\text{bits}.
\]

For any comparison probability distribution q on L,

\[
\lVert P_{MSL}-U_M U_S q_L\rVert_1=2(1-1/d).
\]

Proof: the event A={l=m xor s} has probability one under P and 1/d under the comparison distribution. On A, P(m,s,l)=1/d^2 and the comparison is q(l)/d^2, so the signed difference is nonnegative. Outside A it is nonpositive. The two masses are both 1-1/d, proving the exact norm. Therefore the literal criterion cannot hold with vanishing error for the unit resource ray (R,P,S)=(-1,1,-1), although that ray is explicitly used by the advertised private dynamic achievability argument.

Forwarding a private message by J=M similarly violates the product requirement on MJ. Generating new key by setting T_A=J violates the product requirement on T_A J. These observations identify separate conversion conflicts; they do not require quantum entropy claims.

## N=0 disproves the literal full private region

The mean photon number is nonnegative. With an average budget N=0, the averaged input state is supported on the one-dimensional n-mode vacuum subspace. It is therefore vacuum and product with every reference, so Bob's quantum output is fixed vacuum for every transmissivity. His useful predecoded input consists only of L,J,S_B.

Suppose both the literal security condition and the final correctness condition hold with unhalved trace-norm error at most epsilon. Tracing the security comparison to M,L,J,S_B yields a state in which M is uniform and independent of Bob's whole useful input. Any decoder has success probability at most 1/d on this comparison state. Trace-norm contraction and the variational bound for an event give actual success at most 1/d+epsilon/2. Final correctness gives success at least 1-epsilon/2. Hence

\[
\epsilon\geq1-1/d.
\]

For d growing exponentially in n, no vanishing-error positive generated private rate is possible in the literal model, however many consumed public/private/key resources are supplied. The purported N=0 union has all entropy terms zero and includes (-1,1,-1), because R+P=0, P+S=0, and R+P+S=-1<=0. Thus the literal advertised full private region is false at a mandatory boundary. This is an impossibility certificate for all such protocols, not merely a failed implementation of OTP.

## Correction search and what it supports

The complete seven-page primary [2012 erratum](https://link.springer.com/content/pdf/10.1007/s11128-012-0451-2.pdf), DOI 10.1007/s11128-012-0451-2, published online 2012-08-07, was read. It corrects convex-optimization claims about dynamic capacity formulas, explains separate concavity/convexity in probabilities/signaling states, and gives revised optimization/complexity claims. It does not amend the secrecy condition or consumed-key conversion.

Queries on 2026-10-06 included the exact title plus secrecy/erratum/consumed key, arXiv identifier plus security/secret key, and private dynamic secrecy/correction variants. The author's primary journal list and the earlier 2009 source were inspected. No separate primary correction addressing this exact criterion was found in the searched material. A failed search does not prove novelty. Other current formulations may silently use generated-secret-only security; those require exact statement and proof inspection before adopting them as a repaired coding theorem.

The conventional repair would require only generated private message/key to be jointly uniform and independent of Eve's final quantum system and complete public transcript, while consumed private resources need not remain secret or independent of the output. This is a substantive change of the literal operational model. Merely deleting J,S_B from the displayed condition does not validate the published catalytic converse, whose subtraction explicitly uses leakage of the larger joint variable. A valid proof must bound the necessary extra terms under the repaired convention or use a separately verified coding theorem. The subsequent DEGRADABLE_CONVERSE_REPAIR.md supplies such a bound for physical channels using classical-register conditional entropy and an exact chain identity; it is an explicit model correction and requires independent review. No complete bosonic theorem is certified by this note alone.

Independent route mathematical-resolution estimate: 15%; publication-package estimate: 0%. Exact obstruction and counterexample verified; unconditional upstream entropy input and repaired private converse not verified here.
