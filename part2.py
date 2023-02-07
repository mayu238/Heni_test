import re
string1='19×52cm'
string2='50 x 66,4 cm'
string3='168.9 x 274.3 x 3.8 cm (66 1/2 x 108 x 1 1/2 in.)'
string4='Sheet: 16 1/4 × 12 1/4 in. (41.3 × 31.1 cm) Image: 14 × 9 7/8 in. (35.6 × 25.1 cm)'
string5='5 by 5in'

def part1(string1):
	text=string1
	regex=re.compile(r"(\d+)×(\d+)cm")
	regex2 = regex.search(text)
	height=regex2.group(1)
	width=regex2.group(2)
	print(width)

def part2(string2):
	text=string2
	regex=re.compile(r"(\d+(?:,\d+)?) x (\d+(?:,\d+)?) cm")
	regex2 = regex.search(text)
	height=regex2.group(1)
	width=regex2.group(2)
	print(width)

def part3(string3):
	text=string3
	regex=re.compile(r"(\d+(?:\.\d+)?) x (\d+(?:\.\d+)?) x (\d+(?:\.\d+)?) cm")
	regex2 = regex.search(text)
	height=regex2.group(1)
	width=regex2.group(2)
	depth=regex2.group(3)
	print(depth)

def part4(string4):
	text=string4
	regex=re.compile(r"Image: \d+ × \d+ \d/\d+ in. \((\d+\.\d+) × (\d+\.\d+) cm\)")
	regex2 = regex.search(text)
	height=regex2.group(1)
	width=regex2.group(2)
	print(height)

def part5(string5):
	text=string5
	regex=re.compile(r"(\d+) by (\d+)in")
	regex2 = regex.search(text)
	height=2.54*float(regex2.group(1))
	width=2.54*float(regex2.group(2))
	print(width)

part1(string1)
part2(string2)
part3(string3)
part4(string4)
part5(string5)


#Regex answers are below
# 1)r"(\d+)x(\d+)cm"
# 2)r"(\d+(?(:,\d+)?) x (\d+(?:,\d+)?) cm"
# 3)r"(\d+(?:\.\d+)?) x (\d+(?:\.\d+)?) x (\d+(?:\.\d+)?) cm"
# 4)r"Image: \d+ × \d+ \d/\d+ in. \((\d+\.\d+) × (\d+\.\d+) cm\)"
# 5)r"(\d+) by (\d+)in" - this gets the dimensions in inches. Can then multiply by 2.54 to get the cm