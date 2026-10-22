from pathlib import Path
import importlib.util,json,datetime
D=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr210_5100033/physical_geometry_01")
spec=importlib.util.spec_from_file_location("physical_geometry",D/"physical_geometry.py")
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
out=[]
for ratio,N,tau in [("8",11,5),("2",21,10)]:
    values=[]
    for precision,iterations in [(125,430),(190,680)]:
        p.M.mp.dps=precision
        a=p.M.mpf(ratio);b=p.M.mpf(1)
        lo=p.M.mpf("1e-110");hi=1-lo
        for j in range(iterations):
            mid=(lo+hi)/2
            if p.winding_lift(mid,a,b,N)<tau:lo=mid
            else:hi=mid
        lam=(lo+hi)/2
        Bs,res,geo=p.orbit_geometry(a,b,lam,N,tau,p.M.mpf("0.63"))
        values.append({"precision":precision,"bisections":iterations,"lambda":p.M.nstr(lam,180),
                       "product":p.M.nstr(Bs[0]*Bs[1],180),"max_geometric_residual":p.M.nstr(res,15)})
    p.M.mp.dps=190
    relative=abs(p.M.mpf(values[0]["product"])-p.M.mpf(values[1]["product"]))/max(1,abs(p.M.mpf(values[1]["product"])))
    if relative>p.M.mpf("1e-100"):raise AssertionError(("precision instability",str(relative)))
    out.append({"a_over_b":ratio,"N":N,"tau":tau,"values":values,"relative_product_change":p.M.nstr(relative,25)})
result={"timestamp_UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"scope":"Independent precision-sensitivity diagnostic of hardest two fixtures, not interval certification.","results":out}
(D/"PRECISION_SENSITIVITY.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
