import cv2
import numpy as np
import pyautogui
import tkinter as tk

# تحديد الحد الأدنى والحد الأقصى لللون الأحمر في تدرج BGR
lower_red = (0, 0, 100)
upper_red = (100, 100, 255)


# دالة للتحقق مما إذا كانت الصورة مفتوحة أم لا
def is_image_open():
    return pyautogui.screenshot() is not None


# دالة لتحريك المؤشر إلى أكبر نقطة حمراء
def move_cursor_to_red():
    if is_image_open():
        # التقاط لقطة شاشة للصورة المفتوحة
        screenshot = pyautogui.screenshot()

        # تحويل لقطة الشاشة إلى صورة OpenCV
        image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # تحويل الصورة إلى تدرج اللون HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # إنشاء قناع للون الأحمر
        red_mask = cv2.inRange(hsv_image, lower_red, upper_red)

        # البحث عن مواقع البكسلات الحمراء
        red_pixel_locations = cv2.findNonZero(red_mask)

        if red_pixel_locations is not None:
            # حساب أكبر نقطة حمراء
            max_area = 0
            max_point = None
            for point in red_pixel_locations:
                area = cv2.contourArea([point])
                if area > max_area:
                    max_area = area
                    max_point = point

            if max_point is not None:
                x = max_point[0][0]
                y = max_point[0][1]
                pyautogui.moveTo(x, y)
                label.config(text="تم العثور على أكبر نقطة حمراء!")
            else:
                label.config(text="لم يتم العثور على أي نقطة حمراء في الصورة.")
        else:
            label.config(text="لم يتم العثور على أي نقطة حمراء في الصورة.")
    else:
        label.config(text="لا يوجد صورة مفتوحة حاليًا.")


# دالة لفحص وجود صورة حمراء وعرض رسالة
def check_for_red_image():
    if is_image_open():
        move_cursor_to_red()
    else:
        label.config(text="لا يوجد صورة مفتوحة حاليًا.")


# إنشاء نافذة رسومية
root = tk.Tk()
root.title("تحريك الماوس إلى صورة حمراء")

# إنشاء زر للتحقق من وجود صورة حمراء
button = tk.Button(root, text="فحص الصورة", command=check_for_red_image)
button.pack(pady=10)

# إنشاء عنصر نصي لعرض الرسائل
label = tk.Label(root, text="")
label.pack(pady=10)

# تشغيل الحلقة الرئيسية لعرض النافذة
root.mainloop()
