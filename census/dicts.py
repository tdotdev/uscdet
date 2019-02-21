__CODE_TO_STNAME = {
    'AL':'Alabama', 'AK':'Alaska', 'AZ':'Arizona', 'AR':'Arkansas', 'CA':'California', 
    'CO':'Colorado', 'CT':'Connecticut', 'DE':'Delaware', 'FL':'Florida', 'GA':'Georgia', 
    'HI':'Hawaii', 'ID':'Idaho', 'IL':'Illinois', 'IN':'Indiana', 'IA':'Iowa', 
    'KS':'Kansas', 'KY':'Kentucky', 'LA':'Louisiana', 'ME':'Maine', 'MD':'Maryland', 
    'MA':'Massachusetts','MI':'Michigan', 'MN':'Minnesota', 'MS':'Mississippi', 'MO':'Missouri', 
    'MT':'Montana', 'NE':'Nebraska', 'NV':'Nevada', 'NH':'New Hampshire', 'NJ':'New Jersey',
    'NM':'New Mexico', 'NY':'New York', 'NC':'North Carolina', 'ND':'North Dakota',  'OH':'Ohio', 
    'OK':'Oklahoma', 'OR':'Oregon', 'PA':'Pennsylvania', 'RI':'Rhode Island', 'SC':'South Carolina', 
    'SD':'South Dakota', 'TN':'Tennessee', 'TX':'Texas', 'UT':'Utah', 'VT':'Vermont', 'VA':'Virginia', 
    'WA':'Washington', 'WV':'West Virginia', 'WI':'Wisconsin', 'WY':'Wyoming'
}

def __make_code_to_stname(code_to_stname):
    stname_to_code = {}
    for code in code_to_stname:
        stname_to_code[code_to_stname[code]] = code
    return stname_to_code

def __make_fips_to_stname(code_to_stname):
    fips_to_stname = {}

    skip = (3, 7, 14, 11, 43, 52)
    stnames = [code_to_stname[key] for key in code_to_stname]

    state_index = 0
    for i in range(56):
        fips_code = i + 1
        if fips_code in skip:
            continue
        if fips_code < 10:
            fips_code = f"0{fips_code}"
        else:
            fips_code = f"{fips_code}"
        fips_to_stname[fips_code] = stnames[state_index]
        state_index += 1

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
    for k in __FIPS_TO_STNAME:
        print(__FIPS_TO_STNAME[k], k)