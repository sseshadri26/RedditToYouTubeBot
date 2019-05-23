
import praw

import unicodedata

from PIL import Image, ImageDraw, ImageFont
import textwrap

from gtts import gTTS

import string
from mutagen.mp3 import MP3
import shutil

import cv2
import os

from natsort import natsorted, ns

from pydub import AudioSegment
import ffmpeg
import moviepy.editor as mp
import glob



def makeVid (audioTimes, imageDir, qNum, title):

    #multiplies everything by 10
    audioTimes = [x * 10 for x in audioTimes]


    inBetweenImage = 'static.png'
    video_name = 'res/video' + str(qNum)
    fileType = '.avi'

    imagesTemp = []
    images = []

    for img in os.listdir(imageDir):
        if (img.endswith(".png")):
            imagesTemp.append(img)

    imagesTemp = natsorted(imagesTemp, key=lambda y: y.lower())

    i=0
    for img in imagesTemp:
        if (img.startswith(str(qNum))):
            images.append(img)

        i+=1


    #sort images in natural order


    print(images)

    frame = cv2.imread(os.path.join(imageDir, images[0]))
    height, width, layers = frame.shape


    framerate = 10
    # 1 second for each photo. This means photos must be repeated based on how many seconds their audio takes.

    video = cv2.VideoWriter(video_name + fileType, 0, framerate , (1270, 720))

    # for i in range(0, len[images]):
    #     image = images[i]
    #     video.write(cv2.imread(os.path.join(image_folder, image)))
    #     #video.write(cv2.imread(os.path.join(image_folder, image)))



    i=0
    for image in images:
        for j in range (0, int(audioTimes[i])):
            video.write(cv2.imread(os.path.join(imageDir, image)))
        i+=1

    cv2.destroyAllWindows()
    video.release()
    mergeAudio(video_name, qNum, title)



def mergeAudio(videoFile, qNum, title):

    voicesDir = 'res/voice'
    voices = [img for img in os.listdir(voicesDir) if (img.endswith(".mp3") and img.startswith(str(qNum)))]

    #sort voices in natural order
    voices = natsorted(voices, key=lambda y: y.lower())



    # Concatenation is just adding
    # audioFile = AudioSegment.from_mp3("res/voice/" + voices[0])
    # for l in range (1, len(voices)):
    #     voice = voices[l]
    #     fullAudio+= AudioSegment.from_mp3(voice)

    audioFile = AudioSegment.empty()
    for voice in voices:
        audioFile += AudioSegment.from_mp3("res/voice/" + voice)

    # writing mp3 files is a one liner
    audioFile.export('res/voice' + str(qNum) + '.mp3', format="mp3")

    video = mp.VideoFileClip('res/video' + str(qNum) + '.avi')

    video.write_videofile("res/final/final "+ str(qNum) +".mp4", audio='res/voice' + str(qNum) + '.mp3')

    # cmd = 'ffmpeg -y -i '+audioFile+'  -r 30 -i '+videoFile+'  -filter:a aresample=async=1 -c:a flac -c:v copy av.mkv'
    # subprocess.call(cmd, shell=True)                                     # "Muxing Done
    # print('Mixing Done')

    clearDirs()

    uploadToYouTube(qNum, title)

def uploadToYouTube(qNum, title):
    fileName = 'res/final/final ' + str(qNum)
    title = title.replace("\"", "")
    title = title.replace("\'", "")
    print(title)
    cmd = "python upload_video.py --file='"+fileName+".mp4' --title='Top Ask Reddit of Yesterday' --description='Ask Reddit: "+title+"' --keywords='meme'"
    print(cmd)
    os.system(cmd)

def clearDirs ():
    files = glob.glob('res/images/*')
    for f in files:
        os.remove(f)
    files = glob.glob('res/voice/*')
    for f in files:
        os.remove(f)

def createImages (text, author, imagePrefix):

    audioTimes = []

    text = text.replace("*","")

    screenSize=(1270, 720)
    #print(novo)
    fontSize=40


    font = ImageFont.truetype("Verdana.ttf", fontSize)
    authorFont = ImageFont.truetype("Verdana.ttf", int(fontSize/1.5))


    #text = 'Hello World! This is a bunch of text. Can we get an F in the chat? Wow, much words. The Glasgow Ice Cream Wars - 6 people died in a turf war over ice cream van routes (they were dealing heroin out of the vans). In 2007 a paraglider got trapped in the updraft of two joining thunderstorms and lifted to an altitude of 10 kilometers. She landed 3,5 hours later about 60 kilometers north of her starting position having survived extreme cold, lightning and lack of oxygen. Wow, much words. The Glasgow Ice Cream Wars - 6 people died in a turf war over ice cream van routes (they were dealing heroin out of the vans). In 2007 a paraglider got trapped in the updraft of two joining thunderstorms and lifted to an altitude of 10 kilometers. She landed 3,5 hours later about 60 kilometers north of her starting position having survived extreme cold, lightning and lack of oxygen. Hello World! This is a bunch of text. Can we get an F in the chat? Wow, much words. The Glasgow Ice Cream Wars - 6 people died in a turf war over ice cream van routes (they were dealing heroin out of the vans). In 2007 a paraglider got trapped in the updraft of two joining thunderstorms and lifted to an altitude of 10 kilometers. She landed 3,5 hours later about 60 kilometers north of her starting position having survived extreme cold, lightning and lack of oxygen. Wow, much words. The Glasgow Ice Cream Wars - 6 people died in a turf war over ice cream van routes (they were dealing heroin out of the vans). In 2007 a paraglider got trapped in the updraft of two joining thunderstorms and lifted to an altitude of 10 kilometers. She landed 3,5 hours later about 60 kilometers north of her starting position having survived extreme cold, lightning and lack of oxygen. Hello World! This is a bunch of text. Can we get an F in the chat? Wow, much words. The Glasgow Ice Cream Wars - 6 people died in a turf war over ice cream van routes (they were dealing heroin out of the vans). In 2007 a paraglider got trapped in the updraft of two joining thunderstorms and lifted to an altitude of 10 kilometers. She landed 3,5 hours later about 60 kilometers north of her starting position having survived extreme cold, lightning and lack of oxygen. Wow, much words. The Glasgow Ice Cream Wars - 6 people died in a turf war over ice cream van routes (they were dealing heroin out of the vans). In 2007 a paraglider got trapped in the updraft of two joining thunderstorms and lifted to an altitude of 10 kilometers. She landed 3,5 hours later about 60 kilometers north of her starting position having survived extreme cold, lightning and lack of oxygen. Hello World! This is a bunch of text. Can we get an F in the chat? Wow, much words. The Glasgow Ice Cream Wars - 6 people died in a turf war over ice cream van routes (they were dealing heroin out of the vans). In 2007 a paraglider got trapped in the updraft of two joining thunderstorms and lifted to an altitude of 10 kilometers. She landed 3,5 hours later about 60 kilometers north of her starting position having survived extreme cold, lightning and lack of oxygen. Wow, much words. The Glasgow Ice Cream Wars - 6 people died in a turf war over ice cream van routes (they were dealing heroin out of the vans). In 2007 a paraglider got trapped in the updraft of two joining thunderstorms and lifted to an altitude of 10 kilometers. She landed 3,5 hours later about 60 kilometers north of her starting position having survived extreme cold, lightning and lack of oxygen. Hello World! This is a bunch of text. Can we get an F in the chat? Wow, much words. The Glasgow Ice Cream Wars - 6 people died in a turf war over ice cream van routes (they were dealing heroin out of the vans). In 2007 a paraglider got trapped in the updraft of two joining thunderstorms and lifted to an altitude of 10 kilometers. She landed 3,5 hours later about 60 kilometers north of her starting position having survived extreme cold, lightning and lack of oxygen. Wow, much words. The Glasgow Ice Cream Wars - 6 people died in a turf war over ice cream van routes (they were dealing heroin out of the vans). In 2007 a paraglider got trapped in the updraft of two joining thunderstorms and lifted to an altitude of 10 kilometers. She landed 3,5 hours later about 60 kilometers north of her starting position having survived extreme cold, lightning and lack of oxygen.'
    textArray = textwrap.wrap(text, width=2200/fontSize)

    numberOfLines = screenSize[1]/(fontSize*1.5) - 2


    numberOfFiles = int(len(textArray)/numberOfLines) + 1

    #img_draw.rectangle((70, 50, 270, 200), outline='red', fill='blue')


    j=0
    currentLine = 0

    for j in range (0, numberOfFiles):
        textOnPage=''
        blank_image = Image.new('RGBA', screenSize, 'white')
        img_draw = ImageDraw.Draw(blank_image)


        for k in range (0, int(numberOfLines)):
            if (currentLine==len(textArray)):
                break

            s = textArray[currentLine]
            textOnPage+=' '
            textOnPage+=s
            authorPos=(400, 666)

            textPos = (20, fontSize*1.5* ( (currentLine%numberOfLines) + 1 ))
            img_draw.text(textPos, s, fill='black', font=font, anchor='None')

            img_draw.text(authorPos, author, fill='black', font=authorFont, anchor='None')

            currentLine+=1

        blank_image.save('res/images/' + imagePrefix + '-' + str(j) + ".png")

        audioTimes.append(createVoice(textOnPage, 'res/voice/' + imagePrefix + '-' + str(j) + ".mp3"))

    staticName = 'res/images/' + fileName + '-static.png'

    shutil.copy('res/static.png', staticName)

    staticName = 'res/voice/' + fileName + '-static.mp3'
    shutil.copy('res/static.mp3', staticName)
    audioTimes.append(1.0)
    return audioTimes



def createTitleImage (text, imagePrefix):

    audioTimes = []

    screenSize=(1270, 720)
    #print(novo)
    fontSize=60


    font = ImageFont.truetype("Verdana.ttf", fontSize)
    authorFont = ImageFont.truetype("Verdana.ttf", int(fontSize/1.5))


    textArray = textwrap.wrap(text, width=2200/fontSize)



    blank_image = Image.new('RGBA', screenSize, 'white')
    img_draw = ImageDraw.Draw(blank_image)

    currentLine=0
    for s in textArray:
        textPos = (20, fontSize*1.5* ( (currentLine) + 1 ))
        img_draw.text(textPos, s, fill='black', font=font, anchor='None')
        currentLine+=1

    blank_image.save('res/images/' + imagePrefix + '-0-0-a' + ".png")
    audioTimes.append(createVoice(text, 'res/voice/' + imagePrefix + '-0-0-a' + ".mp3"))

    staticName = 'res/images/' + imagePrefix + '-0-0-static.png'

    shutil.copy('res/static.png', staticName)

    staticName = 'res/voice/' + imagePrefix + '-0-0-static.mp3'
    shutil.copy('res/static.mp3', staticName)
    audioTimes.append(1.0)
    return audioTimes




def createVoice (text, fileName):

    audioTime = 0
    try:
        tts = gTTS(lang = 'en-in', text = text)

        tts.save(fileName)
        audio = MP3(fileName)

        audioTime=audio.info.length
        audioTime = round(audioTime,1)


    except Exception as e:
        tts = gTTS(lang = 'en-in', text = 'm')
        tts.save(fileName)
        audio = MP3(fileName)
        audioTime=audio.info.length
        audioTime = round(audioTime,1)

    return audioTime












##################################################################################################### reddit stuff







# create the objects from the imported modules

# reddit api login
reddit = praw.Reddit(client_id='id, something',
                     client_secret='secret, something',
                     username='gullu2002',
                     password='a password, im not telling you
                     user_agent='r to YT by u/gullu2002')



# the subreddits you want your bot to live on
subreddit = reddit.subreddit('askreddit')
stream = subreddit.stream

# phrase to activate the bot
keyphrase = '!r2YTbot'

topPosts = subreddit.top('day')
gildedPosts = subreddit.gilded()

postIDs = []
postTitles = []
postComments = []

authorNames = []




for submission in topPosts:
    if submission.score>10000:
        #print(submission.title)
        postIDs.append(submission.id)

i=0

for id in postIDs:
    postComments.append([])
    authorNames.append([])


    #print(id)

    post = reddit.submission(id=id)
    print(post.title)

    postTitles.append(post.title)

    post.comment_sort = 'top'
    allComments = post.comments
    charCount = 0
    for comment in allComments:
        if charCount>3000:
            break
        #print(comment.body)
        #print(i)
        #.replace('\u2019', '\'').replace('\n', '\n')
        # print (comment.body)
        # print (type(comment.body))
        # print('')

        ######################################## format the comment

        formattedComment = comment.body
        try:
            authorName = comment.author.name
        except Exception as e:
            authorName = "<deleted>"


        ######################################## format the comment
        postComments[i].append(formattedComment)
        authorNames[i].append(authorName)
        #print(postComments)

        charCount += len(formattedComment)

    i+=1


print('')
print('')
print('')
print('')
print('')
print('')

for i in range (0, len(postComments)):
    questionArray = postComments[i]
    authorArray = authorNames[i]
    audioTimes = []
    audioTimes += createTitleImage(postTitles[i], str(i))
    for j in range(0, len(questionArray)):
        comment = questionArray[j]
        author = authorArray[j]
        fileName = str(i) + '-' + str(j)
        audioTimes += createImages(comment, '- u/' + author, fileName)


    makeVid(audioTimes, 'res/images', i, postTitles[i])




#print(type(postComments[0][0]))

  #print(subreddit.submissions(id).title)
