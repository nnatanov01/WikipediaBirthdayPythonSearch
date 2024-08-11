import wikipedia;
import mwparserfromhell;
import requests;


#returns index of year + 1. Not necessarily foolproof but good enough method with not fully structured data
def GetIndexOfMonth (birthdatedata) :
    if hasattr(birthdatedata,"params") == False: return None
        
    data = birthdatedata.params;
    t = next(filter(lambda x: x.isnumeric() and len(x) == 4, data), None)
    if t == None : 
        return None 
    else :
       return birthdatedata.params.index(str(t)) + 1;


result = wikipedia.search("serial killer",results = 100000)#100000
massiveString = '';
skippedCounter = 0
for x in result:
    try:
        title = x
        url = 'http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvsection=0&titles=' + title + '&format=json'
        res = requests.get(url)
        text = list(res.json()["query"]["pages"].values())[0]["revisions"][0]["*"]
        wiki = mwparserfromhell.parse(text)
        if len(wiki.filter_templates(matches="birth_date")) < 1 : continue;
        birth_data = wiki.filter_templates(matches="birth_date")[0]
        baseBirthData = birth_data.get('birth_date').value.nodes
        FirstBirthData = next(filter(lambda x: 'birth' in x.lower(), baseBirthData), None)
        if FirstBirthData == None: continue;
        IndexOfMonth = GetIndexOfMonth(FirstBirthData)
        if IndexOfMonth == None: skippedCounter += 1; continue
            
            
        try:
           birth_month = FirstBirthData.params[IndexOfMonth]
        except IndexError:
            skippedCounter += 1
            continue #no data on month
        print(birth_month)
        if (int(str(birth_month)) > 12) : 
            skippedCounter += 1; continue
        massiveString += '(' + str(birth_month) + ')'
    except: skippedCounter = skippedCounter + 1; continue

print (massiveString)
print ('skipped because of lack of data or poor structure ' + str(skippedCounter))
