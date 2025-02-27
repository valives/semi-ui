from tkinter import *
from tkinter import messagebox
import time
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = Tk()


class TkCreate(object):
    """
    图形化界面的面板
    """

    def __init__(self, root_menu, menu, title, state, processing):
        self.processing_thread = None
        self.root_menu = root_menu
        self.menu = menu
        self.title = title
        self.state = state
        self.items = None
        self.root = None
        self.create_btn = None
        self._processing = processing
        self.f = None
        self.lf = None

    def create(self):
        self.root = root
        self.root.title(self.title)
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        width = 1024  # 窗口大小值
        height = 768
        # 计算中心坐标
        cen_x = (sw - width) / 2
        cen_y = (sh - height) / 2
        # 设置窗口大小并居中
        self.root.geometry('%dx%d+%d+%d' % (width, height, cen_x, cen_y))
        self.root.resizable(False, False)  # 将窗口设置为不可改变大小
        self.items = self.menu.direct_display()
        self.create_bottom(self.root)
        self.create_label_buttons(self.root)
        self.root.mainloop()

    def ttk_create(self):
        self.root = ttk.Window(title="窗口名字",  # 设置窗口的标题
                               themename="litera",  # 设置主题
                               size=(1240, 800),  # 窗口的大小
                               position=(0, 0),  # 窗口所在的位置
                               minsize=(0, 0),  # 窗口的最小宽高
                               maxsize=(1920, 1080),  # 窗口的最大宽高
                               resizable=None,  # 设置窗口是否可以更改大小
                               alpha=1.0, )
        self.f = ttk.Labelframe(width=1240, height=600)
        self.f.pack()
        # self.lf = ttk.Frame(width=300, height=80)
        # self.lf.pack()
        self.items = self.menu.direct_display()
        self.ttk_create_label_buttons(self.f)
        self.ttk_create_bottom(self.root)
        self.root.mainloop()

    def ttk_create_label_buttons(self, root):
        labels = [Label(root, text=f"{i}", font=('Times', 14), justify='center', relief=RIDGE, anchor='w', width=20) for
                  i in
                  self.items]
        for i, label in enumerate(labels):
            label.grid(row=i, column=0, sticky="nsew", padx=5, pady=1)
        # 创建右侧按钮
        buttons = [Button(root, text=f"子菜单", font=('Times', 14), justify='center', relief=RIDGE, anchor='w',
                          command=lambda index=i: self.run(index)) for i, label in
                   enumerate(self.items)]
        for i, button in enumerate(buttons):
            button.grid(row=i, column=1, sticky="nsew", padx=5, pady=1)

    def create_label_buttons(self, root, is_root=0):
        title = "子菜单"
        if is_root:
            title = '选择'
        # 创建左侧标签
        labels = [Label(root, text=f"{i}", font=('Times', 16), justify='center', relief=RIDGE, anchor='w') for i in
                  self.items]
        for i, label in enumerate(labels):
            label.grid(row=i+1, column=0, sticky="nsew", padx=5, pady=1)
        # 创建右侧按钮

        buttons = [Button(root, text=f"{title}", font=('Times', 16), justify='center', relief=RIDGE, anchor='w',
                          command=lambda index=i: self.run(index)) for i, label in
                   enumerate(self.items)]

        for i, button in enumerate(buttons):
            button.grid(row=i+1, column=1, sticky="nsew", padx=5, pady=1)

    def run(self, i):
        is_root = 1
        self.menu = self.menu.components[int(i)]
        if self.menu.is_leaf():
            self.menu.run()
            self.menu = self.root_menu
            is_root = 0
        self.clear_all()  # 清除所有按钮
        self.items = self.menu.direct_display()
        self.create_label_buttons(self.root, is_root)

    def ttk_create_bottom(self, root):
        self.create_btn = ttk.Button(root, text="按当前配置生成", bootstyle=SUCCESS,
                                     command=lambda: self.thread_it(self.new_processing))
        self.create_btn.grid()

    def create_bottom(self, root):
        self.create_btn = Button(root, text="按当前配置生成", font=('Times', 16), justify='center', relief=RAISED,
                                 anchor='w', command=lambda: self.thread_it(self.new_processing))
        self.create_btn.grid(row=0, column=0, padx=10, pady=10)

    def thread_it(self, func):  # 可以让按键弹起
        self.create_btn.config(state="disabled", text='Loading......')
        # 创建线程
        t = threading.Thread(target=func)
        # 守护线程
        t.daemon = True
        # 启动线程
        t.start()

    def new_processing(self):
        self._processing()
        self.create_btn.config(state="normal", text='按当前配置生成')
        messagebox.showinfo("提示", "处理完成，文件已输出至 output 文件夹中")

    def clear_all(self):
        for key in self.root.winfo_children():
            if key.cget("text") != "按当前配置生成":  # 确保按钮是Button类实例且文本不是"按当前配置生成"
                key.destroy()  # 销毁所有标签和按钮



