# Independent audit of the Haar perturbation counterexample

Date: 2026-10-14 UTC. Target: OWR-720-011 / dataset 30000043 / queue row 1781.

## Verdict

**Accepted for the fixed-index classical single-generator contract.** The audited candidate gives a dyadic wavelet Riesz basis of all of `L²(R)` whose canonical normalized tight family is not the affine orbit of its zeroth canonical vector with the same indices. This audit evaluates the actual inverse square root through a convergent functional-calculus series. It does not infer canonical-tight failure from canonical-dual failure.

The independently reviewed proof is titled “An explicit dyadic Riesz wavelet whose canonical tightening loses its natural affine indexing.” Its original frozen text has SHA-256 `8c943a270c9b35d0cf3ddef2b94de5ec8bbbcb4ec45deca81d28fd2228e522a1` and byte count `7499`. This audit independently checks its operator realization, frame bounds, functional-calculus estimate, physical translation, and scope. The quantitative estimate below is independently derived and strengthens the original proof’s sufficient lower bound of `1/1000`; it does not alter the frozen proof.

This verdict does not establish an arbitrary-reindexing or changed-lattice impossibility, and does not claim historical novelty or a literature-wide present-day status determination.

## 1. Concrete classical realization

Work on `H=L²(R)` and define

- `Df(x)=sqrt(2) f(2x)`;
- `T_k f(x)=f(x−k)`;
- `h=1_[0,1/2) − 1_[1/2,1)`;
- `e_(j,k)=D^j T_k h`, for all `j,k in Z`.

The full Haar wavelet family `{e_(j,k)}` is an orthonormal basis of `H`.

Define on this orthonormal basis

`V e_(j,k) = e_(j+1,2k)`.

The index map is injective, so `V` extends to an isometry on all of `H`, and `||V||=||V*||=1`. Its adjoint is exactly

`V* e_(j,k) = e_(j−1,k/2)` when `k` is even, and `0` when `k` is odd.

For `0<epsilon<1`, put

`A=I+epsilon V`,

`phi=h+epsilon Dh`.

This is an actual bounded, compactly supported, single function on the real line. The physical identity

`T_k D = D T_(2k)`

gives, for every integer `j,k`,

`D^j T_k phi = e_(j,k)+epsilon e_(j+1,2k) = A e_(j,k)`.

Thus this is a classical single-generator dyadic affine system, not merely an abstract representation or a multi-generator family. Negative `j` cause no exception to this identity.

## 2. Full-space frame and its exact frame operator

The Neumann series for `A^(-1)` converges in operator norm for `epsilon<1`. Hence `{A e_(j,k)}` is a Riesz basis of all of `H`.

More directly, for every `f in H`, Parseval's identity for the Haar basis gives

`sum_(j,k) |<f,Ae_(j,k)>|² = ||A* f||²`.

The triangle and reverse-triangle inequalities show

`(1−epsilon)² ||f||² <= ||A* f||² <= (1+epsilon)² ||f||²`.

These are valid frame bounds; no optimality claim is needed.

The frame operator is exactly

`F=AA*=I+epsilon(V+V*)+epsilon² VV*`.

In particular, `F` is bounded, strictly positive, and invertible. Its canonical normalized tight family is

`y_(j,k)=F^(-1/2)A e_(j,k)=U e_(j,k)`,

where `U=F^(-1/2)A` is unitary. Indeed,

`UU*=F^(-1/2) F F^(-1/2)=I`,

and `U` is invertible because both factors are invertible.

The existence of a same-index affine generator would force that generator to be

`eta=y_(0,0)=U h`.

Consequently it is enough to show `U e_(0,1) != T_1 U h`.

## 3. A norm-certified inverse-square-root expansion

Write `t=epsilon` and

`E=t(V+V*)+t² VV*`,

`r=2t+t²`.

Then `||E||<=r`. For `0<t<=1/100`, `r<=201/10000<1`. The scalar binomial expansion

`(1+z)^(-1/2) = 1−z/2 + sum_(n>=2) c_n z^n`

has coefficients `|c_n|=binom(2n,n)/4^n <=1`. It therefore converges in operator norm at `E` and, by continuous functional calculus for the self-adjoint operator `E`, is the positive inverse square root of `I+E=F`. Set

`R=F^(-1/2)−I+E/2`.

Then

`||R|| <= r²/(1−r)`.

Now expand the exact product

`U=(I−E/2+R)(I+tV)`.

Using `V*V=I` and `VV*V=V`, this becomes

`U = I + (t/2)(V−V*) + Q`,

where

`Q = −(t²/2)VV* −(t²/2)(V+V*)V −(t³/2)VV*V + R(I+tV)`.

Hence

`||Q|| <= (3/2)t² + (1/2)t³ + (1+t)r²/(1−r)`.

For `0<t<=1/100`, division by `t²` bounds the right-hand coefficient by

`301/200 + (101/100)(201/100)² / (9799/10000)`

`=11110501/1959800 < 6`.

Therefore the concrete, uniform bound is

`||U−I−(t/2)(V−V*)|| <= 6t²`.

No finite-dimensional truncation or unquantified asymptotic inference is used.

## 4. Physical translation defect

Let `T=T_1` and `L=(V−V*)/2`. The following identities are exact:

- `T h=e_(0,1)`;
- `V e_(0,1)=e_(1,2)=T e_(1,0)=T Vh`;
- `V*e_(0,1)=0`;
- `V*h=e_(−1,0)`.

Thus

`L e_(0,1)−T Lh = (1/2)T e_(−1,0)`.

Because `T` is unitary and the Haar vector has norm one, this leading defect has norm `1/2`. It is important that `T e_(−1,0)` means literal translation by one. It must not be replaced by `e_(−1,1)`, which is a translation by two in physical coordinates.

From the operator estimate above,

`U e_(0,1)−T Uh = (t/2)T e_(−1,0) + Q e_(0,1)−T Qh`,

and therefore

`||U e_(0,1)−T Uh|| >= t/2 − 2||Q|| >= t/2−12t²`.

Choose the explicit rational parameter

`epsilon=1/100`.

Then

`||F^(-1/2)T_1 phi − T_1 F^(-1/2)phi||`

`=||U e_(0,1)−T Uh|| >= 1/200−12/10000 = 19/5000 > 0`.

This proves failure of the required indexed affine identity already at `(j,k)=(0,1)`.

For a scalar witness, put

`g=T e_(−1,0)=2^(-1/2)(1_[1,2)−1_[2,3))`.

The same estimate yields

`Re <F^(-1/2)T_1 phi−T_1 F^(-1/2)phi,g> >=19/5000`.

## 5. Consistency and exclusions

- The operator being evaluated is `F^(-1/2)`, not `F^(-1)`.
- The affine family has exactly one generator and spans all of `L²(R)`.
- The dilation is exactly `Df(x)=sqrt(2)f(2x)` and the translation lattice is `Z`.
- The failure concerns the original natural indices. A different affine indexing or lattice is outside this proof.
- The source's semi-orthogonal positive case does not apply: `phi=h+tDh` and `Dphi=Dh+tD²h` satisfy `<phi,Dphi>=t !=0`.
- `V` commutes with physical dilation `D`, as one checks on every Haar basis vector. Therefore `A`, `A*`, `F`, `F^(-1/2)`, and `U` commute with `D`. The obstruction is precisely local translation covariance, not dilation covariance.
- The proof does not need, and does not assert, that `V` commutes globally with physical translation.

## 6. Primary-source context checked

1. Bownik–Lemvig, *The canonical and alternate duals of a wavelet frame*, ACHA 23 (2007), 263–272: https://pages.uoregon.edu/mbownik/papers/29.pdf . Theorem 1 is about canonical duals, not canonical tightening; its Theorem 3 has a separate example for each lower bound on the number of dual generators. Proposition 3 gives the corrected frame-operator series. None of these is used as a substitute for the inverse-square-root calculation above.
2. Bownik–Jasper–Speegle, *Orthonormal dilations of non-tight frames*, PAMS 139 (2011), 3247–3256: https://pages.uoregon.edu/mbownik/papers/44.pdf . Theorem 4.1 and Remark 4.1, p.3255, formulate canonical-Parseval affine preservation as local commutation of `F^(-1/2)`. Their abstract dilation convention is the inverse of the physical dilation used here. The audit does not import an abstract example without a classical realization.
3. The recovered Frank report, *Approximation of Frames by Normalized Tight Ones*, OWR 1 (2004), pp.529–531, uses inverse-frame-operator notation and cites Han's semi-orthogonal result. Full Han 2003 text was not recovered in this pass; no uninspected statement from it is needed here.

The primary-source checks contextualize the scope. The counterexample's acceptance rests on Sections 1–4, independently of a literature claim that canonical-dual failure implies canonical-tight failure.
