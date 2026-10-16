# Independent source derivation, before candidate comparison

Recorded 2026-10-14 03:18 UTC. All wrapper and article pages 791-796 were read as text and visually inspected, including complete equation pages 792-794 and all figures, proof, remark, conjecture, references. No earlier priority report or verdict consulted.

Source: S. M. Zemyan (2003), *The Existence of a Waver Point on the Omitted Arc of a Support Point of the Class S*, Complex Variables 48(9), 791-796, DOI 10.1080/02781070310001599359. The example is a genuine global maximizer of Re f(z0), z0=(2/5)exp(5 pi i/6), using Brown's characterization. The article's mathematical observable is phi=arg w', not theta=arg w or the radial angle.

Put B=b exp(i eta), q=1/sqrt(B) with arg sqrt(B)=eta/2; T>0 is fixed by the finite tip; s=exp((t-T)q). Equations (1.2)-(1.4), page 792, give

    w=-4B s/(1-s)^2,
    w'/w=q (1+s)/(1-s),
    w''/w'=q [1+s/(1+s)+3s/(1-s)].

Direct substitution gives B^2/(B-w)*(w'/w)^2=1. The three angular derivatives are therefore

    theta'=Im[q(1+s)/(1-s)],
    phi'=Im[q(1+4s+s^2)/(1-s^2)],
    (theta-phi)'=Im[-2q s/(1-s^2)].

This is an exact distinction. A sign reversal in phi' alone is not one in theta' or (theta-phi)'. On page 792, Zemyan expressly attributes decreasing theta and decreasing arg(w/w') to Brown for this family.

Let a=eta/2 in (0,pi/2), h=T-t>0, xi=h q=x-i y, x>0, y>0. Then w=-B csch^2(xi/2), w'/w=q coth(xi/2), and

    theta'=[x sin(y)-y sinh(x)]/[h(cosh(x)-cos(y))],
    beta'=-[x cosh(x)sin(y)-y sinh(x)cos(y)]/[h(sinh(x)^2+sin(y)^2)],

where beta=theta-phi=arg(w/w') is the radial angle used by this source. Since sin(y)<=y and sinh(x)>x for x>0, theta'<0 for every h>0. If the physical source arc satisfies 0<y<pi, then beta'<0 also: for 0<y<pi/2, tan(y)/y>1>tanh(x)/x; for pi/2<=y<pi, the numerator is directly positive. In the same range,

    Re(w'/w)=[x sinh(x)+y sin(y)]/[h(cosh(x)-cos(y))]>0.

Thus the source example has strict outward increasing radius and beta in (0,pi/2); the magnitude |beta| equals beta and is strictly decreasing. The opposite orientation gamma=phi-theta=-beta is strictly increasing. Tangent phi=theta-beta can reverse even while theta and beta decrease. This gives a direct mechanism explaining the source result without promoting it to the target result.

Source example parameter definitions (pages 793-794): r=2/5, R=log(7/3), eta+R sin(eta)=5 pi/6, b=r/(1-r^2)*exp(R cos(eta)), epsilon_source=exp(-i eta). At the tip ztip=-z0 B/|z0 B|,

    Qtip=[sqrt(1+1/(r epsilon_source))+sqrt(1+r/epsilon_source)]^2,
    Mtip=[sqrt(1+r/epsilon_source)-r sqrt(1+1/(r epsilon_source))]^2/(1-r^2),
    T=sqrt(b) sec(eta/2) [log|Qtip|-Re(epsilon_source log Mtip)+log(r/(1-r^2))].

Here epsilon_source is the paper's phase abbreviation, entirely different from the candidate's tiny perturbation parameter. The branch logarithm of Mtip must be the continuation from z=0 in Brown's formula. The source says s(0)=-V(ztip); equality of 4Bv/(1+v)^2 permits v or 1/v in general. Choosing the inside-disk branch, |Vtip|<1 and |s(0)|<1, resolves this ambiguity. The wording about a unique unit-circle preimage on page 793 is not itself sufficient for that branch selection; a direct phase/residual and modulus check is needed.

Endpoint h->0: w=-4B^2/h^2+B/3+O(h^2), w'/w=2/h+h/(6B)+O(h^3), so theta tends to the continuous branch of arg(-B^2)=2 eta-pi for this example, and beta tends to 0 from above. Both theta' and beta' have the same leading term h Im(1/B)/6<0; their difference cancels to leading order. The tangent derivative satisfies phi'=h^3 Im(1/B^2)/60+O(h^5), which is positive for pi/2<eta<pi. The tip is t=0, not h=0. The source's waver lies strictly between t=0 and t=T.

Pending reproducible checks: high precision source parameters, tip branch residual, bounds ytip<pi, source negative/positive tangent samples, and the other angle samples. This source-first note precedes all reading of the candidate manuscript.
