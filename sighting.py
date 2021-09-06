from selenium import webdriver
import pandas as pd

# Scrapes for UFO sightings by event date from the National UFO Reporting Center
# Includes UFO sightings dating back to June 1400
# Does not include sightings with unspecified or approximate dates

driver = webdriver.Chrome('/Users/drastimehta/Downloads/chromedriver')
driver.get('http://www.nuforc.org/webreports/ndxevent.html')

# find each event month
months = driver.find_elements_by_xpath('//tbody/tr/td[1]')

all_month_dates = []
all_display_months = []
all_dates_times = []
all_cities = []
all_states = []
all_shapes = []
all_duration = []
all_summary = []
all_posted = []

for date in range(len(months) - 1):
    all_month_dates.append(months[date].text)

for i in range(len(all_month_dates)):
    # click on a specific event month/year
    month_year = driver.find_element_by_link_text(all_month_dates[i])
    month_year.click()

    default_xpath = '//table/tbody/tr/'
    dates_times = driver.find_elements_by_xpath(default_xpath + 'td[1]')    # event dates / times
    cities = driver.find_elements_by_xpath(default_xpath + 'td[2]')         # cities
    states = driver.find_elements_by_xpath(default_xpath + 'td[3]')         # states/provinces
    shapes = driver.find_elements_by_xpath(default_xpath + 'td[4]')         # UFO shape
    durations = driver.find_elements_by_xpath(default_xpath + 'td[5]')      # duration of sighting
    summaries = driver.find_elements_by_xpath(default_xpath + 'td[6]')      # brief summary of sighting
    postings = driver.find_elements_by_xpath(default_xpath + 'td[7]')       # date posted

    for dt in range(len(dates_times)):
        all_display_months.append(all_month_dates[i])
        all_dates_times.append(dates_times[dt].text)
        all_cities.append(cities[dt].text)
        all_states.append(states[dt].text)
        all_shapes.append(shapes[dt].text)
        all_duration.append(durations[dt].text)
        all_summary.append(summaries[dt].text)
        all_posted.append(postings[dt].text)
    # go back to main month / year page
    driver.back()

driver.quit()

# once completed, pair the lists together
data_tuples = list(zip(all_display_months[:], all_dates_times[:], all_cities[:], all_states[:], all_shapes[:],
                       all_duration[:], all_summary[:], all_posted[:]))
# create the dataframe
df = pd.DataFrame(data_tuples, columns=['Month/Year of Event', 'Event Date/Time', 'City', 'State/Provinces', 'Shape',
                                        'Duration', 'Summary', 'Posted'])
# create a csv file
df.to_csv('ufo_sightings.csv', index=False, sep='\t')
# create an excel file
writer = pd.ExcelWriter('ufo_sightings.xlsx', engine='xlsxwriter')
df.to_excel(writer, index=False)
writer.save()
