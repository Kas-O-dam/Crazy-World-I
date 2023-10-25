from random import randint

class Bot:
	def __init__(self, country:str, colour:tuple):
		self.name = country
		self.colour = colour
		self.enemies = set()
		self.allies = set()
		self.non_aggression_pacts = set()
		self.right_of_passage = set()
		self.relationships = set()	
		self.borders = set() # variable for save set of pixels in borders

	def turn(self, mainobj, amount_units:int):
		return self.attack(mainobj, amount_units)
	
	# functions 'propose', 'relate' and 'attack' only return results, then 'Main' will set those to properties and files
	
	def relate(self, reciever):
		if reciever in self.enemies:
			return False
		else:
			return randint(0, 10)

	def propose(self, receiver, action):
		match action:
			# Yes, it's not interesting, __now__, without rand lib, without dependencies from other factors... 
			case 'union':
				if not (receiver in self.allies):
					return True
			case 'non-aggression pact':
				if not (receiver in self.non_aggression_pacts):
					return True
			case 'right of passage':
				if not (receiver in self.right_of_passage):
					return True
			case _ :
				return False
	def search_borders_from_zero(self, mainobj): # This function need to get coordinates about all pixels next to the other countries as set and then updating data everyone turn
		end_list = set()
		for x in enumerate(mainobj.map):
			for y in enumerate(x[1]):
				try:
					if mainobj.country_by_colour.get(mainobj.map[x[0]][y[0]], "") == self.name:
						for x_adder in range(-1, 2):
							for y_adder in range(-1, 2):
								if mainobj.country_by_colour.get(mainobj.map[x[0] + x_adder][y[0] + y_adder], "") != self.name:
									end_list.add((x[0] + x_adder, y[0] + y_adder))
					else: continue
				except IndexError: continue
		return end_list
	def attack2(self, mainobj, amount_units:int):
		for i in self.borders: #i is tuple - (x, y)
			if main
	def attack(self, mainobj, amount_units:int):
		result = list()
		print(self.name, amount_units)
		def search(amount_units:int):
			# we have the four ways
			#      north
			#        ^
			#        |
			#west <-- --> east
			#        |
			#       \_/
			#     south
			# and search, for example, from west-north to east-south
			# is samply, what very bad. The front will be like that:
			#z0000000000000000000000000000000
			#zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz00000
			#zzzzzz             00000000000000000
			# one unrealistic line, because we need randomizing way everyone turn
			
			# [WAY-RANDOMIZE]
			end_horizontal = [mainobj.width, 0][randint(0, 1)]
			end_vertical = [mainobj.height, 0][randint(0, 1)]
			start_horizontal = int()
			start_vertical = int()
			step_vertical = int()
			step_horizontal = int()
			match end_horizontal:
				case 0:
					step_horizontal = -1
					start_horizontal = mainobj.width
				case mainobj.width:
					step_horizontal = +1
					start_horizontal = 0
			match end_vertical:
				case 0:
					step_vertical = -1
					start_vertical = mainobj.height
				case mainobj.height:
					step_vertical = +1
					start_vertical = 0
			# /[WAY-RANDOMIZE] => { 
			# 	start_vertical || end_vertical = mainobj.height || 0
			# 	&&
			# 	start_horizontal || end_horizontal = mainobj.width || 0
			#	&&
			#	step_(vertical || horizontal) = 1 || -1
			# }
			
			# yeees, four-level cycle!

			# [RUN-ON-CANVA]
			way = randint(0, 2)
			if way:
				for x in range(start_horizontal, end_horizontal, step_horizontal):
					for y in range(start_vertical, end_vertical, step_vertical):
						try:
							if mainobj.country_by_colour.get(mainobj.map[x][y], "") == self.name: # here returning :(
								#print(x, y, mainobj.country_by_colour[mainobj.map[x][y]], end=" ")
								for x_adder in range(-1, 2): # here we shall check everyone tile next to the checking tile
									if randint(0, 3): continue
									for y_adder in range(-1, 2):
										if randint(0, 3): continue
										if mainobj.country_by_colour.get(mainobj.map[x + x_adder][y + y_adder], "") in self.enemies:
											#print(f"writed: {x + x_adder}:{y + y_adder}")
											amount_units -= 1
											return (x + x_adder, y + y_adder), amount_units
							else: continue
						except IndexError: continue
			else:
				for y in range(start_horizontal, end_horizontal, step_horizontal):
					for x in range(start_vertical, end_vertical, step_vertical):
						try:
							if mainobj.country_by_colour.get(mainobj.map[x][y], "") == self.name: # here returning :(
								#print(x, y, mainobj.country_by_colour[mainobj.map[x][y]], end=" ")
								for x_adder in range(-1, 2): # here we shall check everyone tile next to the checking tile
									if randint(0, 3): continue
									for y_adder in range(-1, 2):
										if randint(0, 3): continue
										if mainobj.country_by_colour.get(mainobj.map[x + x_adder][y + y_adder], "") in self.enemies:
											#print(f"writed: {x + x_adder}:{y + y_adder}")
											amount_units -= 1
											return (x + x_adder, y + y_adder), amount_units
							else: continue
						except IndexError: continue
			# /[RUN-ON-CANVA] => tuple(x, y) & amount_units
			return False, 0
		while amount_units:
			some, amount_units = search(amount_units)
			if some:
				result.append(some)
		
		return result
		
