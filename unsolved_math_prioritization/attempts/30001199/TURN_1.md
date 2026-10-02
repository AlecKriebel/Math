# Turn 1: an injective-specification case and a published-proof dependency

**30001199 / OWR-3394-009. Original general LTI target unresolved, 1/5 substantive author turns.** No main-rule counterexample or complete corrected proof is claimed. The later published Theorem4 is credited as an affirmative claim, with the displayed auxiliary lemma's dependency issue preserved separately.

## 1. Exact model

For each label i in {P1,P2,Q1,Q2}, take finite-dimensional real spaces and

\[
\dot x_i=A_ix_i+B_i u_i+L_i d_i,\qquad y_i=C_i x_i.
\]

Here L is the source report's G, renamed to distinguish disturbances from the later paper's separate external input. Disturbances are free. Closed feedback is u1=−y2, u2=y1. The composite output is the ordered pair (y1,y2). A full simulation is a linear relation with full projection onto the source state space, preserving those outputs and admitting matching target disturbances for every source disturbance. The two premises are

\[
P_1\parallel Q_2\preccurlyeq Q_1\parallel Q_2,
\qquad Q_1\parallel P_2\preccurlyeq Q_1\parallel Q_2.
\tag{1}
\]

## 2. A sufficient condition: one injective specification observation

**Proposition.** If (1) holds and C_Q1 is injective, then

\[
P_1\parallel P_2\preccurlyeq Q_1\parallel Q_2.
\tag{2}
\]

The same conclusion holds if C_Q2 is injective. The implementation observation maps and the other specification observation map need not be injective. “Injective” here is an instantaneous state observation property, stronger than dynamical observability; these must not be conflated.

### Proof when C_Q1 is injective

Let R1 and R2 be full simulations for the first and second premises. Fullness of R1 implies im C_P1 is contained in im C_Q1. Thus there is a unique linear map F:X_P1→X_Q1 with

\[
C_{Q_1}F=C_{P_1}.
\tag{3}
\]

In every tuple (p1,q2,q1,q2')∈R1, output matching and injectivity imply q1=F p1. Likewise every (q1,p2,q1',q2)∈R2 satisfies q1'=q1.

Define

\[
R=\{(p_1,p_2,q_1,q_2):q_1=Fp_1,
       (q_1,p_2,q_1,q_2)\in R_2\}.
\tag{4}
\]

This is a linear subspace. It is full: given any (p1,p2), set q1=F p1 and use fullness of R2 on (q1,p2); its target first state must again equal q1. It preserves outputs by (3) and R2's output equality.

It remains to verify the disturbance quantifier and tangency. Fix any (p1,p2,q1,q2)∈R and arbitrary disturbances d_P1,d_P2. Write the actual implementation derivatives as

\[
f_1=A_{P_1}p_1-B_{P_1}C_{P_2}p_2+L_{P_1}d_{P_1},
\qquad
f_2=A_{P_2}p_2+B_{P_2}C_{P_1}p_1+L_{P_2}d_{P_2}.
\tag{5}
\]

Fullness of R1 gives a tuple (p1,q2,q1,q2')∈R1. Its outputs satisfy C_Q2 q2'=C_Q2 q2=C_P2 p2. Apply R1's simulation/tangency condition to d_P1 and, for its source Q2 component, the arbitrary allowed disturbance zero. The resulting target Q1 derivative must equal F f1, because the relation satisfies q1=F p1. Hence there exists a disturbance alpha such that

\[
A_{Q_1}q_1-B_{Q_1}C_{P_2}p_2+L_{Q_1}\alpha=Ff_1.
\tag{6}
\]

Now apply R2's simulation condition at (q1,p2,q1,q2), feeding its source Q1 the disturbance alpha and its source P2 the given d_P2. Its source derivatives are (F f1,f2), by (3),(5),(6). It provides target derivatives (g1,g2) with

\[
(Ff_1,f_2,g_1,g_2)\in R_2.
\tag{7}
\]

Every vector in R2 has equal first and third components, so g1=F f1. Thus (f1,f2,g1,g2)∈R. These target derivatives have exactly the Q1||Q2 dynamics with the matching disturbances delivered by R2. This proves the required tangency for every source disturbance.

For completeness, the finite-dimensional linear tangency criterion is sufficient for a trajectory simulation: the target-disturbance matching equation is a linear surjective map onto its required range, so a linear right inverse on that range selects matching disturbances as linear functions of the related states and source disturbances. The resulting coupled linear ODE preserves R for all time. This applies, for example, to locally integrable disturbances and their absolutely continuous state solutions, or to the usual piecewise-continuous class. The output equality persists. Therefore R is a full simulation, proving (2).

### The other specification role

If C_Q2 is injective, fullness yields the unique F2 with C_Q2 F2=C_P2. Use

\[
R=\{(p_1,p_2,q_1,q_2):q_2=F_2p_2,
       (p_1,q_2,q_1,q_2)\in R_1\}.
\]

Fullness now follows from R1. First use R2 at (q1,p2,q1',q2) to select a source Q2 disturbance making its derivative F2 f2, then use R1 with d_P1 and that selected Q2 disturbance. Injectivity of C_Q2 forces its two Q2 derivatives to agree, and yields tangency of this R. The signs in (5) remain unchanged; no commutativity of negative feedback is assumed. This proves the second case. ∎

## 3. What the source-dependency test establishes

DEPENDENCY_CHECK.md gives a deterministic diagonal-comparison example against the *displayed enlargement* in Lemma1(22) of Kerber–van der Schaft2010. The initial output-kernel vector (0,1) of a double integrator is not in its unobservable subspace. A signed swap puts unequal future outputs into the enlarged relation, so that relation is not a simulation. All external-input and disturbance matrices in the test are zero, and P2=Q2 supplies the second identity premise.

This test does not refute the main circular rule: the rule's conclusion in the test is an identity simulation. Independent source scrutiny is still needed to settle any transcription/notation qualification of the2010 formula. The2010 claim and its authors remain fully credited. Its general conclusion is not treated as verified merely because it is stated in a published theorem.

## 4. Computational evidence and remaining gap

The exact-rational checker verifies the tangency/fullness construction (4) on its recorded finite suite. The universal result is the proof in §2, not a finite inference.

A separately labeled proposal search over the field with1009 elements checked80 reference pairs and158,400 eligible implementation pairs, involving172,880 simulation calls. It found no main-rule witness in that finite sample. These modular tests are not evidence that all real systems satisfy the rule, and no modular-only witness would be accepted as a real counterexample.

The main gap is the case where **both** specification observation maps have nontrivial kernels. An instantaneous output-kernel enlargement is blocked by §3; replacing it by an invariant/unobservable subspace does not automatically preserve the fullness needed by the circular construction. Any general correction must prove both disturbance compatibility and full projection, rather than transfer either to an unsupported fiber-product assertion. A subsequent turn will pursue a genuinely different hidden-state mechanism.

No full source-target resolution, historical novelty, human peer review, or formal verification is claimed. All work above is retained as substantive author turn1; four turns remain.
