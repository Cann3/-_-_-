import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import simpledialog
import tkinter.font as tkfont
import pymysql
from PIL import Image, ImageTk
from PIL.Image import Resampling  # 显式导入Resampling模块
import re

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123584',
    'database': 'daily_planner',
    'charset': 'utf8'
}


# 封装数据库连接
# 封装数据库连接
def db_connect():
    try:
        return pymysql.connect(**db_config)
    except pymysql.err.OperationalError as oe:
        messagebox.showerror("数据库连接错误", f"无法连接到数据库: {oe}")
        raise
    except pymysql.err.InternalError as ie:
        messagebox.showerror("内部数据库错误", f"数据库内部错误: {ie}")
        raise
    except Exception as e:
        messagebox.showerror("未知错误", f"数据库连接时发生未知错误: {e}")
        raise

# 封装SQL执行
def execute_sql(connection, query, params=None):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
            return cursor
    except pymysql.err.ProgrammingError as pe:
        messagebox.showerror("SQL语法错误", f"执行SQL语句时发生语法错误: {pe}")
    except pymysql.err.IntegrityError as ie:
        messagebox.showerror("数据完整性错误", f"数据完整性问题: {ie}")
    except pymysql.err.DataError as de:
        messagebox.showerror("数据错误", f"数据错误: {de}")
    except pymysql.err.MySQLError as mse:
        messagebox.showerror("MySQL错误", f"MySQL错误: {mse}")
    except Exception as e:
        messagebox.showerror("执行SQL语句时出错", f"执行SQL语句时出错: {e}")




# 创建数据库和表
def create_database_and_table():
    conn = db_connect()
    with conn:
        execute_sql(conn, "CREATE DATABASE IF NOT EXISTS daily_planner")
        execute_sql(conn, "USE daily_planner")
        execute_sql(conn, """
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            due_date DATE,
            status VARCHAR(50)
        )
        """)


# CRUD操作
# 添加任务
def validate_date(date_text):
    # 使用正则表达式验证日期格式，例如 YYYY-MM-DD
    if re.match(r"\d{4}-\d{2}-\d{2}", date_text):
        return True
    return False


def add_task(title, description, due_date, status):
    try:
        # 数据验证
        if not title or len(title) > 255:
            raise ValueError("任务标题不能为空且长度不能超过255个字符！")
        if not validate_date(due_date):
            raise ValueError("截止日期格式不正确！应为 YYYY-MM-DD。")
        if status not in ["未开始", "进行中", "已完成"]:
            raise ValueError("状态必须是预定义的选项之一！")

        # 执行数据库操作
        conn = db_connect()
        with conn:
            execute_sql(conn, "INSERT INTO tasks (title, description, due_date, status) VALUES (%s, %s, %s, %s)",
                        (title, description, due_date, status))
    except ValueError as ve:
        messagebox.showerror("错误", str(ve))
    except Exception as e:
        messagebox.showerror("添加任务时出错", f"添加任务时发生错误: {e}")



# 查询所有任务
def get_all_tasks():
    try:
        conn = db_connect()
        with conn:
            cursor = execute_sql(conn, "SELECT * FROM tasks")
            return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("获取任务时出错", f"获取所有任务时发生错误: {e}")
        return []



# 更新任务
def update_task(task_id, title, description, due_date, status):
    try:
        # 数据验证
        if not title or len(title) > 255:
            raise ValueError("任务标题不能为空且长度不能超过255个字符！")
        if not validate_date(due_date):
            raise ValueError("截止日期格式不正确！应为 YYYY-MM-DD。")
        if status not in ["未开始", "进行中", "已完成"]:
            raise ValueError("状态必须是预定义的选项之一！")

        # 执行数据库操作
        conn = db_connect()
        with conn:
            execute_sql(conn, "UPDATE tasks SET title=%s, description=%s, due_date=%s, status=%s WHERE id=%s",
                        (title, description, due_date, status, task_id))
    except ValueError as ve:
        messagebox.showerror("错误", str(ve))
    except Exception as e:
        messagebox.showerror("更新任务时出错", f"更新任务时发生错误: {e}")



# 删除任务
def delete_task(task_id):
    try:
        conn = db_connect()
        with conn:
            execute_sql(conn, "DELETE FROM tasks WHERE id=%s", (task_id,))
    except Exception as e:
        messagebox.showerror("删除任务时出错", f"删除任务时发生错误: {e}")



class TaskManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("日常计划信息系统")
        self.geometry("1800x1200")

        # 加载图片并调整尺寸以适应窗口
        image = Image.open("background.jpg")  # 替换为你的图片路径
        photo = ImageTk.PhotoImage(
            image=image.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Resampling.LANCZOS))

        # 创建一个Canvas组件，并设置它的尺寸
        canvas = tk.Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        canvas.pack(side='top', fill='both', expand=True)

        # 在Canvas上添加图片
        canvas.create_image(0, 0, image=photo, anchor='nw')

        # 让`photo`变量保持引用，否则图片可能不会显示
        canvas.image = photo

        art_font = tkfont.Font(family="华文行楷", size=48, weight="bold")
        canvas.create_text(100, 50, text="日常计划信息系统", font=art_font, fill="blue", anchor="nw")
        # 创建菜单栏
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # 创建菜单
        menubar.add_command(label="添加任务", command=self.add_task)
        menubar.add_command(label="刷新任务", command=self.refresh_task_list)
        menubar.add_command(label="显示任务", command=self.show_tasks)
        menubar.add_command(label="更新任务", command=self.update_task)
        menubar.add_command(label="删除任务", command=self.delete_task)
        menubar.add_command(label="退出", command=self.quit)

        # 初始绘制任务
        self.refresh_task_list()

    def refresh_task_list(self):
        # 清除旧的任务
        for item in self.winfo_children()[0].find_all():
            if "task" in self.winfo_children()[0].gettags(item):
                self.winfo_children()[0].delete(item)

        # 获取所有任务
        tasks = get_all_tasks()

        # 绘制新的任务
        y_position = 200  # 开始绘制任务的高度
        for task in tasks:
            if task[4] != "已完成":
                self.winfo_children()[0].create_rectangle(100, y_position - 20, 700, y_position + 20, fill="red",
                                                          tags="task")
                self.winfo_children()[0].create_rectangle(100, y_position - 20, 700, y_position + 20, fill="white",
                                                          tags="task")
                self.winfo_children()[0].create_text(110, y_position,
                                                     text=f"编号: {task[0]}, 标题: {task[1]}, 描述: {task[2]}, 截止日期: {task[3]}, 状态: {task[4]}",
                                                     anchor="w", tags="task")
                y_position += 50

    def add_task(self):
        # 创建一个新的顶级窗口
        dialog = tk.Toplevel(self)
        dialog.title("添加任务")
        dialog.geometry('300x200+600+400')
        # 添加一个输入框用于任务标题
        label_title = tk.Label(dialog, text="任务标题:")
        label_title.grid(row=0, column=0)
        entry_title = tk.Entry(dialog)
        entry_title.grid(row=0, column=1)

        # 添加一个输入框用于任务描述
        label_desc = tk.Label(dialog, text="任务描述:")
        label_desc.grid(row=1, column=0)
        entry_desc = tk.Entry(dialog)
        entry_desc.grid(row=1, column=1)

        # 添加一个输入框用于任务截止日期
        label_data = tk.Label(dialog, text="任务截止日期:")
        label_data.grid(row=2, column=0)
        entry_data = tk.Entry(dialog)
        entry_data.grid(row=2, column=1)

        # 添加一个输入框用于任务状态
        label_status = tk.Label(dialog, text="任务状态:")
        label_status.grid(row=3, column=0)

        status_options = ["未开始", "进行中", "已完成"]
        status_var = tk.StringVar()
        status_combobox = ttk.Combobox(dialog, textvariable=status_var, values=status_options, width=18)
        status_combobox.grid(row=3, column=1)
        status_combobox.current(0)  # 设置默认值为第一个选项

        # 添加一个提交按钮
        def submit():
            # 获取输入框中填写的标题
            title = entry_title.get()
            # 获取文本框中输入的所有内容
            desc = entry_desc.get()
            due_date = entry_data.get()
            status = status_var.get()
            add_task(title, desc, due_date, status)
            self.refresh_task_list()
            # 关闭对话框
            dialog.destroy()

        # 创建提交按钮，点击后执行submit函数
        button_submit = tk.Button(dialog, text="提交", command=submit)
        # 将按钮放置在对话框中
        button_submit.grid(row=4, column=1, columnspan=3)

    def show_tasks(self):
        # 创建一个临时的Tkinter窗口
        window = tk.Tk()
        window.title("任务列表")
        tasks = get_all_tasks()
        # 创建Treeview组件
        tree = ttk.Treeview(window, columns=("任务编号", "任务标题", "任务描述", "任务截止日期", "任务状态"),
                            show="headings")
        tree.heading("任务编号", text="任务编号")
        tree.heading("任务标题", text="任务标题")
        tree.heading("任务描述", text="任务描述")
        tree.heading("任务截止日期", text="任务截止日期")
        tree.heading("任务状态", text="任务状态")

        tree.pack(padx=10, pady=10)
        index = 0
        # 清空现有的数据
        tree.delete(*tree.get_children())

        # 将任务添加到Treeview中
        for task_info in tasks:
            # 假设task_info是一个包含所有信息的列表或元组
            index += 1  # 每次循环增加index
            tree.insert("", "end", values=(task_info))

        # 运行Tkinter事件循环
        window.mainloop()

    def update_task(self):
        task_id = simpledialog.askinteger("更新任务", "请输入要更新的任务ID:")
        # 创建一个新的顶级窗口
        dialog = tk.Toplevel(self)
        dialog.title("更新任务")
        dialog.geometry('300x200+600+400')
        # 添加一个输入框用于任务编号
        label_title = tk.Label(dialog, text="任务标题:")
        label_title.grid(row=0, column=0)
        entry_title = tk.Entry(dialog)
        entry_title.grid(row=0, column=1)
        # 添加一个输入框用于任务标题
        label_title = tk.Label(dialog, text="任务标题:")
        label_title.grid(row=0, column=0)
        entry_title = tk.Entry(dialog)
        entry_title.grid(row=0, column=1)

        # 添加一个输入框用于任务描述
        label_desc = tk.Label(dialog, text="任务描述:")
        label_desc.grid(row=1, column=0)
        entry_desc = tk.Entry(dialog)
        entry_desc.grid(row=1, column=1)

        # 添加一个输入框用于任务截止日期
        label_data = tk.Label(dialog, text="任务截止日期:")
        label_data.grid(row=2, column=0)
        entry_data = tk.Entry(dialog)
        entry_data.grid(row=2, column=1)

        # 添加一个输入框用于任务状态
        label_status = tk.Label(dialog, text="任务状态:")
        label_status.grid(row=3, column=0)
        status_options = ["未开始", "进行中", "已完成"]
        status_var = tk.StringVar()
        status_combobox = ttk.Combobox(dialog, textvariable=status_var, values=status_options, width=18)
        status_combobox.grid(row=3, column=1)
        status_combobox.current(0)  # 设置默认值为第一个选项

        # 添加一个提交按钮
        def submit():
            # 获取输入框中填写的标题
            title = entry_title.get()
            # 获取文本框中输入的所有内容
            desc = entry_desc.get()
            due_date = entry_data.get()
            status = status_var.get()
            add_task(title, desc, due_date, status)
            self.refresh_task_list()
            # 关闭对话框
            dialog.destroy()

        # 创建提交按钮，点击后执行submit函数
        button_submit = tk.Button(dialog, text="提交", command=submit)
        # 将按钮放置在对话框中
        button_submit.grid(row=4, column=1, columnspan=3)

    def delete_task(self):
        task_id = simpledialog.askinteger("删除任务", "请输入要删除的任务ID:")
        if task_id is not None:
            delete_task(task_id)
            self.refresh_task_list()
            messagebox.showinfo("提示", "任务删除成功")


if __name__ == "__main__":
    app = TaskManagerApp()
    create_database_and_table()
    app.mainloop()