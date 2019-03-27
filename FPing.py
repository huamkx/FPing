# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
## BY KXHuang 2018-11-05
## Version 1.0
###########################################################################

import wx
import wx.xrc
import configparser
# 保存配置文件必须导入
import time,subprocess,re
from threading import Thread
# 导入线程
from pubsub import pub
from win32con import AW_ACTIVATE, AW_BLEND, AW_CENTER, AW_HIDE, AW_HOR_NEGATIVE, \
    AW_HOR_POSITIVE, AW_SLIDE, AW_VER_NEGATIVE, AW_VER_POSITIVE, SPI_GETWORKAREA
import win32api
from ctypes import windll, c_int
import time

###########################################################################
## Class MyFrame2
###########################################################################
# 多线程函数
def th_do():
        conf = configparser.ConfigParser()
        # 调用configparser属性方法
        conf.read('dbconf.ini')
        # 读取本地文件
        sects = conf.sections()
        cal = 0
        for i in sects:
            # 遍历 sects中的section
            items = conf.items(sects[cal])
            # 获取(key,value)元组
            host_ini = (items[0][1])
            # 获取第一组key中的value（ip信息）
            p = subprocess.Popen(["ping.exe", '%s'%host_ini],stdin = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                shell = True)  
            p.wait() 
            # 等待完成才继续，数量大会造成较长队列，进而会阻塞管道
            returncode = p.returncode
            # 判断shell执行结果，0成功，1失败
            if returncode == 0:
                try:
                        out = p.stdout.read().decode('gbk')
                        # .decode（'gbk'）原理不熟悉，不加会报错
                        packetdelay = re.compile("= (\d+)ms").findall(out)[1] + 'ms'
                        #获取最长的延迟值（re.compile获取到的值类型是元组）
                        
                except IndexError:
                        wx.CallAfter(pub.sendMessage,'update',msg =(cal,1))
                        cal+=1
                        print ('无法访问目标/网络...',returncode) #调试用
                else:
                        packetlost = re.compile("(\d+)%").findall(out)[0] + '%'
                        #获取包丢失比例（re.compile获取到的值类型是元组）
                        wx.CallAfter(pub.sendMessage,'update',msg = (cal,0,packetdelay,packetlost))
                        cal+=1
            else:
                print (returncode) #调试用
                wx.CallAfter(pub.sendMessage,'update',msg =(cal,1))
                cal+=1
                
# returncode 为 1的情况：
'''
① 请求超时。
② PING：传输失败。常见故障。
③ Ping 请求找不到主机 255.255.255.255。请检查该名称，然后重试。


'''

# returncode 为0 的情况：
'''
① 主机或网络一切正常
② 主机或网络不正常，但能接收到回包，因此此类会抛出异常，所以做了try 
'''


class MyFrame2 ( wx.Frame ):
    # 主窗口
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "FreePing", pos = wx.DefaultPosition, size = wx.Size( 600,700 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetIcon(wx.Icon('loadIcon.ico', wx.BITMAP_TYPE_ICO))
        #添加icon
        self.m_menubar1 = wx.MenuBar( 0 )
        self.m_menu1 = wx.Menu()
        self.m_menuItem1 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Add", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.m_menuItem1 )
        
        self.m_menuItem2 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Edit", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.m_menuItem2 )
        self.m_menuItem2.Enable(False)
        
        self.m_menuItem3 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Delete", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.m_menuItem3 )
        self.m_menuItem3.Enable(False)
        self.m_menu1.AppendSeparator()
        
        self.m_menuItem4 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Reset results", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.m_menuItem4 )
        self.m_menuItem4.Enable(False)
        self.m_menu1.AppendSeparator()
        
        self.m_menuItem5 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append( self.m_menuItem5 )
        
        self.m_menubar1.Append( self.m_menu1, u"Host" ) 
        
        self.m_menu3 = wx.Menu()
        self.m_menuItem6 = wx.MenuItem( self.m_menu3, wx.ID_ANY, u"Toolbar", wx.EmptyString, wx.ITEM_CHECK )
        self.m_menu3.Append( self.m_menuItem6 )
        self.m_menuItem6.Check( True )
        self.m_menuItem6.Enable(False)

        self.m_menuItem7 = wx.MenuItem( self.m_menu3, wx.ID_ANY, u"Status Bar", wx.EmptyString, wx.ITEM_CHECK )
        self.m_menu3.Append( self.m_menuItem7 )
        self.m_menuItem7.Check( True )
        self.m_menuItem7.Enable(False)
        
        self.m_menubar1.Append( self.m_menu3, u"View" ) 
        
        self.m_menu4 = wx.Menu()
        # 20181203完善help菜单===========================
        self.m_menuItem9 = wx.MenuItem( self.m_menu4, wx.ID_ANY, u"Manual", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu4.Append( self.m_menuItem9 )
        #-=============================================
        self.m_menuItem8 = wx.MenuItem( self.m_menu4, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu4.Append( self.m_menuItem8 )

        
        
        self.m_menubar1.Append( self.m_menu4, u"Help" ) 
        
        self.SetMenuBar( self.m_menubar1 )
        
        # right_hit menu
        self.m_menu2 = wx.Menu()
        self.menu1 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Add", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu2.Append( self.menu1 )

        self.menu2 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Delete", wx.EmptyString, wx.ITEM_NORMAL )
        self.menu2.Enable(False)
        self.m_menu2.Append( self.menu2 )




        self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY ) 
        #self.m_tool1 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"1.gif", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
        self.m_toolBar1.Realize() 
        self.statusbar = self.CreateStatusBar(1, 0)
        #尾部状态栏
#=================分栏功能,保留==================
        #self.statusbar.SetStatusText(u"欢迎使用Ping工具!", 0)
        #self.statusbar.SetFieldsCount(3)
        #self.statusbar.SetStatusWidths([-3,-2,-1])
        self.statusbar.SetStatusText(u"欢迎使用Ping工具!", 0)
        #self.statusbar.SetStatusText('Running...', 1) 
        #statusbar_date = time.strftime("%Y/%m/%d", time.localtime())
        #self.statusbar.SetStatusText(statusbar_date, 2)
#==============================================
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_listCtrl1 = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, size = wx.Size( 400,500 ),style= wx.LC_REPORT )
        self.m_listCtrl1.InsertColumn(0,u"Host",width=150)
        self.m_listCtrl1.InsertColumn(1,u"Description",width=120)
        self.m_listCtrl1.InsertColumn(2,u"Delay(ms)",width=80)
        self.m_listCtrl1.InsertColumn(3,u"Sent",width=80)
        self.m_listCtrl1.InsertColumn(4,u"Status",width=50)
        self.m_listCtrl1.InsertColumn(5,u"% Lost",width=100)
        self.m_listCtrl1.SetItemState(0, 0, wx.LIST_STATE_SELECTED)  
        # 默认会选中第一行内容，此处我们使第一行不被选中
        self.m_listCtrl1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) ) #字体颜色
        self.m_listCtrl1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) ) #背景色
        bSizer2.Add( self.m_listCtrl1, 1, wx.ALL|wx.EXPAND, 0 )
        self.timer = wx.Timer(self) 
        # 第一个定时时钟，给ping的时候用
#==========================================================================================================================#
        self.timer1 = wx.Timer(self)
        # 第二个定时时钟，给弹窗检查用
        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"定时检查：(选项分别对应 1分钟、30分钟、1个小时、2个小时)" ), wx.HORIZONTAL )

        self.m_checkBox1 = wx.CheckBox( self, wx.ID_ANY, u"Remind Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer1.Add( self.m_checkBox1, 0, wx.ALL, 5 )

        m_choice1Choices = ['60000','1800000','3600000','7200000']
        # 定时器选择，单位为毫秒，分别对应：1分钟，30分钟，1个小时，2个小时
        self.m_choice1 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0 )
        sbSizer1.Add( self.m_choice1, 0, wx.ALL, 5 )
        self.Bind(wx.EVT_TIMER,self.onChecked,self.timer1)
        # 绑定计时器1
        self.m_choice1.Bind(wx.EVT_CHOICE, self.OnChoice)
#====================================================================================================================================#  
        
        bSizer2.Add( sbSizer1, 1, wx.EXPAND, 5 )
        self.SetSizer( bSizer2 )
        self.Layout()
        
        self.Centre( wx.BOTH )
    
    # Connect Events
    #1. 主窗口右键菜单绑定============================================
        self.m_listCtrl1.Bind( wx.EVT_RIGHT_DOWN, self.right_hit)
        # 右键菜单函数    
        self.Bind( wx.EVT_MENU, self.AddConf, id = self.menu1.GetId() )
        # 右键添加事件
        self.Bind( wx.EVT_MENU, self.OnDel, id = self.menu2.GetId() )
        # 右键移除事件
    #===============================================================

    #2.主窗口菜单栏绑定================================================
        self.Bind( wx.EVT_MENU, self.AddConf, id = self.m_menuItem1.GetId() )
        # 主机配置绑定
        self.Bind( wx.EVT_MENU, self.AddExit, id = self.m_menuItem5.GetId() )
        # Exit
        self.Bind( wx.EVT_MENU, self.OnAbout, id = self.m_menuItem8.GetId() )
        # 软件信息绑定
        self.Bind( wx.EVT_MENU, self.OnManual, id = self.m_menuItem9.GetId() )
        # Manual绑定
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        # 退出窗口
    #================================================================

    #3. 多线程定时器绑定，做Ping用 
        self.Bind(wx.EVT_TIMER,self.OnThread,self.timer)
        # 绑定时器对象
        self.timer.Start(5000)
    #===================================================================    
        
    # 读取配置文件并加载到主窗口
        conf = configparser.ConfigParser()
        # 调用configparser属性方法
        conf.read('dbconf.ini')
        # 读取本地文件
        sects = conf.sections()
        cal = 0
        for i in sects:
            # 遍历 sects中的section
            items = conf.items(sects[cal])
            # 获取(key,value)元组
            host_ini = (items[0][1])
            # 获取第一组key中的value（ip信息）
            description_ini =  (items[1][1])
            # 获取第二组key中的value（主机描述信息）
            self.m_listCtrl1.InsertItem(cal,str(host_ini))
            # 主窗口第cal行，第一列插入数据
            self.m_listCtrl1.SetItem(cal,1,str(description_ini))
            self.m_listCtrl1.SetItem(cal,3,'0')
            # 主窗口第cal行，第二列设置数据
            cal+=1
        pub.subscribe(self.listener,'update')
        # 订阅线程通知，线程名“update”

    
    def OnChoice(self,event):
        self.timer1.Stop()
        # 选择不同参数时，会先停止计时器
        self.timer1.Start(int(self.m_choice1.GetString(self.m_choice1.GetSelection())))
        # 获取参数后，重新开始计时
    def onChecked(self,event):
        if self.m_checkBox1.GetValue() == True:
        # 检测checkbox是否启用，即是否选择了定时通知
            onChecked_count = self.m_listCtrl1.GetItemCount()
            #获取主窗口listctrl有多少行
            if  onChecked_count != 0:
            # 判断主窗口是否有数据
                for i in range(onChecked_count):
                # 读取list数据是从第0行开始
                    if self.m_listCtrl1.GetItemText(i,4) == '×':
                    # 检测第i行的第4栏数据是否为Failed
#============================20181126 kx 新增中断服务时间，便于识别============================
                        current_time = time.strftime('%H:%M:%S',time.localtime(time.time()))
                        current_message = self.m_listCtrl1.GetItemText(i) +'      '+'('+'时间：'+ current_time+')'
                        cfgFrame1=Popup(current_message)
#============================================================================================
                        #向指定类传递获取到的值    
                        cfgFrame1.Show(True)
                        # 显示类窗口
# 多线程
    def listener(self,msg):
        if  msg[1] == 0:
            self.m_listCtrl1.SetItem(msg[0],2,msg[2])
            # 最长延迟ms
#====================20181126 kxhuang 增加sent自动包增加，便于直观浏览===========
            sent_packet = int(self.m_listCtrl1.GetItemText(msg[0],3))
            if sent_packet < 5000: #发送满5000后重置，清零
                self.m_listCtrl1.SetItem(msg[0],3,str(sent_packet+1))
            else:
                self.m_listCtrl1.SetItem(msg[0],3,'0')
            # 发送数据包数量
#==============================================================================
            self.m_listCtrl1.SetItem(msg[0],4,str('√'))
            # 网络状态
            self.m_listCtrl1.SetItem(msg[0],5,msg[3])
            # 网络丢包率
            #self.m_listCtrl1.SetItemBackgroundColour(msg[0],wx.Colour(255,255,255))
            # 更改背景色
            self.m_listCtrl1.SetItemTextColour(msg[0],wx.Colour(255,255,255))
            # 更改字体颜色
        else:
            self.m_listCtrl1.SetItem(msg[0],2,str('-'))
            # 最长延迟ms
            #====================2018.11.28 kxhuang 增加sent自动包增加，便于直观浏览===========
            sent_packet = int(self.m_listCtrl1.GetItemText(msg[0],3))
            if sent_packet < 5000: #发送满5000后重置，清零
                self.m_listCtrl1.SetItem(msg[0],3,str(sent_packet+1))
            else:
                self.m_listCtrl1.SetItem(msg[0],3,'0')
            # 发送数据包数量
#==============================================================================
            self.m_listCtrl1.SetItem(msg[0],4,str('×'))
            self.m_listCtrl1.SetItem(msg[0],5,'100%')
            #self.m_listCtrl1.SetItemBackgroundColour(msg[0],wx.Colour(255,0,0))
            #更改背景色
            self.m_listCtrl1.SetItemTextColour(msg[0],wx.Colour(255,0,0))
            #更改字体颜色
    # 启动线程
    def timer_do(self):
        th1 = Thread(target = th_do)
        th1.start()
        #ping算法

    # 调用启动线程方法
    def OnThread(self,event):
        self.timer_do()

    # 主窗口中右键删除后删除本地ini数据
    def OnDel( self, event ):
        del_ini = self.m_listCtrl1.GetFirstSelected()
        # 一定要赋值，否则list gui界面清除完后，鼠标会获取到-1的参数，从而会导致下列dbconf.ini的文件删除
        self.m_listCtrl1.DeleteItem(del_ini)
        # 删除鼠标选中的那一列
        conf = configparser.ConfigParser()
        conf.read('dbconf.ini')
        conf.remove_section(conf.sections()[del_ini])
        # 获取配置文件section元组，例如：['baidu','qq','163']，删除本地指定元素
        conf.write(open('dbconf.ini', 'w'))
        # 从gui界面删除后，再读取本地配置文件，删除并保存。

    # 主窗口鼠标右键菜单
    def right_hit(self,event):
        if self.m_listCtrl1.GetFirstSelected() != -1:
            # 空白地方都默认显示为-1，即没选择任何有数据的列
            self.menu2.Enable(True)#显示按钮
        else:
            self.menu2.Enable(False)#隐藏按钮
        
        self.PopupMenu(self.m_menu2, event.GetPosition())
        print (self.m_listCtrl1.GetFirstSelected())#调试用

#保留=================================================
    def __del__( self ):
        pass     
    def OnAdd(self,event): 
        pass    
    def OnSetMain(self,event): 
        pass
#=====================================================

# 添加主机配置函数===============================
    def AddConf(self, event):
        cfgFrame=CfgFrame(self) 
        #打开配置窗口    
        cfgFrame.Show(True)     
        #显示配置窗口
#==============================================

    def OnAbout(self,event):
        #创建一个带"OK"按钮的对话框。wx.OK是wxWidgets提供的标准ID
        dlg = wx.MessageDialog(self,"By kxhuang(2018)","About",wx.OK) #语法是(self, 内容, 标题, ID)
        dlg.ShowModal() #显示对话框
        dlg.Destroy()   #当结束之后关闭对话框

    def OnManual(self,event):
        #创建一个带"OK"按钮的对话框。wx.OK是wxWidgets提供的标准ID
        Manual_text=u'''
        1.菜单栏显示灰色是该功能暂未开发，做保留
        2.'Dealy(ms)'取值是取最大延迟值
        3.'Sent' 是每次发送4个Ping包，发送到5000后屏幕计数显示清零，重新计算。
        '''
        dlg = wx.MessageDialog(self,Manual_text,"Manual",wx.OK) #语法是(self, 内容, 标题, ID)
        dlg.ShowModal() #显示对话框
        dlg.Destroy()   #当结束之后关闭对话框

    def OnClose(self,event):
        self.Destroy()
        # 销毁窗口
    def AddExit(self,event):
    	self.Destroy()
    	# 销毁窗口
class CfgFrame(wx.Frame):  
# 添加主机配置窗口
    """docstring for CfgFrame"""
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "Ping Data", pos = wx.DefaultPosition, size = wx.Size( 400,200 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHints
        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Configuration" ), wx.VERTICAL )

        bSizer1 = wx.BoxSizer (wx.HORIZONTAL)

        self.m_staticText1 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Host：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        self.m_textCtrl2 = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.m_textCtrl2, 0, wx.ALL, 0 )
        
        self.m_staticText2 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Description：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        bSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )
        
        self.m_textCtrl1 = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.m_textCtrl1, 0, wx.ALL, 0 )
    
        sbSizer1.Add(bSizer1,1,wx.EXPAND,5)

        bSizer2 = wx.BoxSizer (wx.HORIZONTAL)
        self.m_button1 = wx.Button( sbSizer1.GetStaticBox(), wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button1, 0, wx.ALL, 5 )
        
        self.m_button2 = wx.Button( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button2, 0, wx.ALL, 5 )
        
        
        sbSizer1.Add( bSizer2, 1, wx.ALIGN_CENTER, 5 )



        self.SetSizer(sbSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind( wx.EVT_BUTTON, self.OnOK, id = self.m_button1.GetId() )
        # 确认绑定动作
        self.Bind( wx.EVT_BUTTON, self.OnCancel, id = self.m_button2.GetId() )
        # 取消时销毁窗口
    def OnOK(self, event): # 确认后的函数
        a = self.m_textCtrl2.GetValue()
        
        # 获取Host信息
        if a != "": # 防止用户输入空值

#=================================2018.11.29 kx  完善异常抛出===================
            try:
            
                conf = configparser.ConfigParser()
                # 调用configparser属性方法
                conf.read('dbconf.ini')
                # 读取本地文件
                sects = conf.sections()
                print (sects)
                b = self.m_textCtrl1.GetValue()
                # 获取Description信息
                conf.add_section(a)
                # 增加主机
            except (configparser.DuplicateSectionError) as reason:
                print('错误的原因是:', str(reason))#调试用
                ErrorTitle = '重复主机： ' + a
                dlg = wx.MessageDialog(self,ErrorTitle,"Error",wx.ICON_ERROR) #语法是(self, 内容, 标题, ID)
                dlg.ShowModal() #显示对话框
                dlg.Destroy()   #当结束之后关闭对话框
                
            else:
                self.Parent.m_listCtrl1.InsertItem(len(sects),str(a))
                # 输出到主窗口第一列
                self.Parent.m_listCtrl1.SetItem(len(sects),1,b)
                self.Parent.m_listCtrl1.SetItem(len(sects),3,'0')
                # 输出到主窗口第二列
                print ('hello')
                conf.set(a, "Host", a) 
                # 写入host信息   
                conf.set(a, "Description", b)
                # 写入description信息 
                print ('hello1')      
                conf.write(open('dbconf.ini', 'w'))
                # 保存
                print ('hello2')
                self.Destroy()
        else:
            dlg = wx.MessageDialog(self,"禁止输入空主机值","Error",wx.ICON_ERROR) #语法是(self, 内容, 标题, ID)
            dlg.ShowModal() #显示对话框
            dlg.Destroy()   #当结束之后关闭对话框
                
        # 销毁窗口
    def OnCancel(self, event): 
        self.Destroy()
        
        # 销毁窗口
#==========================================================================================================

class Popup(wx.MiniFrame):# 右下角弹出滑出通知

    def __init__(self, label, parent=None, title=u"伺服器网络中断"):
        wx.MiniFrame.__init__(self, parent, -1, title, wx.DefaultPosition, size=(280, 180),
                              style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
        # workarea = win32api.GetMonitorInfo(1)['Work']
        for monitor in win32api.EnumDisplayMonitors():
            monitor_info = win32api.GetMonitorInfo(monitor[0])
            if monitor_info['Flags'] == 1:
                break
        workarea = monitor_info['Work']

        pos = (workarea[2] - 280, workarea[3] - 180)
        bg = wx.Colour(255, 255, 225)
        self.SetBackgroundColour(bg)
        self.SetPosition(pos)
        text = wx.StaticText(self, -1, label)
        # font = wx.Font(13, wx.FONTENCODING_SYSTEM, wx.NORMAL, wx.NORMAL)
        # text.SetFont(font)
        text.SetBackgroundColour(bg)
        flags = AW_SLIDE | AW_VER_NEGATIVE | AW_ACTIVATE
        windll.user32.AnimateWindow(c_int(self.GetHandle()), c_int(600), c_int(flags))
        self.Refresh()
        self.Bind(wx.EVT_CLOSE, self.RemovePopup)

    def RemovePopup(self, evt=None):
        flags = AW_BLEND | AW_HIDE
        windll.user32.AnimateWindow(c_int(self.GetHandle()), c_int(600), c_int(flags))
        self.Destroy()
# wx启动
app = wx.App()
fm = MyFrame2(None)
fm.Show()
app.MainLoop()
