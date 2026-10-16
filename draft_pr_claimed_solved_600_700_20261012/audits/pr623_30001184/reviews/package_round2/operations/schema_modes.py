#!/usr/bin/env python3
"""Pure archive-schema controls runnable with normal Python and -O."""
import datetime,importlib.util,io,json,pathlib,sys,zipfile
sys.dont_write_bytecode=True
OUT=pathlib.Path(__file__).resolve().parent;AUDIT=OUT.parents[2]
spec=importlib.util.spec_from_file_location('prepare_integration',AUDIT/'prepare_integration.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
original,_=p.load_snapshot(AUDIT/'native'/p.PREFIX)
papers={'gns_generation_counterexample.pdf':b'%PDF-1.7\ncontrol\n','gns_generation_counterexample.tex':b'control TeX'}
source=b'Burgarth-Facchi-Hillier corollary control notice\n'
members={'candidate/'+n:d for n,d in original.items()}|papers|{'CURRENT_PRIORITY_AND_STATUS.md':source}
outputs=[]
for schema in [1,True,1.0,2,False]:
    manifest={'schema':schema,'file_count':len(members),'files':[{'path':n,'bytes':len(d),'sha256':p.sha(d)} for n,d in sorted(members.items())],'raw_third_party_fulltexts_included':False}
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for n,d in members.items():z.writestr(n,d)
        z.writestr('PACKAGE_MANIFEST.json',p.json_bytes(manifest))
    try:
        details=p.archive_binding(buf.getvalue(),original,papers,source); outcome='ACCEPTED'
    except Exception as exc:outcome='REJECTED';details={'error':str(exc)}
    outputs.append({'schema':schema,'schema_type':type(schema).__name__,'outcome':outcome,'details':details})
p.require([x['outcome'] for x in outputs]==['ACCEPTED','ACCEPTED','ACCEPTED','REJECTED','REJECTED'],'schema outcomes changed; inspect current helper')
obj={'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python_optimization':sys.flags.optimize,'results':outputs}
(OUT/('SCHEMA_O'+str(sys.flags.optimize)+'_RESULTS.json')).write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps({'python_optimization':sys.flags.optimize,'schema_true_accepted':True,'schema_float_one_accepted':True}))
