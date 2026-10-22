# Source/status gate: Sum-Free Subsets of [N]^d

Checked 2026-10-20 UTC. Queue position supplied: 1823; dataset ID 98; GREEN-006.
Scope: source recovery only. No proof attempt, queue edit, or publication performed.

## Gate decision

**TARGET RECOVERED; NEW ALL-DIMENSION PREPRINT FOUND; DO NOT USE STALE OPEN STATUS.** The asymptotic-density target has a directly matching 2026 primary preprint. This source gate verifies its identity and stated theorem, not the correctness of its proof. An exact finite-cardinality interpretation is stronger and is not settled by the theorem inspected. Any subsequent acceptance report must distinguish these scopes and disclose the preprint's submitted status.

## Exact original target

Ben Green, *100 Open Problems*, Problem 6, PDF page 5:

“Fix an integer d. What is the largest sum-free subset of [N]^d?”

[Author-hosted problem collection](https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf).

The collection defines [N]={1,...,N}. Its comments single out c_d=limsup_(N→∞) f_d(N)/N^d as the main aspect, with d fixed and f_d(N) the maximum cardinality. They describe coordinate-sum slices and credit the known constants c_1=1/2 and c_2=3/5. The current December-2025 revision records Lepsveridze–Sun's d=3,4 result, not d=5.

The local problem record matches the question exactly. Its August-2026 triage says arbitrary fixed d remains open, but omitted the May/June-2026 paper below. That catalog assessment is not reliable current-status evidence.

## Definitions and non-substitution rules

Use positive integers d,N and ordinary componentwise addition in Z^d. A set A is sum-free precisely when (A+A)∩A is empty: there are no x,y,z∈A with x+y=z. No distinctness hypothesis is imposed; x=y is included. This convention is explicitly used in the introductions of both primary research papers below.

Do not replace this problem with sum-freeness modulo N, sum-free sets in finite groups, the Boolean cube with XOR addition, counting the number of sum-free subsets, or merely the continuous measurable problem. “Largest” means maximum cardinality, not inclusion-maximality. A result with fixed d and N→∞ does not automatically give a uniform growing-d estimate.

## Current all-dimensional source

Peter Keevash and Jeck Lim, *On the largest sum-free subset of the lattice cube*, [arXiv:2605.00816v2](https://arxiv.org/abs/2605.00816v2), submitted May 1, 2026; revised June 16, 2026. [Versioned full text](https://arxiv.org/html/2605.00816v2).

Their convention is [n+1]={0,...,n}. Theorem 1.1 bounds every sum-free subset by c_d^* n^d+O(n^(d−1)), for each d≥1, where

c_d^* = max_(0≤u≤d) Vol({x∈[0,1]^d : u≤sum_i x_i<2u}).

The matching slice construction determines the limiting density in every fixed dimension. This does not assert an exact finite-n maximum, uniqueness, or classification of all extremizers. Their method uses discrete slice couplings and linear-programming dual weights. Appendix A includes a numerical-verification component; no execution or independent proof audit was performed here.

Publication check: [Jeck Lim's author page](https://sites.google.com/view/jecklim) currently labels this paper “submitted”. [Peter Keevash's author bibliography](https://people.maths.ox.ac.uk/keevash/) lists its arXiv identifier without journal details. No journal acceptance was verified. Report it as a submitted preprint, not a peer-reviewed publication.

## Convention bridge and exact-versus-asymptotic boundary

This is a boundary comparison, NOT a translation of sum-free sets. Translating a sum-free set need not preserve sum-freeness. The cubes {1,...,N}^d and {0,...,N}^d differ by (N+1)^d−N^d=O_d(N^(d−1)) boundary points. Intersecting any sum-free set with the smaller cube preserves sum-freeness. Thus their maxima differ by at most that boundary count, so the leading constants agree. The inspected theorem and slice lower bound give the intended positive-grid asymptotic f_d(N)=c_d^*N^d+O_d(N^(d−1)). This scope comparison does not establish exact values of f_d(N).

Accordingly: a task targeting Green's highlighted asymptotic constant should audit the Keevash–Lim theorem before attempting a new solution; a task demanding exact finite maxima must be explicitly marked as the stronger residual question. No claim that all such exact questions remain open has been established by this search.

## Earlier published result and version discrepancy

Saba Lepsveridze and Yihang Sun, *Size of the Largest Sum-Free Subset of [n]^3 and [n]^4*, IMRN 2026(9), rnag081, [publisher record](https://doi.org/10.1093/imrn/rnag081), published April 24, 2026. The journal abstract specifies d=3,4. The current [arXiv:2311.18289v3](https://arxiv.org/abs/2311.18289v3), December 16, 2025, agrees. Its Theorem 1.1 has error O(n^(d−1/2)) in those dimensions. The earlier indexed title includes d=5, but that is not the current theorem or journal title. Do not credit a published d=5 result to this paper based on old metadata. The exact reason for the version change was not established.

## Retrieval verification and limitations

Downloaded and text-extracted the three versioned/author-hosted PDFs below. The original question was checked against Green's PDF and the current theorem against Keevash–Lim v2 pages 1–2; definitions and Lepsveridze–Sun's Theorem 1.1 were checked on its v3 pages 1–2. HTML extracts independently corroborate the current theorem and definitions. No proof validation, exhaustive citation search, or independent numerical replay is claimed.

Private source PDFs and extracted text are retained separately and are not publication payloads. Verified PDF metadata:

- Green: 839479 bytes; SHA-256 e06971245914947f152550dee59bbb29fe0e798f0c51b2bc2557f824c2f9a44a.
- Keevash–Lim v2: 469187 bytes; SHA-256 792fe630e8162b7d017d4efd81991a4f4a537e497ad59a4906cdb21499d84fe8.
- Lepsveridze–Sun v3: 664718 bytes; SHA-256 c6a05c9eebe70670164caa6f20fa87badbf9bddc1da80cda5569633d05f27da9.

The source gate contains authored synthesis and public references only; the dataset extracts, full source documents, and coordination material remain private. Nothing has been committed or published.
