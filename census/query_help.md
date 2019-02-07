Let’s begin with a query for the resident population totals per state in the dataset, Vintage 2014 Population Estimates: US, State, and PR Total Population and Components of Change. You will find this dataset listed on the Census Data API Datasets page:

api.census.gov/data.html

Format queries as a URL, as follows (Use Firefox.):

https://api.census.gov/data/2014/pep/natstprc?get=STNAME,POP&DATE=7&for=state:*

Assemble components of this query by following these steps:

    Start your query with the host name: https://api.census.gov/data
    Add the data year to the URL. This is the year the data were estimated;; e.g., 2014

    https://api.census.gov/data/2014
    Add the dataset name’s acronym, which is listed in the “Dataset Name” column on the Census Data API Datasets page (api.census.gov/data.html); e.g., pep/natstprc.

    https://api.census.gov/data/2014/pep/natstprc

    This is the base URL for this dataset.
    Follow the base URL with the query character ? (question mark). Add variables starting with a get clause get= followed by the name of the variable for which you are searching. The link for the list of variables is in the “Variable List” column on the Census Data API Datasets page (api.census.gov/data.html) and will lead you to this Variables page:

    api.census.gov/data/2014/pep/natstprc/variables.html

    Because there is more than one variable in this query, use a comma to separate each variable:

    https://api.census.gov/data/2014/pep/natstprc?get=STNAME,POP

    In this dataset, STNAME will provide the state name to clarify the output reading for state code.
    Add geography using a predicate clause starting with an ampersand (&) to separate it from your get clause, and then a for followed by in clause, if needed; e.g., &for=state. Because we are looking for information for all the states, add a wildcard (:*) to indicate all values; e.g., state:*

    https://api.census.gov/data/2014/pep/natstprc?get=STNAME,POP&DATE=7 &for=state:*

    A full list is available at the geography page linked next to this dataset on the Census Data API Datasets page: api.census.gov/data/2014/pep/natstprc/geography.html. As you can see, you can only search on the state or national level for this dataset. Other datasets present many more geographical subdivisions. Sometimes datasets change the number of geographies they publish from year to year.
    When you finish practicing and are ready to publish your data and use a key, insert &key= followed by your key code into the search URL. You can place this anywhere in the URL after the question mark; e.g., &key=your key here

    https://api.census.gov/data/2014/pep/natstprc?get=STNAME,POP&DATE=7&for=state:*&key=your key here
    You can copy your query results into a spreadsheet to clean it up and analyze it, or you can save it as a file and consume it as JSON. The response for all queries is formatted as a two dimensional JSON array where the first row provides column names and the subsequent rows provide data values. The first rows of output of the query are configured as follows:

    [["STNAME","POP","DATE","state"],
    ["Alabama","4849377","7","01"],
    ["Alaska","736732","7","02"],
    ["Arizona","6731484","7","04"],
    ["Arkansas","2966369","7","05"],
    ["California","38802500","7","06"],
    ["Colorado","5355866","7","08"],
    ["Connecticut","3596677","7","09"],
    ["Delaware","935614","7","10"],
    ["District of Columbia","658893","7","11"],
    .....

    You can find examples of other queries for this dataset by clicking the link in the Examples column on the API datasets page, which takes you to this Example page:
    api.census.gov/data/2014/pep/natstprc/examples.html
