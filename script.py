import http.client
import json
import time
import sys
import collections
import csv

#api_key = "8f347b492ad708ba7ffc3aeaebf5ef49"
url = "https://api.themoviedb.org/3/discover/movie?api_key="+sys.argv[1]+"&sort_by=popularity.desc&primary_release_date.gte=2004-01-01&with_genres=18&page=1"
print("The API Key is: "+sys.argv[1])

conn = http.client.HTTPSConnection("api.themoviedb.org")
payload = "{}"
myJSON = ""
movieList =[]
counter = 0

for page_num in range(1,20):
    print("Page_Num beginning of loop: " + str(page_num))
    conn.request("GET", "/3/discover/movie?api_key="+sys.argv[1]+"&sort_by=popularity.desc&primary_release_date.gte=2004-01-01"
                                                             "&with_genres=18&page="+str(page_num), payload)
    res = conn.getresponse()
    data = res.read()
    myJSON = data.decode('utf8')
    print(myJSON)
    print('- ' * 20)
    finalJSON = json.loads(myJSON)
    print(finalJSON['results'])
    for each in finalJSON['results']:
        refinedDict1 ={'Counter': counter, 'ID': each['id'], 'Title': each['title'], 'Popularity': each['popularity']}
        movieList.append(refinedDict1)
        counter += 1
    time.sleep(0.2)

print("****************************************************************")
print(movieList)

copiedList = []

for items in movieList:
    if(items['Counter'] <=350):
        copiedList.append(items)

print(copiedList)
print("Start Writing Movie List to CSV")
print("****************************************************************")

lst = []
for eachItem in copiedList:
    newDict = {'ID': eachItem['ID'], 'Title': eachItem['Title']}
    lst.append(newDict)

order = ["ID","Title"]

print("Writing")
with open('movie_ID_name.csv', 'w',newline='') as output_file:
    dict_writer = csv.DictWriter(output_file,order)
    #dict_writer.writeheader()
    dict_writer.writerows(lst)

print("****************************************************************")
print("Completed Writing Movie List to CSV, created movie_ID_name.csv")


print ("*" * 120)
print(" Retrieve first 5 similar movies for each")

conn = http.client.HTTPSConnection("api.themoviedb.org")

#movieIDTest = [504172,424694,480530,505954,446021,337167,254128]
movieIDs = []
for eachItem in lst:
    movieIDs.append(eachItem['ID'])

print("Printing the Movie IDs retrieved")
print(movieIDs)

movieSimilarList = []
movieSimilarIDs = []

print("Printing the Similar Movies json files")
for movieID in movieIDs:
    for page_num in range(1,2):
        conn.request("GET", "/3/movie/" + str(movieID) + "/similar?api_key=" + sys.argv[1], payload)
        res = conn.getresponse()
        data = res.read()
        myJSON = data.decode('utf8')
        #print(myJSON)
        print('- ' * 20)
        print("Retrieving similar movies for ID: " + str(movieID))
        finalJSON = json.loads(myJSON)
        #print(finalJSON['results'])
        counter = 0  # Resetting Counter
        for each in finalJSON['results']:
            if counter < 5:
                refinedDict2 = {'MovieID': movieID,'Counter': counter,  'SimilarID': each['id'], 'Title': each['title'],
                                'Popularity': each['popularity']}
                movieSimilarList.append(refinedDict2)
                refinedDict3 = {'MovieID': movieID, 'SimilarID': each['id']}
                movieSimilarIDs.append(refinedDict3)
            counter += 1
        time.sleep(0.2)

print("Similar Movie List")
print(movieSimilarIDs)


# print("Start Writing Similar List to CSV")
# print("****************************************************************")
#
# order = ["MovieID","SimilarID"]
#
# print("Writing")
# with open('simMovieList.csv', 'w',newline='') as output_file:
#     dict_writer = csv.DictWriter(output_file,order)
#     #dict_writer.writeheader()
#     dict_writer.writerows(movieSimilarIDs)
#
# print("****************************************************************")
# print("Completed Writing Similar Movie List to CSV")

swap=[]
newDict = {}
for eachItem in movieSimilarIDs:
    if (eachItem['MovieID'] > eachItem['SimilarID']):
        newDict = {'MovieID': eachItem['SimilarID'], 'SimilarID': eachItem['MovieID']}
        swap.append(newDict)
    if (eachItem['MovieID'] < eachItem['SimilarID']):
        newDict = {'MovieID': eachItem['MovieID'], 'SimilarID': eachItem['SimilarID']}
        swap.append(newDict)

# print("Start Writing Swap List to CSV")
# print("****************************************************************")
#
# order = ["MovieID","SimilarID"]
#
# print("Writing")
# with open('swapList.csv', 'w',newline='') as output_file:
#     dict_writer = csv.DictWriter(output_file,order)
#     #dict_writer.writeheader()
#     dict_writer.writerows(swap)
#
# print("****************************************************************")
# print("Completed Writing Swapped List to CSV")

dedupedList = []
for i in range(0, len(swap)):
    if swap[i] not in swap[i+1:]:
        dedupedList.append(swap[i])
    if swap[i] in swap[i+1:]:
        print("Duplicate Entry: "+str(swap[i]))

print("Start Writing Deduped List to CSV")
print("****************************************************************")

order = ["MovieID","SimilarID"]

print("Writing")
with open('movie_ID_sim_movie_ID.csv', 'w',newline='') as output_file:
    dict_writer = csv.DictWriter(output_file,order)
    #dict_writer.writeheader()
    dict_writer.writerows(dedupedList)

print("****************************************************************")
print("Completed Writing Deduped List to CSV")