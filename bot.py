from random import randint
from random import shuffle
from random import random

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

		self.diplomaty_cancel = 0.0 # for limit diplomaty requests
		self.diplomaty_cancel_step = 0.0 # speed of turn of limit

		self.fronts = list() # variable for save set of pixels in borders
		self.attacked_pixels_to_check = list()
		self.pixels_on_borders_to_delete = list()
		self.update_borders_counter = 0
		self.stayed_units = int()

	def turn(self, mainobj, amount_units:int):
		self.fronts = self.search_borders_from_zero(mainobj)
		#print(f"[ S ] {self.name}, {amount_units}")
		return self.attack2(mainobj, amount_units)
	
	def borders_view(self, mainobj, amount_units:int):
		self.fronts = self.search_borders_from_zero(mainobj)
		self.stayed_units = 0
		return list(self.fronts)



	# functions 'propose', 'relate' and 'attack' only return results, then 'Main' will set those to properties and files
	
	def relate(self, reciever):
		if reciever in self.enemies:
			return 0
		else:
			if random() < 0.1:
				return randint(1, 10)

	def propose(self, receiver, action:str):
		# here you can see randomizing shit
		if random() > 0.5:
			return False # по приколу (ru)
		alliance_probability = 0.0
		non_agression_pact_probability = 0.0
		right_of_passage_probability = 0.0
		declare_war_probability = 0.0
#![ALLIANCE]
		if action == 'alliance':
			if self.relationships[receiver.name] > randint(40, 100):
				alliance_probability += 0.06
			if len(list(set(self.enemies) & set(receiver.enemies))) >= len(self.enemies) // 2:#if we have more then half similar enemies/allies...
				alliance_probability += 0.095
			if len(list(set(self.allies) & set(receiver.allies))) >= len(self.allies) // 2:# ^^higher^^
				alliance_probability += 0.090
			if not(receiver.name in self.allies) and not(receiver.name in self.enemies) and random() < alliance_probability:
				return True
			else:
				return False
#![NON-AGGRESION PACT]
		elif action == 'non-aggression pact':
			if self.relationships[reciever.name] > randint(-90, -40):
				non_agression_pact_probability += 0.032
			if self.enemies: # ... is not empty
				non_agression_pact_probability += 0.25
			if reciever.name in self.allies:
				non_agression_pact_probability += 0.33
			if not(receiver.name in self.non_aggression_pacts) and not(receiver.name in self.enemies) and random() < non_agression_pact_probability:
				return True
			else:
				return False
#![RIGHT OF PASSAGE]
		elif action == 'right of passage':
			if self.relationships[reciever.name] > randint(0, 20):
				right_of_passage_probability += 0.3
			if reciever.name in self.allies:
				right_of_passage_probability += 0.2
			if list(set(self.enemies) & set(self.enemies)):
				right_of_passage_probability += 0.15
			if not(receiver.name in self.right_of_passage) and not(receiver.name in self.enemies) and random() < right_of_passage_probability:
				return True
			else:
				return False
#![DECLARE WAR]
		elif action == "declare war":
			if list(set(reciever.enemies) & set(self.allies)):
				declare_war_probability += 0.45
			if self.relationships[reciever.name] < randint(-100, -60):
				declare_war_probability += 0.2
			if not(reciever.name in self.allies) and not(reciever.name in self.enemies) and random() < declare_war_probability:
				return True
			else:
				return False
		else:
			return False
	def search_borders_from_zero(self, mainobj): # This function need to get coordinates about all pixels next to the other countries as set and then updating data everyone turn
		end_list = list()
		for x in enumerate(mainobj.map):
			for y in enumerate(x[1]):
				try:
					if mainobj.country_by_colour.get(mainobj.map[x[0]][y[0]], "") == self.name:
						for x_adder in range(-1, 2):
							for y_adder in range(-1, 2):
								if mainobj.country_by_colour.get(mainobj.map[x[0] + x_adder][y[0] + y_adder], "") in self.enemies and not((x[0], y[0]) in end_list):
									end_list.append((x[0], y[0]))
									assert True
					else: continue
				except (IndexError, AssertionError): continue
		shuffle(end_list) #mixing for randomization
		return end_list
	def attack2(self, mainobj, amount_units:int):
		result = list()
		similar_elements = list(set(self.empire) & set(self.fronts))
		self.fronts = similar_elements + list(set(self.fronts) - set(similar_elements))
		for i_value in self.fronts:
			if amount_units:
				for x_adder in range(-1, 2):
					for y_adder in range(-1, 2):
						try:
							if mainobj.country_by_colour.get(mainobj.map[i_value[0] + x_adder][i_value[1] + y_adder]) in self.enemies:
								if amount_units: # ... is not zero
									result.append((i_value[0] + x_adder, i_value[1] + y_adder))
									amount_units -= 1
						except IndexError:
							pass
			else:
				break
		self.stayed_units = amount_units
		return result
