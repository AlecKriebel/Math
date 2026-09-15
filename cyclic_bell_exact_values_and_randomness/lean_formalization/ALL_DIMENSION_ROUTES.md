# All-dimensional routes and proof obligations

**All Lean statements discussed here are uncompiled source candidates.**
This note explains intended mathematical mechanisms so an offline reviewer can
separate a library/API problem from a mathematical gap. It is not proof-assistant
verification, independent review, or a novelty claim.

## 1. Continuous factors instead of discontinuous polar division

For a complex number w, define

\[
h(w)=\sqrt{|w|},\qquad k(w)=w/\sqrt{|w|},
\]

with k(0)=0 (as given by totalized field division). Both are continuous, including
at zero, because |k(w)|=sqrt(|w|). The pointwise identities are

\[
\overline h h=|w|,\quad \overline k k=|w|,\quad \overline h k=w.
\]

For U=A0* A1 and w_y(z)=1+omega^y z, continuous functional calculus gives H_y,
K_y with H_y*=H_y, H_y^2=|w_y|(U), K_y* K_y=|w_y|(U), H_y K_y=I+omega^y U.
(The star on A0 here denotes its adjoint.) All these are functions of Alice's
unitary U and commute with Bob's operators under cross-party commutation.

Set P_y=H_y A0* - K_y B_y. Expansion gives

\[
P_y^*P_y=A0 H_y^2 A0^*+H_y^2-
 [(A0+\omega^y A1)B_y+((A0+\omega^y A1)B_y)^*].
\]

The scalar bound supplies a nonnegative function
M_d-sum_y |1+omega^y z|. Taking its continuous square root gives G and the
complete gap

\[
M_d I-I_d=\tfrac12\sum_yP_y^*P_y+
 \tfrac12 G^*G+\tfrac12(GA0^*)^*(GA0^*).
\]

The aligned augmentation is another square. No inverse of H_y, no assumed
nonzero spectrum, and no chosen unitary polar extension enters the upper bound.
The matrix theorem and complete-Hilbert theorem instantiate this mechanism
separately. They do not infer infinite-dimensional validity from a matrix result.

Review the continuity-at-zero estimate, the spectrum unit-circle theorem, CFC
star/sum/product transport and the exact orientation of P_y. These are among
the least compilation-tested, most library-sensitive portions of the source.

## 2. The physical Fourier route

On Z/d, chi(j)=exp(2*pi*i*j/d), define

\[
\widehat q_m=\sum_jq_j\chi(mj),\qquad
R_t=\sum_jq_{j+t}\overline{q_j}.
\]

Wiener--Khinchin and inversion imply

\[
|\widehat q_m|^2=\sum_t R_t\chi(mt),\qquad
R_t=d^{-1}\sum_m|\widehat q_m|^2\chi(-mt).
\]

The actual rank-one projectors on Phi_d give
p(a,b)=|qhat_(−a−b)|^2/d^3. The transpose, not an adjoint, in the entangled
trace identity fixes the sum of outcomes. Parseval proves uniform local
marginals, while zero nonzero-lag autocorrelations characterize a uniform joint
table. The canonical chirp is cyclic because of its parity correction.

The final-two transposition affects three adjacent-weight products and yields
R2=(z_(d−1)-z_(d−2))(z_(d−3)-z_0), nonzero for d>=4. The source proves the exact
absolute value and the manuscript quantitative gap.

A useful stronger intermediate inequality is written as well. If x_m is the
power spectrum minus its mean, Delta=max x_m and t!=0, then

\[
d|R_t|=|\sum_m(\Delta-x_m)\chi(-mt)|
 \le\sum_m(\Delta-x_m)=d\Delta.
\]

Here Delta-x_m is nonnegative and sum chi(-mt)=0. Thus the peak excess is at
least |R_t|, which implies the manuscript's weaker stated bound. This is an
intended exact deduction, not a claim of a new externally verified result.

## 3. Second-family coefficients

The actual source formula is retained, including the l=0 signed exponent and
negative sine denominator. Its finite signed geometric sum gives
S_l=d lambda_l r_l. Parseval on the unit polar-phase sequence gives coefficient
normalization. DFT orthogonality gives sum Bhat_l* Bhat_l=d^2 I. Expanding
P_l=d lambda_l I-A_l Bhat_l yields prefactor 1/(2d). On Phi_d the explicit
Fourier-compressed Bob cycle cancels each residual. These identities are proved
as source statements rather than supplied as validity fields of a strategy.

## 4. Support rigidity from actual saturation

The density-matrix square root provides a purification coefficient matrix T.
Alice's support is the range of the actual partial trace, identified with the
range of the corresponding rectangular amplitude matrix. Vanishing expectation
of a positive square is its zero action on the purification, not a global
operator-zero assertion.

A finite-spectrum calculus supplies exact zero transfer: if f vanishes only
where g vanishes on the finite spectrum, f(U)T=0 implies g(U)T=0. The quotient
is defined only on the finite spectrum and is zero at denominators that vanish;
there is no global inverse claim. This first identifies equality-root support,
then allows cancellation of polar moduli on that support.

The augmented stabilizer supplies A0 T=T D. Polar residual cancellation supplies
V_y T=T B_y*. Their scalar adjacent-phase relation gives a reflection I-2E_k,
with the wrap-around minus sign encoded through exp(pi*i/d)^d=-1. The power
relations are derived from Bob's actual order-d PVM encodings.

A relative rank telescoping argument proves rank(T)<=d rank(E_k T). Orthogonal
root projections sum to the support, so their ranks sum to rank(T). The lower
bounds then force every rank to equal rank(T)/d. The source additionally
identifies the projected ranges with the actual supported eigenspaces and
proves support invariance and positive multiplicity. No conclusion extends to
unused ambient blocks, approximate saturation, or a commuting-model support.

## 5. Physical privacy and low-setting ingredients

For purification coefficients T, the conditional Eve matrix is defined as a
true sandwich and partial trace, then related to an effect kernel. This makes
operator Fourier inversion and the private-MUB sandwich proof applicable to
physical conditional states. The binary calculation derives on-state
anticommutation from two vanishing squares; it never assumes global Pauli
relations for arbitrary maximizing realizations.

The one-input model uses a product of conditional distributions, with a default
outcome for a zero-probability conditioning event. The complete hidden table is
stored coherently in a pure tripartite state. All grouping measurements and
Eve's success are explicit.

## 6. A simpler computational-MUB exposure proof

A Hermitian sum of circulants and a diagonal-unitary conjugate of a circulant
has constant diagonal. If e_r is an eigenvector with eigenvalue kappa, that
constant diagonal is kappa. If kappa is a scalar spectral upper or lower bound,
then +/- (K-kappa I) is PSD with zero diagonal. A PSD matrix with zero diagonal
is zero: represent it as a Gram matrix and use the diagonal squared norms.
Thus K=kappa I. A nonscalar K cannot have this computational eigenvector at a
spectral extreme. This proves the source's scoped obstruction by a stronger
constant-diagonal argument, without claiming its Toeplitz block proof is checked.

## Remaining boundary

The full correlation-model embeddings, closure and supremum wrappers are not
written, even though their main upper-bound and witness ingredients now are.
The appendix source-strategy identification and some benchmark/asymptotic
calculations are also absent. See `COVERAGE.md` for the exact current boundary.
