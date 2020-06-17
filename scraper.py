import requests, pypandoc, datetime, os

from configparser import ConfigParser
from bs4 import BeautifulSoup
from os.path import join as pjoin

# Startpage
currentPage = 1

# Define the config file
parser = ConfigParser()
parser.read('config.ini')

# Amount of pages to loop through
amountToLoopThrough = int( parser.get('Settings', 'amount-of-pages') )
url = str( parser.get('Settings', 'url') )

# If the url does not end with a /, add one
if not url.endswith('/'):
    url = url + '/'

# Open the file to write to file
dir_path = pjoin("output")
file = open(pjoin(dir_path, "single_page.html"), "w", encoding="UTF-8")

# Define allEntries as an array
allEntries = []

# Get a starttime
starttime = datetime.datetime.now()

# Declare a string to use in the while loop
looping = " - Getting posts."

while True:
    # Check if the loop should be broken
    if currentPage > amountToLoopThrough:
        break
    # Print looping to let know there's progress
    print("Page " + str(currentPage) + looping)

    # Make it fancy by adding full stops and all
    if len(looping) >= looping.find(".")+3:
        looping = looping.split('.')[0]
    else:
        looping += "."

    # Get the page
    page = requests.get(url + str(currentPage), timeout=5)
    
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
o = open(pjoin(dir_path, "entries.html"),"w", encoding="utf-8") 

# Define the file to read from 
readable = open(pjoin(dir_path, "single_page.html"), "r", encoding="utf-8")

# Create the two tags that are defined in the settings as variables to use when adding headers
header_open = parser.get('Settings', 'header-tag')
header_close = header_open[:1] + '/' + header_open[1:]

# For each line in the readable file, replace the <u> and </u> tags with <h1> and </h1> respectively
for line in readable:
    # Actually replace the tags
    line = line.replace(header_open,"<h1>")
    line = line.replace(header_close,"</h1>")

    # Write it to the file
    o.write(line) 

# Close the file for garbage collection
o.close()

# Print it to show progress
print("Underlines replaced for " + str(currentPage - 1) + " pages.")

# Print to show progress
print("Coverting to .docx file.")

# Retrieve filename from settings
filename = parser.get('Settings', 'output-name')

# Transform the formatted file to a .docx file
output = pypandoc.convert_file(pjoin(dir_path, "entries.html"), format='html', to='docx', outputfile=pjoin(dir_path, filename + '.docx'))

# Get the time information
endtime = datetime.datetime.now()
tdelta = endtime - starttime

print("Done!")
print("Started at: " + starttime.strftime("%H:%M:%S"))
print("Finished at: " + endtime.strftime("%H:%M:%S"))
print("All the work took: " + str(tdelta) + " seconds.")