import random
import time
import csv
import pandas as pd
from playwright.sync_api import sync_playwright
import os
import  secret


# import  job_list_generator
# print('Job list generator started')
# job_list_generator.Jobs_generator()


lastname = secret.lastname  # Add your LastName
firstname = secret.firstname# Add your FirstName
joblink = []  # Initialized list to store links
maxcount = 20  # Max daily apply quota for Naukri
keywords = ['Data scientist', 'Data Analyst', 'Product Analyst']  # Add your list of roles you want to apply (comma-separated)
location = 'Pune'  # Add your location/city name for within India or remote
applied = 0  # Count of jobs applied successfully
failed = 0  # Count of jobs failed
applied_list = {
    'passed': [],
    'failed': []
}  # Saved list of applied and failed job links for manual review
yournaukriemail= secret.yournaukriemail
yournaukripass = secret.yournaukripass



# Set up Playwright
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    try:
        # Log in to Naukri
        page = context.new_page()
        page.goto('https://login.naukri.com/')
        page.fill('input[id="usernameField"]', yournaukriemail)
        page.fill('input[id="passwordField"]', yournaukripass)
        page.press('input[id="passwordField"]', 'Enter')
        time.sleep(random.randint(1,3))
        # page.goto('https://www.naukri.com/job-listings-data-analyst-acv-max-saisystems-health-tech-pvt-ltd-chennai-2-to-3-years-150623500361?src=jobsearchDesk&sid=16872734599063286&xp=20&px=1&nignbevent_src=jobsearchDeskGNB')


        manual_urls=[]
        # Application Process
        data = pd.read_csv('D:/pythonProject/Gather_Job/Naukri/NaukriJobs.csv')
        urls = list(data.URLs.values)

        for i in urls:
            time.sleep(random.randint(1,3))
            print(i)
            page.goto(i)
            if applied <= maxcount:
                try:
                    time.sleep(random.randint(1,2))
                    if "company-site-button" in page.content() :
                        manual_application = pd.DataFrame({'Urls':manual_urls.append(i)})  #creating data fram to apply on companysite
                        data.drop(i,inplace=True)
                        print('company website')
                        continue
                    # Application if true
                    elif "apply-button" in page.content():
                        if page.query_selector(".apply-button").inner_text()=='Applied':
                            continue
                        print('applying')
                        page.click(".apply-button")
                        time.sleep(random.randint(1,2))
                        applied += 1
                        applied_list['passed'].append(i)
                        print('Applied for', i, 'Count:', applied)
                    else:
                        print('wrong link')
                        continue

                except Exception as e:
                    failed += 1
                    applied_list['failed'].append(i)
                    print(e, 'Failed', failed)

                # Some Application need this information
                try:
                    if page.text_content() == 'Your daily quota has been expired.':
                        print('MAX Limit reached. Closing browser.')
                        break
                    if ' 1. First Name' in  page.text_content() :
                        page.fill('//input[@id="CUSTOM-FIRSTNAME"]', firstname)
                    if ' 2. Last Name' in page.text_content() :
                        page.fill('//input[@id="CUSTOM-LASTNAME"]', lastname)
                    if 'Submit and Apply' in page.text_content() :
                        page.click('//*[text()="Submit and Apply"]')
                except:
                    print('No ')

            else:
                break




    except Exception as e:
        print('Error while scrapping ',e)

    finally:
        directory = r'D:\pythonProject\Gather_Job\Naukri\data'
        file_count = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])   # creating the file which store failed links and passed links
        # result_df= pd.DataFrame(applied_list)
        # result_df.to_csv(f'D:\pythonProject\Gather_Job\\Naukri\data\\applied_on_{file_count}.csv',index=False)
        context.close()
        browser.close()

print('Completed applying. Saving applied jobs to CSV.')
