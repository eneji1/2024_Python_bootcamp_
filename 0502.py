import json 
import tkinter as tk
from tkinter import filedialog
from datetime import date #실시간 날짜 가져오기

# 월 변수
MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
# 요일 변수 
DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday", "Sunday"]

#년도와 달 표시

def print_month_year(month, year):
    #Prints the month and year at the top of the calendar.
    written_month = MONTH_NAMES[month - 1]
    month_year_label = tk.Label(calendar_frame, text=f"{written_month} {year}", font=("Arial", 20))
    month_year_label.grid(column=2, row=0, columnspan=3)

#캘린더 아래에 테그스트 박스 저장을 위한 딕셔너리

def month_generator(start_date, num_days):
    #각 달에 맞는 캘린더 만드는 함수 
    #enumerate : 순서가있든 자료형을 받았을때 인덱스와 값을 리턴
    for name_number, day_name in enumerate(DAY_NAMES):
        names_label = tk.Label(calendar_frame, text=day_name, fg="black")
        names_label.grid(column=name_number, row=1, sticky='nsew')

    index = 0
    day = 1
    for row in range(6):
        for column in range(7):
            if index >= start_date and index <= start_date + num_days - 1:
                day_frame = tk.Frame(calendar_frame)
                text_box = tk.Text(day_frame, width=15, height=5)
                text_box.grid(row=1)
                text_object_dict[day] = text_box
                day_frame.grid(row=row +2, column=column, sticky='nsew')
                day_frame.columnconfigure(0, weight=1)
                day_number_label = tk.Label(day_frame, text=day)
                day_number_label.grid(row=0)
                day += 1
            index += 1
    load_button = tk.Button(calendar_frame, text="불러오기", command=load_from_json)
    save_button = tk.Button(calendar_frame, text="저장", command=save_to_json)
    load_button.grid(row=8, column=4)
    save_button.grid(row=8, column=2)

def get_start_day_of_month(month, year):
    # 무슨 요일에 1일인지 찾는 함수
    last_two_year = year - 2000
    calculation = last_two_year // 4 + 6
    if month in [1, 10]:
        calculation += 1
    elif month in [2, 3, 11]:
        calculation += 4
    elif month == 5:
        calculation += 2
    elif month == 6:
        calculation += 5
    elif month == 8:
        calculation += 3
    elif month in [9, 12]:
        calculation += 6
    leap_year = is_leap_year(year)
    if leap_year and month in [1, 2]:
        calculation -= 1
    calculation += 6 + last_two_year
    return calculation % 7

#윤년 함수 
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

#day_in_month 만들기
def days_in_month(month,year):
    #매달 몇일이 있는지 지정하는 함수
    if month in [1,3,5,7,8,10,12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 29 if is_leap_year(year) else 28

def make_buttons():
    #월 변환 버튼 만들기
    go_back = tk.Button(calendar_frame,text="<", command=lambda:switch_months(-1))
    go_back.grid(column=0, row=0)
    go_forward = tk.Button(calendar_frame, text=">", command=lambda: switch_months(1))
    go_forward.grid(column=6, row=0)

def switch_months(direction):
    #월 변환 시 실행되는 함수 : 월 변환시 년도가 바뀔경우
    global month, year, calendar_frame  # Declare calendar_frame as global here
    month += direction
    if month == 0:
        month = 12
        year -= 1
    elif month == 13:
        month = 1
        year += 1

    # 이미 존재하는 calendar_frame 이 있다면 destroy
    if calendar_frame:
        calendar_frame.destroy()

    #calendar_frame 다시 만들어주기
    calendar_frame = tk.Frame(window)
    calendar_frame.grid()

    # 새로운 캘린더 출력(main함수랑 비슷하게 쓰는듯)
    print_month_year(month, year)
    
    start_date = get_start_day_of_month(month, year)
    num_days = days_in_month(month, year)
    make_buttons()
    month_generator(start_date, num_days)

def save_to_json():
    #Saves the calendar data to a JSON file.
    for day in range(1, len(text_object_dict) + 1):
        save_dict[day] = text_object_dict[day].get("1.0", "end - 1 chars")

    file_location = filedialog.asksaveasfilename(initialdir="/", title="Save JSON to..")
    if file_location:
        with open(file_location, 'w') as json_file:
            json.dump(save_dict, json_file)
#inintialdir : 초기 디렉토리
def load_from_json():
    #Loads calendar data from a JSON file.
    file_location = filedialog.askopenfilename(initialdir="/", title="Select a JSON to open")
    if file_location:
        with open(file_location) as json_file:
            global save_dict
            save_dict = json.load(json_file)
            for day in range(1, len(text_object_dict) + 1):
                text_object_dict[day].insert("1.0", save_dict.get(str(day), ""))

    
    
    







#main함수

#datepakage에서 날짜가져오기
month = date.today().month
year = date.today().year

window = tk.Tk()
window.title("Calendar")
window.geometry("1000x800")
window.columnconfigure(0,weight=1)

calendar_frame = tk.Frame(window)

calendar_frame.grid()

text_object_dict = {}
save_dict = {}

calendar_frame.grid()
make_buttons()
print_month_year(month, year)
start_date = get_start_day_of_month(month, year)
num_days = days_in_month(month, year)

month_generator(start_date, num_days)

window.mainloop()