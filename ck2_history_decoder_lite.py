import re
import json
from jinja2 import Environment, FileSystemLoader
import os
import time
start_time = time.time()

file_loader = FileSystemLoader('')
env = Environment(loader=file_loader)

def savestr_to_str(input):
    return input[0].replace('bn="','').replace('"','').replace('_',' ').replace('nick','').replace('\n','').replace('\t','').replace('{','')

titles_html = []
known_names = {}
known_dynasties = {}

def get_dynamic_title(id,data):
    title = id
    #find the name of the dynamic title
    if 'e_' in title:
        addon = 'Empire of '
    else:
        addon = 'Kingdom of '
    title_data = re.findall(r'%s=\n		{.+?\n\t\t}' % title, data, re.S)[0]
    title = re.findall(r'name=".+?"', title_data, re.S)
    title = addon + title[0].replace('name=','').replace('"','')
    return title

def get_dynasty_name(id,data):
    dynasty_data = re.findall(r'%s=\n		{.+?\n\t\t}' % id.replace('dnt=',''), data, re.S)[0].replace('\t','')
    name = re.findall(r'name=".+?"', dynasty_data, re.S)[0].replace('"','').replace('name=','')
    known_dynasties[id] = name
    return name

def create_title_history_html(id,data,folder_id):
    title = id
    #find the history data of title
    title_data = re.findall(r'%s=\n\t\t{.+?\n\t\t}' % title,data, re.S)[0]
    history_data = re.findall(r'history=.+?\n\t\t\t}', title_data, re.S)[0].replace('history=','').replace('\t','')
    data_split = history_data.split('\n')
    chunks = []
    if 'dyn' in title:
        title = get_dynamic_title(title,data)
    title = title.replace('b_','Barony of ').replace('c_','County of ').replace('e_','Empire of ').replace('k_','Kingdom of ').replace('d_','Duchy of ').replace('_',' ')
    titles_html.append(title)
    i4 = 0
    #now break the data into history chunks
    #here the most mess is made cuz the size of the chunks varies
    for line in data_split:
        if '=' and '.' in line:
            line = line.replace('=','')
            if '}' in data_split[i4+3]:
                owner = data_split[i4+2].replace('holder=','')
                if owner == '"0"':
                    owner = 'None'
                else:
                    #here i find the real name
                    if owner not in known_names:
                        owner = get_char_name(owner)
                    else:
                        owner = known_names[owner]
                chunk = {'date':line,'owner':owner,'type':'','title':title}
                chunks.append(chunk)
            else:
                owner = data_split[i4+4].replace('who=','')
                if owner == '"0"':
                    owner = 'Unknown'
                else:
                    #here i find the real name
                    if owner not in known_names:
                        owner = get_char_name(owner)
                    else:
                        owner = known_names[owner]
                chunk = {'date':line,'owner':owner,'type':data_split[i4+5].replace('type=','') + ', ','title':title}
                chunks.append(chunk)
        i4 = i4 + 1
    #render and save the file
    template = env.get_template('template3.html')
    output = template.render(data=chunks)    
    f = open("Player " + str(i) + ' history/titles/' + title.replace('\t','') + ".html", "w")
    f.write(output)
    f.close()

def get_char_name(charid):
    try:
        chardata = re.findall(r'%s=\n\t\t{.+?\n\t\t}' % charid, data, re.S)
        #make the data readable
        correct_data = chardata[0]
        #get the essentials like names and bdays
        name = savestr_to_str(re.findall(r'bn=".+?"', correct_data, re.S))
        dynasty_id = savestr_to_str(re.findall(r'dnt=.+?\n\t\t\t', correct_data, re.S))
        if dynasty_id not in known_dynasties:
            name = name + ' ' + get_dynasty_name(dynasty_id,data)
        else:
            name = name + ' ' + known_dynasties[dynasty_id]
        known_names[charid] = name
        return name
    except:
        return 'Unknown'

print('Name of the non compressed ck2 save file (without .ck2):')
filename = input()
with open (filename+".ck2", "r") as myfile:
    data=myfile.read()
    print('File lenght: ' + str(len(data)) + ' characters or: ' + str(len(data.split('\n'))) + ' lines')
    charachterhistory = re.findall(r'character_history={.+?\n}', data, re.S)
    #now we have a dirty list of player charachters with not nice chars and stuff
    i = 0
    for item in charachterhistory:
        charachterhistory[i] = str.split(charachterhistory[i].replace('character_history=','').replace('{','').replace('\n',' ').replace('\t',''),'}')
        i2 = 0
        for item2 in charachterhistory[i]:
            #convert to dict
            #look at the amount of work required to make the data into a dictionary. Like wtf paradox?
            if i2 == 0:
                item2 = ' ' + item2
            item2 = item2.replace(' ','',3)
            item2 = item2.replace(' ',',',2)
            item2 = item2.replace(' ','',1)
            item2 = item2.replace('=',':')
            item2 = item2.replace('identity','"identity"')
            item2 = item2.replace('date','"date"')
            item2 = item2.replace('score','"score"')
            item2 = '{' + item2 + '}'
            try:
                charachterhistory[i][i2] = json.loads(item2)
            except:
                print('Something went wrong while loading the character history. The current loading state: ' + item2)
            i2 = i2 + 1
        charachterhistory[i] = list(filter(None,charachterhistory[i]))
        # now we have a clean list of dicts, yay
        i = i + 1
    print('Character history decoded...')
    print('Starting character detail extraction now')
    #lets render the results and stuff
    i = 0
    lines = data.split('\n')
    for item in charachterhistory:
        titles_html = []
        # create the directory
        try:
            os.mkdir("Player " + str(i) + " history")
        except:
            print('Directory is already here...')
        try:
            os.makedirs("Player " + str(i) + " history/titles")
        except:
            print('Title directory is already here...')
        i2 = 0
        #foreach character id
        for character in item:
            charid = str(character['identity'])
            #get the data 
            chardata = re.findall(r'%s=\n		{.+?\n\t\t}' % charid, data, re.S)
            #make the data readable
            correct_data = chardata[0]
            #get the essentials like names and bdays
            name = savestr_to_str(re.findall(r'bn=".+?"', correct_data, re.S))
            dynasty_id = savestr_to_str(re.findall(r'dnt=.+?\n\t\t\t', correct_data, re.S))
            if dynasty_id not in known_dynasties:
                name = name + ' ' + get_dynasty_name(dynasty_id,data)
            else:
                name = name + ' ' + known_dynasties[dynasty_id]
            known_names[charid] = name
            bd =  savestr_to_str(re.findall(r'b_d=".+?"', correct_data, re.S))
            try:
                nick = savestr_to_str(re.findall(r'nick=.+?\n', correct_data, re.S))
            except:
                nick = 'No nickname'
            try:
                kills = re.findall(r'kill_list=.+?\n\t\t\t}', correct_data, re.S)
                kills_internal = re.findall('id', kills[0], re.S)
                num_of_kills = len(kills_internal)
            except:
                num_of_kills = 0
            try:
                #try and get the death date
                dd = savestr_to_str(re.findall(r'd_d=".+?"', correct_data, re.S))
                #while we are here might just as well get the titles
                titles = re.findall(r'oh=".+?"', correct_data, re.S)
                claims = []
                #try and get the cause of death (sometimes its missing)
                try:
                    cd = savestr_to_str(re.findall(r'c_d=.+?\n', correct_data, re.S))
                except:
                    cd = 'NA'
            except:
                #if that fails the char must be alive
                dd = 'Not dead'
                titles = []
                lineid = 0
                #find all the lines with holder=charid
                for line in lines:
                    if line == '\t\t\tholder=' + charid:
                        #now calculate the line id of the line with the title name
                        line_correct = lines[lineid - 3]
                        #now just make sure to grab the right line
                        if line_correct == '\t\t\t\tis_custom=yes':
                            titles.append(lines[lineid - 9].replace('=',''))
                        elif '_' and '='  in line_correct:
                            titles.append(line_correct.replace('=',''))
                        elif '_' and '=' in lines[lineid - 2]:
                            titles.append(lines[lineid - 2].replace('=',''))
                        elif '_' and '=' in lines[lineid -4]:
                            titles.append(lines[lineid - 4].replace('=',''))
                    lineid = lineid + 1
                claims = re.findall(r'claim=.+?}', correct_data, re.S)
            #try and get the religion (it might be missing)
            try:
                rel =  savestr_to_str(re.findall(r'rel=".+?"', correct_data, re.S))
            except:
                rel = 'NA'
            #get the culture (it might be misssing)
            try:
                cul =  savestr_to_str(re.findall(r'cul=".+?"', correct_data, re.S))
            except:
                cul = 'NA'
            i3 = 0
            #now work on the claim data to make it human friendly
            claims = list(filter(None,claims))
            for claim in claims:
                claim = claim.replace('claim=','').replace('}','').replace('{','').replace('\n',' ').replace(' ','',2).replace('\t','')
                claim = claim.replace('title=','')
                if 'base_' in claim:
                    claim = claim.replace(' ','',2).replace('"','')
                claim = claim.split(' ')[0]
                if 'dyn_' in claim:
                    create_title_history_html(claim,data,i)
                    claim = get_dynamic_title(str(claim).replace('\t',''),data)
                if claim not in titles_html and 'd_' in claim or 'e_' in claim or 'k_' in claim:
                    try:
                        create_title_history_html(claim,data,i)
                    except:
                        print(claim)
                claims[i3] = claim.replace('b_','Barony of ').replace('c_','County of ').replace('e_','Empire of ').replace('k_','Kingdom of ').replace('d_','Duchy of ')
                i3 = i3 + 1
            #reset the i3 counter and make the title friendly
            i3 = 0
            for title in titles:
                title = title.replace('oh="','').replace('"','').replace('title=','').replace('{','')
                if 'dyn_' in title:
                    create_title_history_html(title,data,i)
                    title = get_dynamic_title(title,data)
                if title not in claims:
                    #if the title isnt also a claim
                    if title not in titles_html and 'd_' in title or 'e_' in title or 'k_' in title:
                        create_title_history_html(title,data,i)
                    title = title.replace('b_','Barony of ').replace('c_','County of ').replace('e_','Empire of ').replace('k_','Kingdom of ').replace('d_','Duchy of ')
                    titles[i3] = title.replace('_',' ')
                else:
                    #if for some reason a claim and a title overlap delete the title
                    titles.pop(i3)
                i3 = i3 + 1
            #get the chars goverment type
            gov =  savestr_to_str(re.findall(r'gov=.+?\n', correct_data, re.S))
            #nice one big array
            chardata = [name,bd.replace('b d=',''),dd.replace('d d=',''),cd.replace('c d=','').replace('death trait','natural causes'),rel.replace('rel=',''),cul.replace('cul=',''),gov.replace('gov=',''),titles,claims,nick.replace('=',''),num_of_kills]
            #we have the data and now is the time to create html files for the encyclopedia
            item[i2]['identity'] = name
            item[i2]['id_local'] = i2
            template = env.get_template('template2.html')
            output2 = template.render(data=chardata,titles=titles_html)
            history = "history\ "
            f = open("Player " + str(i) + ' ' + history.replace(' ','') + chardata[0] + str(i2) + ".html", "w")
            f.write(output2)
            f.close()
            i2 = i2 + 1
        #all the little files are rendered, time to render the hub
        template = env.get_template('template.html')
        output = template.render(data=item)    
        f = open("Player " + str(i) + " history\Player " + str(i) + " history.html", "w")
        f.write(output)
        f.close()
        i = i + 1
    print('Done...')
    print("--- %s seconds ---" % (time.time() - start_time))
input('Press enter to end the program...')


