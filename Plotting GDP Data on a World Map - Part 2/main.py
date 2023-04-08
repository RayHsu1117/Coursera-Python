"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table


def read_csv_as_dict(filename, separator, quote="'"):
    """
    Reads the CSV file filename into a list of dictionaries where the
    keys are the fields in the file header and the values are the
    fields in the row for a given line in the file.

    Inputs:
      filename  - Name of CSV file
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      A list of dictionaries containing the contents of the CSV file
    """
    table = []
    with open(filename, "rt", newline='') as csvfile:
        csvreader = csv.DictReader(csvfile,
                                   delimiter=separator,
                                   quotechar=quote)
        for row in csvreader:
            table.append(row)
    return table


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    # Read in the country code CSV file
    with open(codeinfo['codefile'], 'r', newline='') as codefile:
        reader = csv.DictReader(codefile, delimiter=codeinfo['separator'], quotechar=codeinfo['quote'])
        # Build a dictionary mapping plot codes to data codes
        converter = {}
        for row in reader:
            converter[row[codeinfo['plot_codes']]] = row[codeinfo['data_codes']]
    return converter


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    # Create a dictionary to hold the mapping of plot_countries codes to gdp_countries codes
    code_mapping = {}
    # Create a set to hold the plot_countries codes that have no match in gdp_countries
    unmatched_codes = set()

    # Loop through the plot_countries codes and find matches in gdp_countries
    for plot_code, country_name in plot_countries.items():
        for country in gdp_countries.values():
            if country_name == country['Country Name']:
                code_mapping[plot_code] = country['Country Code']
    for plot_code in plot_countries.keys():
        if plot_code not in code_mapping.keys():
            unmatched_codes.add(plot_code)
    return code_mapping, unmatched_codes


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """

    gdp_dict = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_code"], gdpinfo["separator"],
                                       gdpinfo["quote"])
    code_dict = read_csv_as_nested_dict(codeinfo["codefile"], codeinfo['plot_codes'], codeinfo["separator"],
                                        codeinfo["quote"])

    map_dict = {}
    missing_countries = set(plot_countries.keys())
    missing_years = set()

    for code in plot_countries:
        country_name = plot_countries[code]
        if country_name in code_dict:
            country_code = code_dict[country_name]
            if country_code[codeinfo['data_codes']].upper() in gdp_dict:
                if year in gdp_dict[country_code[codeinfo['data_codes']].upper()]:
                    gdp = gdp_dict[country_code[codeinfo['data_codes']].upper()][year]
                    if gdp != "":
                        map_dict[code] = math.log(float(gdp), 10)
                        missing_countries.discard(code)
                    else:
                        missing_countries.discard(code)
                        missing_years.add(code)
                else:
                    missing_years.add(code)
            # else:
            #     missing_years.add(code)
            elif country_code[codeinfo['data_codes']].lower() in gdp_dict:
                if year in gdp_dict[country_code[codeinfo['data_codes']].lower()]:
                    gdp = gdp_dict[country_code[codeinfo['data_codes']].lower()][year]
                    if gdp != "":
                        map_dict[code] = math.log(float(gdp), 10)
                        missing_countries.discard(code)
                    else:
                        missing_countries.discard(code)
                        missing_years.add(code)
                else:
                    missing_years.add(code)
            # else:
            #     missing_years.add(code)
            elif country_code[codeinfo['data_codes']] in gdp_dict:
                if year in gdp_dict[country_code[codeinfo['data_codes']]]:
                    gdp = gdp_dict[country_code[codeinfo['data_codes']]][year]
                    if gdp != "":
                        map_dict[code] = math.log(float(gdp), 10)
                        missing_countries.discard(code)
                    else:
                        missing_countries.discard(code)
                        missing_years.add(code)
                else:
                    missing_years.add(code)
            # else:
            #     missing_years.add(code)
        else:
            missing_countries.add(code)

    return map_dict, missing_countries, missing_years


# def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
#     """
#     Inputs:
#       gdpinfo        - A GDP information dictionary
#       codeinfo       - A country code information dictionary
#       plot_countries - Dictionary mapping plot library country codes to country names
#       year           - String year of data
#       map_file       - String that is the output map file name
#
#     Output:
#       Returns None.
#
#     Action:
#       Creates a world map plot of the GDP data in gdp_mapping and outputs
#       it to a file named by svg_filename.
#     """
#     return


# def test_render_world_map():
#     """
#     Test the project code for several years
#     """
#     gdpinfo = {
#         "gdpfile": "isp_gdp.csv",
#         "separator": ",",
#         "quote": '"',
#         "min_year": 1960,
#         "max_year": 2015,
#         "country_name": "Country Name",
#         "country_code": "Country Code"
#     }
#
#     codeinfo = {
#         "codefile": "isp_country_codes.csv",
#         "separator": ",",
#         "quote": '"',
#         "plot_codes": "ISO3166-1-Alpha-2",
#         "data_codes": "ISO3166-1-Alpha-3"
#     }
#
#     # Get pygal country code map
#     pygal_countries = pygal.maps.world.COUNTRIES
#
#     # 1960
#     render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")
#
#     # 1980
#     render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")
#
#     # 2000
#     render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")
#
#     # 2010
#     render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

# test_render_world_map()

print(
    build_map_dict_by_code({'gdpfile': 'gdptable3.csv', 'separator': ';', 'quote': "'", 'min_year': 20010, 'max_year': 20017, 'country_name': 'ID', 'country_code': 'CC'}, {'codefile': 'code1.csv', 'separator': ',', 'quote': "'", 'plot_codes': 'Code4', 'data_codes': 'Code3'}, {'C1': 'c1', 'C2': 'c2', 'C3': 'c3', 'C4': 'c4', 'C5': 'c5'}, '20012')
    , build_map_dict_by_code({'gdpfile': 'gdptable2.csv', 'separator': ',', 'quote': '"', 'min_year': 1953, 'max_year': 1958, 'country_name': 'Country Name', 'country_code': 'Code'}, {'codefile': 'code2.csv', 'separator': ',', 'quote': "'", 'plot_codes': 'Cd2', 'data_codes': 'Cd1'}, {'C1': 'c1', 'C2': 'c2', 'C3': 'c3', 'C4': 'c4', 'C5': 'c5'}, '1953')
)
