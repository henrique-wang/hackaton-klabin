""""
This class is used as a reference to get/create a comment properties
"""
class Comment:
    def __init__(self, userID, date, message, comID, area, Smile, score=0):
        self.commentID = comID
        self.userid = userID
        self.date = date
        self.message = message
        self.score = score
        self.area = area
        self.smile = Smile

    def __str__(self):
        string = "comID: {}; userID: {}; date: {}; comment: {}; score: {}; smile: {}".format(
            self.getCommentID(), self.getUserID(), self.getDate(), self.getMessage(), self.getScore(), self.getSmile()
        )
        return string

    def getCommentID(self):
        return self.commentID

    def getUserID(self):
        return self.userid

    def getDate(self):
        return self.date

    def getScore(self):
        return self.score

    def getMessage(self):
        return self.message

    def getArea(self):
        return self.area

    def getSmile(self):
        return self.smile

    def setScore(self, newScore):
        self.score = newScore