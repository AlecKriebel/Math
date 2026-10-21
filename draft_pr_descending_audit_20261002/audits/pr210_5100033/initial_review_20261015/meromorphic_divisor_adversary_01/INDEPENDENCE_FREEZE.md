# Independent mechanism map, frozen before inherited review

UTC: 2026-10-15T11:57:13Z. Audit completion estimate: 12%.

Inputs read so far: root INTAKE.json and only the immutable original PROOF.md and SOURCES.md. No inherited review, checker, author verification, root research notes, or other new review has been read. Scope: head 2180d64b648b81ac660a792f7823d0b715f9cf12. This map records hypotheses to audit, not acceptance.

## Exact claim and independent route

For 0<k<1, 0<v<K, v=2K*tau/N, odd N>=3, gcd(tau,N)=1, 0<tau<N/2, use a=alpha*dn(v)/cn(v), b=alpha*k'/cn(v), c=alpha*k. The target signed focal-pedal area product is T(w)T(w+2K), with Q(w)=(a(c-a*sn(w)), ab*cn(w))/(a-c*sn(w)), and T the cyclic determinant sum for step delta=2v. It suffices to prove that on lattice (4K/N,4iK') this T is an even function about b0=K-v, odd under 2iK', with at most one simple pole in each imaginary half. A nonzero such elliptic function has precisely two simple poles and two forced zeros at their horizontal half-period translates; its half-real-period product is constant. For odd N, 2K is the half reduced real period modulo the reduced lattice.

## Independent preliminary deductions

1. sn has period 4K,2iK'; cn has period 4K,4iK', with sign change under 2iK'. Therefore Q must be put on the larger torus. Merely assigning Q the sn torus would be false.
2. If the quarter-shift identities are correct, sn(r+-v)=a/c and cn(r+-v)=-ib/c, while dn changes sign; r=K+iK'. Thus the two numerator vectors coincide and the two denominator derivatives are opposites. The residue vectors are nonzero, opposite and isotropic. Their determinant is zero. The translate by 2iK' flips the second coordinate and hence the isotropic direction.
3. All ordinary Jacobi poles must be treated separately from zeros of a-c*sn: division by the common simple pole makes Q regular there. Need verify no other singularity and simple degree-two root count on the small torus.
4. At a collision of adjacent singular vertices the double-pole determinant cancels. A single pole can survive; no cancellation of its coefficient is required. For N=3 the two other edges share the sole regular vertex, and must be counted separately. Exact modular collision counting is required for all coprime stars and both imaginary copies.
5. T has period delta by cyclic reindexing and 4K by Q. A Bezout combination of tau and N produces 4K/N. On the reduced large torus, the roots differing by delta collapse to one simple possible pole in each imaginary half, without increasing local order.
6. Q(2K-w)=JQ(w), det J=-1. Reversal of edges contributes a second minus sign; T(2K-w)=T(w). Combining this with period 2v yields evenness about K-v.
7. Let F(z)=T(K-v+z), p=iK'. At z=p+L/2, evenness changes z to -p-L/2, and period L changes that to -p+L/2; anti-period 2p changes its value to -F(p+L/2). The point is disjoint from the poles for L>0. Hence it is zero. The translated zero is distinct. If no pole survives then compactness and anti-period force F identically zero, which needs its own branch of the argument.

## Falsification agenda

Independently derive all shifts and derivatives against primary DLMF; explicitly catalogue common poles/removable limits; compute numerator and derivative residues symbolically; enumerate exact rational real-lattice collisions for odd/even small N and every coprime star; include N=3 and v near 0,K (through varying N,tau). Fresh high-precision calculations will probe complex pole slopes, residue directions, regular common-pole limits, forced zeros, character identities, geometry-product constancy, and even-period failure. These are controls, not proof substitutes. Try deliberate wrong shifts and missing adjacent-pole cancellation to show tests discriminate. Check constant and zero-function branches without dividing by T. Real geometry remains a separate scope question: finite outer vertices, signed orientation, proper cyclic side correspondence, and excluded degeneracies.

## Currently strongest verified conclusion and gap

The elementary divisor lemma follows from the stated analytic hypotheses. The complete theorem is not yet accepted: canonical parameter assumptions, exact Jacobi data, complete pole catalogue, collision count, character proof, and real construction require detailed verification. Completion estimate 12%.
