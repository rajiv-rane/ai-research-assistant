# Step1: Access arXiv using URL

from winreg import QueryValue
import requests
import xml.etree.ElementTree as ET

from langchain_core.tools import tool

def search_arxiv_papers(topic:str, max_results:int =5)-> dict:
    # Handle advanced syntax if agent uses it (au:, ti:, etc)
    if any(prefix in topic.lower() for prefix in ['au:', 'ti:', 'abs:', 'all:', 'cat:']):
        query = topic.replace(" ", "+")
    else:
        # Default to multi-word AND search across all fields
        query = "all:" + "+AND+all:".join(topic.lower().split())

    for char in list('()"'):
        if char in query:
            print(f"Invalid character {char} in query: {query}")
            raise ValueError(f"Cannot have character: '{char}' in query: {query}")

    url=(
        "http://export.arxiv.org/api/query"
        f"?search_query={query}"
        f"&max_results={max_results}"
        "&sortBy=submittedDate"
        "&sortOrder=descending"
    )

    print(f"Making request to ArXiv API: {url}")
    res=requests.get(url)


    if not res.ok:
        print(f"ArXiv API request failed: {res.status_code}--{res.text}")
        raise Exception(f"Bad response from ArXiv API : {res}\n{res.text}")

    print(f"Status code:",res.status_code)
    # print(f"Status text:",res.text)

    data=parse_arxiv_xml(res.text)
    
    return data


# Step2: Parse XML 

def parse_arxiv_xml(xml_content:str)-> dict:
    """ Parse the XML content of an ArXiv API response into a dictionary of papers. """
    entries=[]
    ns={
        "atom":"http://www.w3.org/2005/Atom",
        "arxiv":"http://arxiv.org/schemas/atom"
    }
    root = ET.fromstring(xml_content)

    #loop thro each <entry> in Atom namespace
    for entry in root.findall("atom:entry",ns):
        #Extract authors
        authors=[
            author.findtext("atom:name",namespaces=ns)
            for author in entry.findall("atom:author",ns)
        ]

        #Extract categories
        categories=[
            cat.attrib.get("term", "")
            for cat in entry.findall("atom:category",ns) 
        ]
        
        #Extract PDf link (rel=related and type= "application/pdf")
        pdf_link=None
        for link in entry.findall("atom:link",ns):
            if link.attrib.get("type") == "application/pdf":
                pdf_link=link.attrib.get("href")
                break
        
        entries.append({
            "title":entry.findtext("atom:title",namespaces=ns),
            "summary":entry.findtext("atom:summary",namespaces=ns).strip(),
            "authors":authors,
            "categories":categories,
            "pdf":pdf_link
        })

    return {"entries":entries}

# print(search_arxiv_papers(topic="Prompt Engineering",max_results=5))


# Step3: COnvert the functionality into a tool

@tool
def arxiv_search(topic:str, max_results:int = 5)-> dict:
    """Search for recently uploaded arXiv papers
    Args:
        topic: The topic to search for papers about
        max_results: The maximum number of papers to return (default: 5)

    Returns:
        List of papers with their metadata including titile, authors, summary, etc
    """
    print("ARXIV Agent called")
    print(f"Searching arXiv for papers about: {topic}")
    try:
        papers=search_arxiv_papers(topic, max_results=max_results)
        if len(papers['entries'])==0:
            return {"error": f"No papers found for topic: {topic}", "suggestion": "Try a broader search term."}
        print(f"Found {len(papers['entries'])} papers about {topic}")
        return papers
    except Exception as e:
        print(f"ArXiv Tool Error: {str(e)}")
        return {"error": str(e), "message": "ArXiv search failed. Please try a simpler search term."}

