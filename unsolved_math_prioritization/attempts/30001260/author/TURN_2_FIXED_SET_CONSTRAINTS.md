# Turn 2: force the 2-primary fixed-set geometry

## Attempt

Search for a contradiction among the necessary fixed-set dimensions of a hypothetical smooth action on M=S^n with rank-one isotropy. Set the dimension of an empty fixed set equal to -1. We use the classical Smith theorem and Borel dimension formula. For an elementary abelian group E of order four acting on a mod-2 homology sphere Y, the latter is

    dim(Y)-dim(Y^E) = sum over |K|=2 of [dim(Y^K)-dim(Y^E)].

For smooth fixed sets the homological and manifold dimensions agree here. Indeed Smith theory makes a positive-dimensional fixed set a connected closed mod-2 homology manifold with precisely sphere homology, while in dimension zero it consists of two points. A closed positive-dimensional component cannot have the homology of a point, by its mod-2 fundamental class. The formula also applies to the quotient actions used below. See Hambleton–Yalçın, *Homotopy representations over the orbit category*, Section 5, Definition 5.1(ii), for the precise subgroup-quotient formula.

## Necessary dimension theorem

Let a=dim M^<(12)(34)> and b=dim M^<(12)>. Rank-one isotropy forces M^E_A=M^E_B=empty. Conjugacy and the formula give

    n+1 = 3(a+1),
    n+1 = 2(b+1)+(a+1).

Subtracting shows a=b=r, with r>=0, and

    n = 3r+2.

In particular all involutions have nonempty fixed sets of the same dimension. Dimensions 0 and 1 are excluded by these equations alone. No claim that every n=3r+2 is realizable is made.

There is also a C4 consequence. Take c=(1234), z=c^2=(13)(24), s=(13), and P=<c,s>, a Sylow D8 subgroup. On F=M^<z>, the quotient P/<z> is a Klein four group. Its three order-two subgroups have preimages <c>, <z,s>, and <z,cs>. The latter two are Klein four groups, so their fixed sets are empty. The whole P-fixed set is empty as well. Borel's formula for this quotient action therefore gives

    r+1 = (dim M^<c>+1)+0+0.

Thus M^<c> has dimension r and is nonempty. Its inclusion into F is an inclusion of closed smooth submanifolds of equal dimension, and is open in F. If r>0, Smith theory makes F connected; hence the inclusion is equality. If r=0, both fixed sets have exactly two points, so equality still holds. Therefore

    M^<c> = M^<c^2>

for every four-cycle c.

## Differential consequences

At every involution fixed point the normal codimension is n-r=2r+2. An involution acts by -I on its normal space. Consequently it preserves the orientation of M. In particular all transpositions preserve orientation, and since they generate S5, the entire hypothetical action is orientation preserving.

On the common fixed manifold F=M^<c>=M^<c^2>, the normal action of c squares to -I. Its derivative therefore gives a complex structure J on the real normal bundle, of complex rank r+1. This is an honest local bundle constraint on a smooth realization, not a global S5 representation.

## Why the attempted contradiction does not close

All these equalities are compatible with a local D8 rotation representation: m copies of the three-dimensional rotation representation have ambient sphere dimension 3m-1 and every nontrivial cyclic 2-subgroup fixed sphere dimension m-1. Taking m=r+1 meets the equations and the complex normal-rank constraint. Turn 3 makes common Sylow dimensions explicit. Thus these necessary conditions do not contradict existence.

No assumption of prime-power or cyclic isotropy was used. Mixed-prime rank-one stabilizers allowed by the original problem have not been excluded. No conclusion for arbitrary nonsmooth topological actions is extracted from the differential argument.
