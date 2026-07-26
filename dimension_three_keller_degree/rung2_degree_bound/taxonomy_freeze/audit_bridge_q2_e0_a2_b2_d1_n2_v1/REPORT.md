# Post-freeze bridge audit: `Q2-E0-A2-B2-D1-N2`

**Verdict:** **PASS**

**Audit completed (UTC):** 2026-07-26T10:25:10Z.

This is a row-level certificate for exclusion as a quartic Keller
counterexample.  It does not claim that the row contains no Keller maps:
the conclusion is that every Keller map in the row is a polynomial
automorphism.

No shared ledger, registry, frozen file, or Git state was changed.

## 1. Blinded provenance

Before 2026-07-26T10:10:25Z, the only pre-existing project files read were
the frozen taxonomy and its machine-readable manifest.  The resulting
normal forms, boundary routing, and polynomial frozen-coefficient map are
sealed in `BLINDED_DERIVATION.md`.

Frozen input hashes:

```text
41fccc44d23fab125819990a2b27526771fbfb62293910b98cfcf1821576d03d  FROZEN_TAXONOMY_v1.md
5a2bdd57438e9ebcca18d04c53ebc98ced2b61209e2de99674aede501c615c23  frozen_manifest_v1.json
```

The blinded form of every row point is
\[
H_4=uR(p,q)+vS(p,q),
\]
where \(u,v\) are independent target vectors, \(p,q\) are a primitive
coprime quadratic pencil, and \(R,S\) are coprime binary quadratics.  The
calculation retains the general six coefficients of each of \(p,q\), all
six coefficients of \(R,S\), and all six entries of \(u,v\).

## 2. Exhaustive conic-pencil bridge

Exact simultaneous-congruence classification gives five, and only five,
primitive pencil types:

| blinded chart | representative | \(\det(\lambda P+\mu Q)\) | double line? | legacy route |
|---|---|---|---|---|
| `P111` | \(\langle x^2+z^2,y^2+z^2\rangle\) | \(\lambda\mu(\lambda+\mu)\) | no | \(R_3=0\), quadratic-component exit |
| `P11_1` | \(\langle x^2+y^2,z^2\rangle\) | \(\lambda^2\mu\) | unique | \(\langle x^2,yz\rangle\) joint-orbit tree |
| `P2_1` | \(\langle y^2+z^2,2xy+z^2\rangle\) | \(-\mu^2(\lambda+\mu)\) | no | \(R_3=0\), quadratic-component exit |
| `P21` | \(\langle y^2,2xy+z^2\rangle\) | \(-\mu^3\) | unique | \(\langle x^2,y^2+xz\rangle\) joint-orbit tree |
| `P3` | \(\langle2yz,2xz+y^2\rangle\) | \(-\mu^3\) | no | \(R_3=0\), quadratic-component exit |

The only coprime identically singular boundary is
\(\langle x^2,y^2\rangle\).  It is composite because
\[
\mathbb C((x/y)^2)\subsetneq\mathbb C(x/y),
\]
and therefore routes to `Q2-E0-A1-B4-D1-N4`.  The other identically
singular Kronecker type has a common linear factor and routes after gcd
extraction.  Hence no sixth internal pencil chart is missing.

This table is the missing bridge between the intrinsic frozen row and the
two legacy unique-double-line normal forms.  The top first-integral
argument covers the three no-double-line charts uniformly.

## 3. Exact universal ranks, kernels, and cokernels

Let
\[
D_{p,q}=(\nabla p\times\nabla q)\cdot\nabla.
\]
The two clean-room verifiers independently construct its coefficient
matrices, their complete right kernels, and complete left kernels.

| chart | \(D:S_2\to S_3\), shape | rank / kernel / cokernel | exact kernel | \(D:S_3\to S_4\), shape | rank / kernel / cokernel | exact kernel |
|---|---:|---:|---|---:|---:|---|
| `P111` | \(10\times6\) | \(4/2/6\) | \(\langle p,q\rangle\) | \(15\times10\) | \(10/0/5\) | \(0\) |
| `P11_1` | \(10\times6\) | \(4/2/6\) | \(\langle p,q\rangle\) | \(15\times10\) | \(8/2/7\) | \(\langle z^3,z(x^2+y^2)\rangle\) |
| `P2_1` | \(10\times6\) | \(4/2/6\) | \(\langle p,q\rangle\) | \(15\times10\) | \(10/0/5\) | \(0\) |
| `P21` | \(10\times6\) | \(4/2/6\) | \(\langle p,q\rangle\) | \(15\times10\) | \(8/2/7\) | \(\langle y^3,y(2xy+z^2)\rangle\) |
| `P3` | \(10\times6\) | \(4/2/6\) | \(\langle p,q\rangle\) | \(15\times10\) | \(10/0/5\) | \(0\) |

Full dual cokernel bases over \(\mathbb Q\) are retained in
`bridge_exact_data_sympy.json`.  Thus the degree-eight Keller identity
forces \(R_3=0\) on `P111`, `P2_1`, and `P3`.  On the other two charts it
forces exactly the two legacy cubic shapes \(L^3\) and \(Lq\), with no
unlisted cubic mode.

When \(R_3=0\), the degree-seven identity gives
\(R_2\in\langle p,q\rangle\), and the third target component has degree at
most two.  The independently hostile-audited quadratic-component theorem
then makes the Keller map an automorphism.  Its exact coordinate/fibre
checker was rerun and passed.

## 4. Division-free map to all frozen pivots

For
\[
\begin{aligned}
p&=\sum_{i=0}^5a_im_i,\qquad q=\sum_{i=0}^5b_im_i,\\
R&=r_0p^2+r_1pq+r_2q^2,\qquad
S=s_0p^2+s_1pq+s_2q^2,
\end{aligned}
\]
the blinded note lists the 45 frozen coefficients explicitly as
\[
c_{15(k-1)+m}=u_k(r_0A_m+r_1B_m+r_2C_m)
+v_k(s_0A_m+s_1B_m+s_2C_m),
\]
where \(A_m,B_m,C_m\) are the convolution coefficients of
\(p^2,pq,q^2\) in the frozen monomial order.  These are polynomial
identities; no source coefficient, target minor, discriminant, branch
parameter, or ramification coordinate is inverted.

For every row point, the unique first nonzero \(c_i\) gives its frozen
stratum
\[
\mathrm C_i:\ c_0=\cdots=c_{i-1}=0,\quad c_i\ne0.
\]
This maps every normal form and every stabilization boundary back to
`C00`--`C44`.  A vanished computational pivot changes only the first
nonzero \(c_i\), unless the ordered intrinsic boundary routing sends the
point to another frozen row.

## 5. General lower terms and the complete joint-orbit assembly

The replay began with two arbitrary cubic components (20 coefficients), all
three arbitrary quadratic components (18 coefficients), and an arbitrary
\(3\times3\) linear part (9 coefficients).  The third cubic component is
then restricted only by the complete degree-eight kernel above.  Every
later source translation or target shear is an invertible equivalence and
merely relabels still-arbitrary lower coefficients.

For `P11_1`, the exact stabilizer of
\(\langle x^2,yz\rangle\) induces only scaling (and the finite involution)
on the pencil line.  The replay includes:

1. both outer critical points finite and finite companion, including open,
   noncritical triple, marked triple, and both \(F/G\) resonances;
2. one outer critical point at infinity and every finite companion,
   including both resonances and all endpoints;
3. companion at infinity, for finite and infinite outer-critical charts,
   including the reciprocal resonance.

For `P21`, the exact stabilizer of
\(\langle x^2,y^2+xz\rangle\) induces the full Borel fixing the marked
double-line value.  Its six joint-orbit rows are:

1. marked critical pair with triple companion;
2. marked critical pair with coincident mixed companion;
3. marked critical pair with distinct mixed companion;
4. unmarked triple;
5. unmarked finite companion \(c\in\mathbb C^\times/\{\pm1\}\), split into
   \(c^2=9\) and its complement;
6. unmarked companion at infinity.

Every item above has a supplied exact verifier and an independently written
hostile verifier.  All were rerun in this audit and passed.

The fail-closed row wrapper `verify_strict.sh` reruns the clean-room bridge,
the top determinant and quadratic-component checks, and every primary and
hostile terminal package.  Its observed final transcript was exactly:

```text
PASS: strict post-freeze Q2-E0-A2-B2-D1-N2 bridge and full legacy replay
```

## 6. Lower raw-rank ledger

Every raw \(E_7\) matrix below has shape \(36\times26\).  The kernel bases
are explicit in the terminal verifiers and were checked both by
\(MK=0\) and by a nonzero independence minor.  The cokernel dimensions
below are therefore exact.

| joint-orbit stratum | rank | kernel dimension | cokernel dimension |
|---|---:|---:|---:|
| generic/open finite companion | 18 | 8 | 18 |
| either finite \(F/G\) resonance | 14 | 12 | 22 |
| noncritical triple | 16 | 10 | 20 |
| marked triple | 8 | 18 | 28 |
| marked or unmarked mixed generic | 18 | 8 | 18 |
| either outer-infinity finite-companion resonance | 14 | 12 | 22 |
| companion-at-infinity nonresonant | 18 | 8 | 18 |
| companion-at-infinity reciprocal resonance | 14 | 12 | 22 |
| rank-one-restriction unmarked \(c=0\) | 16 | 10 | 20 |
| rank-one-restriction unmarked \(c^2=9\) | 14 | 12 | 22 |
| rank-one-restriction marked mixed (both types) | 18 | 8 | 18 |
| rank-one-restriction marked triple | 8 | 18 | 28 |
| rank-one-restriction unmarked infinity | 18 | 8 | 18 |

The repeated entries are not inferred by specialization: each exceptional
rank has its own nonzero maximal minor and complete kernel basis.

At the lower linear stages, the decisive exact maps have:

- open finite-companion \(E_6\): rank \(10\), zero kernel on its ten
  transverse variables, cokernel dimension \(18\);
- \(F/G\) resonance \(E_6\): rank \(8\), with complete displayed solve and
  square-compatibility left-cokernel syzygies;
- outer-infinity generic \(E_6\): rank \(10\), zero kernel on its ten
  transverse variables, cokernel dimension \(18\);
- companion-infinity resonance \(E_6\): constant rank \(8\), with the four
  complete square compatibilities;
- rank-one-restriction open \(E_6\): rank \(10\), zero kernel on its ten
  transverse variables, cokernel dimension \(18\);
- rank-one unmarked triple \(E_6\): constant rank \(10\);
- rank-one unmarked resonance \(E_6\): constant rank \(8\);
- rank-one unmarked infinity \(E_6\): constant rank \(10\);
- rank-one marked mixed \(E_6\): constant rank \(10\);
- rank-one marked triple general \(E_6\): rank \(4\), with every rank-drop
  leaf rebuilt before solving.

The cokernel syzygies at these stages are the displayed square, cube, and
product compatibility certificates.  Each terminal then forces either two
proportional columns or a zero column of the linear part, hence
\(\det L=0\), including every zero specialization of the lower parameters.

## 7. Two methodologically independent checks

The bridge itself was checked twice:

1. `verify_blinded_bridge_sympy.py` uses symbolic polynomial expansion,
   exact rational matrices, right nullspaces, and left nullspaces.  It also
   verifies every one of the 45 coefficient-convolution formulas and writes
   `bridge_exact_data_sympy.json`.
2. `verify_blinded_bridge_pure.py` uses no CAS dependency.  It implements a
   sparse polynomial dictionary, exact `Fraction` arithmetic, and its own
   RREF/nullspace algorithm.  It independently reconstructs every
   \(D:S_2\to S_3\) and \(D:S_3\to S_4\) rank, kernel, and cokernel.

The legacy lower calculation was also checked by two different paths:

- the supplied SymPy verifiers expand determinant coefficients and solve
  exact coefficient matrices;
- independent PARI/GP hostile reconstructions rebuild raw Jacobian
  determinants, maximal minors, kernels, left-kernel compatibilities, and
  zero/rank-drop branches.  The unmarked companion-at-infinity audit adds a
  third, dependency-free sparse-polynomial reconstruction.

This is more than two interpreters evaluating one reduction.

## 8. Smallest gap and repair

The smallest material gap was exactly the one identified by the frozen
audit: the pre-freeze synthesis had no post-freeze proof that its two
normal-form trees covered an arbitrary intrinsic row point, and no
division-free map to `C00`--`C44`.  That was a scope/reproducibility gap,
not a discovered surviving Keller branch.

The repair is:

1. the five-chart intrinsic pencil classification and complete boundary
   routing in `BLINDED_DERIVATION.md`;
2. the chart-to-legacy table in Section 2 above;
3. the polynomial 45-coefficient map;
4. two clean-room exact bridge verifiers; and
5. a fresh replay of every terminal primary and hostile package.

No remaining scope gap or reproducibility failure was found.  The row
therefore passes the post-freeze bridge audit.

## 9. Artifact hashes

```text
11d3d595e07343b322376d2c1411496498ef63e56e4955bda03a30203c01a530  BLINDED_DERIVATION.md
c6592cad695183a6d276c9ff83fbe336d051d5549f40ae17d2394dc9280ee6ac  verify_blinded_bridge_sympy.py
8bb253a2a38a6ded034eeb3080702c1f8ab161c837a1951db28051f23a2bee54  verify_blinded_bridge_pure.py
0604cba75bf113a149c8eb82e8dcfc9d2cdda8fd7c43c669b3f4a836e97d20c9  bridge_exact_data_sympy.json
5716e790da10f5c857e980ca7dc2cfc0d10fa859337bcdaf20ee5782c139968b  verify_strict.sh
```
