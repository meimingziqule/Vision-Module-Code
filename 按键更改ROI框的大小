#在调整ROI前加入边界检查。(√)
#只在所有调整完成后重新绘制一次ROI。
#考虑使用更稳定的统计方法（如均值或中位数）来确定颜色阈值。（可以尝试一下）
#处理多个按钮同时按下的情况，确保每个按钮的效果都被正确应用。（√）
import sensor, image, time, pyb
from pyb import Pin
#初始化一次auto_roi->=找到auto_roi中的红色色块并返回外接矩形框坐标->=将该坐标赋值给auto_roi->=由statistics得到新的颜色阈值->=从第二步开始循环
red_thresholds = (47, 0, 78, 11, 65, -31)    #定义变量
lab =  [0,0,0,0,0,0]
x,y,w,h = 0,0,40,40
#ROI = (x,y,w,h)
sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QQVGA2 (128×160)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

pin_value = [1,1,1,1]  # 0 1 0 1
pin_num = [0,1,2,3]  

lab =  [0,0,0,0,0,0]


def pin_IN(pin_num):
    for i in range(len(pin_num)):#设置引脚为输入引脚并获取引脚值
        p_in = Pin('P'+str(pin_num[i]), Pin.IN, Pin.PULL_UP)
        pin_value[i] = p_in.value()

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    #p_in = Pin('P7', Pin.IN, Pin.PULL_UP)#设置p_in为输入引脚，并开启上拉电阻
    #value = p_in.value() # get value, 0 or 1#读入p_in引脚的值
    ROI = (x,y,w,h)
    get_auto_roi_blobs = img.find_blobs([red_thresholds],pixels_threshold=50, area_threshold=50)
    img.draw_rectangle(ROI, lab = (255,255,255))   #画ROI框
    pin_IN(pin_num)#设置GPIO引脚输入
    if pin_value[0] == 0:
        x += 5
        if x >= 320:
            x = 0
        pyb.delay(100)#消除按键抖动
    if pin_value[1] == 0:
        y += 5
        if y >= 240:
            y = 0
        pyb.delay(100)    
    if pin_value[2] == 0:
        w += 5
        if w >= 240-x:
            w = 40
        pyb.delay(100)    
    if pin_value[3] == 0:
        h += 5
        if h >=240-y:
            h = 40
        pyb.delay(200)   #有问题找延时
        
    
    img.draw_rectangle(ROI, lab = (255,255,255))   #画roi框
    
    statistics_Data = img.get_statistics(roi = ROI )

    lab[0] =  statistics_Data.l_median()
    lab[1] =  statistics_Data.a_median()
    lab[2] =  statistics_Data.b_median()

    #计算颜色阈值，这样写的话，颜色阈值是实时变化的，后续想要什么效果可以自己修改
    red_thresholds = (lab[0]-20,lab[0]+20, lab[1]-20, \
                        lab[1]+20,lab[2]-20, lab[2]+20,)
    
    #img.binary([red_thresholds]) #二值化看图像效果
    print('red_thresholds:')
    print(red_thresholds)        #打印输出颜色阈值
    print("fps:")
    fps = 'fps:'+str(clock.fps())
    img.draw_string(0, 0, fps, lab=(255, 0, 0), scale=2)
    img.draw_string(0, 20, str(x), lab=(255, 255, 255), scale=2)
    img.draw_string(0, 40, str(y), lab=(255, 255, 255), scale=2)
    img.draw_string(0, 60, str(w), lab=(255, 255, 255), scale=2)
    img.draw_string(0, 80, str(h), lab=(255, 255, 255), scale=2)
    
    print(clock.fps())
    img.draw_rectangle(ROI, lab = (255,255,255))   #画roi框


