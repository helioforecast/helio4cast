#distribute_tweet.py
#for putting the real time results on the @helio4cast twitter account



import sys


#add path for modules
sys.path.insert(0, r'/home/cmoestl/.ssh')
import os
import tweepy
from id_twitter_helio4cast import *
from web_data import *

#tweet only once per day to not overflow twitter timelines

print('------------------ twitter')

#now read modules from my home directory with twitter keys for helio4cast account
#these can be redone on developer.twitter.com
#authenticae
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

print('tweet predstorm_real.png at @helio4cast ')

#tweet predstorm forecast
api.update_with_media(path+'predstorm/predstorm_real.png', status="Current PREDSTORM solar wind forecast near Earth.")



print('make gifs smaller')
output_directory='aurora_realtime'
os.system(ffmpeg_path+' -i '+ path+'auroramaps/results/'+output_directory+'/prob_global.mp4  -b:v 5000k -vf scale=500:-1 '+path+'auroramaps/results/'+output_directory+'/prob_global_very_small.gif  -y -loglevel quiet ')
os.system(ffmpeg_path+' -i '+ path+'auroramaps/results/'+output_directory+'/prob_europe.mp4  -b:v 5000k -vf scale=500:-1 '+path+'auroramaps/results/'+output_directory+'/prob_europe_very_small.gif  -y -loglevel quiet ')
os.system(ffmpeg_path+' -i '+ path+'auroramaps/results/'+output_directory+'/prob_canada.mp4  -b:v 5000k -vf scale=500:-1 '+path+'auroramaps/results/'+output_directory+'/prob_canada_very_small.gif  -y -loglevel quiet')


#Für gifs in guter Auflösung (zB wenn man ein .mpeg in ein .gif konvertieren möchte:
#Zuerst muss man die Farbpalette des movies abspeichern:
#ffmpeg -i 20100203_B_ensemble_movie.mpeg -vf \ fps=15,scale=1000:-1:flags=lanczos, palettegen palette.png

#Und danach:

#ffmpeg -i 20100203_B_ensemble_movie.mpeg -i palette.png -filter_complex "scale=1000:-1:flags=lanczos[x];[x][1:v]paletteuse" ELEvoHI_movie.gif

#os.system(ffmpeg_path+' -i '+ path+'auroramaps/results/'+output_directory+'/prob_global.mp4  -vf fps=25 "scale=1000:-1:flags=lanczos" palettegen'+ path+'auroramaps/results/'+output_directory+'/palette.png ')

#os.system(ffmpeg_path+' -i '+ path+'auroramaps/results/'+output_directory+'/prob_global.mp4 -i '+ path+'auroramaps/results/'+output_directory+'/palette.png -filter_complex "scale=1000:-1:flags=lanczos[x];[x][1:v]paletteuse"        '+path+'auroramaps/results/'+output_directory+'/prob_canada_very_small.gif  -y -loglevel quiet')


print('tweet aurora gifs at @helio4cast ')
api.update_with_media(path+'auroramaps/results/aurora_realtime/prob_global_very_small.gif', status="Current northern hemisphere aurora forecast")
api.update_with_media(path+'auroramaps/results/aurora_realtime/prob_europe_very_small.gif', status="Current Europe aurora forecast")
api.update_with_media(path+'auroramaps/results/aurora_realtime/prob_canada_very_small.gif', status="Current North America aurora forecast")




#for more than one image

# upload images and get media_ids
#filenames = ['/nas/helio/AURORAMAPS/results/aurora_realtime/prob_europe_small.gif']#, '/nas/helio/AURORAMAPS/results/aurora_realtime/prob_canada_small.gif','/nas/helio/AURORAMAPS/results/aurora_realtime/prob_global_small.gif']
#media_ids = []
#for filename in filenames:
#     res = api.media_upload(filename)
#     media_ids.append(res.media_id)

# tweet with multiple images
#api.update_status(status='many images!✨', media_ids=media_ids)


#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    print(tweet.text)



print('done')
print()



