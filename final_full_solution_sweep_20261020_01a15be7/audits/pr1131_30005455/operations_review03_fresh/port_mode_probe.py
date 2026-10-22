#!/usr/bin/env python3
"""Pure all-optimization-mode check of exact reviewed alias parser bytes."""
import pathlib,sys
p=pathlib.Path(__file__).resolve().parent;d=p/'review_driver.py';ns={'__file__':str(d),'__name__':'fresh_driver'}
exec(compile(d.read_bytes(),str(d),'exec'),ns)
live=ns['load']()('collect_live');rows=[]
for host in ['doi.org','www.doi.org','dx.doi.org','shortdoi.org','www.shortdoi.org','doi.org.']:
    for port in ['80','443','444']:
        bare=host+':'+port+'/abc'
        for v in [bare,'https://ordinary.invalid/?r='+bare,'https://ordinary.invalid/#'+bare,bare.replace(':','%253A')]:
            try:r=live.identities(v);accepted=True;error=None
            except Exception as e:accepted=False;r=None;error=str(e)
            rows.append({'value':v,'accepted':accepted,'identities':sorted(r) if r is not None else None,'error':error})
ns['dump'](p/('PORT_MODE_'+str(sys.flags.optimize)+'.json'),{'at':ns['stamp'](),'mode':sys.flags.optimize,'operations_sha256':ns['OPS_SHA'],'bootstrap_sha256':ns['BOOT_SHA'],'cases':rows,'accepted_unresolved_forms':sum(x['accepted'] for x in rows),'external_attempts':ns['ATTEMPTS'],'real_external_mutations':0})
print(ns['json'].dumps({'mode':sys.flags.optimize,'tested':len(rows),'accepted_unresolved_forms':sum(x['accepted'] for x in rows)}))
