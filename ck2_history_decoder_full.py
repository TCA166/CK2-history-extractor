import re
import json
from jinja2 import Environment, FileSystemLoader
import os
import time
import ClauseWizard
start_time = time.time()

file_loader = FileSystemLoader('')
env = Environment(loader=file_loader)

titles_html = []
known_names = {}
known_dynasties = {}

def savestr_to_str(input):
    return input[0].replace('bn="','').replace('"','').replace('_',' ').replace('nick','').replace('\n','').replace('\t','').replace('{','')

def get_real_title_name(input):
    if input.count('_') > 1:
        input = ' '.join(input.rsplit('_', input.count('_') - 1))
    return input.replace('b_','Barony of ').replace('c_','County of ').replace('e_','Empire of ').replace('k_','Kingdom of ').replace('d_','Duchy of ')

def get_all_once_owned(charid,data,titles):
    data_split = re.findall(r'\ttitle=\n\t{.+?\n\t}',data, re.S)[0].split('\n')
    i = 0
    chars_once_owned = []
    chars_once_owned_raw = []
    title_name = ''
    for line in data_split:
        if line == '\t\t\tprevious=':
            previous_owners = data_split[i + 2].replace('\t','')
            previous_owners = previous_owners.split(' ')
            if charid in previous_owners and real_title not in titles:
                chars_once_owned.append(real_title)
                chars_once_owned_raw.append(title_name)
        elif line == '\t\t{':
            title_name = data_split[i - 1].replace('=','').replace('\t','')
            if 'dyn' in title_name:
                real_title = get_dynamic_title(title_name,data)
            else:
                real_title = get_real_title_name(title_name)
        i = i + 1
    return [chars_once_owned,chars_once_owned_raw]

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
    history_data = re.findall(r'history=.+?\n\t\t\t}', title_data, re.S)[0]
    if 'dyn' in title:
        title = get_dynamic_title(title,data)
    title = get_real_title_name(title)
    try:
        liege = re.findall(r'liege=.+?\n', title_data, re.S)[0]
        liege = liege.replace('liege=','')
        if '{' in liege:
            liege = re.findall(r'title=".+?"', title_data, re.S)[0]
            liege = liege.replace('"','').replace('title=','')
        if 'dyn' in liege:
            liege = get_dynamic_title(liege,data)
        liege = get_real_title_name(liege)
    except:
        liege = 'None'
    try:
        de_liege = re.findall(r'de_jure_liege=.+?\n', title_data, re.S)[0]
        de_liege = de_liege.replace('de_jure_liege=','')
        if '{' in de_liege:
            de_liege = re.findall(r'title=".+?"', title_data, re.S)[0]
            de_liege = de_liege.replace('"','').replace('title=','')
        if 'dyn' in de_liege:
            de_liege = get_dynamic_title(de_liege,data)
        de_liege = get_real_title_name(de_liege)
    except:
        de_liege = 'None'
    cw_tokens = ClauseWizard.cwparse(history_data)
    cw_data = ClauseWizard.cwformat(cw_tokens)
    chunks = []
    for item in cw_data['history']:
        if isinstance(cw_data['history'][item]['holder'], dict):
            owner = cw_data['history'][item]['holder']['who']
            if owner not in known_names:
                owner = get_char_name(owner)
            else:
                owner = known_names[owner]
            chunk = {'date':item,'owner':owner,'type':cw_data['history'][item]['holder']['type'] + ', ','title':title}
            chunks.append(chunk)
        elif isinstance(cw_data['history'][item]['holder'], int):
            owner = cw_data['history'][item]['holder']
            
            if owner not in known_names:
                owner = get_char_name(owner)
            else:
                owner = known_names[owner]
            chunk = {'date':item,'owner':owner,'type':'created' + ', ','title':title}
            chunks.append(chunk)
        else:
            chunk = {'date':item,'owner':'None','type':'','title':title}
            chunks.append(chunk)
    titles_html.append(title)
    #render and save the file
    template = env.get_template('template3.html')
    output = template.render(data=chunks,liege=liege,dejure=de_liege)    
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
            print('Created player directory...')
        except:
            print('Directory is already here...')
        try:
            os.makedirs("Player " + str(i) + " history/titles")
            print('Created title directory...')
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
            cw_tokens = ClauseWizard.cwparse(chardata[0])
            cw_data = ClauseWizard.cwformat(cw_tokens)
            chardata = cw_data[charid]
            #get the essentials like names and bdays
            name = chardata['bn']
            dynasty_id = chardata['dnt']
            if dynasty_id not in known_dynasties:
                name = name + ' ' + get_dynasty_name(str(dynasty_id),data)
            else:
                name = name + ' ' + known_dynasties[dynasty_id]
            known_names[charid] = name
            bd =  chardata['b_d']
            try:
                nick = '"' + chardata['nick'].replace('_',' ').replace('nick','').replace(' ','',1) + '"'
            except:
                nick = 'No nickname'
            try:
                kills = chardata['kill_list']
                num_of_kills = len(kills)
            except:
                num_of_kills = 0
            try:
                dd = chardata['d_d'].replace('','')
                #while we are here might just as well get the titles
                titles = chardata['oh']
                claims = []
                #try and get the cause of death (sometimes its missing)
                cd = chardata['c_d']
                try:
                    cd = cd.replace('_',' ').replace('death trait','natural causes')
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
                claims = chardata['claim']
                print(claims)
            #try and get the religion (it might be missing)
            rel =  chardata['rel']
            try:
                rel = rel.replace('_',' ')
            except:
                rel = 'NA'
            #get the culture (it might be misssing)
            cul =  chardata['cul']
            try:
                cul = cul.replace('_',' ')
            except:
                cul = 'NA'
            i3 = 0
            #now work on the claim data to make it human friendly
            if not isinstance(claims, list):
                claims = [claims]
            for claim in claims:
                claim = claim['title']
                if isinstance(claim, dict):
                    claim = claim['title']
                if 'dyn_' in claim:
                    create_title_history_html(claim,data,i)
                    claim = get_dynamic_title(str(claim),data)
                else:
                    claim = get_real_title_name(claim)
                if claim not in titles_html and 'd_' in claim or 'e_' in claim or 'k_' in claim:
                    try:
                        create_title_history_html(claim,data,i)
                    except:
                        print(claim)
                claims[i3] = claim
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
                    title = get_real_title_name(title)
                    titles[i3] = title.replace('_',' ')
                else:
                    #if for some reason a claim and a title overlap delete the title
                    titles.pop(i3)
                i3 = i3 + 1
            i3 = 0
            once_owned = get_all_once_owned(charid,data,titles)
            for title in once_owned[1]:
                if title not in titles_html and 'd_' in title or 'e_' in title or 'k_' in title:
                    create_title_history_html(title,data,i)
            #get the chars goverment type
            gov =  chardata['gov'].replace('_',' ')
            #nice one big array
            chardata = [name,bd,dd,cd,rel,cul,gov,titles,claims,nick,num_of_kills,once_owned[0]]
            #we have the data and now is the time to create html files for the encyclopedia
            item[i2]['identity'] = name
            item[i2]['id_local'] = i2
            template = env.get_template('template2.html')
            output2 = template.render(data=chardata,titles=titles_html)
            history = "history\ "
            print('Created history file for: ' + chardata[0] + '...')
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


