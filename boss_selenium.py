#modified from a script by jhcoco on Github by ben warren
#last updated 7/30 01:00 AM

#funtion: scrape boss zhipin website for job listings into a csv output file

#Current issues:
#   - Need a new approach to finding the next box to click on
#   - Uploading to a database, not just a local csv (not essential)

import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import random

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
browser = webdriver.Chrome() 

#func: get_next_job -> finds the next job card on the page and clicks on it to show details
def get_next_job():
        all_jobs_list = browser.find_element(By.CLASS_NAME, 'position-job-list')
        list_els = all_jobs_list.find_elements(By.TAG_NAME, 'li')

        #Locate the element with the class "job-card-box-active"
        active_job_card_box = browser.find_element(By.CLASS_NAME, 'job-card-box active')

        #Find the element with the class "job-card-box" just after the "job-card-box-active"
        target_element = None
        found_active = False

        for job_card in list_els:
            if found_active:
                target_element = job_card
                break
            if job_card == active_job_card_box:
                found_active = True

        #Click on the target element if it exists - otherwise, click the next page
        if target_element:
            target_element.click()
        else:
            #click on the next page:
            try:
                next_page = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[4]/div[1]/div[1]/div/div/a[6]')
                next_page.click()
            except Exception as e:
                print("Couldn't find next page", e)

#func: scrape_jobs -> scrapes the number of jobs specified as num_jobs from the url specified as url
def scrape_jobs(url, num_jobs):
    #set browser to chrome
    index_url = url

    #access url page
    browser.get(index_url)

    #wait 10 seconds
    time.sleep(10)
    listings = []

    titles = []
    companies = []
    salaries = []
    descriptions = []
    tag_list = []
    locations = []
    links = []
    label_list = []


    job_counter = 0
    #need to click through elements on page to get more details
    while job_counter < num_jobs:
        job_details = browser.find_element(By.CLASS_NAME, 'job-detail-box')

        title_el = job_details.find_element(By.CLASS_NAME, 'job-name')
        salary_el = job_details.find_element(By.CLASS_NAME, 'job-salary')
        label_el = job_details.find_element(By.CLASS_NAME, 'job-label-list')
        desc_el = job_details.find_element(By.CLASS_NAME, 'desc')
        location_el = job_details.find_element(By.CLASS_NAME, 'job-address-desc')
        link_el = job_details.find_element(By.CLASS_NAME, 'more-job-btn')

        #this contains a city, number of days of work, experience, etc.
        tags_el = job_details.find_element(By.CLASS_NAME, 'tag-list')

        if title_el:
            title = title_el.text
        else:
            title = None

        if salary_el:
            salary = salary_el.text
        else:
            salary = None
        
        if desc_el:
            desc = desc_el.text
        else:
            desc = None
        
        if location_el:
            location = location_el.text
        else:
            location = None

        if link_el:
            link = link_el.text
        else:
            link = None


        #Iterate through elements with lists (labels and tags)
        if label_el:
            list_els = label_el.find_elements(By.TAG_NAME, 'li')
            labels = [item.text for item in list_els]
        else:
            labels = None
        
        if tags_el:
            list_els = tags_el.find_elements(By.TAG_NAME, 'li')
            tags = [item.text for item in list_els]
        else:
            tags = None


        #add values to lists
        titles.append(title)
        companies.append(company)
        salaries.append(salary)
        descriptions.append(desc)
        tag_list.append(tags)
        label_list.append(labels)
        locations.append(location)
        links.append(link)

        #add 1 to job count
        job_counter += 1

        print("Job title" + title)

        #click on the next job
        get_next_job()

        #wait 1 second for render
        time.sleep(1)
    
    #create return dataframe
    df = pd.DataFrame({
       "company": companies,
        "title": titles,
        "description": descriptions,
        "salary": salaries,
        "tags": tag_list,
        "location": locations,
        "salary": salaries,
        "labels": label_list,
        "link": links
    })

    return df

#list of companies to scrape
companies = {
    "SpeechOcean": "https://www.zhipin.com/gongsi/job/5f112b4b026160051nxy3t8~.html?ka=company-jobs"
    # "Magic Data": "https://www.zhipin.com/gongsi/job/20487114181789790HJ_0966.html?ka=company-jobs",
    # "奥睿智创招聘": "https://www.zhipin.com/gongsi/job/49baf7f633b562931HZ73Nm7GFE~.html?ka=company-jobs",
    # "数据堂": "https://www.zhipin.com/gongsi/job/de5dbc52daf2078c1Hd53Q~~.html?ka=company-jobs",
    # "MindFlow": "https://www.zhipin.com/gongsi/job/3dc2d9787c8ca5e51HVz3N27Fg~~.html?ka=company-jobs",
    # "Konvery Data": "https://www.zhipin.com/gongsi/job/a9da50dc31f7fa5a1XRy2Nq-E1o~.html?ka=company-jobs",
    # "景联文": "https://www.zhipin.com/gongsi/job/d3567367aedd5f810Xx50928Ew~~.html?ka=company-jobs",
    # "上海爱数": "https://www.zhipin.com/gongsi/job/32bcf535b61457941H1y290~.html?ka=company-jobs",
    # "致鑫科技": "https://www.zhipin.com/gongsi/job/0289fd3719ffbbfa1XBy29y8EQ~~.html?ka=company-jobs"
}

#get current datetime
current_date = datetime.date.today().strftime('%Y-%m-%d')

#set filename to current datetime
file_name = str(current_date) + "scraped_jobs.csv"

company_dfs = []

for company in companies.keys():
    try:
        df = scrape_jobs(companies[company], 10)
        company_dfs.append(df)
    except Exception as e:
        print("Failed to scrape" + company + "Exception:" + str(e))

#add all the dfs together
final_df = pd.concat(company_dfs)

#download to csv
final_df.to_csv("/Users/benwarren/Downloads/zhipin_data/zhipin_data_download_1.csv")
    