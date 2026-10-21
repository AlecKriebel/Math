# Geometry adversarial controls and exact checks

The submitted induction has the correct codimension at every step. Start with f:S^1 -> R^2. Given f:T^(d-1) -> R^d and a global unit normal nu, put

F(p,phi)=(f(p)+epsilon cos(phi) nu(p), epsilon sin(phi)) in R^(d+1).

Orientability supplies nu: an oriented basis for tangent space followed by the positive normal agrees with the fixed ambient orientation. A hypersurface of codimension one has a real line normal bundle, so this prescription is a nowhere-zero global section. No orientation of a higher-rank unspecified normal bundle is used as a substitute for trivialization. In R^(d+1), the normal bundle is explicitly spanned by (nu,0) and (0,1), giving a trivial rank-two disk bundle. Compactness supplies a uniform positive tubular radius, and choose epsilon below it.

In tubular coordinates F is exactly the restriction (p,u,v)=(p,epsilon cos phi,epsilon sin phi). Its angular derivative is nonzero since (-sin phi,cos phi) never vanishes; tubular coordinates separate p and the two normal coordinates, proving injectivity and immersion. Compact source upgrades this to an embedding. A global unit normal to the next hypersurface is (cos phi nu(p),sin phi). For p variations its dot product with dF is zero because nu dot df=0 and nu dot dnu=0; for the phi variation the cosine/sine terms cancel. Its norm is one. The next stage is two-sided explicitly. Thus no unsupported orientability or trivialization step is hidden in the induction.

Falsifier 1: the product torus in R^(2d) does not provide the required collar in R^(d+1). Rejected; the submitted boundary-of-trivial-disk-bundle induction supplies the exact ambient dimension.

Falsifier 2: a compact T^n cannot embed as an open n-dimensional submanifold of R^n by invariance of domain. Rejected as an attack on the actual proof: only T^(n-1) is embedded into R^n. Its collar is open and noncompact in its transverse direction, of dimension n.

Falsifier 3: two-sidedness is not true for all arbitrary hypersurfaces without hypotheses. The submitted hypersurface is compact orientable torus in orientable Euclidean ambient space. Those hypotheses provide the normal line orientation and global normal. The induction additionally provides one by formula.

Falsifier 4: global real-valued angular coordinate functions do not exist. Rejected as an attack: invariant angular vector fields and invariant 1-forms do exist on the Lie group torus and commute. Local lifts of angles are enough for coordinate charts. Diffeomorphism preserves their brackets, so the pushed frame commutes even though ambient Cartesian coefficients vary.

Falsifier 5: cutting off at a collar boundary could leave derivative jumps or a torsion distribution. Rejected because the tensor is exactly zero on both entire open end strips. Its support is inside the compact image of T^(n-1) x [-3/4,3/4], itself strictly inside the open collar. Each point outside the collar has a neighborhood disjoint from that support. The extended tensor is identically zero there; all derivatives vanish, and torsion vanishes by locality. The angular frame need never be extended outside the collar.

Falsifier 6: realizing only a closed hypersurface does not give a nonempty open domain. Rejected: the central strip T^(n-1) x (-1/4,1/4) maps to a nonempty open subset of R^n. It is connected. Any small connected coordinate box contained in it works if a coordinate domain is desired.

Dimension-one boundary case has no torus step. Nijenhuis torsion is alternating in two vector arguments, so every endomorphism field in dimension one is Nijenhuis. A scalar smooth bump equal to the specified real scalar on an interval gives compact support, including zero scalar.

These are analytic controls, not a finite-topology extrapolation. All dimensions follow from the exact induction and tubular-neighborhood theorem. No candidate edits were made.
