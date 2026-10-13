# Exact ordinary boundary criterion

Let f be holomorphic from the open unit disk into itself and write

\[\Phi_f(z)=(1-|z|^2)|f'(z)|/(1-|f(z)|^2).\]

Assume the ordinary limit of this expression at 1 is 1. A constant strict disk map has distortion0 and therefore cannot satisfy the hypothesis. Choose δ>0 so every disk point with |z−1|<δ has Φ_f(z)>1/2. For every fixed ξ on the open circle arc |ξ−1|<δ/2, sufficiently close disk points also lie inside the original collar. Their unrestricted liminf is at least1/2. Applying the credited Kraus–Roth–Ruscheweyh arc criterion gives local holomorphic continuation across this arc, with circle-valued boundary values. The essential quantifier is control of *every* nearby interior point, not just a radius or Stolz angle.

At 1 the continuation has value η of modulus1. After shrinking the neighborhood it is nonzero. Set u=−log|f| on the disk side. This harmonic function is strictly positive there and zero on the smooth boundary arc. The local Hopf boundary lemma applies on a small interior tangent ball and gives positive inward normal derivative of u. The tangential derivative of |f(e^{it})|² at t=0 makes η̄ f'(1) real; its radial derivative, with Hopf's sign, makes this number α strictly positive. Thus f'(1)=αη≠0 and the local complex inverse exists. No global injectivity follows.

Conversely suppose such local holomorphic circle reflection exists for a strict disk map. The preceding argument gives α>0. In local real coordinates normal and tangential to the circle, the real-analytic function 1−|f(z)|² vanishes when 1−|z|²=0. Integration of its normal derivative factors it as (1−|z|²)H(z), with H continuous near1 and H(1)=α. The numerator's remaining factor |f'(z)| also tends toα. Hence Φ_f(z)=|f'(z)|/H(z) tends to1 for every interior approach. This factorization avoids dividing an O(|z−1|²) error by a possibly much smaller boundary distance.

The affine strict disk map f(z)=(1+z)/2 illustrates the quantifier boundary. In any non-tangential approach its distortion tends to1. Along z=1−t²+it, 0<t<1, the point stays inside the disk, since 1−|z|²=t²−t⁴>0, and

\[\Phi_f(z)=2(1-t^2)/(3-t^2)\longrightarrow2/3.\]

Thus it has no unrestricted limit1. This is a counterexample to replacing the premise by an angular limit, not a counterexample to the target theorem. Local reflection also permits z² and a singular inner function analytic near1, so automorphism, whole-circle continuation, derivative1 and finite Blaschke conclusions are unsupported.

The imported arc theorem, Hopf lemma and inverse function theorem remain established inputs. This review does not newly certify the complete2007journal proof. There is no new project solution or priority claim, and the proper disposition remains already_solved, original0/5,new0,audit0, with no paper/new DOI/tracker.
