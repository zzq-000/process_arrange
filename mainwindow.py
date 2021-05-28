from tkinter import *
import login
import select
from proce import *
import queue


def getArrive(a: proce) -> int:
    return a.arrive


def getCall(a: proce) -> float:
    return a.call


class mainwindow():

    def reback(self):
        self.initface.destroy()
        login.login(self.root)

    def print(self):
        subwindow = Toplevel(self.root, )
        text = Text(subwindow)
        text.grid()
        text.insert(END, "pid   完成时间   周转时间   带权周转时间\n")
        for i in self.result:
            text.insert(END, " " + str(i.name) + "        " + str(i.fintime) + "         " + str(
                i.rtime) + "         " + str(i.valtime) + "\n")
        self.result.clear()
        return

    def prepro(self):
        a = len(self.pid)
        for i in range(a):
            node = proce(self.pid[i].get(), int(self.arrive[i].get()), int(self.dura[i].get()))
            self.p.append(node)
        return

    def FCFS(self):
        self.prepro()
        self.p.sort(key=getArrive, reverse=False)
        t = 0
        while len(self.p) != 0:
            process = self.p.pop(0)
            if t < process.arrive:
                t += process.dura + process.arrive - t
            else:
                t += process.dura
            process.fintime = t
            process.rtime = process.fintime - process.arrive
            process.valtime = process.rtime / process.dura
            self.result.append(process)
        self.print()
        return

    def RR(self):
        self.prepro()
        self.p.sort(key=getArrive, reverse=False)
        t = self.p[0].arrive
        tool = []
        while len(self.p) != 0 and self.p[0].arrive == t:
            tool.append(self.p.pop(0))
        while len(tool) != 0:
            temp = tool.pop(0)
            temp.leftime -= 1
            t += 1
            while len(self.p) != 0 and self.p[0].arrive == t:
                tool.append(self.p.pop(0))
            if temp.leftime == 0:
                temp.fintime = t
                temp.rtime = temp.fintime - temp.arrive
                temp.valtime = temp.rtime / temp.dura
                self.result.append(temp)
            else:
                tool.append(temp)
        self.print()
        return

    def SJF(self):
        self.prepro()
        self.p.sort(key=getArrive, reverse=False)
        tool = queue.PriorityQueue()
        t = self.p[0].arrive
        while len(self.p) != 0 and self.p[0].arrive == t:
            tool.put(self.p.pop(0))
        while tool.qsize() != 0:
            tt = tool.get()
            if t < tt.arrive:
                t = tt.arrive + tt.dura
            else:
                t += tt.dura
            while len(self.p) != 0 and self.p[0].arrive <= t:
                temp = self.p.pop(0)
                tool.put(temp)
            tt.fintime = t
            tt.rtime = tt.fintime - tt.arrive
            tt.valtime = tt.rtime / tt.dura
            self.result.append(tt)
        self.print()
        return

    def HRN(self):
        self.prepro()
        self.p.sort(key=getArrive, reverse=False)
        tool = []
        t = self.p[0].arrive
        while len(self.p) != 0 and self.p[0].arrive == t:
            tool.append(self.p.pop(0))
        while len(tool) != 0:
            for i in tool:
                i.call = (t - i.arrive + i.dura) / i.dura
            tool.sort(key=getCall, reverse=True)
            a = tool.pop(0)
            if t < a.arrive:
                t = a.arrive + a.dura
            else:
                t += a.dura
            a.fintime=t
            a.rtime=a.fintime-a.arrive
            a.valtime=a.rtime/a.dura
            self.result.append(a)
            while len(self.p) != 0 and self.p[0].arrive <= t:
                tool.append(self.p.pop(0))
        self.print()
        return

    def sure(self):
        for i in self.pid:
            i.grid_forget()
        for i in self.arrive:
            i.grid_forget()
        for i in self.dura:
            i.grid_forget()
        self.pid.clear()
        self.arrive.clear()
        self.dura.clear()
        num = int(self.sinput1.get())
        if (num > 0 and num <= 10):
            lb1 = Label(self.initface, text='进程')
            lb2 = Label(self.initface, text='到达时间')
            lb3 = Label(self.initface, text='服务时间')
            lb1.grid(row=2, column=1, padx=5)
            lb2.grid(row=2, column=2, padx=5)
            lb3.grid(row=2, column=3, padx=5)

            for i in range(num):
                input1 = Entry(self.initface, width=8)
                input1.grid(row=i + 3, column=1, padx=5, pady=2)
                self.pid.append(input1)
                input2 = Entry(self.initface, width=8)
                input2.grid(row=i + 3, column=2, padx=5, pady=2)
                self.arrive.append(input2)
                input3 = Entry(self.initface, width=8)
                input3.grid(row=i + 3, column=3, padx=5, pady=2)
                self.dura.append(input3)

            btnadd = Button(self.initface, text='FCFS', width=6, fg='black', font=('黑体', 10), command=self.FCFS)
            btndel = Button(self.initface, text='RR', width=6, fg='black', font=('黑体', 10), command=self.RR)
            btnsel = Button(self.initface, text='SJF', width=6, fg='black', font=('黑体', 10), command=self.SJF)
            btnupd = Button(self.initface, text='HRN', width=6, fg='black', font=('黑体', 10), command=self.HRN)
            btnback = Button(self.initface, text='退出登录', width=8, fg='black', font=('黑体', 10), command=self.reback)
            btnadd.grid(row=15, column=1, padx=3, ipady=2, pady=10)
            btnupd.grid(row=15, column=3, padx=3, ipady=2, pady=10)
            btndel.grid(row=16, column=1, padx=3, ipady=2, pady=10)
            btnsel.grid(row=16, column=3, padx=3, ipady=2, pady=10)
            btnback.grid(row=16, column=2, padx=3, ipady=2, pady=10)

    def __init__(self, master):
        self.root = master
        self.root.title('管理')
        self.initface = Frame(self.root, )
        self.initface.pack()
        self.pid = []
        self.arrive = []
        self.dura = []
        self.p = []
        self.result = []
        lb1 = Label(self.initface, text='请输入进程调度数')
        lb1.grid(row=1, column=1, padx=5)
        self.sinput1 = Entry(self.initface, width=14)
        self.sinput1.grid(row=1, column=2, padx=5)
        btnsure = Button(self.initface, text='确认', fg='black', font=('黑体', 9), command=self.sure)
        btnsure.grid(row=1, column=3, padx=5)
