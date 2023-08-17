import os
import sys
if sys.__stdout__ is None or sys.__stderr__ is None:
    os.environ['KIVY_NO_CONSOLELOG'] = '1'
from kivy.core.text import LabelBase
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
import kivy
import pymongo
# from pymongo import MongoClient
# from pymongo.server_api import ServerApi
import excute
basedir = os.path.dirname(__file__)
LabelBase.register('Roboto', 'msyhl.ttc')
print(basedir)
kivy.require("2.2.1")
Builder.load_file("style.kv")
Window.size = 700, 600


class MyLayout(Widget):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.id_num = ""
        self.password = ""
        self.save_status = False
        self.course_order = []
        self.show_info = True

    def check_input(self, input):
        if input == "":
            self.ids.status.text = "1"
            return 1

        else:
            if "," in input:
                if input.replace(",", "").isnumeric():
                    self.ids.status.text = "2"
                    return 2
                else:
                    self.ids.status.text = "4"
                    return 4
            elif "，" in input:
                if input.replace("，", "").isnumeric():
                    self.ids.status.text = "3"
                    return 3
                else:
                    self.ids.status.text = "4"
                    return 4
            else:
                self.ids.status.text = "4"
                return 4

    def qulified(self, id_num):
        # res = collection.find_one({"id_num": id_num})
        res = {"time": 10000}
        # todo fix this bug
        # res = None
        if res == None:
            print("用户未注册")
            return -1
        elif res["time"] == 0:
            print("次数已用完")
            return 0
        else:
            # store the password and id_num and time-1 in the database
            print(self.password)
            # collection.update_one({"id_num": id_num}, {
            #                       "$set": {"password": self.password, "time": res["time"]-1}})
            return 1

    # 检查输入
    def get(self):
        id_num = self.ids.account_num.text
        password = self.ids.password.text
        course_order = self.ids.course_order.text

        check = self.qulified(id_num)
        input_check = self.check_input(course_order)
        if id_num == '' or password == '':
            # if not, show a message box
            # tk.messagebox.showinfo(title='提示', message='请输入用户名和密码')
            self.ids.status.text = "请输入用户名和密码"
        elif check == -1:
            self.save_status = False
            # tk.messagebox.showinfo(title='提示', message='请先注册')
            self.ids.status.text = "用户未注册，请找管理员先注册"
        elif check == 0:
            self.save_status = False
            # tk.messagebox.showinfo(title='提示', message='次数已用完')
            self.ids.status.text = "次数已用完"
        elif check == 1:
            # default order
            if input_check == 1:
                self.course_order = "default"
                # tk.messagebox.showinfo(title='提示', message='检查成功')
                self.ids.status.text = "检查成功"
                # id_entry.config(state='disabled')
                self.save_status = True
            # custom order with ","
            elif input_check == 2:
                self.course_order = course_order.split(',')
                # change the button to clicked
                # tk.messagebox.showinfo(title='提示', message='检查成功')
                self.ids.status.text = "检查成功"
                # id_entry.config(state='disabled')
                self.save_status = True
            # custom order with "，"
            elif input_check == 3:
                self.course_order = course_order.split('，')
                # change the button to clicked
                # tk.messagebox.showinfo(title='提示', message='检查成功')
                self.ids.status.text = "检查成功"
                # id_entry.config(state='disabled')
                self.save_status = True
            elif input_check == 4:
                # tk.messagebox.showinfo(title='提示', message='请输入用逗号隔开的数字')

                self.ids.status.text = "请输入用逗号隔开的数字"
                self.save_status = False

    def run(self):
        self.id_num = self.ids.account_num.text
        self.password = self.ids.password.text
        print(self.id_num)
        print(self.password)
        print(self.course_order)
        # check the save button is clicked or not
        if self.save_status == False:
            # tk.messagebox.showinfo(title='提示', message='请点击<检查输入>按钮')
            self.ids.status.text = "请点击<检查输入>按钮"
        else:
            self.save_status = False
            # if yes, destroy the window
            if self.course_order != 'initial' and self.course_order != 'default':
                try:

                    excute.execute(self.id_num, self.password, usr_setting=True,
                                   usr_setting_course_order=self.course_order)
                except:
                    self.ids.status.text = "已关闭浏览器窗口，请重新运行程序"

            else:
                try:
                    excute.execute(self.id_num, self.password, usr_setting=False,
                                   usr_setting_course_order=[])
                except:
                    self.ids.status.text = "已关闭浏览器窗口，请重新运行程序"

    def load_info(self):
        try:
            with open(os.path.join(basedir, "login.txt"), "x") as f:
                f.write("initial")
        except:
            pass
        with open(os.path.join(basedir, "login.txt"), "r") as f:
            txt = f.read().splitlines()
        if txt[0] == "initial":
            # tk.messagebox.showinfo(title='提示', message='未保存用户名和密码，请输入用户名和密码并保存')
            self.ids.status.text = "未保存用户名和密码，请输入用户名和密码并保存"
        else:
            self.id_num = txt[0]
            self.password = txt[1]
            self.ids.account_num.text = self.id_num
            self.ids.password.text = self.password

    def save_info(self):
        self.id_num = self.ids.account_num.text
        self.password = self.ids.password.text
        id_num = self.id_num
        password = self.password

        if id_num == '' or password == '':
            # if not, show a message box
            # tk.messagebox.showinfo(title='提示', message='请输入用户名和密码')
            self.ids.status.text = "请输入用户名和密码"
        else:
            try:
                with open(os.path.join(basedir, "login.txt"), "x") as f:
                    f.write("initial")
            except:
                pass

            with open(os.path.join(basedir, "login.txt"), "w") as f:
                f.write(id_num+"\n"+password)
            # tk.messagebox.showinfo(title='提示', message='保存到本地成功')
            self.ids.status.text = "保存到本地成功"

    def show_pass(self):
        if self.show_info == False:
            # change kv file textinput password property to false
            # 设置密码模式为True，改为*
            print(1)
            self.ids.password.password = True
            self.ids.password_show_btn.text = "显示密码"
            self.show_info = True

        else:
            print(2)
            self.ids.password.password = False
            self.ids.password_show_btn.text = "隐藏密码"
            self.show_info = False
        print(self.show_info)


class CourseeApp(App):
    def build(self):
        return MyLayout()


if __name__ == "__main__":
    # try:
    #     cluster = pymongo.MongoClient(
    #         "mongodb+srv://dylan:DylanBee23@cluster0.a4ejgtt.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
    # except:
    #     cluster = pymongo.MongoClient(
    #         "mongodb://dylan:DylanBee23@ac-hpnfpjp-shard-00-00.a4ejgtt.mongodb.net:27017,ac-hpnfpjp-shard-00-01.a4ejgtt.mongodb.net:27017,ac-hpnfpjp-shard-00-02.a4ejgtt.mongodb.net:27017/?ssl=true&replicaSet=atlas-a94cse-shard-0&authSource=admin&retryWrites=true&w=majority")
    # db = cluster["user"]
    # collection = db["member"]
    CourseeApp().run()
