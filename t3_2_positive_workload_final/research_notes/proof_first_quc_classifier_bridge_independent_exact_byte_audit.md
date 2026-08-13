# Independent exact-byte audit of the Q/U/C classifier bridge

**Audit date:** 2026-08-12 PDT.  
**Frozen target:** proof_first_quc_classifier_bridge_and_raw_trichotomy.md  
**Target SHA-256:** 014a317602b60c765dc9a9eb98f0921ba3fd8f779221e271e0dd7f53e245f54c.

The target has 250 lines and 9,259 bytes. It pins the independently passed
both-available current-target theorem at SHA-256
157e94cd035dec9a41947129dfcbbab0ebc6e72c01abde6bcf6626052954f1ed.

## 1. Verdict

**STRICT PASS** at the target's stated scope. The ordered classifier is
reproduced literally; Q, U, C, and S are disjoint and exhaustive; every Q-,
U-, or C-classified linkage satisfies the marked available-target path
hypothesis; and the raw AA/mixed/SS incidence partition is exact.

The proof is symbolic. A clean-room finite replay was used only to audit the
classifier transcription and displayed counts. No orientation, reaction
history, population state, or rate vector was searched to infer a stochastic
estimate.

## 2. Ordered classifier: pass

Let \(T\) be the top block of a nontrivial support under
\(h=(h_A,h_B,0)\), with \(h_A,h_B>0\). The target applies the inherited
tests in their literal order:

1. flat \(T=L\) gives S;
2. an active-quadratic top gives Q;
3. the one-active-particle flat identity gives S;
4. a unary top gives U;
5. a top and lower \(C\)-containing pair gives C;
6. the remainder gives S.

Each test acts only after the preceding tests fail, so the four outputs are
disjoint and exhaustive. This is precisely the clean-room classifier and
does not depend on an orientation.

## 3. Q/U/C terminal construction: pass

For Q, choose an active-quadratic \(q\in T\). Binaryity forces \(q_C=0\).
Because Q is reached only after the flat test fails,
\(L\setminus T\neq\varnothing\); any \(c\in L\setminus T\) satisfies

\[
                         q_C=0\le c_C,
 \qquad h\cdot q>h\cdot c.                         \tag{3.1}
\]

For U, a unary top cannot equal \(C\). If it did, the top weight would be
zero; nonnegative weights would then force every linkage complex to have
weight zero and hence \(T=L\), contradicting the failed flat test. Thus
\(q\in\{A,B\}\), so (3.1) again holds for any lower \(c\).

For C, both chosen complexes contain \(C\). This test follows Q, so a top
\(C\)-containing \(q\) cannot have two active particles. The top is nonflat
and has positive weight, hence binaryity gives \(q\in\{A+C,B+C\}\) and

\[
                   q_C=1\le c_C\in\{1,2\},
 \qquad h\cdot q>h\cdot c.                         \tag{3.2}
\]

Thus every available type has a faster \(q\) and lower terminal \(c\) with
\(q_C\le c_C\). No probabilistic conclusion is inferred at this step.

## 4. Actual-target path and terminal rarity: pass

At a marked start \((x_n,t)\), the actual target satisfies \(x_n\ge t\), so
\(t\) is physically enabled. Strong connectivity gives a simple path from
\(t\) to \(c\). Every subsequent designated source is the preceding actual
target. On path success the population telescopes exactly to

\[
                            z_n=x_n-t+c\ge c.          \tag{4.1}
\]

If the bounded phase, source support, active set, shell, or source-order cell
changes first, the causing physical reaction is a structural exit. On the
nonexit branch, bounded displacement preserves the strict source comparison.
In Q and U, \(q_C=0\); in C, (3.2)--(4.1) enable \(q\). Therefore

\[
 p_c(z_n)
 \le {\lambda_c(z_n)\over\lambda_q(z_n)}
 ={K_c(z_n)_c\over K_q(z_n)_q}\longrightarrow0.      \tag{4.2}
\]

This proves the exact available-target hypothesis from every actual target,
for every strong orientation and positive fixed rate vector. Crucially, it
does not condition on or wait for a future C-type activation.

## 5. Raw trichotomy and arithmetic: pass

Applying the two-valued split \({\rm A}=\{{\rm Q},{\rm U},{\rm C}\}\)
versus S independently to two disjoint linkages yields exactly AA, AS, SA,
or SS. The target correctly passes AA to the independently audited
both-available theorem, mixed AS/SA to the pair-specific
shielded/available pipeline, and SS to the invariant/deficiency/service
atlas. It makes no recurrence inference for mixed or SS charts.

The ordered assignment count is independently

\[
 3^{10}-2(2^{10}+10\,2^9)+(1+10+10+90)=46{,}872.     \tag{5.1}
\]

The four workload representatives give 187,488 incidences. A clean-room
replay of the ordered mathematical classifier returned

\[
\begin{array}{c|r}
AA&163{,}612\\
AS&11{,}715\\
SA&11{,}715\\
SS&446,
\end{array}
\qquad\text{sum }187{,}488,                           \tag{5.2}
\]

and found zero Q/U/C incidences lacking a pair \(q,c\) satisfying the
symbolic inequalities of Section 3. Equation (5.2) is regression evidence
for the finite partition only; Sections 3--4 prove the bridge.

## 6. Scope discipline

The target does not claim deletion or recurrence monotonicity, does not use
support inclusion, and does not extend the both-available theorem to mixed
charts. Its only stochastic handoff is the literal available-target
hypothesis already audited at the exact pinned bytes.

**Final disposition: STRICT PASS for the classifier bridge theorem and the
raw AA/mixed/SS trichotomy at SHA-256
014a317602b60c765dc9a9eb98f0921ba3fd8f779221e271e0dd7f53e245f54c.**
