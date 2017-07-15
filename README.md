# paperDownloader
Downloads research papers from arXiv using a yaml config file that specifies topics, number of papers, and where the pdfs should be saved (among other things). The long term goal is to have a system that everyday at 6am downloads one research paper that's not already been downloaded. It will also update a Latex bib file for later citation. Might end up using MongoDb as a backend rather than just files and might add a 'print' feature. 

### Upcoming work
[] decide between plain file/folder and a database implementation
[] make sure duplicates are downloaded 
[] randomize the download and get only 1 pdf file (currently downloads top 5 for each topic)
[] write function to update a bib file 
[] write a cronjob or something to run it every x days at 6am
