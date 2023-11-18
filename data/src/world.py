from .config import *

class World():
    Day = 1
    Month = 1
    Year = 5
    Hour = 0
    Minute = 0
    Second = 0
    Wait_Time = TimeConverter(DB).getTime(0.05)
    def SkipSecond(self):
        self.Wait_Time -= 1
        if self.Wait_Time <= 0:
            self.Second += 1
            self.Wait_Time = TimeConverter(DB).getTime(0.05)
            if self.Second >= 60:
                self.Minute += 1
                self.Second = 0
    def SkipMinute(self):
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
        self.SkipSecond()
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
    
    def GetSeconds(self) -> str:
        h = ''
        if self.Second < 10:
            h = f'0{self.Second}'
        else:
            h = f'{self.Second}'
        return h
    
    def GetTime(self,format:list=['H','M','S']) -> str:
        r = ''
        if 'H' in format:
            IsMinutes = lambda: ':' if 'M' in format else ''
            r += f'{self.GetHour()}{IsMinutes()}'
        if 'M' in format:
            IsSeconds = lambda: ':' if 'S' in format else ''
            r += f'{self.GetMinute()}{IsSeconds()}'
        if 'S' in format:
            r += f'{self.GetSeconds()}'
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

        Alpha_Time_Fix = 6

        Alpha_Hour_Fix = lambda hour: hour if hour < 24 else Alpha_Time_Fix

        Alpha_Percentage = Alpha_Hour_Fix((self.Hour+Alpha_Time_Fix))/24 # Percentage

        Alpha = int(Max * Alpha_Percentage)
        if Alpha >= Max:
            Alpha = Max
        elif Alpha < Min:
            Alpha = Min
        if not (self.Hour > 17):
            Alpha = 0
        if not (self.Hour < 6) and self.Hour > 0:
            Alpha = 0
        return Alpha

    def Load(self,data:dict):
        self.__dict__ = data