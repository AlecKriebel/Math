# Additional geometry audit notes

Written after complete candidate exposure. Section7 was already implemented in the frozen pre-exposure symbolic code; sections8-9 are post-exposure stress checks.

## 7. Central quadrilaterals: pedal area has no dependence on pole

This additional direct calculation was completed before the proof was opened. Let the original centered quadrilateral be P,Q,-P,-Q with k=det(P,Q)>0. Its two positive side supports are h1=k/|Q-P|, h2=k/|P+Q| and their unit normals satisfy det(n1,n2)=2k/(|Q-P||P+Q|). Relative to an arbitrary pole F, the four feet are (h1-f1)n1,(h2-f2)n2,(-h1-f1)n1,(-h2-f2)n2, where fj=F dot nj. Shoelace gives

    A_p=2h1h2 det(n1,n2)
       =4k³/(|Q-P|² |Q+P|²).

The f1,f2 contributions cancel. This was used in symbolic_four_phase.py. It neither changes the antipedal pole nor licenses a moving focus in the target.

## 8. Exact zero-area stress family (after candidate exposure)

For r in[3,5], set b=1,

    a²=(r-1)³(r+1)/(4r),
    x=(r²-1)/(r²+1), y=2r/(r²+1),
    lambda=a²/(a²+r²).

Use the convex ordered octagon (a,0),(ax,y),(0,1),(-ax,y),(-a,0),(-ax,-y),(0,-1),(ax,-y). The first chord has tangency parameter lambda=a²/[a²+r²]; the second has lambda=a²/[1+a²((r+1)/(r-1))²]. These agree exactly because (r-1)³(r+1)=4a²r. Axis reflection propagates all eight contacts. Standard confocal reflection gives the billiard law; exact reflection at the off-axis vertex was also checked directly for both bracket endpoints. The eight distinct convex vertices make the period primitive.

At r=3: a²=8/3, lambda=8/35, A_p=576 sqrt(6)/245, A_a=56 sqrt(6)/81>0.

At r=5: a²=96/5, lambda=96/221, A_p=19200 sqrt(30)/3757, A_a=-10064 sqrt(30)/625<0.

Since a>b>0 and 0<lambda<b² over this interval, the direct geometric finiteness argument applies throughout. The signed antipedal area is continuous and changes sign, so some admitted primitive period-eight ellipse/caustic pair has zero antipedal area. This existence argument is exact and does not rely on the submitted product proof. Numerical identification gives a/b approximately1.853847304381821 and lambda/b² approximately0.2527893504891402. At the estimated root all five phase samples have product about-1.4784e-44 (root bracket width about5.96e-45), pedal areas about7.15, and minimum focal-normal angle sine above0.16. See the separate exact and numeric receipts.

## 9. Boundary and scaling facts

A uniform similarity of factor rho sends every foot and antipedal intersection to its scaled image, so each signed area scales by rho² and the product by rho⁴. Reversal reverses both derived vertex lists up to a cyclic shift, so both areas negate. Cyclic relabeling preserves them. In the excluded circle limit, a=b=R and F=O, a regular primitive star of winding m has theta=pi m/N, pedal radius R cos(theta), antipedal radius R/cos(theta), and product (N²R⁴/4)sin²(2theta), matching the nearcircle diagnostics. At lambda=b² the caustic becomes a focal segment and the focus is no longer strictly interior; antipedal finiteness need not persist. At lambda=0 the caustic coincides with the outer ellipse and distinct finite chords fail. Neither excluded limit is silently covered by the candidate proof.
