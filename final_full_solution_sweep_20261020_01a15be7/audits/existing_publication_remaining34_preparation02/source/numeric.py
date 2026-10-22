"""Full raw spreadsheet metadata and strict numeric43-column dual views."""
from ops_core import require,typed_equal,strict_json
BOOK='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
GID=1254632077
SCHEMA=['Original Problem','Solution Chat URL','DOI','Notes']

def target(raw):
    require(type(raw) is dict and raw.get('spreadsheetId')==BOOK,'Wrong metadata workbook')
    require(type(raw.get('sheets')) is list,'Missing full metadata sheets')
    found=[s['properties'] for s in raw['sheets'] if type(s) is dict and type(s.get('properties')) is dict and type(s['properties'].get('sheetId')) is int and s['properties']['sheetId']==GID]
    require(len(found)==1,'Numeric sheet not unique')
    s=found[0];g=s.get('gridProperties')
    require(s.get('title')=='Math Puzzles' and s.get('sheetType')=='GRID' and type(g) is dict,'Wrong sheet identity')
    require(type(g.get('columnCount')) is int and g['columnCount']==43 and type(g.get('rowCount')) is int and g['rowCount']>0,'Wrong typed full extent')
    require(typed_equal(raw,raw),'Malformed recursive metadata JSON')
    return s

def metadata(provider):
    raw=provider.gws(['get'],{'spreadsheetId':BOOK,'includeGridData':False})
    target(raw)
    return raw

def read(provider,mode,meta):
    require(mode in ['UNFORMATTED_VALUE','FORMULA'],'Invalid render mode')
    s=target(meta)
    filters=[{'gridRange':{'sheetId':GID,'startRowIndex':0,'endRowIndex':s['gridProperties']['rowCount'],'startColumnIndex':0,'endColumnIndex':43}}]
    raw=provider.gws(['values','batchGetByDataFilter'],{'spreadsheetId':BOOK},{'dataFilters':filters,'majorDimension':'ROWS','valueRenderOption':mode})
    require(type(raw) is dict and raw.get('spreadsheetId')==BOOK,'Wrong read workbook')
    matches=raw.get('valueRanges');require(type(matches) is list and len(matches)==1,'Wrong range match count')
    match=matches[0];require(type(match) is dict and typed_equal(match.get('dataFilters'),filters),'Typed numeric range echo changed')
    value=match.get('valueRange');require(type(value) is dict,'Missing valueRange')
    require(value.get('range')=="'Math Puzzles'!A1:AQ"+str(s['gridProperties']['rowCount']) and value.get('majorDimension')=='ROWS','Range extent changed')
    rows=value.get('values');require(type(rows) is list and bool(rows) and typed_equal(rows[0],SCHEMA),'Header changed')
    require(all(type(row) is list and len(row)<=43 and all(type(c) in (str,int,float,bool) and typed_equal(c,c) for c in row) for row in rows),'Invalid typed rows')
    require(len(rows)<=s['gridProperties']['rowCount'],'Rows beyond grid capacity')
    return raw,rows

def observe(provider,expected=None):
    first=metadata(provider)
    vr,values=read(provider,'UNFORMATTED_VALUE',first)
    fr,formulas=read(provider,'FORMULA',first)
    last=metadata(provider)
    require(typed_equal(first,last),'Complete raw metadata drift between paired GETs')
    require(typed_equal(vr,fr) and typed_equal(values,formulas),'Complete typed VALUE/FORMULA response mismatch')
    result={'metadata':first,'value_raw':vr,'formula_raw':fr,'values':values,'formulas':formulas}
    if expected is not None:
        require(typed_equal(result,expected),'Any full43-column view/header/range/full-metadata drift')
    return result
