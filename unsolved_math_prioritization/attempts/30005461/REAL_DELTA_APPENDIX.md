# Secondary check: the real delta invariant is 6

This appendix is independent of the principal cubic-surface proof and is not needed for its conclusion. It supplies the target-specific local calculation suggested by *Stubborn Polynomials*, arXiv:2602.01191v1, Definition 6.3. That source is a preprint; none of its Del Pezzo or resolution criteria is imported by the principal proof.

Fix \(0<c<3\) and let \(M_c=x^4y^2+x^2y^4+z^6-cx^2y^2z^2\). AM--GM gives \(M_c\ge(3-c)x^2y^2z^2\). Thus a real projective zero has \(xyz=0\); if \(z\ne0\), setting either \(x\) or \(y\) to zero leaves \(z^6>0\). On \(z=0\), the form is \(x^2y^2(x^2+y^2)\). Its only real projective zeros are consequently \(P=[1:0:0]\) and \(Q=[0:1:0]\).

In the chart \(x=1\) at \(P\), write \((u,v)=(y,z)\). The local equation is

\[
F_0(u,v)=u^2+u^4+v^6-cu^2v^2.
\]

It has multiplicity 2 with tangent cone \(u^2\). We inspect both real charts of each blowup, dividing by the exceptional factor squared at each multiplicity-2 center.

1. First blowup. In the chart \(u=av\),
   \[
   F_0(av,v)=v^2F_1(a,v),\quad
   F_1=a^2+a^4v^2+v^4-ca^2v^2.
   \]
   On the exceptional divisor \(v=0\), the strict transform is \(a^2=0\), so the unique real point is \((a,v)=(0,0)\). Its multiplicity is 2 and tangent cone \(a^2\). In the other chart \(v=bu\), the strict transform is
   \[
   1+u^2+b^6u^4-cb^2u^2,
   \]
   whose value on the exceptional divisor \(u=0\) is 1. There are no omitted real first-order points.

2. Second blowup at \((a,v)=(0,0)\). In the chart \(a=bv\),
   \[
   F_1(bv,v)=v^2F_2(b,v),\quad
   F_2=b^2+b^4v^4+v^2-cb^2v^2.
   \]
   On \(v=0\), the only real point is \(b=0\). At its origin the multiplicity is 2, with tangent cone \(b^2+v^2\). In the other chart \(v=sa\), the strict transform is
   \[
   1+s^2a^4+(s^4-cs^2)a^2,
   \]
   with value 1 on \(a=0\). Again there are no other real points over the center.

3. Third blowup at \((b,v)=(0,0)\). In the chart \(b=tv\), the strict transform is
   \[
   F_3(t,v)=1+t^2-ct^2v^2+t^4v^6.
   \]
   Its restriction to \(v=0\) is \(1+t^2>0\). In the other chart \(v=sb\), the strict transform is
   \[
   1+s^2-cs^2b^2+s^4b^6,
   \]
   with restriction \(1+s^2>0\) to \(b=0\). There are no real first-order infinitely near points beyond this third multiplicity-2 center. The two complex tangent directions are not real and are not counted in the real delta recursion.

The centers in the second and third steps lie on the newest exceptional divisor only: in the displayed vertical chart the strict transform of the older exceptional divisor is in the complementary direction at infinity. Thus there is also no unexamined real point at an intersection of older exceptional curves. Equivalently, the complementary chart checks above cover those directions explicitly.

Definition 6.3 adds \(m(m-1)/2=1\) at each of these three multiplicity-2 centers, and then terminates because there are no real infinitely near points. Therefore \(\delta_P^{\mathbb R}(M_c)=3\). Symmetry in \(x,y\) gives \(\delta_Q^{\mathbb R}(M_c)=3\), and hence

\[
\delta^{\mathbb R}(M_c)=3+3=6\qquad(0<c<3).
\]

The local calculation is actually independent of the real parameter \(c\); the restriction \(0<c<3\) is used to identify the complete global real zero set. In particular, no continuity extrapolation from \(c=1\) is used. At \(c=3\) additional global real zeros occur, so this appendix makes no claim that the total invariant there is 6.
