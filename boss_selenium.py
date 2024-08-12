#modified from a script by jhcoco on Github by ben warren
#last updated 8/11 11:15 PM

#funtion: scrape boss zhipin website for job listings into a csv output file

import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import func_timeout
from func_timeout import func_timeout

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
browser = webdriver.Chrome() 


#func: scrape_jobs -> scrapes the number of jobs specified as num_jobs from the url specified as url
def scrape_jobs(url, num_jobs):
    # Set browser to chrome
    index_url = url
    browser.get(index_url)
    browser.maximize_window()

    # Wait until the job list is present
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'position-job-list'))
    )

    titles = []
    companies = []
    salaries = []
    descriptions = []
    tag_list = []
    locations = []
    links = []
    label_list = []

    job_counter = 0
    clicked_jobs = set()  # To track clicked job elements

    while job_counter < num_jobs:
        # Re-find the job list each iteration to ensure it's fresh
        all_jobs_list = browser.find_element(By.CLASS_NAME, 'position-job-list')
        list_els = all_jobs_list.find_elements(By.TAG_NAME, 'li')

        for internal_counter in range(len(list_els)):
            target_element = list_els[internal_counter]

            # Check if the element has already been clicked
            if target_element in clicked_jobs:
                continue  # Skip if already clicked

            if target_element:
                target_element.click()
                print("Clicked")
                
                # Add the element to the set of clicked jobs
                clicked_jobs.add(target_element)

                # Explicit wait until job details are visible
                WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'job-detail-box'))
                )
                WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'job-detail-body'))
                )
            else:
                continue

            job_details = browser.find_element(By.CLASS_NAME, 'job-detail-box')
            job_body = browser.find_element(By.CLASS_NAME, 'job-detail-body')

            title_el = job_details.find_element(By.CLASS_NAME, 'job-name')
            salary_el = job_details.find_element(By.CLASS_NAME, 'job-salary')
            label_el = job_details.find_element(By.CLASS_NAME, 'job-label-list')
            desc_el = job_details.find_element(By.CLASS_NAME, 'desc')
            location_el = job_details.find_element(By.CLASS_NAME, 'job-address-desc')
            link_el = job_body.find_element(By.CLASS_NAME, 'more-job-btn')

            tags_el = job_details.find_element(By.CLASS_NAME, 'tag-list')

            # Extracting details
            title = title_el.text if title_el else None
            salary = salary_el.text if salary_el else None
            desc = desc_el.text if desc_el else None
            location = location_el.text if location_el else None
            link = link_el.get_attribute("href") if link_el else None

            labels = [item.text for item in label_el.find_elements(By.TAG_NAME, 'li')] if label_el else None
            tags = [item.text for item in tags_el.find_elements(By.TAG_NAME, 'li')] if tags_el else None

            # Append to lists
            titles.append(title)
            salaries.append(salary)
            descriptions.append(desc)
            tag_list.append(tags)
            label_list.append(labels)
            locations.append(location)
            links.append(link)
            companies.append(company)

            job_counter += 1
            print(f"Scraped {job_counter} job(s)")

            if job_counter >= num_jobs:
                break

            # Wait a bit before moving to the next job
            time.sleep(1)

        # Scroll the page to load more jobs if needed
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Create return dataframe
    df = pd.DataFrame({
       "company": companies,
        "title": titles,
        "description": descriptions,
        "salary": salaries,
        "tags": tag_list,
        "location": locations,
        "labels": label_list,
        "link": links
    })

    return df


#list of companies to scrape
companies = {
    "SpeechOcean": "https://www.zhipin.com/gongsi/job/5f112b4b026160051nxy3t8~.html?ka=company-jobs",
    "Magic Data": "https://www.zhipin.com/gongsi/job/20487114181789790HJ_0966.html?ka=company-jobs",
    # "奥睿智创招聘": "https://www.zhipin.com/gongsi/job/49baf7f633b562931HZ73Nm7GFE~.html?ka=company-jobs",
    "数据堂": "https://www.zhipin.com/gongsi/job/de5dbc52daf2078c1Hd53Q~~.html?ka=company-jobs",
    "MindFlow": "https://www.zhipin.com/gongsi/job/3dc2d9787c8ca5e51HVz3N27Fg~~.html?ka=company-jobs",
    "Konvery Data": "https://www.zhipin.com/gongsi/job/a9da50dc31f7fa5a1XRy2Nq-E1o~.html?ka=company-jobs",
    "景联文": "https://www.zhipin.com/gongsi/job/d3567367aedd5f810Xx50928Ew~~.html?ka=company-jobs",
    "上海爱数": "https://www.zhipin.com/gongsi/job/32bcf535b61457941H1y290~.html?ka=company-jobs",
    "致鑫科技": "https://www.zhipin.com/gongsi/job/0289fd3719ffbbfa1XBy29y8EQ~~.html?ka=company-jobs"
}

#get current datetime
current_date = datetime.date.today().strftime('%Y-%m-%d')

#set filename to current datetime
file_name = "/Users/benwarren/Downloads/zhipin_data/" + str(current_date) + "_scraped_jobs_full.csv"

company_dfs = []

for company in companies.keys():
    print("Scraping jobs from " + company)
    try:
        df = func_timeout(60, scrape_jobs, args=(companies[company], 20))
        company_dfs.append(df)
    except Exception as e:
        print("Failed to scrape" + company + "Exception:" + str(e))
        continue

#add all the dfs together
final_df = pd.concat(company_dfs)

no_dupes = final_df.drop_duplicates(subset='link')

#download to csv
no_dupes.to_csv(file_name)
