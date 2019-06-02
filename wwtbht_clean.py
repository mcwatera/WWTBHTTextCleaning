#!/usr/bin/env python

import os
import re
import os.path
import nltk
import operator
from nltk import word_tokenize

dir = os.getcwd()

stop_words = nltk.corpus.stopwords.words('english')

punctuations = [".", ". ", ",", ", ", "!", "! ", "?", "? ", ";", "; ", "‘", "‘ ", "’", "’ ", ":", ": ", "'", "' ", "—", "— ", "'s", "'s ", "(", "( ", ")", ") ", " ", " ", "\n", "\t", "-", "- "]

nonsense_letters = ["b", "c", "d", "e", "f", "g", "h", "a", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

words = set(nltk.corpus.words.words())

#clean xml tags
#clean "poem" tags for separate export

def clean_html(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext

for filename in os.listdir('source_text'):
	with open(os.path.join('source_text', filename)) as currentfile:
		content = currentfile.read().lower()
		no_html_content = clean_html(content)
		tokens = word_tokenize(no_html_content)
		real_tokens = []
		for i in tokens:
			if i not in stop_words and "xml" not in i and i not in punctuations and i not in nonsense_letters and i.isalpha():
				if "." in i:
					place = i.index(".")
					first_word = i[0:place]
					second_word = i[place+1:]
					real_tokens.append(first_word)
					real_tokens.append(second_word)
					continue
				if "—" in i and i.index("—") != len(i)-1:
					place = i.index("—")
					first_word = i[0:place]
					second_word = i[place+1]
					real_tokens.append(first_word)
					real_tokens.append(second_word)
					continue
				real_tokens.append(i)
		for i in real_tokens:
			for punctuation in punctuations:
				if punctuation in i:
					i = i.replace(punctuation, "")
			if i == " " or i == "\t" or i == "\n":
				real_tokens.remove(i)
		for i in real_tokens:
			if i not in words:
				real_tokens.remove(i)
		new_file_name = filename + "_new"
		new_file = open(new_file_name, "a+")
		for token in real_tokens:
			new_file.write("%s \n" %token)
	print("Created and appended for new %s file" %filename)
	
				
			
