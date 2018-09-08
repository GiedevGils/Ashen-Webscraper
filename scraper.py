import requests, pypandoc, datetime, os

from ConfigParser import SafeConfigParser
from bs4 import BeautifulSoup
from os.path import join as pjoin


# Startpage
currentPage = 1

# Define the config file
parser = SafeConfigParser()
parser.read('config.ini')

# Amount of pages to loop through
amountToLoopThrough = parser.get('Settings', 'amount-of-pages')

# Open the file to write to file
dir_path = pjoin("output")
file = open(pjoin(dir_path, "single_page.html"), "w", encoding="utf-8")

# Define allEntries as an array
allEntries = []

# Get a starttime
starttime = datetime.datetime.now()

# Declare a string to use in the while loop
looping = "Looping - Getting pages"

while True:
    # Check if the loop should be broken
    if currentPage >= amountToLoopThrough:
        break
    # Print looping to let know there's progress
    print(str(currentPage) + ": " + looping)

    # Make it fancy by adding full stops and all
    if len(looping) >= looping.find("s")+4:
        looping = looping.split('.')[0]
    else:
        looping += "."

    # Get the page
    page = requests.get("https://theashenchapter.enjin.com/home/m/8190140/viewthread/21525056-field-book-tz-davidss/page/" + str(currentPage), timeout=5)
    
    # Up the counter by one for the next iteration through the loop
    currentPage+=1

    # Get all the content of the page, as HTML
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get all entries by looking for divs with the class 'post-content'
    entries = soup.find_all("div", {"class":'post-content'})

    # Add the entries on a single webpage to the complete array
    allEntries.append(entries)
    
# For each entry object in allEntries, write it to the entry1.html file
for entry in allEntries:
    file.write(''.join(map(str, entry)))

# Close the file as garbage collection
file.close()

# Open a file to write to after the formatting
o = open(pjoin(dir_path, "entries.html"),"w") 

# Define the file to read from 
readable = open(pjoin(dir_path, "single_page.html"), "r")

# For each line in the readable file, replace the <u> and </u> tags with <h1> and </h1> respectively
for line in readable:
    # Actually replace the tags
    line = line.replace("<u>","<h1>")
    line = line.replace("</u>","</h1>")
    # Write it to the file
    o.write(line) 

# Close the file for garbage collection
o.close()

# Print it to show progress
print("Underlines replaced for " + str(currentPage - 1) + " pages.")

# Print to show progress
print("Coverting to .docx file.")

# Transform the formatted file to a .docx file
output = pypandoc.convert_file(pjoin(dir_path, "entries.html"), format='html', to='docx', outputfile=pjoin(dir_path, 'Fieldbook.docx'))

# Get the time information
endtime = datetime.datetime.now()
tdelta = endtime - starttime

print("Done!")
print("Started at: " + starttime.strftime("%H:%M:%S"))
print("Finished at: " + endtime.strftime("%H:%M:%S"))
print("All the work took: " + str(tdelta))