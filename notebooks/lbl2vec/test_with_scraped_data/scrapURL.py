import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning 
import os

from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
from bs4.element import Comment

import numpy as np
import re
import string

# Disable displaying SSL verification warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

HEADERS = ({'User-Agent':
			'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
			'Accept-Language': 'en-US, en;q=0.5'})



# Helper function to filter out futile HTML tags
def tag_visible(element):
	blacklist = ['style', 'label', '[document]', 'embed', 'img', 'object',
				'noscript', 'header', 'html', 'iframe', 'audio', 'picture',
				'meta', 'title', 'aside', 'footer', 'svg', 'base', 'figure',
				'form', 'nav', 'head', 'link', 'button', 'source', 'canvas',
				'br', 'input', 'script', 'wbr', 'video', 'param', 'hr']
				
	if element.parent.name in blacklist:
		return False
	if isinstance(element, Comment):
		return False
	return True



def getTextFromURL(url):
	try:
		page = requests.get(url, headers=HEADERS)          #to extract page from website
		html_code = page.content                           #to extract html code from page

		soup = BeautifulSoup(html_code, 'html.parser')     #Parse html code
		text = soup.findAll(text=True)                     #find all text
		title = soup.title.string

		text_from_html = ''

		visible_texts = filter(tag_visible, text)  
		text_from_html = " ".join(t.strip() for t in visible_texts)

		text_from_html = text_from_html.strip()

		text_from_html = re.sub('\n', ' ', text_from_html)
		res = re.sub(' +', ' ', text_from_html)

		filename = "_".join(title.split())+".txt"
		with open(filename, 'w') as f:
			f.write(res)
		print(f"Output saved in file {filename}")

		return res

	except Exception as e:
		print(e)
		return(str(e))

os.chdir("scraped_articles")

os.chdir("business")
urls = [
	# FTX crypto
	"https://edition.cnn.com/2022/11/12/business/ftx-missing-funds/index.html",
	"https://edition.cnn.com/2022/11/12/business/ftx-hack/index.html",
	"https://edition.cnn.com/2022/11/11/business/cz-crypto-crisis/index.html",
	"https://edition.cnn.com/2022/11/09/business/bitcoin-crypto-prices-fall-ftx-binance-ctrp/index.html",
	"https://edition.cnn.com/2022/07/19/investing/bitcoin-cryptocurrencies-stocks-coinbase/index.html",
	# stocks
	"https://edition.cnn.com/2022/11/11/business/singles-day-sales-growth-hit-intl-hnk/index.html",
	"https://edition.cnn.com/2022/11/09/investing/dow-stock-market-today-midterms/index.html",
	"https://edition.cnn.com/2022/11/08/business/elon-musk-tesla-stock-sale-twitter-purchase/index.html",
	"https://edition.cnn.com/2022/11/11/investing/premarket-stocks-trading/index.html",
	"https://edition.cnn.com/2022/11/10/economy/cpi-inflation-report-october/index.html"
]

# os.chdir("educational")
# urls = [
# 	# whats DL
# 	"https://www.ibm.com/in-en/cloud/learn/deep-learning",
# 	"https://machinelearningmastery.com/what-is-deep-learning/",
# 	"https://www.analyticsvidhya.com/blog/2018/10/introduction-neural-networks-deep-learning/",
# 	# CNN LSTM
# 	"https://towardsdatascience.com/a-comprehensive-guide-to-convolutional-neural-networks-the-eli5-way-3bd2b1164a53",
# 	"https://www.ibm.com/cloud/learn/convolutional-neural-networks",
# 	"https://machinelearningmastery.com/gentle-introduction-long-short-term-memory-networks-experts/",
# 	# applications
# 	"https://www.analyticssteps.com/blogs/8-applications-neural-networks",
# 	"https://www.tutorialspoint.com/artificial_neural_network/artificial_neural_network_applications.htm",
# 	# machine learning
# 	"https://en.wikipedia.org/wiki/Machine_learning",
# 	"https://www.analyticsvidhya.com/blog/2021/12/a-guide-on-deep-learning-from-basics-to-advanced-concepts/"
# ]

# os.chdir("entertainment")
# urls = [
# 	# movies
# 	"https://www.ndtv.com/entertainment/ranveer-singh-honoured-with-etoile-dor-award-at-marrakech-actor-sings-gully-boy-rap-3513323",
# 	"https://indianexpress.com/article/entertainment/hollywood/black-panther-wakanda-forever-box-office-collection-day-1-marvel-sequel-outperforms-bollywood-releases-but-trails-doctor-strange-2-and-thor-4-8264149/",
# 	"https://www.hindustantimes.com/entertainment/bollywood/amitabh-bachchan-says-he-will-hesitate-to-go-to-mr-natwarlal-director-rakesh-sharma-s-funeral-101668310202189.html",
# 	"https://www.koimoi.com/box-office/uunchai-box-office-day-3-jumps-quite-well-on-saturday-needs-to-keep-growing/",
# 	"https://www.livemint.com/news/india/slash-prices-akshay-kumar-shares-formula-as-bollywood-struggles-to-see-light-of-success-11668333350291.html",
# 	"https://www.geo.tv/latest/452059-anya-taylor-joy-rejected-disney-for-this-role-find-out",
# 	# songs
# 	# "https://www.pinkvilla.com/entertainment/hollywood/does-louis-tomlinson-keep-in-touch-with-his-one-direction-bandmates-singer-reveals-1198624",
# 	"https://www.pinkvilla.com/entertainment/music-bank-in-chile-forced-to-cancel-txt-ateez-nct-dreams-performances-called-off-1198776",
# 	"https://www.indiatimes.com/entertainment/celebs/a-farmers-son-mc-square-gets-a-grand-welcome-at-his-hometown-after-winning-mtv-hustle-20-584618.html",
# 	"https://www.vogue.in/culture-and-living/content/bts-rm-reveals-first-solo-album-indigo-and-release-date",
# 	"https://www.indiatvnews.com/entertainment/music/jigar-mulani-s-new-song-tu-hi-toh-hai-stars-sumedh-mudgalkar-and-rhea-sharma-2022-11-10-822923"
# ]

# os.chdir("news")
# urls = [
# 	# india, modi, asean, summit, g20, indian, leaders, US
# 	"https://economictimes.indiatimes.com/news/india/india-should-shape-a-global-agenda-suresh-prabhu-former-union-minister-and-g20-sherpa/articleshow/95477894.cms",
# 	"https://www.livemint.com/news/india/g20-pm-narendra-modi-to-visit-indonesia-tomorrow-may-hold-bilateral-meeting-with-rishi-sunak-11668320761213.html",
# 	"https://economictimes.indiatimes.com/industry/renewables/india-for-phase-down-of-all-fossil-fuels-not-just-coal/articleshow/95480567.cms",
# 	"https://news.abplive.com/news/world/pm-modi-to-hold-several-bilateral-meetings-with-g20-leaders-will-address-indian-community-on-nov-15-external-affairs-ministry-1563121",
# 	"https://www.hindustantimes.com/india-news/us-supports-india-g-20-presidency-jaishankar-blinken-meet-discuss-ukraine-101668324207550.html",
# 	"https://www.ndtv.com/world-news/in-latest-gaffe-joe-biden-thanks-colombia-instead-of-cambodia-for-hosting-asean-summit-3516267",
# 	# us, democrats, republicans, poll, biden, election, senate, midterm
# 	"https://zeenews.india.com/world/us-midterm-polls-result-democrats-retain-majority-despite-republican-red-wave-predictions-2534621.html",
# 	"https://www.indiatoday.in/india/story/joe-biden-pleased-with-us-midterm-polls-turnout-2296727-2022-11-13",
# 	"https://www.ndtv.com/world-news/democrats-retain-control-of-the-us-senate-after-key-election-news-agency-afp-quoting-reports-3515469",
# 	"https://www.deccanherald.com/international/world-news-politics/cortez-masto-wins-nevada-senate-race-clinching-democratic-control-of-senate-1161880.html"
# ]

# os.chdir("ecommerce")
# urls = [
# 	# laptops
# 	"https://www.flipkart.com/redmibook-pro-core-i3-11th-gen-8-gb-256-gb-ssd-windows-11-home-thin-light-laptop/p/itm302328cdf5e24?pid=COMG4Z35GKZTRDSF&lid=LSTCOMG4Z35GKZTRDSFFNBHAW&marketplace=FLIPKART&q=laptop&store=6bo%2Fb5g&spotlightTagId=BestsellerId_6bo%2Fb5g&srno=s_1_1&otracker=search&otracker1=search&fm=Search&iid=4a640a3a-b937-4e29-a5c8-ea8d09b3d15d.COMG4Z35GKZTRDSF.SEARCH&ppt=sp&ppn=sp&ssid=7pk7c05fnbhael1c1668346740581&qH=312f91285e048e09",
# 	"https://www.flipkart.com/apple-2020-macbook-air-m1-8-gb-256-gb-ssd-mac-os-big-sur-mgn63hn-a/p/itmde54f026889ce?pid=COMFXEKMGNHZYFH9&lid=LSTCOMFXEKMGNHZYFH9P56X45&marketplace=FLIPKART&q=laptop&store=6bo%2Fb5g&srno=s_1_5&otracker=search&otracker1=search&fm=organic&iid=4a640a3a-b937-4e29-a5c8-ea8d09b3d15d.COMFXEKMGNHZYFH9.SEARCH&ppt=dynamic&ppn=dynamic&ssid=7pk7c05fnbhael1c1668346740581&qH=312f91285e048e09",
# 	"https://www.flipkart.com/hp-intel-core-i5-11th-gen-8-gb-512-gb-ssd-windows-10-home-14s-dq2535tu-thin-light-laptop/p/itmbdd471acce208?pid=COMG22MXENCNK53Y&lid=LSTCOMG22MXENCNK53Y7XB804&marketplace=FLIPKART&fm=productRecommendation%2Fsimilar&iid=R%3As%3Bp%3ACOMFXEKMGNHZYFH9%3Bl%3ALSTCOMFXEKMGNHZYFH9P56X45%3Bpt%3App%3Buid%3A9c9eadde-6358-11ed-8968-4b5e1f5f1f51%3B.COMG22MXENCNK53Y&ppt=pp&ppn=pp&ssid=7pk7c05fnbhael1c1668346740581&otracker=pp_reco_Similar%2BProducts_5_34.productCard.PMU_HORIZONTAL_HP%2BIntel%2BCore%2Bi5%2B11th%2BGen%2B-%2B%25288%2BGB%252F512%2BGB%2BSSD%252FWindows%2B10%2BHome%2529%2B14s-%2BDQ2535TU%2BThin%2Band%2BLight%2BLaptop_COMG22MXENCNK53Y_productRecommendation%2Fsimilar_4&otracker1=pp_reco_PINNED_productRecommendation%2Fsimilar_Similar%2BProducts_GRID_productCard_cc_5_NA_view-all&cid=COMG22MXENCNK53Y",
# 	"https://www.flipkart.com/asus-vivobook-15-2022-core-i5-10th-gen-8-gb-512-gb-ssd-windows-11-home-x515ja-ej562ws-x515ja-ej592ws-thin-light-laptop/p/itm2e65b7fbcb497?pid=COMG87FF2SD7ZHK6&lid=LSTCOMG87FF2SD7ZHK6CCCXCI&marketplace=FLIPKART&q=laptop&store=6bo%2Fb5g&srno=s_1_9&otracker=search&otracker1=search&fm=organic&iid=4a640a3a-b937-4e29-a5c8-ea8d09b3d15d.COMG87FF2SD7ZHK6.SEARCH&ppt=dynamic&ppn=dynamic&ssid=7pk7c05fnbhael1c1668346740581&qH=312f91285e048e09",
# 	# watches
# 	"https://www.amazon.in/Noise-ColorFit-Bluetooth-Monitoring-SmartWatch/dp/B09P18XVW6/ref=sr_1_15?crid=2W5TJZLIIM96V&keywords=smart+watch&qid=1668346683&qu=eyJxc2MiOiI3LjQxIiwicXNhIjoiNy40OCIsInFzcCI6IjYuNzUifQ%3D%3D&sprefix=smart+watc%2Caps%2C270&sr=8-15",
# 	"https://www.amazon.in/Noise-ColorFit-Display-Monitoring-Smartwatches/dp/B09PNKXSKF/ref=sr_1_3?crid=2W5TJZLIIM96V&keywords=smart+watch&qid=1668346683&qu=eyJxc2MiOiI3LjQxIiwicXNhIjoiNy40OCIsInFzcCI6IjYuNzUifQ%3D%3D&sprefix=smart+watc%2Caps%2C270&sr=8-3",
# 	# phones
# 	"https://www.reliancedigital.in/motorola-e32s-32-gb-3-gb-ram-misty-silver-mobile-phone/p/492849905?gclid=Cj0KCQiAyMKbBhD1ARIsANs7rEEwO5WZWmAbo6T4RtjlfKKAjLAKFNzUlanra7SveNrW8OmgVHqy4TgaArVwEALw_wcB",
# 	"https://www.amazon.in/OnePlus-Nord-Shadow-128GB-Storage/dp/B0B3CQBRB4/?_encoding=UTF8&pd_rd_w=YY4C2&content-id=amzn1.sym.86bd9ba7-f177-459f-9995-c8e962dd9848&pf_rd_p=86bd9ba7-f177-459f-9995-c8e962dd9848&pf_rd_r=5QAG5C8K12X7B7CPEF6T&pd_rd_wg=SWJ2m&pd_rd_r=46cd90ff-fe7f-43e6-b3dc-d15ad23e4b00&ref_=pd_gw_ci_mcx_mi",
# 	"https://www.reliancedigital.in/apple-iphone-13-128-gb-blue/p/491997702?gclid=Cj0KCQiAyMKbBhD1ARIsANs7rEH9zCloxwnEECV3BQbRrYpB5ILSHSO7GKVXpE_PxRHluiZ4_iDD1VsaAlhBEALw_wcB",
# 	"https://www.croma.com/apple-iphone-13-128gb-starlight-white-/p/243460?utm_source=google&utm_medium=ps&utm_campaign=SOK_PMax-iPhone&gclid=Cj0KCQiAyMKbBhD1ARIsANs7rEGTL6SZAS7IQnur3JJ8ZxMyuus9CgA82829FYQ6_9orD19c1kCW3xYaAsf4EALw_wcB"
# ]


print(f"Current directory: {os.getcwd()}")
for url in urls:
	getTextFromURL(url)

# print(getTextFromURL("https://medium.com/analytics-vidhya/topic-modelling-using-lda-aa11ec9bec13"))
