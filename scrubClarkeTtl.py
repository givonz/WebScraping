# Get all links for Clarks entries.

from bs4 import BeautifulSoup
from urllib.request import urlopen

def get_all_links(webPage):
#
#   ClarkeStart = urlopen("http://www.homeoint.org/clarke/a.htm").read()
    ClarkeStart = urlopen(webPage).read()
    soup=BeautifulSoup(ClarkeStart,"html.parser")
    y=soup.find_all("a")

#open file, append
    for link in y:
        if len(link.get("href"))==5:
            continue
        if  link.get("href")[-9:]=="index.htm":
            continue
#go to remedy page
        webpage2="http://www.homeoint.org/clarke/"+link.get("href")
        remedyRead = urlopen(webpage2).read()
        soup2=BeautifulSoup(remedyRead,"html.parser")
        y2=soup2.find_all("p")
# p2 = latin name, p3=common names
# p4=clinical uses--have to parse p4 manually, looses data in soup
        for line in range(len(y2)):
            print(y2[2],"\n",y2[3],"\n")
            ans=input("Y/N ")
# extract name
            name=str(y2[2])
# countStop is "<" because 2nd "<" indicates end of name
            countStop=0
            start=0
            stop=0
            for pos in range(len(name)-1):
# countStart first ">" indicates beginning of name
                 if name[pos:pos+1]==">":
                     start=pos+1
                 if name[pos:pos+1]=="<":
                     countStop+=1
                     if countStop==2:
#removes period after name
                         stop=pos-1
            print(name[start:stop])
            ans=input("y-n")
#extract common names
            commonNames=str(y2[3])
# countStop is "<" because 2nd "<" indicates end of name
            countStop=0
            start=0
            stop=0
            for pos in range(len(commonNames)-1):
# countStart first ">" indicates beginning of name
                 if commonNames[pos:pos+1]==">":
                     start=pos+1
                 if commonNames[pos:pos+1]=="<":
                     countStop+=1
                     if countStop==2:
#removes period after name
                         stop=pos-1
            print(commonNames[start:stop])
#&&&
            searchLen=len(commonNames)
            for x in range(searchLen):
                 if x==searchLen:
                      break
                 if commonNames[x:x+8]=="        ":
                      commonNames=commonNames[:x-1]+commonNames[x+10:]
            start=0
            stop=0
            for pos in range(len(commonNames)):
                  if commonNames[pos:pos+1]=="<":
                      start=pos
                  if commonNames[pos:pos+1]==">":
                      stop=pos
                      break
            commonNames=commonNames[1:1]+commonNames[pos+1:]
            formattedCommonNames=convert2CSV(commonNames)
#extract diseases
            diseases=extractDiseases(soup2)
            print(diseases)
#write record
            break
#close file

def extractDiseases(soup3):
  info=str(soup3)
  passClinical=0
  startDiseases=0
  stopDiseases=0
  for pos in range(len(info)):
      if info[pos:pos+8]=="Clinical":
          passClinical=1
      if passClinical==1 and info[pos:pos+4]=="</b>":
          startDiseases=pos+4
      if startDiseases>0 and info[pos:pos+13]=="</blockquote>":
          stopDiseases=pos
          break
  print(info[startDiseases:stopDiseases])
  reformattedDiseases=info[startDiseases:stopDiseases]
  print(startDiseases,stopDiseases)
# parse for <i> & replace with 2
  print(reformattedDiseases)
  searchLen=len(reformattedDiseases)
  for x in range(searchLen):
      if x==searchLen:
          break
      if reformattedDiseases[x:x+3]=="<i>":
          reformattedDiseases=reformattedDiseases[:x]+" 2"+reformattedDiseases[x+3:]
      if reformattedDiseases[x:x+22]=='<font color="#0000ff">':
          reformattedDiseases=reformattedDiseases[:x]+reformattedDiseases[x+22:]
      if reformattedDiseases[x:x+7]=="</font>":
          reformattedDiseases=reformattedDiseases[:x]+reformattedDiseases[x+7:]
#due to repositioning, must start search from beginning
  for x in range(searchLen):
      if x==searchLen:
          break
      if reformattedDiseases[x:x+4]=="</i>":
          reformattedDiseases=reformattedDiseases[:x]+reformattedDiseases[x+4:]
#due to repositioning, must start search from beginning
  for x in range(searchLen):
      if x==searchLen:
          break
      if reformattedDiseases[x:x+1]=="\n":
          reformattedDiseases=reformattedDiseases[:x]+reformattedDiseases[x+1:]
  for x in range(searchLen):
      if x==searchLen:
          break
      if reformattedDiseases[x:x+8]=="        ":
          reformattedDiseases=reformattedDiseases[:x]+reformattedDiseases[x+6:]
#or reformattedDiseases[x:x+1]=="\f" or reformattedDiseases[x:x+1]=="\r" or reformattedDiseases[x:x+1]=="\t":
          reformattedDiseases=reformattedDiseases[:x]+reformattedDiseases[x+1:]

  print(reformattedDiseases)
#format output record
  outrec=convert2CSV(reformattedDiseases)

#  info=info[startDiseases:stopDiseases]
#remove all tags, replace italics with numeral 2
# &&& up to here
  ans=input("display diseases")
  return(info[startDiseases:stopDiseases])

def convert2CSV(outrec):
  csvRecord='"'
  x=0
  upto=0
  while(x < len(outrec)):
      if outrec[x:x+1] == '.':
           if outrec[x-1:x]=='N' or outrec[x-1:x]=='O':
                x+=1
                continue
           csvRecord=csvRecord+outrec[upto:x]+'","'
           y=1
           while(outrec[x+y:x+y+1]==' '):  #passing over space
               y+=1
               continue
           upto=x+y
      x+=1
  csvRecord=csvRecord[:len(csvRecord)-2]  #remove trailing ',"'
#add in level 1
  x=0
  while(x < len(csvRecord)):
      if csvRecord[x:x+1] == '"' and (csvRecord[x+1:x+2]>="A" and csvRecord[x+1:x+2]<="Z"):
           csvRecord=csvRecord[:x+1]+'1'+csvRecord[x+1:]
      x+=1
#separate levels into separate fields
  x=0
  while(x < len(csvRecord)):
      if csvRecord[x:x+1] == '"':
            if csvRecord[x+1:x+2]=="1":
                 csvRecord=csvRecord[:x+2]+'","'+csvRecord[x+2:]
                 x=x+3
            if csvRecord[x+1:x+2]=="2":
                 csvRecord=csvRecord[:x+2]+'","'+csvRecord[x+2:]
                 x=x+3   #advance 2 characters + 1, or grows infinitely
      x+=1
  print(csvRecord)
  ans=input("y--n")
  return(csvRecord)

def main():
#loop 26 times, from a-z
    for x in range(26):
        webPage="http://www.homeoint.org/clarke/"+chr(97+x)+".htm"
#       print(webPage)
        get_all_links(webPage)

main()

