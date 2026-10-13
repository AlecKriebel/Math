"""Cross-check canonical trace against independent conic-generated polygons."""
import json
from pathlib import Path
import direct_geometry_check as g
mp=g.mp
mp.mp.dps=100
rows=[]
for row in json.load(open('PRE_EXPOSURE_NUMERIC.json'))['target_cases']:
    a=mp.mpf(row['a']);b=mp.mpf(row['b']);lam=mp.mpf(row['lambda']);n=row['N'];m=row['winding']
    # Recompute the caustic to avoid restricting precision to serialized 35 digits.
    lam=g.caustic(a,b,n,m)
    scale=mp.sqrt(a*a-lam);k=mp.sqrt(a*a-b*b)/scale;K=mp.ellipk(k*k)
    v=mp.ellipf(mp.asin(mp.sqrt(lam/(b*b))),k*k);h=4*K/n;delta=2*v
    coeff_ap=[];coeff_aa=[];circle_errors=[];geometry_errors=[];minpedal=mp.inf
    for theta in map(mp.mpf,row['phases']):
        poly,_,_=g.orbit(a,b,lam,n,theta);f=(mp.sqrt(a*a-b*b),mp.mpf(0))
        feet,anti,_=g.pedal_anti(poly,f)
        # True absolute circle residual; the frozen initial checker reported a signed deviation.
        circle_errors.extend(abs(g.dot(g.vadd(q,f),g.vadd(q,f))-(a*a-lam))/(a*a) for q in feet)
        w=mp.ellipf(theta-mp.pi/2,k*k)
        canonical=[(-a*mp.ellipfun('sn',w+i*delta,k*k),b*mp.ellipfun('cn',w+i*delta,k*k)) for i in range(n)]
        geometry_errors.append(max(g.norm(g.vsub(p,q))/a for p,q in zip(poly,canonical)))
        T=lambda z:sum(mp.ellipfun('dn',z+i*delta,k*k) for i in range(n))
        aa=g.area(anti)/(scale*scale);ap=g.area(feet)/(scale*scale)
        minpedal=min(minpedal,ap)
        coeff_aa.append(aa/T(w));coeff_ap.append(ap/T(w+h/2))
    span=lambda coeff:(max(coeff)-min(coeff))/max(mp.mpf(1),max(abs(x) for x in coeff))
    rows.append({'a':row['a'],'b':row['b'],'N':n,'winding':m,'rotation_param_residual':g.strnum(abs(n*v/(2*K)-m)),'max_conic_vs_canonical_vertex_residual':g.strnum(max(geometry_errors)),'max_absolute_pedal_circle_residual':g.strnum(max(circle_errors)),'antipedal_trace_coefficient_relative_span':g.strnum(span(coeff_aa)),'pedal_shifted_trace_coefficient_relative_span':g.strnum(span(coeff_ap)),'minimum_normalized_pedal_area':g.strnum(minpedal)})
result={'provenance':'After candidate proof exposure. Polygons still generated only by independent conic tangency; classical Jacobi trace then evaluated for comparison. No submitted author/reviewer checker read or run. This is numerical corroboration, not an all-period proof.','digits':mp.mp.dps,'rows':rows}
Path('POST_EXPOSURE_DIAGNOSTICS.json').write_text(json.dumps(result,indent=2)+'\n')
print('Cases checked:',len(rows))
for key in ['rotation_param_residual','max_conic_vs_canonical_vertex_residual','max_absolute_pedal_circle_residual','antipedal_trace_coefficient_relative_span','pedal_shifted_trace_coefficient_relative_span']:
 print(key,max(mp.mpf(x[key]) for x in rows))
