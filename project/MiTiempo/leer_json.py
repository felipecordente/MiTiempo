#!/usr/bin/python3
import json
import sys

diccionario = {}

def main():
	with open("municipios.json", 'r', encoding = "ISO-8859-1") as json_file:
	    munis = json.load(json_file)

	for muni in munis:
		diccionario[muni['nombre']] = muni

	return diccionario


if __name__ == '__main__':
	main()
