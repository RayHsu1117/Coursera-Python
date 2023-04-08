"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
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

def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo  - GDP data information dictionary
      gdpdata  - GDP data dictionary for a single country

    Output:
      Returns a list of plot values for the GDP data. The plot
      values should be a list of (year, gdp) tuples. Only include
      plot values for the range of years specified in the gdpinfo
      dictionary. If a year is missing from the gdpdata dictionary,
      use the value None for its GDP.

      If a GDP value cannot be converted to a float, skip that
      (year, GDP) pair.
    """
    plot_values = []

    for year in range(gdpinfo['min_year'], gdpinfo['max_year'] + 1):
        year_str = str(year)
        if year_str in gdpdata:
            gdp_str = gdpdata[year_str]
            if gdp_str:
                gdp = float(gdp_str)
                plot_values.append((year, gdp))
        # else:
        #     plot_values.append((year, None))
    return plot_values


def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values 
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    result_dict = {}
    for country in country_list:
        gdp_data_dict = read_csv_as_nested_dict(gdpinfo['gdpfile'], gdpinfo['country_name'],
                                                gdpinfo['separator'], gdpinfo['quote'])
        if country in gdp_data_dict:
            gdp_data = gdp_data_dict[country]
            plot_values = build_plot_values(gdpinfo, gdp_data)
            result_dict[country] = plot_values
        else:
            result_dict[country] = []
    return result_dict


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    plot_dict = build_plot_dict(gdpinfo, country_list)

    xy_chart = pygal.XY()
    xy_chart.title = 'GDP for Countries in {}'.format(', '.join(country_list))
    for country in country_list:
        xy_chart.add(country, plot_dict[country])
    xy_chart.render_to_file(plot_file)


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"],
                   "isp_gdp_xy_uk+usa.svg")


# Make sure the following call to test_render_xy_plot is commented out
# when submitting to OwlTest/CourseraTest.

# test_render_xy_plot()
