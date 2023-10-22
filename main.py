import tkinter as tk

from json import loads
from json import dumps
from time import sleep
from random import randint
from PIL import Image

# import from local scripts
from bot import Bot
#from user import User

class Main:
	class SizeWarning():
		def __init__(self, size:tuple):
			self.name = 'SizeWarning'
		def __str__(self):
			return f'\033[34m{self.name}\033[0m: width ({size[0]}) isn\'t equal height ({size[1]}), height will assign mean from width'
	# place canva
	def place_canvas(self):
		self.canvas.place(x = 0, y = 0)
		self.turn_button[0].place(x = 0, y = 0)
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
		for country in self.countryset:
			data = country.turn(self, randint(0, 100))
			for i in data:
				if i is not None:
					self.place_unit(i[0], i[1], country.colour)
					self.map[i[0]][i[1]] = country.colour
			# for country_data in data:
			# 	if country_data[0]:
			# 		for unit in country_data[0]:
			# 			self.place_unit(unit[0], unit[1], '#ff00ff')
	# for PIL
	def rgb_to_hex(self, rgb:tuple):
		if not rgb[3]: return self.colour_sea
		return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
	# convert from png to tkinter's canvas and save to self.map	
	def init_map(self, path:str):
		self.map = []
		with Image.open(path + '/map.png') as self.png:
			self.png.mode = 'RGBA'
			self.premap = self.png.load()
			for x in range(self.png.width):
				self.map.append([])
				for y in range(self.png.height):
					self.place_unit(x, y, self.rgb_to_hex(self.premap[x, y]))
					self.map[len(self.map) - 1].append(self.rgb_to_hex(self.premap[x, y]))
	def pack(self, path:str):
		...
	#some work with game saving (config/countryset.json)
	def unpack(self, path:str): #work with json/yaml
		with open(f'{path}/config.json', 'r') as file: # [{name: str, colour: str, allies:list, enemies: list, et cetera}]
			unpacked_countries = loads(file.read())
			for country in unpacked_countries:
				player = ...
				if country['type'] == 'bot':
					player = Bot(country['name'], country['colour'])
				#elif country['type'] == 'user':
				#	player = User(country['name'], country['colour'])
				player.enemies = country['enemies']
				player.allies = country['allies']
				player.non_aggression_pacts = country['non-aggression pacts']
				player.right_of_passage = country['right of passage']
				player.relationships = country['relationships']
				self.countryset.add(player)
		return True
	def __init__(self, unit_size:int, width = 1600, height = 900):
		self.width = width
		self.height = height
		self.unit_size = unit_size
		self.colour_sea = '#6790a8'
		self.window = tk.Tk()
		self.window.geometry(f'{self.width}x{self.height}')
		self.canvas  = tk.Canvas(width = self.width, height = self.height, bg = self.colour_sea)
		self.turn_button = tk.Button(text="Turn", command=self.loop, width=2, height=1),
		#self.Object["menu-block"].insert(INSERT, "Hi")
		#self.Object["menu-block"].config(state=DISABLED)
		self.countryset = set()
		self.country_by_colour = {
			"#6790a8": "Sea",
			"#864747": "Britain",
			"#457540": "Russian empire",
			"#373737": "German empire"
		}
main = Main(1, width=400, height=225)
main.place_canvas()
main.unpack('scenario/1914')
main.init_map('scenario/1914')
main.window.mainloop()