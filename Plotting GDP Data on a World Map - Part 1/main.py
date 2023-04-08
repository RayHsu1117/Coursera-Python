"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

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


def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries. The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    matched_countries = {}
    unmatched_codes = set(plot_countries.keys())
    for gdp_country_name in gdp_countries.keys():
        for code, plot_country_name in plot_countries.items():
            if gdp_country_name.lower() == plot_country_name.lower():
                matched_countries[code] = gdp_country_name
                unmatched_codes.discard(code)
                break
    return matched_countries, unmatched_codes


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """

    # Initialize empty dictionaries and sets
    gdp_map = {}
    missing_countries = set()
    no_data_countries = set()

    # Read the GDP data file for the given year
    filename = gdpinfo['gdpfile']
    separator = gdpinfo['separator']
    quote = gdpinfo['quote']
    country_name = gdpinfo['country_name']
    gdp_data = read_csv_as_nested_dict(filename,country_name, separator, quote)

    # Iterate over the countries in plot_countries
    for code, name in plot_countries.items():

        # Check if the country is in the GDP data file
        if name not in gdp_data:
            missing_countries.add(code)
            continue

        # Get the GDP value for the given year
        gdp_year = gdp_data[name].get(year, None)

        # Check if there is no GDP data for the given year
        if gdp_year is None or gdp_year == '':
            no_data_countries.add(code)
            continue

        # Convert GDP value to a float and calculate the logarithm
        try:
            gdp_value = float(gdp_year)
            gdp_map[code] = math.log10(gdp_value)
        except ValueError:
            no_data_countries.add(code)
            continue

    # Return the dictionary and sets
    return gdp_map, missing_countries, no_data_countries


# def test_render_world_map():
#     """
#     Test the project code for several years.
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
#     # Get pygal country code map
#     pygal_countries = pygal.maps.world.COUNTRIES
#
#     # 1960
#     # render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")
#     #
#     # # 1980
#     # render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")
#     #
#     # # 2000
#     # render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")
#     #
#     # # 2010
#     # render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")
#     #


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.
#
# test_render_world_map()

