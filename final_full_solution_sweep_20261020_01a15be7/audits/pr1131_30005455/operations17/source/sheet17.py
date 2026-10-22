"""Type-strict full numeric43-column/value/FORMULA/raw-metadata preservation."""
if not globals().get('_OPS17_VERIFIED',False):raise RuntimeError('Use verified17 bootstrap')
import copy,json,math
C=None
def need(v,m):
    if not v:raise RuntimeError(m)
def json_types(value,depth=0):
    need(depth<=64,'JSON nesting bound exceeded')
    t=type(value)
    need(t in {dict,list,str,int,float,bool,type(None)},'Non-JSON provider value')
    if t is float:need(math.isfinite(value),'Nonfinite provider number')
    if t is dict:
        need(all(type(k) is str for k in value),'Non-string provider key')
        for v in value.values():json_types(v,depth+1)
    if t is list:
        for v in value:json_types(v,depth+1)
def typed_equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(typed_equal(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(typed_equal(x,y) for x,y in zip(a,b))
    return a==b
def metadata(book):
    json_types(book);identity=C.sheet_identity(book)
    for sheet in book['sheets']:
        p=sheet['properties']
        for name in ['hidden','rightToLeft']:
            if name in p:need(type(p[name]) is bool,'Malformed sheet Boolean property '+name)
        grid=p.get('gridProperties',{})
        for name in ['rowCount','columnCount','frozenRowCount','frozenColumnCount']:
            if name in grid:need(type(grid[name]) is int and grid[name]>=0,'Malformed integer grid property')
        for name in ['hideGridlines','rowGroupControlAfter','columnGroupControlAfter']:
            if name in grid:need(type(grid[name]) is bool,'Malformed Boolean grid property')
    return identity
def get_metadata():
    book=C.command(['gws','sheets','spreadsheets','get','--params',json.dumps({'spreadsheetId':C.SHEET,'includeGridData':False})])
    return book,metadata(book)
def read():
    start=C.stamp();book,identity=get_metadata()
    grid={'sheetId':C.SHEET_ID,'startColumnIndex':0,'endColumnIndex':43}
    responses=[]
    for mode in ['UNFORMATTED_VALUE','FORMULA']:
        body={'dataFilters':[{'gridRange':grid}],'majorDimension':'ROWS','valueRenderOption':mode}
        r=C.command(['gws','sheets','spreadsheets','values','batchGetByDataFilter','--params',json.dumps({'spreadsheetId':C.SHEET}),'--json',json.dumps(body)])
        json_types(r)
        need(type(r) is dict and r.get('spreadsheetId')==C.SHEET,'Numeric ledger workbook changed')
        ranges=r.get('valueRanges');need(type(ranges) is list and len(ranges)==1 and type(ranges[0]) is dict,'Numeric range count changed')
        matched=ranges[0]
        need(typed_equal(matched.get('dataFilters'),[{'gridRange':grid}]),'Numeric grid echo recursively differs in type/value')
        value=matched.get('valueRange')
        need(type(value) is dict and value.get('majorDimension')=='ROWS'
             and value.get('range') in {"'Math Puzzles'!A1:AQ"+str(identity['row_count']),"Math Puzzles!A1:AQ"+str(identity['row_count'])},'Full numeric range/ROWS changed')
        rows=value.get('values')
        need(type(rows) is list and rows and typed_equal(rows[0],C.HEADERS)
             and all(type(row) is list and len(row)<=4 and all(type(cell) is str for cell in row) for row in rows),
             'Ledger outside exact four-cell schema')
        need(len(rows)<=identity['row_count'],'Ledger exceeds allocated grid')
        responses.append(r)
    need(typed_equal(*responses),'Formula/unformatted numeric ledger views differ in type/value')
    after,after_identity=get_metadata()
    need(typed_equal(book,after) and typed_equal(identity,after_identity),'Full raw sheet metadata changed between paired GETs')
    value=responses[0]['valueRanges'][0]['valueRange']
    return {**value,'identity':identity,'metadata_before':book,'metadata_after':after,
            'numeric_response':responses[0],'numeric_formula_response':responses[1],'observed_at':start},value['values']
def preserve(before,after,rows):
    need(typed_equal(before['metadata_before'],after['metadata_before'])
         and typed_equal(before['metadata_after'],after['metadata_after']),
         'Complete raw sheet metadata changed across ledger boundary')
    for key in ['numeric_response','numeric_formula_response']:
        expected=copy.deepcopy(before[key])
        expected['valueRanges'][0]['valueRange']['values']=rows
        need(typed_equal(expected,after[key]),'Complete numeric response/old rows changed across ledger boundary')
def append_response(response,before):
    json_types(response)
    required={'spreadsheetId','replies'}
    allowed=[required|{'updatedSpreadsheet'},required|{'commentUpdateState'},required|{'updatedSpreadsheet','commentUpdateState'}]
    need(type(response) is dict and set(response)in allowed
         and response['spreadsheetId']==C.SHEET and typed_equal(response['replies'],[{}]),'Malformed literal append response')
    if 'commentUpdateState'in response:need(type(response['commentUpdateState'])is str and response['commentUpdateState']=='NO_UPDATES_REQUESTED','Unreviewed append comment-update state')
    if 'updatedSpreadsheet'in response:
        metadata(response['updatedSpreadsheet'])
        need(typed_equal(response['updatedSpreadsheet'],before['metadata_before']),'Append response full raw sheet metadata changed')
