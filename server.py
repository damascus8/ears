import flask
from flask import Flask, render_template,send_from_directory

import dbConnection as db
app = Flask(__name__,static_url_path='/static')


@app.route('/')
def videos():
   # videos = ['videos/video1.mp4','videos/video2.webm']
   raw = db.fetchVideoNames()
   # print videos
   listvideos=[]
   print("raw........",raw)
   for video in raw:
       listvideos.append({"url":"videos/" + video["name"],"location":video["location"]})

   # listvideos.append("videos/"+raw[1][0])
   print("listvideos ..... ",listvideos)
   return render_template('index.html', videos = listvideos)


@app.route('/videos/<path>')
def send_js(path):
    # videolist=db.dbConnect()
    # path= videolist[0][0]
    return send_from_directory('videos-to-show',path)

if __name__ == '__main__':
	app.run(debug = True,host="0.0.0.0")
