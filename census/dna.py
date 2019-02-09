import re

pattern = r"ATG([ACTG]{3})*(TAA|TAG|TGA)"
string = "@#@$%1323^&*(^%$# \
        CACAATGAAACCCTTTGGGTAGAAA \
        #$%#$234$"

pattern = re.compile(pattern)
match = pattern.search(string)

print(match.group(0))