import requests as req
from bs4 import BeautifulSoup as bs
import time
import json
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
class ApprenticeGovScraper:
    def fetch(self, RESULTS, Keywords, Location, WithinDistance):
        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
        Keywords = Keywords.rstrip()
        Keywords = Keywords.replace(" ", "%20")
        Location = Location.rstrip()
        Location = Location.replace(" ", "")
        URL = (f"https://www.findapprenticeship.service.gov.uk/apprenticeships?SearchField=All&Keywords={Keywords}&Location={Location}&WithinDistance={WithinDistance}&sortType=Distance&resultsPerPage={RESULTS}&DisplayDistance=true&DisplayClosingDate=true&DisplayStartDate=true&&DisplayWage=true")
        print(URL)
        pre_time = time.time()
        r = req.get(URL, headers=headers)
        post_time = time.time()
        scraping_time = (post_time-pre_time)
        print("Scraping Complete.")
        r = r.text
        with (open("source.html", "w", encoding='utf-8')) as f:
            f.write(r)
        f.close
        print("Done")

    def parsing(self):
        with open("source.html", "r") as f:
            raw = f.read()
        f.close()
        soup = bs(raw, "html5lib")
        grids = soup.find_all("li", "search-result sfa-section-bordered")
        distance_list = []
        title_list = []
        print(f"{len(grids)} results found")
        for i in grids:
            distance_list.append(i.find("span", id="distance-value").get_text())
            title_list.append(i.find("a", "vacancy-link").get_text())

        print("Done")
        salaries = soup.find_all("ul", """list sfa-no-margins vacancy-details-list""")
        salaries = str(salaries)
        salaries = salaries.replace("""<li class="" data-show="DisplayWage">
                                    <span class="bold-small">Wage:</span>""", "------")
        salaries = salaries.replace("""</li>

                                    <li class="sfa-hide-tablet hide-nojs">""", "------")
        salaries = salaries.replace("\\n", "")
        salaries = salaries.replace("                                ", "")
        salaries = salaries.split("------")
        every_second_element = salaries[1::2]
        converted = []
        for element in every_second_element:
            converted.append(element.strip())
        with open("salary.json","w") as f:
            json.dump(converted,f,ensure_ascii=False)
        f.close()
        for i in range(len(converted)):
            print("\n")
            print(f"{title_list[i]}")
            print(f"{converted[i]}")
            print(f"{distance_list[i]} miles away")
            print("\n")
    def salary_cleaning(self):
        wage_list = []
        salary_list = []
        for split_element in salary_data:
            x = split_element.split(" ")
            for i in x:
                if "week" in x:
                    wage_list.append(i)
                if "year" in x:
                    salary_list.append(i)
        cleaned_salary = []
        cleaned_wages = []
        for i in salary_list:
            if "£" in i:
                cleaned_salary.append(i)
            else:
                pass
        for i in wage_list:
            if "£" in i:
                cleaned_wages.append(i)
        salary_round_1 = []
        for i in cleaned_salary:
            salary_round_1.append(i.replace("£",""))
        salary_round_2 = []
        for i in salary_round_1:
            salary_round_2.append(i.replace(",",""))
        salary_round_3 = []
        for i in salary_round_2:
            salary_round_3.append(float(i))
        wage_round_1 = []
        for i in cleaned_wages:
            wage_round_1.append(i.replace("£",""))
        wage_round_2 = []
        for i in wage_round_1:
            wage_round_2.append(i.replace(",",""))
        wage_round_3 = []
        for i in wage_round_2:
            wage_round_3.append(float (i))
        wage_round_3 = sorted(wage_round_3)
        wage_round_3= list(dict.fromkeys(wage_round_3))
        print((wage_round_3))
        plt.hist(salary_round_3,bins=20)
        plt.show()

if __name__ == "__main__":
    scraper = ApprenticeGovScraper()
    Keywords = str(input("Enter keywords : "))
    print("\n")
    Location = str(input("Enter location : "))
    print("\n")
    WithinDistance = str(input("Enter Within Distance (miles) : "))
    print("\n")
    current_time = time.time()
    scraper.fetch("10000", Keywords, Location, WithinDistance)
    scraper.parsing()
    current_time1 = time.time()
    print(current_time1 - current_time)
    with open("salary.json","r") as f:
        salary_data =json.load(f)
    f.close()
    scraper.salary_cleaning()

