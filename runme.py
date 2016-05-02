import pytumblr as py
import csv
import time
import unicodedata
import httplib
import httplib2
import socket
import os
import sqlite3

usual_suspects = (IOError, httplib.HTTPException, httplib2.ServerNotFoundError, socket.error, socket.timeout)

default_timeout = 10

def getClient(credentials):
    f = open(credentials,'rb')
    reader = csv.reader(f)
    rows = []
    for row in reader:
        rows.append(row)
    f.close()
    client = py.TumblrRestClient(rows[1][0],rows[1][1],rows[1][2],rows[1][3])
    client.clientpath = os.path.dirname(os.path.abspath(credentials))
    client.blogname = name(client)
    return client
    
def u_to_s(uni):
    return unicodedata.normalize('NFKD',uni).encode('ascii','ignore')
    
def getFollowers(myblog, waittime = 1, autorestart = True, verbose = False, cutoff = None, timeout = default_timeout, targetBlog = None, blogNumber=0):
    socket.setdefaulttimeout(timeout)
    goahead = False
    while goahead == False:
        try:
            minfo = myblog.info()
            minfo2 = minfo['user']['blogs'][blogNumber]
            if targetBlog == None:
                targetBlog = u_to_s(minfo2['name'])
            n = myblog.followers(targetBlog)['total_users']
            goahead = True
        except usual_suspects:
            goahead = False

    if cutoff != None:
        n = min(n,cutoff)
    m = 20
    rem = n % m
    cycles = n/m
    result = []    
    for i in range(0,cycles):
        if verbose == True:
            print "Trying Blogs {} to {}".format(m*i + 1, m*i + m)
        params = {'offset': m*i, 'limit': m}
        goahead = False
        while goahead == False:
            try:
                time.sleep(waittime)
                tmp = myblog.followers(targetBlog,**params)
                goahead = True
            except usual_suspects:
                goahead = False
        result = result + tmp['users']
    params = {'offset': m*cycles, 'limit': rem}
    if verbose == True:
        print "Finishing..."
    if rem != 0:
        goahead = False
        while goahead == False:
            try:
                time.sleep(waittime)
                tmp = myblog.followers(targetBlog,**params)
                goahead = True
            except usual_suspects:
                goahead = False
        result = result + tmp['users']
    return result

def name(myblog,blogNumber=0):
    goahead = False
    while goahead == False:
        try:
            minfo = myblog.info()
            minfo2 = minfo['user']['blogs'][blogNumber]
            targetBlog = u_to_s(minfo2['name'])
            goahead = True
        except usual_suspects:
            goahead = False
    return targetBlog

def processFollowers(client):
    myfollowers = getFollowers(client)
    n = len(myfollowers)
    mytime = time.time()
    tmptime = time.gmtime(mytime)
    cnx = sqlite3.connect(client.clientpath + "/" + client.blogname + ".db")
    c = cnx.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS data (Year INTEGER, Month INTEGER, Day INTEGER, Hour INTEGER, Minute INTEGER, User TEXT, Idle INTEGER);")
    for i in range(0,n):
        c.execute("INSERT INTO data VALUES (?,?,?,?,?,?,?);", (str(tmptime[0]), str(tmptime[1]), str(tmptime[2]), str(tmptime[3]), str(tmptime[4]), str(u_to_s(myfollowers[i]['name'])), str(mytime - myfollowers[i]['updated'])))
    c.close()
    cnx.commit()
    cnx.close()