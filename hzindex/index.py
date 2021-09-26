import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, SchemaClass
import sys
import json


class IndexSchema(SchemaClass):
    Title = TEXT(stored=True)
    Article_id = ID(stored=True)
    Magazine_edition = ID(stored=True)
    Content = TEXT
    Date = TEXT(stored=True)
    Textdata = TEXT(stored=True)

def CreateIndex(root):
    if not os.path.exists("indexdir1"):
        os.mkdir("indexdir1")
 
    # Creating an index writer to add document as per defined schema
    ix = create_in("indexdir1",IndexSchema)
    writer = ix.writer()
 
    filepaths = [os.path.join(root,i) for i in os.listdir(root)]
    for path in filepaths:
        print(path)
        fp = open(path)
        data = json.load(fp)
        # print(data)
        writer.add_document(Title=data["Title"], Article_id=data["Article_id"],\
          Magazine_edition=data["Magazine_edition"], Content=data["Text"], Textdata=data["Text"], Date=data["Date"] )
        fp.close()
    writer.commit()
 
root = "pandora"
CreateIndex(root)

