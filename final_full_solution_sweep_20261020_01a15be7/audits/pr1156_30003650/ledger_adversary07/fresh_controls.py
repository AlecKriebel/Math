"""Independent review07 full-main fixtures, consumed by offline_whole_helper."""
def fresh_cases():
    out=[]
    def add(name,cfg=None,expect='reject',appends=0):out.append({'name':'v7_'+name,'cfg':cfg or {},'expect':expect,'appends':appends})
    def putlink(location,url):
        def edit(records):
            item=records[1]
            if location=='links':item['links']={'probe':url}
            elif location=='parent.links':item['parent']={'id':'90000003','links':{'probe':url}}
            elif location=='files.links':item['files']=[{'checksum':'md5:'+'0'*32,'links':{'probe':url}}]
            else:raise RuntimeError('Bad fixture location')
        return edit
    locations=['links','parent.links','files.links']
    routes=[
      '/api/records/90000001','/records/90000001/',
      '/api/records/90000001/draft','/api/records/90000001/draft/pids/doi',
      '/api/records/90000001/draft/files','/api/records/90000001/draft/media-files',
      '/api/records/90000001/draft/actions/publish','/api/records/90000001/draft/review',
      '/api/records/90000001/files','/api/records/90000001/files/a.bin/content',
      '/api/records/90000001/media-files','/api/records/90000001/versions',
      '/api/records/90000001/versions/latest','/api/records/90000001/latest',
      '/api/records/90000001/access','/api/records/90000001/access/links',
      '/api/records/90000001/access/grants','/api/records/90000001/access/users',
      '/api/records/90000001/access/request','/api/records/90000001/communities',
      '/api/records/90000001/communities-suggestions','/api/records/90000001/request-deletion',
      '/api/records/90000001/file-modification','/api/records/90000001/quota-increase',
      '/api/records/90000001/requests','/api/records/90000001/export/json',
      '/uploads/90000001','/api/iiif/record:90000001/manifest',
      '/api/iiif/draft:90000001/info.json','/doi/10.5281/zenodo.90000001']
    for loc in locations:
        for route in routes:
            add('owned_route_'+loc+'_'+route,{'edit_account':putlink(loc,'https://zenodo.org'+route)},'pass',1)
    add('actual197_native_account_and_actual181_ledger',{'actual_account':True},'pass',1)
    for loc in locations:
        for route in ['/api/records/90000001/unknown-route','/api/user/90000001','/api/iiif/unknown:90000001/manifest','/api/records/90000001/draft/unknown','/uploads/99999999','/api/records/99999999/quota-increase']:
            if route.endswith('/draft/unknown'):
                # This is unprojected but the established binding deliberately
                # recognizes draft descendants as a parent-record lead.
                add('unknown_route_visible_'+loc+'_'+route,{'edit_account':putlink(loc,'https://zenodo.org'+route)},'pass',1)
            else:add('unknown_route_visible_'+loc+'_'+route,{'edit_account':putlink(loc,'https://zenodo.org'+route)})
        for prefix in ['https://zenodo.org:443','http://zenodo.org','https://www.zenodo.org','https://zenodo.org.','https://user@zenodo.org','https://zenodo.org:8443','HTTPS://ZENODO.ORG','//zenodo.org']:
            add('nonprojected_authority_'+loc+'_'+prefix,{'edit_account':putlink(loc,prefix+'/api/iiif/record:90000001/manifest')})
        for value in ['https://foreign.invalid/api/iiif/record:90000001/manifest','https://zenodo.org.evil.invalid/api/iiif/record:90000001/manifest']:
            add('nonofficial_nonlead_'+loc+'_'+value,{'edit_account':putlink(loc,value)},'pass',1)
        # Query and file/IIIF suffix content must retain unresolved leads. No
        # assertion about URI equivalence, redirection or target identity.
        encode=lambda s:''.join('%'+format(c,'02X') for c in s.encode())
        for label,lead in [('short_resolver','//shortdoi.org/abc'),('bare_long_target',encode('10.5281/zenodo.23350364')),('encoded_concept',encode('https://zenodo.org/records/23350363')),('encoded_resolver',encode('//doi.org/abc'))]:
            for slot,path in [('query','/api/records/90000001?related='+lead),('file_suffix','/api/records/90000001/files/'+lead),('iiif_suffix','/api/iiif/record:90000001/'+lead)]:
                add('preserve_hidden_lead_'+loc+'_'+slot+'_'+label,{'edit_account':putlink(loc,'https://zenodo.org'+path)})
        for lead in ['CP-plus rank theorem','OWR-15957-003','PR #1156','30003650']:
            add('raw_semantic_not_suppressed_'+loc+'_'+lead,{'edit_account':putlink(loc,'https://zenodo.org/api/records/90000001?title='+lead)})
        add('fragment_not_projected_'+loc,{'edit_account':putlink(loc,'https://zenodo.org/api/iiif/record:90000001/manifest#//shortdoi.org/abc')})
    for field in ['metadata','pids','arbitrary_raw','parent_metadata']:
        for lead in ['//doi.org/abc','https://zenodo.org/api/iiif/record:90000001/manifest','%31%30%2E%35%32%38%31%2F%7A%65%6E%6F%64%6F%2E%32%33%33%35%30%33%36%34']:
            def edit(records,f=field,v=lead):
                if f=='parent_metadata':records[1]['parent']={'id':'90000003','metadata':{'unknown':v}}
                else:records[1][f]={'unknown':v}
            add('unprojected_field_'+field+'_'+lead,{'edit_account':edit})
    for f in BASE_PLAN['existing_publication']['files']:
        def edit(records,c=f['checksum']):records[1]['files']=[{'checksum':c,'links':{'self':'https://zenodo.org/api/records/90000001/files/content'}}]
        add('md5_independent_of_projection_'+f['name'],{'edit_account':edit})
    for text in ['Oberwolfach Report 10/2025; DOI 10.4171/OWR/2025/10','OWR 10/2025; https://doi.org/10.4171/owr/2025/10','OWR 10/1999; 10.4171/owr/1999/10','oBeRwOlFaCh RePoRt 10/2025; 10.4171/OWR/2025/10']:
        add('typed_bibliography_'+text,{'edit_account':lambda r,v=text:r[1]['metadata'].__setitem__('description',v)},'pass',1)
    bibliography_negatives=[
      'Oberwolfach Report 10/2025',
      'Oberwolfach Report 10/2025; 10.4171/OWR/2024/10',
      'Oberwolfach Report 10/2025; 10.4171/OWR/2025/11',
      'Report 10/2025; 10.4171/OWR/2025/10',
      '10/2025; 10.4171/OWR/2025/10',
      'OWR 10/2025; 10.4171/OWR/2025/10EXTRA',
      'OWR 10/2025; 10.4171/OWR/2025/100',
      'OWR 10/2025; https://doi.org/10.4171/OWR/2025/10; separately 10/abc',
      'Oberwolfach Report 10/2025; 10.4171/OWR/2025/10; //doi.org/abc',
      'OWR 10/2025; 10.4171/OWR/2025/10; separately 10/2025',
      'OWR 10/2025; 10.4171/OWR/2025/10; https://shortdoi.org/abc',
      'OWR 10/2025; 10.4171/OWR/2025/10; %31%30%2F%61%62%63',
      'OWR 10/2025; 110.4171/OWR/2025/10',
      'OWR 10/2025; x10.4171/OWR/2025/10',
    ]
    for text in bibliography_negatives:
        add('bibliography_negative_'+text,{'edit_account':lambda r,v=text:r[1]['metadata'].__setitem__('description',v)})
    for lead in ['CP-plus rank theorem','%31%30%2E%35%32%38%31%2F%7A%65%6E%6F%64%6F%2E%32%33%33%35%30%33%36%34','//doi.org/abc']:
        def edit(records,v=lead):
            item=records[1];item['metadata']['description']='OWR 10/2025; 10.4171/OWR/2025/10';item['arbitrary_raw']=v
        add('bibliography_other_field_survives_'+lead,{'edit_account':edit})
    def actual_drop_control(r):r[:]=[x for x in r if x['id']!=23408971]
    add('actual197_positive_record_required',{'actual_account':True,'edit_account':actual_drop_control})
    add('actual197_target_added',{'actual_account':True,'edit_account':lambda r:r.append(clean_record(23350364))})
    add('actual197_unknown_resolver_added',{'actual_account':True,'edit_account':lambda r:r[0]['metadata'].__setitem__('new_probe','//shortdoi.org/abc')})
    return out
