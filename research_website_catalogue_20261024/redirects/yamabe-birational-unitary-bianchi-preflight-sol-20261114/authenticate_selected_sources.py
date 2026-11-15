"""Authenticate selected native inputs through their original distinct seals."""
from preflight_core import *
from datetime import datetime,timezone
out=[];external=[]
for r in RECORDS:
    S=P/'papers'/r/'sources';manifest=S/'SOURCE_READY_MANIFEST.json';seal=S/'SOURCE_READY_SEAL.json'
    m=load(manifest);s=load(seal)
    mk='SOURCE_READY_MANIFEST_SHA256' if r=='22929857' else 'manifest_sha256'
    rk={'23383952':'SOURCE_READY_sha256','23539734':'SOURCE_READY_sha256','22929857':'SOURCE_READY_SHA256','23320818':'source_ready_sha256'}[r]
    need(sha(manifest.read_bytes())==s[mk],'Native source ready manifest seal')
    need(sha((S/'SOURCE_READY.json').read_bytes())==s[rk],'Native source ready seal')
    selected=[x for x in load(O/'SOURCE_BINDINGS.json') if x['path'].startswith(str(S)+'/')]
    matched=[]
    for x in selected:
        rel=str(Path(x['path']).relative_to(S));e=next(y for y in m['files'] if y['path']==rel)
        dk='SHA256' if r=='22929857' else 'sha256'
        need(binding(x['path'])=={'bytes':e['bytes'],'sha256':e[dk]},'Native selected original member '+rel)
        matched.append({'native_relative_path':rel,'original_manifest_digest_field':dk,**x})
    out.append({'record':r,'native_manifest':{'path':str(manifest),**binding(manifest)},'native_seal':{'path':str(seal),**binding(seal)},
                'original_manifest_digest_selector':mk,'original_readiness_digest_selector':rk,'selected_originals_authenticated':matched,
                'no_native_original_object_or_schema_edited':True})
    for p in [manifest,seal]:external.append({'path':str(p),**binding(p)})
for typ,oid in [('commit',COMMIT),('tree',TREE)]:
    b=git('cat-file',typ,oid)
    need(hashlib.sha1((typ+' '+str(len(b))+'\0').encode()+b).hexdigest()==oid,'Actual Git object hash')
    (O/('git-object-'+oid+'.raw')).write_bytes(b)
(O/'NATIVE_SOURCE_AUTHENTICATION.json').write_text(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'records':out,'additional_external_bindings':external},indent=2)+'\n')
print(json.dumps({'native_source_packets':len(out),'selected_native_files':sum(len(x['selected_originals_authenticated']) for x in out),'native_seals_and_manifests':len(external),'Git_objects':2}))
