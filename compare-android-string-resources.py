#!/usr/bin/python3

import sys
import os

if len(sys.argv) != 2:
	print("Invalid input arguments")
	print()
	print("Usage: %s resource_directory" % sys.argv[0])
	exit(1)

sResourceDirectory = sys.argv[1]
if not os.path.isdir(sResourceDirectory):
	print("Invalid directory")
	exit(2)

hResources = {}

for sItem in os.listdir(sResourceDirectory):
	sDir = os.path.join(sResourceDirectory, sItem)

	if os.path.isdir(sDir) and sItem.startswith("values"):
		sResourceFile = os.path.join(sDir, "strings.xml")
		sLocale = sItem.replace("values-", "")
		sLocale = sLocale.replace("values", "")
		if len(sLocale) == 0:
			sLocale = "default"

		if(os.path.isfile(sResourceFile)):
			hResources[sLocale] = sResourceFile

iLen = len(hResources)
if iLen == 0:
	print("No string resource files found")
	exit(3)
elif iLen == 1:
	print("Only one string resource file found")
	exit(4)

print("Found %d string resource files" % iLen)
hResourceNames = {}

for k,v in hResources.items():
	print("Parsing locale %s ..." % k)
	
	hResourceNamesSet = set()
	hResourceNames[k] = hResourceNamesSet

	with open(v, "r") as f:
		for sLine in f:
			sLine = sLine.strip()
			
			if not sLine.startswith("<string name="):
				continue
			
			# the string has been already found
			iStartIdx = 14
			iEndIdx = sLine.find("\">",iStartIdx)

			if iEndIdx == -1:
				continue

			hResourceNamesSet.add(sLine[iStartIdx:iEndIdx])


print()
print("Checking consistency between localizations")
print("Going to look for differences between the default locale and the others found in the project")

hDefaultLocale = hResourceNames["default"]
bFound = False

for k,v in hResourceNames.items():
	if k == "default":
		continue
	
	hDiffSet = hDefaultLocale - v
	if len(hDiffSet) > 0:
		bFound = True
		print("\nFound %d differences (default -> %s)" % (len(hDiffSet),k))
		for s in hDiffSet:
			print("\t%s" % s)
	
	hDiffSet = v - hDefaultLocale
	if len(hDiffSet) > 0:
		bFound = True
		print("\nFound %d differences (%s -> default)" % (len(hDiffSet),k))
		for s in hDiffSet:
			print("\t%s" % s)

if not bFound:
	print("\nSeems your string resource files are in a good state. Good job dude")
