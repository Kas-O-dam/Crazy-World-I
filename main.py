import tkinter as tk

from json import loads
from json import load
from json import dumps
from time import sleep
from random import randint
from PIL import Image
from icecream import ic
from os import system

# import from local scripts
from bot import Bot
from shell_errors import *
#from user import User

class Main:
	# place canva
	def place_canvas(self):
		self.canvas.place(x = 0, y = 0)
		self.turn_button[0].place(x = 0, y = 0)
		self.view_button[0].place(x = 70, y = 0)

	#place unit (pixel but with custom sizes)
	def place_unit(self, x:int, y:int, colour:str):
		return self.canvas.create_rectangle(x * self.unit_size, y * self.unit_size, x * self.unit_size + self.unit_size, y * self.unit_size + self.unit_size, width = 0, fill = colour)
	# hz
	def init_canvas(self, path):
		with open(path, 'r') as map:
			map = json.loads(map.read())
			x_counter = int()
			y_counter = int()
			for x in range(0, self.width, self.unit_width):
				x_counter += 1
				for y in range(0, self.height, self.unit_height):
					y_counter += 1
					place_unit((x, y, map[x_counter][y_counter]))

	def loop(self): # recursive function for turns
		system("clear")
		for country in self.countryset:
			data = dict()
			# data = {
			# 	"attack": [(x1, y1), (x2, y2)...],
			# 	"propose": (what proposed, to who proposed)
			# }
			country.stayed_units = randint(0, country.power)
			while country.stayed_units:
				data = country.turn(self, country.stayed_units)
				# when the attack is relised and pixels were put, we need come back if have some "amount_units" yet
				if not data["attack"]: break # if country hasn't borders with enemie
				for i in data["attack"]:
					self.place_unit(i[0], i[1], country.colour)
					self.map[i[0]][i[1]] = country.colour
			if data.get("propose", False):
				if data["propose"][0] == "declare war":
					print("[ \033[34mG\033[0m ]", "\033[33m", country.name, "\033[0mdeclare war to\033[33m", data["propose"][1].name, "\033[0m")
					data["propose"][1].enemies.add(country.name)
					country.enemies.add(data["propose"][1])
				elif data["propose"][0] == "allie":
					print("[ \033[34mG\033[0m ]", "\033[33m", country.name, "\033[0mcreate allie with\033[33m", data["propose"][1].name, "\033[0m")
					data["propose"][1].allies.add(country.name)
					country.allies.add(data["propose"][1])
				elif data["propose"][0] == "right of passage":
					print("[ \033[34mG\033[0m ]", "\033[33m", country.name, "\033[0mcreate right of passage with\033[33m", data["propose"][1].name, "\033[0m")
					data["propose"][1].right_of_passage.add(country.name)
					country.right_of_passage.add(data["propose"][1])
				elif data["propose"][0] == "non-aggression pact":
					print("[ \033[34mG\033[0m ]", "\033[33m", country.name, "\033[0mcreate non-aggression pact with\033[33m", data["propose"][1].name, "\033[0m")
					data["propose"][1].non_aggression_pacts.add(country.name)
					country.non_aggression_pacts.add(data["propose"][1])
			if data.get("relate", False):
				if data["relate"][0] > 0:
					print("[ \033[34mG\033[0m ]", "\033[33m", country.name, "\033[0m relation to\033[33m", data["relate"][1].name, "\033[0mbecomes better per", data["relate"][0])
				else:
					print("[ \033[34mG\033[0m ]", "\033[33m", country.name, "\033[0mrelation to\033[33m", data["relate"][1].name, "\033[0mbecomes worst per", data["relate"][0])
				country.relationships[data["relate"][1].name] += data["relate"][0]
				

	def view_loop(self): # for debug
		for country in self.countryset:
			data = list()
			data += country.borders_view(self, country.stayed_units)
			for i in data:
				if i is not None:
					self.place_unit(i[0], i[1], 'magenta')

	def rgb_to_hex(self, rgb:tuple):
		if not rgb[3]: return self.colour_sea
		return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
	# convert from png to tkinter's canvas and save to self.map	
	def init_map(self):
		self.map = []
		with Image.open(self.scenario_path + '/map.png') as self.png:
			self.png.mode = 'RGBA'
			self.premap = self.png.load()
			for x in range(self.png.width):
				self.map.append([])
				for y in range(self.png.height):
					self.place_unit(x, y, self.rgb_to_hex(self.premap[x, y]))
					self.map[len(self.map) - 1].append(self.rgb_to_hex(self.premap[x, y]))
		self.__delattr__("png")
		self.__delattr__("premap")
	def pack(self, path:str):
		...
	def unpack(self): #work with json/yaml
		empires = dict()
		with open(f'{self.scenario_path}/empires.json', 'r') as empires_JSON:
			empires = loads(empires_JSON.read())
		with open(f'{self.scenario_path}/country-set.json', 'r') as file: # [{name: str, colour: str, allies:list, enemies: list, et cetera}]
			unpacked_countries = loads(file.read())
			for country in unpacked_countries:
				player = ...
				if country['type'] == 'bot':
					player = Bot(country['name'], country['colour'], country['power'])
				#elif country['type'] == 'user':
				#	player = User(country['name'], country['colour'])
				player.enemies = set(country['enemies'])
				player.allies = set(country['allies'])
				player.non_aggression_pacts = set(country['non-aggression pacts'])
				player.right_of_passage = set(country['right of passage'])
				player.relationships = country['relationships']
				player.empire = list(map(tuple, empires[player.name]))
				self.countryset.add(player)
	def __init__(self, unit_size:int, path:str, width = 1600, height = 900):
		self.width = width
		self.height = height
		self.unit_size = unit_size
		self.colour_sea = '#6790a8'
		self.scenario_path = path
		self.window = tk.Tk()
		self.window.geometry(f'{self.width}x{self.height}')
		self.canvas  = tk.Canvas(width = self.width, height = self.height, bg = self.colour_sea)
		self.canvas.bind('<Button-1>', lambda event: print(self.country_by_colour[self.map[event.x//self.unit_size][event.y//self.unit_size]], event.x//self.unit_size, event.y//self.unit_size))
		self.turn_button = tk.Button(text="Turn", command=self.loop, width=2, height=1),
		self.view_button = tk.Button(text="Borders", command=self.view_loop, width=3, height=1),
		#self.Object["menu-block"].insert(INSERT, "Hi")
		#self.Object["menu-block"].config(state=DISABLED)
		self.countryset = set()
		with open('{}/country-by-colour.json'.format(self.scenario_path), 'r') as JSON:
			self.country_by_colour = load(JSON)
main = Main(3, 'scenario/1914', width=1600, height=900)
main.place_canvas()
main.unpack()
main.init_map()
for country in main.countryset:
	country.borders = country.search_borders_from_zero(main)
main.window.mainloop()
