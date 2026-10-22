"""New whole-main controls derived from the exact197/181 corpus, independent of parser semantics."""
STATS=['downloads','unique_downloads','version_downloads','version_unique_downloads','views','unique_views','version_views','version_unique_views']
def fresh_cases():
    out=[]
    def add(name,cfg=None,expect='reject',appends=0):out.append({'name':'new02_'+name,'cfg':cfg or {},'expect':expect,'appends':appends})
    row=copy.deepcopy(BASE_PLAN['proposed_row'])
    add('actual197_181_positive',expect='pass',appends=1)
    add('fresh197_counter152_positive',{'fresh_account':True},'pass',1)
    add('reordered_account_inventory_positive',{'edit_account':lambda r:r.reverse()},'pass',1)
    for size in [1,7,24,26,196,197]:add('account_page_size_'+str(size),{'page_size':size},'pass',1)
    add('missing_acceptance',{'missing_acceptance':True})
    add('acceptance_after_external_pin_change',{'edit_acceptance_file':lambda p:p.write_bytes(p.read_bytes()+b' ')})
    add('unreviewed_helper_bytes',{'helper_changed':True})
    for name in ['source_14_account.json','source_10_ledger_live.json']:
        add('missing_corpus_'+name,{'missing_corpus':name})
        add('corrupt_corpus_'+name,{'corrupt_corpus':name})
    for field in STATS:
        for bad in [True,False,1.0,'1',None,-1,[],{'downloads':1}]:
            add('stats_'+field+'_bad_'+repr(bad),{'edit_account':lambda r,k=field,v=bad:r[0]['stats'].__setitem__(k,v)})
        for good in [0,10**60]:
            add('stats_'+field+'_allowed_'+str(good),{'edit_account':lambda r,k=field,v=good:r[0]['stats'].__setitem__(k,v)},'pass',1)
        add('stats_'+field+'_removed',{'edit_account':lambda r,k=field:r[0]['stats'].pop(k)})
    add('stats_new_integer_counter_forbidden',{'edit_account':lambda r:r[0]['stats'].__setitem__('downloads_v2',12)})
    add('stats_nested_exception_forbidden',{'edit_account':lambda r:r[0]['metadata'].__setitem__('stats',{'downloads':10})})
    add('new_unrelated_record',{'edit_account':lambda r:r.append(clean_record(90000001))})
    add('remove_last_record',{'edit_account':lambda r:r.pop()})
    add('duplicate_record_id',{'edit_account':lambda r:r.append(copy.deepcopy(r[0]))})
    add('swap_one_record_id',{'edit_account':lambda r:r[0].__setitem__('id',90000001)})
    # Enumerate every observed recursively normalized path/type shape across all197
    # records. No fixture expected-path strings are invented by the target.
    shapes={}
    def walk(v,path,index):
        shape=tuple('*' if type(k) is int else k for k in path)+(type(v).__name__,)
        shapes.setdefault(shape,(index,path,v))
        if isinstance(v,dict):
            for k,x in v.items():walk(x,path+(k,),index)
        elif isinstance(v,list):
            for k,x in enumerate(v):walk(x,path+(k,),index)
    for index,r in enumerate(ACTUAL_ACCOUNT['records']):walk(r,(),index)
    def replace_at(records,index,path,value):
        obj=records[index]
        for k in path[:-1]:obj=obj[k]
        if path:obj[path[-1]]=copy.deepcopy(value)
        else:records[index]=copy.deepcopy(value)
    for n,(shape,(index,path,value)) in enumerate(shapes.items()):
        label=str(n)+'_'+'.'.join(map(str,path))
        # Change every observed type, including booleans/None and stats ints.
        bad=[] if not isinstance(value,list) else {}
        add('shape_type_'+label,{'edit_account':lambda r,i=index,p=path,v=bad:replace_at(r,i,p,v)})
        iscounter=len(path)==2 and path[0]=='stats' and path[1] in STATS
        if not iscounter and not isinstance(value,(dict,list)):
            altered=(value+'\u200b') if isinstance(value,str) else not value if type(value) is bool else value+1 if type(value) is int else 'unexpected'
            add('shape_scalar_'+label,{'edit_account':lambda r,i=index,p=path,v=altered:replace_at(r,i,p,v)})
        if isinstance(value,dict):
            def edit(r,i=index,p=path):
                obj=r[i]
                for k in p:obj=obj[k]
                obj['NEW_<a href="https://doi.org/10.5281/zenodo.&#50;3350364">']=0
            add('shape_new_key_'+label,{'edit_account':edit})
        elif isinstance(value,list):
            def edit(r,i=index,p=path):
                obj=r[i]
                for k in p:obj=obj[k]
                obj.append(copy.deepcopy(obj[0]) if obj else 'new')
            add('shape_list_length_'+label,{'edit_account':edit})
            if len(value)>1 and value!=value[::-1]:
                def edit(r,i=index,p=path):
                    obj=r[i]
                    for k in p:obj=obj[k]
                    obj.reverse()
                add('shape_list_order_'+label,{'edit_account':edit})
        if path and isinstance(path[-1],str):
            def edit(r,i=index,p=path):
                obj=r[i]
                for k in p[:-1]:obj=obj[k]
                del obj[p[-1]]
            add('shape_removed_key_'+label,{'edit_account':edit})
    aliases=[
        '<a href="https://doi.org/10.5281/zenodo.&#50;3350364">same result</a>',
        '&#49;&#48;.5281/zenodo.23350364',
        'https://doi.org/10.5281/zenodo.２３３５０３６４',
        'https://doi.org/10.5281/zenodo.23350\u200b364',
        'https://unrecognized.invalid/alias',
        'https%253A%252F%252Fshortdoi.org%252Funknown',
        'https://doi.org/10.5281/zenodo.23350364?unexpected=1#extra',
        'ordinary unrelated text',
    ]
    for n,value in enumerate(aliases):
        for col in range(4):
            add('new_row_'+str(n)+'_col'+str(col),{'edit_rows':lambda r,c=col,v=value:r.append(['' if i!=c else v for i in range(4)])})
            add('change_cell_'+str(n)+'_col'+str(col),{'edit_rows':lambda r,c=col,v=value:r[1].__setitem__(c,v)})
            # Main v1 defect, with every cell position and both opaque and known
            # text: exact182 before ->183/changed182 after must reject0append.
            add('idempotent_postread_extra_'+str(n)+'_col'+str(col),{'edit_rows':lambda r:r.append(copy.deepcopy(row)),'edit_immediate_rows':lambda r,c=col,v=value:r.append(['' if i!=c else v for i in range(4)])})
            add('idempotent_postread_changed_'+str(n)+'_col'+str(col),{'edit_rows':lambda r:r.append(copy.deepcopy(row)),'edit_immediate_rows':lambda r,c=col,v=value:r[1].__setitem__(c,v)})
        for field in ['links','metadata','pids','parent']:
            def edit(r,k=field,v=value):
                if k=='links':r[-1][k]['self']=v
                elif k=='metadata':r[-1][k]['description']=v
                else:r[-1][k]={'id':v}
            add('account_late_alias_'+str(n)+'_'+field,{'edit_account':edit})
    for step in ['before','immediate','after','idempotent_after']:
        for fault in ['delete','reverse','duplicate','fifthcolumn','unknownrow']:
            def edit(r,f=fault):
                if f=='delete':r.pop(3)
                elif f=='reverse':r[1:3]=r[1:3][::-1]
                elif f=='duplicate':r.append(copy.deepcopy(r[1]))
                elif f=='fifthcolumn':r[2].append('unknown')
                else:r.append(['unreviewed','','',''])
            cfg={};appends=0
            if step=='before':cfg['edit_rows']=edit
            elif step=='immediate':cfg['edit_immediate_rows']=edit
            elif step=='after':cfg['edit_after_rows']=edit;appends=1
            else:cfg={'edit_rows':lambda r:r.append(copy.deepcopy(row)),'edit_immediate_rows':edit}
            add('ledger_'+step+'_'+fault,cfg,appends=appends)
    for field in ['head','base','body','state','merged','draft']:
        for step in ['initial','immediate']:
            def edit(r,k=field):
                if k in {'head','base'}:r[k]['sha']='f'*40
                elif k=='body':r[k]+=' '
                elif k=='state':r[k]='closed'
                else:r[k]=not r[k]
            # Initial state is not hard-coded by plan, so state can already be
            # closed/merged/non-draft. This is observational, no PR operation.
            expect='pass' if step=='initial' and field in {'state','merged','draft'} else 'reject'
            add('pr_'+step+'_'+field,{'edit_pr' if step=='initial' else 'edit_final_pr':edit},expect,1 if expect=='pass' else 0)
    for field in ['updatedCells','updatedRows','updatedColumns']:
        for bad in [True,False,'1',-1,0,None,1.0 if field=='updatedRows' else 4.0]:
            add('response_bad_'+field+'_'+repr(bad),{'edit_response':lambda r,k=field,v=bad:r['updates'].__setitem__(k,v)},appends=1)
    for url in ['https://zenodo.org/records/23350364#fragment','https://zenodo.org/records/23350364?x=1','https://zenodo.org:443/records/23350364','https://ZENODO.org/records/23350364','https://zenodo.org/records/%32%33%33%35%30%33%36%34','https://zenodo.org/records/233503640']:
        add('doi_reject_'+url,{'doi_url':url})
    for total in [True,197.0,'197',-1,None,{'value':197,'relation':'gte'}]:
        add('pagination_invalid_total_'+repr(total),{'edit_page':lambda r,n,v=total:r['hits'].__setitem__('total',v)})
    for url in ['http://zenodo.org/api/user/records?page=2','https://zenodo.org:443/api/user/records?page=2','https://zenodo.org@evil.invalid/api/user/records?page=2','https://evil.invalid/api/user/records?page=2']:
        add('pagination_invalid_next_'+url,{'edit_page':lambda r,n,v=url:r['links'].__setitem__('next',v)})
    add('pagination_reorder_entries_positive',{'edit_page':lambda r,n:r['hits']['hits'].reverse()},'pass',1)
    # Precisely record no-write idempotence boundaries; these expectations do
    # not certify observation freshness or a distributed transaction.
    add('idempotent_expired_observations_boundary',{'exact_age':181,'edit_rows':lambda r:r.append(copy.deepcopy(row))},'pass')
    add('idempotent_no_second_PR_read_boundary',{'edit_rows':lambda r:r.append(copy.deepcopy(row)),'edit_final_pr':lambda p:p['head'].__setitem__('sha','f'*40)},'pass')
    return out

def cases():
    inherited=inherited_cases()
    # Prior generic parser controls adding unrelated data are inadmissible for
    # finite profile. Exact existing planned row remains intentionally accepted.
    for c in inherited:
        if c['expect']=='pass' and ('edit_rows' in c['cfg'] or 'edit_account' in c['cfg']) and c['name'] not in {'exact_existing_row_idempotent','retry_known_exact_row_with_intent_is_idempotent'}:
            c['expect']='reject';c['appends']=0
    return inherited+fresh_cases()
