# Approach 5: empirical invariance, entropy, and symbolic degeneration

**Result:** a rigorous reduction exposing a missing entropy-production step; no uniform positive entropy is obtained. This is a failed proof route, not a claimed new theorem solving the problem.

## Approximate simultaneous invariance
For L>=0 define the probability measure
mu_L=(L+1)^(-2) sum_{n,k=0}^L delta_(a^n b^k r/s mod 1).
Multiplicity is retained. Let T_a(x)=ax mod 1. Cancellation of the interior rows gives exactly
(T_a)_*mu_L-mu_L=(L+1)^(-2) sum_{k=0}^L [delta_(a^(L+1)b^k r/s)-delta_(b^k r/s)].
Its total variation norm, using the convention ||nu||=sup_{|f|<=1}|nu(f)|, is at most 2/(L+1). The analogous formula holds for T_b. Thus any weak subsequential limit along L->infinity is jointly invariant: integrate a continuous f, pass to the limit in both f and f composed with T_a or T_b, and use the displayed bound. Compactness of probability measures on the circle supplies subsequential limits.

## What entropy would suffice
Let P_q be the partition into q half-open equal intervals, and let H_mu(P_q) be Shannon entropy using natural logarithms. If the support of mu is covered by K intervals of length 1/q in [0,1], at most 2K partition atoms have positive measure. (A length-1/q interval cannot meet more than two half-open atoms carrying distinct points of its support.) Hence
H_mu(P_q)<=log(2K).
Thus proving H_(mu_L)(P_q)>=c log log s for q comparable to (log s)^N would be sufficient, after subtracting log 2. The implication is only in this direction: low entropy of this particular weighting does not imply small support covering number.

The injective short-block measure from Approach 1 has H(P_s)=2 log(L+1), of order log log s. That is at denominator resolution. The elementary partition comparison gives only
H(P_q)>=H(P_s)-log(ceil(s/q)+1).
To prove this, use the joint refinement P_s join P_q. Each P_q atom meets at most ceil(s/q)+1 atoms of P_s. Conditional entropy is bounded by the logarithm of that number, while H(P_s)<=H(P_s join P_q). For q a fixed power of log s the resulting lower bound is negative and supplies no information.

## A symbolic warning that the scale loss is real
For a single base a>=2, set s_m=a^m-1 and
nu_m=(1/m) sum_{j=0}^{m-1} delta_(a^j/s_m),  m>=2.
Its support has exactly m points, since the displayed positive fractions are distinct. Multiplication by a cycles them, so nu_m is exactly T_a-invariant. It has H_(nu_m)(P_(s_m))=log m.

For an integer 1<=ell<m, multiplication of the j-th support point by a^ell has integer part 0 for j<m-ell, and a^(j+ell-m) for m-ell<=j<m. Indeed
 a^(j+ell)/(a^m-1)=a^t+a^t/(a^m-1)
when t=j+ell-m>=0, and the remainder is less than 1. Hence in P_(a^ell) there is one atom of mass 1-ell/m and ell distinct atoms of mass 1/m. Therefore exactly
H_(nu_m)(P_(a^ell))=-(1-ell/m)log(1-ell/m)+(ell/m)log m.
For ell=O(log m) this tends to zero. Its support is covered by at most ell+1 intervals of length a^(-ell). Thus, at any scale delta comparable to a fixed negative power of log s_m, the covering number is O(log log s_m), despite the fine-scale entropy log m comparable to log log s_m.

Also nu_m converges weakly to delta_0. For any epsilon>0, at most a constant depending on a,epsilon of the fractions a^j/(a^m-1) exceed epsilon: solving the inequality bounds m-j. Their total mass tends to zero; uniform continuity then proves weak convergence to delta_0.

This is a single-generator obstruction, explicitly not a counterexample for two multiplicatively independent bases. It proves that exact invariance, many fine-grid points, and a naive passage to weak limits cannot by themselves preserve the needed entropy scale.

## Remaining gap
One must exploit the interaction of the two independent multipliers to produce entropy at the polylogarithmic scale, uniformly for all rational starting points, rather than merely establish their approximate invariance. Neither the qualitative positive-entropy rigidity theorem nor its effective version supplies the missing entropy hypothesis for free. Invoking them without that input would be circular. This fifth approach stops at that precise missing step.
