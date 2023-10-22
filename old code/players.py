from random import randint
from json import loads

class Bot():
	def __init__(this, game, country):
		this.playerId = this.getId()
		this.gameId = game
		this.country = country
	def getId(this):
			characters = "0123456789abcdefghijklmnop-qrstuvwxyz"
			result = ""
			for i in range(0, 50):
				result += characters[randint(0, 35)]
			return result
	def turn(this, map, diplomaty, power):
		actions = []
		assumes = []
		powerGenerator = randint(0, 5)
		for iterations in range(0, powerGenerator): # это перебор учитывающий количество силы
			for indexX, x in enumerate(map): # перебор по иксу
				for indexY, y in enumerate(x): # по игрику
					if map[indexX][indexY][0] == this.country: # если клетка равна стране за которую играет бот
						# далле перебор условиями всех соседних клеток для поиска врага, включая соседей по диагонали
						if map[ indexX + 1][ indexY ][0] in diplomaty['enemies']:
							assumes.append((indexX + 1, indexY))
						elif map[ indexX - 1 ][ indexY ][0] in diplomaty['enemies']:
							assumes.append((indexX - 1, indexY))
						elif map[ indexX ][ indexY + 1 ][0] in diplomaty['enemies']:
							assumes.append((indexX, indexY + 1 ))
						elif map[ indexX ][ indexY - 1 ][0] in diplomaty['enemies']:
							assumes.append((indexX, indexY - 1 ))
						elif map[ indexX + 1 ][ indexY + 1 ][0] in diplomaty['enemies']:
							assumes.append((indexX + 1, indexY + 1 ))
						elif map[ indexX + 1 ][ indexY - 1 ][0] in diplomaty['enemies']:
							assumes.append((indexX + 1, indexY - 1 ))
						elif map[ indexX - 1 ][ indexY + 1 ][0] in diplomaty['enemies']:
							assumes.append((indexX - 1, indexY + 1 ))
						elif map[ indexX - 1 ][ indexY - 1 ][0] in diplomaty['enemies']:
							assumes.append((indexX - 1, indexY - 1 ))
			for action in assumes:
				map[action[0]][action[1]][0] = this.country
				assumes.pop(0)
		return map
	def getJSON(this, path='diplomaty.json'):
		with open(path, 'r') as file:
			this.dipJSON = file.read()
			this.dip = loads(this.dipJSON)
		return this.dip
	#{
	# "action": declare war,
	# "sender": germany,
	# "recipient": poland,
	# "result": True # war declared
	# }
	# sender = country
	# recipient = country
	# actions = declare war, propose allie, relation
	# result (for relation int)
	def relation(this, actions):
		for action in actions:
			if action["action"] == "declare war": # Если кто-то кому-то объявил войну, то его репутация немного понижается
				randomNumber = randint(-1, 0)
				this.dip[action["sender"]]["relationships"][this.country] += randomNumber
				this.dip[this.country]["relationships"][action["sender"]] += randomNumber
			elif action["action"] == "relation":
				if action["recipient"] in this.dip[this.country]["allies"]: # Если оскорбляют нашего союзника, то мы тоже слегка оскорбляем отправителя (если союзник кого-то оскарбляет, то нам пофиг)
					if action["result"] < 0:
						randomNumber = randint(-3, 0)
						this.dip[action["sender"]]["relationships"][this.country] += randomNumber
						this.dip[this.country]["relationships"][action["sender"]] += randomNumber
					elif action["result"] > 0:
						randomNumber = randint(0, 3) # здесь аналогично для "подружения"
						this.dip[action["sender"]]["relationships"][this.country] += randomNumber
						this.dip[this.country]["relationships"][action["sender"]] += randomNumber
				elif action["recipient"] in this.dip[this.country]["enemies"]: # А здесь для врагов
					if action["result"] < 0:
						randomNumber = randint(0, 3)
						this.dip[action["sender"]]["relationships"][this.country] += randomNumber
						this.dip[this.country]["relationships"][action["sender"]] += randomNumber
					elif action["result"] > 0:
						randomNumber = randint(-3, 0) # если кто-то подражился с нашим врагом
						this.dip[action["sender"]]["relationships"][this.country] += randomNumber
						this.dip[this.country]["relationships"][action["sender"]] += randomNumber
				elif randint(0, 9) > 7: # немного нестабильности
					if randint(0, 1):
						randomNumber = randint(0, 9)
						this.dip[action["sender"]]["relationships"][this.country] += randomNumber
						this.dip[this.country]["relationships"][action["sender"]] += randomNumber
					else:
						randomNumber = randint(-9, 0)
						this.dip[action["sender"]]["relationships"][this.country] += randomNumber
						this.dip[this.country]["relationships"][action["sender"]] += randomNumber
			return {"action": "relation", "sender": this.country, "recipient": action["sender"], "result": randomNaumber}
		

	def declareWar(this, recipient):
		this.dip = this.getJSON()
		counter = 0
		if this.dip[recipient]["enemies"] != []:
			for country in this.dip[recipient]["enemies"]: # Если во врагах принимающего нет союзников отправителя
				if country in this.dip[this.country]["allies"]:
					counter += 1
		if this.dip[recipient]["allies"] != []:
			for country in this.dip[recipient]["allies"]: # Если в союзниках принимающего нет врагов отправителя
				if country in this.dip[this.country]["enemies"]:
					counter += 1
		if this.dip[recipient]["relationships"][this.country] > -30: # Если отношения больше 30 и отправителю повезло
			if randint(0, 9) > 5:
				counter += 1
		if counter > 1.56: # То союз был заключён
			this.dip[this.country]["relationships"][recipient] = -100
			this.dip[recipient]["relationships"][this.country] = -100
			this.dip[this.country]["enemies"].append(recipient)
			this.dip[recipient]["enemies"].append(this.country)
			return True
		else:
			return False
	def proposeAllie(this, recipient):
		counter = 0
		if this.dip[recipient]["enemies"] != []:
			for country in this.dip[recipient]["enemies"]: # Если во врагах принимающего нет союзников отправителя
				if not(country in this.dip[this.country]["allies"]):
					counter += 1
		else:
			counter += 1
			print("first")
		if this.dip[recipient]["allies"] != []:
			for country in this.dip[recipient]["allies"]: # Если в союзниках принимающего нет врагов отправителя
				if not(country in this.dip[this.country]["enemies"]) or (this.dip[this.country]["enemies"] == []):
					counter += 1
		else:
			counter += 1
			print("second")
		for enemie in this.dip[recipient]["enemies"]: # Если у них есть общие враги
			if enemie in this.dip[this.country]["enemies"]:
				counter += 1
		if this.dip[recipient]["relationships"][this.country] > 30: # Если отношения больше 30 и отправителю повезло
			if randint(0, 9) > 5.49:
				counter += 1
		if counter == 3: # То союз был заключён
			randomAdd = randint(0, 19)
			this.dip[this.country]["relationships"][recipient] += randomAdd
			this.dip[recipient]["relationships"][this.country] += randomAdd
			this.dip[this.country]["allies"].append(recipient)
			this.dip[recipient]["allies"].append(this.country)
			return True
		else:
			return False

