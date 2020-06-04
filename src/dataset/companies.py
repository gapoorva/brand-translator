import csv
import string
from collections import Counter

class CompaniesDataset():
    def __init__(self, csv_infile, industries_infile, outpath):
        self.csv_infile = csv_infile
        self.industries_infile = industries_infile
        self.outpath = outpath
        self.load()

    def load(self):
        csvfile = open(self.csv_infile)
        self.csv_reader = csv.DictReader(csvfile)

        industries = open(self.industries_infile, 'r').read().splitlines()
        self.industries = { k: [] for k in industries }

    def create_company_name(self, name):
        return ''.join([ch for ch in name if ch.isalnum() or ch.isspace()])

    def categorize_industries(self):
        counter = 0
        stats = Counter()

        for row in self.csv_reader:
            counter += 1
            if counter % 500000 == 0:
                print('processed', counter)

            stats[row['industry']] += 1

        top_industries = [ i + '\n' for i, c in stats.most_common(15) ]
        f = open(self.industries_infile, 'w')
        f.writelines(top_industries)
        f.close()

    def categorize_companies(self):
        counter = 0

        for row in self.csv_reader:
            counter += 1
            if counter % 500000 == 0:
                print('processed', counter)

            if row['country'] != 'united states':
                continue

            if int(row['current employee estimate']) < 1000:
                continue

            if row['industry'] in self.industries.keys():
                self.industries[row['industry']].append(self.create_company_name(row['name']) + '\n')

        for industry, names in self.industries.items():
            outfile = ''.join([ch for ch in industry if ch.isalnum()])
            f = open(self.outpath + '/' + outfile, 'w')
            f.writelines(names)
            f.close()

if __name__ == "__main__":
    dataset = CompaniesDataset(
        './data/raw/kaggle/companies_sorted.csv',
        './data/companies/top_industries',
        './data/companies/industries'
    )
    dataset.categorize()
