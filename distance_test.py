from math import cos, asin, sqrt

def phonenumber(string):
	digits = [each for each in string]
	x = "(" + "".join(digits[:3]) + ')'
	y = ' ' + "".join(digits[3:6]) + '-'
	z = "".join(digits[6:])
	return x + y + z

string = '6166341698'

print phonenumber(string)