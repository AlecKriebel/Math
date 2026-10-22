# Turn 2: scalar equilibrium reduction for the distinct Lck core

Started 2026-10-01 06:15 UTC. Unreviewed mathematical work for the still-unresolved bundled target; not the receptor/phosphatase recurrence of PR145.

In Brechmann's Lck-only N-step network let d_i>0 be dissociation of C_i (d_0=k2), u_i,v_i,w_i>0 the association, dissociation and catalysis rates in C_i+E ⇄ B_i → C_(i+1)+E. Set a_i=u_i/(v_i+w_i), q_i=w_i*a_i. At any steady state, B_i=a_i*e*C_i, where e is free enzyme. The unbound receptor and ligand are r,m. The remaining balances are

q_(i-1)*e*C_(i-1)=(d_i+q_i*e)*C_i (1≤i<N),
q_(N-1)*e*C_(N-1)=d_N*C_N,
k1*r*m=(d_0+q_0*e)*C_0.

For p_0(e)=1, define p_i(e)=prod_(j=0)^(i-1)(q_j*e)/prod_(j=1)^i(d_j+q_j*e) for 1≤i<N and p_N(e)=prod_(j=0)^(N-1)(q_j*e)/(d_N*prod_(j=1)^(N-1)(d_j+q_j*e)). Then C_i=C_0*p_i(e).

Let G(e)=sum_(i=0)^(N-1) a_i*p_i(e), H(e)=sum_(i=0)^N p_i(e)+e*G(e). Enzyme conservation gives C_0=(Etot-e)/(e*G(e)); bound receptor total is W(e)=(Etot-e)*H(e)/(e*G(e)). Receptor and ligand conservation give r=Rtot-W(e), m=Mtot-W(e).

Thus the exact positive steady-state problem is the scalar equation

k1*(Rtot-W(e))*(Mtot-W(e))=(d_0+q_0*e)*(Etot-e)/(e*G(e))

on the explicitly filtered physical set 0<e<Etot and W(e)<min(Rtot,Mtot). Every denominator is positive there. These conditions reconstruct all species and all three fixed totals positively. The receptor source balance and successive phosphorylation balances imply every original species equation; summing gives both free-pool equations and enzyme conservation gives its equation. Conversely every positive equilibrium has this form.

A finite polynomial reduction follows after multiplying by Q(e)=prod_(j=1)^(N-1)(d_j+q_j*e). Write P_i=Q*p_i, g=Q*G and h=Q*H. The degree of P_i is at most N-1 for i<N, P_N has degree N, g has degree at most N-1, h degree N. Up to positive constant denominators from d_N, the equation is

k1*[Rtot*e*g-(Etot-e)*h]*[Mtot*e*g-(Etot-e)*h]
 -(d_0+q_0*e)*(Etot-e)*Q*e*g = 0.

Its degree is at most 2N+2. All positive polynomial roots outside the physical filter must be rejected. This is a necessary-and-sufficient reconstruction, not a claim that the raw number of positive polynomial roots counts physical equilibria. It supplies an exact route toward branch and stability investigations; no all-parameter dynamical classification follows from it.

## Exact controls and completion

The separate locally authored checker verifies 197 exact assertions through N=8, including every receptor-chain balance, enzyme conservation, physical positivity and the polynomial degree bounds. In the all-unit-rate, all-unit-total N=1 control, clearing denominators yields 4e^4+5e^3-6e^2-6e+4. It has two positive roots, one in (0.56,0.57) and one in (0.89,0.90). The bound-receptor total W=2(1-e^2)/e is above one throughout the first interval and below one throughout the second. Only the second root is physical. The initial checker mistakenly demanded strict positivity of every polynomial coefficient, including structural zero coefficients; it was corrected to nonnegativity. No mathematical claim depended on that test error.

Turn 2 completed 06:17 UTC. The reduction is exact but does not determine the complete higher-N dynamics.
