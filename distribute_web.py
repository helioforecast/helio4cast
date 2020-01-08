#distribute_web.py
#for putting the real time results to helioforecast.space every hour

#pip install pysftp

import sys
import os
import pysftp
from web_data import *


#(1) ############### copy to helioforecast.space server


print('------------------ helioforecast.space')
print()


sftp=pysftp.Connection(server, username=user, private_key=key,port=port)


sftp.chdir('helioforecast/static/realtime_plots')  #change dir
print(sftp.pwd)

print('copy predstorm_real.png/txt to ',sftp.pwd) #show current dir
sftp.put(path+'predstorm/predstorm_real.png')  # upload file to public/ on remote
sftp.put(path+'predstorm/predstorm_real.txt')  # upload file to public/ on remote


print('copy aurora maps to ',sftp.pwd) #show current dir
sftp.put(path+'auroramaps/results/aurora_realtime/prob_canada.gif')
sftp.put(path+'auroramaps/results/aurora_realtime/prob_europe.gif')
sftp.put(path+'auroramaps/results/aurora_realtime/prob_global.gif')
sftp.put(path+'auroramaps/results/aurora_realtime/prob_canada_small.gif')
sftp.put(path+'auroramaps/results/aurora_realtime/prob_europe_small.gif')
sftp.put(path+'auroramaps/results/aurora_realtime/prob_global_small.gif')
sftp.put(path+'auroramaps/results/aurora_realtime/prob_canada.mp4')
sftp.put(path+'auroramaps/results/aurora_realtime/prob_europe.mp4')
sftp.put(path+'auroramaps/results/aurora_realtime/prob_global.mp4')



#sftp.get('remote_file')         # get a remote file
sftp.close()

print()
print()



#(2) ############### copy to  chris dropbox


drop=1
import dropbox
from dropbox.files import WriteMode

if drop > 0:

    print('------------------ chris dropbox')
    print()


    print('upload predstorm_real.png/txt and 3 small aurora gifs to my dropbox ')  
   
    db = dropbox.Dropbox(dropkey)
    #print('Account infos: ', db.users_get_current_account())


    fname = path+'predstorm/predstorm_real.png'     # Name einer lokalen Datei
    dname = '/predstorm_real.png'  # Name der Datei in Dropbox
    f = open(fname, 'rb')
    response = db.files_upload(f.read(), dname,mode=WriteMode('overwrite'))

    fname = path+'predstorm/predstorm_real.txt'    # Name einer lokalen Datei
    dname = '/predstorm_real.txt'  # Name der Datei in Dropbox
    f = open(fname, 'rb')
    response = db.files_upload(f.read(), dname,mode=WriteMode('overwrite'))
    #print('uploaded:', response)
    
    
    fname = path+'auroramaps/results/aurora_realtime/prob_global_small.gif'     # Name einer lokalen Datei
    dname = '/prob_global_small.gif'  # Name der Datei in Dropbox
    f = open(fname, 'rb')
    response = db.files_upload(f.read(), dname,mode=WriteMode('overwrite'))
    

    fname = path+'auroramaps/results/aurora_realtime/prob_europe_small.gif'     # Name einer lokalen Datei
    dname = '/prob_europe_small.gif'  # Name der Datei in Dropbox
    f = open(fname, 'rb')
    response = db.files_upload(f.read(), dname,mode=WriteMode('overwrite'))
    
    
    fname = path+'auroramaps/results/aurora_realtime/prob_canada_small.gif'     # Name einer lokalen Datei
    dname = '/prob_canada_small.gif'  # Name der Datei in Dropbox
    f = open(fname, 'rb')
    response = db.files_upload(f.read(), dname,mode=WriteMode('overwrite'))
    
   
    
    
    f.close()
