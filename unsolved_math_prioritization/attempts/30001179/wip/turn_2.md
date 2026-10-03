# Author turn 2: a separable measure-class free product system

Timestamp: 2026-10-03T06:41:07Z. WIP, not independently verified. Completion estimate: 65%. This turn establishes the proposed measure-class construction. The full tensor-core and continuous-bundle argument will be consolidated separately.

## 1. A sequence measure absorbing finite prefixes

Let γ be the countable product of standard real Gaussian measures. On R×(0,∞)×R^N put the σ-finite measure da·dδ/δ·γ(dz), and map it to sequences by x_k=a+δ2^(-k)z_k, k≥0. Denote its pushforward by μ.

Almost surely,

- a(x)=lim x_k=a;
- d(x)^2=lim_(N→∞) N^(-1) Σ_(k=0)^(N-1) 4^k(x_k-a(x))²=δ².

The first identity follows from Gaussian tail bounds and Borel–Cantelli; the second is the strong law for z_k². Consequently the parameters a and δ are recoverable Borel functions almost everywhere. In particular μ is σ-finite: restricting |a(x)|≤j and j^(-1)≤d(x)≤j gives finite measure and covers its support.

Let C be the Borel set of sequences for which these two limits exist and 0<d(x)<∞. Translation preserves C and d; prepending k arbitrary real coordinates preserves C and multiplies d by 2^k. Every finite tail of a member of C lies in C. Thus prepend gives an actual Borel bijection R^k×C→C.

The law of the tail y=(x_k,x_(k+1),…) is μ after the substitution δ'=δ2^(-k); dδ/δ is invariant. Conditional on y, the omitted coordinates have the independent Gaussian densities

q_k(v;y)=Π_(j=0)^(k-1) [1/(2^(k-j)d(y))] φ((v_j-a(y))/(2^(k-j)d(y))),

where φ is the standard Gaussian density. Therefore, in prepend coordinates,

μ(d(v,y))=q_k(v;y) dv_0…dv_(k-1) μ(dy).

All q_k are finite and strictly positive on R^k×C. Hence μ and Lebesgue^k×μ have the same null sets under prepend. This is an equality of measures with the displayed density, not just a heuristic independence assertion. The density chain rule is q_(k+l)(v,w;y)=q_k(v;prepend(w,y))q_l(w;y).

For each fixed real cut c, a(x)≠c μ-almost everywhere because a has Lebesgue measure. Convergence therefore makes the binary word recording x_k<c or x_k>c eventually constant, with finitely many runs. Individual coordinates equal c only on a null set.

## 2. Ordinal word spaces and concatenation

For α=ωn+m<ω² (n,m nonnegative integers), let Ω_α=C^n×R^m and ν_α=μ^n×Lebesgue^m. For α=0 use a single vacuum point of mass one. This is the canonical coordinate presentation of a word of ordinal length α. Let Ω be their countable disjoint union, with measure ν equal to the sum of the ν_α.

Finite concatenation of words of lengths α_1,…,α_r has length α=α_1+…+α_r<ω². For fixed lengths it is a Borel bijection Π Ω_(α_i)→Ω_α. The only nontrivial coordinate operation is absorbing a finite suffix into the first ω-block of a subsequent word. The preceding prefix lemma proves that concatenation and its inverse preserve null sets. Their canonical unitary on L² is the coordinate pushforward with the positive square-root Radon–Nikodym factor. For instance, C_(k,ω)f(v,y)=q_k(v;y)^(-1/2)f(v,y), interpreted in the target sequence coordinates. The chain rule makes these unitaries associative under every regrouping.

For an open interval I let Ω(I) contain words all of whose coordinates lie in I, with restricted measure ν_I. Put E(I)=L²(Ω(I),ν_I), with the vacuum as distinguished vector. The fibres E_t=E((0,t)), t>0, are separable because all spaces are standard Borel with σ-finite measures and the direct sum has countably many summands. Put E_0=Cω.

## 3. Free factorization at a cut

Fix s,t>0. Ignore the ν-null set containing coordinates or infinite-block limits equal to t. Every word in Ω((0,s+t)) then has a unique finite sequence of maximal monochromatic convex runs for the colors (0,t) and (t,s+t). Each run has order type below ω² and belongs to the corresponding interval word space. Conversely a finite alternating list of nonempty words in the two disjoint intervals concatenates to such a word; the runs are maximal because adjacent colors differ.

Each choice of number of runs, colors and ordinal lengths is a measurable chart. There are countably many charts. On each chart concatenation is measure-class preserving by the prefix lemma, with restrictions exactly imposing the interval conditions. Hence the charts implement a unitary from the pointed Hilbert-space free product E((t,s+t))⊛E((0,t)) to E((0,s+t)). The empty list maps to the vacuum. Translate all labels of the first factor by t to obtain

u_(s,t): (E_s,ω)⊛(E_t,ω)→(E_(s+t),ω).

Translation is measure preserving: in each μ-block it changes only a to a+t; finite coordinates carry Lebesgue measure. The maps at zero time are the canonical identifications. At three or more fixed cuts the same construction merely flattens the same finite colored-run list. The concatenation Radon–Nikodym chain rule proves associativity exactly as operators. Exceptional null sets may depend on a finite collection of cut parameters; no common full-measure set for every real cut is required by the operator identities.

## 4. Remaining full-candidate checks

The relevant tensor image at a partition is the support subspace of words whose interval colors occur in decreasing order without returning to a later interval. Infinite Gaussian blocks have infinitely many rises almost surely (independent pairs give independent symmetric sign tests), so all infinite ordinal sectors should disappear from the partition intersection. The finite-word intersection is the usual time-ordered Fock sector. Its free hull should be exactly the finite-word Fock sector, leaving nonzero infinite-word sectors outside.

Regularity can be checked in a common separable global Hilbert space L²(Ω,ν). Interval support projections are strongly continuous; translation is strongly continuous in the a-variable; and fixed-length concatenation is a fixed global unitary. Finite-grade elementary sections therefore provide a concrete route to continuous multiplication. These details must be written and checked before freezing a complete candidate.
