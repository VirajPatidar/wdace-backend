import os
import pandas as pd

# df = pd.DataFrame(
# 	columns=["class_index", "title", "text"]
# )

os.chdir("scraped_articles")

class_index = []
title = []
text = []

os.chdir("business")
print(f"Current directory: {os.getcwd()}")

files = os.listdir()
for file in files:
	class_index.append(1)
	with open(os.path.join(os.getcwd(),file), 'r') as f:
		content = f.readlines()
	title.append(file.split('.')[0])
	text.append(content[0])


# os.chdir("../")
# os.chdir("ecommerce")
# print(f"Current directory: {os.getcwd()}")

# files = os.listdir()
# for file in files:
# 	class_index.append(2)
# 	with open(os.path.join(os.getcwd(),file), 'r') as f:
# 		content = f.readlines()
# 	title.append(str(file.split('.')[0]))
# 	text.append(str(content[0]))


os.chdir("../")
os.chdir("educational")
print(f"Current directory: {os.getcwd()}")

files = os.listdir()
for file in files:
	class_index.append(3)
	with open(os.path.join(os.getcwd(),file), 'r') as f:
		content = f.readlines()
	title.append(file.split('.')[0])
	text.append(content[0])


os.chdir("../")
os.chdir("entertainment")
print(f"Current directory: {os.getcwd()}")

files = os.listdir()
for file in files:
	class_index.append(4)
	with open(os.path.join(os.getcwd(),file), 'r') as f:
		content = f.readlines()
	title.append(file.split('.')[0])
	text.append(content[0])


os.chdir("../")
os.chdir("news")
print(f"Current directory: {os.getcwd()}")

files = os.listdir()
for file in files:
	class_index.append(5)
	with open(os.path.join(os.getcwd(),file), 'r') as f:
		content = f.readlines()
	title.append(file.split('.')[0])
	text.append(content[0])


df = pd.DataFrame({
	'class': class_index,
	'title': title,
	'text': text
})

os.chdir("../../data")
df.to_csv('train.csv', header=False, index=False)
