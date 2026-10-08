# Turn 5: thicken the known complex and analyze boundary surgery

## Attempt

Try to convert a known finite S5-CW homotopy sphere X into a smooth action by taking an equivariant regular neighborhood and its boundary. This turns the category gap into a concrete homological surgery problem, but does not solve it.

We do **not** assume without proof that an appropriate smooth equivariant thickening exists. Instead grant the favorable additional hypothesis: a compact connected oriented smooth D-manifold N, with smooth S5 action and an equivariant deformation retraction N -> X, exists, where X is homotopy equivalent to S^n, n>=2, and D>=2n+3. This is a conditional analysis of that proposed route.

If x in N is fixed by a subgroup K, equivariance makes its retraction point K-fixed in X. Therefore every stabilizer in N is contained in a stabilizer in X, and rank-one isotropy passes to N and its invariant boundary. This part of the route would work under the hypothesis.

## Boundary homology calculation

N has integral homology and cohomology Z in degrees 0,n and zero otherwise. Poincaré–Lefschetz duality gives

    H_i(N,boundary N;Z) = H^(D-i)(N;Z),

so the relative groups are Z exactly at i=D,D-n. Because D>=2n+3, these relative degrees and their shifts do not collide with the absolute degree n.

The long exact sequence of the pair now gives

    H_i(boundary N;Z) = Z  for i=0,n,D-n-1,D-1,
    H_i(boundary N;Z) = 0  otherwise.

Details: at i=n, both adjacent relative groups vanish, so inclusion identifies boundary H_n with N's H_n=Z. At i=D-n, the absolute groups on either side vanish, so the relative Z maps isomorphically to boundary H_(D-n-1). The relative fundamental class at degree D maps isomorphically to boundary H_(D-1). Finally H_1(N,boundary N)=H_0(N,boundary N)=0, giving H_0(boundary N)=Z. All other degrees follow from exactness and the same vanishings. Thus the boundary is connected, but has two nonzero intermediate homology groups.

In particular boundary N is not even a homology sphere. The nonequivariant example N=S^n times D^(D-n) has precisely this boundary homology, with boundary S^n times S^(D-n-1), so the obstruction is not an artifact of the calculation.

## Surgery bottleneck

One would have to perform additional S5-equivariant surgeries killing these intermediate groups while preserving the fixed-set conditions of Turn 2 and keeping every stabilizer of rank at most one. An ordinary nonequivariant surgery result is insufficient: attaching whole orbits of handles, their stabilizer representations, framings, and their effects on the various fixed strata must be controlled simultaneously.

No equivariant normal map or surgery obstruction calculation establishing that these steps succeed is supplied. No implication from a vanishing ordinary obstruction to a vanishing equivariant obstruction is claimed. If one obtained a smooth homotopy sphere, identifying or correcting its smooth structure would remain necessary for a claim about a standard smooth sphere.

## Outcome

The raw boundary-of-a-thickening proposal provably fails to produce a sphere even under its favorable existence hypothesis. This identifies a necessary additional surgery task; it is neither a proof that every possible equivariant surgery fails nor a resolution of the original existence question.
