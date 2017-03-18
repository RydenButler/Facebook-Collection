import urllib.request
import json
import simplejson
from lxml import html
import requests
from pandas import DataFrame, read_csv
import math
import time

OUTPUT_AS_BYTES = False
STANDARD_NODE_LIMIT =  10
POSTS_LIMIT = STANDARD_NODE_LIMIT
LIKES_LIMIT = 1000
PAGINATION = True
FINISH_ON_LIKES = True
DIRECTORY = '.\\output\\'
PRETTY_OUTPUT = False
RESTRICT_DATES = True
DATE_RANGE = ("2017-02-18", "2017-02-22")
START_TIME = time.strptime(DATE_RANGE[0], "%Y-%m-%d")
FINISH_TIME = time.strptime(DATE_RANGE[1], "%Y-%m-%d")

APP_SECRET = “INPUT_SECRET_HERE”
APP_ID = “INPUT_APP_ID_HERE”
access_token = APP_ID + "|" + APP_SECRET
graph_url = "https://graph.facebook.com/"

def create_node_url(node, edge = '', limit = STANDARD_NODE_LIMIT, fields = ''):
    node_url = graph_url + node + '/' + edge + '?limit=' + str(limit) + '&' + fields + '&' + 'access_token=' + access_token
    return(node_url)

def get_node(node, edge = '', limit = STANDARD_NODE_LIMIT, fields = '', pagination = PAGINATION):
    node_url = create_node_url(node, edge, limit, fields)
    web_response = urllib.request.urlopen(node_url)
    readable_page = web_response.read().decode("utf-8")
    node = json.loads(readable_page)
    get_next = pagination
    # If pagination is True then get_node cycles through every page and adds the elements of data to the
    # same attribute in the returned dict
    if pagination:
        next_node = node
        pages = 0
        while(get_next):
            # checks if the current page has a next page
            if 'paging' in next_node.keys():
                if 'next' in next_node['paging'].keys():
                    pages += 1
                    if pages % 10 == 0:
                        print("Page " + str(pages))
                    next_node_url = next_node['paging']['next']
                    web_response = urllib.request.urlopen(next_node_url)
                    readable_page = web_response.read().decode("utf-8")
                    next_node = json.loads(readable_page)
                    node['data'] += next_node['data']
                else: get_next = False
            else: get_next = False
    return(node)

def get_network(start_node, edge_list = [], date_range = DATE_RANGE):
    start_time = time.strptime(date_range[0], "%Y-%m-%d")
    finish_time = time.strptime(date_range[1], "%Y-%m-%d")
    lim = STANDARD_NODE_LIMIT
    network = {}
    # If edge_list is empty, simply return the listed start node. This is a base case of the recursion.
    if len(edge_list) == 0:
        network = get_node(start_node)
        return(network)
    else:
        # limit the number of likes or posts retrieved per page. To maximise efficiency, these
        # should be 1000 and 100 respectively. If PAGINATION = True then you should maximise.
        if edge_list[0] == 'likes':
            lim = LIKES_LIMIT
        if edge_list[0] == 'posts':
            lim = POSTS_LIMIT
        # If there is one edge to get (e.g. page_id/posts)
        if len(edge_list) == 1:
            next_node = get_node(start_node, edge_list[0], limit = lim)
            network = {}
            # If FINISH_ON_LIKES is True, only return a list of liker ids rather than each
            # liker as a node. This is a base case.
            if (FINISH_ON_LIKES & (edge_list[0] == 'likes')):
                network = []
                for i in range(len(next_node['data'])):
                    network += [next_node['data'][i]['id']]
            # If not, then get every subsequent edge of the current node as a leaf
            # (i.e. one more recursion of this function)
            else:
                network[edge_list[0]] = {}
                for i in range(len(next_node['data'])):
                    # time.sleep(1)
                    if (("created_time" in next_node['data'][i].keys()) & RESTRICT_DATES):
                        if time.strptime(next_node['data'][i]['created_time'][:10], "%Y-%m-%d") > finish_time:
                            continue
                    if (("created_time" in next_node['data'][i].keys()) & RESTRICT_DATES):
                        if time.strptime(next_node['data'][i]['created_time'][:10], "%Y-%m-%d") < start_time:
                            print('breaking')
                            return(network)
                    network[edge_list[0]][next_node['data'][i]['id']] = next_node['data'][i]
            return(network)
        # If there are 2 or more elements in edge_list continue the function recursively.
        else:
            next_node = get_node(node = start_node, edge = edge_list[0], limit = lim)
            network[edge_list[0]] = {}
            for i in range(len(next_node['data'])):
                if (("created_time" in next_node['data'][i].keys()) & RESTRICT_DATES):
                    if time.strptime(next_node['data'][i]['created_time'][:10], "%Y-%m-%d") > finish_time:
                        continue
                    else:
                        print(next_node['data'][i]['created_time'][:10])
                    if (("created_time" in next_node['data'][i].keys()) & RESTRICT_DATES):
                        if time.strptime(next_node['data'][i]['created_time'][:10], "%Y-%m-%d") < start_time:
                            print('breaking')
                            return(network)
                network[edge_list[0]][next_node['data'][i]['id']] = next_node['data'][i]
                network[edge_list[0]][next_node['data'][i]['id']][edge_list[1]] = get_network(network[edge_list[0]][next_node['data'][i]['id']]['id'], edge_list[1:], date_range)
            return(network)

def get_networks_from_user_list(user_list, edge_list = [], date_range = DATE_RANGE):
    start_time = time.strptime(date_range[0], "%Y-%m-%d")
    finish_time = time.strptime(date_range[1], "%Y-%m-%d")

    for user in user_list:
        print(user)
        network = {}
        try:
            network = get_network(user, edge_list, date_range)
        except Exception:
            print('Shite.')
        out_file_name = DIRECTORY + ((date_range[0] + '_' + date_range[1] + '_') if RESTRICT_DATES else '') + user + '.json'
        with open(out_file_name, 'w') as outfile:
            if PRETTY_OUTPUT:
                outfile.write(simplejson.dumps(network, indent = 4, sort_keys = True))
            else:
                outfile.write(json.dumps(network))
    
def find_total_edges(node, edge):
    if edge in ['posts']:
        lim = POSTS_LIMIT
    elif edge in ['likes']:
        lim = LIKES_LIMIT
    else:
        lim = STANDARD_NODE_LIMIT
    num_edges = len(get_node(node, edge, limit = lim, pagination = True)['data'])
    return(num_edges)


def main():
    '''page_ids = ['senatoralfranken', 'amyklobuchar', 'SenatorAngusSKingJr', 'senatorbencardin', 'SenatorSasse', 'senatorsanders', 'billcassidy', 'billnelson', 'SenatorBobCasey', 'bobcorker', 'MenendezForNJ', 'SenBrianSchatz', 'SenatorCortezMasto', 'senatorchriscoons', 'ChrisMurphyCT', 'chrisvanhollen', 'grassley', 'senschume', 'senatormccaskill', 'corybooker', 'SenCoryGardner', 'SenDanSullivan', 'SenatorDavidPerdue', 'SenDeanHeller', 'senatordebfischer', 'stabenow', 'SenatorFeinstein', 'SenatorDurbin', 'EdJMarkey', 'ElizabethWarren', 'SenGaryPeters', 'SenatorHeidiHeitkamp', 'SenJackReed', 'SenatorLankford', 'SenatorShaheen', 'senatorjeffflake', 'jeffmerkley', 'jerrymoran', 'jiminhofe', 'SenatorRisch', 'senatordonnelly', 'JoeManchinIII', 'barrassoforwyoming', 'BoozmanforArkansas', 'SenJohnCornyn', 'SenatorJohnHoeven', 'senatorjohnmccain', 'JohnKennedyLouisiana', 'johnthune', 'isakson', 'senatortester', 'senjoniernst', 'SenatorKamalaHarris', 'KirstenGillibrand', 'senatorlamaralexander', 'LindseyGrahamSC', 'SenLisaMurkowski', 'SenatorLutherStrange', 'SenatorHassan', 'SenatorMarcoRubio', 'senatorcantwell', 'MarkRWarner', 'MartinHeinrich', 'senatorhirono', 'senbennetco', 'mikecrapo', 'mikeenzi', 'senatormikelee', 'SenatorMikeRounds', 'mitchmcconnell', 'senatororrinhatch', 'SenPatRoberts', 'senatortoomey', 'SenatorPatrickLeahy', 'pattymurray', 'SenatorRandPaul', 'SenBlumenthal', 'SenatorRichardBurr', 'RichardShelby', 'senrobportman', 'SenatorWicker', 'senronjohnson', 'wyden', 'SenatorBlunt', 'SenatorWhitehouse', 'senshelley', 'sherrod', 'SteveDainesMT', 'susancollins', 'senatortammybaldwin', 'SenDuckworth', 'SenatorTedCruz', 'Thad-Cochran', 'SenatorThomTillis', 'SenatorKaine', 'SenatorTimScott', 'SenatorToddYoung', 'tomcarper', 'SenatorTomCotton', 'senatortomudall']'''

    '''page_ids = ["Sen.Franken", "amyklobuchar", "SenatorAngusSKingJr", "barbaraboxer", "senatormikulski", "senatorbencardin",  "senatorsanders", "billcassidy", "billnelson", "BobCaseyJr", "bobcorker", "senatormenendez", "BrianSchatz", "senatorchriscoons", "ChrisMurphyCT", "grassley", "chuckschumer", "clairemccaskill", "corybooker", "CongressmanGardner", "180671148633644", "DanSullivanforAlaska", "perduesenate", "davidvitter", "DeanHeller", "senatordebfischer", "stabenow", "DianneFeinstein", "SenatorDurbin", "EdJMarkey", "ElizabethWarren", "88851604323", "HarryReid", "HeidiforNorthDakota", "SenJackReed", "RepLankford", "SenatorShaheen", "JeffFlake1", "jeffmerkley", "jeffsessions", "jerrymoran", "jiminhofe", "10148632367", "168059529893610", "10150135395755200", "johnbarrasso", "JohnBoozman", "Sen.JohnCornyn", "SenatorJohnHoeven", "johnmccain", "johnthune", "isakson", "senatortester",  "kellyayottenh", "KirstenGillibrand", "lamaralexander", "USSenatorLindseyGraham", "SenLisaMurkowski", "SenatorMarcoRubio", "senatorcantwell", "SenatorKirk", "MarkRWarner", "VoteMartinHeinrich", "mazie.hirono", "senatorbennet", "mikecrapo", "mikeenzi", "senatormikelee", "mikerounds", "McConnellForSenate", "OrrinHatch", "SenPatRoberts", "senatortoomey", "PatrickLeahy", "pattymurray", "senatorrandpaul", "dickblumenthal", "senatorburr", "RichardShelby", "robportman", "senatorwicker", "senronjohnson", "wyden", "SenatorBlunt", "SenatorWhitehouse", "8057864757", "sherrod", "SteveDainesMT", "susancollins", "TammyBaldwin", "SenatorTedCruz", "112579798754326", "ThomTillisNC", "timkaine", "RepTimScott", "tomcarper", "cottonforcongress", "senatortomudall", "RepKinzinger", "CongressmanSchiff", "RepAdamSmith", "AdrianSmithNE", "RepAlGreen", "alangrayson", "lowenthalforcongress2012", "81058818750", "95696782238",   "RepAmiBera", "200388204657", "CongressmanAndreCarson", "harrisforcongress",  "RepKirkpatrick", "RepAnnWagner", "RepAnnaEshoo", "kuster", "RepAustinScott",  "RepBarbaraLee",  "RepBenRayLujan", "7259193379", "BetoORourkeTX16", "repbettymccollum", "RepBillFlores", "CongressmanBillFoster", "rephuizenga", "RepBillJohnson", "183092598372008", "pascrell", "bill.posey15", "Rep.Shuster", "Rep.Billy.Long", "BlaineLuetkemeyer", "BlakeFarenthold", "RepBobGibbs", "6459789414",  "congressmanbobbyrush", "CongressmanBobbyScott",   "63158229861", "USABrad", "byrneforalabama",   "21836146886",  "RepBrianHiggins",   "CongresswomanCandiceMiller",  "RepCarolynMaloney", "mcmorrisrodgers", "RepRichmond", "RepBoustany", "ChuckFleischmann", "CBRangel", "congressmandent", "ChelliePingree", "RepCheri",  "RepChrisGibson", "group.php", "RepChrisStewart", "chrisvanhollen",   "congresswomanbrown",  "ClawsonTheOutsider", "cynthia.lummis", "CongressmanDan", "Kildee",  "78476240421",  "repdanlipinski", "RepWebster",   "CongressmanIssa", "DaveLoebsack", "repdavereichert", "davebratforcongress", "CongressmanDavidCicilline", "DavidJollyCD13", "RepDaveJoyce", "RepMcKinley", "8338225975", "dcrouzer", "repdavidschweikert", "113303673339",  "106005029501370",   "RepDebbieWassermanSchultz", "186775984680072", "CongressmanDennyHeck",   "DianaDeGette", "DianeBlackTN06", "dinatitusforcongress",  "RepDonYoung",   "673569277", "doris.matsui", "78720895942", "LaMalfaUSRep",  "DuncanHunter", "100001266049722",   "blumenauer", "Ed4Colorado", "CongresswomanEBJtx30", "EdRoyce", "elijahcummings", "103355984852", "EliseforCongress%7C", "EstyforCongress", "emanuelcleaverii", "Swalwellforcongress", "128558293848160",  "UsCongressmanFilemonVela", "111799732192", "6403238609", "7872057395", "6517277731", "RepFredUpton", "RepWilson",  "congressmangkbutterfield",   "RepGeneGreen", "GeorgeHoldingforCongress", "177164035838",  "CongressmanGT", "repgracemeng", "RepGraceNapolitano", "repgregwalden", "GreggHarper", "gregory.meeks", "GusBilirakis",  "GwenSMoore",   "115356957005", "152569121550", "iroslehtinen", "JackieSpeier", "standwithjackie", "206613968946", "jameseclyburn",  "janschakowsky", "RepJaniceHahn", "174429005962554", "jaredpolis", "212373730233", "JasonSmithForMissouri", "RepHensarling", "RepJeffDenham", "RepJeffDuncan", "jefffortenberry", "RepJeffMiller", "CongressmanNadler", "jerrymcnerney", "BridenstineForCongress", "JimCooper",  "CongressmanJimHimes", "repjimjordan", "CongressmanJimLangevin", "CongressmanJimMcDermott", "RepJimMcGovern", "repjimrenacci", "RepSensenbrenner", "326420614138023",  "RepJoeBarton", "joecourtney", "heck4nevada", "JoeWilson", "JohnCarneyDE", "judgecarter", "CongressmanConyers", "congressmanculberson", "johndelaneyforcongress", "CongressmanDuncan", "RepJohnFleming", "repgaramendi", "JohnKatkoForCongress", "16149655054", "RepJohnLarson", "RepJohnLewis", "JohnMica",   "JSarbanes", "repshimkus", "214258646163", "RepJoseSerrano", "JoeCrowleyNY", "JoeKennedyforCongress", "94156528752", "JoyceBeattyforCongress", "VargasforCongress", "RepJudyChu", "juliabrownley", "justinamash", "RepKarenBass", "KatherineClarkForCongress",  "USRepKathyCastor", "RepKayGranger", "Keith.Ellison", "keithrothfus",  "70063393423", "6349487899", "kevinbrady", "CongressmanKevinCramer", "CongressmanKevinMcCarthy", "CongressmanKevinYoder",  "repschrader", "ksinemaaz", "LamarSmithTX21", "RepLarryBucshon", "LeeMZeldin", "CongressmanLance", "CongresswomanLindaSanchez", "LloydDoggett", "loiscapps", "loisfrankel", "LorettaSanchez", "CongressmanLouBarletta", "50375006903", "RepLouiseSlaughter",  "RepGutierrez", "alukemesser", "replynnjenkins", "71389451419", "repmacthornberry", "CongressmanMarcVeasey",  "6225522279", "119538428117878", "MarkAmodei",  "MeadowsforCongress", "MarkPocan", "marksanford", "TakanoCA",  "mullinforcongress", "CongressmanMarlinStutzman",   "Representative.Martha.Roby", "cartwrightpa", "salmonforcongress",    "6916472567", "mecapuano",   "michaeltmccaul", "96007744606",   "MickMulvaneyforCongress",   "mike.conaway",   "CongressmanPompeo", "repmikequigley", "6406874733",   "105473048278", "morgangriffithforcongress", "NancyPelosi", "nikitsongas", "RepLowey",  "8037068318", "CongressmanMcHenry",  "PatrickMurphyforCongress",  "electpaulcook", "repgosar", "reppaulryan", "reppaultonko",  "20718168936", "petesessions",  "reppeteking", "RepRoskam", "repvisclosky", "PeterWelch",   "randyforbes", "RepHultgren", "Rep.Randy.Neugebauer", "119692511035", "Rep.Grijalva", "raul.r.labrador", "DrRaulRuiz", "157169920997203", "reneeellmers", "reprichardhanna",   "RepRichNugent",   "135654683137079", "221299057908533", "130802746950682", "RepRobWittman", "172573036140374", "RobertAderholt",  "RepDold", "RepRobertHurt", "237760959647650", "reprobinkelly",  "RepRodneyDavis", "1336791945", "rogerwilliamstx", "RonDeSantisFlorida", "repronkind", "CongresswomanRosaDeLauro",  "CongressmanRubenHinojosa",    "118514606128", "52454091867", "28619590584", "sanfordbishop",  "repscottgarrett",  "scottpeterssandiego", "167851429918010",  "RepSeanDuffy", "seanpatrickmaloneyforcongress",  "CongresswomanSheilaJacksonLee", "WhipHoyer",   "repstephenlynch",   "israelforcongress", "SteveKingIA", "RepStevePearce",  "RepSteveScalise",  "RepSteveWomack", "stevenpalazzo", "SusanBrooks2012",  "RepDelBene", "suzannebonamici", "TammyDuckworth", "CongressmanTedDeutch",  "106631626049851", "CongressmanTedYoho", "RepSewell",  "reptomrooney", "HuelskampforCongress",   "RepWalberg",  "RepToddRokita", "RepToddYoung", "TomColeOK04",  "reptomgraves", "info",   "reptomprice", "153594440504", "TomRiceforCongress", "100001348238852", "TrentFranks",  "143059759084016", "votetulsi", "CongressmanBuchanan",   "15083070102",   "106483796053597",  "repyvettedclarke"]
    '''

    page_ids = ['DonaldTrump']
    page_ids = ['amyklobuchar']

    edges = ['posts', 'likes']
    
    get_networks_from_user_list(user_list = page_ids, edge_list = edges)
    
if __name__ == "__main__":
    
	main()    