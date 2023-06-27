import os
import time
import csv
from playwright.sync_api import sync_playwright
import secret




class Jobs_generator():
    joblink = []  # Initialized list to store links
    maxcount = 5  # Max daily apply quota for Naukri
    keywords = ['Data Analyst, Data scientist'

                ]  # Add your list of roles you want to apply (comma-separated)
    location = 'Pune'  # Add your location/city name for within India or remote
 # Saved list of applied and failed job links for manual review
    yournaukriemail = secret.yournaukriemail
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
            time.sleep(5)

            for k in keywords:
                try:
                    if location == '':
                        url = f"https://www.naukri.com/{k.lower().replace(' ', '-')}"
                    else:
                        url = f"https://www.naukri.com/{k.lower().replace(' ', '-')}-jobs-in-{location.lower().replace(' ', '-')}"
                    page.goto(url)
                    print(url)
                    time.sleep(1)
                    while True:
                        try:

                            # Scrape the URLs from the search results

                            count = 1000 # number of pages want to scrape
                            while True:
                                print('Page no.',count)
                                if count == 0:
                                    break
                                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')

                                # Modify the style attribute
                                page.eval_on_selector('.rc-slider-track', 'el => el.style.width = "0%"')


                                urls = page.query_selector_all('.list a[href^="http"]')
                                for url in urls:
                                    href = url.get_attribute('href')
                                    if 'ambitionbox' in href or '-jobs-careers-' in href:
                                        continue
                                    if ('-0-to' in href   or '-1-to' in href) and (
                                            'analyst' in href or 'scientist' in href or 'analytics' in href or 'BI developer' in href
                                    ):
                                        joblink.append(href)
                                    else:
                                        continue
                                print(len(joblink))
                                # Check if there is a "Next" button and click on it
                                print('Clicked next')
                                next_button = page.query_selector('a[class="fright fs14 btn-secondary br2"]')
                                if next_button:
                                    page.click('a[class="fright fs14 btn-secondary br2"]')
                                    time.sleep(2)  # Add a small delay to allow page transition
                                else:
                                    break
                                count -= 1

                        except Exception as e:
                            print('Error while gathering url ', e)
                        finally:
                            print('Completed the gathering url')
                            break
                except Exception as e:
                    print('Error in url scrapping', e)
            # os.makedirs(f'{os.getcwd()}/data',exist_ok=True)
            # Store the URLs in a CSV file
            with open(f'D:\pythonProject\Gather_Job\\Naukri\\NaukriJobs.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['URLs'])
                writer.writerows([[url] for url in joblink])
        except Exception as e:
            print('Error In genration of file',e)

        finally:
            print('Job List successfully generated')