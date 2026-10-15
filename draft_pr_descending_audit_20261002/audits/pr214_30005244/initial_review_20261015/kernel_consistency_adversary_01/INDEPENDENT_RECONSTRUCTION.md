# Independent kernel and consistency reconstruction

Recorded 2026-10-15T07:57:38Z, before reading any inherited independent-review, final-disposition, or source-audit verdict. The frozen candidate itself and the two primary source texts were read. This is an adversarial verification of the stated conditional theorem, not a new author proof attempt or a full-source-scope verdict.

## Claim under examination

For a fixed complex frequency k and bounded measurable support O, with cubic center-sampling masks satisfying |O_h symmetric-difference O| -> 0, the zero-diagonal static matrices, embedded by cellwise constants in whole-space L2, converge strongly to compression of pv K0; the dynamic remainder matrices converge in Hilbert-Schmidt norm to the compressed remainder kernel. The uniform static norm and form interval come from the published static lattice theorem. The exact claims to test are the normalization, absence of an unaccounted self term, validity for arbitrary grid translations, strength of the mask assumption, actual matrix embedding, and the two convergence modes. Abstract spectral consequences are outside this family's main remit.

## Direct radial calculation

Put g(r)=exp(ikr)/(4 pi r), e=x/r. The radial Hessian is g'' ee^T +(g'/r)(I-ee^T). Substituting g' and g'' gives

    K_k(x) = exp(ikr)/(4 pi r^3)
       [(1-ikr-k^2 r^2) I +(k^2 r^2+3ikr-3) ee^T].

Thus K0=(I-3ee^T)/(4 pi r^3), exactly the d=3 kernel in CDN (3.41), since nu_3=4 pi/3. Expanding the I and ee^T scalar coefficients separately gives

    R_k=K_k-K0
       = -k^2 (I+ee^T)/(8 pi r) - i k^3 I/(6 pi) + O(r).

There is no r^-2 term or ee^T constant term. For each fixed k in C and finite L, |R_k(x)|_F <= C(k,L)/r for 0<r<=L. Negative imaginary k causes exponential growth at infinity, but this local bound on a bounded difference set remains valid. No whole-space nonzero-frequency lattice operator is needed.

## Distributional normalization

Off zero, -D_i D_j(1/(4 pi r)) equals K0_ij. Spherical principal value gives a homogeneous distribution of degree -3, so its difference from the distributional Hessian is an order-zero distribution supported at zero. Reflection and coordinate-permutation symmetry force c I delta_0. Taking the matrix trace gives -Delta(1/(4 pi r))=delta_0 while trace pv K0=0, hence 3c=1. Consequently the distributional volume operator is pv K0+I/3 plus the ordinary weakly singular R_k kernel. The static Fourier multiplier is xi xi^T/|xi|^2-I/3 with eigenvalues -1/3,-1/3,2/3. The dynamic distributional delta coefficient is unchanged because g_k-g0 is locally Lipschitz with first radial expansion constant +O(r), and its second derivatives have only locally integrable O(1/r) singularities.

## Static translated-grid consistency

For any radial compact cutoff chi, every finite sum sum_{j!=0} h^3 K0(hj) chi(hj) vanishes exactly. Reflections kill mixed entries. Permutations make the three diagonal sums equal. Their sum is zero termwise. Grid translations cancel in center differences, so the argument is independent of a_h. The identical continuum radial integral vanishes. This controls the omitted diagonal without assuming that a bare conditionally convergent infinite sum has a prescribed value.

For smooth compact phi, subtract phi(x_m) in both near terms. Their norms are at most C ||grad phi||_infinity delta, because h^3 sum_{0<|hj|<=2delta}|hj|^-2 <= C delta. The integer-radius shell count O(j^2) proves the latter uniformly in h; if 2delta<h the sum is empty. With delta fixed, all remaining center sums are ordinary uniform Riemann sums on every bounded set, of smooth compactly supported functions of the integration variable. Continuity of the continuum convolution handles values within a cell. Only after this limit is taken is delta sent to zero.

For |x|>R beyond twice the smooth input support, the lattice sum is absolutely finite and bounded by C(1+|x|)^-3, using a uniform bound on h^3 sum |phi(x_n)|. The same bound holds for the integral. Its squared tail integral is O(R^-3). Thus local convergence promotes to whole-space L2 convergence. The source-provided uniform static norm extends this dense-set argument to all L2. No norm convergence of the static operator is claimed or required.

## Measurable masks and the dynamic embedding

For u in L2, ||(M_h-M)u||_2^2 is the integral of |u|^2 over O_h symmetric-difference O, and tends to zero by absolute continuity. Products of bounded strongly convergent factors give M_h D_h M_h -> M D M strongly. No boundary regularity or sampling of u is used. Boundedness of O implies the occupied cubes lie in a common bounded box for small h.

The dynamic kernel constant on Q_m x Q_n, equal to R_k(x_m-x_n) for m!=n and zero for m=n, integrates a cellwise constant input to sum_n h^3 R_k(x_m-x_n)u_n. It annihilates the orthogonal complement of cellwise constants. Consequently this is the actual zero-diagonal DDA matrix, not a cell-averaged replacement.

On |x-y|<delta, centers satisfy |x_m-x_n|<delta+sqrt(3)h. The squared kernel integral is at most

    C h^6 #I_h sum_{0<|hj|<delta+sqrt(3)h}|hj|^-2
       <= C (h^3 #I_h)(delta+h) <= C'(delta+h).

The continuum squared remainder integral there is at most C delta. On the complement, after h<delta/(2sqrt(3)), R is bounded uniformly continuous and all same-cell pairs have already disappeared from that complement. Center values converge uniformly, and the two-variable indicator products converge in L2 because their difference is supported in (O_h triangle O)xB union Bx(O_h triangle O). This proves Hilbert-Schmidt convergence by first h->0 and then delta->0. The proof applies also when O is merely measurable subject to G, or is null, and when occupied cells are empty at some meshes.

## Established input and provisional result

CDN's polynomial/cancellation assumptions hold entrywise for p_ij(x)=(delta_ij |x|^2-3x_i x_j)/(4 pi). The Ewald proof provides the bounded lattice operator; its real even symmetric matrix kernel makes it selfadjoint. Its numerical-range closure is an interval containing [-1/3,2/3]. Compression to any finite index set uses only boundedness and the form bound, not source assumptions about geometric regularity or a full-domain instability assertion.

No kernel or consistency gap has been found in this independent reconstruction. Remaining work: check exact algebra with a separate symbolic control; inspect page images for the primary equations; construct independent finite controls for radial shells, translation, h scaling, and the actual dynamic matrix embedding. This is not a novelty conclusion, nor an assertion that the source's full pathological-support target is settled.
