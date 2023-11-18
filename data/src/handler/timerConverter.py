

class TimeConverter():
    def __init__(self, DB) -> None:
        self.config = dict(DB.database.get_value('config','data',0))
        self.FPS = self.config['FPS']
        self._define()


    def _define(self):
        self.ONE_SECOND = self.FPS
        self.TWO_SECOND = self.ONE_SECOND*2
        self.ONE_MINUTE = self.TWO_SECOND*30
        self.HALF_SECOND = self.ONE_SECOND//2

    def getTime(self, time:int or float) -> int or float:
        """Time in seconds"""
        time = time * self.FPS
        return time