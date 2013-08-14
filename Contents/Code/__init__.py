######################################################################################
#
#	KISS ANIME CHANNEL (BY TEHCRUCIBLE) - v0.03
#
######################################################################################

TITLE = "Kiss Anime"
PREFIX = "/video/kissanime"
ART = "art-default.jpg"
ICON = "icon-default.png"
ICON_LIST = "icon-list.png"
ICON_NEXT = "icon-next.png"
ICON_COVER = "icon-cover.png"
ICON_SEARCH = "icon-search.png"
BASE_URL = "http://kissanime.com"

######################################################################################
# Set global variables

def Start():

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON_COVER)
	VideoClipObject.art = R(ART)	
	TVShowObject.thumb = R(ICON_COVER)
	TVShowObject.art = R(ART)
	SeasonObject.thumb = R(ICON_COVER)
	SeasonObject.art = R(ART)
	EpisodeObject.thumb = R(ICON_COVER)
	EpisodeObject.art = R(ART)
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:22.0) Gecko/20100101 Firefox/22.0'
	
######################################################################################
# Params page_count & offset are used for paginating results and should not be changed

@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu():
	oc = ObjectContainer()
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Most Popular", category = "/MostPopular/?page=", page_count = 1, offset = 0), title = "Most Popular", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Latest Updates", category = "/LatestUpdate/?page=", page_count = 1, offset = 0), title = "Latest Updates", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key = Callback(ShowCategory, title="Newest Anime", category = "/Newest/?page=", page_count = 1, offset = 0), title = "Newest Anime", thumb = R(ICON_LIST)))
	oc.add(InputDirectoryObject(key=Callback(Search), title = "Search", prompt = "What are you searching for?", thumb = R(ICON_SEARCH)))
	return oc

######################################################################################
# Collects 50 results per page, paginates by groups of 10
	
def ShowCategory(title, category, page_count, offset):

	count = 0
	show_count = 0

	if offset >= 50:
		page_count += 1
		offset = 0

	oc = ObjectContainer(title1 = title)
	page_data = HTML.ElementFromURL("http://kissanime.com/AnimeList" + str(category) + str(page_count))
	
	for each in page_data.xpath("//table[@class='listing']//td//a"):
		if show_count < 10:
			show_url = BASE_URL + each.xpath("./@href")[0]
			show_title = each.xpath("./text()")[0].strip()
			
			if show_url.count("/") <= 4:		
				count += 1
				if count > offset:
					oc.add(GetShow(show_title, show_url))
					show_count += 1		
	
	offset += 10
	oc.add(NextPageObject(key = Callback(ShowCategory, title = title, category = category, page_count = page_count, offset = offset), title = "More...", thumb = R(ICON_NEXT)))
	
	if len(oc) < 1:
		Log ("page_data.xpath is empty")
		return ObjectContainer(header="Error", message="Something has gone horribly wrong...")  
	
	return oc

######################################################################################
# Finds total number of pages from Anime List and searches each for query in show_title - 10 Maximum
	
def Search(query):
	oc = ObjectContainer()
	page_count = 1
	show_count = 0
	last_page = HTML.ElementFromURL("http://kissanime.com/AnimeList?page=" + str(page_count)).xpath("//ul[@class='pager']/li[5]/a/@href")[0]
	total_pages = int(last_page.rsplit("=")[1])
	
	while page_count <= total_pages and show_count <= 10: 
		for each in HTML.ElementFromURL("http://kissanime.com/AnimeList?page=" + str(page_count)).xpath("//table[@class='listing']//td//a"):
			show_url = BASE_URL + each.xpath("./@href")[0]
			show_title = each.xpath("./text()")[0].strip()
			lower_title = show_title.lower()
			
			if lower_title.find(query.lower()) >= 0 and show_url.count("/") <= 4:
				oc.add(GetShow(show_title, show_url))
				show_count += 1
		
		page_count += 1
	
	if len(oc) < 1:
		Log ("Search returned no results.")
		return ObjectContainer(header="Search", message="Sorry, no results. Try being less specific.")  
	
	return oc
	
######################################################################################
# Collects metadata from show_url and returns TVShowObject	
	
def GetShow(show_title, show_url):
	page_data = HTML.ElementFromURL(show_url)
	show_thumb = page_data.xpath("//div[@class='rightBox'][1]//div[@class='barContent']/div/img/@src")[0]
	show_ep_count = len(page_data.xpath("//table[@class='listing']//td/a"))
	show_genres = page_data.xpath("//div[@id='leftside']//p[2]/a/text()")
	show_summary = '\r\n\r\n'.join(map(str, page_data.xpath("//div[@id='leftside']//p[5]/text()")))
	if len(show_summary) < 1:
		show_summary = '\r\n\r\n'.join(map(str, page_data.xpath("//div[@class='bigBarContainer'][1]//td/text()")))
	
	show_object = TVShowObject(
		key = Callback(PageEpisodes, show_title = show_title, show_url = show_url),
		rating_key = show_title,
		title = show_title,
		thumb = Resource.ContentsOfURLWithFallback(url = show_thumb, fallback='icon-cover.png'),
		summary = show_summary,
		episode_count = show_ep_count,
		viewed_episode_count = 0,
		genres = show_genres,
		rating = 10.0
		)
	
	return show_object

######################################################################################
# Loops over episode list in groups of 30, creating SeasonObjects with ListEpisodes()	

def PageEpisodes(show_title, show_url):

	page_data = HTML.ElementFromURL(show_url)
	show_thumb = page_data.xpath("//div[@class='rightBox'][1]//div[@class='barContent']/div/img/@src")[0]
	show_ep_count = len(page_data.xpath("//table[@class='listing']//td/a"))
	show_genres = page_data.xpath("//div[@id='leftside']//p[2]/a/text()")
	show_summary = '\r\n\r\n'.join(map(str, page_data.xpath("//div[@id='leftside']//p[5]/text()")))
	if len(show_summary) < 1:
		show_summary = '\r\n\r\n'.join(map(str, page_data.xpath("//div[@class='bigBarContainer'][1]//td/text()")))
	
	offset = 0
	rotation = (show_ep_count - (show_ep_count % 30)) / 30

	oc = ObjectContainer(title1 = show_title)
	
	while rotation > 0:
	
		start_ep  = offset
		end_ep = offset + 30
		
		oc.add(SeasonObject(
			key = Callback(ListEpisodes, show_title = show_title, show_url = show_url, start_ep = start_ep, end_ep = end_ep),
			rating_key = show_title,
			title = "Episodes " + str(start_ep + 1) + " - " + str(end_ep),
			thumb = Resource.ContentsOfURLWithFallback(url = show_thumb, fallback='icon-cover.png'),
			summary = show_summary,
			episode_count = 30,
			show = show_title
			)
		)
		offset += 30
		rotation = rotation - 1
	
	oc.add(SeasonObject(
		key = Callback(ListEpisodes, show_title = show_title, show_url = show_url, start_ep = offset, end_ep = offset + (show_ep_count % 30)),
		rating_key = show_title,
		title = "Episodes " + str(offset + 1) + " - " + str(offset + (show_ep_count % 30)),
		thumb = Resource.ContentsOfURLWithFallback(url = show_thumb, fallback='icon-cover.png'),
		summary = show_summary,
		episode_count = show_ep_count % 30,
		show = show_title
		)
	)
	
	return oc

######################################################################################
# Grabs metadata and returns EpisodeObject for episodes between start_ep and end_ep
	
def ListEpisodes(show_title, show_url, start_ep, end_ep):

	page_data = HTML.ElementFromURL(show_url)
	show_thumb = page_data.xpath("//div[@class='rightBox'][1]//div[@class='barContent']/div/img/@src")[0]
	show_summary = '\r\n\r\n'.join(map(str, page_data.xpath("//div[@id='leftside']//p[5]/text()")))
	if len(show_summary) < 1:
		show_summary = '\r\n\r\n'.join(map(str, page_data.xpath("//div[@class='bigBarContainer'][1]//td/text()")))	
	
	eps_list = page_data.xpath("//table[@class='listing']//td/a")
	eps_list.reverse()
	
	oc = ObjectContainer(title1 = show_title)

	for each in eps_list[int(start_ep):int(end_ep)]:
		ep_url = BASE_URL + str(each.xpath("./@href")[0])
		ep_title = each.xpath("./text()")[0].strip()
		
		oc.add(EpisodeObject(
			url = ep_url,
			rating_key = ep_title,
			title = ep_title,
			thumb = R(ICON_COVER),
			summary = "Watch " + ep_title,
			show = show_title
			)
		)

	return oc