# Independent geometric reconstruction

Written from the primary-source baseline and the mathematical portions of TURN_1 through TURN_5, before opening candidate code, numerical outputs, status JSON, final files, history, or old reviews. This family tests the complex-geometric prerequisites rather than treating curvature, positivity, or hyperbolicity as a substitute for the original bounded-function question.

## 1. Geometry of the separated hypersurface

Let `s=f1(z1)+f2(z2)+f3(z3)`, with all three functions nonconstant and entire. Since a derivative is not identically zero, its zero set is discrete and locally finite. Thus

`Sing(V) subset Crit(f1) x Crit(f2) x Crit(f3)`

is locally finite. `V` has pure complex dimension two. A repeated local hypersurface factor would force `ds` to vanish at every point of a two-dimensional component, impossible for the displayed discrete set. Consequently the hypersurface is reduced; its isolated singularities have codimension two. The hypersurface normality criterion applies. With the explicitly credited Rubel-Squires-Taylor irreducibility theorem, `V_reg` is connected and dense. The irreducibility theorem is a genuine dependency, corroborated in Demailly's primary paper, rather than a new argument of this review.

None of this yields a positive cotangent bundle or a hyperbolic metric. With `f3(z3)=z3`, the map

`(x,y) -> (x,y,-f1(x)-f2(y))`

is a biholomorphism `C^2 -> V`, giving a global tangent and cotangent frame and many entire curves. On the quadratic cone `z1^2+z2^2+z3^2=0`, blowing up the vertex has exceptional conic `E` isomorphic to `P^1`. The restriction of the smooth resolved surface's cotangent bundle surjects onto `Omega_E=O(-2)`. An ample vector bundle has ample quotient bundles, so that cotangent restriction is not ample. This is an exact geometric obstruction to an unjustified universal positivity claim. The candidate makes no such claim; it uses regular loci and density instead.

## 2. Polynomial pullback as a finite spectral construction

For a polynomial map `p=(P1,P2,P3)` with nonzero degrees, every fiber consists of a fixed finite number `D=product deg(Pi)` of points counted with multiplicity, and p is surjective. Given ambient entire F, the finite fiber multiset of its values defines a characteristic polynomial. To check its global coefficients independently, regard

`C[z1,z2,z3]/(P1(z1)-w1,P2(z2)-w2,P3(z3)-w3)`

as a free rank-D module in the standard bounded-degree monomial basis. Multiplication by each zj is a commuting matrix with polynomial coefficients in w. Entire F can be evaluated on these matrices: uniform bounds on compact w-sets and the absolutely convergent scalar Taylor series imply normally convergent matrix evaluation. Its characteristic coefficients are ambient entire and are the elementary symmetric functions of F on each multiplicity-counted fiber, including collisions. A bound M on the full pullback gives `|Hk| <= binom(D,k) M^k` on the base hypersurface. Base Liouville makes the coefficients constant. The connected pullback then has its F-values in a fixed finite root set and hence a single value. The reverse direction is composition and surjectivity. This checks the ambient quantifier and ramified boundary in TURN_1 without selecting global inverse branches.

## 3. Finite rational quotient and the ultra-Liouville hypothesis

Suppose the first input is `R(exp x)`, where R is nonconstant Laurent polynomial, and the other inputs are arbitrary nonconstant entire g and h. The quotient

`Y={(u,y,z) in C* x C^2 : R(u)=-g(y)-h(z)}`

is locally covered by the first-coordinate exponential map. Its regular locus is connected by the same irreducibility dependency. Let d be the degree of the rational map R on `P^1`. Remove from the target C the finite set B containing all finite critical values and finite values at u=0 and u=infinity. The excluded subset of `C^2` is the finite analytic union

`A=union_{b in B}{g(y)+h(z)=-b}`.

It is proper because neither g nor h is constant. Off A the quotient projection has exactly d distinct u-roots in C*, all with nonzero R' and therefore all regular. Its local inverse branches are holomorphic. A subset `R(u)=b` cannot contain a relatively open two-dimensional piece of Y: its u-values lie in a finite set, leaving a one-dimensional equation `g(y)+h(z)=-b`. Thus the off-A covering portion is dense in `Y_reg`, including near an isolated singular point before regularization.

For a bounded continuous plurisubharmonic v on `Y_reg`, the finite fiber maximum off A is locally the maximum of d plurisubharmonic functions. It is bounded, extends plurisubharmonically across A, and is constant on `C^2` by the linewise subharmonic Liouville theorem. The maximum is attained on a finite nonexceptional fiber. Density and continuity place every v-value below that maximum, so the connected-manifold maximum principle forces v constant. This proves **ultra-Liouville**, exactly the stronger hypothesis needed by Lin-Zaidenberg Theorem 1.6. The exponential lift over `Y_reg` is a connected regular Z-cover. The theorem makes that lift Liouville, and density recovers the whole original hypersurface. Polynomial first-coordinate phases are handled by the preceding finite pullback.

This argument is insensitive to singular values or growth of g and h, because finiteness comes from R. It does not apply when R is replaced by an arbitrary entire function of u. The finite attained maximum is the central mechanism, not an infinite-fiber supremum.

## 4. Two-input slice route and degeneration control

For `R1(u)+R2(v)=c` in `(C*)^2`, each Ri is a rational map of finite degree di. Outside sums of their finite branch/end-point values, the t-projection `t=R1(u)` is a product covering whose disjoint puncture sets independently generate the two transitive monodromy images. It is therefore connected. Critical-gradient failure would require c in the excluded sumset, and hence a generic curve is smooth and connected. All omitted t-fibers are finite and no curve component can lie in one, so connection of the open covering portion implies connection of the full algebraic curve.

On its compact normalization, u and v are meromorphic of degrees at most d2 and d1. If all puncture valuation vectors were rank at most one, some nonzero integral `(a,b)` would kill them. Then `u^a v^b` has zero divisor and is constant on the compact curve. Neither exponent can be zero, since neither coordinate is constant. The curve lies on a one-dimensional torus coset, parametrizable as `(alpha t^r,beta t^s)` with nonzero r,s. Substituting into the separated Laurent equation forces the level c to be the sum of the two Laurent constant terms. Away from that extra level, two independent valuation vectors exist; their determinant bounds the exponential-lift component count by `2 d1 d2`. Each lifted component is an abelian cover of an ultra-Liouville algebraic curve.

The isotopy in TURN_2 fixes the first branch/end-point neighborhoods, translates the second neighborhoods, and fixes infinity. Its two rational lifts starting from identity extend across each finite local model `q -> q^m` and fix 0 and infinity. Their exponential lifts yield local topological component labels; no properness of the exponential family is silently assumed. Local holomorphic sections provide the component-constant F-values. The elementary symmetric functions of those finitely many values are bounded holomorphic in the arbitrary third variable off a discrete exceptional set, extend across it, and are constant. Local openness of `R1(exp x)` establishes density at exceptional levels even at critical x. This closes the exceptional-fiber step.

The zero level of two simple exponentials demonstrates the necessary caution: `e^x+e^y=0` is a disjoint union of parallel affine lines, whereas nonzero levels have the established connected Liouville behavior. The candidate's density and finite-root argument explicitly bridges this degeneration; it never claims that all exceptional fibers retain the generic number of components.

## 5. Normal monodromy pullback under virtual nilpotence

For an entire f whose restriction off a finite singular-value exclusion S is a covering, take the regular cover of `B=C\S` corresponding to the kernel of the inverse-monodromy action. This is a topological normal closure, which may have infinite degree. A connected component of its pullback by `H(y,z)=-g(y)-h(z)` over `U=H^{-1}(B)` is regular with deck group equal to a subgroup of the monodromy image G. U is a connected complement of an analytic hypersurface in `C^2`, so bounded continuous plurisubharmonic functions extend to `C^2` and U is ultra-Liouville.

If G is virtually nilpotent, so is its subgroup. Taking a finite-index nilpotent normal core produces a finite intermediate cover; finite fiber maxima show that this intermediate space is still ultra-Liouville. Lin-Zaidenberg then applies to the remaining nilpotent cover. The original nonregular pullback is connected after a proper analytic subset is removed from the irreducible full hypersurface. Path lifting shows each chosen normal-cover component surjects onto it, so constancy descends. Dense continuation handles all exceptional values.

For `f=exp(exp z)`, inverse labels `(k,n)` can be chosen so a loop around zero sends `k -> k+1`, while a loop around one increments n only at k=0. Conjugation produces independent integer lamps at every k. The generated faithful image is `Z wr Z`. Any finite-index subgroup contains positive powers `a^r,b^s`. Its iterated commutators have lamp vector `s(shift_r-I)^m delta_0`; the coefficient at mr is nonzero for every m. Hence no such subgroup is nilpotent. This excludes this route's hypothesis, not Liouville itself. No theorem about all solvable or amenable covers has been substituted for the cited nilpotent theorem.

## 6. Independent divisor proof of double-exponential character rigidity

Put `V2={sum exp(exp zj)=0}` and `Y={sum exp uj=0}`. Under the coordinate exponential covering, V2 maps onto `Y*=Y\union Dj`, where `Dj={uj=0}`. Y is a smooth surface with global parametrization by the Demailly curve times C:

`(a,b,t) -> (a+t+pi i,b+t+pi i,t)`, `exp a+exp b=1`.

A Dj is smooth because another exponential derivative is nonzero. At the intersection of two Dj's, the remaining exponential derivative is nonzero and the two vanishing coordinates are local coordinates. There is no triple point, since three zeros give sum 3. Thus the coordinate divisors have simple normal crossings. Points obtained by permuting `(0,log 2,log 3+pi i)` give isolated meridians with the three basic winding vectors. Those meridians verify that the exponential pullback is connected.

Let bounded F have a character under logarithmic deck translations. If nonzero, boundedness under positive and negative powers forces its character to be unitary. Write the three weights uniquely as `alpha_j in [0,1)`. Removing the automorphy factor gives a single-valued holomorphic function

`H(u)=exp(-sum alpha_j zj) F(z)`, with `|H| <= M product |uj|^{-alpha_j}`.

Near a single divisor the coefficient of a negative power `s^{-m}` is bounded by `C r^{m-alpha}`, which tends to zero for every integer m>=1. At a crossing, two Laurent integrals give the corresponding product bound; all negative powers vanish. Uniform parameter estimates give joint holomorphic extension. This extends H to all of Y even for irrational character weights, without a finite-cover assumption.

On every entire common-translation line in Y, H is entire in t and for large |t| is bounded by `C|t|^{-sum alpha_j}`. If any weight is positive, it tends to zero, so one-variable Liouville makes it zero on that line and hence everywhere. If all are zero, H is bounded on Y and the Demailly curve times C is Liouville, making H constant. Therefore every nontrivial character admits only zero and the trivial character admits constants.

On a finite-dimensional space of bounded deck translates, the deck transformations are commuting invertible isometries for the supremum norm. An eigenvalue off the unit circle contradicts bounded powers; a nontrivial Jordan block contradicts the polynomial growth of powers. Simultaneous diagonalization reduces to the verified character statement. Exponential polynomials have finite-dimensional translation span, including all polynomial coefficients and repeated exponent vectors, and hence are included.

The exact gap is the **unrestricted infinite-dimensional deck orbit** of an arbitrary ambient entire F. A bounded representation of the abelian deck group need not have a complete spanning family of eigenvectors. Nothing here produces a finite maximum on the non-ultra-Liouville quotient. A source theorem does not close that gap.

## Source qualifications

The 1979 C. R. announcement already covers two simple exponential inputs and arbitrary third meromorphic input. These results deserve direct credit, as in the candidate. The Lin-Zaidenberg theorem requires ultra-Liouville; Remark 1.9.2 expressly gives Demailly's curve as Liouville but not ultra-Liouville. The quoted Green-function construction is consistent with that remark: if G is positive Green, `exp(-G)` is bounded continuous subharmonic, extending as zero at its pole. On the punctured locus its Laplacian is nonnegative; continuity and local boundedness allow subharmonic removal at the pole. Restriction to a dense divisor complement remains nonconstant.

A metadata correction to the immutable source-first baseline: the class-B paper lists authors **Lasse Rempe-Gillen and Dave Sixsmith**. The baseline's reversed abbreviated names do not affect its theorem routing or hypotheses. The review fetched the stated paper and exact hash throughout.

All original claims remain universally quantified. The strongest verified candidate theorem is the conjunction of the one-Laurent-exponential-input result and the virtual-nilpotent-monodromy criterion, plus the finite-orbit obstruction on V2. These are valid partial affirmative mechanisms. They are neither a counterexample nor a complete original-problem resolution.
