# Python project to pull COVID-19 data statistics
from kaggle import KaggleApi
import datadotworld as dw
import pandas as pd

# Authenticate self using a Kaggle API token
api = KaggleApi()
api.authenticate()


# Class to import data from Kaggle and data.world, merge datasets, and compute values from that data in new columns
class covid_project:
    # Initialize the object by pulling the datasets and merging them together
    def __init__(self):
        # Load initial datasets
        dw_dataset = dw.load_dataset('resiport/who-dataset')
        api.dataset_download_file('imdevskp/corona-virus-report', 'country_wise_latest.csv')

        # Convert datasets into Pandas format and merge together on country
        self.covid_dataset = pd.read_csv('country_wise_latest.csv')
        self.covid_dataset.rename(columns={'Country/Region': 'country'}, inplace=True)
        self.who_dataset = pd.DataFrame(dw_dataset.tables['who'])
        self.merged_dataset = pd.merge(left=self.who_dataset, right=self.covid_dataset, on='country')

    # Computes the percent of COVID-19 cases recovered for each country
    def compute_recovered_percent(self):
        self.merged_dataset["Recovered_Percent"] = (self.merged_dataset["Recovered"] / self.merged_dataset["Confirmed"])
        self.merged_dataset["Recovered_Percent"] = self.merged_dataset["Recovered_Percent"] * 100

    # Computes the percent of the population confirmed with COVID-19 for each country
    def compute_infected_percent(self):
        self.merged_dataset["Infected_Percent"] = (self.merged_dataset["Confirmed"] /
                                                   self.merged_dataset["population_in_thousands_total"])
        self.merged_dataset["Infected_Percent"] = (self.merged_dataset["Infected_Percent"] / 1000) * 100


# Create a covid_project object and compute the two columns
cp = covid_project()
cp.compute_recovered_percent()
cp.compute_infected_percent()
# print(cp.merged_dataset)
