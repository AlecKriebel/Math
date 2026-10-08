# Author approach 3: restriction–corestriction descent

Aim: reduce equality to extensions where a calculation is simpler, without discarding the torsion that carries the invariants.

## Descent in the actual quotient targets

Let L/F be a finite separable extension of degree n. Galois restriction and corestriction give maps on B_i. They also give maps on Q_{i,r}. Indeed restriction takes r[A] cup z to r[A_L] cup res(z), and the projection formula gives

    cor(r[A_L] cup w)=r[A] cup N_{L/F}(w).

Here N is the Milnor K-theory transfer. Therefore corestriction preserves the denominator subgroups. On the quotient, as on B_i,

    cor res = n id.

Let f,g be natural homomorphisms from SK_i(A) to one common target Q_{i,r}, and put delta=f-g. Suppose d SK_i(A)=0; the index bound in Kahn's introduction supplies this with d=ind(A). Then d delta(x)=0 for every x.

If delta_L(res x)=0, naturality implies res(delta_F(x))=0. Applying cor yields n delta_F(x)=0. Consequently, if gcd(n,d)=1, Bezout gives delta_F(x)=0. More generally, if restrictions kill the difference over finitely many extensions of degrees n_1,...,n_t and gcd(d,n_1,...,n_t)=1, the same conclusion follows. This is a pointwise result: the hypothesis is needed for the particular restrictions of x. It need not assume surjectivity of SK_i(A)→SK_i(A_L).

For a prime l dividing d, the same argument detects the l-primary component of delta whenever n is prime to l. Testing the components separately is enough because every value is d-torsion. This yields a precise primary descent criterion, applicable both to beta_i versus sigma_1^i and to any genuinely common-target comparison involving c_A.

## Why the obvious splitting-field approach fails

All the relevant invariants vanish after passing to a splitting field, since SK_i of a split algebra is zero. But every finite splitting extension has degree divisible by ind(A). Thus the resulting equation ind(A) delta=0 is already known; it does not prove delta=0.

This is not merely a hypothetical objection. Approach 1 supplies actual maps sigma_1^1 and q_1 c_A that become equal after splitting A but are unequal over F. Inverting d, or rationalizing, also kills the entire source, so agreement there gives no information about the desired torsion equality.

For an abstract control of the transfer step, take B=Z/d and a zero restriction to the zero group. Corestriction is zero and cor res=d id=0. The nonzero elements of B survive over the base despite vanishing after restriction. This finite model is only a check on the logic; the preceding Platonov example provides the genuine mathematical obstruction.

## A normalization issue for the SL_1 invariant

Throughout this argument, c_A means the invariant attached to the fixed base algebra, evaluated after extension. It is not silently replaced by the newly normalized universal generator c_{A_L}. Kahn Remark 10.8 explains that universality can change after extension; Lemma 10.9 guarantees preservation of the normalized generator when exp(A_L)=exp(A). If that condition is unavailable, comparing newly normalized generators is an additional task.

## Outcome and gap

A verified comparison over suitable prime-to-l extensions would descend the l-primary equality. No family of such extensions on which beta_i and sigma_1^i can actually be computed is established here. Splitting fields and rational coefficients do not fill that gap.
