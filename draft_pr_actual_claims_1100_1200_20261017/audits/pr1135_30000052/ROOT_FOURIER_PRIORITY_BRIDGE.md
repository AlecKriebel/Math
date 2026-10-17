# Root Fourier proof using classical tools

This is a NEW audit application of classical tools, not a verified earlier resolution of Novak's displayed comparison. The root freshly read and visually checked Su's printed451 Fourier formula and Anderson et al.'s printed1383 Lemma2.1, read the surrounding definitions and full lemma proof1383–85, and independently derives the following argument. The model-specific choice of coefficient, shift cancellation, averaging and comparison are supplied here; the old generic formulas alone do not establish historical priority. Final disposition is recorded separately in ROOT_PRIORITY_DECISION.md.

Su, *A LeVeque-type lower bound for discrepancy*, in *Monte Carlo and Quasi-Monte Carlo Methods1998*, Springer2000,448–458, proves in Lemma4's proof that the nonzero Fourier coefficients of cumulative discrepancy equal the empirical measure coefficients divided by−2πim. The author's reprint explicitly identifies that publication; it is not a new2026 source. Its discrepancy supremum theorems are not substituted for an L4 statement: only the displayed cumulative Fourier identity is used. The added centering constantK changes only Fourier mode0.

For the actual normalized anchored function F(x)=n^-1 sum_j1[t_j<x]−x, direct integration also checks every endpoint convention:

integral_0^1 F(x) exp(−2πix) dx = (2πin)^-1 sum_j exp(−2πit_j).

Indeed each indicator integral is(exp(−2πit_j)−1)/(2πi) and integral_0^1 x exp(−2πix) dx=−1/(2πi), so constants cancel. This works also when an indexed point is0; the value at a single endpoint has zero integration measure. Thus no unjustified integration-by-parts boundary term or mean-zero assumption enters.

Triangle inequality and Hölder on the unit interval give |sum_j exp(2πit_j)|/n≤2π||F||_1≤2π||F||_4. For t_j={jz+Delta}, the sum is a unit-modulus shift phase times D_n(z)=sum_(j=0)^(n−1)exp(2πijz). Taking fourth powers and averaging the actual full product generator/shift law therefore yields

E disc_4^4 ≥ (16π^4 n^4)^-1 integral_0^1|D_n(z)|^4 dz.

Anderson–Ash–Jones–Rider–Saffari, *Exponential sums with coefficients0 or1 and concentrated Lp norms*, Ann.Inst.Fourier57(2007),1377–1404, equation(1.1) defines this exact length-n one-sided Dirichlet kernel, and Lemma2.1 states its pth moment is δ_p n^(p−1)+o(n^(p−1)), δ_p>0, for every p>1, with full proof supplied. In particular the imported p4 bound alone makes the right-hand side bounded below by a positive constant/n eventually. The iid fourth moment is(3n−1)/(30n³)=O(n^-2), as independently verified. Hence the original universal comparison is false for sufficiently large n. This is a direct substitution of the identical kernel/law, not an assumption that a typical-generator estimate controls high moments.

An elementary exact check removes even the asymptotic boundary: orthogonality gives integral|D_n|^4 equal to the number of a+b=c+d with0≤a,b,c,d<n. The pair-sum multiplicities are1,2,...,n−1,n,n−1,...,1, so the count is(2n³+n)/3. Consequently

E disc_4^4 ≥ (2n²+1)/(48π^4 n³).

At n234 this lower bound already exceeds the iid value. It is enough to check60n²+30−48π^4(3n−1)>0. Usingπ<22/7 gives the positive lower bound5975502/2401 at n234, and the resulting quadratic in n−234 has positive constant, linear and quadratic coefficients. The upper boundπ<22/7 can itself be checked without importing a delicate decimal estimate: the strictly positive integral_0^1 x^4(1−x)^4/(1+x²) dx equals22/7−π by polynomial division. Alternativelyπ<4 and n1000 already provide a coarser strict rational witness. Neither finite witness is essential to the older theorem's eventual full-negative implication.

The parent program `root_reproduction/check_fourier_bridge.py` independently checks pair-sum/Laurent-constant-term energy, a small four-index expansion, the rationalπ upper-bound identity, and explicit strict comparison certificates. These algebraic checks supplement the universal proof. The new application does not supply n3 minimality or its exact fraction; those can remain useful refinements, but a single sufficiently large n counterexample already settles the complete original universally quantified target.

Source receipts: `sources/ROOT_CLASSICAL_FETCH.json`. SuPDF236076 bytes SHA2560cbb07f38ab5e30700208c66831c6917497bea453a963d9a7db6bedd422003bf; AIFPDF540419 bytes SHA25635b5354d153b430ba9dc3c2043a0729385b2a67469064548fb6c113e80b588f9. All third-party bodies/text/renders remain ignored. The later Ferudun14Oct2026 exact-overlap preprint is chronologically distinct from this pre-existing2000/2007 theorem consequence and from the10Oct2026 source PR. No claim of who first recognized the consequence is made.
