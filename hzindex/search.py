from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
import sys


def GetSearch(query):
    ix = open_dir("indexdir1")
     
    # query_str is query string
    # query_str = sys.argv[1]
    # Top 'n' documents as result
    topN = 100
    response = []
     
    with ix.searcher(weighting=scoring.Frequency) as searcher:
        query = QueryParser("Textdata", ix.schema).parse(query)
        results = searcher.search(query,limit=topN)
        try:
            for i in range(topN):
                response.append({"Title": results[i]['Title'], "Article_id" : results[i]['Article_id'], "Magazine_edition" : results[i]['Magazine_edition'], "Textdata": results[i]['Textdata'], "Score" : str(results[i].score)})
        except Exception as e:
            print(e)

    return response

print(GetSearch("auf"))

