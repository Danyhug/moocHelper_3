VERSION 5.00
Begin VB.Form Form1 
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "智慧职教助手 - 控制台"
   ClientHeight    =   7050
   ClientLeft      =   105
   ClientTop       =   450
   ClientWidth     =   14130
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   7050
   ScaleWidth      =   14130
   ShowInTaskbar   =   0   'False
   StartUpPosition =   2  '屏幕中心
   Begin VB.Frame Frame2 
      Caption         =   "智慧职教功能区"
      BeginProperty Font 
         Name            =   "微软雅黑"
         Size            =   14.25
         Charset         =   134
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   6135
      Left            =   5040
      TabIndex        =   12
      Top             =   480
      Width           =   3975
      Begin VB.Frame Frame5 
         Height          =   2295
         Left            =   120
         TabIndex        =   13
         Top             =   600
         Width           =   3735
         Begin VB.OptionButton Option20 
            Caption         =   "是"
            Height          =   255
            Left            =   2160
            TabIndex        =   15
            Top             =   1200
            Width           =   495
         End
         Begin VB.OptionButton Option21 
            Caption         =   "否"
            Height          =   255
            Left            =   2760
            TabIndex        =   14
            Top             =   1200
            Width           =   615
         End
         Begin VB.Label Label4 
            Caption         =   "注：在智慧职教不能退出课程时会需要自行联系客服退出"
            BeginProperty Font 
               Name            =   "微软雅黑"
               Size            =   10.5
               Charset         =   134
               Weight          =   400
               Underline       =   0   'False
               Italic          =   0   'False
               Strikethrough   =   0   'False
            EndProperty
            ForeColor       =   &H000000FF&
            Height          =   615
            Left            =   120
            TabIndex        =   17
            Top             =   1560
            Width           =   3495
         End
         Begin VB.Label Label5 
            Caption         =   "全部完成功能自动获取答案(意味着会使用大号来获取答案并退出课程后加入，建议选否，自行使用小号获取答案再使用大号答题)"
            BeginProperty Font 
               Name            =   "微软雅黑"
               Size            =   10.5
               Charset         =   134
               Weight          =   400
               Underline       =   0   'False
               Italic          =   0   'False
               Strikethrough   =   0   'False
            EndProperty
            Height          =   1215
            Left            =   120
            TabIndex        =   16
            Top             =   240
            Width           =   3495
         End
      End
   End
   Begin VB.CommandButton readConf 
      Caption         =   "读取配置"
      BeginProperty Font 
         Name            =   "微软雅黑"
         Size            =   10.5
         Charset         =   134
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   735
      Left            =   1560
      TabIndex        =   11
      Top             =   2760
      Width           =   975
   End
   Begin VB.CommandButton saveConf 
      Caption         =   "保存配置"
      BeginProperty Font 
         Name            =   "微软雅黑"
         Size            =   10.5
         Charset         =   134
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   735
      Left            =   600
      TabIndex        =   10
      Top             =   5520
      Width           =   3015
   End
   Begin VB.CommandButton Command1 
      Caption         =   "清空保存账号"
      BeginProperty Font 
         Name            =   "微软雅黑"
         Size            =   10.5
         Charset         =   134
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   735
      Left            =   600
      TabIndex        =   9
      Top             =   4320
      Width           =   3015
   End
   Begin VB.Frame Frame3 
      Caption         =   "职教云功能区"
      BeginProperty Font 
         Name            =   "微软雅黑"
         Size            =   14.25
         Charset         =   134
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   6135
      Left            =   9600
      TabIndex        =   2
      Top             =   480
      Width           =   3975
      Begin VB.Frame Frame4 
         Height          =   1695
         Left            =   120
         TabIndex        =   3
         Top             =   600
         Width           =   3735
         Begin VB.TextBox Text1 
            BeginProperty Font 
               Name            =   "黑体"
               Size            =   10.5
               Charset         =   134
               Weight          =   400
               Underline       =   0   'False
               Italic          =   0   'False
               Strikethrough   =   0   'False
            EndProperty
            Height          =   375
            Left            =   120
            TabIndex        =   8
            Text            =   "Text1"
            Top             =   1080
            Width           =   2895
         End
         Begin VB.OptionButton Option2 
            Caption         =   "否"
            Height          =   375
            Left            =   3000
            TabIndex        =   6
            Top             =   240
            Width           =   615
         End
         Begin VB.OptionButton Option1 
            Caption         =   "是"
            Height          =   375
            Left            =   2400
            TabIndex        =   5
            Top             =   240
            Width           =   495
         End
         Begin VB.Label Label2 
            Caption         =   "输入评论内容："
            BeginProperty Font 
               Name            =   "微软雅黑"
               Size            =   10.5
               Charset         =   134
               Weight          =   400
               Underline       =   0   'False
               Italic          =   0   'False
               Strikethrough   =   0   'False
            EndProperty
            Height          =   255
            Left            =   120
            TabIndex        =   7
            Top             =   720
            Width           =   1455
         End
         Begin VB.Label Label3 
            Caption         =   "是否在课件评论区评论"
            BeginProperty Font 
               Name            =   "微软雅黑"
               Size            =   10.5
               Charset         =   134
               Weight          =   400
               Underline       =   0   'False
               Italic          =   0   'False
               Strikethrough   =   0   'False
            EndProperty
            Height          =   255
            Left            =   120
            TabIndex        =   4
            Top             =   240
            Width           =   2295
         End
      End
   End
   Begin VB.Frame Frame1 
      Caption         =   "提示"
      BeginProperty Font 
         Name            =   "微软雅黑"
         Size            =   14.25
         Charset         =   134
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   1815
      Left            =   600
      TabIndex        =   0
      Top             =   360
      Width           =   3255
      Begin VB.Label Label7 
         Caption         =   "保存后需要重新启动智慧职教助手"
         BeginProperty Font 
            Name            =   "宋体"
            Size            =   10.5
            Charset         =   134
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H000080FF&
         Height          =   495
         Left            =   360
         TabIndex        =   18
         Top             =   1080
         Width           =   2415
      End
      Begin VB.Label Label1 
         Caption         =   "更改参数后点击保存按钮即可"
         BeginProperty Font 
            Name            =   "宋体"
            Size            =   10.5
            Charset         =   134
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Left            =   360
         TabIndex        =   1
         Top             =   480
         Width           =   2415
      End
   End
   Begin VB.Line Line1 
      BorderStyle     =   2  'Dash
      X1              =   4440
      X2              =   4440
      Y1              =   240
      Y2              =   6840
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Declare Function GetPrivateProfileString Lib "kernel32" Alias "GetPrivateProfileStringA" (ByVal lpApplicationName As String, ByVal lpKeyName As Any, ByVal lpDefault As String, ByVal lpReturnedString As String, ByVal nSize As Long, ByVal lpFileName As String) As Long
Private Declare Function WritePrivateProfileString Lib "kernel32" Alias "WritePrivateProfileStringA" (ByVal lpApplicationName As String, ByVal lpKeyName As Any, ByVal lpString As Any, ByVal lpFileName As String) As Long
Public zjyAddActivity As String, zjyAddActivityContent As String

Private Function read(k As String, value As String) As String
    ' 该函数用来读取配置文件，传入option和value，返回字符串
    Dim t As String
    Dim read_OK As Long
    t = String(255, 0)
    read_OK = GetPrivateProfileString(k, value, "0", t, 256, App.Path & "\conf\conf.ini")
    read = t
End Function

Private Function save(k As String, value As String, v As String) As Integer
    ' 该函数用来写入配置文件，传入option和value，返回结果
    '参数一： Section Name (节的名称)。
    '参数二： 节下面的项目名称。
    '参数三： 项目的内容。
    '参数四： ini配置文件的路径名称。
    Dim t As String
    Dim write_OK As Long
    t = String(255, 0)
    write_OK = WritePrivateProfileString(k, value, v, App.Path & "\conf\conf.ini")
    save = write_OK
End Function

Private Sub Command1_Click()
    Kill App.Path & "\conf\moocUser"
    MsgBox "清除成功！"
End Sub

Private Sub Form_Load()
    readConf = True
End Sub


Private Sub readConf_Click()
    doAllWorkAutoGetAnswer = read("mooc", "doAllWorkAutoGetAnswer") ' 智慧职教全部完成功能自动获取答案
    If doAllWorkAutoGetAnswer = True Then
        Option20.value = True
    Else
        Option21.value = True
    End If

    zjyAddActivity = read("zjy", "zjyaddactivity")  ' 职教云是否评论
    If zjyAddActivity = True Then
        Option1.value = True
    Else
        Option2.value = True
    End If
    
    zjyAddActivityContent = read("zjy", "zjyAddactivityContent")    ' 职教云评论内容
    Text1.Text = zjyAddActivityContent
    
    MsgBox "读取配置完毕"
End Sub

Private Sub saveConf_Click()
    r = save("mooc", "doAllWorkAutoGetAnswer", Option20.value)
    r = save("zjy", "zjyaddactivity", Option1.value)
    r = save("zjy", "zjyAddactivityContent", Text1.Text)
    
    MsgBox "保存成功！"
End Sub
