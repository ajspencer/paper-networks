import web
import re
import json
import tempfile
import os
import os.path
import json
import sys
import pymysql
from threading import Lock
##Hack-y way of adding external package needed for reading PDFs
sys.path.insert(0, 'CiteSeerExtractor/src')
import service

#Declare the API endpoints of the application
urls = (
'/papers', 'paperHandler', #Handler for storing papers, getting the authors
'/', 'Index', #homepage
'/upload', 'upload', #upload page
'/papers/authors' , 'authorHandler', #API endpoint to get the authors of a paper, takes a path to the paper's location on the server
'/network', 'networkHandler', #API endpoint to get the dictionary of adjaceny lists for every author that is currently stored on the server
'/graphics', 'graphHandler' #API endpoint to get the network of connections among authors
)
#possible race condition when I upload two files at the same time?


class graphHandler:
    def GET(self):
        web.header('Content-Type', 'text/html')
        raise web.seeother('static/network.html')

class networkHandler:
    """Used for getting the network in json format"""
    def GET(self):
        db = pymysql.connect(host='localhost', user='root', password='root', db='network', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        web.header('Content-Type', 'application/json')
        cursor = db.cursor()
        sql = "select * from network"
        cursor.execute(sql)
        authors = cursor.fetchall()
        network = {}
        for author in authors:
            authorName = str(author['name'])
            authorConnections = str(author['adjacency'])
            authorConnections = re.sub('u[^a-zA-Z\d\s:]+','', authorConnections)
            authorConnections = authorConnections.split(',')
            web.debug(authorConnections);
            for connection in authorConnections:
                if(len(connection) > 0 and connection[len(connection) - 1] == '\''):
                    connection = connection[:-1]
                if(len(connection) > 0 and connection[0] == ' '):
                    connection = connection[1:]
            network[authorName] = authorConnections
        cursor.close()
        db.close()
        return json.dumps(network)

    """Insert into the network given a JSON of author meta data"""
    def POST(self, paperAuthors):
        #ensure json formatting
        paperAuthors = json.loads(paperAuthors)
        web.debug(paperAuthors)
        #Open the database connection
        db = pymysql.connect(host='localhost', user='root', password='root', db='network', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        if type(paperAuthors) == dict:
        #if it's a dictionary then there's only one author and we can just grab their name
            thisName = removeNonAscii(paperAuthors[0]['name'])
            #see if the database entry already exists
            sql = "select count(1) from network where name = %s"
            cursor.execute(sql, thisName)
            cursor.close()
            result = cursor.fetchone()
            if(not result):
                #there is only one person, so we can't say anything about whom they've published with
                #we will insert the empty string as a placeholder for the value
                cursor = db.cursor()
                cursor.execute(("insert into network (name, adjacency) values (%s, %s);"), (thisName, ''))
                cursor.close()
                db.commit()
            #if the database entry does already exist, then we don't need to do anything since there is only one author if the result is a singular dict, not a list
        #if it's a list there are multiple authors and we will iterate over the dictionary that contains their info
        if type(paperAuthors[0]) == list:
            authorsInThisList = []
            listOfAuthors = paperAuthors[0]
            #iterate over every dictionary in the list
            for author in listOfAuthors:
                thisName = removeNonAscii(author['name'])
                #if the one for this name does not already exist, make sure to add it!
                sql = "select count(1) from network where name = %s"
                cursor = db.cursor()
                cursor.execute(sql, (thisName))
                result = cursor.fetchone()
                cursor.close()
                if(not result['count(1)']):
                        #we need to make sure we add the form for a new name with no connections for all names that aren't currently in the database so that the next db query works correctly
                        cursor = db.cursor()
                        cursor.execute(("insert into network (name, adjacency) values (%s, %s);"), (thisName, ''))
                        cursor.close()
                        db.commit()
                #no matter what, we need to add the name to the list of authors in the list
                authorsInThisList.append(thisName)
            #now that we have all the authors, iterate over them and add their names to each of the lists
            for author in authorsInThisList:
                thisName = removeNonAscii(author)
                myPartners = []
                sql = "select adjacency from network where name = %s"
                cursor = db.cursor()
                cursor.execute(sql,thisName)
                currentAdj = cursor.fetchone()
                cursor.close()
                for otherAuthor in authorsInThisList:
                    if(thisName != otherAuthor):
                        myPartners.append(removeNonAscii(otherAuthor))
                sql = ("update network set adjacency = %s where name = %s")
                #strip out the brackets from the conversion to string so that the adjacency list is just a comma deliminated list
                cursor = db.cursor()
                cursor.execute(sql, (str(myPartners).strip('[]'), thisName))
                db.commit()
                cursor.close()
            #must close the connection with the database to end
            db.close()


class Index:
    """ Display the index page when the user loads the root of the application """
    def GET(self):
        web.header('Content-Type', 'text/html; charset=utf-8')
        raise web.seeother('static/index.html')

class upload:
    """ Display the index page when the user loads the root of the application """
    def GET(self):
        web.header('Content-Type', 'text/html; charset=utf-8')
        raise web.seeother('static/index.html')

class paperHandler:
    """Upload files given from the user to the server in the get request"""
    def POST(self):
        upload = web.input(image={})
        directory = 'papers'
        fileSubmit = authorHandler()
        #ensure that the file being uploaded is a pdf
        if 'image' not in upload or upload['image'].filename[-3:] != "pdf":
            web.ctx.status = '400 Please only upload .pdf files.'
            return
        name = upload.image.filename  #set the file name of the upload
        #Upload the file to the server, do the work of converting the pdf to a txt file and extract the author
        fout = open(directory + '/' + name, 'w+') #create a file to store the file the user uploaded in
        fout.write(upload.image.file.read()) #write the uploaded file the newly created file
        fout.close() #closes the newly uploaded file since the upload is complete
        #fileSubmit throws an attribute exception if the author attribute can not be accessed
        try:
            authors = fileSubmit.GET(name)
        except AttributeError as err:
            web.ctx.status = '400 Could not extract the author.'
            return
        except ValueError as err:
            web.ctx.status = '400 Not a valid paper'
            return
        #insert the authors into the database
        inserter = networkHandler()
        inserter.POST(authors)
        web.ctx.status = '200 done'

class authorHandler:
    """Call the API on a given paper and generate the text file from the pdf. Take the name of the paper"""
    def GET(self, name):
        #array to store all of the data for the funciton calls
        data = [];
        if(os.path.splitext('papers/' + name)[1] != '.pdf'):
            web.badrequest()
        if os.path.isfile('papers/' + name):
            #Call the API, generate a text file from the pdf so that we can extract the authors
            handler = service.FileHandler()
            result = handler.POST(os.path.abspath('papers/'+name))
            #if there was an error in the process, raise a value error
            if result:
                raise ValueError
            #raise another error to be handled by the caller
            #Call the API and extract the header information from the file
            extractor = service.Extractor()
            result = (extractor.GET(os.path.abspath('papers/' + name + '.txt'), 'header'))
            paperName = result.keys()[0]
            #get the dictionary that contains a tuple that has the list of authors
            if(result[paperName]['authors']):
                authors = result[paperName]['authors']['author']
                data.append(authors)
            else:
                raise AttributeError('Could not get the author of the paper')
        return json.dumps(data)

"""Implement logic for requests to be handled by a single thread. Each time  process starts it will aquire a lock and not release until completed"""
def mutex_processor():
    mutex = Lock()

    """Logic for aquiring a lock each time a process is started"""
    def processor_func(handle):
        mutex.acquire()
        try:
            return handle()
        finally:
            mutex.release()
    return processor_func

def removeNonAscii(text):
    return re.sub(r'[^\x00-\x7F]+',' ', text)


if __name__ == "__main__":
    app = web.application(urls, globals())
    #Single thread requests
    #TODO: only single thread request to author handler?
    app.add_processor(mutex_processor())
    app.run()
