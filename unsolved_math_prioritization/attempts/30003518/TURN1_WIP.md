# Turn 1: residual global-convergence route (unreviewed)

Source-model audit is still in progress. The following analysis concerns Brechmann (2024), equation (5.5), the one-phosphorylation Lck core. It does not claim to settle every asymptotic question in the imported bundle.

Write x=C0+B0+C1, b=B0, c=C1 and let positive conserved totals be Rtot,Mtot,E. Then C0=x-b-c and free enzyme is E-b. For g(x)=k1(Rtot-x)(Mtot-x), the reduced equations are

x'=g(x)-k2*x+k2*b+(k2-k6)*c,
b'=k3*(x-b-c)*(E-b)-(k4+k5)*b,
c'=k5*b-k6*c.

Set A=k1*(Rtot+Mtot-2*x)+k2, p=k3*(E-b), q=k3*(x-b-c)+k4+k5. All are positive in the physical interior. The Jacobian is

[[-A, k2, k2-k6], [p,-p-q,-p], [0,k5,-k6]].

Its second additive compound in the wedge basis (12,13,23) is

[[-A-p-q,-p,k6-k2], [k5,-A-k6,k2], [0,p,-p-q-k6]].

The ordinary induced l1 matrix measure is not automatically negative: the second column gives -A-k6+2*p. Thus this coordinate change does not by itself remove the global-stability obstruction. A uniform sign conclusion from cancellation before taking absolute values would be invalid. Next possibilities are a state-dependent metric, monotone-system structure, or exact counterexample search, only after source scope is complete.

## Positive-compartment mechanism found 06:03 UTC

A different elimination avoids the mixed-sign reduced Jacobian. Keep x=(r,c,b,z)=(free receptor,C0,B0,C1), eliminate only free ligand m=r+Delta (Delta=Mtot-Rtot) and free Lck e=Etot-b. Write f(r)=k1*r*(r+Delta). Then

r'=-f(r)+k2*c+k6*z,
c'=f(r)-k2*c-k3*c*(Etot-b)+k4*b,
b'=k3*c*(Etot-b)-(k4+k5)*b,
z'=k5*b-k6*z.

The physical domain is the convex compact set r,c,b,z≥0, r+Delta≥0, b≤Etot and r+c+b+z=Rtot. Every boundary face is forward invariant in the required direction. The Jacobian is Metzler on this set and its column sums vanish. Its directed off-diagonal graph contains the strongly connected edges r→c, c→r, c→b, b→c, b→z, z→r.

For a fixed positive equilibrium x*, the difference x(t)-x* solves y'=A(t)y with A(t)=integral_0^1 J(x*+theta*(x(t)-x*)) dtheta. This is Metzler with zero column sums. The c→b rate is at least k3*(Etot-b*)/2>0, and r→c is k1*(r(t)+r*+Delta)≥k1*m*>0. All other listed edges have fixed positive lower bounds. Thus A(t) is uniformly bounded and has a uniformly positive strongly connected graph for all physical initial data, even boundary data. Its time-one transition matrix has every entry bounded below by a fixed epsilon>0, by integrating along directed paths after adding a large multiple of the identity. Being column stochastic, it contracts the l1 norm of every zero-sum vector by at most 1-4*epsilon. Iteration proves exponential convergence to x* within each conservation class, with a nonsharp class-dependent rate. This argument does not require importing the thesis's persistence theorem.

Existence and uniqueness of x* can be obtained directly. At equilibrium z=(k5/k6)b and c=((k4+k5)/k3)*b/(Etot-b). Let w(b)=c+(1+k5/k6)b. On the interval where 0<b<Etot and w(b)<min(Rtot,Mtot), the equation

k1*(Rtot-w(b))*(Mtot-w(b))=k2*c(b)+k5*b

has a strictly decreasing left side and a strictly increasing right side, with opposite endpoint signs. It therefore has exactly one root. Reconstruction gives all free and bound species strictly positive.

This is an unreviewed full candidate for the single-step subproblem. It is not a resolution of arbitrary chain length or of the entire imported asymptotic bundle. Literature and exact source-model constraints still need audit; the cooperative first-integral mechanism is classical and no novelty claim is made.
