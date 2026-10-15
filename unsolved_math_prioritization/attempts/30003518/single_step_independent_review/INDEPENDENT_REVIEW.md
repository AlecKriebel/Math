# Independent review of the single-step Lck convergence theorem

**Verdict: PASS for the scoped N=1 theorem, with no mandatory mathematical correction. The original bundled problem 30003518 remains unresolved.**

Reviewed on 2026-10-01. The exact input is `SINGLE_STEP_CANDIDATE.md`, SHA-256 `fb38e57705eeaf1c08325696905f6101318d6c5df59c2232c0549fca0b934ff3`. The reviewer did not contribute to its derivation. This audit is not a certification of historical novelty or human peer review. Source validation, this audit, and packaging do not constitute additional substantive author turns.

## Exact source and scope

I independently read the relevant source text and rendered the original equations and theorem pages in Pia Brechmann's 2024 dissertation, [Mathematical Models for T cell Activation through Kinetic Proofreading](https://openscience.ub.uni-mainz.de/bitstreams/a948dbbc-0daf-4167-bfd8-23ab6e574d64/download). The reading copy has SHA-256 `03cfaec57b310bae13ac077521c0e66034ce0c544365d23cbc8e2b8a65056e2a`.

- Section 2.4, equations (2.2) and (2.3), printed pp. 23–24, give the Lck-only network and its three conserved pools. Setting N=1 identifies the candidate's `(r,m,e,c,b,z)` with `(R,M,L,C0,B0,C1)` exactly.
- Equation (5.5), printed p. 126, independently confirms the same three reduced equations after eliminating all free species. The candidate retains r while eliminating m and e, which is a different but equivalent coordinate choice on the same conservation class.
- Theorem 10, printed p. 134, gives local stability and sufficient conditions for global stability. Its displayed restrictions are not hypotheses of the submitted proof. The candidate's all-positive-rate assertion is a genuine strengthening of that scoped theorem's stated sufficient conditions, assuming no separate historical-priority claim.
- The candidate excludes the full Altan–Bonnet–Germain network, feedback, CD8, ZAP-70, additional ligand species, and arbitrary phosphorylation chains. It does not add enzyme-bound-complex dissociation. These exclusions are essential to identifying the model correctly.

The source describes a broader connection to the 2005 core, but that connection is not used to promote this special-case result to the complete original OWR question. The original asymptotic bundle and N≥2 work remain open in this campaign after author turn 1.

## 1. Physical domain and global existence

The physical set is exactly the intersection of a conservation hyperplane with the inequalities r,c,b,z≥0, r+Delta≥0, and b≤Etot. It is convex and compact and is nonempty for every three positive totals; the all-free state r=Rtot, m=Mtot, e=Etot, c=b=z=0 is an example.

The stated boundary checks are correct. At either free-pool boundary the binding term vanishes. At c=0 its derivative is k1rm+k4b≥0; at b=0 its derivative is k3cEtot≥0; at z=0 its derivative is k5b≥0. At b=Etot its derivative is strictly negative. The sum of the four retained derivatives is identically zero. Local uniqueness for the polynomial vector field plus these inward-pointing conditions gives invariance, and compactness gives forward existence for all time. The affine constraint causes no issue: an ambient polynomial extension is used only to compute a derivative on line segments lying inside the convex physical set.

## 2. Equilibrium existence, uniqueness, and positivity

The b-equation gives c(b)=(k4+k5)b/[k3(Etot-b)], and the z-equation gives z(b)=k5b/k6. Thus w(b)=c(b)+b+z(b) increases from zero to infinity as b rises from zero to Etot. Its derivative is strictly positive. The unique beta with w(beta)=min(Rtot,Mtot) lies strictly below Etot.

On (0,beta), both free pools are positive. The derivative of the scalar balance F is

F'(b) = -k1 w'(b)(Rtot+Mtot-2w(b)) - k2 c'(b) - k5 < 0.

The endpoint signs F(0)>0 and F(beta)<0 hold also when receptor and ligand totals agree. Hence there is exactly one interior root. No boundary equilibrium has been missed: b=0 forces c=z=0 and then c'>0; b=Etot has b'<0; at any remaining equilibrium c,z>0, and a zero free pool would force r'>0. All six recovered concentrations are therefore strictly positive.

## 3. Averaged Jacobian and the apparent boundary degeneracy

The displayed four-dimensional Jacobian is correct. It is Metzler on the entire physical set, and its columns sum to zero. Since the field is differentiable and the domain convex, integrating its Jacobian along the segment between the trajectory and the equilibrium gives the exact difference equation y'=A(t)y. No local linearization approximation is made.

The decisive lower bounds are valid even with boundary initial conditions:

- A(c,r)=k1(r+r*+Delta)=k1(r+m*)≥k1m*>0
- A(b,c)=k3(e+e*)/2≥k3e*/2>0

The equality in the first line holds for either sign of Delta. It does not assume r or m is uniformly positive along the whole trajectory. The positive equilibrium already constructed supplies both constants. The other directed edges have the lower bounds k2, k4, k5 and k6. Their graph is strongly connected with maximum shortest-path length three. Thus neither persistence nor convergence is being assumed to prove convergence.

A concrete time-independent diagonal shift is available, for example

Mshift = 1 + k1(Rtot+Mtot) + k2 + k3(Etot+Rtot) + k4+k5+k6.

It strictly exceeds every possible negative diagonal magnitude of J on the class and therefore of A. This verifies explicitly the bounded-shift existence used by the author. Any positive delta below the six edge bounds works.

## 4. Time-dependent stochastic contraction

For a unit time interval, apply the Peano–Baker expansion to A(t)+Mshift I. Every matrix entry is nonnegative. For a directed path of length ell≤3, one corresponding time-ordered product is bounded below by delta^ell throughout its simplex; integrating gives delta^ell/ell!. Restoring the scalar shift gives the author's positive uniform lower bound. For diagonal entries the identity term gives ell=0. This argument works with time-varying A and does not incorrectly replace the chronological exponential by an ordinary matrix exponential.

The transition matrix is nonnegative and column stochastic because 1^T A(t)=0. Taking epsilon to be the minimum of the finitely many path bounds and 1/8 gives P≥epsilon 11^T. Subtracting that rank-one matrix leaves a nonnegative matrix with column sums 1-4epsilon. On the sum-zero conservation tangent space, epsilon 11^T annihilates the vector, so its l1 contraction factor is at most 1-4epsilon<1. On incomplete time intervals, stochasticity gives l1 nonexpansion. Consequently the displayed estimate with the integer part of t is correct; equivalently it is C exp(-lambda t) for fixed positive C and lambda depending on this class and the rates.

The equilibrium is Lyapunov stable by the same nonexpansion argument, and all original coordinates are recovered by fixed affine maps. This completes the global exponential convergence assertion for every nonnegative initial point in the stated class.

## Independent checks and limitations

`independent_check.py` was independently written from the six reaction stoichiometry columns, rather than copied from author code. It passes **683 exact assertions**, including all conservation laws; the reduced field; the full Jacobian and column sums; the exact integrated mean-value identity; both lower-bound formulas; equilibrium identities and derivative decomposition; all 16 directed shortest-path distances; rational boundary controls with unequal pools and enzyme saturation; and stochastic zero-sum contraction controls. No simulation or floating-point certificate is used.

These finite controls supplement the universal proof, rather than establish an infinite-parameter theorem by sampling. The author's separately sealed checker was then read and replayed in an isolated copy. All four single-step manifest hashes matched, all 575 author assertions passed, and its receipt reproduced byte-for-byte. AUTHOR_REPLAY.json records that supporting replay; it does not replace the independently authored controls.

Strictly positive rates and totals remain mandatory. No uniform convergence rate over singular parameter limits is asserted. N≥2 generally introduces negative cross-derivatives after free-enzyme elimination, so this four-coordinate cooperative proof cannot be transferred unchanged. In particular, this scoped PASS is not permission to mark the original bundled problem claimed_solved or to count review work as an author turn.
