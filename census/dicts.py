__CODE_TO_STNAME = {
    'AK':'Alaska', 'AL':'Alabama', 'AR':'Arkansas', 'AZ':'Arizona','CA':'California', 
    'CO':'Colorado', 'CT':'Connecticut', 'DE':'Delaware', 'FL':'Florida', 'GA':'Georgia', 
    'HI':'Hawaii', 'IA':'Iowa', 'ID':'Idaho', 'IL':'Illinois', 'IN':'Indiana', 
    'KS':'Kansas', 'KY':'Kentucky', 'LA':'Louisiana', 'MA':'Massachusetts', 'MD':'Maryland', 
    'ME':'Maine', 'MI':'Michigan', 'MN':'Minnesota', 'MO':'Missouri', 'MS':'Mississippi', 
    'MT':'Montana', 'NC':'North Carolina', 'ND':'North Dakota', 'NE':'Nebraska', 'NH':'New Hampshire', 
    'NJ':'New Jersey', 'NM':'New Mexico', 'NV':'Nevada', 'NY':'New York', 'OH':'Ohio', 
    'OK':'Oklahoma', 'OR':'Oregon', 'PA':'Pennsylvania', 'RI':'Rhode Island', 'SC':'South Carolina', 
    'SD':'South Dakota', 'TN':'Tennessee', 'TX':'Texas', 'UT':'Utah', 'VA':'Virginia', 
    'VT':'Vermont', 'WA':'Washington', 'WI':'Wisconsin', 'WV':'West Virginia', 'WY':'Wyoming'
}

def __make_code_to_stname(code_to_stname):
    stname_to_code = {}
    for code in code_to_stname:
        stname_to_code[code_to_stname[code]] = code
    return stname_to_code

def __make_fips_to_stname(code_to_stname):
    fips_to_stname = {}
    for i, (code) in enumerate(code_to_stname):
        stname = code_to_stname[code]
        fips_code = i + 1
        if fips_code < 10:
            fips_code = f"0{fips_code}"
        else:
            fips_code = f"{fips_code}"
        fips_to_stname[fips_code] = stname
    return fips_to_stname

__STNAME_TO_CODE = __make_code_to_stname(__CODE_TO_STNAME)
__FIPS_TO_STNAME = __make_fips_to_stname(__CODE_TO_STNAME)

def stname_from_code(code):
    code = code.upper()
    return __CODE_TO_STNAME.get(code)

def stname_from_fips(fips_code):
    return __FIPS_TO_STNAME.get(fips_code)

def code_from_stname(stname):
    return __STNAME_TO_CODE.get(stname)

if __name__ == '__main__':
    print(stname_from_fips('49'))