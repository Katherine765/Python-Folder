import calendar


year = 2024
month = 2
day = 7

year_beg = int(str(year)[:2])
year_end = int(str(year)[2:])

century_code = {0:6,100:4,200:2,300:0}[year_beg % 4]
year_code = year_end + ((year_end/4 + 7) %7)

if calendar.isleap(year):
    month_code = {1:0,2:3,3:3,4:6,5:1,6:4,7:6,8:2,9:5,10:0,11:3,12:5}[month]
else:
    month_code = {1:6,2:2,3:3,4:6,5:1,6:4,7:6,8:2,9:5,10:0,11:3,12:5}[month]

final = (century_code + year_code + month_code + day) % 7

convert = {1:'Sun',2:'Mon',3:'Tues',4:'Wed',5:'Thurs',6:'Fri',7:'Fri'}




print(convert[final])

