"""Inert model uses actual reviewed phase shapes; no actual1329 state is edited."""
from pathlib import Path
import copy,json
def install_phase_world(w,phase):
    root=Path(__file__).resolve().parent
    actual=root.parent.parent/'pr1329_30003208/root_publication_action01'
    native=w.native;original=native.records
    draft_legacy=json.loads((actual/'LEGACY_AFTER_CREATE.json').read_bytes())
    draft_native=json.loads((actual/'NATIVE_DRAFT_AFTER_CREATE.json').read_bytes())
    def phased_records():
        fault=native.fault;native.fault=None
        try:l,n,f=original()
        finally:native.fault=fault
        published=native.published;r=777;c=778;api='https://zenodo.org/api/records/777';dep='https://zenodo.org/api/deposit/depositions/777'
        if not published:
            for key in ['doi','doi_url','conceptdoi']:l.pop(key,None)
            l['metadata'].pop('doi',None);n['pids']={};n['parent']['pids']={}
            n['versions']={'index':1,'is_latest':False,'is_latest_draft':True}
            n['expires_at']=draft_native['expires_at'];n['parent']['access'].update(grants=[],links=[])
        else:n.pop('expires_at',None)
        n['ui']['is_draft']=not published;l['title']=native.metadata['title']
        if not published:
            for key in ['stats','swh','deletion_status']:n.pop(key,None)
            n['revision_id']=5
        else:
            n['versions']={'index':1,'is_latest':True,'is_latest_draft':True};n['revision_id']=3
            n['created']=l['created']='2026-10-22T15:00:00.000000+00:00'
            n['updated']=l['modified']='2026-10-22T15:00:01.000000+00:00'
            n['deletion_status']={'is_deleted':False,'status':'P'};n['swh']={}
            zero={'views':0,'unique_views':0,'downloads':0,'unique_downloads':0,'data_volume':0.0}
            n['stats']={'this_version':copy.deepcopy(zero),'all_versions':copy.deepcopy(zero)}
        lkeys=set(native.lr['links'])if published else set(draft_legacy['links'])
        nkeys=set(native.nr['links'])if published else set(draft_native['links'])
        lroute=phase.routes('legacy',r,c,published);nroute=phase.routes('native',r,c,published)
        l['links']={k:lroute[k]for k in lkeys-{'bucket','thumb250','thumbs'}}
        l['links']['bucket']='https://zenodo.org/api/files/'+native.bucket
        if not published:l['links']['badge']='https://zenodo.org/badge/doi/.svg'
        n['links']={k:nroute[k]for k in nkeys-{'thumbnails'}}
        f['links']={'self':api+(''if published else '/draft')+'/files'}
        for e in f['entries']:
            name=e['key'];route=api+(''if published else '/draft')+'/files/'+name
            e['links']={'self':route,'content':route+'/content'}
            if published:e.update(created='2026-10-22T15:00:00.100000+00:00',updated='2026-10-22T15:00:00.200000+00:00')
            if not published:e['links']['commit']=route+'/commit'
            if name.endswith('.pdf'):
                e['metadata']={'width':612,'height':792};prefix='https://zenodo.org/api/iiif/'+('record:'if published else 'draft:')+'777'
                e['links'].update(iiif_canvas=prefix+'/canvas/'+name,iiif_base=prefix+':'+name,iiif_info=prefix+':'+name+'/info.json',iiif_api=prefix+':'+name+'/full/full/0/default.png')
            entry=n['files']['entries'][name];entry['metadata']=copy.deepcopy(e['metadata'])
            if published:entry['links']=copy.deepcopy(e['links'])
            else:entry.pop('links',None)
            legacy=next(x for x in l['files']if x['filename']==name)
            legacy['links']={'self':(api if published else dep)+'/files/'+legacy['id'],'download':api+'/draft/files/'+name+'/content'}
        pdf=next((name for name in native.present if name.endswith('.pdf')),None)
        if pdf:
            l['links'].update(phase.thumbnails('legacy',r,pdf));n['links'].update(phase.thumbnails('native',r,pdf))
        if published and pdf:
            key=pdf+'.ptif';entry=copy.deepcopy(next(iter(json.loads((actual/'AFTER_PUBLISH_NATIVE.json').read_bytes())['media_files']['entries'].values())))
            entry.update(key=key,id='00000000-0000-0000-0000-000000004444')
            entry['processor']['source_file_id']=n['files']['entries'][pdf]['id']
            entry['links']={'self':api+'/files/'+key,'content':api+'/files/'+key+'/content'}
            n['media_files']={'enabled':True,'order':[],'count':1,'total_bytes':0,'entries':{key:entry}}
        if fault:fault(l,n,f)
        return l,n,f
    native.records=phased_records
    original_upload=native.upload
    def actual_bucket_ack(bucket,entry):
        original_upload(bucket,entry)
        l,n,f=native.records();file=next(e for e in f['entries']if e['key']==entry['name'])
        route=bucket+'/'+entry['name']
        return {'created':file['created'],'updated':file['updated'],'version_id':file['version_id'],
                'key':entry['name'],'size':entry['size'],'mimetype':file['mimetype'],'checksum':'md5:'+entry['md5'],
                'is_head':True,'delete_marker':False,
                'links':{'self':route,'version':route+'?version_id='+file['version_id'],'uploads':route+'?uploads=1'}}
    native.upload=actual_bucket_ack
    # Public raw route uses the native-style link vocabulary seen in both actual
    # public captures, while its legacy metadata projection remains unchanged.
    original_public=native.public;api_public='https://zenodo.org/api/records/777'
    def public():
        p=original_public();l,n,f=native.records();p['links']=copy.deepcopy(n['links'])
        p.update(recid='777',title=native.metadata['title'],revision=n['revision_id'],created=n['created'],updated=n['updated'],modified=l['modified'],swh=copy.deepcopy(n.get('swh',{})))
        p['files']=[{'id':e['file_id'],'key':e['key'],'size':e['size'],'checksum':e['checksum'],'links':{'self':api_public+'/files/'+e['key']+'/content'}}for e in f['entries']]
        return p
    native.public=public
    original_records=w.records;w.list_file_omissions=[]
    def account_list():
        records=original_records()
        for value in records:
            if value.get('id')==777 and not native.published:
                if value['files']:w.list_file_omissions.append(len(value['files']))
                value['files']=[]
        return records
    w.records=account_list
