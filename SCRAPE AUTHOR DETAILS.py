#Import required libraries
import requests
import bs4

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


#By using beautiful soup

#Requesting on link
basic_url = "https://www.theguardian.com/books/list/authorsaz#keyword1"
request = requests.get(basic_url)

#Getting author names
soup = bs4.BeautifulSoup(request.text,'lxml')
authors_tag = soup.select("ol")
                          
authors = []
for num in range(1,len(authors_tag)-1):
    sub_authors = authors_tag[num].text
    for author in sub_authors.strip().split('\n'):
        authors.append(author.strip())






#Some Authors names are mismatched in the website while scraping the book of them. So replacing the names with
# desired names as per in the website
original_author_names = ["WH Auden","JG Ballard","AS Byatt","GK Chesterton","JM Coetzee","Junot Diaz",
                        "Alexandre Dumas, pere","EM Forster","G Willow Wilson","EL James","PD James","AL Kennedy",
                        "RD Laing","Ursula K Le Guin","CS Lewis","George RR Martin","AD Miller","VS Naipaul","RK Narayan",
                        "JK Rowling","Saki (Hector Hugh Munro)","JD Salinger","Sarah J Maas","Dorothy L Sayers",
                         "WG Sebald","TS Eliot","Francois Marie Arouet de Voltaire","HG Wells","PG Wodehouse","WB Yeats",
                        "Slavoj Zizek","Emile Zola","William Shakespeare"]
#Indexes of original authors names
indexes = []
for name in original_author_names:
    index = authors.index(name)
    indexes.append(index)
#Replacing the original names with desired value as per the website
replaced_authors_names = ["W.H. Auden","J.G. Ballard","A.S. Byatt","G.K. Chesterton","J.M. Coetzee","Junot Díaz",
                         "Alexandre Dumas","E.M. Forster","G. Willow Wilson","E.L. James","P.D. James","A.L. Kennedy",
                         "R.D. Laing","Ursula K. Le Guin","C.S. Lewis","George R.R. Martin","A.D. Miller","V.S. Naipaul",
                         "R.K. Narayan","J.K. Rowling","Saki","J.D. Salinger","Sarah J. Maas","Dorothy L. Sayers",
                          "W.G. Sebald","T.S. Eliot","Voltaire","H.G. Wells","P.G. Wodehouse","W.B. Yeats",
                          "Slavoj Žižek","Émile Zola","William Shakespeare"]
#Replcaed the value by using the indexes
for indx,value in zip(indexes,replaced_authors_names):
    authors[indx] = value








#By using selenium
path = "C:\Program Files\msedgedriver.exe"
driver = webdriver.Edge(path)

second_url = "https://www.thriftbooks.com/"
driver.get(second_url)


#Finding the author books
for author in authors:  
    search_for_input = driver.find_element_by_class_name("Search-input.is-empty")
    search_for_input.send_keys(author)
    search_for_input.send_keys(Keys.RETURN)
        
    #Finding the total pages per author
    try:
        search_for_total_page_num = driver.find_elements_by_class_name("Pagination-bar")[0]
        total_string = " ".join(search_for_total_page_num.text.split("\n")).split(" ")
    
        no_of_pages = -1
        
        for word in total_string:
            if word.isdigit():
                no_of_pages += int(word)
                break


        # Saving the author books
        books_list = []          

        #Looping throug pages
        for page in range(no_of_pages):

            #List of elements and its length
            list_of_book_details = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "SearchResultTileItem-topSector")))
            length_of_list = len(list_of_book_details)

            #Looping through each book and saving the title
            for index in range(length_of_list):
                try:
                    book_details = list_of_book_details[index].text
                    back_to_string = " ".join(book_details.split("\n"))
                    book_details_in_list_format = list(back_to_string.partition("by"))

                    author_name = book_details_in_list_format[2].strip()
                    book_title = book_details_in_list_format[0].strip()

                    if author == author_name:
                        books_list.append(book_title)
                except:
                    pass

            #To the next page
            Next = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "Pagination-link.is-right.is-link")))
            time.sleep(15)

            #To the next page
            try:
                Next.click()
            except:
                Next.click()

        #Converting list into string to save into text file
        books = ", ".join(books_list)    

        #Saving the data text file 
        with open('Author book details.txt',mode='a') as f:
                f.write(f"AUTHOR NAME: {author} \nBOOKS: {books}\n\n")
    
        #Reload the web page
        refresh_web_page = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME,"DesktopHeader-logoLink")))
        time.sleep(15)

        try:
            refresh_web_page.click()
        except:
            refresh_web_page.click()
            
    except:
        #Saving the data text file 
        with open('Author book details.txt',mode='a') as f:
                f.write(f"AUTHOR NAME: {author} \nBOOKS: {books}\n\n")
                
        #Reload the web page
        refresh_web_page = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME,"DesktopHeader-logoLink")))
        time.sleep(15)

        try:
            refresh_web_page.click()
        except:
            refresh_web_page.click()
            
print("Done with the scraping")