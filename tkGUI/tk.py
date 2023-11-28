from tkinter import *
from tkinter import messagebox
import time
import threading


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

    def create(self):
        self.root = Tk()
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
        self.create_label_buttons(self.root)
        self.create_bottom(self.root)
        self.root.mainloop()

    def create_label_buttons(self, root):
        # 创建左侧标签
        labels = [Label(root, text=f"{i}", font=('Times', 16), justify='center', relief=RIDGE, anchor='w') for i in
                  self.items]
        for i, label in enumerate(labels):
            label.grid(row=i, column=0, sticky="nsew", padx=5, pady=1)
        # 创建右侧按钮
        buttons = [Button(root, text=f"子菜单", font=('Times', 16), justify='center', relief=RIDGE, anchor='w',
                          command=lambda index=i: self.run(index)) for i, label in
                   enumerate(self.items)]
        for i, button in enumerate(buttons):
            button.grid(row=i, column=1, sticky="nsew", padx=5, pady=1)

    def run(self, i):
        self.menu = self.menu.components[int(i)]
        # if self.menu.is_leaf():
        #     self.menu.run()
        #     current_menu = self.root_menu

    def modify(self, new_value):
        self.menu = new_value
        self.items = self.menu.direct_display()

    def create_bottom(self, root):
        self.create_btn = Button(root, text=f"按当前配置生成", font=('Times', 16), justify='center', relief=RAISED,
                                 anchor='w', command=lambda: self.thread_it(self.new_processing))
        self.create_btn.grid()

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




# 添加按钮防抖
class DebouncedButton:
    def __init__(self, button, debounce_time=1.0):
        self.button = button
        self.debounce_time = debounce_time
        self.last_click_time = 0
        self.button.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        current_time = time.time()
        if current_time - self.last_click_time < self.debounce_time:
            # 防抖处理：如果点击间隔太短，忽略此次点击
            return
        self.last_click_time = current_time
        # 执行你的逻辑代码
        print("Button clicked!")
