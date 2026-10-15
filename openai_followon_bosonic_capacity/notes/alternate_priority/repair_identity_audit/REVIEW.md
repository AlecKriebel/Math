# Independent audit of the generated-secret-only converse

Timestamp: 2026-10-06 21:26 America/Los_Angeles.

Reviewed file: `../DEGRADABLE_CONVERSE_REPAIR.md`.
Latest completely read version SHA-256:
`db79ea56d9203f8ada365ba51c42322500bd94db7b41011750c939cbfee74361`.
Earlier versions inspected:
`184efa7e06a96e4cb03bd9bf7dae170987d6fef1a7f8da28a614e3987ebedd39`
(degradability proof) and
`0877ee2d736c5f0d311ea4e7b62366b83e6f61c89763e402721b56094d4dcb67`
(classical-register proof before channel-marginal clarification).

## Verdict and reviewed scope

The three converse inequalities in the latest note are correct for the stated
parallel-channel protocol, finite classical resources, initially independent
uniform public/private messages, generated-secret-only security against the
entire public transcript and Eve, and fixed finite gross rates. The general
classical-register repair is valid without degradability. No sign, chain-rule,
quantum-output, or consumed-rate error was found.

This is a lemma audit, not a complete-package review or certification of an
exact bosonic capacity theorem. I did not audit the entropy breakthrough,
Gaussian-achievability construction, arbitrary infinite-dimensional coding
approximation, closure, bibliographic priority exhaustively, or publication
files. The original stronger consumed-register security condition remains a
different model. This lemma does not show equality of the two models.

## Independent finite-block derivation

Use base-two logarithms, with any other base allowed by consistent conversion.
Let `d_A` denote the finite alphabet cardinality of a classical register A.
Let the total correctness error probability for the generated K, M, T_A
registers be at most delta, and suppose

\[
\tfrac12\|\omega^{WEX}-\pi^W\otimes\sigma^{EX}\|_1\le\delta,
\qquad W=MT_A,\quad X=KL,\quad V=JS_B.
\]

Here E is the physical complementary channel output before decoding. Security
against a larger final Eve system implies this condition by partial trace,
provided K,L are part of the public information. Set, for delta at most 1/2,

\[
 f_\delta(d)=h_2(\delta)+\delta\log_2 d,
 \qquad
 c_\delta(d)=2\delta\log_2d+(1+\delta)
 h_2\!\left(\frac{\delta}{1+\delta}\right).
\]

Fano's inequality and data processing give

\[
H(KM\mid BLV)\le f_\delta(d_{KM}),\quad
H(W\mid BVX)\le f_\delta(d_W),\quad
H(KW\mid BLV)\le f_\delta(d_{KW}).
\]

The finite-dimensional-system conditional-entropy continuity bound gives
`H(W|EX) >= log_2 d_W - c_delta(d_W)`. The conditioning system can be infinite
dimensional; the bound uses only d_W. See Winter, Lemma 2 and its preceding
discussion in [arXiv:1507.07775](https://arxiv.org/html/1507.07775).

For the first bound, A=KM is exactly uniform and remains independent of S_B.
Thus

\[
\begin{aligned}
\log_2d_A
&\le I(A;BLJS_B)+f_\delta(d_A)\\
&=I(A;B\mid LJS_B)+I(A;LJ\mid S_B)+f_\delta(d_A)\\
&\le I(ALJS_B;B)+\log_2d_{LJ}+f_\delta(d_A)\\
&\le I(XWV;B)+\log_2d_{LJ}+f_\delta(d_A).
\end{aligned}
\]

The third line uses positivity of I(LJS_B;B), and the last line adds T_A to
the label. Both steps are valid for quantum B.

For the second bound, directly cancel H(W|X):

\[
\begin{aligned}
F&=I(W;BV\mid X)-I(W;E\mid X)\\
 &=H(W\mid EX)-H(W\mid BVX)\\
 &\ge\log_2d_W-c_\delta(d_W)-f_\delta(d_W).
\end{aligned}
\]

The note's exact chain identity decomposes F into the desired private
information plus the residual

\[
I(W;V\mid X)-I(V;B\mid X)+I(V;E\mid WX).
\]

For classical V and classical WX,
`I(V;E|WX) <= H(V|WX)`. The residual is consequently at most
`H(V|X)-I(V;B|X)=H(V|BX) <= log_2 d_V`. Hence

\[
\log_2d_W\le I(WV;B\mid X)-I(WV;E\mid X)
 +\log_2d_V+c_\delta(d_W)+f_\delta(d_W).
\]

For the third bound, an independent expansion yields

\[
\begin{aligned}
G&=I(KW;BLV)-I(W;E\mid KL)\\
 &=H(K)+I(W;L\mid K)+H(W\mid EKL)-H(KW\mid BLV)\\
 &\ge\log_2d_K+\log_2d_W-c_\delta(d_W)-f_\delta(d_{KW}).
\end{aligned}
\]

The note's exact chain identity writes G minus
`I(KLWV;B)-I(WV;E|KL)` as

\[
I(KW;LV)-I(LV;B)+I(V;E\mid WKL).
\]

Its last term is at most H(V|WKL), so this residual is at most
`I(KW;L)+H(V|L)-I(LV;B) <= log_2 d_L + log_2 d_V`.
This proves the third claimed bound, with remainder
`c_delta(d_W)+f_delta(d_KW)`.

All three inequalities concern the same X,Y=WV ensemble, so they can be
subtracted simultaneously against the three consumed-rate sums. With all
generated alphabet logarithms O(n) and delta tending to zero, the displayed
remainders are o(n). Fixed finite net rates alone do not imply this if gross
rates are permitted to grow superlinearly. The latest note explicitly excludes
that convention.

## Falsification checks and necessary boundaries

1. **Quantum versus classical conditioning.** The only entropy upper bounds
   involving a quantum conditioning system use a classical conditioned
   register V or W. Thus `0 <= H(V|BX) <= H(V)` is valid. These bounds would
   fail for arbitrary quantum consumed registers. The proof does not assert
   that the actual joint BE state is produced by degrading B.

2. **Arbitrary entanglement across uses.** Conditioning on finite classical
   labels leaves arbitrary mixed n-use inputs. Applying the channel to their
   conditional states produces the required ensemble. No input factorization
   or entropy additivity is used here.

3. **Finite-energy bosonic inputs.** Finite average input photon number implies
   finite unconditional B/E entropy for the pure-loss channel. Every
   positive-probability branch of a finite classical ensemble has finite
   energy. This suffices for the note's ordinary entropy expansions. The
   information inequalities also admit conditional-entropy formulations using
   only finite classical dimensions; no bounded dimension of B/E is required.

4. **N=0 and the resource rays.** The repaired security condition admits the
   one-time pad: independent uniform M,S, ciphertext L=M xor S, and constant
   physical-channel outputs have W=M independent of L. Joint MS leaks to L,
   so the original condition is not established. Secret-key distribution
   W=J is also admissible after J has transmitted the newly generated random
   key. The second repaired bound is tight in these examples.

5. **Common randomness is a distinct task.** Initial independence of K,M and
   S_B is essential to the first bound. A constant channel, no L/J, and
   K=S_B produce one public common-randomness bit per consumed key bit.
   This violates the first bound if one relabels arbitrary common-randomness
   generation as public message transmission. The repaired lemma therefore
   applies to the stated initially independent message model, not every
   possible common-randomness generation protocol. The original paper's
   Section 5 language about common randomness must not be repeated without
   this restriction.

6. **Endpoints.** No channel property remains in this lemma, so eta=1/2,
   eta=1, and vacuum inputs introduce no new converse obstruction. The sharp
   entropy optimization and achievable Gaussian boundary are separate tasks.

## Primary-source checks and attribution limits

I read [Wilde–Hsieh arXiv:1005.3818v3](https://arxiv.org/html/1005.3818v3),
Sections 2–5, particularly its initial state, encoding/decoding registers,
stronger security condition before Eq. (14), and all three converse chains.
The replacement above does not invoke that stronger condition.

I also inspected the operational security criterion and converse in
[Hsieh–Wilde, Phys. Rev. A 80, 022306 (2009)](https://www.markwilde.com/publications/PhysRevA_80_022306.pdf),
Eq. (4) and Sections IV–V. That paper's Eq. (4) likewise constrains Eve jointly
with the consumed key, even at fixed public/private messages. It is therefore
not an automatic generated-secret-only achievability certificate. A separate
direct proof is appropriate.

Targeted primary-literature searches did not identify the exact elementary
repair as an explicitly named result. This limited search establishes no
novelty or historical priority; all capacity formulas and resource machinery
remain attributed to their original sources. No external individual was
contacted.

## Checkable algebra certificate

`symbolic_checks.py` expands mutual and conditional information into exact
integer coefficients of formal entropies. Five independent residuals vanish:
the second and third chain identities, both classical-entropy cancellations,
and the third reliability/secrecy expression. Run with Python 3.14.6:

```
python3 symbolic_checks.py
```

This is an exact algebra check, not a formal verification of the entropy
inequalities or the capacity theorem. No floating-point computation is used.
