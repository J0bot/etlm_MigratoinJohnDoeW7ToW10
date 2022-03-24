### ETML
### Description : script de migration de Win7 vers Win10
### Auteurs : José Carlos, Ahmad Jano
### Date : 03.03.2022

import json
import os
import uuid
import platform
import shutil
import sqlite3

JSON_EDGE = '{"checksum":"898a10e47fbae1e55ca1acf1f3240ba5","roots":{"bookmark_bar":{"children":[],"date_added":"13290611272933907","date_modified":"13290611281715534","guid":"00000000-0000-4000-a000-000000000002","id":"1","name":"Favorites bar","source":"unknown","type":"folder"},"other":{"children":[],"date_added":"13290611272933909","date_modified":"0","guid":"00000000-0000-4000-a000-000000000003","id":"2","name":"Other favorites","source":"unknown","type":"folder"},"synced":{"children":[],"date_added":"13290611272933910","date_modified":"0","guid":"00000000-0000-4000-a000-000000000004","id":"3","name":"Mobile favorites","source":"unknown","type":"folder"}},"version":1}'

# Fonction qui permet le backup des favoris Firefox
def backupBookmarks():
    
    # Récupération des favoris Firefox de la base de donnée SQLITE (places.sqlite)
    def extractBookmarks(profileName):
        print("Récupération des favoris Firefox en cours...")

        bookmarks = []
        conn = sqlite3.connect(mozPath + "\\" + profileName + "\\places.sqlite")

        query = 'SELECT moz_bookmarks.title, moz_places.url FROM moz_bookmarks INNER JOIN moz_places ON moz_bookmarks.fk = moz_places.id'

        for row in conn.execute(query):
            bookmarks.append({
                "name":row[0],
                "url":row[1],
                "type":"url",
                "show_icon": False 
            })

        conn.close()

        print('Les favoris Firefox ont été extrait.')

        return bookmarks

    # Partie de parse des bookmarks en JSON
    def convertToJSON(bookmarks):
        print('Conversion des favoris en fichier JSON en cours...')

        jsonobj = json.loads(JSON_EDGE)

        for bookmark in bookmarks:
            jsonobj['roots']['bookmark_bar']['children'].append(bookmark)

        f = open("Bookmarks", "w")
        f.write(json.dumps(jsonobj))
        f.close()
        
        print('Conversion réussie !')

    # Trouver le profil Firefox 
    mozPath = os.environ['APPDATA'] + "\\Mozilla\\Firefox\\Profiles"
    for profile in os.listdir(mozPath):
        if (profile.endswith(".default-release")):
            bookmarks = extractBookmarks(profile)
            convertToJSON(bookmarks)
            break # Prendre le premier profil trouvé.

def restoreBookmarks():
    edgePath = os.environ['LOCALAPPDATA'] + '\\Microsoft\\Edge\\User Data\\Default'
    bookmarkPath = edgePath + '\\Bookmarks'

    if os.path.exists(bookmarkPath):
        shutil.copyfile('Bookmarks',bookmarkPath)
        
def backupXnViewData():
    xnviewPath = os.environ['APPDATA'] + '\\XnView'
    xnviewDataPath = os.getcwd() + "xnviewData"
    if os.path.exists(xnviewDataPath):
        shutil.rmtree(xnviewDataPath)
    print("copy from " + xnviewPath + " to "  + xnviewDataPath)
    shutil.copytree(xnviewPath, xnviewDataPath)

def restoreXnViewData():
    xnviewPath = os.environ['APPDATA'] + '\\XnView'
    xnviewDataPath = os.getcwd() + "\\xnviewData"
    if os.path.exists(xnviewPath):
        shutil.rmtree(xnviewPath)
    print("copy from " + xnviewDataPath + " to "  + xnviewPath)
    shutil.copytree(xnviewDataPath, xnviewPath)

def backupData():
    cDataPath = "C:\\DATA"
    cDataDataPath = os.getcwd() + "CDATA"
    if os.path.exists(cDataDataPath):
        shutil.rmtree(cDataDataPath)
    print("copy from " + cDataPath + " to "  + cDataDataPath)
    shutil.copytree(cDataPath, cDataDataPath)

def restoreData():
    cDataPath = "C:\\DATA"
    cDataDataPath = os.getcwd() + "\\CDATA"
    if os.path.exists(cDataPath):
        shutil.rmtree(cDataPath)
    print("copy from " + cDataDataPath + " to "  + cDataPath)
    shutil.copytree(cDataDataPath, cDataPath)

def backupShortcuts():
    desktopPath =  os.environ['USERPROFILE'] + "\\Desktop"
    desktopDataPath = os.getcwd() + "\\desktop_shortcuts"

    if os.path.exists(desktopDataPath):
        shutil.rmtree(desktopDataPath)
    
    os.mkdir(desktopDataPath)

    links = [link for link in os.listdir(desktopPath) if link.endswith('.lnk')]
    for link in links:
        shutil.copy(desktopPath + '\\' + link, desktopDataPath + '\\' + link)

    #print(links)
    print("copy from " + desktopPath + " to "  + desktopDataPath)

def restoreShortcuts():
    desktopPath =  os.environ['USERPROFILE'] + "\\Desktop"
    desktopDataPath = os.getcwd() + "\\desktop_shortcuts"

    links = [link for link in os.listdir(desktopPath) if link.endswith('.lnk')]
    for link in links:
        os.remove(desktopPath + '\\' + link)
    
    links = [link for link in os.listdir(desktopDataPath) if link.endswith('.lnk')]
    for link in links:
        shutil.copy(desktopDataPath + '\\' + link, desktopPath + '\\' + link)

   

    #print(links)
    print("copy from " + desktopDataPath + " to "  + desktopPath)

if 'Server-6.1' in platform.platform():
    #choice = input('Windows 7 detected. Would you like to start migrating Firefox bookmarks (Y|N) ?')
    #if choice == 'Y':
    print('Windows 7 detected.')
    backupBookmarks()
    backupXnViewData()
    backupData()
    backupShortcuts()

else:
    print('Windows 10 detected.')
    restoreBookmarks()
    restoreXnViewData()
    restoreData()
    restoreShortcuts()