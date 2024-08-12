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



def scrape_jobs(url, num_jobs):
    #set browser to chrome
    index_url = url

    #access url page
    browser.get(index_url)

    #wait 10 seconds
    time.sleep(10)


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
        all_jobs_list = browser.find_element(By.CLASS_NAME, 'position-job-list')
        
        list_els = all_jobs_list.find_elements(By.TAG_NAME, 'li')

        internal_counter = 0
        while(internal_counter < len(list_els)):
            
            target_element = list_els[internal_counter]
            if target_element:
                target_element.click()
                print("Clicked")
                time.sleep(2)
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
                link = link_el.get_attribute("href")
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
            internal_counter += 1
            print(internal_counter)

            print("Job title" + title)

            #click on the next job
            # get_next_job()

            #wait 1 second for render
            time.sleep(1)
        
        job_counter += internal_counter

        #scroll the page
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
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

