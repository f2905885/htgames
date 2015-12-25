# -*- coding: cp936 -*-
import wx
#import sys
import MySQLdb
import time
import wx.lib.agw.aquabutton as AB
import  wx.lib.mixins.listctrl  as  listmix

area_list = {}
area_list[1] = ["1区","180.153.250.137",3306,"shanghaikefu","Rdi3zc2]qaxVagdc","sgs2012_new"]
area_list[2] = ["2区","114.80.99.59",3306,"shanghaikefu","Rdi3zc2]qaxVagdc","sgs2012_new"]
#area_list[3] = ["3区","180.153.250.131",3306,"shanghaikefu","Rdi3zc2]qaxVagdc","sgs2012_new"]
area_list[4] = ["4/5区","114.80.99.60",3306,"shanghaikefu","Rdi3zc2]qaxVagdc","sgs2012_new"]
#area_list[6] = ["6区","125.39.178.19",3306,"shanghaikefu","Rdi3zc2]qaxVagdc","sgs2012_new"]
area_list[5] = ["7/8区","114.80.99.58",3306,"shanghaikefu","Rdi3zc2]qaxVagdc","sgs2012_new"]
area_list[6] = ["9区","sp4fdfdb3655d9a.mysql.aliyun.com",3306,"sgs2012_user","qrjf_u87joqwvu3","sgs2012_new"]

lock_time_list = ['1天', '5天', '10天', '1个月', '1年', '5年']
lock_time_dict = {}
lock_time_dict['1天'] = 1
lock_time_dict['5天'] = 5
lock_time_dict['10天'] = 10
lock_time_dict['1个月'] = 30
lock_time_dict['1年'] = 365
lock_time_dict['5年'] = 365 * 5

lock_reason_list = ['空', '1', '2', '3', '4']
lock_reason_dict = {}
lock_reason_dict['空'] = "NULL"
lock_reason_dict['1'] = 1
lock_reason_dict['2'] = 2
lock_reason_dict['3'] = 3
lock_reason_dict['4'] = 4

class ResultDisplay(wx.ListCtrl, listmix.TextEditMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(
	    self, parent, -1, size=(450,160),
            style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES
            )
        listmix.TextEditMixin.__init__(self)
        #self.il = wx.ImageList(16, 16)
        #self.idx1 = self.il.Add(images.Smiles.GetBitmap())
        #self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        self.InsertColumn(0, "ID")
        self.InsertColumn(1, "大区")
        self.InsertColumn(2, "玩家帐号")
        self.InsertColumn(3, "解封时间")
        self.InsertColumn(4, "原因")
        self.SetColumnWidth(0, 30)
        self.SetColumnWidth(1, 50)
        self.SetColumnWidth(2, 120)
        self.SetColumnWidth(3, 150)
        self.SetColumnWidth(4, 50)

        self.il = wx.ImageList(16, 16)
        #self.idx1 = self.il.Add(images.Smiles.GetBitmap())
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

class MyPanel(wx.Panel):
    def __init__(self, parent, colour, label):
        wx.Panel.__init__(self, parent, style=0)
        self.SetBackgroundColour(colour)
        vbox_top = wx.BoxSizer(wx.HORIZONTAL)
        #panel = wx.Panel(self, -1)
        panel = self
        vbox = wx.BoxSizer(wx.VERTICAL)
        # panel0
        panel_0 = wx.Panel(panel, -1)
        l1 = wx.StaticText(panel_0, -1, "", pos=(0,0))
        vbox.Add(panel_0, 0, wx.BOTTOM, 5)
        
        # panel1
        panel_1 = wx.Panel(panel, -1)
        sizer_1 = wx.StaticBoxSizer(wx.StaticBox(panel_1, -1, "大区选择"), orient=wx.VERTICAL)
        grid_1 = wx.GridSizer(2, 7, 5, 5)
        self.area_1 = wx.CheckBox(panel_1, -1, area_list[1][0])
        self.area_2 = wx.CheckBox(panel_1, -1, area_list[2][0])
        #self.area_3 = wx.CheckBox(panel_1, -1, area_list[3][0])
        self.area_4 = wx.CheckBox(panel_1, -1, area_list[4][0])
        self.area_5 = wx.CheckBox(panel_1, -1, area_list[5][0])
        self.area_6 = wx.CheckBox(panel_1, -1, area_list[6][0])
        self.area_10 = wx.CheckBox(panel_1, -1, "全选")
        self.area_11 = wx.CheckBox(panel_1, -1, "反选")
        self.area_1.SetValue(True)
        self.area_2.SetValue(True)
        #self.area_3.SetValue(True)
        self.area_4.SetValue(True)
        self.area_5.SetValue(True)
        self.area_6.SetValue(True)
        self.Bind(wx.EVT_CHECKBOX, self.AllChoice, self.area_10)
        self.Bind(wx.EVT_CHECKBOX, self.ReverseChoice, self.area_11)
        
        grid_1.Add(self.area_1, 0, wx.LEFT|wx.BOTTOM, 3)
        grid_1.Add(self.area_2, 0, wx.LEFT|wx.BOTTOM, 3)
        #grid_1.Add(self.area_3, 0, wx.LEFT|wx.BOTTOM, 3)
        grid_1.Add(self.area_4, 0, wx.LEFT|wx.BOTTOM, 3)
        grid_1.Add(self.area_5, 0, wx.LEFT|wx.BOTTOM, 3)
        grid_1.Add(self.area_6, 0, wx.LEFT|wx.BOTTOM, 3)
        grid_1.Add(self.area_10, 0, wx.LEFT|wx.BOTTOM, 3)
        grid_1.Add(self.area_11, 0, wx.LEFT|wx.BOTTOM, 3)

        sizer_1.Add(grid_1, 0, wx.TOP, 5)
        panel_1.SetSizer(sizer_1)
        vbox.Add(panel_1, 0, wx.BOTTOM, 5)

        """
        # panel2
        panel_2 = wx.Panel(panel, -1)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        lock_time_rb = wx.RadioBox(
                panel_2, -1, "封号时长", wx.DefaultPosition, wx.DefaultSize,
                lock_time_list, 6, wx.RA_SPECIFY_COLS
                )
        lock_time_rb.SetSelection(5)
        self.lock_time_rb = lock_time_rb
        sizer_2.Add(lock_time_rb, 0, wx.TOP, 5)
        panel_2.SetSizer(sizer_2)
        vbox.Add(panel_2, 0, wx.BOTTOM, 5)

        # panel3
        panel_3 = wx.Panel(panel, -1)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        lock_reason_rb = wx.RadioBox(
                panel_3, -1, "封号原因", wx.DefaultPosition, wx.DefaultSize,
                lock_reason_list, 6, wx.RA_SPECIFY_COLS
                )
        lock_reason_rb.SetSelection(0)
        self.lock_reason_rb = lock_reason_rb
        sizer_3.Add(lock_reason_rb, 5, wx.TOP, 5)
        panel_3.SetSizer(sizer_3)
        vbox.Add(panel_3, 0, wx.BOTTOM, 5)
        """
        
        # panel4
        panel_4 = wx.Panel(panel, -1)
        l1 = wx.StaticText(panel_4, -1, "帐号", pos=(0,12))
        t1 = wx.TextCtrl(panel_4, -1, "", pos=(30,10), size=(200, -1))
        self.account_value = t1
        
        query_action_button = AB.AquaButton(panel_4, -1, None, "查   询", (250, 0), (100,50))
        query_action_button.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Verdana'))
        #query_action_button.SetBackgroundColour('RED')
        self.Bind(wx.EVT_BUTTON, self.QueryAction, query_action_button)
        
        #lock_action_button = AB.AquaButton(panel_4, -1, None, "封  号", (320, 0))
        #lock_action_button.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Verdana'))
        #lock_action_button.SetBackgroundColour('RED')
        #self.Bind(wx.EVT_BUTTON, self.LockAction, lock_action_button)

        '''齐骏说这个功能不要了
        unlock_action_button = AB.AquaButton(panel_4, -1, None, "解   封", (380, 0), (100,50))
        unlock_action_button.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Verdana'))
        #unlock_action_button.SetBackgroundColour('RED')
        self.Bind(wx.EVT_BUTTON, self.UnlockAction, unlock_action_button)
        '''
        vbox.Add(panel_4, 0, wx.BOTTOM, 5)

        # panel5
        panel_5 = wx.Panel(panel, -1)
        l1 = wx.StaticText(panel_5, -1, "", pos=(0,0))
        vbox.Add(panel_5, 0, wx.BOTTOM, 5)

        # panel6
        panel_6 = wx.Panel(panel, -1)
        sizer_6 = wx.StaticBoxSizer(wx.StaticBox(panel_6, -1, '结果显示'), orient=wx.VERTICAL)
        vbox_6 = wx.BoxSizer(wx.VERTICAL)
        grid_6 = wx.GridSizer(1, 1, 0, 5)
        self.result_display = ResultDisplay(panel_6)
        grid_6.Add(self.result_display)
        vbox_6.Add(grid_6)
        sizer_6.Add(vbox_6, 0, wx.TOP, 4)

        panel_6.SetSizer(sizer_6)
        vbox.Add(panel_6, 0, wx.BOTTOM, 15)
        
        ####
        vbox_top.Add(vbox, 1, wx.LEFT, 5)
        panel.SetSizer(vbox_top)

        self.Centre()
        self.Show()

    def AllChoice(self, event):
        if event.IsChecked() is True:
            self.area_1.SetValue(True)
            self.area_2.SetValue(True)
            #self.area_3.SetValue(True)
            self.area_4.SetValue(True)
            self.area_5.SetValue(True)
            self.area_6.SetValue(True)
            self.area_11.SetValue(False)

    def ReverseChoice(self, event):
        if event.IsChecked() is True:
            self.area_1.SetValue(not self.area_1.GetValue())
            self.area_2.SetValue(not self.area_2.GetValue())
            #self.area_3.SetValue(not self.area_3.GetValue())
            self.area_4.SetValue(not self.area_4.GetValue())
            self.area_5.SetValue(not self.area_5.GetValue())
            self.area_6.SetValue(not self.area_6.GetValue())
            self.area_10.SetValue(False)

    def ConnectAction(self, area, n):
        if area.GetValue() is True:
            try:
                db_conn = MySQLdb.connect(host=area_list[n][1],user=area_list[n][3],passwd=area_list[n][4],db=area_list[n][5])
                db_cursor = db_conn.cursor()
                sql = "SELECT * FROM  tblblockaccount WHERE useraccount = '%s';" % self.lock_account
                execute_value = db_cursor.execute(sql)
                if execute_value > 0:
                    sql = "DELETE FROM tblblockaccount WHERE useraccount = '%s';" % self.lock_account
                    m = db_cursor.execute(sql)
                sql = "INSERT INTO tblblockaccount (useraccount,maylogin,why) values ('%s','%s',%s);" % (self.lock_account, self.lock_user_time, self.lock_why_value)
                execute_value = db_cursor.execute(sql)
                db_cursor.close()
                db_conn.commit()
                db_conn.close()
                db_error = 0
                if self.end_msg == "":
                    self.end_msg = self.end_msg + area_list[n][0]
                else:
                    self.end_msg = self.end_msg + "," + area_list[n][0]
            except:
                db_error = 1
                warn_msg = area_list[n][0] + "数据库操作错误!!!!!!!"
                dlg = wx.MessageDialog(self, warn_msg, '警告!',
                                       wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy            
            

    def LockAction(self, event):
        self.result_display.DeleteAllItems()
        add_seconds = lock_time_dict[lock_time_list[self.lock_time_rb.GetSelection()]] * 24 * 3600 - time.timezone
        self.lock_user_time = time.strftime("%Y-%m-%d %H:%M:%S",  time.gmtime( time.time() + add_seconds) )
        self.lock_why_value = lock_reason_dict[lock_reason_list[self.lock_reason_rb.GetSelection()]]
        self.lock_account = self.account_value.GetValue().encode("gbk")
        if self.lock_account == "":
            dlg = wx.MessageDialog(self, "请输入玩家帐号！！！", '提示!',
                                       wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy
        else:
            #print self.lock_account, self.lock_user_time, self.lock_why_value
            self.end_msg = ""
            self.ConnectAction(self.area_1, 1)
            self.ConnectAction(self.area_2, 2)
            #self.ConnectAction(self.area_3, 3)
            self.ConnectAction(self.area_4, 4)
            self.ConnectAction(self.area_5, 5)
            self.ConnectAction(self.area_6, 6)
            
            #self.end_msg = self.end_msg + "数据库操作成功."
            #dlg = wx.MessageDialog(self, self.end_msg, '提示!',
            #                               wx.OK | wx.ICON_INFORMATION)
            #dlg.ShowModal()
            #dlg.Destroy

    def QueryConnectAction(self, area, n):
        if area.GetValue() is True:
            try:
                db_conn = MySQLdb.connect(host=area_list[n][1],user=area_list[n][3],passwd=area_list[n][4],db=area_list[n][5])
                db_cursor = db_conn.cursor()
                sql = "SELECT useraccount,maylogin,why FROM tblblockaccount WHERE useraccount = '%s';" % self.lock_account
                execute_value = db_cursor.execute(sql)
                for single_result in db_cursor.fetchall():
                    (useraccount, maylogin, why) = single_result
                    self.result_display.InsertStringItem(self.idx, str(self.idx+1))
                    self.result_display.SetStringItem(self.idx, 1, area_list[n][0])
                    self.result_display.SetStringItem(self.idx, 2, str(useraccount))
                    self.result_display.SetStringItem(self.idx, 3, str(maylogin))
                    self.result_display.SetStringItem(self.idx, 4, str(why))
                    self.result_display.SetItemTextColour(self.idx, "blue")
                    self.idx += 1
                db_cursor.close()
                db_conn.close()
                db_error = 0
                if self.end_msg == "":
                    self.end_msg = self.end_msg + area_list[n][0]
                else:
                    self.end_msg = self.end_msg + "," + area_list[n][0]
            except:
                db_error = 1
                warn_msg = area_list[n][0] + "数据库查询错误!!!!!!!"
                dlg = wx.MessageDialog(self, warn_msg, '警告!',
                                       wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy
            
    def QueryAction(self, event):
        self.result_display.DeleteAllItems()
        self.lock_account = self.account_value.GetValue().encode("gbk")
        self.idx = 0
        self.end_msg = ""
        if self.lock_account == "":
            dlg = wx.MessageDialog(self, "请输入玩家帐号！！！", '提示!',
                                       wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy
        else:
            self.QueryConnectAction(self.area_1, 1)
            self.QueryConnectAction(self.area_2, 2)
            #self.QueryConnectAction(self.area_3, 3)
            self.QueryConnectAction(self.area_4, 4)
            self.QueryConnectAction(self.area_5, 5)
            self.QueryConnectAction(self.area_6, 6)

    def UnlockConnectAction(self, area, n):
        if area.GetValue() is True:
            try:
                db_conn = MySQLdb.connect(host=area_list[n][1],user=area_list[n][3],passwd=area_list[n][4],db=area_list[n][5])
                db_cursor = db_conn.cursor()
                sql = "DELETE FROM tblblockaccount WHERE useraccount = '%s';" % self.lock_account
                execute_value = db_cursor.execute(sql)
                db_cursor.close()
                db_conn.commit()
                db_conn.close()
                db_error = 0
                if self.end_msg == "":
                    self.end_msg = self.end_msg + area_list[n][0]
                else:
                    self.end_msg = self.end_msg + "," + area_list[n][0]
            except:
                db_error = 1
                warn_msg = area_list[n][0] + "数据库操作错误!!!!!!!"
                dlg = wx.MessageDialog(self, warn_msg, '警告!',
                                       wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy    

    def UnlockAction(self, event):
        self.result_display.DeleteAllItems()
        self.lock_account = self.account_value.GetValue().encode("gbk")
        self.end_msg = ""
        if self.lock_account == "":
            dlg = wx.MessageDialog(self, "请输入玩家帐号！！！", '提示!',
                                       wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy
        else:
            self.UnlockConnectAction(self.area_1, 1)
            self.UnlockConnectAction(self.area_2, 2)
            #self.UnlockConnectAction(self.area_3, 3)
            self.UnlockConnectAction(self.area_4, 4)
            self.UnlockConnectAction(self.area_5, 5)
            self.UnlockConnectAction(self.area_6, 6)
    
class WarnFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(555, 570))
        dlg = wx.MessageDialog(self, '没有找到礼包配置文件!!!!!', '警告!',
                                       wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy

class ConnDbError(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(555, 570))
        dlg = wx.MessageDialog(self, '数据库连接失败!!!!!', '警告!',
                                       wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy



