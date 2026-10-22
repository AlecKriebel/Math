"""A perturbed nonconfocal inner ellipse must not survive reflected dynamics."""
from pathlib import Path
import runpy,json
root=Path(__file__).resolve().parent
g=runpy.run_path(str(root/"independent_geometry.py"));mp=g['mp']
a,b=mp.mpf(3),mp.mpf(2);lam=mp.mpf(36)/13
aa=mp.sqrt(a*a-lam);bb=mp.sqrt(b*b-lam+mp.mpf('0.001'))
rows=[]
for phase in g['PHASES']:
    p=(a*mp.cos(phase),b*mp.sin(phase));x,y=p[0]/aa,p[1]/bb
    r=x*x+y*y;h=mp.sqrt(r-1)
    contact=(aa*(x-y*h)/r,bb*(y+x*h)/r)
    d=g['unit'](g['sub'](contact,p))
    if g['cross']((p[0]/a,p[1]/b),(d[0]/a,d[1]/b))<0:
        contact=(aa*(x+y*h)/r,bb*(y-x*h)/r)
        d=g['unit'](g['sub'](contact,p))
    points=[p];errors=[]
    for j in range(4):
        q=g['second_hit'](p,d,a,b)
        ell=(q[1]-p[1],p[0]-q[0])
        errors.append(abs((aa*aa*ell[0]**2+bb*bb*ell[1]**2-g['dot'](ell,p)**2)/(a*a*g['dot'](ell,ell))))
        points.append(q);d=g['reflected'](d,q,a,b);p=q
    g['check']('initial perturbed-ellipse chord really tangent',errors[0]<mp.mpf('1e-65'))
    g['check']('nonconfocal tangency not preserved',max(errors[1:])>mp.mpf('1e-8'))
    value=g['focal_logproduct'](g['intersections'](points,a,b),a,b,1)
    rows.append({'phase':mp.nstr(phase,15),'max_later_tangency_residual':mp.nstr(max(errors[1:]),15),
                 'logproduct':mp.nstr(value,40)})
variation=max(abs(mp.mpf(v['logproduct'])-mp.mpf(rows[0]['logproduct'])) for v in rows)
g['check']('nonconfocal product phase variation detected',variation>mp.mpf('1e-8'))
result={'status':'PASS negative control rejected invalid extension','outer_axes':['3','2'],
        'inner_axes_squared':['9-36/13','4-36/13+1/1000'],'phase_logproduct_variation':mp.nstr(variation,15),'rows':rows}
(root/'nonconfocal_negative_control.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
