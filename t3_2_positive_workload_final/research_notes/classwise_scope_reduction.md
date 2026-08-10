# Classwise meaning of the T3-2 scope

The inherited phrase “dynamically active” is ambiguous. The only classwise
reduction compatible with the three-coordinate atlas is the following.

Fix a closed irreducible population class $\Gamma$.

- A species is **dynamic on $\Gamma$** when its population coordinate is not
  constant on $\Gamma$. Bounded-but-varying and tight infinite-support
  coordinates count as dynamic; “dynamic” must not mean merely unbounded.
- A linkage is **active on $\Gamma$** when some channel in it is enabled at
  some state of $\Gamma$.

If $X_i\equiv m_i$ on $\Gamma$, every channel enabled anywhere on
$\Gamma$ has $\zeta_{e,i}=0$, since closure would otherwise put a state with
a different $i$-coordinate in $\Gamma$. If one channel in a weakly
reversible linkage is enabled, its actual target is present after firing and
a directed target path can be lifted reaction by reaction. Hence every
complex of that linkage is physically reachable with the same residual, and
the constant coordinate has one common stoichiometric value throughout the
linkage. Its falling-factorial contribution is a fixed factor that can be
absorbed into the positive rate constants, after which the coordinate can be
deleted.

A linkage having no enabled source on $\Gamma$ is deleted. After projecting
constant species, two previously distinct linkages may share a projected
complex. Their union is then strongly connected and should be merged; labels
and parallel rates remain distinct. Projection and merging do not increase
the number of linkage classes.

An exact classwise theorem should therefore say:

> After deleting coordinates constant on the fixed closed irreducible class,
> deleting linkages inactive on that class, and merging projected linkages
> that share a complex, the reduced network has at most three species and at
> most two linkage classes.

For a simpler but narrower manuscript statement, require from the outset that
the whole network has at most three species and at most two linkage classes.
