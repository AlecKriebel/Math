# Turn 3: a nilpotent coupling proof of the full circular LTI rule

**30001199 / OWR-3394-009. Complete candidate after 3/5 substantive author turns, pending independent review.** The affirmative theorem was already stated by Kerber–van der Schaft (2010), Theorem 4. This packet proposes a complete alternative argument that does not use its displayed instantaneous-kernel enlargement. It makes no historical-priority claim. The auxiliary-lemma diagnostic is not a counterexample to this theorem.

## 1. Exact theorem

All component spaces are finite-dimensional real vector spaces. Components have constant matrices and unrestricted disturbance signals:

\[
\Sigma_i:\quad \dot x_i=A_i x_i+B_i u_i+L_i d_i,
\qquad y_i=C_i x_i.
\tag{1}
\]

Closed feedback is \(u_1=-y_2,\ u_2=y_1\); the observed composite output is the ordered pair \((y_1,y_2)\). Disturbances may, for example, be locally integrable, with absolutely continuous state trajectories. A full simulation is a linear relation with full projection onto the implementation state space, preserving output and matching every implementation disturbance by some specification disturbance while remaining in that relation for all future times.

**Theorem.** In this exact source model,

\[
P_1\parallel Q_2\preccurlyeq Q_1\parallel Q_2,
\quad Q_1\parallel P_2\preccurlyeq Q_1\parallel Q_2
\quad\Longrightarrow\quad
P_1\parallel P_2\preccurlyeq Q_1\parallel Q_2.
\tag{2}
\]

There is no injectivity, observability, controllability, stability or disturbance-rank assumption. Disturbance constraints or nonlinear/discrete models are outside this theorem. Below, unadorned subscripts 1, 2 refer to Q1,Q2; implementation matrices retain P1,P2 subscripts.

## 2. Reduction by genuine output-nulling subspaces

For a component (A,B,L,C), let N* be the largest subspace satisfying

\[
N^*\subseteq\ker C,\qquad AN^*\subseteq N^*+\operatorname{im}L.
\tag{3}
\]

It is the stabilized value of the descending iteration

\[
N_0=\ker C,\qquad N_{k+1}=\ker C\cap A^{-1}(N_k+\operatorname{im}L).
\]

Choose a linear K0 with \((A+LK_0)N^*\subseteq N^*\), and form the quotient pi:X→X/N* with matrices

\[
\bar A\pi=\pi(A+LK_0),\quad\bar B=\pi B,
\quad\bar L=\pi L,\quad\bar C\pi=C.
\tag{4}
\]

The graph \(\bar x=\pi x\) is a full bisimulation: use \(\bar d=d-K_0x\) in the forward direction and \(d=\bar d+K_0x\) in the reverse direction. The interconnection input u is not changed. These linear disturbance selections are admissible for the signal class in §1.

This quotient has zero maximal output-nulling subspace. A nonzero such quotient subspace would lift to a larger subspace satisfying (3), contradicting maximality. Because both directions preserve the interconnection output, replacing Q1 or Q2 by this quotient preserves each premise and the desired conclusion under closed feedback, by the product bisimulation and transitivity. The full details, including zero-dimensional quotients, are proved in TURN_2.md §§1–4.

We may therefore work with specifications satisfying

\[
N^*_1=N^*_2=\{0\}.
\tag{5}
\]

No quotient of the implementation components is required.

A fact used below is that any zero-output trajectory of \(\dot x=Ax+Ld\) starts in N*. Indeed it lies in N0 for all times. If it lies in Nk, its derivative lies in Nk almost everywhere; thus Ax lies in Nk+im L almost everywhere and, by continuity and closedness, everywhere. Induction gives membership in every Nk. Consequently, under (5), a zero-output trajectory has identically zero state.

## 3. The two premise relations become graphs

Let R1 and R2 be any full simulations for the premises after reduction.

First, in a tuple \((p_1,q_2,q_1,q_2')\in R_1\), the two copies of Q2 have equal outputs. Along matching trajectories they also have equal inputs, because the P1 and Q1 outputs agree. Their state difference is therefore a zero-output trajectory of Q2 driven by the difference of its disturbances. By(5), q2'=q2. Similarly every tuple in R2 has its two Q1 states equal.

Next the remaining target state in R1 is unique for each (p1,q2). If two choices differ by delta q1, linearity of R1 puts \((0,0,\delta q_1,0)\) in R1. Apply simulation to the identically zero source trajectory with zero disturbances. The matching target trajectory has both outputs zero. Its Q1 input is zero, so(5) forces delta q1=0. The same reasoning gives uniqueness of the target Q2 state in R2.

Fullness and linearity now yield linear maps F,E,H,J with

\[
R_1=\{(p_1,q_2,Fp_1+Eq_2,q_2)\},
\qquad
R_2=\{(q_1,p_2,q_1,Hq_1+Jp_2)\}.
\tag{6}
\]

Their output identities are

\[
C_1F=C_{P_1},\quad C_1E=0,
\qquad C_2H=0,\quad C_2J=C_{P_2}.
\tag{7}
\]

## 4. Algebra forced by the disturbance quantifiers

Put \(V_i=\operatorname{im}L_i\). Varying only the source context disturbance at the zero state in each premise gives

\[
EV_2\subseteq V_1,\qquad HV_1\subseteq V_2.
\tag{8}
\]

To spell out the first relation: in R1, varying the source Q2 disturbance yields derivative L2 d2 in q2; differentiating q1=F p1+E q2 forces the target Q1 disturbance image to equal E L2 d2. The second relation follows identically from R2.

Varying the source state q2 in R1 with p1=0 and zero source disturbances gives

\[
\operatorname{im}\big(EA_2-A_1E+(B_1-FB_{P_1})C_2\big)\subseteq V_1.
\tag{9}
\]

Varying q1 in R2 with p2=0 similarly gives

\[
\operatorname{im}\big(HA_1-A_2H+(JB_{P_2}-B_2)C_1\big)\subseteq V_2.
\tag{10}
\]

These identities are just differentiated graph constraints, with the minus sign of the first feedback input retained. They do not require selecting unique target disturbances, only their images under Li.

Let

\[
K=EH:X_{Q_1}\to X_{Q_1}.
\]

Equations (7)–(10) imply

\[
C_1K=0,\qquad KV_1\subseteq V_1,
\qquad \operatorname{im}\big(KA_1-A_1K-D C_1\big)\subseteq V_1
\tag{11}
\]

for \(D=E(B_2-JB_{P_2})\). For the last identity expand

\[
KA_1-A_1K=E(HA_1-A_2H)+(EA_2-A_1E)H.
\]

The term involving C2 H vanishes; E maps the error image in V2 into V1 by (8), and the other error image already lies in V1.

## 5. Nilpotence removes the circular obstruction

We use an elementary finite-dimensional lemma.

**Lemma.** Suppose A,K,C and a subspace V satisfy CK=0, KV⊂V, and
\(\operatorname{im}([K,A]-DC)\subseteq V\) for some D. Let m≥1 be such that
\(\operatorname{im}K^m=\operatorname{im}K^{m+1}\). Then

\[
M:=\operatorname{im}K^m\subseteq\ker C,
\qquad AM\subseteq M+V.
\tag{12}
\]

**Proof.** The first inclusion follows from CK=0. For y∈M, stabilization gives y=K^m x with x∈im K, so Cx=0. The commutator identity

\[
[K^m,A]=\sum_{j=0}^{m-1}K^j[K,A]K^{m-1-j}
\]

shows \([K^m,A]x\in V\). Terms coming from the error image stay in V because KV⊂V. A DC term vanishes when its right-hand power of K is positive; the remaining term vanishes because Cx=0. Thus
\(Ay=K^mAx-[K^m,A]x\in M+V\). ∎

Apply the lemma to (11), with V1=im L1. Since M is an output-nulling controlled-invariant subspace and N1*=0, M=0. Therefore K is nilpotent. One can take \(m=\max\{1,\dim X_{Q_1}\}\), because the descending images of a linear endomorphism have stabilized by then. Hence

\[
S=(I-K)^{-1}=I+K+\cdots+K^{m-1}
\tag{13}
\]

exists and maps V1 into V1. This is a finite algebraic inverse; no convergence, norm contraction or stability assumption is used.

## 6. Full initial-state relation

For every implementation state pair (p1,p2), define

\[
q_1=S(Fp_1+EJp_2),\qquad q_2=Hq_1+Jp_2.
\tag{14}
\]

These are the unique simultaneous solutions of

\[
q_1=Fp_1+Eq_2,\qquad q_2=Hq_1+Jp_2.
\tag{15}
\]

Their graph R is a linear relation with full projection onto all implementation states. Both equations place the relevant tuples in the premise relations (6), and(7) gives
\(C_1q_1=C_{P_1}p_1\), \(C_2q_2=C_{P_2}p_2\).

The initial target state(14) depends only on the initial implementation state, not on any future or current disturbance value.

## 7. Compatible disturbances and trajectory simulation

Fix a related state and arbitrary implementation disturbances. Write

\[
f_1=A_{P_1}p_1-B_{P_1}C_{P_2}p_2+L_{P_1}d_{P_1},
\quad
f_2=A_{P_2}p_2+B_{P_2}C_{P_1}p_1+L_{P_2}d_{P_2},
\]

and the zero-disturbance target derivatives

\[
a_1=A_1q_1-B_1C_2q_2,\qquad a_2=A_2q_2+B_2C_1q_1.
\]

Define

\[
r_1=Ff_1+Ea_2-a_1,\qquad r_2=Ha_1+Jf_2-a_2.
\tag{16}
\]

Then r1∈V1: apply R1's simulation condition at its tuple in (15), with the specified d_P1 and source Q2 disturbance zero. Its Q2 derivative is a2, because C_P1 p1=C1 q1; differentiating the graph forces the Q1 matching disturbance image to be r1. Similarly R2 with source Q1 disturbance zero and given d_P2 shows r2∈V2.

Choose disturbance images

\[
v_1=S(r_1+Er_2)\in V_1,\qquad v_2=r_2+Hv_1\in V_2.
\tag{17}
\]

Membership follows from (8), (13). These solve

\[
v_1-Ev_2=r_1,\qquad v_2-Hv_1=r_2.
\tag{18}
\]

Choose actual target disturbances with Li d_Qi=vi, using a fixed linear right inverse of Li on Vi. The target derivatives gi=ai+vi satisfy

\[
g_1=Ff_1+Eg_2,\qquad g_2=Hg_1+Jf_2.
\tag{19}
\]

Thus the derivative tuple remains in R. More explicitly, for an arbitrary implementation trajectory p(t), define q(t) by (14). Its derivatives solve the differentiated equations (15). Equation(19) and uniqueness from I−EH invertible show that these derivatives are exactly ai+vi. Formula(17) gives admissible target disturbances depending linearly on p(t) and the current implementation disturbances. Outputs agree for all time, and the graph relation persists. This is a full simulation, including the initial-state and universal disturbance quantifiers.

Finally transfer back from the reduced specifications using the full bisimulations in §2. An explicit original-state relation is \(\pi_i x_{Q_i}=q_i(p_1,p_2)\). Any related initial lift is allowed; the disturbance feedback from (4) maintains the projected trajectories and outputs. This proves (2) in the original state spaces. ∎

## 8. Credit, boundary, and audit requirements

The theorem's conclusion is already the affirmative claim of Kerber–van der Schaft (2010), Theorem 4; this is not presented as discovery of a previously unstated theorem. Controlled-invariant simulation quotients are standard geometric control tools, and TURN_2.md gives the needed argument explicitly. The distinguishing mechanism here is the nilpotent product EH forced by zero output-nulling subspaces, replacing the displayed instantaneous-kernel enlargement under audit. Historical novelty of the proof mechanism is unestablished.

The source is specifically LTI closed feedback with free disturbances. This proof does not establish circular rules for arbitrary nonlinear systems, transition systems, algebraically constrained parallel composition, bounded disturbances, or different assume-guarantee semantics. The two premise simulations must be full; nonfull relations do not suffice.

The exact checks supplement this written universal proof. A final independent audit must verify the output-nulling quotient, graph uniqueness, commutator signs, stable-image lemma, full initial-state construction, and simultaneous disturbance images. Final disposition remains pending that audit; count 3/5.
