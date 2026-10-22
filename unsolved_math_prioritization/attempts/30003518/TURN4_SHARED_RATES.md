# Turn 4: shared-rate monostationarity obstruction

Started 2026-10-01 06:23 UTC. Unreviewed theorem for the Lck-only core, with an explicit additional rate restriction. This does not assert that every reaction in the original 2005 model has this form.

Assume all unbound-complex dissociation rates d_0,...,d_N equal nu>0, and all Lck association, dissociation and catalysis rates are respectively u,v,w>0. Let a=u/(v+w), q=w*a, and let e denote free enzyme. Put s(e)=q*e/(nu+q*e), so 0<s<1. At equilibrium, with C0>0,

C_i=C0*s^i (0≤i<N), C_N=C0*(q*e/nu)*s^(N-1).

Consequently the total unbound-enzyme receptor-complex concentration is

T=sum_(i=0)^N C_i=C0/(1-s), and C_N=T*s^N.

The bound-enzyme total is a*e*T*(1-s^N). Thus enzyme conservation gives

T(e)=(Etot-e)/theta(e), theta(e)=a*e*(1-s(e)^N).

For 0<e<Etot, theta>0 and

theta'(e)/a=1-s^N-N*s^N*(1-s)
 =(1-s)*[sum_(j=0)^(N-1)s^j-N*s^N]>0.

Every term in the sum is strictly larger than s^N. It follows that T(e) is strictly decreasing, from infinity at e=0 to zero at e=Etot. The total occupied-receptor concentration W(e)=T(e)+Etot-e is also strictly decreasing from infinity to zero. There is therefore a unique beta in (0,Etot) with W(beta)=min(Rtot,Mtot); the physical enzyme interval is (beta,Etot).

Summing the steady free-receptor balance yields the remaining equation

k1*(Rtot-W(e))*(Mtot-W(e))=nu*T(e).

On the physical interval the left side increases strictly from zero to k1*Rtot*Mtot, while the right side decreases strictly from a positive number to zero. Exactly one solution exists. The positive reconstruction from turn 2 yields exactly one physical positive equilibrium for every N≥1 and all positive rate constants/totals within this shared-rate specialization.

This is a structural obstruction to transferring the arbitrary-rate N=2 bistable example into this homogeneous family. The witness has unequal d_i and unequal catalysis rates; neither can be silently identified with shared source parameters. This result is about equilibrium multiplicity, not global convergence.

The original OWR paragraph does not enumerate its strongest simplifying assumptions. The 2024 dissertation supplies the precise independently parameterized core. The original 2005 supplement was recovered as XML data and inspected, never executed: its explicit Lck catalytic values repeat 10.4, and the binding/unbinding values repeat 10000/50 across the sequential core. Other molecular interactions and protected states remain present there, so the homogeneous Lck-only theorem is not promoted to the full original network.
