import requests
import os
import sys
from bs4 import BeautifulSoup
import urllib.request
import subprocess

""""Alrébb megy az adott n számmal, az adott tagtől"""
def Nextelementby(giventag, n):
    for inside in range(n):
        giventag = giventag.next_element
    return giventag

""""Alrébb megy, a kövi siblingre, az adott n számmal, az adott tagtől"""
def Nextsiblingby(giventag, n):
    for inside in range(n):
        # ez azért kell hogy ha nem lenne tesója, ne krepáljon be
        try:
            giventag = giventag.next_sibling
        except:
            giventag = None
            break
    return giventag

"""gets a picture's resolution, from an <img>"""
def picture_resolution(location_in_a_page):
    return "".join([location_in_a_page.attrs["width"],"x",location_in_a_page.attrs["height"]])

"""gets a picture file's size, from file path"""
def picture_size(path_of_pic):
    return"".join([str(os.path.getsize(path_of_pic))," byte"])

"""gets a picture's extension from string"""
def picture_extension(extension):
    return extension[len(extension)-3:]

"""Gets a link, and returns the parsed version, ready to work with"""
def Get_html_by_link(mylink):
    return BeautifulSoup((requests.get(mylink)).text,"lxml")

WIKIPEDIA_ORG="https://hu.wikipedia.org"
WIKIPEDIA_FLAG_ORG="https://hu.wikipedia.org/wiki/F%C3%A1jl:"
WEB_LINK="https:"
"""__________________________________________________________________________________"""
size_of_all_images=0
"""First We get the pilot names, teams, and numbaaz"""
url='https://hu.wikipedia.org/wiki/Formula%E2%80%931'
main_soup=Get_html_by_link(url)

# print(main_soup.find('span',id="Érvényes_rajtszámok").parent)
#this is the first <tr> in the table
# print(Nextsiblingby(main_soup.find('span',id="Érvényes_rajtszámok").parent, 4).find('td',string="1").parent.parent)
LIST_OF_PILOTS=[]
ENGINE_SUPPLIERS=set()
#gets all <tr> in table of érvényes rajtszámok
all_tr_in_table=Nextsiblingby(main_soup.find('span',id="Érvényes_rajtszámok").parent, 4).find('td',string="1").parent.parent.find_all('tr')
for tr_s in all_tr_in_table[1:]:
    #let's find all <td>-s in the actual <tr>
    all_td_in_tr = tr_s.find_all('td')
    # print(all_td_in_tr)
    pilot_number = all_td_in_tr[0].string
    pilot_names = all_td_in_tr[2].string
    print([pilot_names,pilot_number])
    #now let's get the team of pilot, and make a set of teams
    try:
        # pilot_page_url = "".join([WIKIPEDIA_ORG, all_td_in_tr[2].find('a').attrs['href']])
        # this is the page of the current pilot
        pilot_soup = Get_html_by_link("".join([WIKIPEDIA_ORG, all_td_in_tr[2].find('a').attrs['href']]))
        pilot_team_location=pilot_soup.find('b',string="Csapata") or pilot_soup.find('b',string="Korábbi csapatai")
        pilot_teams_location = Nextsiblingby(pilot_team_location.parent, 1).find_all('a')[1]
        # print(pilot_teams.string)
        pilot_team_name=pilot_teams_location.string
        # print(pilot_teams.attrs["href"])
        team_page = Get_html_by_link("".join([WIKIPEDIA_ORG, pilot_teams_location.attrs["href"]]))
        motor_location = team_page.find('b', string="Motor")
        # print(motor_location)
        try:
            motor_location=team_page.find('b', string="Motor")
            # print("found")
            ENGINE_SUPPLIERS.add(motor_location.parent.parent.find('a').attrs["title"])
        except:
            pass
        # print(team_page)
    except:
        # pilot_page_url ="-"
        pilot_team_name="-"
    LIST_OF_PILOTS.append([pilot_names,pilot_number,pilot_team_name])
print(LIST_OF_PILOTS)
print(ENGINE_SUPPLIERS)

"""Next we get the flags, their decription, and their pictures"""
# print(main_soup.find('th',string="Zászló").parent.parent.find_all('tr'))
LIST_OF_FLAGS=[]
flag_trs=main_soup.find('th',string="Zászló").parent.parent.find_all('tr')
for i in range(1,len(flag_trs)):#going through all the <tr>-s, except the first
    #let's get the description of a flag
    all_td=flag_trs[i].find_all('td')
    flag_description=str(all_td[1])
    # print(flag_description)
    badstring = "<br/>"
    flag_description=flag_description.replace(badstring,"")
    flag_description=flag_description[4:len(flag_description) - 6]
    # print(flag_description)
    # now we get all a-s in this particular <td>
    all_a=all_td[0].find_all('a')
    flag_links=[all_a[t].attrs["href"] for t in range(len(all_a))]
    # for t in range(len(all_a)):
    #     entry.append(all_a[t].attrs["href"])
    # print(entry)
    LIST_OF_FLAGS.append([flag_description,flag_links])
# print(LIST_OF_FLAGS) # this contains description of flags, and their links to pictures
#
"""Now let's create the folders we are gonna save into"""
MAIN_FOLDER="The_Thing_JohnCarpenter"
SMOLLER_FOLDER_NoID="UFO"
SMOLLER_FOLDER_ID="Identified"
SMOLLER_FOLDER_FLAGs="Flags"
# if sys.platform =="Windows":
try:
    os.mkdir(MAIN_FOLDER)
except:
    pass
try:
    os.mkdir("".join([MAIN_FOLDER,"/",SMOLLER_FOLDER_FLAGs]))
except:
    pass
try:
    os.mkdir("".join([MAIN_FOLDER,"/",SMOLLER_FOLDER_ID]))
except:
    pass
try:
    os.mkdir("".join([MAIN_FOLDER,"/",SMOLLER_FOLDER_NoID]))
except:
    pass

# elif sys.platform == "Linux":
"""At first let's save flag pictures, and their data"""
# LIST_OF_FLAG_PICTURES=[]
number_of_flagpics=0
for i in range(len(LIST_OF_FLAGS)):
    index=0
    for flag_link in LIST_OF_FLAGS[i][1]:
        # print(flag_link)
        # flag_page_url="".join([WIKIPEDIA_ORG,flag_link])
        flag_soup = Get_html_by_link("".join([WIKIPEDIA_ORG,flag_link]))  # this is the flag picture page
        flag_name=flag_link.replace("/wiki/F%C3%A1jl","")
        search_target="".join(["Fájl",flag_name]).replace("_"," ")
        # print(search_target)
        flag_loc_in_page=flag_soup.find('img',alt=search_target)
        flag_picture_link="".join([WEB_LINK,flag_loc_in_page.attrs["src"]])#this is the download link of flag picture
        # print(flag_picture_link)
        flag_file_path="".join([MAIN_FOLDER,"/",SMOLLER_FOLDER_FLAGs,"/",flag_name[1:len(flag_name)-4],".",picture_extension(flag_picture_link)])
        # flag_file_path = MAIN_FOLDER + "/" + SMOLLER_FOLDER_FLAGs + "/" + flag_name[1:len(flag_name)-4] + ".png"  # location of flag pictures in sxplorer
        # print(flag_file_path)
        urllib.request.urlretrieve(flag_picture_link,flag_file_path)
        flag_resolution=picture_resolution(flag_loc_in_page)
        # print(flag_resolution)
        flag_pic_size=picture_size(flag_file_path)
        size_of_all_images+=os.path.getsize(flag_file_path)
        # print(flag_pic_size)
        flag_pic_extension=picture_extension(flag_picture_link)
        # print(flag_pic_extension)
        LIST_OF_FLAGS[i][1][index]=([flag_link,flag_file_path,flag_resolution,flag_pic_size,flag_pic_extension])
        number_of_flagpics+=1
        index+=1
print(LIST_OF_FLAGS)
        # now, let's save picures, and their attributes
"""At second, let's get every other picture"""
LIST_OF_PICTURES=[]
all_pictures=main_soup.find_all('img',{"class":"thumbimage"})#ez a helye az <img>
index=0
for picture in all_pictures:
    picture_link="".join([WEB_LINK, picture.attrs["src"]])  # this is the download link of picture
    # print((Nextsiblingby(picture.parent,2).contents.split()))#We are searching this for teams', and racers' names
    NoName=True
    for content in Nextsiblingby(picture.parent, 2).contents:
        for pilots in LIST_OF_PILOTS[1:]:
            if pilots[0] in str(content) or pilots[2] in str(content):
                # print(pilots[0]+" "+pilots[2]+" "+str(content))
                NoName=False
        for engine in ENGINE_SUPPLIERS:
            if engine in str(content):
                # print(pilots[0]+" "+pilots[2]+" "+str(content))
                NoName=False
    if NoName:
        pic_file_location="".join([MAIN_FOLDER,"/",SMOLLER_FOLDER_NoID,"/",str(index),".",picture_extension(picture_link)])
        # pic_file_location = MAIN_FOLDER+"/"+SMOLLER_FOLDER_NoID + "/" + str(index) + "." +picture_extension(picture_link)
        # location of flag pictures in sxplorer
    else:
        pic_file_location = "".join([MAIN_FOLDER, "/", SMOLLER_FOLDER_ID, "/", str(index), ".", picture_extension(picture_link)])
        # pic_file_location = MAIN_FOLDER+"/"+SMOLLER_FOLDER_ID + "/" + str(index) + "." +picture_extension(picture_link)
        # location of flag pictures in sxplorer
    index+=1
    urllib.request.urlretrieve(picture_link, pic_file_location)
    pic_resolution = picture_resolution(picture)
    pic_size=picture_size(pic_file_location)
    size_of_all_images+=os.path.getsize(pic_file_location)
    pic_extension=picture_extension(picture_link)
    LIST_OF_PICTURES.append([pic_file_location,pic_resolution,pic_size,pic_extension])
print(LIST_OF_PICTURES)

"""Let'S make that sexy json"""
Fileout = open(MAIN_FOLDER+"/"+"Morphology_1.json", "w",encoding="utf-8")  # open a file to write test outputs into

Fileout.write("drivers:[\n")
for pilot in LIST_OF_PILOTS:
    Fileout.write("\t{\n")
    Fileout.write("\t\t\"driver_name\" : "+pilot[0]+",\n")
    Fileout.write("\t\t\"driver_number\" : " + pilot[1] + ",\n")
    Fileout.write("\t\t\"driver_team\" : " + pilot[2] + ",\n")
    Fileout.write("\t},\n")
Fileout.write("]\n")
Fileout.write("images:[\n")
for flag in LIST_OF_FLAGS:
    for flagpic in flag[1]:
        Fileout.write("\t{\n")
        Fileout.write("\t\t\"image\" : " + flagpic[1] + ",\n")
        Fileout.write("\t\t\"resolution\" : " + flagpic[2] + ",\n")
        Fileout.write("\t\t\"image_size\" : " + flagpic[3] + ",\n")
        Fileout.write("\t\t\"image_extension\" : " + flagpic[4] + ",\n")
        Fileout.write("\t},\n")
for i in range(len(LIST_OF_PICTURES)):
    Fileout.write("\t{\n")
    Fileout.write("\t\t\"image\" : " + LIST_OF_PICTURES[i][0] + ",\n")
    Fileout.write("\t\t\"resolution\" : " + LIST_OF_PICTURES[i][1] + ",\n")
    Fileout.write("\t\t\"image_size\" : " + LIST_OF_PICTURES[i][2] + ",\n")
    Fileout.write("\t\t\"image_extension\" : " + LIST_OF_PICTURES[i][3] + ",\n")
    Fileout.write("\t},\n")
Fileout.write("]\n")
Fileout.write("flag_rules:[\n")
for flag in LIST_OF_FLAGS:
    for flagpic in flag[1]:
        Fileout.write("\t{\n")
        Fileout.write("\t\t\"flag_image\" : " + flagpic[1] + ",\n")
        Fileout.write("\t\t\"description\" : " + flag[0] + ",\n")
        Fileout.write("\t},\n")
Fileout.write("]\n")
Fileout.close()

""" And now the statisticch"""
number_of_drivers=len(LIST_OF_PILOTS)-1
number_of_engine_suppliers=len(ENGINE_SUPPLIERS)
number_of_images=number_of_flagpics+len(LIST_OF_PICTURES)

if "win" in sys.platform:
    subprocess.call(["Statos_bat.bat",str(number_of_drivers),str(number_of_engine_suppliers),str(number_of_images),str(size_of_all_images)],shell=True)
elif sys.platform == "linux":
    subprocess.call(['sh','Statos_bat.sh',str(number_of_drivers),str(number_of_engine_suppliers),str(number_of_images),str(size_of_all_images)])
else:
    print("Unknown platform detected.")