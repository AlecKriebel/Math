# Turn 2: disturbance-compatible quotients and a larger soundness class

**30001199 / OWR-3394-009. Original target unresolved, 2/5 substantive author turns.** This turn uses controlled-invariant output-nulling quotients, not an instantaneous-kernel enlargement.

We retain the exact LTI model, full simulation definition and closed negative-feedback convention of TURN_1.md. Disturbances are unrestricted signals; no magnitude, energy or prescribed feedback-policy bound is imposed.

## 1. Quotient lemma

Consider a component

\[
\dot x=Ax+Bu+Ld,\qquad y=Cx,
\tag{1}
\]

and a linear subspace N satisfying

\[
N\subseteq\ker C,\qquad AN\subseteq N+\operatorname{im}L.
\tag{2}
\]

Choose a linear map K on the state space such that

\[
(A+LK)N\subseteq N.
\tag{3}
\]

Such a K exists: choose a basis of N, select a disturbance correction for each basis vector using (2), extend linearly on N, then extend to the whole state space. Let pi:X→X/N be the quotient projection, and define

\[
\bar A\pi=\pi(A+LK),\quad \bar B=\pi B,
\quad \bar L=\pi L,\quad \bar C\pi=C.
\tag{4}
\]

Equations(2)–(3) ensure the induced maps are well-defined. The quotient component

\[
\dot{\bar x}=\bar A\bar x+\bar B u+\bar L\bar d,
\qquad \bar y=\bar C\bar x
\tag{5}
\]

is fully bisimilar to (1), through the graph relation \(\bar x=\pi x\), with the same interconnection input u and output y.

**Proof.** For a trajectory of (1) set \(\bar d=d-Kx\). Then (4) gives

\[
\pi\dot x=\bar A\pi x+\bar B u+\bar L(d-Kx),\qquad Cx=\bar C\pi x.
\]

Conversely, for a quotient trajectory and any related initial lift x(0), solve the original linear system with \(d=\bar d+Kx\). Its projection solves the same quotient initial-value problem, so \(\pi x=\bar x\) for all time. These linear state-feedback choices preserve locally integrable or piecewise-continuous disturbance admissibility. Both graph projections are full because pi is surjective. This proves both disturbance quantifiers, not merely trace containment. ∎

The state-feedback change is in the freely chosen auxiliary disturbance, not in a fixed external interconnection input. With bounded or restricted disturbances, this argument would require different hypotheses and is not asserted here.

## 2. Feedback composition preserves these equivalences

For any two components satisfying the quotient lemma, the product graph

\[
(\bar x_1,\bar x_2)=(\pi_1x_1,\pi_2x_2)
\]

is a full bisimulation between their original and quotient closed-feedback systems. Indeed y_i=bar y_i, so u1=−y2 and u2=y1 are exactly the same inputs in the two descriptions. The disturbance substitutions in §1 apply componentwise, and both ordered outputs are preserved. Initial lifts exist independently for the two quotient states.

Consequently, replacing any of P1,P2,Q1,Q2 by such a quotient preserves each full-simulation premise and the conclusion **in both directions**. To see this explicitly, compose the full simulation with the forward/reverse full bisimulation relations. Relational composition remains a linear subspace, remains full over the first state space, and composes the matching-disturbance choices. This is the standard transitivity mechanism, not an assumption that behavior inclusion is equivalent to simulation.

## 3. Soundness when one specification's whole output kernel is controlled invariant

**Theorem.** The exact source circular rule is sound if, for at least one i∈{1,2},

\[
A_{Q_i}\ker C_{Q_i}
\subseteq\ker C_{Q_i}+\operatorname{im}L_{Q_i}.
\tag{6}
\]

**Proof.** Apply §1 to that specification with N=ker C_Qi. Its induced observation \(\bar C_{Q_i}\) is injective, because \(\bar C_{Q_i}\pi x=0\) implies x∈N. Transfer the two premises to this quotient using §2. The one-injective-specification proposition of TURN_1.md proves the quotient conclusion. Transfer that conclusion back using §2. This gives a full simulation in the original state spaces. ∎

Condition(6) is checkable by linear algebra. It is weaker than injectivity and includes the case when ker C_Qi is A_Qi-invariant without any disturbance correction. It also holds whenever im(C_Qi L_Qi)=im C_Qi, since the observable part of A_Qi n can then be canceled for every n∈ker C_Qi.

For a concrete nontrivial kernel example, take

\[
A=\begin{pmatrix}0&1\\-2&3\end{pmatrix},
\quad C=\begin{pmatrix}1&0\end{pmatrix},
\quad L=\begin{pmatrix}1\\0\end{pmatrix}.
\]

With N=span((0,1)), choose K=(0,−1); then (A+LK)N⊂N. The quotient observation is a one-dimensional injective map. This example is only an illustration of the sufficient condition, not a new main-rule witness.

## 4. An exact reduction of the remaining general problem

Let N* be the largest subspace satisfying (2). It is obtained by the descending iteration

\[
N_0=\ker C,\qquad
N_{k+1}=\ker C\cap A^{-1}(N_k+\operatorname{im}L).
\tag{7}
\]

The sequence is nested, stabilizes in at most dim X strict dimension drops, and its stable value satisfies(2). Every controlled-invariant subspace contained in ker C lies in every N_k, by induction, so the stable value is largest.

After applying §1 with N=N*, the quotient's largest controlled-invariant output-nulling subspace is zero. For if a nonzero quotient subspace V had that property, its inverse image pi^{-1}(V) would be contained in ker C and controlled invariant for (A+LK,L), hence also for (A,L). It would strictly contain N*, a contradiction.

Applying these quotients to all four components gives an equivalent instance of the original rule with zero maximal output-nulling subspace in every component. This is an exact model reduction, not a proof that the resulting instance satisfies the rule.

One further useful fact in this reduced class is that, in either premise, the two copies of the common specification component must have the **same state**. They receive equal interconnection inputs because the other outputs match. Their difference is a trajectory of that component with free difference disturbance and identically zero output. Its initial state therefore belongs to the maximal output-nulling subspace, which is zero. The same argument applies at each time. To justify the output-nulling inference directly from(7), a zero-output trajectory lies in N0 for all times. If it lies in Nk, its derivative lies in Nk almost everywhere, so Ax lies in Nk+im L almost everywhere, and then everywhere by continuity and closedness. It therefore lies in N_(k+1) for all times. Induction gives its initial state in N*.

This last fact does not establish that the two premises can be joined with full projection or compatible target disturbances. Those circular compatibility conditions are the remaining difficulty.

## 5. Scope and failed shortcut retained

The output-kernel enlargement criticized in TURN_1.md is still invalid when ker C is not controlled invariant. In particular, the double integrator with L=0 has an instantaneous hidden direction that becomes visible; it fails(6). This turn avoids that failure by imposing the exact invariance condition or passing to N*, rather than assuming the entire kernel can be factored out.

The main gap is now concentrated in reduced specification components with N*=0 but ker C≠0, where hidden state becomes observable through later derivatives. No finite search or coordinate change is being substituted for the required full-simulation proof in that class. No counterexample to the main rule has been found.

All known simulation/controlled-invariant methods and the affirmative2010 literature claim are credited in the source record. These partial deductions carry no historical-priority claim. This is substantive author turn2; three turns remain.
