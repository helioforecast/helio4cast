#distribute_web.py
#for putting the real time results to helioforecast.space every hour

#pip install pysftp

import sys
import os
import pysftp



############### copy to helioforecast.space server



print('------------------ helioforecast.space')
print()


sftp=pysftp.Connection('helioforecast.space', username='weatherman', private_key='/home/cmoestl/.ssh/id_helioweb')

sftp.chdir('helioforecast/static/realtime_plots')  #change dir
print(sftp.pwd)
print('copy predstorm_real.png/txt to ',sftp.pwd) #show current dir
sftp.put('/nas/helio/PREDSTORM/predstorm_real.png')  # upload file to public/ on remote
sftp.put('/nas/helio/PREDSTORM/predstorm_real.txt')  # upload file to public/ on remote

print('copy aurora maps to ',sftp.pwd) #show current dir
sftp.put('/nas/helio/AURORAMAPS/results/aurora_realtime/prob_canada.gif')
sftp.put('/nas/helio/AURORAMAPS/results/aurora_realtime/prob_europe.gif')
sftp.put('/nas/helio/AURORAMAPS/results/aurora_realtime/prob_global.gif')
sftp.put('/nas/helio/AURORAMAPS/results/aurora_realtime/prob_canada_small.gif')
sftp.put('/nas/helio/AURORAMAPS/results/aurora_realtime/prob_europe_small.gif')
sftp.put('/nas/helio/AURORAMAPS/results/aurora_realtime/prob_global_small.gif')
sftp.put('/nas/helio/AURORAMAPS/results/aurora_realtime/prob_canada.mp4')
sftp.put('/nas/helio/AURORAMAPS/results/aurora_realtime/prob_europe.mp4')
sftp.put('/nas/helio/AURORAMAPS/results/aurora_realtime/prob_global.mp4')



#sftp.get('remote_file')         # get a remote file
sftp.close()

print()
print()



############### copy to  chris dropbox


drop=1
import dropbox
from dropbox.files import WriteMode

if drop > 0:

    print('------------------ chris dropbox')
    print()


    print('upload predstorm_real.png/txt and 3 small aurora gifs to my dropbox ')  
   
    db = dropbox.Dropbox('nHTT40xz710AAAAAAAApfE7Qek2_SIPjRfLzLHRuOQ1jz_rtu-0sS-eLRqVU0nLn')
    #print('Account infos: ', db.users_get_current_account())


    fname = '/nas/helio/PREDSTORM/predstorm_real.png'     # Name einer lokalen Datei
    dname = '/predstorm_real.png'  # Name der Datei in Dropbox
    f = open(fname, 'rb')
    response = db.files_upload(f.read(), dname,mode=WriteMode('overwrite'))

    fname = '/nas/helio/PREDSTORM/predstorm_real.txt'     # Name einer lokalen Datei
    dname = '/predstorm_real.txt'  # Name der Datei in Dropbox
    f = open(fname, 'rb')
    response = db.files_upload(f.read(), dname,mode=WriteMode('overwrite'))
    #print('uploaded:', response)
    
    
    fname = '/nas/helio/AURORAMAPS/results/aurora_realtime/prob_global_small.gif'     # Name einer lokalen Datei
    dname = '/prob_global_small.gif'  # Name der Datei in Dropbox
    f = open(fname, 'rb')
    response = db.files_upload(f.read(), dname,mode=WriteMode('overwrite'))
    

    fname = '/nas/helio/AURORAMAPS/results/aurora_realtime/prob_europe_small.gif'     # Name einer lokalen Datei
    dname = '/prob_europe_small.gif'  # Name der Datei in Dropbox
    f = open(fname, 'rb')
    response = db.files_upload(f.read(), dname,mode=WriteMode('overwrite'))
    
    
    fname = '/nas/helio/AURORAMAPS/results/aurora_realtime/prob_canada_small.gif'     # Name einer lokalen Datei
    dname = '/prob_canada_small.gif'  # Name der Datei in Dropbox
    f = open(fname, 'rb')
    response = db.files_upload(f.read(), dname,mode=WriteMode('overwrite'))
    
   
    
    
    f.close()
