import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import requests
from time import sleep
from random import randint
import re

towns = pd.DataFrame()

import pandas as pd
df = pd.read_csv("cities.csv")
town_names = list(df["City-State"])
final_scores = list(df["Final-Score"])
#town_names = ["Casper-Wyoming","Cheyenne-Wyoming","Gillette-Wyoming","Jackson-Wyoming","Laramie-Wyoming","Rock-Springs-Wyoming","Sheridan-Wyoming"]
#final_scores = [11,16,22,62,72,0,12]
i=-1

print("City-State,PercentageMales,MedianAge,Latitude,Longitude,PercentageHighSchoolGrads,PercentagePHDs,PercentageBelowPovertyLevel,Population,PercentageNoReligion,PercentageEvangelicals,FinalScore")

for town_name in town_names:
    i += 1
    try:
        page = requests.get(f"https://www.city-data.com/city/{town_name}.html").text
        page2 = requests.get(f"https://www.city-data.com/poverty/poverty-{town_name}.html").text
        doc = BeautifulSoup(page, "html.parser")
        doc2 = BeautifulSoup(page2, "html.parser")
        final_score = final_scores[i]


        #print(town_name)
        sex_population = str(doc.find(id="population-by-sex"))
        (males, females) = [float(x) for x in re.findall(r"(?<=\()[0-9]+\.[0-9]+(?=\%\))", sex_population)]
        #print(males, females)

        age_population = str(doc.find(id="median-age"))
        #print("Here")
        medianage = float(re.search("Median resident age:.*\>([0-9]*\.[0-9]*).*median age", age_population).groups()[0])
        #print(medianage)

        coordinates = str(doc.find(id="coordinates"))
        latitude = float(re.findall(r"(?<=Latitude:</b> )[0-9]*.[0-9]*", coordinates)[0])
        longitude = float(re.findall(r"(?<=Longitude:</b> )[0-9]*.[0-9]*", coordinates)[0])
        #print(latitude, longitude)

        education_level = str(doc.find(id="education-info"))
        highschoolgrads = float(re.findall("(?<=High school or higher:<\/b> )[0-9]*.[0-9]*", education_level)[0])
        phds = float(re.findall(r"(?<=professional degree:<\/b> )[0-9]*.[0-9]*", education_level)[0])
        #print(highschoolgrads)
        #print(phds)

        poverty_level = str(doc2.find(id="rt"))
        below_poverty_level= float(re.findall(r"[0-9]*\.[0-9]*", poverty_level)[0])
        #print(f"below poverty level: {below_poverty_level}")
        # poverty_level = str(doc.find(id="poverty-level"))
        # print(poverty_level)
        # broke = float(re.findall(r"(?<=<\/b> )[0-9]*.[0-9]*", poverty_level)[0])
        # print(broke)

        # religion_population = str(doc.find(id="religion"))
        # atheist = float(re.findall("(?<=None<\/td><td>)[0-9,]*(?=<\/td><td>)", religion_population)[0].replace(",", ""))
        # print(atheist)

        total_population = str(doc.find(id="city-population"))
        residents = float(re.findall(r"(?<=</b> )(?:[0-9]*\,*)*", total_population)[0].replace(",", ""))
        #residents = float(re.findall(r"(?<=</b> )([0-9]*\,*)*", total_population)[0].replace(",", ""))


        religion_population = doc.find(id="religion").find_all('tr')
        data = []
        for row in religion_population:
            columns = row.find_all('td')
            if columns:
                religion = columns[0].get_text(strip=True)
                number = columns[1].get_text(strip=True).replace(",", "").replace("-","0")
                #print(f'religion: {religion} | number: {number}')
                data.append([religion, int(number)])
        df = pd.DataFrame(data, columns=['religion', 'number'])
        df['percentage'] = (df['number'] / df['number'].sum()) * 100
        atheist=df[df.religion == "None"].iloc[0]["percentage"]
        evangelicals = df[df.religion == "Evangelical Protestant"].iloc[0]["percentage"]
        #print(atheist)
        #print(evangelicals)

        # education_population = doc.find(id="education-info").find_all('b')
        # data = []
        # for row in education_population:
        #     columns = row.find_all('li')
        #     if columns:
        #         education = columns[0].get_text(strip=True)
        #         ed_number = columns[1].get_text(strip=True).replace(",", "").replace("-", "0")
        #         print(f'education: {education} | number: {ed_number}')
        #         data.append([education, int(ed_number)])
        # df = pd.DataFrame(data, columns=['education', 'number'])
        # df['percentage'] = (df['number'] / df['number'].sum()) * 100
        # phds = df.education == "Graduate or professional degree"
        # highschoolgrads = df.education == "High school or higher"
        # print(phds)
        # print(highschoolgrads)

        #Town,PercentageMales,MedianAge,Latitude,Longitude,PercentageHighSchoolGrads,PercentagePHDs,PercentageBelowPovertyLevel,Population,PercentageNoReligion,PercentageEvangelicals
        print(f"{town_name},{males},{medianage},{latitude},{longitude},{highschoolgrads},{phds},{below_poverty_level},{residents},{atheist},{evangelicals},{final_score}")
        sleep(randint(1, 30))
        #print("\n")


    except Exception as e:
        print(e)
        print("SKIPPED")