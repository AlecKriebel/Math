"""Typed complete observations, with explicit intentional phase transitions.

Unknown JSON fields are retained and compared. Only reviewed statistics may
advance between otherwise identical observations. This is no remote atomic lock.
"""
if not globals().get('_OPS17_VERIFIED',False):raise RuntimeError('Use checked17 bootstrap')
import copy,datetime,math,re,uuid
from urllib.parse import quote

def need(v,m):
    if not v:raise RuntimeError(m)
def json_value(v,path):
    if type(v) is dict:
        need(all(type(k) is str for k in v),'Nonstring JSON key '+path)
        for k,x in v.items():json_value(x,path+'/'+k)
    elif type(v) is list:
        for i,x in enumerate(v):json_value(x,path+'/'+str(i))
    else:need(type(v) in {str,int,float,bool,type(None)} and (type(v) is not float or math.isfinite(v)),'Nonfinite/non-JSON value '+path)
def schema(v,s,path):
    if type(s) is str:
        types={'str':str,'int':int,'float':float,'bool':bool,'null':type(None)}
        if s=='json':json_value(v,path)
        elif s=='number':need(type(v) in {int,float} and math.isfinite(v),'Expected JSON number '+path)
        elif s=='identifier':need(type(v) is int and v>0 or type(v) is str and re.fullmatch('[1-9][0-9]*',v),'Bad exact ID '+path)
        elif s=='positive_decimal':need(type(v) is str and re.fullmatch('[1-9][0-9]*',v),'Expected canonical positive decimal string '+path)
        else:need(type(v) is types[s],'Wrong exact schema type '+path)
        return
    if 'anyof' in s:
        for candidate in s['anyof']:
            try:schema(v,candidate,path);return
            except RuntimeError:pass
        raise RuntimeError('No exact schema alternative '+path)
    if 'object' in s:
        need(type(v) is dict,'Expected object '+path)
        for k,x in v.items():schema(x,s['object'].get(k,'json'),path+'/'+k)
    elif 'tuple' in s:
        need(type(v) is list and len(v)==len(s['tuple']),'Expected typed tuple '+path)
        for i,(x,t) in enumerate(zip(v,s['tuple'])):schema(x,t,path+'/'+str(i))
    elif 'list' in s:
        need(type(v) is list,'Expected array '+path)
        for i,x in enumerate(v):schema(x,s['list'],path+'/'+str(i))
    else:
        need('map' in s and type(v) is dict,'Expected named map '+path)
        for k,x in v.items():schema(x,s['map'],path+'/'+k)
def validate_types(role,value):
    json_value(value,role);schema(value,SCHEMA[role],role)
    if role=='public':
        need(set(value)==set(SCHEMA['public']['object']),'Unknown/missing public envelope field; review required')
        owners=value.get('owners')
        need(type(owners) is list and len(owners)==1 and type(owners[0]) is dict
             and set(owners[0])=={'id'},'Public owner schema/cardinality changed; review required')
    # Optional fields absent from the reference still have known typed schemas.
    if role in {'legacy','public'}:
        md=value.get('metadata',{})
        if 'prereserve_doi' in md:
            need(type(md['prereserve_doi'].get('recid')) is int,'Reservation recid must be integer')
    if role=='native':
        for field in ['files','media_files']:
            fs=value[field]
            need(type(fs['count']) is int and fs['count']>=0 and type(fs['total_bytes']) is int and fs['total_bytes']>=0,'Noninteger/negative native inventory')
        if 'revision_id' in value:need(type(value['revision_id']) is int and value['revision_id']>=0,'Invalid revision')
        stats=value.get('stats',{})
        for group in ['this_version','all_versions']:
            if group not in stats:continue
            for k in ['views','unique_views','downloads','unique_downloads','data_volume']:
                if k in stats[group]:need(type(stats[group][k]) in ({int,float} if k=='data_volume' else {int}) and stats[group][k]>=0,'Invalid statistic '+group+'/'+k)
def stamp(value):
    need(type(value) is str,'Timestamp type')
    try:d=datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
    except (ValueError,TypeError):raise RuntimeError('Malformed phase timestamp')
    need(d.tzinfo is not None,'Naive phase timestamp');return d
def eq(a,b):return TYPED_EQUAL(a,b)
def stats_advance(a,b):
    """Only lifetime view/download counters and numeric data volume may advance.
    Unknown statistics remain in the complete object and must be exactly stable.
    """
    for group in ['this_version','all_versions']:
        if group not in a or group not in b:continue
        for k in ['views','unique_views','downloads','unique_downloads','data_volume']:
            if k not in a[group] or k not in b[group]:continue
            need(b[group][k]>=a[group][k],'Lifetime statistic decreased')
            b[group][k]=copy.deepcopy(a[group][k])
def advance_time(a,b,key):
    if key in a and key in b and not eq(a[key],b[key]):
        need(stamp(b[key])>=stamp(a[key]),'Phase timestamp regressed');b[key]=a[key]
def file_map(value,field):
    values=value[field];need(type(values) is list,'File list type')
    result={v['filename' if field=='files' else 'key']:v for v in values}
    need(len(result)==len(values),'Duplicate file identity');return result
def allowed_route(old,new,record):
    if eq(old,new):return True
    if type(old) is not str or type(new) is not str:return False
    base='https://zenodo.org';r=str(record)
    pairs=[(base+'/uploads/'+r,base+'/records/'+r),
           (base+'/api/records/'+r+'/draft',base+'/api/records/'+r),
           (base+'/api/deposit/depositions/'+r,base+'/api/records/'+r)]
    return any((old==a or old.startswith(a+'/')) and new==b+old[len(a):] for a,b in pairs)
def phase_links(a,b,record):
    # Do not discard dictionaries, unknown fields, arbitrary URLs or query data.
    for k in set(a)&set(b):
        if not eq(a[k],b[k]) and allowed_route(a[k],b[k],record):b[k]=a[k]
def compare(first,last,transition=None,added=None):
    for k in ['record','concept','owner','doi','native_metadata']:
        need(eq(first[k],last[k]),'Typed target core changed '+k)
    a=copy.deepcopy(first['semantic17']);b=copy.deepcopy(last['semantic17'])
    PHASE.normalize(a,b,transition,added,first['record'],first['concept'])
    need(set(a)==set(b)=={'legacy','native','file_collection'},'Incomplete whole native observation')
    stats_advance(a['native'].get('stats',{}),b['native'].get('stats',{}))
    old_names=set(first['files']);new_names=set(last['files'])
    need(new_names==old_names|({added} if added is not None else set()),'Unexpected intended file set')
    for n,v in first['files'].items():need(eq(v,last['files'][n]),'Typed content/version/bucket changed')
    if transition in {'upload','update','publish'}:
        advance_time(a['legacy'],b['legacy'],'modified');advance_time(a['native'],b['native'],'updated')
        if 'revision_id' in a['native'] and 'revision_id' in b['native']:
            need(b['native']['revision_id']>=a['native']['revision_id'],'Revision regressed');b['native']['revision_id']=a['native']['revision_id']
    if transition=='upload':
        need(added is not None and added not in old_names,'Missing new upload identity')
        for role,field in [('legacy','files'),('file_collection','entries')]:
            old=file_map(a[role],field);new=file_map(b[role],field)
            need(set(new)==set(old)|{added},'Raw upload inventory differs')
            for n,v in old.items():need(eq(v,new[n]),'Existing raw file changed')
            a[role][field]=[old[n] for n in sorted(old)];b[role][field]=copy.deepcopy(a[role][field])
        fs_a=a['native']['files'];fs_b=b['native']['files']
        need(set(fs_b['entries'])==set(fs_a['entries'])|{added},'Native upload inventory differs')
        for n,v in fs_a['entries'].items():need(eq(v,fs_b['entries'][n]),'Existing native file metadata changed')
        for k in ['entries','count','total_bytes']:fs_b[k]=copy.deepcopy(fs_a[k])
        # A hidden, zero-byte derivative may be created only for the added PDF.
        ma=a['native']['media_files'];mb=b['native']['media_files'];extra=set(mb['entries'])-set(ma['entries'])
        need(extra<=({added+'.ptif'} if added.endswith('.pdf') else set()) and set(ma['entries'])<=set(mb['entries']),'Unrelated derived media change')
        for n,v in ma['entries'].items():need(eq(v,mb['entries'][n]),'Existing derived-media semantics changed')
        if extra:
            for k in ['entries','count','enabled']:mb[k]=copy.deepcopy(ma[k])
    elif transition=='publish':
        need(first['published'] is False and last['published'] is True,'Invalid publish phase')
        b['legacy']['submitted']=a['legacy']['submitted'];b['legacy']['state']=a['legacy']['state']
        for k in ['is_published','is_draft','status']:b['native'][k]=a['native'][k]
        # Both complete pids objects already passed the exact typed native policy.
        b['native']['pids']=copy.deepcopy(a['native']['pids'])
        for role in ['legacy','native','file_collection']:
            if 'links' in a[role] and 'links' in b[role]:phase_links(a[role]['links'],b[role]['links'],first['record'])
        for role,field in [('legacy','files'),('file_collection','entries')]:
            old=file_map(a[role],field);new=file_map(b[role],field)
            need(set(old)==set(new),'Publication raw files changed')
            for n in old:
                if 'links' in old[n] and 'links' in new[n]:phase_links(old[n]['links'],new[n]['links'],first['record'])
            a[role][field]=[old[n]for n in sorted(old)];b[role][field]=[new[n]for n in sorted(new)]
        for field in ['files','media_files']:
            old=a['native'][field]['entries'];new=b['native'][field]['entries']
            need(set(old)==set(new),'Publication native inventory changed')
            for n in old:
                if 'links'in old[n] and 'links'in new[n]:phase_links(old[n]['links'],new[n]['links'],first['record'])
                else:need('links'not in old[n] and 'links'not in new[n],'Unreviewed missing native file links')
        if 'ui' in a['native'] and 'ui' in b['native'] and 'is_draft' in a['native']['ui'] and 'is_draft' in b['native']['ui']:
            if a['native']['ui']['is_draft'] is True and b['native']['ui']['is_draft'] is False:b['native']['ui']['is_draft']=True
    else:need(first['published'] is last['published'],'Unintended publication transition')
    # Treat named file-list order as presentation only; every entry remains whole.
    for obj in [a,b]:
        for role,field in [('legacy','files'),('file_collection','entries')]:
            named=file_map(obj[role],field);obj[role][field]=[named[n]for n in sorted(named)]
    need(eq(a,b),'Complete typed legacy/native/file/media semantics changed')
    if transition!='publish':need(eq(first['bucket'],last['bucket']),'Target upload bucket changed')
def public_owner(value,verified_owner):
    validate_types('public',value)
    need(type(verified_owner) is int and verified_owner>0,'Invalid verified native owner')
    need(value['owners'][0]['id']==str(verified_owner),'Public owner differs from exact native owner')
    return verified_owner
def public_aliases(value,intended,verified):
    record=verified['record'];need(verified['published']is True,'Public verification lacks a published native context')
    need(type(value['recid'])is str and re.fullmatch('[1-9][0-9]*',value['recid']) and value['recid']==str(record),'Public duplicate recid contradicts native record')
    need(type(value['title'])is str and value['title']==intended['title'],'Public duplicate title contradicts intended title')
    raw=verified['semantic17'];native=raw['native'];legacy=raw['legacy']
    need(type(value['revision'])is int and value['revision']==native['revision_id'],'Public revision alias contradicts native revision')
    for key,source in [('created',native['created']),('updated',native['updated']),('modified',legacy['modified'])]:
        need(PHASE.timestamp(value[key])==PHASE.timestamp(source),'Public timestamp alias contradicts verified '+key)
    need(eq(value['swh'],native.get('swh',{})),'Public SWH decoration contradicts native context')
    files=value['files'];need(type(files)is list and len(files)==len(verified['files']),'Public complete file inventory differs')
    seen=set()
    for entry in files:
        need(type(entry)is dict and set(entry)=={'id','key','size','checksum','links'},'Unreviewed public file envelope')
        name=entry['key'];need(type(name)is str and name in verified['files'] and name not in seen,'Public filename missing/duplicate/foreign');seen.add(name)
        wanted=verified['files'][name];identifier=entry['id']
        need(type(identifier)is str,'Public file UUID type')
        try:canonical=str(uuid.UUID(identifier))
        except (ValueError,AttributeError):raise RuntimeError('Public file UUID malformed')
        need(identifier==canonical==wanted['file_id'],'Public file UUID contradicts finalized native identity')
        need(type(entry['size'])is int and entry['size']==wanted['size'],'Public file typed size contradicts intended/native file')
        need(type(entry['checksum'])is str and entry['checksum']==wanted['checksum'],'Public file checksum contradicts intended/native file')
        route='https://zenodo.org/api/records/'+str(record)+'/files/'+quote(name,safe='')+'/content'
        need(type(entry['links'])is dict and set(entry['links'])=={'self'} and type(entry['links']['self'])is str and entry['links']['self']==route,'Public file content route contradicts target/name')
    need(seen==set(verified['files']),'Public file set differs from verified finalized collection')
def install(c,pl,old,typed_equal):
    global TYPED_EQUAL
    TYPED_EQUAL=typed_equal;original=old.validate_target;public_original=old.public_projection
    def validate(legacy,native,collection,*args,**kwargs):
        for role,v in [('legacy',legacy),('native',native),('file_collection',collection)]:validate_types(role,v)
        record=args[2] if len(args)>2 else kwargs['record'];published=args[3] if len(args)>3 else kwargs['published']
        intended=args[0]if args else kwargs['intended']
        L,N,F=PHASE.prepare(legacy,native,collection,record,published,intended)
        result=original(L,N,F,*args,**kwargs)
        result['semantic17']=copy.deepcopy({'legacy':legacy,'native':native,'file_collection':collection})
        result['phase17']={'published':published,'doi_basis':'actual_published_PID' if published else 'exact_legacy_prereservation',
            'native_record_PID_present':bool(native['pids']),'native_parent_PID_present':bool(native['parent']['pids']),
            'raw_complete_objects_retained':True}
        return result
    def public(value,intended,verified):
        # The live unauthenticated route has one {id: canonical-decimal-string}
        # owner. Keep every raw field; adapt ONLY this checked ownership value
        # around the immutable projector's preexisting integer-owner contract.
        owner=public_owner(value,verified['owner'])
        public_aliases(value,intended,verified)
        names={e.get('filename',e.get('key')) for e in value['files']}
        PHASE.top_links(value,'native',verified['record'],verified['concept'],True,names)
        compatibility=copy.deepcopy(value);compatibility['owners']=[owner]
        return public_original(compatibility,intended,verified)
    old.validate_target=validate;old.public_projection=public;pl.observe_target=old.observe;pl.public_projection=public
