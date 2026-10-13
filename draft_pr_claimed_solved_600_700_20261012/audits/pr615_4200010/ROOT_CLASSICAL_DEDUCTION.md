# Root check of the classical implication for PR #615

The current PR is still `claimed_solved`. This checks a priority concern, not
an error in its mathematically valid compact candidate. No publication action
or PR disposition is authorized by this provisional document alone.

## Primary evidence checked

1. H. Anzai, *Ergodic skew product transformations on the torus*, Osaka
   Mathematical Journal 3 (1951), 83–99, section 6, Theorem 6 and Corollary,
   printed pages 91–92; DOI https://doi.org/10.18910/11966. The exact irrational
   torus skew shift and its ergodic/mixed-spectrum mechanism occur there.
2. M. de León and M. Saralegi, *Cosymplectic reduction for singular momentum
   maps*, J. Phys. A 26 (1993), 5033–5043; DOI
   https://doi.org/10.1088/0305-4470/26/19/032. Lemma 3.2, printed page 5036,
   gives the symplectic thickening of a cosymplectic manifold. Section 6.1,
   printed page 5042, takes the old Hamiltonian to be zero and identifies the
   added real coordinate's Hamiltonian field with the lifted Reeb field.

Root visually read the exact relevant pages from primary publisher/author
copies; raw fulltexts remain in ignored private source caches. The implication
below is our checkable deduction from their ingredients. Neither cited paper
is being represented as explicitly discussing Knill's later named question.

## Complete finite-volume consequence

Let F(x,y)=(x+a,y+x) on R²/Z² with irrational a. Its area-preserving derivative
is [[1,0],[1,1]] and F^n(x,y)=(x+na,y+nx+a n(n−1)/2). Its Haar ergodicity and
non-almost-periodic Fourier character orbit are the classical Anzai mechanism.
Form its constant-roof mapping torus N=(T²×R)/((z,t)~(Fz,t−1)). The forms
beta=dx∧dy and tau=dt descend and are closed. Their product has total mass one.
The Reeb field for this cosymplectic pair is R=∂t, with flow psi_s[z,t]=[z,t+s].

On the boundaryless manifold M=N×(0,1), apply the 1993 thickening to obtain
omega=beta+tau∧dE and the globally real H=E. Contraction gives X_H=R. The open
interval has length one, so mu=omega²/2=nu dE has finite total mass one. M is
noncompact, but its complete Hamiltonian flow preserves the E-coordinate and
has compact regular energy components N×{E}. The printed 2000 question has
no compactness assumption, so this is already within its stated unrestricted
symplectic category. This avoids any infinite-ambient-measure ambiguity.

In the globally descended frame V1=∂x−t∂y, V2=∂y, V3=∂t, V4=∂E, the derivative
is Id+sP where P(V1)=V2 and P²=0. Forward and inverse norms are bounded by
1+|s|. Thus all four Lyapunov exponents are zero at every point, in this smooth
metric. For any other smooth metric, its comparison with this frame metric is
uniform on each fixed invariant compact energy component, including the full
tangent bundle along that component. Thus metric independence holds at every
point of M, although the comparison constant can depend on E. The compact
candidate additionally has a uniform constant over the whole phase space.

Continuous-time suspension ergodicity follows from translation invariance in
t and the seam relation plus ergodicity of F. For any positive-measure invariant
C⊂M, invariance at rational times and Fubini show that almost every energy
section is invariant at all rational times; strong L² continuity upgrades to
all times. Each section is full or null by suspension ergodicity. Therefore
C=N×J modulo null sets with Leb(J)>0. The measurable fundamental-domain
observable G=exp(2πiy) has orthogonal integer translates on each component and
on N×J: their inner products equal Leb(J) delta_nm. After normalization their
pairwise distances are sqrt(2), so C is not almost periodic. The maximal good
region exists modulo null sets by countable disjointification, finite-sum L²
approximation and the supremum-of-measures argument. Thus good has zero
measure, bad is empty in the displayed metric (and almost everywhere in any
smooth metric), and ugly has full measure one.

The compact cutoff model in the PR is a valid compact presentation of the
same mechanism. Compactness, explicit volume 1/4 and real circle cutoff do not
restore novelty of the original unrestricted existence question, which was
already answered by the finite-volume classical consequence above. A stronger
new target cannot be silently substituted for that original question.

## Repair assessment and exact remaining decision

Adding the two missing classical citations would repair attribution, and a
note presenting this old consequence could be useful exposition. It would
not establish the requested resolution of an original still-unsolved problem.
The user excludes already-solved outcomes from the publication/merge process.
No new distinct research problem is being invented to rescue eligibility.
An independent adversarial reviewer is checking this implication and whether
it warrants priority rejection. Final disposition awaits that completed review.

Root checkpoint timestamp: 2026-10-13T03:25:27.535708+00:00. Best-guess completion: 70% toward a verified audit disposition; publication remains held.
