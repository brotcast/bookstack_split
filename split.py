#!/bin/python

import os
import re
import sys

# Path to Bookstack HTML files
src_path="./html"
dst_path="./extract"

# empty list
pages = []

if not os.path.isdir(dst_path):
    print("--ERROR-- dst_path does not exists")
    sys.exit(1)

if os.path.isdir(src_path):
    # open file from src_path
    for file in os.listdir(src_path):
            if file.endswith(".html"):

                # get booktitle from filename
                book=file.replace(".html", "")
                chapter=None
                page=None
                content=[]

                file=os.path.join(src_path, file)
                print("Book: " + file)
                f = open(file, "r")

                # read file line by line
                for line in f:
                    # Get chapter title
                    if '<div class="chapter-hint' in line.strip():
                        # regex get content between > me <
                        chapter=re.search('>(.+?)<', line).group(1) 

                    # Get page title
                    if '<h1 id="page-' in line.strip():
                        # if page in None
                        if not page:
                            page=re.search('>(.+?)<', line).group(1)
                        elif page != re.search('>(.+?)<', (line.strip())).group(1):
                            # Save completely loaded page
                            pages.append({"book":book, "chapter":chapter, "page":page, "content":content})
                            # Reset after page change
                            chapter=None
                            content=[]
                            
                            # Set new page name
                            page=re.search('>(.+?)<', line).group(1)
                    
                    # Print content only if page is set. Prevent garbage prints
                    # append line to content
                    if page:
                        content.append(line.strip())

                # when file is closed append page dict to pages list
                pages.append({"book":book, "chapter":chapter, "page":page, "content":content})
   
                # close file
                f.close()
else:
    print("--ERROR-- src_path does not exist")
    sys.exit(1)

# After loading everything to pages list, create folder and files
for item in pages:
    # Build filename
    if item["book"]:
        filename=dst_path + "/" +  item["book"].replace(" ", "_").replace("/", "-").lower()
        
        if item["chapter"]:
            filename=filename + "/" + item["chapter"].replace(" ", "_").replace("/", "-").lower()
        
        # Create folder
        if not os.path.exists(filename):
            os.makedirs(filename)
    
         # Create file 
        if item["page"]:
            filename=filename + "/" + item["page"].replace(" ", "_").replace("/", "-").lower() + ".html"
            if not os.path.isfile(filename):
                # Open append mode
                f = open(filename, "w")
                # write line by line
                for line in item["content"]:
                    f.write(line)
                f.close()
    
        print("File " + filename + " created")

    #print(item["book"] + " > " + str(item["chapter"]) + " > " + item["page"])
    #for line in item["content"]:
    #    print("\t"+line)   

