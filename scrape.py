import urllib.request as urllib2
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

#min is 0, max is 21,400

#column names: date, player name and notes

def scrapeWebsite(url):

	#driver = webdriver.Chrome()
	

	madeDict = {"Date": [], "Team": [], "Name": [], "Relinquished": [], "Notes": []}

	#for i in range(0, 214025, 25):
	for i in range(0, 100, 25):

		currUrl = url + str(i)
		#driver.get(currUrl)
		print(i)
		#soupPage = BeautifulSoup(driver.page_source, 'html.parser')
		page = urllib2.urlopen(currUrl)
		soupPage = BeautifulSoup(page, 'html.parser')

		info = soupPage.find('table', attrs={'class': 'datatable center'})
		extractedInfo = info.findAll('td')
		skipFirstRow = 0
		counter = 0
		for info in extractedInfo:
			firstPass = 0

			currentInfo = info.text.strip()

			#Date entry
			if(counter == 0):
				counter += 1
				madeDict["Date"].append(currentInfo)
			#Team entry	
			elif(counter == 1):
				counter += 1
				madeDict["Team"].append(currentInfo)
			#Name Entry
			elif(counter == 2):
				counter += 1
				#[2:] to clean up name
				#madeDict["Name"].append(currentInfo[2:])
				madeDict["Name"].append(currentInfo)
			#Relinquished entry
			elif(counter == 3):
				counter += 1
				#madeDict['Relinquished'].append(currentInfo[2:])
				madeDict['Relinquished'].append(currentInfo)
			#Notes entry
			else: #counter == 4
				counter = 0
				madeDict["Notes"].append(currentInfo)


		print(madeDict)

	return madeDict

def cutOffSpecialCharacters(x):
	if x == "Acquired" or x == "Relinquished":
		return x
	else:
		return x[2:]


if __name__ == "__main__":
	generatedDict = scrapeWebsite("https://www.prosportstransactions.com/football/Search/SearchResults.php?Player=&Team=&BeginDate=&EndDate=&PlayerMovementChkBx=yes&submit=Search&start=")

	dataFrameDict = pd.DataFrame.from_dict(generatedDict)

	dataFrameDict['Name'] = dataFrameDict['Name'].apply(lambda x: cutOffSpecialCharacters(x))
	dataFrameDict['Relinquished'] = dataFrameDict['Relinquished'].apply(lambda x: cutOffSpecialCharacters(x))

	dataFrameDict = dataFrameDict.drop(['Team', 'Relinquished'], axis = 1)


	dataFrameDict = dataFrameDict[dataFrameDict.Date != 'Date']

	export_csv = dataFrameDict.to_csv ('output.csv', index = False, header=True) #Don't forget to add '.csv' at the end of the path