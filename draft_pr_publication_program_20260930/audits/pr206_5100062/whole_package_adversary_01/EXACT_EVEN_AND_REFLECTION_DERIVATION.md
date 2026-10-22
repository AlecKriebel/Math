# Independent finite and dynamical checks

These derivations are by this auditor after the primary assessment, without using a favorable assessment as proof.

## Why the flag successor is the physical specular successor

At a real outer point P=(x,y), let D=diag(a²,b²), outer normal n_E=D^-1 P, and let n be the unit normal of a chord line with w=n·P. Its caustic tangency condition is lambda=nᵀ(D−PPᵀ)n. Because PᵀD^-1P=1, the symmetric matrix D−PPᵀ annihilates n_E and has positive rank one. Thus it is a positive multiple of the orthogonal projection onto the outer tangent. Fixing lambda leaves two line normals symmetric relative to the outer normal/tangent axes. Specular reflection interchanges these two line directions. Since the proper inner ellipse lies strictly inside the boundary, the two caustic tangents at each real P are distinct and the billiard's incoming and outgoing chords are precisely the two flag choices. This checks the dynamical identification in TeX lines 144–158 rather than transferring the central claim to an unsupported closure statement.

## Diamond focal inverse area

For D=((a,0),(0,b),(−a,0),(0,−b)) and focus (c,0), the squared focal distances are (a−c)²,a²,(a+c)²,a². The four inverse-edge determinants, after translating the focus to the origin, occur in equal pairs b/[a²(a−c)] and b/[a²(a+c)]. Half their sum is

A_c(D)=b/a²[1/(a−c)+1/(a+c)]=2/(ab),

using a²−c²=b². The opposite focus gives the same area. Thus a²=8,b²=5 gives each area sqrt(10)/10 and product 1/10.

## Rectangle focal inverse area

Write S=a²+b², lambda=a²b²/S, alpha=a²/sqrt(S), beta=b²/sqrt(S). The rectangle R=((alpha,beta),(−alpha,beta),(−alpha,−beta),(alpha,−beta)) lies on the outer ellipse, has caustic tangent coordinate sides, and specular reflection follows since its outer normals have coordinate ratios ±1. Four distinct vertices establish primitivity.

For focus c, the right and left squared distances are d_+=2alpha(alpha−c) and d_−=2alpha(alpha+c), since alpha²−c²=beta². Both horizontal inverse-edge determinants equal 2alpha beta/(d_+d_−)=1/(2alpha beta). The vertical determinants are beta/[2alpha²(alpha+c)] and beta/[2alpha²(alpha−c)]. Half the full sum is 1/(alpha beta). The opposite focus gives the same result. At the required axes, each area is 13/40, product 169/1600. The difference from the diamond is 9/1600, within one fixed proper confocal caustic lambda=40/13.

## RGH single-control formula substitution

The Proposition 7 printed expression is rho^8/(8a^8b²) times [(a⁴+2a²b²+4b⁴)delta + 3a⁴b²/2 + a⁶ + 4b⁶]. At a²=8,b²=5,rho=1, the printed radicand a⁴−a²b²−b⁴=−1 is nonreal. Substituting plus b⁴ gives delta=7. The bracket becomes (64+80+100)*7+480+512+500=3200, and the denominator is 8*4096*5=163840. Their ratio is 5/256. This establishes only the stated qualified control comparison and neither repairs the formula universally nor establishes the uninspected journal typography.
