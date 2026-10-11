# Independent algebra and cocycle derivation for PR48

This derivation was recorded before reading the submitted review conclusions or another fresh family. The source statement and the mathematical helpers were read as text first. The target is ordinary commutator length in the full smooth identity component of a closed orientable four-manifold, not a subgroup, a cover, a conservative group, or a fragmentation norm.

## Universal compression, including intersections and word order

Use `[a,b]=aba^{-1}b^{-1}` and `T(g)=FgF^{-1}`. Suppose `H_i=T^i(H)`, for `0<=i<=m`, commute pairwise for distinct indices. This need not be a direct product: intersections may be nontrivial. All calculations below can instead be performed in the abstract direct product of `m+1` copies of `H` and mapped to `G` by multiplying their commuting images. Thus component language never needs injectivity.

For arbitrary `a_i,b_i in H`, put `c_i=[a_i,b_i]`, `h=c_1...c_m`, `s_i=c_{i+1}...c_m` (`0<=i<m`), and

`A=product_{i=1}^m T^i(a_i)`, `B=product_{i=1}^m T^i(b_i)`, `C=product_{i=0}^{m-1} T^i(s_i)`.

The products use increasing indices. Since distinct images commute, `[A,B]=K=product_{i=1}^m T^i(c_i)`. Also `[C,F]=C T(C^{-1})`. Reordering only different images, its zeroth image factor is `s_0=h`; image `i` (`1<=i<m`) has `s_i s_{i-1}^{-1}`; the last has `s_{m-1}^{-1}`. Since `s_{i-1}=c_i s_i`, the middle factor is exactly `c_i^{-1}`. In particular it is not obtained by commuting the input commutators. Consequently `[C,F]=h K^{-1}` and `h=[C,F][A,B]`. This is a universal group-word proof, not a conclusion inferred from finite permutation tests. For `m=1`, the same formula works; for `m=0`, `h` is the identity and needs no commutators. Reversing `[C,F]`, replacing suffixes by prefixes, or reversing internal suffix order generally breaks the identity.

## Compact smooth support and the stabilized subgroup

Perfectness supplies finitely many commutator factors in the group whose isotopies have compact total support. On `M x R^2`, with `M` compact, finitely many endpoint supports fit inside `M x B_R`. Choose `L>2R` and a compactly supported vector field equal to `L partial_x` on a neighborhood of the full compact corridor traced by `B_R` through time `m`. Its trajectories starting in that corridor are literal translations, so the time-one map sends each `B_R+(jL,0)` to the next for `0<=j<m`. Thus the first `m+1` conjugate support regions are disjoint. The vector field's compact support, together with compact `M`, gives a compact-total-support isotopy for the displacement. This imports smooth perfectness as a theorem; finite algebra cannot establish it. No uniform displacement map independent of the input element is required.

For a smooth isotopy `f_t` on closed `M`, select disk neighborhoods `U,V` covering `S^2` with a smooth cutoff `chi` whose support is compact in `U` and whose complementary support is compact in `V`. Then

`a_s(x,y)=(f_{s chi(y)}(x),y)`,
`b_s(x,y)=(f_s f_{s chi(y)}^{-1}(x),y)`.

The fibers are diffeomorphisms depending smoothly on `(s,y)`, so the inverses are smooth; the base coordinate is fixed. Both paths start at the identity. On the first cutoff plateau `a_s` is identity, and on the second `b_s` is identity. Their total supports fit in compact `M` times fixed compact subsets of the disks. At `s=1`, `b_1 a_1=f x id`. Two commutators per disk yield at most four ambient commutators for this particular inclusion. The isotopy need not satisfy any one-parameter group law. The argument applies to powers by choosing an isotopy for `f^n`; it does not require powers of a fixed displacement.

An arbitrary ambient isotopy cannot be substituted. If `F_t` has generator `V_t`, then the derivative of `z -> F_{tau(z)}(z)` has the extra time term `V_{tau(z)}(F_{tau(z)}z) d tau_z`. For rotations about the third axis, `tau=(1+2xy)/2`, and at `w=(0,1,0)`, `v=(-1,0,0)`, one has `tau(w)=1/2`, `d tau_w(v)=-1`, and `dF_tau(v)+partial_t F_tau d tau(v)=0`. The other tangent direction `(0,0,1)` survives, so the sphere tangent derivative has rank exactly one. The inequality `|2xy|<=x^2+y^2<=1` establishes the global cutoff range. This is a failure of this construction; it is not a theorem that no general fragmentation construction works.

## Homogeneous quasimorphisms, length, and covers

Let `q` be homogeneous with finite defect `D`. Homogeneity gives `q(1)=0` and `q(g^{-1})=-q(g)`. The defect bound for `u g^n u^{-1}`, followed by division by positive `n`, gives conjugation invariance. Therefore

`|q([a,b])|=|q((aba^{-1})b^{-1})|<=D`.

For `k>=1` commutators, the iterated defect bound gives `|q(h)|<=(2k-1)D`; the identity case is treated separately. The ambient four-commutator bound for every power of `f x id` gives `|n q(f x id)|<=7D` and hence zero. This does not say all homogeneous quasimorphisms vanish on the full ambient group. A retraction of that ambient group onto this embedded surface group would carry each of the four ambient commutators to surface commutators, giving width at most four, in conflict with the independently imported positive-genus surface theorem.

For a central extension `1 -> Z -> Gtilde -> G -> 1`, commuting additivity follows from `(az)^n=a^n z^n`: the defect error divided by `n` tends to zero, so `q(az)=q(a)+q(z)`. If `q|Z=0`, it is constant on every fiber and the well-defined quotient function has the same homogeneity and no larger defect. Conversely, a pullback from the quotient vanishes on the kernel since `q(1)=0`. Centrality is essential to the stated sufficiency. This criterion concerns descent of a specified quasimorphism; it does not transfer arbitrary unbounded commutator length from a covering group.

For `H<=G`, allowing more factors gives `cl_G(h)<=cl_H(h)`. A lower bound in `H` alone is insufficient. Likewise an upper estimate `cl_G(f)<=2 frag(f)` has no converse. Vanishing stable length is weaker than a uniform bound on ordinary length, and the stabilized result covers only its inclusion.

For a compact manifold with finitely many components, an identity-component diffeomorphism cannot permute them. This gives the finite product of their smooth identity components. Coordinate projections give the lower bound on commutator length. Padding each coordinate factorization to the maximum length with identity commutators gives the reverse inequality. The equality is exact for finite products of perfect groups. No infinite-product statement is used.

## Signed pushforward and the scope of noninvariance

Let `c(fg,x)=c(f,gx)c(g,x)` and let `psi` have defect `Dpsi`. Require finite integrability of `psi(c(fg,x))`, `psi(c(g,x))`, `psi(c(f,gx))`, and `psi(c(f,x))` with respect to the probability measure `mu`; equivalently the last relevant function must be integrable against both `mu` and `g_*mu`. Then the pointwise defect error is integrable and its integral has absolute value at most `Dpsi`. Changing variables in the `f` term gives exactly

`Q(fg)-Q(f)-Q(g)= integral psi(c(f,y)) d(g_*mu-mu)(y) + E(f,g)`.

The sign is pushforward minus original measure, and the transported function involves `f`, not `g`. Invariance kills the term. Noninvariance alone does not prove that this term is unbounded; a uniformly bounded cocycle integrand would bound it by twice that bound. Thus the precise obstruction is the absence of a supplied uniform bound for the actual cocycle family, rather than a universal impossibility theorem for every averaging construction. A finite action with nonuniform weights can verify the sign and nonzero term but cannot demonstrate unbounded defect for a fixed compact smooth construction.

For a positive-dimensional closed connected smooth manifold, choose a coordinate ball relatively compact in a larger coordinate chart. A compactly supported radial compression and chart translation move that ball to any prescribed sufficiently small chart ball by a smooth isotopy. For each finite `N`, choose `N` disjoint such images; the diffeomorphisms may depend on `N` and the image. Invariance under the full identity component would give `N mu(B)<=1` for all `N`, hence `mu(B)=0`. A finite cover by such balls contradicts probability mass one. This excludes an invariant Borel probability on the full group action. It does not exclude signed measures, non-invariant constructions with compensated defect, or quasimorphisms obtained by other mechanisms.

## Initial result and remaining check

The above algebra is sound under its written hypotheses and yields a partial obstruction to two transfer strategies. The strongest verified outcome is the explicit four-commutator bound on the stabilized subgroup and the exact signed-pushforward defect identity. The original four-manifold existence problem is untouched: there is no sequence with unbounded ambient ordinary commutator length and no nonzero homogeneous quasimorphism on the full target group. Imported smooth perfectness, handle-theorem scope, the surface lower bound, source provenance, original accounting, and literal computations remain to be independently authenticated and reproduced before this family can close.
