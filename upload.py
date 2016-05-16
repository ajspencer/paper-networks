import web
import json
import tempfile
import os
import json
import sys
sys.path.insert(0, 'CiteSeerExtractor/src')
import service

#Declare the API endpoints of the application
urls = (
'/papers', 'paperHandler', #Handler for storing papers, getting the authors
'/', 'Index', #homepage
'/upload', 'upload', #upload page
'/papers/authors' , 'authorHandler' #API endpoint to get all the authors of all the papers that are currently stored on the server
)


class matrixCalculator:
    """Matrix calculator class to generate the matrix of author relationships."""
    #Static variable that keeps track of a list of the authors
    authorList = []

class Index:
    """ Display the index page when the user loads the root of the application """
    def GET(self):
        web.header('Content-Type', 'text/html; charset=utf-8')
        raise web.seeother('/static/index.html')

class upload:
    """ Display the index page when the user loads the root of the application """
    def GET(self):
        web.header('Content-Type', 'text/html; charset=utf-8')
        raise web.seeother('static/index.html')

class paperHandler:
    """Upload files given from the user to the server in the get request"""
    def POST(self):
        upload = web.input(image={})
        #ensure that the file being uploaded is a pdf
        if upload['image'].filename[-3:] != "pdf":
            web.ctx.status = '400 Please only upload .pdf files.'
            return
        web.debug(upload['image'].filename)
        return
        directory = 'papers'
        #Upload the file to the server, do the work of converting the pdf to a txt file and extract the author
        fileSubmit = authorHandler()
        if 'image' in upload:
            name = str(len(os.walk('papers').next()[2])) + '.pdf' #get a unique name for the file, name is arbitrary just needs to be unique
            fout = open(directory + '/' + name, 'w') #create a file to store the file the user uploaded in
            fout.write(upload.image) #write the uploaded file the ne newly created file
            fout.close() #closes the newly uploaded file since the upload is complete
            #fileSubmit throws an attribute exception if the author attribute can not be accessed
            authors = ''
            try:
                authors = fileSubmit.GET(name)
            except AttributeError as err:
                web.ctx.status = '400 Could not extract the author.'
                return
            except ValueError as err:
                web.ctx.status = '400 Not a valid paper'
                return
            matrixCalculator.authorList.append(authors)

class authorHandler:
    """Call the API on a given paper and generate the text file from the pdf. Take the name of the paper"""
    def GET(self, name):
        #array to store all of the data for the funciton calls
        data = [];
        if(os.path.splitext('papers/' + name)[1] != '.pdf'):
            web.badrequest()
        #for every file in thee directory of papers that are uploaded, call the API and store the value in an array
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

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
