from PIL import Image, ImageDraw, ImageFont
import re
import copy

MAXLEN = 1000
FONTSIZE = 32
FONTPATH = r"%localappdata%\Microsoft\Windows\Fonts\Roboto-Regular.ttf"

KINDS = {"P":"pens", "W":"windows"}
RE_SPLIT = re.compile(r"(\*|_|€\d+|#\d+|@\d*|&)(?!\1)")
RE_YB = re.compile(r"(\*)(?!\1)")
RE_RESET = re.compile("(&)(?!\1)")
RE_IT = re.compile("(_)(?!\1)")
RE_PEN = re.compile("(€)(\d+)(?!\1\2)")
RE_WIN = re.compile("(#)(\d+)(?!\1\2)")
RE_SIZE = re.compile("(@)(\d*)(?!\1\2)")

PEN_YB = {"b":"1", "fc":"#FFB635", "ec": "#B77B1B", "et": "3"}

def style_add(line, parsed_file):
    kind, params = tuple(line.replace(" ", "").split("::"))
    kind = KINDS[kind[0]]
    base_style = dict([tuple(i.split(sep=":")) for i in params.split(sep=":")])
    parsed_file[kind].append(base_style)
    return parsed_file

def time_set(time):
    times = [i.replace(" ", "") for i in time.split("-->")]
    int_times = [0,0]
    for i, t in enumerate(times):
        tlist = list(re.split(r"\d\d+", t))
        int_times[i] = int(tlist[-1]) + int(tlist[-2])*1000 + int(tlist[-3])*60000 + (0 if len(tlist) < 4 else int(tlist[0])*3600000)
    return tuple(int_times)

def parse_style(word, default={}):
	style = copy.copy(default)
	win = None
	yb_check = False
	if re.match(RE_IT, word):
		if style["i"]:
			del style["i"]
		else:
			style["i"] = "1"
	if m := re.match(RE_WIN):
		win = m[2]
	if re.match(RE_YB):
		if True:
			pass
		

def line_add(line, time, parsed_file, new_win):
    word_list = line.split(" ")
    first = word_list.pop(0)
    if not (new_win or re.match(RE_WIN, first)):
    	parsed_line = parsed_file["lines"].pop(-1)
    else:
    	parsed_line = {"segments":[], "window":None, "pen":{}}
    if re.search(RE_SPLIT, first):
    	parsed_line["pen"], parsed_line["window"] = parse_style(first)
    else:
    	word_list.insert(1, first)
    for w in word_list:
    	if re.search(RE_SPLIT, w):
    		style_list = None
    	else:
    		pass
    return parsed_file

def parse(lines):
    parsed_file = {"pens":[PEN_YB], "windows":[], "lines":[]}
    time = (0, 0)
    new_win = False
    for line in lines:
        if "::" in line:
            parsed_file = style_add(line, parsed_file)
        elif "-->" in line:
            time = time_set(line)
            new_win = True
        elif not line.isspace() and not line == "WEBVTT":
            parsed_file = line_add(line, time, parsed_file, new_win)
            new_win = False

def main():
    filename = input("Filename: ")
    with open(filename + ".vtt", "r") as file:
        parsed_file = parse(file.readlines[3:])

if __name__ == '__main__':
    main()
