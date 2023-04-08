from py2neo import Graph, Node, Relationship
import torrequest
import re
import socks
import requests
from bs4 import BeautifulSoup

# Connect to Neo4j databases
links_graph = Graph("bolt://localhost:7687", auth=("neo4j", "User@123"))

# Regular expression pattern for onion links
onion_pattern = re.compile(r"http(s)?://[a-z2-7]{16}\.onion(/[a-zA-Z0-9-._~%!$&'()*+,;=]*)?")

onion_seeds = [
    "http://gkcns4d3453llqjrksxdijfmmdjpqsykt6misgojxlhsnpivtl3uwhqd.onion/"
    #anime site "http://xi5q6pwggnggxzaq4xdpyvwunwihq5zrwudjlxyk2ryy35wdsvioljyd.onion/"
    #"http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/cgi-bin/omega/omega",
    # "http://catalogpwwlccc5nyp3m3xng6pdx3rdcknul57x6raxwf4enpw3nymqd.onion/"
    ]

def torSearcher(url):
    # BEFORE YOU START - RUN tor.exe !!!!

    def get_tor_session():
        session = requests.session()
        # Tor uses the 9050 port as the default socks port
        session.proxies = {'http':  'socks5h://127.0.0.1:9050',
                           'https': 'socks5h://127.0.0.1:9050'}
        return session

    # Make a request through the Tor connection
    # IP visible through Tor
    session = get_tor_session()
    #url = "http://httpbin.org/ip"
    #url = "http://x.onion/"


    #ua_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577"
    #,"Mozilla/5.0 (X11) AppleWebKit/62.41 (KHTML, like Gecko) Edge/17.10859 Safari/452.6", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36"
    #,"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36", "Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"
    #,"Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"]
    #ua = random.choice(ua_list)
    #headers = {'User-Agent': ua}
    print("Getting ...", url)
    result = session.get(url)
    return result
    # Above should print an IP different than your public IP
    # Following prints your normal public IP
    #print(requests.get("http://httpbin.org/ip").text)
    

def crawl_onion_links():
    # Get unvisited onion links from Neo4j database
    # query = """
    #     MATCH (link:Link {status: 'unvisited'})
    #     RETURN link.url AS url
    # """
    # results = links_graph.run(query)

    for onion_link in onion_seeds:
       
        
        try:
            # Make a request to the onion link
            response = torSearcher(onion_link)
            print(str(response.text))
            # resp = str(response.text)
            # P
            
            soup = BeautifulSoup(response.text, "html.parser")

            text = str(soup.get_text()).strip().replace("\n", " ")
            #print(text)

            # query = """MATCH (link:Link ) 
            #     WHERE link.url = {onion_link}
            #     link.url""".format(onion_link= onion_link)

            # resp = links_graph.run(query, onion_link=onion_link, response=text)

            # node = resp.evaluate()
            # node['url'] = onion_link
            # node['text'] = text
            # node.push()
            # Find all links in the HTML
            links = soup.find_all("a")
            # Extract the link text and URL for each link
            link_info = []
            for link in links:
                link_text = link.get_text()
                link_url = link.get("href")
                link_info.append((link_text, link_url))
                print(link_info)

            # for item in link_info:
            #     # Extract the link text and URL
            #     link_text = item[0]
            #     link_url = item[1]
            #     # Check if the link is a valid onion link
            #     if link_url and onion_pattern.match(link_url):
            #         # Check if the link is already in the database
            #         query = """
            #             MATCH (link:Link)
            #             WHERE link.url = {link_url}
            #             RETURN link.url
            #         """.format(link_url=link_url)
            #         results = links_graph.run(query, link_url=link_url)
            #         if results.data():
            #             # Link already exists in the database
            #             pass
            #         else:
            #             # Link does not exist in the database
            #             # Add the link to the database
            #             # query = """
            #             #     MERGE (link:Link {url: {link_url}})
            #             #     ON CREATE SET link.name = {link_text} AND link.status = 'unvisited'
            #             #     RETURN link.name, link.url
            #             # """
            #             # results = links_graph.run(query, link_text=link_text, link_url=link_url)
            #             new_link = Node("Link", url=link_url, name=link_text, status="unvisited")
            #             links_graph.create(new_link)

            #             # Create a relationship between the onion link and the new link
            #             query = """
            #                 MATCH (link1:Link), (link2:Link)
            #                 WHERE link1.url = {onion_link} AND link2.url = {link_url}
            #                 MERGE (link1)-[r:LINKS_TO]->(link2)
            #                 RETURN link1.name, link2.name
            #             """.format(onion_link=onion_link, link_url=link_url)
            #             results = links_graph.run(query, onion_link=onion_link, link_url=link_url)

        except Exception as e:
            
            print(f"Error: {e}")

# Call the function to crawl onion links recursively
# while True:
crawl_onion_links()