# 作者：你大爹
# 用意：OpenMV阈值
#OpenMV坐标系
#需连接按键
#按键  openmv
# 1     P0
# 2     P1
# 3     P2
# 4     P3
# 5     P7
# 6     P8
# 7     P9


#4. ①3,4按键一起按：roi框位置大小调节模型 1-4分别为x,y,w,h的增加按键
#   ②roi模式下，6，7一起按切换“--”模式，再次6,7一起按切换回“++”模式
#5.按键7切换为自动阈值模式，按键8为二值化图像预览
# 颜色追踪时需要控制环境光线稳定，避免识别标志物的色彩阈值发生改变
import sensor, image, time,math,pyb,time
import ustruct
from pyb import UART, LED
from pyb import Pin

#yellow_threshold  = (54, 78, -3, 44, 33, 127)#设置黄色阈值（原数据）
#yellow_threshold  = (25, 80, 64, -24, 47, 108)#设置黄色阈值（改后）、
baoguang = 80000

roi_change_step  = 2#roi变化步长
roi_jiajian_flag = 0#roi加减模式切换标志位
roi_set_one_flag= 1#roi初始化一次标志位
auto_thresholds_roi_num= [73,61,6,7]
auto_thresholds_roi = (int(auto_thresholds_roi_num[0]),int(auto_thresholds_roi_num[1]),int(auto_thresholds_roi_num[2]),int(auto_thresholds_roi_num[3]))#自动阈值roi

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)   # Set frame size to QQVGA2 (128×160)
sensor.skip_frames(n=2000) #在更改设置后，跳过n张照片，等待感光元件变稳定
sensor.set_auto_exposure(False,baoguang)              # Create a clock object to track the FPS.
sensor.set_auto_gain(False) #使用颜色识别时需要关闭自动自动增益
sensor.set_auto_whitebal(False)#使用颜色识别时需要关闭自动自动白平衡

clock = time.clock() #追踪帧率
uart = UART(3,115200)   #设置串口波特率，与stm32一致
uart.init(115200, bits=8, parity=None, stop=1 )

def find_max_blobs(blobs, img):
    if not blobs:
        print("没有找到任何 blobs")
        return None
    try:
        red_blob = max(blobs, key=lambda b: b.pixels())
        #print("x:%d,y:%d,w:%d,h:%d" % (red_blob.cx(), red_blob.cy(), red_blob.w(), red_blob.h()))
        img.draw_cross(red_blob.cx(),red_blob.cy())
        img.draw_rectangle(red_blob.rect())
        print("色块像素数量：%d" % red_blob.pixels())
        return red_blob
    except Exception as e:
        print("发生错误: ", e)
        return None



pin_value = [1,1,1,1,1,1,1,1]  # 0 1 0 1  高低电平
pin_num = [0,1,2,3,6,7,8,9]  #pin口选择
jia_jian_flag = 0#手动阈值加减模式切换标志位，包含roi模式切换标志位
red_thresholds_num = [0, 100, 38, 77, 5, 69]
#初始阈值
red_thresholds = (red_thresholds_num[0], red_thresholds_num[1], red_thresholds_num[2], red_thresholds_num[3], red_thresholds_num[4], red_thresholds_num[5])   
def handle_buttons(image):#传入画面
    #红色阈值，roi，阈值加减模式标志位，roi加减模式标志位，roi步长
    global red_thresholds_num,red_thresholds,auto_thresholds_roi_num,auto_thresholds_roi,jia_jian_flag,roi_jiajian,roi_jiajian_flag,roi_change_step
    img.draw_rectangle(int(auto_thresholds_roi_num[0]),int(auto_thresholds_roi_num[1]),int(auto_thresholds_roi_num[2]),int(auto_thresholds_roi_num[3]), color=(255,255,255))
    #默认roi++模式  6,7按键同时按下为切换
    if roi_jiajian_flag == 0:
        img.draw_string(80,0,"roi++", color=(0,0,255))
        if pin_value[5] == 0 and pin_value[6] == 0:
            roi_jiajian_flag = 1
            pyb.delay(500)
        if pin_value[0] == 0:
            auto_thresholds_roi_num[0] += roi_change_step
            if auto_thresholds_roi_num[0] >= image.width():
                auto_thresholds_roi_num[0] = 0
            pyb.delay(100)#消除按键抖动
        if pin_value[1] == 0:
            auto_thresholds_roi_num[1] += roi_change_step
            if auto_thresholds_roi_num[1] >= image.height():
                auto_thresholds_roi_num[1] = 0
            pyb.delay(200)    
        if pin_value[2] == 0:
            auto_thresholds_roi_num[2] += roi_change_step
            if auto_thresholds_roi_num[2] >= image.width()-auto_thresholds_roi_num[0]:
                auto_thresholds_roi_num[2] = roi_change_step
            pyb.delay(200)    
        if pin_value[3] == 0:
            auto_thresholds_roi_num[3] += 5
            if auto_thresholds_roi_num[3] >=image.height()-auto_thresholds_roi_num[1]:
                auto_thresholds_roi_num[3] = roi_change_step
            pyb.delay(200)   #有问题找延时
        if pin_value[6] == 0:
            img.draw_rectangle((int(auto_thresholds_roi_num[0]),int(auto_thresholds_roi_num[1]),int(auto_thresholds_roi_num[2]),int(auto_thresholds_roi_num[3])), color = (255,255,255))
            statistics_Data = img.get_statistics(roi = (int(auto_thresholds_roi_num[0]),int(auto_thresholds_roi_num[1]),int(auto_thresholds_roi_num[2]),int(auto_thresholds_roi_num[3])) )
            color_L_median = statistics_Data.l_median()     #分别赋值LAB的众数
            color_A_median = statistics_Data.a_median()
            color_B_median = statistics_Data.b_median()
            #计算颜色阈值，这样写的话，颜色阈值是实时变化的，后续想要什么效果可以自己修改
            
            red_thresholds_num[0] = color_L_median-20
            red_thresholds_num[1] = color_L_median+20
            red_thresholds_num[2] = color_A_median-20
            red_thresholds_num[3] = color_A_median+20
            red_thresholds_num[4] = color_B_median-20
            red_thresholds_num[5] = color_B_median+20
            red_thresholds = (red_thresholds_num[0],red_thresholds_num[1],red_thresholds_num[2],red_thresholds_num[3],red_thresholds_num[4],red_thresholds_num[5])
            img.binary([red_thresholds]) #二值化看图像效果                    
            pyb.delay(200)   #有问题找延时         
        if pin_value[7] == 0:
            img.binary([red_thresholds]) #二值化看图像效果
    #roi模式下1,2同时按切换成roi--模式        
    elif roi_jiajian_flag ==1:
        img.draw_string(80,0,"roi--", color=(0,0,255))
        if pin_value[5] == 0 and pin_value[6] == 0::
            roi_jiajian_flag = 0
            pyb.delay(500)
        if pin_value[0] == 0:
            auto_thresholds_roi_num[0] -= roi_change_step
            if auto_thresholds_roi_num[0] <= 0:
                auto_thresholds_roi_num[0] = image.width()
            pyb.delay(100)#消除按键抖动
        if pin_value[1] == 0:
            auto_thresholds_roi_num[1] -= roi_change_step
            if auto_thresholds_roi_num[1] <= 0:
                auto_thresholds_roi_num[1] = image.height()
            pyb.delay(200)    
        if pin_value[2] == 0:
            auto_thresholds_roi_num[2] -= roi_change_step
            if auto_thresholds_roi_num[2] <= roi_change_step:
                auto_thresholds_roi_num[2] = image.width()-auto_thresholds_roi_num[0]
            pyb.delay(200)    
        if pin_value[3] == 0:
            auto_thresholds_roi_num[3] -= roi_change_step
            if auto_thresholds_roi_num[3] <=roi_change_step:
                auto_thresholds_roi_num[3] = image.height()-auto_thresholds_roi_num[1]
            pyb.delay(200)   #有问题找延时
        if pin_value[6] == 0:
            img.draw_rectangle((int(auto_thresholds_roi_num[0]),int(auto_thresholds_roi_num[1]),int(auto_thresholds_roi_num[2]),int(auto_thresholds_roi_num[3])), color = (255,255,255))
            statistics_Data = img.get_statistics(roi = (int(auto_thresholds_roi_num[0]),int(auto_thresholds_roi_num[1]),int(auto_thresholds_roi_num[2]),int(auto_thresholds_roi_num[3])) )
            color_L_median = statistics_Data.l_median()     #分别赋值LAB的众数
            color_A_median = statistics_Data.a_median()
            color_B_median = statistics_Data.b_median()
            #计算颜色阈值，这样写的话，颜色阈值是实时变化的，后续想要什么效果可以自己修改
            
            red_thresholds_num[0] = color_L_median-20
            red_thresholds_num[1] = color_L_median+20
            red_thresholds_num[2] = color_A_median-20
            red_thresholds_num[3] = color_A_median+20
            red_thresholds_num[4] = color_B_median-20
            red_thresholds_num[5] = color_B_median+20
            red_thresholds = (red_thresholds_num[0],red_thresholds_num[1],red_thresholds_num[2],red_thresholds_num[3],red_thresholds_num[4],red_thresholds_num[5])
            img.binary([red_thresholds]) #二值化看图像效果                    
            pyb.delay(200)   #有问题找延时         
        if pin_value[7] == 0:
            img.binary([red_thresholds]) #二值化看图像效果

def pin_IN(pin_num):
    for i in range(len(pin_num)):#设置引脚为输入引脚并获取引脚值
        p_in = Pin('P'+str(pin_num[i]), Pin.IN, Pin.PULL_UP)
        pin_value[i] = p_in.value()


def sending_data(color,cx,cy):
    global uart
    data = ustruct.pack("<bbbbbb",
    0x2c,0x12,int(color),int(cx),int(cy),0x5b)

    uart.write(data)
    #for i in data:
        #print("data的内容是：    ",hex(i))

while(True):
    img = sensor.snapshot()
    red_blobs = img.find_blobs([red_thresholds], x_stride=5, y_stride=5, pixels_threshold=5 )
    if red_blobs:
        color_status = ord('B')
        for r in red_blobs:

            img.draw_rectangle((r[0],r[1],r[2],r[3]),color=(255,255,255))
            img.draw_cross(r[5], r[6],size=2,color=(255,255,255))
            img.draw_string(r[0], (r[1]-10), "red", color=(0,0,255))
            print("red_blob:中心X坐标",r[5],"中心Y坐标",r[6],"识别颜色类型","红色")
            
            sending_data(color_status,r[5],r[6])
    #只会执行一次  为了设置img的宽和高        
    if roi_set_one_flag== 1:        
        auto_thresholds_roi_num= [img.width()/2,img.height()/2,5,5]
        auto_thresholds_roi = (auto_thresholds_roi_num[0],auto_thresholds_roi_num[1],auto_thresholds_roi_num[2],auto_thresholds_roi_num[3])#自动阈值roi
        roi_set_one_flag= 0
    else:
        pass


    pin_IN(pin_num)#设置GPIO引脚输入
    handle_buttons(img)#处理按钮按键响应

    img.draw_rectangle((int(auto_thresholds_roi_num[0]),int(auto_thresholds_roi_num[1]),int(auto_thresholds_roi_num[2]),int(auto_thresholds_roi_num[3])), color=(255,255,255))
    img.draw_string(0,0,str(red_thresholds_num[0]),color=(0,0,255))
    img.draw_string(0,10,str(red_thresholds_num[1]),color=(0,0,255))
    img.draw_string(0,20,str(red_thresholds_num[2]),color=(0,0,255))
    img.draw_string(0,30,str(red_thresholds_num[3]),color=(0,0,255))    
    img.draw_string(0,40,str(red_thresholds_num[4]),color=(0,0,255))
    img.draw_string(0,50,str(red_thresholds_num[5]),color=(0,0,255))
    print('red_thresholds:',red_thresholds)
    print(red_thresholds)        #打印输出颜色阈值
    print("auto_thresholds_roi_num:",auto_thresholds_roi_num)
    print("auto_thresholds_roi:",auto_thresholds_roi)