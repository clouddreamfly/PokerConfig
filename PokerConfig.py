#!/usr/bin/python
# coding: utf-8

import os
import time
import random
import json
import ConfigParser
import wx



class BaseConfig:
    """configure"""
    
    def __init__(self):

        self.poker_player_count = 2
        self.poker_banker_seat_id = 0
        self.poker_test_count = 0
        self.poker_total_count = 0
        self.poker_pair_count = 1
        self.poker_everyone_count = 14
        self.back_poker_datas = []
        self.player_poker_datas = []
        
    def Reset(self):
        
        self.poker_player_count = 2
        self.poker_banker_seat_id = 0
        self.poker_test_count = 0
        self.poker_total_count = 0
        self.poker_everyone_count = 14
        self.back_poker_datas = []
        self.player_poker_datas = []
        

    def Read(self, path):
        
        config = ConfigParser.ConfigParser()
        try:
            config.readfp(open(path,'r'))
        except:
            print(path, "read error!")
            return False
        
        self.Reset()

        if config.has_section("Options"):

            if config.has_option("Options", "player_count"):
                self.poker_player_count = config.getint("Options", "player_count")                 
                
            if config.has_option("Options", "banker_seat_id"):
                self.poker_banker_seat_id = config.getint("Options", "banker_seat_id")
            
            if config.has_option("Options", "test_count"):
                self.poker_test_count = config.getint("Options", "test_count")
            
            if config.has_option("Options", "total_count"):
                self.poker_total_count = config.getint("Options", "total_count")   
                
            if config.has_option("Options", "pair_count"):
                self.poker_pair_count = config.getint("Options", "pair_count")               
            
            if config.has_option("Options", "everyone_count"):
                self.poker_everyone_count = config.getint("Options", "everyone_count")             
        
        if config.has_section("PokerDatas"):
         
            if config.has_option("PokerDatas","back_poker_datas"):
                poker_datas = config.get("PokerDatas", "back_poker_datas")
                poker_datas = poker_datas.split(",")
                
                for poker_data in poker_datas:
                    if len(poker_data) > 0:
                        self.back_poker_datas.append(int(poker_data, 16))
            
            if self.poker_player_count > 0:
                for seat_id in range(self.poker_player_count):
                    if config.has_option("PokerDatas", "player_poker_datas%d"%(seat_id)):
                        poker_datas = config.get("PokerDatas", "player_poker_datas%d"%(seat_id))
                        poker_datas = poker_datas.split(",")
                        
                        player_poker_datas = []
                        for poker_data in poker_datas:
                            if len(poker_data) > 0:
                                player_poker_datas.append(int(poker_data, 16))
                            
                        self.player_poker_datas.append(player_poker_datas)
                
            
        return True
    
    

    def Write(self, path):
        
        config = ConfigParser.ConfigParser()
        if not config.has_section("Options"):
            config.add_section("Options")

        if not config.has_section("PokerDatas"):
            config.add_section("PokerDatas")
            
        config.set("Options", "player_count", self.poker_player_count)
        config.set("Options", "banker_seat_id", self.poker_banker_seat_id)
        config.set("Options", "test_count", self.poker_test_count)
        config.set("Options", "total_count", self.poker_total_count)
        config.set("Options", "pair_count", self.poker_pair_count)
        config.set("Options", "everyone_count", self.poker_everyone_count)         
        
        back_poker_datas = []
        for poker_data in self.back_poker_datas:
            back_poker_datas.append("0x{:0>2X}".format(poker_data))
        back_poker_datas = ",".join(back_poker_datas)
        config.set("PokerDatas", "back_poker_datas", back_poker_datas)
        
        if self.poker_player_count > 0:
            for seat_id in range(self.poker_player_count):
                if seat_id < len(self.player_poker_datas):
                    one_player_poker_datas = self.player_poker_datas[seat_id]
                    if len(one_player_poker_datas) > 0:
                        poker_datas = []
                        for poker_data in one_player_poker_datas:
                            poker_datas.append("0x{:0>2X}".format(poker_data))
                        one_player_poker_datas = ",".join(poker_datas)
                        config.set("PokerDatas", "player_poker_datas%d"%(seat_id), one_player_poker_datas)

        try:
            config.write(open(path, 'w'))
        except:
            print("wirte error!")
            return False
        
        return True
    

class PokerConfig(BaseConfig):

    def __init__(self):
        
        BaseConfig.__init__(self)
        
    def ReadJson(self, path):
    
        try:
            fp = open(path, 'r')
        except:
            print(path, "open json file error!")
            return False
        
        self.Reset()
        
        config = {}
        with fp:
            try:
                check_bom = fp.read(3)
                if check_bom == '\xef\xbb\xbf':
                    fp.seek(3)
                else:
                    fp.seek(0)
                config = json.load(fp, "utf-8")
            except BaseException as err:
                print("json read error",err)
                return False, err
            
            
        if type(config) == type({}) and len(config) > 0:
            if config.has_key("Options"):
                
                if config["Options"].has_key("player_count"):
                    self.poker_player_count = config["Options"]["player_count"]
                
                if config["Options"].has_key("banker_seat_id"):
                    self.poker_banker_seat_id = config["Options"]["banker_seat_id"]
                    
                if config["Options"].has_key("test_count"):
                    self.poker_test_count = config["Options"]["test_count"]
                    
                if config["Options"].has_key("total_count"):
                    self.poker_total_count = config["Options"]["total_count"]
                    
                if config["Options"].has_key("pair_count"):
                    self.poker_pair_count = config["Options"]["pair_count"]                
                    
                if config["Options"].has_key("everyone_count"):
                    self.poker_everyone_count = config["Options"]["everyone_count"]                        
                
            if config.has_key("PokerDatas"):
                
                if config["PokerDatas"].has_key("back_poker_datas"):
                    poker_datas = config["PokerDatas"]["back_poker_datas"]
                    poker_datas = poker_datas.split(",")
                    
                    for poker_data in poker_datas:
                        if len(poker_data) > 0:                       
                            self.back_poker_datas.append(int(poker_data, 16))   
                        
                if config["PokerDatas"].has_key("player_poker_datas") and len(config["PokerDatas"]["player_poker_datas"]) > 0:
                    if self.poker_player_count > 0:
                        for seat_id in range(self.poker_player_count):
                            if seat_id < len(config["PokerDatas"]["player_poker_datas"]):     
                                poker_datas = config["PokerDatas"]["player_poker_datas"][seat_id]
                                poker_datas = poker_datas.split(",")
                            
                                player_poker_datas = []
                                for poker_data in poker_datas:
                                    if len(poker_data) > 0:
                                        player_poker_datas.append(int(poker_data, 16))
                                    
                                self.player_poker_datas.append(player_poker_datas)                
    
        return True
    
    def WriteJson(self, path):
        
        back_poker_datas = []
        for poker_data in self.back_poker_datas:
            back_poker_datas.append("0x{:0>2X}".format(poker_data))
        back_poker_datas = ",".join(back_poker_datas)
            
        player_poker_datas = []
        if self.poker_player_count > 0:
            for seat_id in range(self.poker_player_count):
                if seat_id < len(self.player_poker_datas):            
                    one_player_poker_datas = self.player_poker_datas[seat_id]
                    if len(one_player_poker_datas) > 0:
                        poker_datas = []
                        for poker_data in one_player_poker_datas:
                            poker_datas.append("0x{:0>2X}".format(poker_data))
                        one_player_poker_datas = ",".join(poker_datas)
                        player_poker_datas.append(one_player_poker_datas)
            
        config = { 
            "Options" : {
                "player_count" : self.poker_player_count,
                "banker_seat_id" : self.poker_banker_seat_id,
                "test_count" : self.poker_test_count,
                "total_count" : self.poker_total_count,
                "pair_count" : self.poker_pair_count,
                "everyone_count": self.poker_everyone_count
            }, 
            "PokerDatas" : {
                "back_poker_datas" : back_poker_datas,
                "player_poker_datas" : player_poker_datas
            } 
        }
        
        try:
            fp = open(path, 'w')
        except:
            print("open json file error!")
            return False
            
        with fp:
            try:
                json.dump(config, fp, indent=4, separators=(',',': '))
            except BaseException as err:
                print("json write error", err)
                return False, err
                
        return True    
    
        
#----------------------------------------------------------------------

class DragShape:
    
    def __init__(self, bmp = None):
        
        self.pos = wx.Point()
        self.shown = True
        self.fullscreen = False
        self.bmp = None
        
    def SetBitmap(self, bmp):
        
        self.bmp = bmp
        
    def SetPos(self, pt):
        
        self.pos = pt
        
    def GetPos(self):
        
        return self.pos
    
    def GetPosX(self):
        
        return self.pos.x
    
    def GetPosY(self):
        
        return self.pos.y
    
    def GetWidth(self):
        
        return self.GetRect().GetWidth()
    
    def GetHeight(self):
        
        return self.GetRect().GetHeight()
    
    def GetSize(self):
        
        return self.GetRect().GetSize()
        
    def GetRect(self):
        
        if self.bmp == None:
            return wx.Rect(self.pos.x, self.pos.y, 1, 1)
        
        return wx.Rect(self.pos.x, self.pos.y, self.bmp.GetWidth(), self.bmp.GetHeight())
    
    def HitTest(self, pt):
        
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)
    

    def Draw(self, dc, op = wx.COPY):
        
        if self.bmp != None and self.bmp.Ok():
            if False:
                dc.DrawBitmap(self.bmp, self.pos.x, self.pos.y, True)
            else:
                mem_dc = wx.MemoryDC()
                mem_dc.SelectObject(self.bmp)
                dc.Blit(self.pos.x, self.pos.y, self.bmp.GetWidth(), self.bmp.GetHeight(), mem_dc, 0, 0, op, True)

            return True
        else:
            return False



POKER_MAX_INDEX = 10 + 10 + 1
POKER_MASK_COLOR = 0xF0
POKER_MASK_VALUE = 0x0F

PokerType_Unknow = 0
PokerType_Heap = 1
PokerType_Left = 2
PokerType_Top = 3
PokerType_Right = 4
PokerType_Bottom = 5



class DragPoker(DragShape):
    
    def __init__(self, poker_data, poker_type = PokerType_Unknow):
        
        DragShape.__init__(self)
        
        self.fullscreen = False
        self.poker_data = 0
        self.poker_type = poker_type
        self.SetPokerData(poker_data)
        
    def  GetPokerData(self):
        
        return self.poker_data
        
    def GetPokerType(self):
        
        return self.poker_type
        
    def SetPokerData(self, poker_data):
        
        try:
            self._SetPokerImage(poker_data)
        except:
            print("set poker image exception!")
            
        self.poker_data = poker_data
        
        
    def _SetPokerImage(self, poker_data):
        
        assert(False)
        pass
        

# 牌堆扑克        
class HeapPoker(DragPoker):
    
    def __init__(self, poker_data):
        
        DragPoker.__init__(self, poker_data, PokerType_Heap)
        

    def _SetPokerImage(self, poker_data):
        
        if self.poker_data == poker_data:
            return 
        
        if poker_data == 0:
            self.SetBitmap(None)
            return
        
        color = (((poker_data & POKER_MASK_COLOR) >> 4) & 0xFF)
        value = ((poker_data & POKER_MASK_VALUE) & 0xFF)
        file_name = 'poker.png'
        if color <= 3 :
            file_name = "poker_%d_%d.png" % (color,  value + 10  if value <=2 else value - 3 )
        elif color == 4: 
            file_name = "poker_%d_%d.png" % (color, value - 13)
        elif color == 5 and value == 0xe:
            file_name =  "poker_back.png"
        
        poker_img = wx.Image('images/normal/%s' % (file_name))
        poker_img = poker_img.Scale(poker_img.GetWidth() * 0.4, poker_img.GetHeight() * 0.4)  
        poker_bmp = wx.EmptyBitmapRGBA(poker_img.GetWidth(), poker_img.GetHeight())
        mem_dc = wx.MemoryDC()
        mem_dc.SelectObject(poker_bmp)  
        mem_dc.DrawBitmap(poker_img.ConvertToBitmap(), 0, 0, True)           
        self.SetBitmap(poker_bmp)        
    
         
# 左边扑克    
class LeftPoker(DragPoker):
    
    def __init__(self, poker_data):
        
        DragPoker.__init__(self, poker_data, PokerType_Left)
    
        
    def _SetPokerImage(self, poker_data):     
    
        if self.poker_data == poker_data:
            return 
        
        if poker_data == 0:
            self.SetBitmap(None)
            return
        
        color = (((poker_data & POKER_MASK_COLOR) >> 4) & 0xFF)
        value = ((poker_data & POKER_MASK_VALUE) & 0xFF)
        file_name = 'poker.png'
        if color <= 3 :
            file_name = "poker_%d_%d.png" % (color,  value + 10  if value <=2 else value - 3 )
        elif color == 4: 
            file_name = "poker_%d_%d.png" % (color, value - 13)
        elif color == 5 and value == 0xe:
            file_name =  "poker_back.png"
        
        poker_img = wx.Image('images/normal/%s' % (file_name))
        poker_img = poker_img.Scale(poker_img.GetWidth() * 0.4, poker_img.GetHeight() * 0.4)  
        poker_bmp = wx.EmptyBitmapRGBA(poker_img.GetWidth(), poker_img.GetHeight())
        mem_dc = wx.MemoryDC()
        mem_dc.SelectObject(poker_bmp)  
        mem_dc.DrawBitmap(poker_img.ConvertToBitmap(), 0, 0, True)
        self.SetBitmap(poker_bmp)
        
        
# 上面扑克
class TopPoker(DragPoker):
    
    def __init__(self, poker_data):
        
        DragPoker.__init__(self, poker_data, PokerType_Top)
        
        
    def _SetPokerImage(self, poker_data):   
        
        if self.poker_data == poker_data:
            return 
        
        if poker_data == 0:
            self.SetBitmap(None)
            return
        
        color = (((poker_data & POKER_MASK_COLOR) >> 4) & 0xFF)
        value = ((poker_data & POKER_MASK_VALUE) & 0xFF)
        file_name = 'poker.png'
        if color <= 3 :
            file_name = "poker_%d_%d.png" % (color,  value + 10  if value <=2 else value - 3 )
        elif color == 4: 
            file_name = "poker_%d_%d.png" % (color, value - 13)
        elif color == 5 and value == 0xe:
            file_name =  "poker_back.png"
        
        poker_img = wx.Image('images/normal/%s' % (file_name))  
        poker_img = poker_img.Scale(poker_img.GetWidth() * 0.4, poker_img.GetHeight() * 0.4)  
        poker_bmp = wx.EmptyBitmapRGBA(poker_img.GetWidth(), poker_img.GetHeight())
        mem_dc = wx.MemoryDC()
        mem_dc.SelectObject(poker_bmp)  
        mem_dc.DrawBitmap(poker_img.ConvertToBitmap(), 0, 0, True)
        self.SetBitmap(poker_bmp)
        
         
# 右边扑克  
class RightPoker(DragPoker):
    
    def __init__(self, poker_data):
        
        DragPoker.__init__(self, poker_data, PokerType_Right)
    
        
    def _SetPokerImage(self, poker_data):   
        
        if self.poker_data == poker_data:
            return 
        
        if poker_data == 0:
            self.SetBitmap(None)
            return
        
        color = (((poker_data & POKER_MASK_COLOR) >> 4) & 0xFF)
        value = ((poker_data & POKER_MASK_VALUE) & 0xFF)
        file_name = 'poker.png'
        if color <= 3 :
            file_name = "poker_%d_%d.png" % (color,  value + 10  if value <=2 else value - 3 )
        elif color == 4: 
            file_name = "poker_%d_%d.png" % (color, value - 13)
        elif color == 5 and value == 0xe:
            file_name =  "poker_back.png"
        
        poker_img = wx.Image('images/normal/%s' % (file_name))  
        poker_img = poker_img.Scale(poker_img.GetWidth() * 0.4, poker_img.GetHeight() * 0.4)  
        poker_bmp = wx.EmptyBitmapRGBA(poker_img.GetWidth(), poker_img.GetHeight())
        mem_dc = wx.MemoryDC()
        mem_dc.SelectObject(poker_bmp)  
        mem_dc.DrawBitmap(poker_img.ConvertToBitmap(), 0, 0, True)
        self.SetBitmap(poker_bmp)
        
      
# 底部扑克   
class BottomPoker(DragPoker):
    
    def __init__(self, poker_data):
        
        DragPoker.__init__(self, poker_data, PokerType_Bottom)
        
        
    def _SetPokerImage(self, poker_data):   
        
        if self.poker_data == poker_data:
            return 
        
        if poker_data == 0:
            self.SetBitmap(None)
            return
        
        color = (((poker_data & POKER_MASK_COLOR) >> 4) & 0xFF)
        value = ((poker_data & POKER_MASK_VALUE) & 0xFF)
        file_name = 'poker.png'
        if color <= 3 :
            file_name = "poker_%d_%d.png" % (color,  value + 10  if value <=2 else value - 3 )
        elif color == 4: 
            file_name = "poker_%d_%d.png" % (color, value - 13)
        elif color == 5 and value == 0xe:
            file_name =  "poker_back.png"
        
        poker_img = wx.Image('images/normal/%s' % (file_name))
        poker_img = poker_img.Scale(poker_img.GetWidth() * 0.5, poker_img.GetHeight() * 0.5)
        poker_bmp = wx.EmptyBitmapRGBA(poker_img.GetWidth(), poker_img.GetHeight())
        mem_dc = wx.MemoryDC()
        mem_dc.SelectObject(poker_bmp)  
        mem_dc.DrawBitmap(poker_img.ConvertToBitmap(), 0, 0, True)
        self.SetBitmap(poker_bmp)
 
 
SeatDirection_Left = 0
SeatDirection_Top = 1
SeatDirection_Right = 2
SeatDirection_Bottom = 3


# 堆立扑克
class PlaneHeapPoker:
    
    def __init__(self, parent, poker_datas = []):
        
        self.parent = parent
        self.shown = True
        self.layout_mode = wx.ALIGN_INVALID
        self.view_rect = wx.Rect()     
        self.display_col_count = 8
        self.poker_views = []
        
        self.InitPokerView(poker_datas)
    
    
    def SetHeapPokers(self, poker_datas):

        poker_count =  len(poker_datas)
        if poker_count > 0:
            for index in range(poker_count):
                poker_data = poker_datas[index]
                if index < len(self.poker_views):
                    self.poker_views[index].SetPokerData(poker_data)
                else:
                    poker_view = HeapPoker(poker_data)
                    self.poker_views.append(poker_view) 
                    self.parent.AddShape(poker_view)
                    
        if len(self.poker_views) > poker_count:
            for index in range(poker_count, len(self.poker_views)):
                self.parent.RemoveShape(self.poker_views[index])
            del self.poker_views[poker_count:]
            

        return True


    def SetHeapMahJong(self, index, poker_data):

        if index < len(self.poker_views):
            self.poker_views[index].SetPokerData(poker_data) 
            return True

        return False

    def GetHeapPokers(self):

        poker_datas = []
        for poker_view in self.poker_views:
            data = poker_view.GetPokerData()
            poker_datas.append(data)

        return poker_datas


    def GetHeapPoker(self, index):

        poker_data = 0
        if index < len(self.poker_views):
            poker_data = self.poker_views[index].GetPokerData()

        return poker_data

    def InitPokerView(self, poker_datas):

        for poker_data in poker_datas:
            poker_view = HeapPoker(poker_data)
            self.poker_views.append(poker_view) 
            self.parent.AddShape(poker_view)  

        self.UpdateView()
        

    def IsShow(self):
        
        return self.shown
    
    def IsHide(self):
        
        return not self.shown
    
    def SetShow(self):
        
        self.shown = True
        
    def SetHide(self):
        
        self.shown =  False
    
    def SetPosition(self, pt, mode = None):
        
        self.view_rect.SetPosition(pt)
        self.layout_mode = mode or self.layout_mode
        self.UpdateView()
        

    def UpdateView(self):

        x = self.view_rect.GetX()
        y = self.view_rect.GetY()
        if self.layout_mode &  wx.ALIGN_CENTER:
            x -= self.view_rect.GetWidth() / 2
            y -= self.view_rect.GetHeight() / 2
        else:
            if self.layout_mode &  wx.ALIGN_CENTER_HORIZONTAL:
                x -= self.view_rect.GetWidth() / 2
            if self.layout_mode &  wx.ALIGN_CENTER_VERTICAL:
                y -= self.view_rect.GetHeight() / 2
                
        h_space = -2
        v_space = -40
        x_count = 0
        y_count = 0
        view_rect =  wx.Rect()
        for poker_view in self.poker_views:
            poker_view.SetPos(wx.Point(x + x_count * (poker_view.GetWidth() + h_space), y + y_count * (poker_view.GetHeight() + v_space)))
            view_rect.Union(poker_view.GetRect())
            x_count += 1
            if x_count >= self.display_col_count:
                x_count = 0
                y_count += 1

        self.view_rect =  view_rect
        self.parent.RefreshRect(self.view_rect)
        
    def Draw(self, dc, op = wx.COPY):
        
        pass        
        
            

INVALID_SEAT_ID = 0xFFFF
NORMAL_POKER_COUNT = 17

# 手上扑克
class HandPoker:
    
    def __init__(self, parent, seat_direction, seat_id = INVALID_SEAT_ID, poker_datas = []):
        
        self.parent = parent
        self.shown = True
        self.seat_id = seat_id
        self.seat_direction = seat_direction
        self.layout_mode = wx.ALIGN_INVALID
        self.view_rect = wx.Rect()
        self.poker_views = []
             
        self.InitPokerView(poker_datas)
            
    def GetSeatDirection(self):
        
        return self.seat_direction
    
    def GetSeatID(self):
        
        return self.seat_id
    
    def SetSeatID(self,  seat_id):
        
        self.seat_id =  seat_id
     
    
    def SetHandPokers(self, poker_datas):
        
        if type(poker_datas) == type([]) and len(poker_datas) > 1:
            poker_datas.sort(reverse=True)
        
        poker_count =  len(poker_datas)
        if poker_count > 0:                
            for index in range(poker_count):
                poker_data = poker_datas[index]
   
                if index < len(self.poker_views):
                    self.poker_views[index].SetPokerData(poker_data)
                else:
                    if self.seat_direction == SeatDirection_Left:
                        poker_view = LeftPoker(poker_data)
                    elif self.seat_direction == SeatDirection_Top:
                        poker_view = TopPoker(poker_data)
                    elif self.seat_direction == SeatDirection_Right:
                        poker_view = RightPoker(poker_data)
                    else:
                        poker_view = BottomPoker(poker_data)                        
                    self.poker_views.append(poker_view) 
                    self.parent.AddShape(poker_view)
                    
        if len(self.poker_views) > poker_count:
            for index in range(poker_count, len(self.poker_views)):
                self.parent.RemoveShape(self.poker_views[index])            
            del self.poker_views[poker_count:]
            
            return True
        
        return False
        
    def SetHandMahJong(self, index, poker_data):
        
        if index < len(self.poker_views):
            self.poker_views[index].SetPokerData(poker_data) 
            return True
        
        return False
    
    def GetHandPokers(self):
        
        poker_datas = []
        for poker_view in self.poker_views:
            data = poker_view.GetPokerData()
            poker_datas.append(data)
        
        if len(poker_datas) > 1:
            random.shuffle(poker_datas)
            
        return poker_datas
    
    
    def GetHandPoker(self, index):
        
        poker_data = 0
        if index < len(self.poker_views):
            poker_data = self.poker_views[index].GetPokerData()
            
        return poker_data
    
    def InitPokerView(self, poker_datas):
        
        if type(poker_datas) == type([]) and len(poker_datas) > 1:
            poker_datas.sort(reverse=True)
            
        if self.seat_direction == SeatDirection_Left:
            self.InitLeftPokerView(poker_datas)
        elif self.seat_direction == SeatDirection_Top:        
            self.InitTopPokerView(poker_datas)
        elif self.seat_direction == SeatDirection_Right:
            self.InitRightPokerView(poker_datas)
        else:
            self.InitBottomPokerView(poker_datas)
            
        self.UpdateView()
            
    
    def InitLeftPokerView(self, poker_datas):
        
        for poker_data in poker_datas:
            poker_view = LeftPoker(poker_data)
            self.poker_views.append(poker_view) 
            self.parent.AddShape(poker_view)  
            
        
    def InitTopPokerView(self, poker_datas):                    
                   
        for poker_data in poker_datas:
            poker_view = TopPoker(poker_data)
            self.poker_views.append(poker_view) 
            self.parent.AddShape(poker_view)  
                
                
    def InitRightPokerView(self, poker_datas):
     
        for poker_data in poker_datas:
            poker_view = RightPoker(poker_data)
            self.poker_views.append(poker_view) 
            self.parent.AddShape(poker_view)  
        
                
    def InitBottomPokerView(self, poker_datas):
        
        for poker_data in poker_datas:
            poker_view = BottomPoker(poker_data)
            self.poker_views.append(poker_view) 
            self.parent.AddShape(poker_view)      
     
    def IsShow(self):
        
        return self.shown
    
    def IsHide(self):
        
        return not self.shown
    
    def SetShow(self):
        
        self.shown = True
        
    def SetHide(self):
        
        self.shown =  False     
            
    def SetPosition(self, pt, mode = None):
        
        self.view_rect.SetPosition(pt)
        self.layout_mode = mode or self.layout_mode
        self.UpdateView()
        
    def GetRect(self):
        
        return self.view_rect
                
    def UpdateView(self):
       
        if self.seat_direction == SeatDirection_Left:
            self.UpdateLeftPokerView()
        elif self.seat_direction == SeatDirection_Top:
            self.UpdateTopPokerView()
        elif self.seat_direction == SeatDirection_Right:
            self.UpdateRightPokerView()
        else:
            self.UpdateBottomPokerView() 
            
        self.parent.RefreshRect(self.view_rect)
        
        
    def UpdateLeftPokerView(self):

        x = self.view_rect.GetX()
        y = self.view_rect.GetY()
        if self.layout_mode &  wx.ALIGN_CENTER_VERTICAL:
            y -= self.view_rect.GetHeight() / 2 
            
        poker_count = len(self.poker_views)
        v_space = (-2 * (poker_count - 16)) if poker_count > 16 else 0
        v_space = v_space if v_space > -6 else -6
        count = 0
        view_rect =  wx.Rect()
        for poker_view in self.poker_views:
            poker_view.SetPos(wx.Point(x, y + count * (poker_view.GetHeight() / 3 + v_space)))
            view_rect.Union(poker_view.GetRect())
            count += 1
            
        self.view_rect =  view_rect
    
        
    def UpdateTopPokerView(self):                    
            
        x = self.view_rect.GetX()
        y = self.view_rect.GetY()
        if self.layout_mode &  wx.ALIGN_CENTER_HORIZONTAL:
            x -= self.view_rect.GetWidth() / 2  
            
        h_space = 0  
        count = 0
        view_rect =  wx.Rect()
        for poker_view in self.poker_views:
            poker_view.SetPos(wx.Point(x + count * (poker_view.GetWidth() / 2 + h_space), y))
            view_rect.Union(poker_view.GetRect())
            count += 1
                
        self.view_rect =  view_rect
                
    def UpdateRightPokerView(self):
     
        x = self.view_rect.GetX()
        y = self.view_rect.GetY()
        if self.layout_mode &  wx.ALIGN_CENTER_VERTICAL:
            y -= self.view_rect.GetHeight() / 2   
            
        poker_count = len(self.poker_views)
        v_space = (-2 * (poker_count - 16)) if poker_count > 16 else 0
        v_space = v_space if v_space > -6 else -6
        count = 0
        view_rect =  wx.Rect()
        for poker_view in self.poker_views:
            poker_view.SetPos(wx.Point(x, y + count * (poker_view.GetHeight() / 3 + v_space)))
            view_rect.Union(poker_view.GetRect())
            count += 1
        
        self.view_rect =  view_rect
                
    def UpdateBottomPokerView(self):   
        
        x = self.view_rect.GetX()
        y = self.view_rect.GetY()
        if self.layout_mode &  wx.ALIGN_CENTER_HORIZONTAL:
            x -= self.view_rect.GetWidth() / 2   
        
        poker_count = len(self.poker_views)
        h_space = (-2 * (poker_count - 16)) if poker_count > 16 else 0
        h_space = h_space if h_space > -20 else -20
        count = 0
        view_rect =  wx.Rect()
        for poker_view in self.poker_views:
            poker_view.SetPos(wx.Point(x + count * (poker_view.GetWidth() / 2 + h_space), y))
            view_rect.Union(poker_view.GetRect())
            count += 1      

        self.view_rect =  view_rect
        
        
    def Draw(self, dc, op = wx.COPY):
        
        pass
        
#----------------------------------------------------------------------

class DragCanvas(wx.Panel):
    
    def __init__(self, parent, ID = -1):
        
        wx.Panel.__init__(self, parent, ID)
        
        self.parent = parent
        self.shapes = []
        self.drag_image = None
        self.drag_shape = None 

        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        self.SetBackgroundStyle(wx.BG_STYLE_ERASE)       
        #self.SetBackgroundColour(wx.Colour(255,255,255))
        
        self.bmp_bg = None
        self.bg_image = wx.Image('images/bg/room_bg.png')
        self.AdjustBackground()

        # init word plate view
        self.InitPokerView()
        self.UpdatePokerView()
        
        # add event
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        
    def InitPokerView(self):
        
        config = self.parent.config

        self.plane_heap_poker = PlaneHeapPoker(self, config.back_poker_datas)
        self.hand_poker_ctrls = []
                    
        seat_directions =  [SeatDirection_Left, SeatDirection_Top,  SeatDirection_Right, SeatDirection_Bottom]
        for seat_direction in seat_directions:
            display = False
            seat_id = INVALID_SEAT_ID
            player_poker_datas = []
            if config.poker_player_count == 1:
                if seat_direction == SeatDirection_Bottom:
                    display = True
                    seat_id =  0
            elif config.poker_player_count == 2:
                if seat_direction == SeatDirection_Top:
                    display = True
                    seat_id = 0
                elif seat_direction == SeatDirection_Bottom:
                    display = True
                    seat_id = 1                    
            elif config.poker_player_count == 3:
                if seat_direction == SeatDirection_Left:
                    display = True
                    seat_id = 0
                elif seat_direction == SeatDirection_Right:
                    display = True
                    seat_id = 1                    
                elif seat_direction == SeatDirection_Bottom:
                    display = True
                    seat_id = 2                    
            elif config.poker_player_count == 4:
                if seat_direction == SeatDirection_Left:
                    display = True
                    seat_id = 0
                elif seat_direction == SeatDirection_Top:
                    display = True
                    seat_id = 1                    
                elif seat_direction == SeatDirection_Right:
                    display = True
                    seat_id = 2                    
                elif seat_direction == SeatDirection_Bottom:
                    display = True
                    seat_id = 3                  
            else:
                display =  False

            if seat_id < len(config.player_poker_datas):   
                player_poker_datas = config.player_poker_datas[seat_id]     
            
            poker_view = HandPoker(self, seat_direction, seat_id, player_poker_datas)
            if display ==  True:
                poker_view.SetShow()
            else:
                poker_view.SetHide()
            self.hand_poker_ctrls.append(poker_view)
                
                
                
    def ResetPokerView(self):
                
        config = self.parent.config
    
        self.plane_heap_poker.SetHeapPokers(config.back_poker_datas)
        self.plane_heap_poker.UpdateView()
        
        for poker_view in self.hand_poker_ctrls:
            display = False
            seat_id = INVALID_SEAT_ID
            player_poker_datas = []
            seat_direction = poker_view.seat_direction
            if config.poker_player_count == 1:
                if seat_direction == SeatDirection_Bottom:
                    display = True
                    seat_id =  0
            elif config.poker_player_count == 2:
                if seat_direction == SeatDirection_Top:
                    display = True
                    seat_id = 0
                elif seat_direction == SeatDirection_Bottom:
                    display = True
                    seat_id = 1                    
            elif config.poker_player_count == 3:
                if seat_direction == SeatDirection_Left:
                    display = True
                    seat_id = 0
                elif seat_direction == SeatDirection_Right:
                    display = True
                    seat_id = 1                    
                elif seat_direction == SeatDirection_Bottom:
                    display = True
                    seat_id = 2                    
            elif config.poker_player_count == 4:
                if seat_direction == SeatDirection_Left:
                    display = True
                    seat_id = 0
                elif seat_direction == SeatDirection_Top:
                    display = True
                    seat_id = 1                    
                elif seat_direction == SeatDirection_Right:
                    display = True
                    seat_id = 2                    
                elif seat_direction == SeatDirection_Bottom:
                    display = True
                    seat_id = 3                  
            else:
                display =  False
                
            if seat_id < len(config.player_poker_datas):   
                player_poker_datas = config.player_poker_datas[seat_id]             
                
            poker_view.SetSeatID(seat_id)
            poker_view.SetHandPokers(player_poker_datas)
            if display == True:
                poker_view.SetShow()
            else:
                poker_view.SetHide()
            poker_view.UpdateView()
                
    def SavePokerViewToConfig(self):
        
        config = self.parent.config
        
        if self.plane_heap_poker.IsShow():
            config.back_poker_datas = self.plane_heap_poker.GetHeapPokers()
        else:
            config.back_poker_datas = []
        
        for poker_view in self.hand_poker_ctrls:
            player_poker_datas = []
            seat_id = poker_view.GetSeatID()
            if poker_view.IsShow():
                player_poker_datas =  poker_view.GetHandPokers()
                
            if seat_id < config.poker_player_count and seat_id < len(config.player_poker_datas):
                config.player_poker_datas[seat_id] = player_poker_datas
        
        if config.poker_test_count <= 0:
            config.poker_test_count = 1
    
    def UpdatePokerView(self):
        
        client_size = self.GetClientSize()
        center_point_x = client_size.GetWidth() / 2
        center_point_y = client_size.GetHeight() / 2 - 10
        if self.parent.config.poker_player_count % 2 == 0:
            heap_center_point_y = center_point_y
        else:
            heap_center_point_y = client_size.GetHeight() / 2 - 160
        self.plane_heap_poker.SetPosition(wx.Point(center_point_x, heap_center_point_y), wx.ALIGN_CENTER)   
        
        for poker_view in self.hand_poker_ctrls:
            if poker_view.seat_direction == SeatDirection_Left:
                poker_view.SetPosition(wx.Point(30, center_point_y + 10), wx.ALIGN_CENTER_VERTICAL)
            elif poker_view.seat_direction == SeatDirection_Top:
                poker_view.SetPosition(wx.Point(center_point_x, 30), wx.ALIGN_CENTER_HORIZONTAL)
            elif poker_view.seat_direction == SeatDirection_Right:
                poker_view.SetPosition(wx.Point(client_size.GetWidth() - poker_view.GetRect().GetWidth() - 30, center_point_y + 10), wx.ALIGN_CENTER_VERTICAL)
            elif poker_view.seat_direction == SeatDirection_Bottom:
                poker_view.SetPosition(wx.Point(center_point_x, client_size.GetHeight() - poker_view.GetRect().GetHeight() - 30), wx.ALIGN_CENTER_HORIZONTAL)
        
        self.Refresh()
        
        
    def AdjustBackground(self):
        
        size = self.GetClientSize()
        bg_size = self.bg_image.GetSize()
        if size.width != 0 and size.height != 0 and size != bg_size:
            image = self.bg_image.Scale(size.width, size.height)
            self.bmp_bg = image.ConvertToBitmap() 
        
        
    def AddShape(self, shape):
        
        is_exist =  False
        for _shape in self.shapes:
            if _shape is shape:
                is_exist =  True
                break
            
        if is_exist == False:
            self.shapes.append(shape)
    
    def RemoveShape(self, shape):
        
        index =  0
        for _shape in self.shapes:
            if _shape is shape:
                del self.shapes[index]
                return True
            
            index += 1
            
        return False
    
        
    def ClearShape(self):
        
        self.shapes =  []
    
    def FindShape(self, pt):
        
        for shape in reversed(self.shapes):
            if shape.HitTest(pt) and shape.shown == True:
                return shape  
            
        return None    
        
    # window size
    def OnSize(self, evt):
        
        self.AdjustBackground()         
        self.UpdatePokerView()
        
        evt.Skip()

    # We're not doing anything here, but you might have reason to.
    # for example, if you were dragging something, you might elect to
    # 'drop it' when the cursor left the window.
    def OnLeaveWindow(self, evt):
        pass


    # tile the background bitmap
    def TileBackground(self, dc):
        
        sz = self.GetClientSize()
        x = 0
        y = 0
        
        if self.bmp_bg != None:
            dc.DrawBitmap(self.bmp_bg, 0, 0, True)


    # Go through our list of shapes and draw them in whatever place they are.
    def DrawShapes(self, dc):
        
        for shape in self.shapes:
            if shape.shown:
                shape.Draw(dc)

    # Clears the background, then redraws it. If the DC is passed, then
    # we only do so in the area so designated. Otherwise, it's the whole thing.
    def OnEraseBackground(self, evt):
        
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        self.TileBackground(dc)

    # Fired whenever a paint event occurs
    def OnPaint(self, evt):
        
        dc = wx.PaintDC(self)
        self.DrawShapes(dc)

    # Left mouse button is down.
    def OnLeftDown(self, evt):

        shape = self.FindShape(evt.GetPosition())
        if shape:
            self.drag_shape = shape
            self.dragStartPos = evt.GetPosition()

    # Left mouse button up.
    def OnLeftUp(self, evt):
        
        if not self.drag_image or not self.drag_shape:
            self.drag_image = None
            self.drag_shape = None
            return

        # Hide the image, end dragging, and nuke out the drag image.
        self.drag_image.Hide()
        self.drag_image.EndDrag()
        self.drag_image = None

        shape = self.FindShape(evt.GetPosition())
        if shape:        
            poker_data1 = shape.GetPokerData()
            poker_data2 = self.drag_shape.GetPokerData()
            shape.SetPokerData(poker_data2)
            self.drag_shape.SetPokerData(poker_data1)
    
            self.drag_shape.shown = True      
            self.RefreshRect(shape.GetRect())
            self.RefreshRect(self.drag_shape.GetRect())
            self.drag_shape = None            
        else:
            self.drag_shape.shown = True
            self.RefreshRect(self.drag_shape.GetRect())
            self.drag_shape = None


    # The mouse is moving
    def OnMotion(self, evt):
        # Ignore mouse movement if we're not dragging.
        if not self.drag_shape or not evt.Dragging() or not evt.LeftIsDown():
            return

        # if we have a shape, but haven't started dragging yet
        if self.drag_shape and not self.drag_image:

            # only start the drag after having moved a couple pixels
            tolerance = 2
            pt = evt.GetPosition()
            dx = abs(pt.x - self.dragStartPos.x)
            dy = abs(pt.y - self.dragStartPos.y)
            if dx <= tolerance and dy <= tolerance:
                return

            # refresh the area of the window where the shape was so it
            # will get erased.
            self.drag_shape.shown = False
            self.RefreshRect(self.drag_shape.GetRect(), True)
            self.Update()

            self.drag_image = wx.DragImage(self.drag_shape.bmp, wx.StockCursor(wx.CURSOR_HAND))
            hotspot = self.dragStartPos - self.drag_shape.pos
            self.drag_image.BeginDrag(hotspot, self, self.drag_shape.fullscreen)
            self.drag_image.Show()
            self.drag_image.Move(pt)
    
        elif self.drag_shape and self.drag_image:
            
            # move drag image to position
            self.drag_image.Move(evt.GetPosition())
            
    
    
class PokerSettingDlg(wx.Dialog):
    
    def __init__(self, parent = None, id = -1,):
        
        wx.Dialog.__init__(self, parent, id, title=u"扑克设置", size=(720, 520))
        
        self.parent = parent
        self.panel = wx.Panel(self)
        frame_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.panel.SetSizer(frame_sizer)        
        
        static_box = wx.StaticBox(self.panel, label=u"扑克游戏配置：")
        static_box_sizer = wx.StaticBoxSizer(static_box, orient=wx.HORIZONTAL)
        frame_sizer.Add(static_box_sizer, 1, wx.LEFT|wx.RIGHT|wx.EXPAND, 4)
        
        label_poker_total_count = wx.StaticText(static_box, label = u"扑克总数目：")
        self.spin_poker_total_count = wx.SpinCtrl(static_box, value='54', size=(50,-1))    
        self.spin_poker_total_count.SetRange(0, 55 * 6)
        self.spin_poker_total_count.SetValue(54)
        self.spin_poker_total_count.Disable()
        static_box_sizer.Add(label_poker_total_count, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 4)
        static_box_sizer.Add(self.spin_poker_total_count, 0, wx.ALIGN_CENTER_VERTICAL)
        static_box_sizer.AddSpacer(8)
        
        label_poker_pair_count = wx.StaticText(static_box, label = u"扑克副数：")
        self.spin_poker_pair_count = wx.SpinCtrl(static_box, value='1', size=(36,-1))    
        self.spin_poker_pair_count.SetRange(1, 6)
        self.spin_poker_pair_count.SetValue(1)
        static_box_sizer.Add(label_poker_pair_count, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 4)
        static_box_sizer.Add(self.spin_poker_pair_count, 0, wx.ALIGN_CENTER_VERTICAL)
        static_box_sizer.AddSpacer(8)        
        
        label_poker_player_count = wx.StaticText(static_box, label = u"游戏人数：")
        self.spin_poker_player_count = wx.SpinCtrl(static_box, value='4', size=(36,-1))    
        self.spin_poker_player_count.SetRange(2, 4)
        self.spin_poker_player_count.SetValue(4)
        static_box_sizer.Add(label_poker_player_count, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 4)
        static_box_sizer.Add(self.spin_poker_player_count, 0, wx.ALIGN_CENTER_VERTICAL)
        static_box_sizer.AddSpacer(8)
        
        label_poker_everyone_count = wx.StaticText(static_box, label = u"每人牌数：")
        self.choice_poker_everyone_count = wx.Choice(static_box, size=(40,-1), choices= ['14', '15', '16', '17', '18', '19', '20'])    
        self.choice_poker_everyone_count.Select(0)
        static_box_sizer.Add(label_poker_everyone_count, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 4)
        static_box_sizer.Add(self.choice_poker_everyone_count, 0, wx.ALIGN_CENTER_VERTICAL)
        static_box_sizer.AddSpacer(8)        
        
        label_poker_banker_seat_id = wx.StaticText(static_box, label = u"庄家座位：")
        self.spin_poker_banker_seat_id = wx.SpinCtrl(static_box, value='0', size=(36,-1))    
        self.spin_poker_banker_seat_id.SetRange(0, 3)
        self.spin_poker_banker_seat_id.SetValue(0)
        static_box_sizer.Add(label_poker_banker_seat_id, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 4)
        static_box_sizer.Add(self.spin_poker_banker_seat_id, 0, wx.ALIGN_CENTER_VERTICAL)
        static_box_sizer.AddSpacer(8)
        
        label_poker_test_count = wx.StaticText(static_box, label = u"测试次数：")
        self.spin_poker_test_count = wx.SpinCtrl(static_box, value='1', size=(60,-1))    
        self.spin_poker_test_count.SetRange(0, 1000)
        self.spin_poker_test_count.SetValue(1)
        static_box_sizer.Add(label_poker_test_count, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 4)
        static_box_sizer.Add(self.spin_poker_test_count, 0, wx.ALIGN_CENTER_VERTICAL)          
        
        
        static_box1 = wx.StaticBox(self.panel, label=u"扑克数目配置：")
        static_box_sizer1 = wx.StaticBoxSizer(static_box1, orient=wx.VERTICAL)
        frame_sizer1_1 = wx.BoxSizer(orient=wx.HORIZONTAL)
        frame_sizer1_2 = wx.BoxSizer(orient=wx.HORIZONTAL)
        frame_sizer1_3 = wx.BoxSizer(orient=wx.HORIZONTAL)
        frame_sizer1_4 = wx.BoxSizer(orient=wx.HORIZONTAL)
        frame_sizer1_5 = wx.BoxSizer(orient=wx.HORIZONTAL)
        frame_sizer1_6 = wx.BoxSizer(orient=wx.HORIZONTAL)
        frame_sizer1_56 = wx.BoxSizer(orient=wx.HORIZONTAL)
        static_box_sizer1.AddSpacer(8)
        static_box_sizer1.Add(frame_sizer1_1)
        static_box_sizer1.AddSpacer(8)
        static_box_sizer1.Add(frame_sizer1_2)
        static_box_sizer1.AddSpacer(8)
        static_box_sizer1.Add(frame_sizer1_3)
        static_box_sizer1.AddSpacer(8)
        static_box_sizer1.Add(frame_sizer1_4)
        static_box_sizer1.AddSpacer(8)
        frame_sizer1_56.Add(frame_sizer1_5)
        frame_sizer1_56.AddSpacer(168)
        frame_sizer1_56.Add(frame_sizer1_6)    
        static_box_sizer1.Add(frame_sizer1_56)        
        static_box_sizer1.AddSpacer(6)
        frame_sizer.Add(static_box_sizer1, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 6)
        
        label_poker_type_diamond  = wx.StaticText(static_box1, label = u"方块\n扑克：")
        label_poker_type_club = wx.StaticText(static_box1, label = u"梅花\n扑克：")        
        label_poker_type_heart  = wx.StaticText(static_box1, label = u"红桃\n扑克：")
        label_poker_type_spade = wx.StaticText(static_box1, label = u"黑桃\n扑克：")
        label_poker_type_king = wx.StaticText(static_box1, label = u"王牌\n扑克：")
        label_poker_type_magic = wx.StaticText(static_box1, label = u"癞子\n扑克：")
        font = label_poker_type_diamond.GetFont()
        font.SetPointSize(10) 
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        label_poker_type_diamond.SetFont(font)
        label_poker_type_club.SetFont(font)
        label_poker_type_heart.SetFont(font)
        label_poker_type_spade.SetFont(font)
        label_poker_type_king.SetFont(font)
        label_poker_type_magic.SetFont(font)
        frame_sizer1_1.Add(label_poker_type_diamond, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 4)
        frame_sizer1_2.Add(label_poker_type_club, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 4)
        frame_sizer1_3.Add(label_poker_type_heart, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 4)
        frame_sizer1_4.Add(label_poker_type_spade, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 4)
        frame_sizer1_5.Add(label_poker_type_king, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 4)
        frame_sizer1_6.Add(label_poker_type_magic, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 4)

        self.poker_diamond_list = []
        self.poker_club_list = []
        self.poker_heart_list = []
        self.poker_spade_list = []
        self.poker_king_list = []     
        self.poker_magic_list = []
        
        for i in range(13):
        
            file_name = "smallpoker_%d.png" % (i+1)
            poker_img = wx.Image('images/tiny/%s' % (file_name))
            poker_bmp = self.ImageMerge(poker_img)            
            img_poker = wx.StaticBitmap(static_box1, bitmap=poker_bmp)
            spin_poker_count = wx.SpinCtrl(static_box1, size=(poker_bmp.GetWidth() + 6,-1), value='4', min=0, max=4)
            self.poker_diamond_list.append({"image": img_poker, "poker_data": i+1, "poker_count": spin_poker_count})
            poker_sizer = wx.BoxSizer(orient=wx.VERTICAL)
            poker_sizer.Add(img_poker, 0, wx.CENTER)
            poker_sizer.Add(spin_poker_count, 0, wx.CENTER)
            frame_sizer1_1.Add(poker_sizer)
            frame_sizer1_1.AddSpacer(10)
            
            file_name = "smallpoker_%d.png" % (0x10+i+1)
            poker_img = wx.Image('images/tiny/%s' % (file_name))
            poker_bmp = self.ImageMerge(poker_img)               
            img_poker = wx.StaticBitmap(static_box1, bitmap=poker_bmp)
            spin_poker_count = wx.SpinCtrl(static_box1, size=(poker_bmp.GetWidth() + 6,-1), value='4', min=0, max=4)
            self.poker_club_list.append({"image": img_poker, "poker_data": 0x10+i+1, "poker_count": spin_poker_count})
            poker_sizer = wx.BoxSizer(orient=wx.VERTICAL)
            poker_sizer.Add(img_poker, 0, wx.CENTER)
            poker_sizer.Add(spin_poker_count, 0, wx.CENTER)
            frame_sizer1_2.Add(poker_sizer)
            frame_sizer1_2.AddSpacer(10)
            
            file_name = "smallpoker_%d.png" % (0x20+i+1)
            poker_img = wx.Image('images/tiny/%s' % (file_name))
            poker_bmp = self.ImageMerge(poker_img)               
            img_poker = wx.StaticBitmap(static_box1, bitmap=poker_bmp)
            spin_poker_count = wx.SpinCtrl(static_box1, size=(poker_bmp.GetWidth() + 6,-1), value='4', min=0, max=4)
            self.poker_heart_list.append({"image": img_poker, "poker_data": 0x20+i+1, "poker_count": spin_poker_count})
            poker_sizer = wx.BoxSizer(orient=wx.VERTICAL)
            poker_sizer.Add(img_poker, 0, wx.CENTER)
            poker_sizer.Add(spin_poker_count, 0, wx.CENTER)
            frame_sizer1_3.Add(poker_sizer)
            frame_sizer1_3.AddSpacer(10)
            
            file_name = "smallpoker_%d.png" % (0x30+i+1)
            poker_img = wx.Image('images/tiny/%s' % (file_name))
            poker_bmp = self.ImageMerge(poker_img)               
            img_poker = wx.StaticBitmap(static_box1, bitmap=poker_bmp)
            spin_poker_count = wx.SpinCtrl(static_box1, size=(poker_bmp.GetWidth() + 6,-1), value='4', min=0, max=4)
            self.poker_spade_list.append({"image": img_poker, "poker_data": 0x30+i+1, "poker_count": spin_poker_count})
            poker_sizer = wx.BoxSizer(orient=wx.VERTICAL)
            poker_sizer.Add(img_poker, 0, wx.CENTER)
            poker_sizer.Add(spin_poker_count, 0, wx.CENTER)
            frame_sizer1_4.Add(poker_sizer)
            frame_sizer1_4.AddSpacer(10)            

        for i in range(2):
            file_name = "smallpoker_%d.png" % (0x4e+i)
            poker_img = wx.Image('images/tiny/%s' % (file_name))
            poker_bmp = self.ImageMerge(poker_img)               
            img_poker = wx.StaticBitmap(static_box1, bitmap=poker_bmp)
            spin_poker_count = wx.SpinCtrl(static_box1, size=(poker_bmp.GetWidth() + 6,-1), value='0', min=0, max=4)
            self.poker_king_list.append({"image": img_poker, "poker_data": 0x4e+i, "poker_count": spin_poker_count})
            poker_sizer = wx.BoxSizer(orient=wx.VERTICAL)
            poker_sizer.Add(img_poker, 0, wx.CENTER)
            poker_sizer.Add(spin_poker_count, 0, wx.CENTER)
            frame_sizer1_5.Add(poker_sizer)
            frame_sizer1_5.AddSpacer(i == 0 and 52 or 10)  

        for i in range(1):
            file_name = "smallpoker_back.png" 
            poker_img = wx.Image('images/tiny/%s' % (file_name))
            poker_bmp = self.ImageMerge(poker_img)               
            img_poker = wx.StaticBitmap(static_box1, bitmap=poker_bmp)
            spin_poker_count = wx.SpinCtrl(static_box1, size=(poker_bmp.GetWidth() + 6,-1), value='0', min=0, max=4)
            self.poker_magic_list.append({"image": img_poker, "poker_data": 0x5e, "poker_count": spin_poker_count})
            poker_sizer = wx.BoxSizer(orient=wx.VERTICAL)
            poker_sizer.Add(img_poker, 0, wx.CENTER)
            poker_sizer.Add(spin_poker_count, 0, wx.CENTER)
            frame_sizer1_6.Add(poker_sizer)
            frame_sizer1_6.AddSpacer(10)       
            
        
        self.check_all_poker_diamond = wx.CheckBox(static_box1, label=u"全选", style=wx.CHK_3STATE)
        self.check_all_poker_club = wx.CheckBox(static_box1, label=u"全选", style=wx.CHK_3STATE)
        self.check_all_poker_heart = wx.CheckBox(static_box1, label=u"全选", style=wx.CHK_3STATE)
        self.check_all_poker_spade = wx.CheckBox(static_box1, label=u"全选", style=wx.CHK_3STATE)
        self.check_all_poker_king = wx.CheckBox(static_box1, label=u"全选", style=wx.CHK_3STATE)
        self.check_all_poker_magic = wx.CheckBox(static_box1, label=u"全选", style=wx.CHK_3STATE)
        self.check_all_poker_diamond.Set3StateValue(wx.CHK_CHECKED)
        self.check_all_poker_club.Set3StateValue(wx.CHK_CHECKED)
        self.check_all_poker_heart.Set3StateValue(wx.CHK_UNCHECKED)       
        self.check_all_poker_spade.Set3StateValue(wx.CHK_CHECKED)
        self.check_all_poker_king.Set3StateValue(wx.CHK_CHECKED)
        self.check_all_poker_magic.Set3StateValue(wx.CHK_UNCHECKED)         
        frame_sizer1_1.Add(self.check_all_poker_diamond, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 2)
        frame_sizer1_2.Add(self.check_all_poker_club, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 2)
        frame_sizer1_3.Add(self.check_all_poker_heart, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 2)        
        frame_sizer1_4.Add(self.check_all_poker_spade, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 2)
        frame_sizer1_5.Add(self.check_all_poker_king, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 2)
        frame_sizer1_6.Add(self.check_all_poker_magic, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 2)    
        
        self.UpdateSettings()
        self.UpdatePokerTotalCount()
        
        
        # 控件事件绑定
        self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinPokerTotalCount, self.spin_poker_total_count)
        self.Bind(wx.EVT_TEXT, self.OnChangeSpinPokerTotalCount, self.spin_poker_total_count) 
        
        self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinPokerPairCount, self.spin_poker_pair_count)
        self.Bind(wx.EVT_TEXT, self.OnChangeSpinPokerPairCount, self.spin_poker_pair_count)         
        
        self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinValue, self.spin_poker_player_count)
        self.Bind(wx.EVT_TEXT, self.OnChangeSpinValue, self.spin_poker_player_count)        
        self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinValue, self.spin_poker_banker_seat_id)
        self.Bind(wx.EVT_TEXT, self.OnChangeSpinValue, self.spin_poker_banker_seat_id)      
        self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinValue, self.spin_poker_test_count)
        self.Bind(wx.EVT_TEXT, self.OnChangeSpinValue, self.spin_poker_test_count)
        
        self.Bind(wx.EVT_CHOICE, self.OnChoiceValue, self.choice_poker_everyone_count)
        
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, self.check_all_poker_diamond) 
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, self.check_all_poker_club)  
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, self.check_all_poker_heart) 
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, self.check_all_poker_spade)  
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, self.check_all_poker_king)        
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox, self.check_all_poker_magic)   
        
        for poker_ctrl in self.poker_diamond_list:
            self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinPokerTotalCount, poker_ctrl["poker_count"])
            self.Bind(wx.EVT_TEXT, self.OnChangeSpinPokerTotalCount, poker_ctrl["poker_count"]) 
        for poker_ctrl in self.poker_club_list:
            self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinPokerTotalCount, poker_ctrl["poker_count"])
            self.Bind(wx.EVT_TEXT, self.OnChangeSpinPokerTotalCount, poker_ctrl["poker_count"]) 
        for poker_ctrl in self.poker_heart_list:
            self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinPokerTotalCount, poker_ctrl["poker_count"])
            self.Bind(wx.EVT_TEXT, self.OnChangeSpinPokerTotalCount, poker_ctrl["poker_count"]) 
        for poker_ctrl in self.poker_spade_list:
            self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinPokerTotalCount, poker_ctrl["poker_count"])
            self.Bind(wx.EVT_TEXT, self.OnChangeSpinPokerTotalCount, poker_ctrl["poker_count"]) 
        for poker_ctrl in self.poker_king_list:
            self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinPokerTotalCount, poker_ctrl["poker_count"])
            self.Bind(wx.EVT_TEXT, self.OnChangeSpinPokerTotalCount, poker_ctrl["poker_count"])                     
        for poker_ctrl in self.poker_magic_list:
            self.Bind(wx.EVT_SPINCTRL, self.OnSelectedSpinPokerTotalCount, poker_ctrl["poker_count"])
            self.Bind(wx.EVT_TEXT, self.OnChangeSpinPokerTotalCount, poker_ctrl["poker_count"])         
   
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        
    def ImageMerge(self, poker_img):
        
        poker_img = poker_img.Scale(poker_img.GetWidth() * 0.85, poker_img.GetHeight() * 0.85)  

        return poker_img.ConvertToBitmap()        
    
    
    def UpdateSettings(self):
        
        self.spin_poker_player_count.SetValue(self.parent.config.poker_player_count)
        self.parent.config.poker_player_count = self.spin_poker_player_count.GetValue()
        if self.parent.config.poker_player_count > 0:
            self.spin_poker_banker_seat_id.SetRange(0, self.parent.config.poker_player_count - 1)
        else:
            self.spin_poker_banker_seat_id.SetRange(0, 0)
        
        if self.parent.config.poker_banker_seat_id >= self.spin_poker_player_count:
            self.parent.config.poker_banker_seat_id = self.spin_poker_player_count - 1
        self.spin_poker_banker_seat_id.SetValue(self.parent.config.poker_banker_seat_id)
        self.parent.config.poker_banker_seat_id = self.spin_poker_banker_seat_id.GetValue()
        
        self.spin_poker_test_count.SetValue(self.parent.config.poker_test_count if self.parent.config.poker_test_count != 0 else 1)
        self.parent.config.poker_test_count = self.spin_poker_test_count.GetValue()
        
        select_index = 0
        select_values = []        
        chioce_values = [i for i in range(14, 109)]
        if self.parent.config.poker_everyone_count not in chioce_values:
            self.parent.config.poker_everyone_count = chioce_values[0]
            
        for index in range(len(chioce_values)):
            select_values.append(str(chioce_values[index]))
            if chioce_values[index] == self.parent.config.poker_everyone_count:
                select_index = index
        self.choice_poker_everyone_count.SetItems(select_values)
        self.choice_poker_everyone_count.Select(select_index)
        
        self.spin_poker_pair_count.SetValue(self.parent.config.poker_pair_count if self.parent.config.poker_pair_count != 0 else 1)
        self.parent.config.poker_pair_count = self.spin_poker_pair_count.GetValue()
        
        poker_datas = []
        for poker_data in self.parent.config.back_poker_datas:
            poker_datas.append(poker_data)
                
        for player_poker_datas in self.parent.config.player_poker_datas:
            for poker_data in player_poker_datas:
                poker_datas.append(poker_data)              
            
        for poker_control in self.poker_diamond_list:
            poker_control["poker_count"].SetValue(self.GetPokerCount(poker_datas, poker_control["poker_data"]))
                
        for poker_control in self.poker_club_list:
            poker_control["poker_count"].SetValue(self.GetPokerCount(poker_datas, poker_control["poker_data"])) 
                
        for poker_control in self.poker_heart_list:
            poker_control["poker_count"].SetValue(self.GetPokerCount(poker_datas, poker_control["poker_data"]))  
                
        for poker_control in self.poker_spade_list:
            poker_control["poker_count"].SetValue(self.GetPokerCount(poker_datas, poker_control["poker_data"])) 
                
        for poker_control in self.poker_king_list:
            poker_control["poker_count"].SetValue(self.GetPokerCount(poker_datas, poker_control["poker_data"]))                                   
                
        for poker_control in self.poker_magic_list:
            poker_control["poker_count"].SetValue(self.GetPokerCount(poker_datas, poker_control["poker_data"]))
                
                
    @staticmethod
    def GetPokerCount(poker_datas, poker_data):
        
        poker_count = 0
        for data in poker_datas:
            if data == poker_data:
                poker_count += 1
                
        return poker_count
    
    def GetPokerDatas(self):
        
        poker_datas = []
        for poker_control in self.poker_diamond_list:
            if poker_control["poker_count"].GetValue() > 0:
                for index in range(poker_control["poker_count"].GetValue()):
                    poker_datas.append(poker_control["poker_data"])
                    
        for poker_control in self.poker_club_list:
            if poker_control["poker_count"].GetValue() > 0:
                for index in range(poker_control["poker_count"].GetValue()):
                    poker_datas.append(poker_control["poker_data"])
                                
        for poker_control in self.poker_heart_list:
            if poker_control["poker_count"].GetValue() > 0:
                for index in range(poker_control["poker_count"].GetValue()):
                    poker_datas.append(poker_control["poker_data"])
                    
        for poker_control in self.poker_spade_list:
            if poker_control["poker_count"].GetValue() > 0:
                for index in range(poker_control["poker_count"].GetValue()):
                    poker_datas.append(poker_control["poker_data"])                                            
                
        for poker_control in self.poker_king_list:
            if poker_control["poker_count"].GetValue() > 0:
                for index in range(poker_control["poker_count"].GetValue()):
                    poker_datas.append(poker_control["poker_data"])   
                
        for poker_control in self.poker_magic_list:
            if poker_control["poker_count"].GetValue() > 0:
                for index in range(poker_control["poker_count"].GetValue()):
                    poker_datas.append(poker_control["poker_data"])
                
        return poker_datas
    
    
    def AdjustPokerDatas(self, poker_datas):
        
        config = self.parent.config
        
        if len(poker_datas) > 0:
            random.shuffle(poker_datas)
        
        config.back_poker_datas = []
        config.player_poker_datas = []
        if config.poker_player_count > 0:
            
            for seat_id in range(config.poker_player_count):
                poker_count = config.poker_everyone_count
                if len(poker_datas) >= poker_count: 
                    player_poker_datas = poker_datas[0 : poker_count]
                    del poker_datas[0 : poker_count]
                    config.player_poker_datas.append(player_poker_datas)
                elif len(poker_datas) > 0:
                    player_poker_datas = poker_datas[0 : ]
                    del poker_datas[0 : ]
                    config.player_poker_datas.append(player_poker_datas)                    
                
        if len(poker_datas) > 0:
            for poker_data in poker_datas:
                config.back_poker_datas.append(poker_data)
                
                
    
    def UpdatePokerTotalCount(self):
        
        poker_pair_count = self.spin_poker_pair_count.GetValue()
        poker_total_count = 0
        poker_diamond_count = 0
        poker_club_count = 0
        poker_heart_count = 0
        poker_spade_count = 0
        poker_king_count = 0   
        poker_magic_count = 0
        
        for poker_ctrl in self.poker_diamond_list:
            poker_count = poker_ctrl["poker_count"].GetValue()
            if poker_count > poker_pair_count: poker_ctrl["poker_count"].SetValue(poker_pair_count)
            poker_diamond_count += poker_ctrl["poker_count"].GetValue()
            poker_total_count += poker_ctrl["poker_count"].GetValue()
            
        for poker_ctrl in self.poker_club_list:
            poker_count = poker_ctrl["poker_count"].GetValue()
            if poker_count > poker_pair_count: poker_ctrl["poker_count"].SetValue(poker_pair_count)            
            poker_club_count += poker_ctrl["poker_count"].GetValue()
            poker_total_count += poker_ctrl["poker_count"].GetValue()        
            
        for poker_ctrl in self.poker_heart_list:
            poker_count = poker_ctrl["poker_count"].GetValue()
            if poker_count > poker_pair_count: poker_ctrl["poker_count"].SetValue(poker_pair_count)            
            poker_heart_count += poker_ctrl["poker_count"].GetValue()
            poker_total_count += poker_ctrl["poker_count"].GetValue()
            
        for poker_ctrl in self.poker_spade_list:
            poker_count = poker_ctrl["poker_count"].GetValue()
            if poker_count > poker_pair_count: poker_ctrl["poker_count"].SetValue(poker_pair_count)            
            poker_spade_count += poker_ctrl["poker_count"].GetValue()
            poker_total_count += poker_ctrl["poker_count"].GetValue()     
            
        for poker_ctrl in self.poker_king_list:
            poker_count = poker_ctrl["poker_count"].GetValue()
            if poker_count > poker_pair_count: poker_ctrl["poker_count"].SetValue(poker_pair_count)            
            poker_king_count += poker_ctrl["poker_count"].GetValue()
            poker_total_count += poker_ctrl["poker_count"].GetValue()
            
        for poker_ctrl in self.poker_magic_list:
            poker_count = poker_ctrl["poker_count"].GetValue()
            if poker_count > poker_pair_count: poker_ctrl["poker_count"].SetValue(poker_pair_count)            
            poker_magic_count += poker_ctrl["poker_count"].GetValue()
            poker_total_count += poker_ctrl["poker_count"].GetValue()  
            
        self.check_all_poker_diamond.Set3StateValue(wx.CHK_UNCHECKED if poker_diamond_count == 0 else (wx.CHK_CHECKED if poker_diamond_count == 13 * poker_pair_count else wx.CHK_UNDETERMINED))
        self.check_all_poker_club.Set3StateValue(wx.CHK_UNCHECKED if poker_club_count == 0 else (wx.CHK_CHECKED if poker_club_count == 13 * poker_pair_count else wx.CHK_UNDETERMINED))
        self.check_all_poker_heart.Set3StateValue(wx.CHK_UNCHECKED if poker_heart_count == 0 else (wx.CHK_CHECKED if poker_heart_count == 13 * poker_pair_count else wx.CHK_UNDETERMINED))
        self.check_all_poker_spade.Set3StateValue(wx.CHK_UNCHECKED if poker_spade_count == 0 else (wx.CHK_CHECKED if poker_spade_count == 13 * poker_pair_count else wx.CHK_UNDETERMINED))        
        self.check_all_poker_king.Set3StateValue(wx.CHK_UNCHECKED if poker_king_count == 0 else (wx.CHK_CHECKED if poker_king_count == 2 * poker_pair_count else wx.CHK_UNDETERMINED))            
        self.check_all_poker_magic.Set3StateValue(wx.CHK_UNCHECKED if poker_magic_count == 0 else (wx.CHK_CHECKED if poker_magic_count == 1 * poker_pair_count else wx.CHK_UNDETERMINED))  
               
        self.spin_poker_total_count.SetValue(poker_total_count)
        self.parent.config.poker_total_count = poker_total_count
        
        
    def OnClose(self, evt):
        
        poker_datas =  self.GetPokerDatas()
        self.AdjustPokerDatas(poker_datas)
        evt.Skip()
        
    
    def OnCheckBox(self, evt):
        
        poker_pair_count = self.spin_poker_pair_count.GetValue()
        checkbox = evt.GetEventObject()
        if checkbox is self.check_all_poker_diamond:
            for poker_ctrl in self.poker_diamond_list:
                poker_ctrl["poker_count"].SetValue(0 if checkbox.Get3StateValue() == wx.CHK_UNCHECKED else poker_pair_count)            
        elif checkbox is self.check_all_poker_club:
            for poker_ctrl in self.poker_club_list:
                poker_ctrl["poker_count"].SetValue(0 if checkbox.Get3StateValue() == wx.CHK_UNCHECKED else poker_pair_count)   
        elif checkbox is self.check_all_poker_heart:
            for poker_ctrl in self.poker_heart_list:
                poker_ctrl["poker_count"].SetValue(0 if checkbox.Get3StateValue() == wx.CHK_UNCHECKED else poker_pair_count)    
        elif checkbox is self.check_all_poker_spade:
            for poker_ctrl in self.poker_spade_list:
                poker_ctrl["poker_count"].SetValue(0 if checkbox.Get3StateValue() == wx.CHK_UNCHECKED else poker_pair_count)    
        elif checkbox is self.check_all_poker_king:
            for poker_ctrl in self.poker_king_list:
                poker_ctrl["poker_count"].SetValue(0 if checkbox.Get3StateValue() == wx.CHK_UNCHECKED else poker_pair_count)                    
        elif checkbox is self.check_all_poker_magic:
            for poker_ctrl in self.poker_magic_list:
                poker_ctrl["poker_count"].SetValue(0 if checkbox.Get3StateValue() == wx.CHK_UNCHECKED else poker_pair_count)
                
        self.UpdatePokerTotalCount()
        
        
    def FindPokerSpinCtrl(self, spin):
        
        for poker_ctrl in self.poker_diamond_list:
            if spin is poker_ctrl["poker_count"]:  
                return True
        for poker_ctrl in self.poker_club_list:
            if spin is poker_ctrl["poker_count"]:  
                return True
        for poker_ctrl in self.poker_heart_list:
            if spin is poker_ctrl["poker_count"]:  
                return True
        for poker_ctrl in self.poker_spade_list:
            if spin is poker_ctrl["poker_count"]:  
                return True
        for poker_ctrl in self.poker_king_list:
            if spin is poker_ctrl["poker_count"]:  
                return True
        for poker_ctrl in self.poker_magic_list:
            if spin is poker_ctrl["poker_count"]:  
                return True
            
        return False
            
        
    def OnSelectedSpinPokerTotalCount(self, evt):
        
        spin = evt.GetEventObject()
    
        if spin is self.spin_poker_total_count:
            self.parent.config.poker_total_count = spin.GetValue()
        else:
            if self.FindPokerSpinCtrl(spin):
                self.UpdatePokerTotalCount()
        
    def OnChangeSpinPokerTotalCount(self, evt):

        spin = evt.GetEventObject()

        if spin is self.spin_poker_total_count:
            self.parent.config.poker_total_count = spin.GetValue()        
        else:
            if self.FindPokerSpinCtrl(spin):
                self.UpdatePokerTotalCount()  
                
    def OnSelectedSpinPokerPairCount(self, evt):
        
        spin = evt.GetEventObject()
    
        if spin is self.spin_poker_pair_count:
            self.parent.config.poker_pair_count = spin.GetValue()
            self.UpdatePokerTotalCount()
            
            
    def OnChangeSpinPokerPairCount(self, evt):
        
        spin = evt.GetEventObject()

        if spin is self.spin_poker_pair_count:
            self.parent.config.poker_pair_count = spin.GetValue()    
            self.UpdatePokerTotalCount()
                
    def OnSelectedSpinValue(self, evt):
        
        spin = evt.GetEventObject()
    
        if spin is self.spin_poker_player_count:
            self.parent.config.poker_player_count = spin.GetValue()
            if self.parent.config.poker_player_count > 0:
                self.spin_poker_banker_seat_id.SetRange(0, self.parent.config.poker_player_count - 1)
                if self.spin_poker_banker_seat_id.GetValue() >= self.parent.config.poker_player_count:
                    self.spin_poker_banker_seat_id.SetValue(self.parent.config.poker_player_count - 1)
                    
                select_index = 0
                select_values = []        
                chioce_values = [i for i in range(14, 109)]
                if self.parent.config.poker_everyone_count not in chioce_values:
                    self.parent.config.poker_everyone_count = chioce_values[0]
                    
                for index in range(len(chioce_values)):
                    select_values.append(str(chioce_values[index]))
                    if chioce_values[index] == self.parent.config.poker_everyone_count:
                        select_index = index
                self.choice_poker_everyone_count.SetItems(select_values)
                self.choice_poker_everyone_count.Select(select_index)                    
            else:
                self.spin_poker_banker_seat_id.SetRange(0, 0)
                self.spin_poker_banker_seat_id.SetValue(0)
                self.choice_poker_everyone_count.SetItems(["14"])
                self.choice_poker_everyone_count.Select(0)                 
                
            self.parent.config.poker_banker_seat_id = self.spin_poker_banker_seat_id.GetValue()
            
            select_index = self.choice_poker_everyone_count.GetCurrentSelection()
            self.parent.config.poker_everyone_count = int(self.choice_poker_everyone_count.GetString(select_index))            
            
        elif spin is self.spin_poker_banker_seat_id:
            self.parent.config.poker_banker_seat_id = spin.GetValue() 
            
        elif spin is self.spin_poker_test_count:
            self.parent.config.poker_test_count = spin.GetValue()               
        
    def OnChangeSpinValue(self, evt):

        spin = evt.GetEventObject()

        if spin is self.spin_poker_player_count:
            self.parent.config.poker_player_count = spin.GetValue()
            if self.parent.config.poker_player_count > 0:
                self.spin_poker_banker_seat_id.SetRange(0, self.parent.config.poker_player_count - 1)
                if self.spin_poker_banker_seat_id.GetValue() >= self.parent.config.poker_player_count:
                    self.spin_poker_banker_seat_id.SetValue(self.parent.config.poker_player_count - 1)
            else:
                self.spin_poker_banker_seat_id.SetRange(0, 0)
                self.spin_poker_banker_seat_id.SetValue(0)
                
            self.parent.config.poker_banker_seat_id = self.spin_poker_banker_seat_id.GetValue() 
            
        elif spin is self.spin_poker_banker_seat_id:
            self.parent.config.poker_banker_seat_id = spin.GetValue()  
            
        elif spin is self.spin_poker_test_count:
            self.parent.config.poker_test_count = spin.GetValue()
            
    def OnChoiceValue(self, evt):
        
        choice =  evt.GetEventObject()
        
        if choice is self.choice_poker_everyone_count:
            select_index = choice.GetCurrentSelection()
            self.parent.config.poker_everyone_count = int(choice.GetString(select_index))

    

class PokerMainFrame(wx.Frame):
    
    def __init__(self):
        
        wx.Frame.__init__(self, parent = None, id = -1, title = u'扑克做牌工具') 
        
        self.SetIcon(wx.Icon("images/poker.ico"))
        self.SetWindowStyle(self.GetWindowStyle() & ~wx.MAXIMIZE_BOX)
        self.SetSize(self.ClientToWindowSize((960, 640)))
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())
        
        self.config = PokerConfig()
        if self.config.Read("PokerConfig.ini") == False:
            self.config.ReadJson("PokerConfig.json")
        
        chioce_values = [i for i in range(14, 109)]
        if self.config.poker_everyone_count not in chioce_values:
            self.config.poker_everyone_count = chioce_values[0]        
        global NORMAL_POKER_COUNT
        NORMAL_POKER_COUNT = self.config.poker_everyone_count

        self.save_config_path = None
        
        self.canvas = DragCanvas(self)
        frame_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.canvas.SetSizer(frame_sizer)
        
        self.btn_setting = wx.Button(self.canvas, label=u"设置", size = (40, -1))
        self.btn_config_path = wx.Button(self.canvas, label=u"设置保存路径", size = (90, -1))
        self.btn_save = wx.Button(self.canvas, label=u"保存", size = (40, -1))
        settings_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        settings_sizer.Add(self.btn_setting, 0, wx.LEFT, 2)
        settings_sizer.AddStretchSpacer(1)
        settings_sizer.Add(self.btn_config_path, 0, wx.RIGHT, 2)
        settings_sizer.Add(self.btn_save, 0, wx.RIGHT, 2)
        frame_sizer.Add(settings_sizer, 1, wx.ALL|wx.EXPAND, 0)
        
        self.Bind(wx.EVT_CLOSE,  self.OnClose)
        self.Bind(wx.EVT_BUTTON, self.OnBtnSetting, self.btn_setting)
        self.Bind(wx.EVT_BUTTON, self.OnBtnConfigPath, self.btn_config_path)
        self.Bind(wx.EVT_BUTTON, self.OnBtnSave, self.btn_save)
        
    def __del__(self):
        
        self.config.Write("PokerConfig.ini")
        self.config.WriteJson("PokerConfig.json")
        print('save config to file')
        
    def OnClose(self, evt):
 
        self.canvas.SavePokerViewToConfig()
        evt.Skip()
        

    def OnBtnSetting(self, evt):
        
        setting_dlg = PokerSettingDlg(self)
        setting_dlg.ShowModal()
        setting_dlg.Destroy()
        
        global NORMAL_POKER_COUNT
        NORMAL_POKER_COUNT = self.config.poker_everyone_count
    
        self.canvas.ResetPokerView()
        self.canvas.UpdatePokerView()
        
    def OnBtnConfigPath(self,  evt):
        
        wildcard = "config file format ini (PokerConfig.ini)|*.ini|"     \
                   "config file format json (PokerConfig.json)|*.json|" \
                   "All files (*.*)|*.*"        
        file_dlg = wx.FileDialog(self, message="Save file as ...", defaultDir=os.getcwd(),
                                  defaultFile="PokerConfig.ini", wildcard=wildcard, style=wx.SAVE)
        file_dlg.SetFilterIndex(0)
        if file_dlg.ShowModal() == wx.ID_OK:
            self.save_config_path = file_dlg.GetPath()
        
        
    def OnBtnSave(self, evt):
        
        if self.save_config_path != None:
            self.canvas.SavePokerViewToConfig()
            if os.path.isdir(self.save_config_path):
                save_path =  os.path.join(self.save_config_path, "PokerConfig.ini")
                self.config.Write(save_path)
                save_path =  os.path.join(self.save_config_path, "PokerConfig.json")
                self.config.WriteJson(save_path)
            else:
                file_name = os.path.basename(self.save_config_path)
                ext_name =  os.path.splitext(file_name)[1]
                if ext_name.lower() == '.json':
                    self.config.WriteJson(self.save_config_path)
                else:
                    self.config.Write(self.save_config_path)
            
            wx.MessageBox(u"保存成功！", u"温馨提示", wx.OK, self)
        

class PokerApp(wx.App):  

    def OnInit(self):
        frame = PokerMainFrame()
        frame.Show(True)
        return True
    


def main():
    """software start runing """

    app = PokerApp()  
    app.MainLoop()

    return

    
if __name__ == "__main__":
    main()

 
