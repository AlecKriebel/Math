# Independent mathematical assessment before historical review exposure

Date: 2026-10-02 UTC. Verification effort, not a new proof-search attempt.

Exposure disclosure: the assignment disclosed the proposed credited/already-solved disposition, 2/5 accounting, four stationary points, epsilon interval and Ni–Zhang–Zhang prior. I read repository instructions and inventoried filenames, then accidentally read the entire current RESULT.md before opening the literal primary source. This violates the requested source-first ordering; I preserve that fact rather than claiming source-first blindness. I then read the actual Ghomi PDF page image (printed p6) and text with its preceding definition, and Ni–Zhang–Zhang v1 pp1–3. No earlier family/root proof, report, interpretation, or verdict has yet been read. This is an independently reconstructed check of an exposed candidate, not a blind discovery.

Ghomi permits continuous osculating planes and a continuous one-to-one field orthogonal to them. No regularity of the map B is in the literal question. An embedded positive-curvature counterexample with a unit Frenet binormal therefore suffices even under stronger interpretations of those hypotheses.

Put p=(cos t,sin t)=(c,s), g=(c,s,(c²-s²)/4), w=(-c³,s³,1), r=|w|. Direct differentiation of g gives g'=(-s,c,-sc), g''=(-c,-s,-(c²-s²)) and cross product w. Thus speed and curvature are positive. B=w/r is a smooth unit compatible binormal, globally injective because ratios -Bx/Bz and By/Bz determine c³ and s³. Bz=1/r>0. Differentiating w=rB proves B'=0 iff w'=0, since its z component forces r'=0. w'=(3c²s,3s²c,0) vanishes iff cs=0: exactly four cardinal parameters. The determinant (g',g'',g''')=3cs gives torsion 3cs/r². There is no illicit assumption that B is an immersion.

The map F(x,y)=(-x³,y³,1)/sqrt(1+x⁶+y⁶) on the convex closed unit disk has derivative norm <=3: normalization has norm <=1/|w|<=1 and the cubic derivative norm <=3. The xy projection shares this bound. For 0<e<1/3 the map Q=p+e Fxy(p) has global lower distance bound (1-3e)|p-q| and derivative lower bound (1-3e)|v|. Restriction to the circle is therefore a smooth embedded parametrized curve. Its spatial lift g+eB is embedded.

The orientation-preserving global polynomial shear H(x,y,z)=(x,y,z-(x²-y²)/4) flattens g onto the unit circle. For P=g+eB,
H_z(P)=e/r[1+(c⁴+s⁴)/2-e(c⁶-s⁶)/(4r)] >=e/r(1-e/4)>0.
This inequality holds for every parameter and every 0<e<1/3, with no numerical/sampling inference. H(P) misses the entire spanning unit disk, so both curves are disjoint and their linking number is zero by the intersection definition. The sign/orientation convention cannot change zero.

The dated earlier v1 section 2 prints V=(x,y,x⁴-y⁴), normal (-4x³,4y³,1)/sqrt(1+16x⁶+16y⁶), and gamma_a=(ac,as,a⁴(c⁴-s⁴)). Direct differentiation yields gamma_a'×gamma_a''=a²(-4a³c³,4a³s³,1), so its normal is the Frenet binormal. Choosing a=4^(-1/3) and scaling by 1/a gives precisely g, since c⁴-s⁴=c²-s² and a³=1/4. A positive homothety preserves orientation and unit binormals and takes delta to e=delta/a. The supplied counterexample is an elementary exact consequence of this construction, not an independent new construction eligible for a novelty claim. This establishes a sufficient dated prior construction, not worldwide earliest priority or that the paper names Ghomi/linking.

For the printed graph disk at a=1, its positive normal displacement q has alpha=e/|(-4x³,4y³,1)|>0. For 0<e<1/4, |x-4alpha x³|<=|x| and |y+4alpha y³|>=|y|. Hence q_z-q_x⁴+q_y⁴>=alpha>0, an independent surface-avoidance certificate. It gives small disjoint push-offs; embedding for the entire 1/4 interval is not implied by this calculation.

The graph Gaussian curvature is -144x²y²/(1+16x⁶+16y⁶)² and vanishes on axes. At a regular curve on a strictly negatively curved surface the shape operator is invertible, so its normal derivative cannot vanish. Thus neither this counterexample nor its cited graph settles the later strictly negative curvature target or tight-surface rigidity.

Preliminary conclusion: I find the universal counterexample and exact positive-scale prior equivalence correct. This is not a final verdict; historical proof/metadata/program/source/accounting checks remain. Audit completion estimate 20%; mathematical conclusion conditional on verified primary/frozen byte bindings.
