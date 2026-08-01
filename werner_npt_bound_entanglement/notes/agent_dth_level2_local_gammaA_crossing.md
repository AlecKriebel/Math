# Local \(S_7\) crossing for the prolonged DTH support face

## 1. Exact mixed-module census

After partial transpose of the anchored first bivector, one physical site
carries

\[
\overline{\mathbb C^3}^{\otimes2}\otimes
(\mathbb C^3)^{\otimes5}.
\tag{1}
\]

In determinant-shifted highest-weight notation its complete irreducible
census is

\[
\begin{array}{c|rrrrrrrrrr}
\lambda&(5,0,-2)&(5,-1,-1)&(4,1,-2)&(4,0,-1)&(3,2,-2)&
(3,1,-1)&(3,0,0)&(2,2,-1)&(2,1,0)&(1,1,1)\\ \hline
m_\lambda&1&1&4&10&5&24&20&15&36&11\\
d_\lambda&81&28&64&35&35&27&10&10&8&1.
\end{array}
\tag{2}
\]

Here \(m_\lambda\) is the multiplicity and \(d_\lambda\) the irreducible
carrier dimension.  In particular,

\[
\sum_\lambda m_\lambda d_\lambda=2187=3^7,
\qquad
\sum_\lambda m_\lambda^2=2761.
\tag{3}
\]

The holomorphic seven-replica module has the eight \(S_7\) shapes

\[
[7],[6,1],[5,2],[5,1,1],[4,3],[4,2,1],[3,3,1],[3,2,2]
\]

with multiplicities

\[
(1,6,14,15,14,35,21,21)
\]

and \(U(3)\)-carrier dimensions

\[
(36,48,42,15,24,15,6,3).
\]

Its commutant dimension is also \(2761\).

### Exact proof of (2)

On each dominant weight space of (1), form the two integral raising maps for
\(E_{01}\) and \(E_{12}\).  Modular row reduction proves that the dimensions
of their common characteristic-zero kernels are at most the values
\(m_\lambda\) in (2).  These upper bounds, multiplied by the Weyl dimensions
\(d_\lambda\), already sum to the entire module dimension \(3^7\).
Complete reducibility therefore forces every upper bound to be attained and
excludes any omitted irreducible.  This is a finite exact proof, independently
replayed by \`verification/verify_dth_level2_mixed_s7_census.py\`.

## 2. Numerical crossing construction

Let \(P_\pi\) be the seven-replica permutation diagram for
\(\pi\in S_7\), and let \(\Gamma_{01}\) transpose the two legs of the
anchored bivector.  The local crossing was constructed without forming any
\(2187\times2187\) dense diagram:

1. restrict each sparse \(\Gamma_{01}(P_\pi)\) to the ten mixed
   highest-weight multiplicity spaces;
2. construct Young-orthogonal \(S_7\) representations along an
   adjacent-transposition breadth-first tree; and
3. use finite-group Fourier inversion to recover every normalized
   holomorphic matrix unit.

For a holomorphic shape \(\nu\), multiplicity indices \(a,b\), carrier
dimension \(d_\nu\), and Specht dimension \(f_\nu\), the matrix unit is

\[
\frac{f_\nu}{7!d_\nu}
\sum_{\pi\in S_7}
\rho_\nu(\pi)_{ab}P_\pi.
\tag{4}
\]

Equation (4) fixes both the orientation and trace normalization.

The resulting crossing is a real \(2761\times2761\) matrix.  Its independent
numerical audits are

\[
\begin{aligned}
\|C^{\mathsf T}D_{\rm mix}C-D_{\rm hol}\|_F
 &=2.4002991346120364\times10^{-14},\\
\|C^{\mathsf T}D_{\rm mix}C-D_{\rm hol}\|_{\max}
 &=1.8318679906315083\times10^{-15},\\
\text{maximum trace error}
 &=8.43769498715119\times10^{-15}.
\end{aligned}
\tag{5}
\]

The discovery cache
\`discovery/dth_level2_local_gammaA_crossing.npz\` has SHA-256

\`\`\`
af76759c761b1deafd335418779e6735120b5e860a0893c17a3b155d4866a5e5
\`\`\`

and is intentionally not tracked because it is a 55 MB floating-point
artifact.

## 3. Scope and next reduction

The exact census and the numerical crossing settle the **local** symmetry
layer of the prolonged support test.  They do not yet establish positivity
of the partial transpose of the saved degree-three extension.  A naive
three-site tensor product would contain mixed multiplicity blocks as large
as \(36^3=46656\), so dense assembly is inappropriate.  The next calculation
must combine the pair symmetry and the support-kernel projector before
testing the mixed spectrum, or apply the crossed blocks matrix-free and rank
the active negative sectors.

