# Independent pre-audit derivation

Isolation: written after reading original Problem 7.37 (Hayman–Lingham v2, PDF pp.172–173), EH1995 pp.2793–2797, and LP2009 interfaces, before opening main.tex, inputs, root conclusions or earlier review reports/programs. Parent's assignment already disclosed the claimed construction and constant; independence is of derivation/check, not of route discovery or novelty.

Let disks B_j centered z_j have area πλ_j. LP finite smash sum Ω contains all B_j, is bounded, has area π, and boundary null by repeated Prop2.12/Cor2.13, and satisfies whole-Ω quadrature ∫Ω h = πΣλ_j h(z_j) for integrable harmonic h by applying Prop6.6 to h and −h. For ANY z outside closure Ω the functions Re(w−z)^−2, Im(w−z)^−2 are harmonic/integrable on Ω, independently of complement component. Thus −TχΩ(z)=Σλ_j/(z−z_j)^2=g(z), T=−(1/π)∫(z−w)^−2. S=closure Ω is compact area π, excludes every pole by containment of its positive disk, is independent of R.

For fixed R>1 split E=Ω∩D(√2R), F=Ω\E. Let a=|E|∈[0,π]. On D(R)\S use TχΩ=TχE+TχF a.e. EH scaled indicator estimate yields ∫D(R)\S |TχE| ≤ a log(2πR²/a), with endpoint a=0 by continuity. For each |w|≥√2R,
(1/π)∫D(R) |z−w|^−2 dA(z)=log(|w|²/(|w|²−R²))≤log2.
Hence by Tonelli far contribution ≤(π−a)log2, giving ∫≤2a logR+a log(π/a)+πlog2≤2πlogR+π/e+πlog2. EH off-source indicator estimate makes the near integrand L1; far term is finite, so the integral is ordinary finite. Repeated poles combine; remote poles alter only boundedness radius, not constant; tiny positive masses still have neighborhoods; S one for all R.

Sharp leading coefficient: g=z^−2. For any measurable areaπ S, the removed integral on 1<|z|<R is at most π (because |z|^−2≤1 there). Thus ∫D(R)\S≥2πlogR−π; no coefficient below2π works. This argument does not require S to be compact or contain zero. Additive constant not optimized.

Exact remaining source check: visually confirm LP null-boundary/whole-domain hypotheses and EH2002 correction compatibility; confirm main proof matches this derivation and release programs do not overclaim certificates.
