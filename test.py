#By Lily and Rebecca for CMPSC 463
#Project 2: Class Scheduling
#Look into 30 CMPSC/IST courses, schedule them into 5 classrooms from 7am to 6pm
# Greedy algorithm

# differerent courses:
# 1) CMPSC 312 - Computer Organization and Architecture
# 2) CMPSC 430 - Database Design
# 3) CMPSC 462 - Data Structures
# 4) CMPSC 463 - Design and Analysis of Algorithms
# 5) CMPSC 469 - Formal Languages with Applications
# 6) CMPSC 472 - Operation System Concepts
# 7) CMPSC 487W - Software Engineering and Design
# 8) CMPSC 330 - Advanced Programming in C++
# 9) CMPSC 360 - Discrete Mathematics for Computer Science
# 10) CMPSC 441 - Artificial Intelligence
# 11) CMPSC 445 - Applied Machine Learning in Data Science
# 12) CMPSC 446 - Data Mining
# 13) CMPSC 457 - Computer Graphics Algorithms
# 14) CMPSC 497 - Special Topics
# 15) CMSPC 313 - Assembly Language Programming
# 16) CMPSC 470 - Compiler Construction
# 17) CMSPC 221 - Object Oriented Programming with Web-Based Applications
# 18) CMPSC 412 - Data Structures Lab
# 19) CMPSC 413 - Algorithms Lab
# 20) CMPSC 475 - Applications Programming
# 21) CMPSC 496 - Independent Studies
# 22) CMPSC 414 - Contest Programming
# 23) CMPSC 421 - Net-centric Computing
# 24) CMPSC 444 - Secure Programming
# 25) CMPSC 438 - Computer Network Architecture and Programming
# 26) CMPSC 489 - Deep Learning for Computer Vision
# 27) CMPSC 488 - Computer Science Project
# 28) CMPSC 201 - Programming for Engineers with C++
# 29) CMPSC 131 - Programming and Computation I: Fundamentals
# 30) CMPSC 132 - Programming and Computation II: Data Structures

#Classes availiable from 7am - 6pm:
# 1) Woodland Building 342
# 2) Woodland Building 345
# 3) Woodland Building 343
# 4) Woodland Building 346
# 5) Sutherland Building 209

#importing from CSV (excel file)
#source: https://www.geeksforgeeks.org/reading-csv-files-in-python/
import csv

courses = []
#open the file
with open('final cmpsc463.csv', newline='') as file:
    reader = csv.reader(file)
    next(reader) #skip first row (header)
    #read each row, extract course number (first variable : 0)
    # course name (second variable : 1)
    # duration (third variable : 2)
    for row in reader:
        course_number = row[0]
        course_name = row[1]
        duration = int(row[2]) #conv duration to int
        courses.append((course_number, course_name, duration)) # store each course as a tuple



# using the activity selection problem solved using greedy algorithm as a base
# source: https://www.tutorialspoint.com/Activity-Selection-Problem
# instead of having n different activities with their starting time and ending time and having to select the max num of activities each person can solve,
# we have 5 different classrooms and we must decide how many classes can fit into one class from a schedule of 7am-6pm
# to start the greedy algorithm, we first have to sort from smallest duration to lngest duration
# using bubble sort:
n = len(courses)
for i in range(n):
    for j in range(0, n-i-1):
        if courses[j][2] > courses[j+1][2]: #compare the durations
            #swap if the duration i greater
            temp = courses[j]
            courses[j] = courses[j+1]
            courses[j+1] = temp

#now we must setup the classrooms and initial room times
# we used minutes as duration, so conv time into minutes from midnight
rooms = ['Woodland 342', 'Woodland 345', 'Woodland 343', 'Woodland 346', 'Sutherland 209']
# create a dictionary to store what classes happen in eaach room
#each room will have a list of scheduld classes
schedule = {room: [] for room in rooms}
# create another dictionary to keep track of what time each room is avalible
room_times = {room: 7 * 60 for room in rooms} #start at 7am in minutes from midnight (7 hours from midnight x 60 minutes each hour) = 420 minutes

# now startng the greedy algorithm
# we will assign classes one-by-one into the earliest avalible room
# begin a for loop over each course (after we finish sorting)
#set course index as 0
course_index = 0 #starting with first course
while course_index < len(courses):
    course_number, course_name, duration = courses[course_index] # course info
    earliest_room = None #track the room  that is avaliable earliest
    #set the earliest time to a large number so anything will be smaller
    #for this purpose, we will do the number of minutes in a 24-hour-period: 24 hours x 60 minutes  = 1440 minutes
    earliest_time = 24 * 60

    #check each room if the particular room is avaliable earlier than the others
    # also check if the class will fit before 6pm (in minutes, it is 18 hours from midnight x 60 minutes per hour = 1080 minutes).
    for room in rooms:
        #room must be avaliable earlier and class must finish before 6pm
        if room_times[room] < earliest_time and room_times[room] + duration <= 18 * 60:
            #set the earliest room to this room and set the earliest time to the rooms duration
            earliest_room = room
            earliest_time = room_times[room]
        #if theres already an earliest class, do this:

    #after checking all the rooms, if we found a room that can fit the course,
    if earliest_room is not None:
        start_time = room_times[earliest_room] # the start time is the room's avalaible time
        end_time = start_time + duration # end time is start time + duration
        #append the course to the room's schedule
        schedule[earliest_room].append((start_time, end_time, course_number, course_name))
        #update the room's next avaliable time to after this class finishes
        room_times[earliest_room] = end_time

        course_index += 1 #only move to next course if scheduled
    else:
        #this will break the loop
        break #means no rooms are avaliable, so we cant schedule more in this room

#function that turns minutes into AM/PM time
def mins_to_time(minutes):
    hour = int(minutes / 60) #for hour
    minute = int(minutes % 60) #get remainder, which is extra minutes
    time = "AM" if hour < 12 else "PM" #determine AM or PM
    #this converts 24-hour military time to 12-hour time
    hour = hour if 1 <= hour <= 12 else (hour - 12 if hour > 12 else 12)
  #return formatted time like 7:00AM
    return f"{hour}:{minute:02d} {time}"


#print schedule
for room in rooms:
    print(f"\nSchedule for {room}: ")
    for start, end, course_number, course_name in schedule[room]:
        print(f" {mins_to_time(start)} - {mins_to_time(end)}: {course_number} {course_name}")