import json
import time
from matplotlib import pyplot as plt
class SalaryData:
    def data_check(self):
        if type(salary_data) == list:
            pass
        else:
            quit()

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
        for i in salary_list:
            if "£" in i:
                cleaned_salary.append(i)
            else:
                pass
        salary_round_1 = []
        for i in cleaned_salary:
            salary_round_1.append(i.replace("£",""))
        salary_round_2 = []
        for i in salary_round_1:
            salary_round_2.append(i.replace(",",""))
        salary_round_3 = []
        for i in salary_round_2:
            salary_round_3.append(float(i))
        plt.hist(salary_round_3 , bins=5)









if __name__ == "__main__":
    with open("salary.json","r") as f:
        salary_data =json.load(f)
    f.close()
    DisplayData=SalaryData()
    DisplayData.data_check()
    DisplayData.salary_cleaning()
