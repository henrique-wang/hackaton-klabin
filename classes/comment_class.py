""""
This class is used as a reference to get/create a comment properties
"""
class Comment:
    def __init__(self, userID, date, message, comID, point=-1):
        self.commentID = comID
        self.userID = userID
        self.date = date
        self.message = message
        self.point = point

    def __str__(self):
        string = "comID: {}; userID: {}; date: {}; comment: {}; point: {}".format(
            self.getCommentID(), self.getUserID(), self.getDate(), self.getMessage(), self.getPoint()
        )
        return string

    def getCommentID(self):
        return self.commentID

    def getUserID(self):
        return self.userID

    def getDate(self):
        return self.date

    def getPoint(self):
        return self.point

    def getMessage(self):
        return self.message

    def setPoint(self, newPoint):
        self.point = newPoint