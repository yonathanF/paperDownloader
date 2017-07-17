'''
gets top x number of papers from arxiv search result, downloads the pdf version, and updates a latex bib file. 
It will use a .yml file to get configuration such as keywords to search, how many papers to download, if it should try to
print the pdf papers, and so on. 
'''

import yaml
import urllib.request
import xml.etree.ElementTree as et

#a simple function that parses a yml config file and returns values
def parseConfigFile(fileLocation='config.yaml'):
    result=[]
    with open(fileLocation, 'r') as stream:
        try:
            result=(yaml.load(stream))

        except yaml.YAMLError as er:
            result.append(er)

    resToDic={}
    #todo a for loop might be nicer
    for dic in result:
        if 'AmountOfPapers' in dic.keys():
            resToDic['AmountOfPapers']=dic['AmountOfPapers']
        elif 'DownloadPdfs' in dic.keys():
            resToDic['DownloadPdfs']= dic['DownloadPdfs']
        elif 'UpdateBib' in dic.keys():
            resToDic['UpdateBib']=dic['UpdateBib']
        elif 'PrintPdfs' in dic.keys():
            resToDic['PrintPdfs']=dic['PrintPdfs']
        elif 'LocationOfPdfs' in dic.keys():
            resToDic['LocationOfPdfs']=dic['LocationOfPdfs']
        elif 'Keywords' in dic.keys():
            resToDic['Keywords']=dic['Keywords']
            
    return resToDic


#downloads papers depending on the config just parsed 
def getPapers():
    config=parseConfigFile()
    
    links=[]
    
    #look up each keyword and collects links 
    for searchTerm in config['Keywords']:
        xmlString=''
        with urllib.request.urlopen('http://export.arxiv.org/api/query?search_query=all:'+str(searchTerm)+'&start=0&max_results='+str(config['AmountOfPapers'])) as response:

            for line in response:
               xmlString+=line.decode('UTF-8')
        
        rootOfXml=et.fromstring(xmlString)

        for element in rootOfXml:
            if element.tag == '{http://www.w3.org/2005/Atom}entry':
                published=element[2].text
                title=element[3].text
                summary=element[4].text
                author=element[5][0].text
        
                for link in element.findall('{http://www.w3.org/2005/Atom}link'):
                    if 'type' in link.attrib.keys() and link.attrib['type'] == 'application/pdf':
                        links.append((link.attrib['href'], title))

    for link in links:
        with urllib.request.urlopen(link[0]) as stream:
            with open(link[1]+".pdf", 'wb') as pdf:
                pdf.write(stream.read())
                print('Finished saving pdf')


getPapers()

