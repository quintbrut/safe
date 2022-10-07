import requests, random, time, lxml, html5lib, json, pytz
from bs4 import BeautifulSoup as bs
from datetime import datetime 

listOfMuls = []
listOfAdjectives = [
	'bold',
	'spoilt ',
	'naughty ',
	'suspicious ',
	'frivolous ',
	'greedy',
	'deceitful ',
	'devious ',
	'sneaky ',
	'selfish ',
	'snobbish ',
	'arrogant',
	'aloof ',
	'eccentric ',
	'lazy ',
	'stubborn ',
	'rude ',
	'strict ',
	'sarcastic ',
	'cruel ',
	'evil ',
	'nosey ',
	'talkative ',
	'cunning',
	'tactless ',
	'touchy ',
	'ungrateful ',
	'grumpy ',
	'silly ',
	'forgetful ',
	'dull ',
	'aggressive ',
	'messy ',
	'hesitant ',
	'moody ',
	'bossy ',
	'clumsy ',
	'coward ',
	'careless ',
	'prejudiced ',
	'quirky ',
	'passive ',
	'timid ',
	'zany ',
	'stingy ',
	'obstinate',
	'vulgar',
	'coarse',
	'foolish',
	'boring',
	'impudent',
	'obnoxious',
	'daring',
	]
for x in listOfAdjectives:
	listOfMuls.append('Ork'+str(x).strip().capitalize())



# Создаем сесию пользователя
user = requests.Session()
# Браузер пользователя
userAgent = 'Mozilla/5.0 (Windows NT 10.0; rv:96.0) Gecko/20100101'
passForMults = '7shokpar7'
newMult = ''
myLevel = 0
myDots = []
url_take_card = ''
currentFightsCount = 0
goodRobsCount = 0
gand_id_for_request = 11691
user.headers = {
	    'user-agent': userAgent
	}
isAllowedToBuyEnergy = True

#Ссылки
url = 'https://pacan.mobi'
randomAttackUrl = url + '/index.php?r=crop/attackRandom'
urlToLight = url + '/index.php?r=site/layout&layout=light'
urlToDefault = url + '/index.php?r=site/layout&layout=default'
urlProfile = url + '/index.php?r=profile'
urlQuests = url + '/index.php?r=quests'
urlToHarvestAll = url + '/index.php?r=crop/harvest&id=all'
urlToCheckCropsByPage = url + '/index.php?r=crop/index&info=open&page='
urlToExchange = url + '/index.php?r=harvest/exchange'

# Ссылки точек
urlToOpen = url + '/index.php?r=crop/view&id='
urlToRemove = url + '/index.php?r=crop/remove&id='
urlToBoost = url + '/index.php?r=crop/boost&id='
urlToAdd = url + '/index.php?r=crop/add&id={0}&user_crop_id={1}'
urlToHarv = url + '/index.php?r=crop/harvest&id='

# Нужные нам точки 
needCrops = [
	'Магазин электроники "Синус"',
	'Мясная лавка "Гаф-Гафыч"',
	'#Казино "Royal"',
	'#Супермаркет "Пуля"',
	'#Ресторан "Бульвар"',
	'#Солярий "Шоколадка"'
]


songLines = [
	'Не позволяйте траве расти на пути дружбы. (Сократ)', 
	'Короли или правители - это не те, кто носит скипетр, а те, кто знает, как командовать. (Сократ)',
	]

LOST_CROP_NOTIFICATION = 'Эту точку уже кто-то обнес, дружище. Выбери другую.'

currentVictimBoxes = 0
currentVictimRelationsCops = 0
currentVictimRelationsBandits = 0


def login(userLogin,pasword):
	"""
	Функция авторизации
	"""
	
	
	loginData = {
	    'login': userLogin,
		'password': pasword
	}
	
	# Жмем кнопку авторизоваться с данными введенными ранее
	user.post(url + '/index.php?r=site/auth/', data=loginData)
	print('Авторизованы под ником ', userLogin)
	waitHalfSecond()

def writeToFile(nick):
	with open('combinat_result_temp.txt', 'a', encoding="utf8") as mf:
		mf.write(str(nick)+'\n')
	pass


def waitHalfSecond():
	#time.sleep(0.45)
	pass


def getSoup(url):
	waitHalfSecond()
	page = user.get(url)
	soup = bs(page.content, "lxml")
	return soup

def gotoband():
	user.get(url + '/index.php?r=gangBase/request&id='+str(gand_id_for_request))
	waitHalfSecond()
	user.get(url + '/index.php?r=gangBase/request&id='+str(gand_id_for_request))
	printWithLevel('заявка')

def setFunnyDescription():
	randomDate = random.randint(1,27)
	if randomDate<10:
		randomDate = '0'+str(randomDate)
	randomMonth = random.randint(1,11)
	if randomMonth<10:
		randomMonth = '0'+str(randomMonth)
	randomYear = random.randint(1980,1999)
	randonIndex = random.randint(0,len(songLines)-1)
	funnyDescription = songLines[randonIndex]
	user.post(urlProfile+'/edit', data = {
				'Profile[name]': 'Орыч',
				'Profile[city]': '',
				'Profile[info]': '',
				'Profile[phone]': '',
				'Profile[email]': '',
				'Profile[subscribed]': '0',
				'Profile[subscribed]': '1',
				'yt0': 'Сохранить',
				'Profile[birthday]': str(randomDate),
				'Profile[birthmonth]': str(randomMonth),
				'Profile[birthyear]': str(randomYear),
				'Profile[phone_code]': '7'})
	printWithLevel('Поставили описание: '+str(funnyDescription))
	waitHalfSecond()



	

def harvestAll():
	user.get(urlToHarvestAll)
	print('[{0}] Сбор всех точек.'.format(myLevel))


def removeDot(id_c):
	user.post(urlToRemove+str(id_c),data = {'confirm':'Базарю'})
	print('Удалил точку')
	waitHalfSecond()

def boostDot(id_c):
	user.post(urlToBoost+str(id_c),data = {'confirm':'Базарю'})
	print('Ускорил точку')
	waitHalfSecond()

def changeLayoutToLight():
	user.get(urlToLight)
	print('[Процесс] Ставим облегченный режим.')

def changeLayoutToDefault():
	user.get(urlToDefault)
	print('[Процесс] Ставим полный режим.')

def getAwards(x=5):
	changeLayoutToLight()
	print('[{0}] Проверка награды'.format(myLevel))
	for i in range(x):
		waitHalfSecond()
		try:
			openQuestsSoup = getSoup(urlQuests)
			aw_url = openQuestsSoup.find('a', attrs = {'class':'bttn_green'})['href']
			print('[{0}] Перейдем по ссылке: {1}'.format(myLevel, aw_url))
			user.get(url+aw_url)
		except Exception as e:
			pass
			# print('[Ошибка] Не удалось перейти по ссылке', e)
		waitHalfSecond()


def printWithLevel(text):
	print('[{0}] {1}'.format(myLevel,text))


def upgrade_stats():
	user.get(url + '/index.php?r=fights/params&param_id=strength')
	printWithLevel('Улучшили силу')
	#time.sleep(2)
	pass

def checkLevel():
	global myLevel
	docent = 0
	changeLayoutToLight()
	soup = getSoup(urlProfile)
	try:
		myLevel = int(soup.find('span',id='z-level').find("span").get_text())
		print('Мой уровень: ',myLevel)
	except:
		print('[Ошибка] Не получил данные о уровне')

def newAccount(mulLog):
	global user, newMult
	try:
		user.close()
	except:
		print('Нет сессий.')
	user = requests.Session()
	tutorialLinks = [
		url + '/index.php?r=site/index&no_cookies=1&reason=',
		url + '/index.php?r=tutorial/alternative/view&new=1',
		url + '/index.php?r=site/layout&layout=light',
		url + '/index.php?r=tutorial/alternative/finish',
		url + '/index.php?r=site/signUpPost']
	for idx, link in enumerate(tutorialLinks):
		user.get(link)
		print('[Туториал] Шаг {0} из {1}'.format(idx,len(tutorialLinks)))
		waitHalfSecond()
	
	
	user.post(url + '/index.php?r=site/signUpPost', data = {'login': str(mulLog), 'password': passForMults,'phoneOrMail':''})
	writeToFile(mulLog)
	print('[Туториал] Создали персонажа: ', mulLog)
	newMult = str(mulLog)
	checkLevel()

def addDot(type_id,id_c):
	user.get(urlToAdd.format(type_id,id_c))
	printWithLevel('Поставили: '+str(type_id))
	waitHalfSecond()

def harvDot(id_c):
	user.get(urlToHarv+str(id_c))
	printWithLevel('Запрос на сбор точки: '+str(id_c))
	waitHalfSecond()

def getDotsId(page=0):
	global myDots
	myDots = []
	changeLayoutToLight()
	waitHalfSecond()
	getCrops = getSoup(urlToCheckCropsByPage+str(page))
	dot_divs = getCrops.find_all('div', attrs = {'class':'dots-item'})
	for dot in dot_divs:
		try:
			url_corp = str(dot.find('a').get('href'))
			if len(url_corp) == 25:
				pass
			else:
				x = url_corp.split("id=")
				if len(x[1])>13:
					x2 = x[1]
					x3=x2.split("&")
					#print(x3)
					corp_x = x3[0]
					myDots.append(corp_x)
				else:
					corp_x = x[1]
					myDots.append(corp_x)
				
				
		except Exception as e:
			pass
			# print('[Ошибка] Не удалось получить данные о точке: ', e)
def harvestAllEachOne():
	printWithLevel('Соберем точки каждого по индивидуальному клику.')
	getDotsId()
	for id_c in myDots:
		harvDot(id_c)
		waitHalfSecond()
	user.get(urlToExchange)

def printStartMission(level):
	print('[Выполнение миссий] Уровень {0}, фактический: {1}'.format(str(level), myLevel))


def robs(count):
		
	def getPageCountAndVictimId(soup):
		pager = soup.find('div', attrs={'class': 'pager'})
		if pager == None:
			print('У жертвы нет больше 1-ой страницы, по этому 777')
			waitHalfSecond()
			return 777, 1
		else:
			lastPage = pager.find('li', attrs={'class': 'last'})
			if lastPage:
				lastCropsUrl = lastPage.find('a')['href']
				rawUrl = lastCropsUrl.split('&')
				victimId = int(rawUrl[1].split('id=')[1])
				pageCount = int(rawUrl[2].split('page=')[1])
				print('ID жертвы', victimId)
				print('Количество страниц', pageCount)
				return victimId, pageCount

			else:
				print('У жертвы нет больше 1-ой страницы')
				return 777, 1



	def getSortedCrops(cropContainer):
		sortedCrops = []
		for crop in cropContainer:
			ripe = crop.find('img', attrs={'alt': 'прибыль'})
			if ripe:
				# Подойдет
				sortedCrops.append(crop)

		print('Можно ограбить: ', len(sortedCrops))
		return sortedCrops

	def findTheNeedCrop(sortedCrops):
		foundCrops = []
		for crop in sortedCrops:
			# imgContainer = crop.findAll('img')
			# cropName = imgContainer[1]['alt'].strip()
			# if cropName in needCrops:
			# 	# print(cropName, ' нам нужен!')
			foundCrops.append(crop)
			# else:
			# 	# print(cropName, ' нам не нужен!')
			# 	pass
		print('Точки которые мы ищем: ', len(foundCrops), ' шт.')
		return foundCrops

	def getlinksToRob(foundCrops):
		harvestLinks = []
		for crop in foundCrops:
			harvestLink = crop.find('a')['href']
			harvestLinks.append(harvestLink)
		return harvestLinks

		pass

	def getAvailableCrops(robSoup):
		# pages = range(1,pageCount+1)
		allCrops = []
		# for page in pages:
		# 	waitHalfSecond()
		# 	pageUrl = url + '/index.php?r=crop/index&id={0}&page={1}'.format(victimId,page)
		# 	crops = getSoup(pageUrl)
		# 	if crops:
		cropContainer = robSoup.findAll('div', attrs={'class': 'field_empty'})
		if cropContainer:
			allCrops = allCrops + cropContainer
		print('Не отсортированные точки:', len(allCrops))
		sortedCrops = getSortedCrops(allCrops)
		foundCrops = findTheNeedCrop(sortedCrops)
		if len(foundCrops) != 0:
			linksToRob = getlinksToRob(foundCrops)
			robByLinks(linksToRob)
		else:
			print('Нет доступных точек')
			return 0
		print('С этим закончили!')
		return 1





	def getNotificationText(robSoup):
		notification = robSoup.find('div', attrs={'class': 'notification'})
		if notification:
			text = notification.get_text().strip()
			if text:
				return text
			else:
				return None


	def getNotificationFull(robSoup):
		notification = robSoup.find('div', attrs={'class': 'notification'})
		if notification:
			return notification
		else:
			return None


	def closeNotification():
		urlToCloseNotification = url + '/index.php?r=user/notice'
		urlToCloseElection = url + '/index.php?r=election'
		user.get(urlToCloseNotification)
		user.get(urlToCloseElection)
		print('Закрыли уведомление.')
		waitHalfSecond()


	def addToRewards(boxCount, relationCount, rewardType):
		global currentVictimBoxes, currentVictimRelationsCops, currentVictimRelationsBandits
		currentVictimBoxes = currentVictimBoxes + boxCount

		if rewardType == 'bandits':
			currentVictimRelationsBandits = currentVictimRelationsBandits + relationCount
		elif rewardType == 'cops':
			currentVictimRelationsCops = currentVictimRelationsCops + relationCount
		else:
			print(rewardType)


	def cleanCurrentRewars():
		global currentVictimBoxes, currentVictimRelationsCops, currentVictimRelationsBandits
		currentVictimBoxes = 0
		currentVictimRelationsCops = 0
		currentVictimRelationsBandits = 0



	def determineRewardType(notify):
		banditsImg = 'https://static.hata.mobi/i/relations/Reshetka.png'
		copsImg = 'https://static.hata.mobi/i/relations/Furazhka.png'
		cap = notify.find('img', attrs={'src': copsImg})
		lattice = notify.find('img', attrs={'src': banditsImg})
		if lattice != None:
			findOutReward(notify,'bandits')	
		elif cap != None:
			findOutReward(notify,'cops')
		else:
			# print('cap: ',cap, 'lattice: ',lattice)
			findOutReward(notify,'only-crops')
			


	def findOutReward(notify, rewardType):
		splitedText = notify.get_text().strip().split(' ')
		boxCount = int(splitedText[-4])
		relationCount = int(splitedText[-1].split('.')[0])
		addToRewards(boxCount, relationCount, rewardType)


	def getRobResult(text):
		splitedText = text.split(' ')
		if splitedText[0] == 'Стопе!':
			print(text.strip())
			return 'stop'
		elif splitedText[0] == 'Красава!':
			return 'next'	
		elif splitedText[0] == 'Нифига':
			return 'next'		
		elif splitedText[0] == 'Ты':
			print(splitedText)
			return 'next'
		elif splitedText[0] == 'Братан,':
			return 'energy'	
		elif splitedText[0] == 'Эту':
			return 'collected'	
		elif splitedText[0] == 'Мусорская':
			closeNotification()
			return 'notification'
		else:
			closeNotification()
			return 'notification'
		

	def one_rob(link):
		waitHalfSecond()
		robUrl = url + link
		robSoup = getSoup(robUrl)
		text = getNotificationText(robSoup)
		if text:
			result = getRobResult(text)
			if result == 'next':
				notify = getNotificationFull(robSoup)
				# determineRewardType(notify)
			return result
		else:
			print('Нет текста')
			# print(robSoup)
			return robSoup
				

	def buyEnergyRob():
		# urlToBuyEnergy = url + '/index.php?r=crop/energyRepair'
		# user.get(urlToBuyEnergy)
		print('Нет энергии, ждем 30 сек и продолжим')
		#time.sleep(30)

	def tryToRob(link):
		global goodRobsCount
		resultOfRob = one_rob(link)
		if resultOfRob == 'next':
			randInt = random.randint(1, 9)
			print('Ограбили [{0}/{1}]'.format(goodRobsCount, count))
			goodRobsCount = goodRobsCount + 1
			if goodRobsCount >= count:
				return 'enough'
			waitHalfSecond()
			return tryToRob(link)
		elif resultOfRob == 'energy':
			buyEnergyRob()
			waitHalfSecond()
			return tryToRob(link)
		elif resultOfRob == 'stop':
			return 'break'	
		elif resultOfRob == 'collected':
			print('Уже собрали')
			waitHalfSecond()
			return 'good'
		elif resultOfRob == 'notification':
			print('Уведомление какое то другое, закрыли')
			waitHalfSecond()
			return tryToRob(link)
		else:
			randInt2 = random.randint(1, 3)
			print('Харе так бешанно кликать! Ждем {0} секунд'.format(randInt2))
			#time.sleep(randInt2)
			return tryToRob(link)

	def robByLinks(linksToRob):
		print('Количество ссылок: ', len(linksToRob))
		for link in linksToRob:
			print('У нас ссылка есть: ', link)
			result = tryToRob(link)
			if result == 'break':
				print('Похоже тут охрана')
				break
			elif result == 'good':
				pass
			elif result == 'enough':
				print('А мы все!')
				return
			else:
				print('Не понятная аномалия')
				print(result)
				#time.sleep(1)

	def getCurrentTime():
		tzAlmaty = pytz.timezone('Asia/Almaty') 
		datetimeAlmaty = datetime.now(tzAlmaty) 
		robberyDate = datetimeAlmaty.strftime("%d.%m.%y %H:%M:%S")
		print('Дата ограбления: ', robberyDate)
		return robberyDate



	def getRewards():
		
		copsReward = '{0} - фуражек. '.format(currentVictimRelationsCops)
		banditsReward = '{0} - решеток. '.format(currentVictimRelationsBandits)

		rewards = '{0} - ящиков. '.format(currentVictimBoxes)

		if currentVictimRelationsBandits>0:
			rewards = rewards + banditsReward
		
		if currentVictimRelationsCops>0:
			rewards = rewards + copsReward

		if currentVictimBoxes == 0 and currentVictimRelationsCops == 0 and currentVictimRelationsBandits == 0:
			rewards = 'У человека охрана :) '

		print(rewards)
		return rewards

	def writeVictimAndRewardToFile(victimName):
		rewards = getRewards()
		robberyDate = getCurrentTime()
		with open("victimsNames.txt", "a", encoding='utf-8') as file:
			file.write(victimName + ': ' + rewards + robberyDate+'\n')

	def parseRandomRob():
		robSoup = getSoup(randomAttackUrl)
		notification = getNotificationText(robSoup)
		if notification:
			try:
				victimName = notification.split('фраера')[1].split('.')[0].strip()
				# victimId, pageCount = getPageCountAndVictimId(robSoup)
				
				# if victimId !=0 and pageCount != 0:
				isHaveResult = getAvailableCrops(robSoup)
				if isHaveResult:
					print('Похоже мы смогли ограбить что то!')
					return 1
				else:
					print('Мы не ограбили этого.')
					return 0
			except:
				closeNotification()
				return 0
			# else:
			# 	# print('Найдем друого!')
			# 	waitHalfSecond()
			# 	return 0
		else:
			closeNotification()
			return 0

	changeLayoutToDefault()
	global goodRobsCount
	goodRobsCount = 0
	while goodRobsCount < count:

		status = parseRandomRob()
		if status == 1:
			goodRobsCount = goodRobsCount + 1
		else:
			print('Дальше грабим!')
			waitHalfSecond()
	changeLayoutToLight()
	return
			


def fights(needFightsCount):
	global currentFightsCount
	currentFightsCount = 0
	rivalUrl = url + '/index.php?r=fights/rival'
	toLightUrl = url + '/?r=site/layout&layout=light'
	toHitUrl = url + '/index.php?r=fights/hit&type='
	startFightUrl =url + '/index.php?r=fights/choose&club=official'
	isCanToBuyEnergy = False
	needEnemyType = 'all'


	nextFightButtonsLables = ['Следующий!', 'В бой', 'Ещё бой!']

	enemyTypes = {
		'strength':'Силач-Дэбил',
		'critical':'Критач-таутуированный',
		'dexterity':'Ловкач-Брюс-Ли',
		'defence':'Защитник-Сумоист',
		'woman':'Женщина'
	}
	hitTypesLables = {
		'strength':'силу',
		'critical':'крит',
		'dexterity':'ловкость',
	}

	hitTypes = ['strength','dexterity', 'critical']

	def buyEnergy():
		# urlToBuyEnergy = url + '/index.php?r=crop/energyRepair'
		# user.get(urlToBuyEnergy)
		# print('Закупились энергией')
		# waitHalfSecond()
		print('Нет энергии для боев, ждем 30 сек и продолжим')
		time.sleep(30)


	def replenishEnergy(soup):
		energySpan = soup.find('span', attrs={'id': 'z-energy'})
		if energySpan:
			energyCount = int(energySpan.get_text().strip().split('/')[0])
			if energyCount < 7 and isCanToBuyEnergy:
				buyEnergy()
		else:
			refreshIfDummy(soup)

				


	def getFightStatus(soup):
		enemyName = soup.find('div', attrs={'class': 'fight-head-name'})
		if enemyName:
			print('Противник: ', enemyName.get_text().strip())
		else:
			return 'ended'

		nextFightButton = soup.find('a', attrs={'class': 'bttn_green long mt5'})
		changeEnemyButton = soup.find('a', attrs={'class': 'bttn_sea'})
		if nextFightButton:
			nextFightButtonText = nextFightButton.get_text().strip()
			isEnd = nextFightButtonText in nextFightButtonsLables
			if isEnd:
				print('Битва закончилась.')
				return 'ended'
			
		elif changeEnemyButton:
			isEnd = changeEnemyButton.get_text().strip() == 'Сменить противника'
			if isEnd:
				print('Битва закончилась на охране.')
				return 'needToChange'
			else:
				return 'now'
		else:
			return 'now'

	def parseStats(soup):
		fightStatsMe = soup.find('div', attrs={'class': 'fight-stats _me'}).findAll('div', attrs={'class': 'fight-stat'})
		fightStatsEnemy = soup.find('div', attrs={'class': 'fight-stats _enemy'}).findAll('div', attrs={'class': 'fight-stat'})
		strength_my = int(fightStatsMe[0].get_text().strip())+5
		dexterity_my = int(fightStatsMe[1].get_text().strip())+5
		critical_my = int(fightStatsMe[2].get_text().strip())

		strength_enemy = int(fightStatsEnemy[0].get_text().strip())
		dexterity_enemy = int(fightStatsEnemy[1].get_text().strip())
		critical_enemy = int(fightStatsEnemy[2].get_text().strip())
		print('  ',strength_my,dexterity_my,critical_my,'  ')
		print('  ',strength_enemy,dexterity_enemy,critical_enemy,'  ')
		stats = {
			'strength_my':strength_my,
			'dexterity_my':dexterity_my,
			'critical_my':critical_my,
			'strength_enemy':strength_enemy,
			'dexterity_enemy':dexterity_enemy,
			'critical_enemy':critical_enemy
		}

		return stats


	def determineHowToHit(stats):
		if stats['strength_my'] > stats['strength_enemy']:
			swin = 1
		else:
			swin = 0
		if stats['dexterity_my'] > stats['dexterity_enemy']:
			lwin = 3
		else:
			lwin = 0
		if stats['critical_my'] > stats['critical_enemy']:
			kwin = 5
		else:
			kwin = 0
		wcount = swin + lwin + kwin
		# Высчитываем фактор победы
		if wcount <= 3:
			print('lose because wcount ==', wcount)
			return 'lose'
			#Это поражение
		elif wcount == 5:
			return 'lose'
			#Это поражение
		elif wcount == 4:
			#Ты сильнее его и ловчее
			return 'strength-dexterity'
		elif wcount == 6:
			#Ты сильнее и критичнее
			return 'strength-critical'
		elif wcount == 8:
			#Ты ловчее и критичнее
			return 'dexterity-critical'
		elif wcount == 9:
			return 'ALL'


	def refreshIfDummy(soup):
		isDummyPage = isDummy(soup)
		if isDummyPage:
			#time.sleep(2)
			checkRival(0)
		else:
			print('ВНИМАНИЕ, ЧТО ТО НЕ СРАБОТАЛО И ЭТО НЕ ИЗ-ЗА ЗАГЛУШКИ')

	def changeEnemy(soup):
		changeEnemyButton = soup.find('a', attrs={'class': 'bttn_sea'})
		if changeEnemyButton:
			changeUrl = url + changeEnemyButton['href']
			nextStep = getSoup(changeUrl)
			checkRival(nextStep)
		else:
			refreshIfDummy(soup)

	def newEnemy(soup):
		global currentFightsCount
		currentFightsCount = currentFightsCount + 1 
		newEnemyButton = soup.find('a', attrs={'class': 'bttn_green long mt5'})
		if newEnemyButton:
			changeUrl = url + newEnemyButton['href']
			nextStep = getSoup(changeUrl)
			checkRival(nextStep)
		else:
			refreshIfDummy(soup)

	def getTokenToHit(soup):
		hitButton = soup.find('a', attrs={'class': 'square-btn-green'})
		if hitButton:
			token = hitButton['href'].split('&token=')[1]
			return token
		else:
			refreshIfDummy(soup)


	def determineDisabledButton(soup):
		disabledButton = soup.find('span', attrs={'class': 'square-btn-gray'})
		if disabledButton:
			return disabledButton.find('img')['src'].split('hit/')[1].split('.')[0]
		else:
			return None

	def hitByType(hitType, token):
		hitUrl = toHitUrl + hitType + '&token='+token
		soup = getSoup(hitUrl)
		print('Ударил использовав: ', hitTypesLables[hitType])
		checkRival(soup)


	def hit(winFactor, token, disabledButton):
		if winFactor == 'ALL':
			for hitType in hitTypes:
				if hitType != disabledButton:
					hitByType(hitType,token)
					break
		else:
			currentHitTypes = winFactor.split('-')
			for hitType in hitTypes:
				if hitType != disabledButton:
					hitByType(hitType,token)
					break



			
			
		

	def continueTheFight(soup):
		stats = parseStats(soup)
		winFactor = determineHowToHit(stats)
		if winFactor == 'lose':
			print('Сменим противника, потому что он сильнее')
			changeEnemy(soup)
		else:
			disabledButton = determineDisabledButton(soup)
			token = getTokenToHit(soup)
			if token:
				hit(winFactor, token, disabledButton)

	def checkRival(soup):
		global currentFightsCount
		printWithLevel('Проведено боев: {0}/{1}'.format(currentFightsCount,needFightsCount))
		if currentFightsCount >= needFightsCount:
			return 'enough'
		if soup == 0:
			rivalSoup = getSoup(rivalUrl)
		else:
			rivalSoup = soup

		fightStatus = getFightStatus(rivalSoup)
		enemyType = getEnemyType(rivalSoup)
		replenishEnergy(rivalSoup)
		isNeedType = (enemyType == needEnemyType) or (needEnemyType == 'all')
		if fightStatus == 'now' and isNeedType:
			continueTheFight(rivalSoup)
		elif enemyType == 'noEnemy':
			currentFightsCount = currentFightsCount + 1 
			soup = getSoup(startFightUrl)
			checkRival(soup)
		elif fightStatus == 'ended':
			waitHalfSecond()
			newEnemy(rivalSoup)	
		else:
			waitHalfSecond()
			changeEnemy(rivalSoup)
			
		
	def getEnemyType(soup):
		fightBack = soup.find('div', attrs={'class': 'fight-back'})
		if fightBack:
			enemyType = fightBack['style'].split('bgs/')[1].split('/')[0]
			print('Это {0}.'.format(enemyTypes[enemyType]))
			return enemyType
		else:
			return 'noEnemy'

	def isDummy(soup):
		refresh = soup.find('a', attrs={'class': 'btn-a t-c mt5'})
		if refresh:
			isDummyPage = refresh.get_text().strip() == 'Обновить'
			if isDummyPage:
				print('Харе так бешанно :)')
			return isDummyPage
		else:
			return False
	while True:
		result = checkRival(0)
		if result == 'enough':
			printWithLevel('Закончили бои, их было: '+str(currentFightsCount))
			currentFightsCount = 0
			break



def waitNextLevel(needLevel):
	while True:
		checkLevel()
		if myLevel >= needLevel:
			print('Апнули левел на: ', myLevel)
			return True
		else:
			harvestAllEachOne()
			getAwards(2)
			#time.sleep(30)
			pass


def add_params(need_equipments):

	for equipment_id in need_equipments:
		user.get(url + '/?r=fights/equipments&equipment_id='+equipment_id)
		waitHalfSecond()
	pass


def getAndReturnСhain(itemName):
	user.get(url + '/index.php?r=property/add&id='+itemName)
	waitHalfSecond()
	chainPage = user.get(url + '/index.php?r=property/list&top=clothes&cat=chain')
	waitHalfSecond()
	try:
		soup = bs(chainPage.content, 'html.parser')
		chain_cancel_url = soup.find('a', attrs = {'class':'bttn_red'})['href']
		chain_cancel = user.get(url+chain_cancel_url)
		chain_cancel = user.get(url+chain_cancel_url)
	except:
		print('NO!')
	print('купили и вернули')

def get_card():
	try:
		pvp = user.get(url + '/index.php?r=cards/cards')
		soup = bs(pvp.content, "lxml")
		inf_one = soup.find_all('a', attrs={'class': 'card'})
		inf_two = inf_one[0]
		global url_take_card
		url_take_card = inf_two['href']
		return True
	except:
		print('Карзино заперто.')
		return False



def take_card():
	print('Берем карту')
	card = get_card()
	if card:
		cc = str(url+url_take_card)
		print(cc)
		takecard = user.get(cc)
		print('Взяли карту')
	else:
		print('Нет карты')

def takefuckingoffice():
	harvestAllEachOne()
	#time.sleep(5)
	user.get(url + '/?r=estate')
	printWithLevel('Жду 2 секунды в офисе')
	#time.sleep(2)
	user.get(url + '/index.php?r=estate/shoplist&slot=0')
	printWithLevel('Жду 2 секунды в офисе')
	#time.sleep(2)
	user.get(url + '/index.php?r=estate/shopview&slot=0&type=office')
	printWithLevel('Жду 2 секунды в офисе')
	#time.sleep(1)
	user.get(url + '/index.php?r=estate/estatebuy&slot=0&type=office')
	printWithLevel('Жду 2 секунды в офисе')
	#time.sleep(2)
	user.get(url + '/index.php?r=estate/estatebuy&slot=3&type=office')
	printWithLevel('Жду 2 секунды в офисе')
	#time.sleep(2)
	harvestAllEachOne()
	pass


def mission2():
	checkLevel()
	printStartMission(2)
	getDotsId()
	dots = myDots[2:]
	for id_c in dots:
		printWithLevel('Ставим беляшную Гаф-Гаф')
		addDot('bone_setter',id_c)
		waitHalfSecond()
	printWithLevel('Нужно подождать 30 сек до созревания точек')
	time.sleep(30)
	harvestAllEachOne()
	getAwards(2)
	waitHalfSecond()
	getAwards(2)
	setFunnyDescription()

def mission3():
	checkLevel()
	printStartMission(3)
	printWithLevel('Нужно сделать 4 боя, сбор точек, поставить гаф гаф')
	fights(4)
	printWithLevel('Заберем награду за 4 боя.')
	getAwards(2)
	waitHalfSecond()
	getAwards(2)
	printWithLevel('Ставим гафгаф')
	getDotsId()
	removeDot(myDots[4])
	printWithLevel('Ставим snack_bar')
	addDot('snack_bar',myDots[4])
	#time.sleep(1)
	printWithLevel('забираем награду')
	getAwards(2)
	waitNextLevel(4)


def mission4():
	waitHalfSecond()
	checkLevel()
	printStartMission(4)
	upgrade_stats()
	user.get(url + '/index.php?r=fights/equipments&equipment_id=bita')
	waitHalfSecond()
	printWithLevel('Бежим за цепурой')
	getAndReturnСhain('first_chain')
	waitNextLevel(5)

def mission5():
	checkLevel()
	printStartMission(5)
	printWithLevel('5 боев, 5 точек и 3 грабежа!')
	printWithLevel('надо попробовать грабануть')
	robs(3)
	printWithLevel('Ожидание 30 секунд')
	time.sleep(30)
	fights(5)
	printWithLevel('Ожидание 20 секунд')
	time.sleep(20)
	printWithLevel('дальше только точки')
	waitNextLevel(6)

def mission6():
	waitHalfSecond()
	checkLevel()
	printStartMission(6)
	printWithLevel('тут нам надо набить авторитету, сходить в гоп-стоп и поставить столовку хавчик')
	printWithLevel('начнем с хавчика')
	getDotsId()
	dots = myDots[2:]
	idc = 0
	for id_c in dots:
		idc = idc + 1;
		if idc == 3:
			printWithLevel('Сюда ставим!')
			removeDot(id_c)
			addDot('dining',id_c)
		else:
			pass
	printWithLevel('что-ж пора улучшить параметры!')
	print('теперь ты непобедим! (среди бомжей)')
	getAwards(2)
	printWithLevel('пока пособираем точки где то 200 сек')
	for i in range(8):
		harvestAllEachOne()
		print('ждем 35 сек')
		time.sleep(31)
	printWithLevel('и 12 боев надо, шоб наверняка')
	fights(12)
	printWithLevel('пошли забирать награду!')
	getAwards(4)
	#time.sleep(1)
	getAwards(4)
	user.get(url + '/index.php?r=property/add&id=first_rosary')
	#time.sleep(2)
	waitNextLevel(7)

def mission7():
	waitHalfSecond()
	checkLevel()
	printStartMission(7)
	upgrade_stats()
	upgrade_stats()
	printWithLevel('Не больше 5 грабежей')
	robs(5)
	for x in range(12):
		printWithLevel('Точки соберу')
		harvestAllEachOne()
		#time.sleep(10)

	printWithLevel('казино, 1 место под точку, 2 подполки, олимпийка, барыга, 5 точек, 7 боев, и все!')
	printWithLevel('сразу начнем с покупки точки!')
	user.get(url + '/index.php?r=crop/addslot&type=slow')
	waitHalfSecond()
	user.get(url + '/?r=pusher')
	getAwards(1)
	print('+1 доц за барыгу')
	take_card()
	printWithLevel('забрали финку, надо его надеть.')
	user.get(url + '/index.php?r=property/list&top=clothes&cat=weapon')
	waitHalfSecond()
	printWithLevel('5 раз сходим за вещями')
	for i in range(5):
		user.get(url + '/index.php?r=property/add&id=sharpening')
		printWithLevel('купим олимпийку')
		waitHalfSecond()
		user.get(url + '/index.php?r=property/add&id=sweatshirts')
		printWithLevel('забираем награду')
	getAwards(2)
	waitHalfSecond()
	harvestAllEachOne() #сбор точек всех
	getAwards(1)
	#time.sleep(5)
	getDotsId()
	dots = myDots[2:]
	for id_c in dots:
		removeDot(id_c)
		printWithLevel('Ставим карточный клуб')
		addDot('card_club',id_c)
	waitHalfSecond()
	printWithLevel('подполки поставил!')
	printWithLevel('бои даже стараться не буду делать, лучше левел апнуть')
	getAwards(2)
	#time.sleep(1)
	getAwards(2)
	waitNextLevel(8)


def mission8():
	waitHalfSecond()
	checkLevel()
	printStartMission(8)
	user.get(url + '/index.php?r=fights/params&param_id=strength')
	waitHalfSecond()
	user.get(url + '/index.php?r=fights/params&param_id=critical')
	waitHalfSecond()
	upgrade_stats()
	upgrade_stats()
	printWithLevel('тут офис, 6 точек, 5 боев и 8 грабежей')
	for i in range(5):
		takefuckingoffice()
	print('Офис на месте!')
	getAwards(1)
	printWithLevel('8 грабежей не просто сделать, так что тупо буду собирать точки')
	#time.sleep(30)
	harvestAllEachOne()
	getAwards(1)
	waitNextLevel(9)



def mission9():
	waitHalfSecond()
	checkLevel()
	printStartMission(9)
	upgrade_stats()
	printWithLevel('тут у нас: 2 летника, 1 ускорение, сбор с 8 точек и 8 грабежей')
	harvestAllEachOne() #сбор точек всех
	getAwards(1)
	print('два летника ставим!')
	getDotsId()
	dots = myDots[2:4]
	for id_c in dots:
		removeDot(id_c)
		print('Ставим летники')
		addDot('outdoor_cafe',id_c)
	printWithLevel('летники поставил!')
	#time.sleep(5)
	getAwards(1)
	printWithLevel('надо че нить ускорить!')
	getDotsId()
	dots = myDots[2:]
	idc = 0
	for id_c in dots:
		idc = idc + 1;
		if idc == 3:
			printWithLevel('эту ускорим!')
			boostDot(id_c)
			#time.sleep(0.3)
		else:
			pass
	#time.sleep(2)
	harvestAllEachOne()
	getAwards(2)
	printWithLevel('уже должны апнуть 10ку!')
	waitNextLevel(10)


def writeToGoodFile(nick):
	with open('combinat_result.txt', 'a', encoding="utf8") as mf:
		mf.write(str(nick)+'\n')
	pass

def misses():
	mission2()
	mission3()
	mission4()
	mission5()
	mission6()
	mission7()
	mission8()
	mission9()
	gotoband()
	writeToGoodFile(newMult)


def main():
	global user
	print('Привет, я создаю быстрых мультов из списка')

	for nick in listOfMuls:
		newAccount(nick)
		misses()
		print('Закончили с ', nick)
		try:
			user = requests.Session()
			user.close()
		except:
			pass


def test():
	login('hg6jytras781','22rafaelka23')
	robs(3)

if __name__ == '__main__':
	main()