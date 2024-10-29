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
def db_connect():
    try:
        return pymysql.connect(**db_config)
    except pymysql.err.OperationalError as oe:
        messagebox.showerror("数据库连接错误", f"无法连接到数据库: {oe}")
    except pymysql.err.InternalError as ie:
        messagebox.showerror("内部数据库错误", f"数据库内部错误: {ie}")
    except Exception as e:
        messagebox.showerror("未知错误", f"数据库连接时发生未知错误: {e}")

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
    try:
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
    except Exception as e:
        messagebox.showerror("创建数据库和表时出错", f"创建数据库和表时发生错误: {e}")

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

        # 如果验证通过，继续执行数据库操作
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

        # 如果验证通过，继续执行数据库操作
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

def main():
    try:
        create_database_and_table()

        while True:
            print("\n日常计划管理系统")
            print("1. 添加任务")
            print("2. 显示所有任务")
            print("3. 更新任务")
            print("4. 删除任务")
            print("5. 退出系统")
            choice = input("请选择操作: ")

            if choice == '1':
                title = input("请输入任务标题: ")
                description = input("请输入任务描述: ")
                due_date = input("请输入任务截止日期 (YYYY-MM-DD): ")
                status = input("请输入任务状态 (未开始/进行中/已完成): ")
                add_task(title, description, due_date, status)
            elif choice == '2':
                tasks = get_all_tasks()
                for task in tasks:
                    print(task)
            elif choice == '3':
                task_id = int(input("请输入要更新的任务ID: "))
                title = input("请输入新的任务标题: ")
                description = input("请输入新的任务描述: ")
                due_date = input("请输入新的任务截止日期 (YYYY-MM-DD): ")
                status = input("请输入新的任务状态 (未开始/进行中/已完成): ")
                update_task(task_id, title, description, due_date, status)
            elif choice == '4':
                task_id = int(input("请输入要删除的任务ID: "))
                delete_task(task_id)
            elif choice == '5':
                print("谢谢使用，系统退出！")
                break
            else:
                print("无效的选择，请重新输入。")
    except Exception as e:
        messagebox.showerror("主程序错误", f"主程序运行时发生错误: {e}")

if __name__ == "__main__":
    main()
