import pandas as pd

data = pd.read_csv('/Users/benwarren/Downloads/zhipin_data/2024-08-11_scraped_jobs_full.csv')

no_dupes = data.drop_duplicates(subset='link')

no_dupes.to_csv('/Users/benwarren/Downloads/zhipin_data/2024-08-11_scraped_jobs_full_unique.csv')