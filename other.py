import datetime

def print1(text):
	current_time = datetime.datetime.now()
	tstr = current_time.strftime("%m/%d/%Y, %H:%M:%S")
	print(f"[{tstr}] {text}")