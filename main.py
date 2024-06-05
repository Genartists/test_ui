from tkinter import *
from tkinter import filedialog, messagebox
import cv2
import time
from functools import partial

import numpy as np
from PIL import Image
import PIL.ImageTk
from tkinter.font import BOLD
import my_module

listItem = [
    "Cân bằng histogram",
    "Tách ngưỡng",
    "Lấy âm bản",
    "Biến đổi Logarith",
    "Tăng tương phản"
]
listFunc = [
    my_module.hist_equal,
    my_module.thresholding,
    my_module.negative,
    my_module.logarith,
    my_module.normalize
]

def process(current):
    global cv_final
    for i in range(5):
        btn[i].configure(relief=RAISED)
    btn[current].configure(relief=SUNKEN)

    start_time = time.time()
    cv_final = listFunc[current](cv_img)[0]#
    end_time = time.time()
    print('Thời gian thực hiện phép %s là %f ms' %
          (listItem[current], (end_time - start_time) * 1000))
    pil_final = cv2.cvtColor(cv_final, cv2.COLOR_BGR2RGB)
    new = PIL.ImageTk.PhotoImage(Image.fromarray(pil_final))
    imgR.configure(image=new)
    imgR.image = new


def update_UI(old, new):
    imgL.configure(image=old)
    imgR.configure(image=new)
    imgL.image = old
    imgR.image = new
    labelL.pack()
    imgL.pack()
    btn_open.pack(pady=5)
    labelR.pack()
    imgR.pack()
    btn_save.pack(pady=5)
    for i in range(5):
        btn[i] = Button(footer, text=listItem[i],
                        relief=RAISED, command=partial(process, i))
        btn[i].grid(row=int(i / 5), column=i % 5)


def resize_image(img, desired_size=600):
    old_size = img.shape[:2]

    ratio = float(desired_size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])

    img = cv2.resize(img, (new_size[1], new_size[0]))

    delta_w = desired_size - new_size[1]
    delta_h = desired_size - new_size[0]
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)

    color = [0, 0, 0]
    new_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return new_img


def select_img():
    global cv_img
    path = filedialog.askopenfilename()
    try:
        cv_img = cv2.imread(path)
        cv_img = resize_image(cv_img)
        pil_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        old = PIL.ImageTk.PhotoImage(Image.fromarray(pil_img))
        new = PIL.ImageTk.PhotoImage(Image.fromarray(pil_img))
        b.destroy()
        update_UI(old, new)
    except:
        if (path != ''):
            messagebox.showerror("Lỗi", "Vui lòng chọn đúng định dạng ảnh!")


def another_img():
    global cv_img
    path = filedialog.askopenfilename()
    try:
        cv_img = cv2.imread(path)
        cv_img = resize_image(cv_img)
        pil_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        old = PIL.ImageTk.PhotoImage(Image.fromarray(pil_img))
        new = PIL.ImageTk.PhotoImage(Image.fromarray(pil_img))
        update_UI(old, new)
    except:
        if (path != ''):
            messagebox.showerror("Lỗi", "Vui lòng chọn đúng định dạng ảnh!")


def save_img():
    filetypes = [
        ('PNG files', '*.png'),
        ('JPEG files', '*.jpg'),
        ('All files', '.')
    ]
    path = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=filetypes)
    if not path:
        messagebox.showerror("Error", "Không có file nào được chọn!")
    else:
        try:
            if isinstance(cv_final, np.ndarray):
                cv2.imwrite(path, cv_final)
            else:
                messagebox.showerror("Error", "Ảnh không đúng định dạng!")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", f"Không lưu được file: {e}")


win = Tk()
win.title("Xử lý ảnh")
###########################
header = Frame()
content = Label(
    header, text="CHƯƠNG TRÌNH THỰC HIỆN CÁC PHÉP XỬ LÝ ẢNH", font=("Arial", 20, BOLD))
content.pack()
header.pack(side=TOP)
###########################
body = Frame()

bodyL = LabelFrame(body)
labelL = Label(bodyL, text="Ảnh ban đầu", font=(10))
imgL = Label(bodyL)
btn_open = Button(bodyL, text="Chọn ảnh khác", command=another_img)
bodyL.pack(side=LEFT)

bodyR = LabelFrame(body)
labelR = Label(bodyR, text="Ảnh sau khi xử lý", font=(10))
imgR = Label(bodyR)
btn_save = Button(bodyR, text="Lưu kết quả", command=save_img)
bodyR.pack(side=RIGHT)

body.pack(side=TOP, pady=10)
##########################
footer = Frame()
btn = [0] * 5
footer.pack(side=BOTTOM)
##########################
b = Button(text="Chọn file ảnh", command=select_img)
b.pack(ipadx=10, ipady=10, pady=10)
cv_img, cv_final = '', ''

if __name__ == "__main__":
    mainloop()
