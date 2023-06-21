import csv
from playwright.sync_api import sync_playwright
import time
import os
# Set up Playwright
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Create a new page
    page = context.new_page()

    # Search on Google
    search_query = """ site:wd3.myworkdayjobs.com/en-us  "analyst" """
    search_url = f"https://www.google.com/search?q={search_query}"
    page.goto(search_url)
    time.sleep(2)
    # Scrape the URLs from the search results
    url_list = []
    count = 10
    while True:
        if count==0:
            break
        urls = page.query_selector_all('.v7W49e a[href^="http"]')
        for url in urls:
            href = url.get_attribute('href')
            url_list.append(href)

        # Check if there is a "Next" button and click on it
        next_button = page.query_selector('a[id="pnnext"]')
        if next_button:
            page.click('a[id="pnnext"]')
            time.sleep(2)  # Add a small delay to allow page transition
        else:
            break
        count-=0.5
    # Store the URLs in a CSV file
    directory = r'D:\pythonProject\Gather_Job\googledata'
    file_count = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
    # Store the URLs in a CSV file

    with open(f"""D:\pythonProject\Gather_Job\googledata\\urls{file_count}.csv""", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['URLs'])
        writer.writerows([[url] for url in url_list])

    # Clean up
    context.close()
    browser.close()