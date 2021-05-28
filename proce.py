class proce():
    def __init__(self, name, arrive, dura):
        self.name = name
        self.arrive = arrive
        self.dura = dura
        self.leftime = dura
        self.fintime = 0
        self.rtime = 0  # 周转时间
        self.val_rtime = 0  # 带权周转时间
        self.call=0         #相应比
    def __lt__(self, other):
        return self.dura < other.dura
