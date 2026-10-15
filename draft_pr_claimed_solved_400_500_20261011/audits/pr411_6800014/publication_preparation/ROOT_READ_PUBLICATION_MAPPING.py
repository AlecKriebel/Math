#!/usr/bin/env python3
"""Eight genuine GETs, exact public schema mapping; no state edits or mutations."""
import base64
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
CASE = HERE.parent
HELPER = HERE / 'admin_helper_v2/publication_admin_v2.py'
HELPER_SHA = 'afe03699b252c4aff76f29ba71404dfbe3c9c6a8c924b7028cfa4141f0759f8a'
V2_STATE_SHA = '46e1b481e5291520fd1d2fb2ca9403b9e8184e097b8d240a9b1d4cc0ea4db66c'
ADOPTION_SHA = 'ccc384738d0a1c81ee4eb42c389dac28acd024ec0d11f88dbf419243560a9fca'

def main():
    fd = os.open(HELPER, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as f: raw = f.read()
    if hashlib.sha256(raw).hexdigest() != HELPER_SHA: raise RuntimeError('helper changed')
    spec = importlib.util.spec_from_file_location('root_publication_mapping', HELPER)
    m = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(HELPER), 'exec'), m.__dict__)
    v2raw, _ = m.g.read_regular(m.STATE, private=True)
    m.need(m.sha(v2raw) == V2_STATE_SHA, 'historical V2 state changed')
    path = m.PRIVATE / 'ROOT_READONLY_PUBLIC_MAPPING_20261013T0510'
    e = m.Admin(m.v1.Production(), path)
    j = e.read_state(m.SPEC_SHA)
    m.need(j['adoption']['sha256'] == ADOPTION_SHA and j['publish_intent'] is True
           and j['append_intent'] is False and j['phase'] == 'intent_recorded', 'known STOP state differs')
    m.v1.save(path / 'ORIGINAL_V2_PRODUCTION_STATE.json', json.loads(v2raw), True)
    m.need(m.sha(m.g.read_regular(path / 'ORIGINAL_V2_PRODUCTION_STATE.json', private=True)[0]) == V2_STATE_SHA,
           'copy changed original state bytes')
    try:
        os.environ['ZENODO_TOKEN'] = m.z.token_for('production')
        s = j['spec']; expected = e.accepted_native(m.ROOT_SNAPSHOT_SHA)
        d = e.request('zenodo', f'GET /api/deposit/depositions/{m.ID}')
        e.legacy(d, s, m.ID)
        m.need(d['submitted'] is True and d['doi'] == f'10.5281/zenodo.{m.ID}', 'publication not confirmed')
        snapshot, native = e.native(m.ID, s, False, expected)
        public = e.request('public_json', 'GET', {'id': m.ID, 'native': False})
        p = public['metadata']
        keys = {'access_right','creators','description','doi','keywords','language','license','notes',
                'publication_date','relations','resource_type','title','version'}
        m.need(set(p) == keys and str(public['id']) == str(m.ID), 'public legacy shape changed')
        same = keys - {'doi','license','relations','resource_type'}
        m.need({k:p[k] for k in same} == {k:s['metadata'][k] for k in same}, 'nine exact public fields differ')
        m.need(p['license'] == {'id':s['metadata']['license']} and p['resource_type'] ==
               {'subtype':s['metadata']['publication_type'], 'title':'Preprint','type':s['metadata']['upload_type']},
               'explicit public projection differs')
        m.need(p['doi'] == d['doi'] and public['doi'] == d['doi'], 'public DOI differs')
        concept = e.contract['concept_id']
        m.need(concept == '23331231' and p['relations'] == {'version':[{'index':0,'is_last':True,
               'parent':{'pid_type':'recid','pid_value':concept}}]}, 'actual version relation differs')
        pn = e.request('public_json', 'GET', {'id':m.ID,'native':True})
        parent = native['parent']; pa = parent['access']
        m.need(pa.get('grants') == [] and pa.get('links') == [], 'auth parent grants/links not the observed empty values')
        public_parent = {**parent, 'access':{k:v for k,v in pa.items() if k not in ('grants','links')}}
        m.need(str(pn['id']) == str(m.ID) and all(pn.get(k) == v for k,v in snapshot.items())
               and pn.get('pids') == native.get('pids') and pn.get('parent') == public_parent
               and pn.get('is_draft') is False and snapshot['metadata']['publisher'] == 'Zenodo',
               'public native complete snapshot, publisher or identity differs')
        m.need(native['pids']['doi']['identifier'] == d['doi'], 'native DOI differs')
        m.z.verify({'metadata':s['metadata'],'files':list(pn['files']['entries'].values())},s['metadata'],s['assets'])
        hashes=[]
        for f in s['assets']:
            h = e.request('public_hash','GET',{'id':m.ID,'name':f['name']})
            m.need(h['http_status'] == 200 and all(h[k] == f[k] for k in ('sha256','md5','size')), 'public download differs')
            hashes.append({'name':f['name'],**h})
        m.need(e.count == 8, 'positive eight GET count differs')
        pins={}
        for file in sorted(path.iterdir()):
            b,_=m.g.read_regular(file,private=True)
            pins[str(file.relative_to(CASE))]={'bytes':len(b),'sha256':m.sha(b)}
        result={'result':'ROOT_ACTUAL_PUBLICATION_PUBLIC_MAPPING_ACCEPTED','utc':dt.datetime.now(dt.timezone.utc).isoformat(),
                'id':m.ID,'doi':d['doi'],'doi_url':'https://doi.org/'+d['doi'],'record_url':f'https://zenodo.org/records/{m.ID}',
                'scientific_head':m.HEAD,'whole_acceptance_sha256':m.WHOLE_ACCEPTANCE_SHA,'spec_sha256':m.SPEC_SHA,
                'approved_native_snapshot_sha256':m.ROOT_SNAPSHOT_SHA,'helper_sha256':HELPER_SHA,
                'original_v1_state_sha256':m.ORIGINAL_STATE_SHA,'original_v2_stop_state_sha256':V2_STATE_SHA,
                'authenticated_requested_metadata12_exact':True,'public_legacy_exact13keys':True,'public_exact9fields':sorted(same),
                'explicit_license_projection':p['license'],'explicit_resource_type_projection':p['resource_type'],
                'actual_first_version_relation':p['relations'],'concept_id':concept,
                'public_native_full_metadata_access_custom_fields_equal_approved':True,'parent_public_projection':'exact authenticated parent with only empty access.grants and access.links omitted','publisher_legacy_omitted_native_exact':'Zenodo',
                'public_downloads':hashes,'get_requests':8,'remote_mutations':0,'sheet_append_attempted':False,
                'original_state_edits':0,'positive_private_originals':pins}
        m.g.durable(HERE / 'ROOT_ACTUAL_PUBLICATION_MAPPING_ACCEPTANCE.json',result,exclusive=True)
        m.v1.save(path/'RESULT.json',result,True)
        print(json.dumps({'result':result['result'],'doi':result['doi'],'get_requests':8,'remote_mutations':0,
                          'acceptance_sha256':m.sha(m.g.read_regular(HERE/'ROOT_ACTUAL_PUBLICATION_MAPPING_ACCEPTANCE.json')[0])}))
    finally:
        os.environ.pop('ZENODO_TOKEN',None)
        m.need(m.sha(m.g.read_regular(m.STATE,private=True)[0]) == V2_STATE_SHA,'V2 state edited')
        e.check_original()

if __name__ == '__main__': main()
