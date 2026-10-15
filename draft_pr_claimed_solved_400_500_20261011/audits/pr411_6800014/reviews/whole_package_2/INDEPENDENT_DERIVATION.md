# Newly reconstructed theorem attack

The independently authored code contracts raw five-dimensional structure constants using the Koszul formula, rather than importing any package checker. It reproduces Ric00=-||S||², Ric0V=0, RicV=[A,Aᵀ]/2 for the trace-zero slice, F=s²/(s²+q/4), and P=q-8s².

For any positive Gram Γ, the orthonormal complement f0=c(e0−ΓV⁻¹β), c=(α−βᵀΓV⁻¹β)^−1/2 and ideal frame T=ΓV^−1/2 give cT⁻¹AuT. The shift commutes with the ideal, so all ten ideal metric coordinates, four cross terms and complement length are covered. Scaling and orthogonal conjugation preserve F. Every conjugacy is realized by declaring its inverse-change frame orthonormal.

For conjugates near Au, E=I+A² is an exact idempotent onto ker A². The supplied p=Ee4 construction has nonzero denominators at u>0, hence smooth local frame. The quotient C has C²=−I and skew sign k>0. The cross-block L is unrestricted. Its six transverse coordinates plus v form the requisite local slice; no orthogonality of E is assumed. An independent Sylvester computation additionally shows all such L lie in the actual orbit, using disjoint spectra of C and N.

Exact multiplication in independent_exact.py gives the displayed P=Qv+Rv with every sign verified. Put I=[v−,v+]⊂(0,1/2). The two 2×2 mixed blocks have positive leading entry, determinant 1−4v² and trace 2−3v². Thus twice the smaller eigenvalue is ≥2det/trace≥1−4v²≥c0=1−4v+². The a,b coefficient also exceeds c0. Hence Q≥c0ρ².

Each remainder bound follows from disjoint-pair Cauchy inequalities |wz+xy|,|wy−xz|,|wx+yz|,|wx−yz|≤r²/2 and |a|+|b|≤√2ρ. For ρ≤1, k≤√2 and k−1≤h²/2. The six bounds are 12ρ⁴,12√2ρ³,12√2ρ³,√2ρ³,ρ⁴/2,ρ⁴. Their sum ≤(13.5+25√2)ρ³<50ρ³. For ρ≤c0/100, P≥c0ρ²/2. Since slice coordinates are continuous, inverse image of these strict bounds is an actual neighborhood in the full Gram cone. Flat v is uniformly controlled on I, and F=1/3 exactly when transverse ξ=0. This supplies the missing argument beyond a semidefinite Hessian.

The original Ric diagonal forces c=−u²/2 from [e0,e1]=e2; [e0,e4]=ue3 then fails by u². Independent exact conjugacy TB H Au H⁻¹ TB⁻¹=B yields s=3/2,q=8,F=9/17. Nearby v>0 are same-group flat conjugates, proving non-strictness.

The exact same-orbit slice x=w=a=b=0,z=t,y=vt gives P=2(1−4v²)t²−4v²t⁴. At v=1/2, P=−t⁴, so the endpoint fails; above it, ascent is already quadratic. At u=0, the smooth nilpotent frame construction is invalid and F is undefined at the flat metric, consistent with the theorem's exclusions.

The group law's metric dt²+||exp(−tAu)dX||² splits as Euclidean dx1²+dx2² plus dt²+(dx3−ut dx4)²+dx4². This is R²×H3 and the product derivation diag(1.5u²,1.5u²,u²,2u²,u²) with c=−1.5u² obeys the Heisenberg bracket. It does not obey the original rotation brackets. This independently confirms the Ricci soliton distinction.

Status: all five mathematical mechanism families verified; no scientific gap found in the complete theorem. No reliance on any prior PASS. Scientific deductions are exact; no empirical assumption or finite sampling is promoted to proof.
