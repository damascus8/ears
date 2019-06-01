import MySQLdb as mysqldb

mydb = mysqldb.connect(
    host="localhost",
    user="root",
    passwd="pradnya7",
    database="EARS"
)


def fetchVideoNames():
    mycursor = mydb.cursor()
    videos = [];
    mycursor.execute("SELECT videoName,location FROM SavedVideos order by SrNo desc;")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
        videos.append({"name":x[0],"location":x[1]})
    print(videos)
    mydb.commit()
    return videos


def insertVideoName(newVidName,location):
    mycursor = mydb.cursor()
    query = "INSERT INTO SavedVideos(videoName,location) VALUES(%s,%s)"
    args = (newVidName,location)
    mycursor.execute(query, [newVidName])
    mydb.commit()


if __name__ == '__main__':
    fetchVideoNames()
    # insertVideoName("new my.mp4")
