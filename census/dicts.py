

CODE_TO_STNAME = {
    'AK':'Alaska', 'AL':'Alabama', 'AR':'Arkansas', 'AZ':'Arizona','CA':'California', 
    'CO':'Colorado', 'CT':'Connecticut', 'DE':'Delaware', 'FL':'Florida', 'GA':'Georgia', 
    'HI':'Hawaii', 'IA':'Iowa', 'ID':'Idaho', 'IL':'Illinois', 'IN':'Indiana', 
    'KS':'Kansas', 'KY':'Kentucky', 'LA':'Louisiana', 'MA':'Massachusetts', 'MD':'Maryland', 
    'ME':'Maine', 'MI':'Michigan', 'MN':'Minnesota', 'MO':'Missouri', 'MS':'Mississippi', 
    'MT':'Montana', 'NC':'North Carolina', 'ND':'North Dakota', 'NE':'Nebraksa', 'NH':'New Hampshire', 
    'NJ':'New Jersey', 'NM':'New Mexico ', 'NV':'Nevada', 'NY':'New York', 'OH':'Ohio', 
    'OK':'Oklahoma', 'OR':'Oregan', 'PA':'Pennsylvania', 'RI':'Rhode Island', 'SC':'South Carolina', 
    'SD':'South Dakota', 'TN':'Tennessee', 'TX':'Texas', 'UT':'Utah', 'VA':'Virginia', 
    'VT':'Vermont', 'WA':'Washington', 'WI':'Wisconsin', 'WV':'West Virginia', 'WY':'Wyoming'
}

def make_code_to_stname(code_to_stname):
    stname_to_code = {}
    for code in code_to_stname:
        stname_to_code[code_to_stname[code]] = code
    return stname_to_code


STNAME_TO_CODE = make_code_to_stname(CODE_TO_STNAME)
print(STNAME_TO_CODE)
def stname_from_code(code):
    code = code.upper()
    return CODE_TO_STNAME[code]


