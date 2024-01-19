"""
A World System For Control the time of the In Game
"""

from .config import *

class World():
    Day = 1
    Month = 1
    Year = 5
    Hour = 0
    Minute = 0
    Wait_Time = TimeConverter(DB).getTime(0.25)
    def SkipMinute(self):
        self.Wait_Time -= 1
        if self.Wait_Time <= 0:
            self.Minute += 1
            self.Wait_Time = TimeConverter(DB).getTime(0.25)
        if self.Minute >= 60:
            self.Hour += 1
            self.Minute = 0
    def SkipHour(self):
        if self.Hour >= 24:
            self.Day += 1
            self.Hour = 0
    
    def SkipDay(self):
        if self.Day >= 31:
            self.Month += 1
            self.Day = 1
    def SkipMonth(self):
        if self.Month >= 13:
            self.Year += 1
            self.Month = 1
    
    def AutoSkipping(self):
        self.SkipMinute()
        self.SkipHour()
        self.SkipDay()
        self.SkipMonth()

    def GetHour(self) -> str:
        h = ''
        if self.Hour < 10:
            h = f'0{self.Hour}'
        else:
            h = f'{self.Hour}'
        return h

    def GetMinute(self) -> str:
        h = ''
        if self.Minute < 10:
            h = f'0{self.Minute}'
        else:
            h = f'{self.Minute}'
        return h
    
    
    def GetTime(self,format:list=['H','M']) -> str:
        r = ''
        if 'H' in format:
            IsMinutes = lambda: ':' if 'M' in format else ''
            r += f'{self.GetHour()}{IsMinutes()}'
        if 'M' in format:
            r += f'{self.GetMinute()}'
        return r
    
    def GetDate(self,format:list=['D','M','Y']) -> str:
        r = ''
        ToExtra = lambda data: f'0{data}' if data < 10 else data
        if 'D' in format:
            IsMonth = lambda: '/' if 'M' in format else ''
            r += f'{ToExtra(self.Day)}{IsMonth()}'
        if 'M' in format:
            IsYear = lambda: '/' if 'Y' in format else ''
            r += f'{ToExtra(self.Month)}{IsYear()}'
        if 'Y' in format:
            r += f'{ToExtra(self.Year)}'
        return r
    
    def getAlpha(self):
        """Based on hors"""
        Max = 200
        Min = 1

        if self.Hour < 6:
            Alpha_Percentage = 1
        elif self.Hour >= 11:
            if self.Hour >= 17:
                Alpha_Percentage = self.Hour/24
            else:
                Alpha_Percentage = Min/200
        else:
            Alpha_Percentage = Min/200

        Alpha = Max*Alpha_Percentage
        if Alpha < Min:
            Alpha = Min
        
        return Alpha

    def Load(self,data:dict):
        self.__dict__ = data