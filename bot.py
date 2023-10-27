from random import randint

class Bot:
	def __init__(self, country:str, colour:tuple, power:int):
		self.name = country
		self.colour = colour
		self.power = power
		self.enemies = set()
		self.allies = set()
		self.non_aggression_pacts = set()
		self.right_of_passage = set()
		self.relationships = set()	
		self.borders = set() # variable for save set of pixels in borders
		self.attacked_pixels_to_check = list()
		self.pixels_on_borders_to_delete = list()
		self.update_borders_counter = 0

	def turn(self, mainobj, amount_units:int):
		self.borders = self.search_borders_from_zero(mainobj)
		#print(f"[ S ] {self.name}, {amount_units}")
		return self.attack2(mainobj, amount_units)
	
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
		#print(f'[ S ] Updating borders for \033[33m{self.name}\033[0m')
		end_list = set()
		for x in enumerate(mainobj.map):
			for y in enumerate(x[1]):
				try:
					if mainobj.country_by_colour.get(mainobj.map[x[0]][y[0]], "") == self.name:
						for x_adder in range(-1, 2):
							for y_adder in range(-1, 2):
								if mainobj.country_by_colour.get(mainobj.map[x[0] + x_adder][y[0] + y_adder], "") in self.enemies:
									end_list.add((x[0], y[0]))
					else: continue
				except IndexError: continue
		return end_list
	def attack2(self, mainobj, amount_units:int): # STOP! This code is very hard for understand. Do you really want to continue?
		result = list()
	#![MAIN CYCLE]
		for i_index, i_value in enumerate(self.borders): #i_value is tuple - (x, y)
			if amount_units:
				for x_adder in range(-1, 2):
					#seriosly?
					for y_adder in range(-1, 2):
						#I warned you!
						try:
							if mainobj.country_by_colour.get(mainobj.map[i_value[0] + x_adder][i_value[1] + y_adder]) in self.enemies:
								if amount_units: # ... is not zero
									result.append((i_value[0] + x_adder, i_value[1] + y_adder))
									self.attacked_pixels_to_check.append((i_value[0] + x_adder, i_value[1] + y_adder) )
									self.pixels_on_borders_to_delete.append((i_index, i_value))
									amount_units -= 1
						except IndexError:
							pass
			else:
				break
		print(self.name, len(result), amount_units)
		if amount_units and result:
			self.borders = self.search_borders_from_zero(mainobj)
			result += self.attack2(mainobj, amount_units)
		return result
	def refresh_borders(self, mainobj):
#![CHECK PIXEL_ON_CHECKING]
		for pixel_on_checking in self.attacked_pixels_to_check:
			if mainobj.country_by_colour.get(mainobj.map[pixel_on_checking[0]][pixel_on_checking[1]] != self.name):
				break
			for x_adder_of_checked_pixel in range(-1, 2):
				for y_adder_of_checked_pixel in range(-1, 2):
					pixel_on_checking_of_checked_pixel = mainobj.country_by_colour.get(mainobj.map[pixel_on_checking[0] + x_adder_of_checked_pixel][pixel_on_checking[1] + y_adder_of_checked_pixel]) # name of country as str
					if pixel_on_checking_of_checked_pixel != self.name:
						self.borders.add(pixel_on_checking)
#![CHECK I_VALUE]
		for i_index, i_value in self.pixels_on_borders_to_delete:
			switcher = True # if False then we don't touch to i_value, else delete from self.borders
			if mainobj.country_by_colour.get(mainobj.map[i_value[0]][i_value[1]]) != self.name:
				self.borders.discard(i_value)
				break
			for x_adder in range(-1, 2):
				for y_adder in range(-1, 2):
					if mainobj.country_by_colour.get(mainobj.map[i_value[0] + x_adder][i_value[1] + y_adder]) != self.name:
						switcher = False
			if switcher:
				self.borders.discard(i_value)


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
		
