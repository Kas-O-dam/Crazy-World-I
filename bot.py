from random import randint
from random import shuffle
from random import choice
from random import random
from icecream import ic

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

		self.fronts = list() # variable for save set of pixels in borders
		self.attacked_pixels_to_check = list()
		self.pixels_on_borders_to_delete = list()
		self.update_borders_counter = int()
		self.stayed_units = int()

	def __repr__(self):
		return f'Bot player:\ncountry={self.name},\ncolour={self.colour},\nenemies={self.enemies},\nallies={self.allies}'

	def turn(self, mainobj, amount_units:int):
		self.fronts = self.search_borders_from_zero(mainobj)
		result = dict()
		result["attack"] = self.attack2(mainobj, amount_units)
		result["propose"] = self.propose(choice(tuple(mainobj.countryset)), choice(("allie", "non-aggression pact", "right of passage", "declare war")))
		result["relate"] = self.relate(choice(tuple(mainobj.countryset)))
		return result
	
	def borders_view(self, mainobj, amount_units:int):
		self.fronts = self.search_borders_from_zero(mainobj)
		self.stayed_units = 0
		return list(self.fronts)



	# functions 'propose', 'relate' and 'attack' only return results, then 'Main' will set those to properties and files
	
	def relate(self, receiver):
		relation = int()
		if receiver.name == self.name:
			return False
		if receiver.name in self.enemies and random() < 0.1:
			relation += randint(-5, 0)
		if receiver.name in self.allies and random() < 0.1:
			relation += randint(0, 5)
		if random() < 0.2:
			relation += randint(-3, 3)
		if self.relationships[receiver.name] > 0 and self.relationships[receiver.name] <= 100:
			relation += randint(0, 4)
		if self.relationships[receiver.name] < 0 and self.relationships[receiver.name] >= -100:
			relation += randint(-4, 0)
		if relation:
			return (relation, receiver)
		else:
			return False

	def propose(self, receiver, action:str):
		if receiver.name == self.name:
			return False
		alliance_probability = float()
		non_agression_pact_probability = float()
		right_of_passage_probability = float()
		declare_war_probability = float()
#![ALLIANCE]
		if action == 'alliance':
			if self.relationships[receiver.name] > randint(40, 100):
				alliance_probability += 0.06
			if len(list(set(self.enemies) & set(receiver.enemies))) >= len(self.enemies) // 2:#if we have more then half similar enemies/allies...
				alliance_probability += 0.095
			if len(list(set(self.allies) & set(receiver.allies))) >= len(self.allies) // 2:# ^^higher^^
				alliance_probability += 0.090
			if not(receiver.name in self.allies) and not(receiver.name in self.enemies) and random() < alliance_probability:
				return (action, receiver)
			else:
				return False
#![NON-AGGRESION PACT]
		elif action == 'non-aggression pact':
			if self.relationships[receiver.name] > randint(-90, -40):
				non_agression_pact_probability += 0.032
			if self.enemies: # ... is not empty
				non_agression_pact_probability += 0.25
			if receiver.name in self.allies:
				non_agression_pact_probability = 0.0
			if not(receiver.name in self.non_aggression_pacts) and not(receiver.name in self.enemies) and random() < non_agression_pact_probability:
				return (action, receiver)
			else:
				return False
#![RIGHT OF PASSAGE]
		elif action == 'right of passage':
			if self.relationships[receiver.name] > randint(0, 20):
				right_of_passage_probability += 0.13
			if receiver.name in self.allies:
				right_of_passage_probability += 0.12
			if list(set(self.enemies) & set(self.enemies)):
				right_of_passage_probability += 0.05
			if not(receiver.name in self.right_of_passage) and not(receiver.name in self.enemies) and random() < right_of_passage_probability:
				return (action, receiver)
			else:
				return False
#![DECLARE WAR]
		elif action == "declare war":
			if list(set(receiver.enemies) & set(self.allies)):
				declare_war_probability += 0.45
			if self.relationships[receiver.name] < randint(-100, -60):
				declare_war_probability += 0.2
			if not(receiver.name in self.allies) and not(receiver.name in self.enemies) and random() < declare_war_probability:
				return (action, receiver)
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
