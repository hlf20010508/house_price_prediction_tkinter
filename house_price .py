import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
import custom_widget as tkpp
import pandas as pd
import joblib
import os
from PIL import Image,ImageTk
import ttkbootstrap.themes.user
import datetime
import lists
import numpy as np
from time import sleep
import tkinter.messagebox

model_path='model.pkl'
train_origin_path='train.csv'
test_origin_path='test.csv'
test_modified_path='test_modified.csv'
submission_path='submission.csv'
images_path='picture'
main_page_bg_path='images/main_page_bg.jpg'
sub_bg_path='images/sub_bg.jpg'
pre_single_path='images/pre_single_bg.jpg'

style=ttkb.Style(theme='litera')
root=style.master
sw=root.winfo_screenwidth()//2
sh=root.winfo_screenheight()//2

main_page_window_size=(900,650)
data_browser_window_size=(1400,800)
data_browser_search_window_size=(1400,300)
pre_data_page_window_size=(250,610)
predict_page_search_window_size=(250,100)
pre_single_page_window_size=data_browser_window_size
element_select_window_size=pre_single_page_window_size
analysis_page_window_size=(935,800)
message_box_window_size=(200,100)

image_size=(200,200)

def resize(image,k):
    size=image.size
    return image.resize((int(size[0]*k),int(size[1]*k)))

def load_npy(name):
    return list(np.load('npy/%s.npy'%name,allow_pickle=True))

def set_window_position(root,pos):
    ws=pos
    root.geometry(str(ws[0])+'x'+str(ws[1]))
    root.geometry('+{}+{}'.format(sw-ws[0]//2,sh-ws[1]//2))
    root.resizable(0,0)

def multipleList(root,area,data=None,height=5,width=100,width_column=20,anchor='n',padding=(0,0,0,0),style='info',place_anchor='nw',relx=0,rely=0.1,command=None):#padding为表外留白
    ac=[]
    for i in range(len(area)):
        ac.append(i)
    ac=tuple(ac)
    
    tv=ttkb.Treeview(
        root,
        columns=ac,
        show='headings',
        height=height,
        padding=padding,
        bootstyle=style)
    
    for i in range(len(area)):
        tv.column(
            ac[i],
            width=int(width/len(area)),
            minwidth=width_column,
            stretch=True,
            anchor=anchor)
                
        tv.heading(ac[i],text=area[i])
        
    tv.bind('<Double-Button-1>',command)
    tv.place(anchor=place_anchor,relx=relx,rely=rely)
    
    if isinstance(data,pd.core.frame.DataFrame):
        for index, row in data.iterrows():
            tv.insert('','end',values=row.tolist())
    elif data==None:
        return tv
    else:
        for i in data:
            tv.insert('','end',values=i)
        return tv

class message_box:
    def __init__(self,content):
        self.root=ttkb.Toplevel(title=' ')
        set_window_position(self.root,message_box_window_size)
        ttkb.Label(
            self.root,
            text=content,
            bootstyle='dark').place(anchor='n',relx=0.5,rely=0.2)
        ttkb.Button(
            self.root,
            text='确定',
            bootstyle='primary',
            command=self.exit).place(anchor='n',relx=0.5,rely=0.55)
    
    def exit(self):
        self.root.destroy()

class data_browser:
    def __init__(self,path):
        if path==train_origin_path:
            self.root=ttkb.Toplevel(title='训练数据集')
        elif path==test_origin_path:
            self.root=ttkb.Toplevel(title='测试数据集')

        set_window_position(self.root,data_browser_window_size)
        
        image=Image.open(sub_bg_path)
        image=resize(image,1)
        bg=ImageTk.PhotoImage(image)
        cv =ttkb.Canvas(self.root,width=data_browser_window_size[0],height=data_browser_window_size[1])
        cv.pack()
        cv.create_image(data_browser_window_size[0]//2,data_browser_window_size[1]//2,image=bg)
        
        self.data=pd.read_csv(path)
        self.data2=self.data
        self.data=self.data.astype(str)
        self.features=list(self.data)
        size=len(self.data)
        
        self.balloon=None

        ttkb.Button(
            self.root,
            text='退出',
            bootstyle='primary',
            command=self.exit).place(anchor='n',relx=0.04,rely=0.05)
        
        self.search_layer=ttkb.Combobox(
            self.root,
            values=self.features,
            width=8,
            bootstyle="primary")
        self.search_layer.place(anchor='n',relx=0.75,rely=0.05)

        # self.search_layer.bind('<<ComboboxSelected>>',self.seperate)

        self.search_entry = ttkb.Entry(
            self.root,
            width=9,
            bootstyle='dark')
        self.search_entry.place(anchor='n', relx=0.83, rely=0.05)
        self.search_entry.bind('<Enter>',lambda event=True,x=0.80,y=0.05-0.03:self.balloon_show(event,x,y))
        self.search_entry.bind('<Leave>',self.balloon_hide)

        # self.left_search_entry=None
        # self.label_to=None
        # self.right_search_entry=None

        search_button=ttkb.Button(
            self.root,
            text='搜索',
            bootstyle='primary',
            command=self.search)
        search_button.place(anchor='n',relx=0.9,rely=0.05)
        
        multipleList(
            self.root,
            self.features,
            self.data,
            width=data_browser_window_size[0],
            width_column=100,
            height=38)
        
        show_size=ttkb.Label(
            self.root,
            bootstyle='info',
            text='共 '+str(size)+' 个样本')
        show_size.place(anchor='n',relx=0.05,rely=0.91)

        self.root.mainloop()

    # def seperate(self,event):
    #     _type=self.data2.dtypes[self.search_layer.get()]
    #     if _type==np.dtype('float64') or _type==np.dtype('int64'):
    #         self.search_entry.destroy()

    #         self.left_search_entry=ttkb.Entry(
    #             self.root,
    #             width=4,
    #             bootstyle='dart')
    #         self.left_search_entry.place(anchor='nw', relx=0.79, rely=0.05)

    #         self.label_to=ttkb.Label(
    #             self.root,
    #             text='~',
    #             bootstyle='dart')
    #         self.label_to.place(anchor='nw', relx=0.83, rely=0.055)

    #         self.right_search_entry=ttkb.Entry(
    #             self.root,
    #             width=4,
    #             bootstyle='dart')
    #         self.right_search_entry.place(anchor='nw', relx=0.844, rely=0.05)
    #     else:
    #         self.left_search_entry.destroy()
    #         self.label_to.destroy()
    #         self.right_search_entry.destroy()

    #         self.search_entry = ttkb.Entry(
    #             self.root,
    #             width=9,
    #             bootstyle='dark')
    #         self.search_entry.place(anchor='n', relx=0.83, rely=0.05)

    def balloon_show(self,event,x,y):
        _type=self.data2.dtypes[self.search_layer.get()]
        if _type==np.dtype('float64') or _type==np.dtype('int64'):
            self.balloon=ttkb.Label(
                self.root,
                text="输入单个数或用'-'分隔")
        else:
            self.balloon=ttkb.Label(
                self.root,
                text='输入单个值')
        self.balloon.place(relx=x,rely=y)
                
    def balloon_hide(self,event):
        self.balloon.destroy()

    def search(self):
        feature=self.search_layer.get()
        if self.data2.dtypes[self.search_layer.get()] == object:
            result=self.data.loc[self.data[feature]==self.search_entry.get()]
        else:
            try:
                sp=self.search_entry.get().split('-')
                if len(sp)==2:
                    bottom,top=sp
                    result=self.data.loc[(self.data2[feature]>=float(bottom))&(self.data2[feature]<=float(top))]
                else:
                    result=self.data.loc[self.data2[feature]==float(sp[0])]
                # print(bottom,top)
                
            except:
                message_box('请规范输入！')

        if len(result)>0:
            show=ttkb.Toplevel(title='搜索结果  共 '+str(len(result))+' 条结果')
            set_window_position(show,data_browser_search_window_size)
            multipleList(
                show,
                self.features,
                result,
                width=data_browser_window_size[0],
                width_column=100,
                height=16,
                style='success',
                rely=0.01)
        else:
            message_box('没有搜索到结果！')
    
    def exit(self):
        global root
        self.root.destroy()
        root.destroy()
        

class analysis_page:
    def __init__(self):
        self.root=ttkb.Toplevel(title='分析')
        
        set_window_position(self.root,analysis_page_window_size)
        
        size,self.image_names,self.images,self.images_origin=self.get_images()
        
        image=Image.open(sub_bg_path)
        image=resize(image,1)
        bg=ImageTk.PhotoImage(image)
        cv =ttkb.Canvas(self.root,width=analysis_page_window_size[0],height=analysis_page_window_size[1])
        cv.pack()
        cv.create_image(analysis_page_window_size[0]//2,analysis_page_window_size[1]//2,image=bg)
        
        pos=(3,4)
        self.c=0
        
        ttkb.Button(
            self.root,
            text='退出',
            bootstyle='primary',
            command=self.quit).place(relx=0.05,rely=0.02)
        
        pady=40
        x=analysis_page_window_size[0]
        y=analysis_page_window_size[1]-pady
        relx=1/8
        rely=1/6
        for i in range(pos[0]):
            if self.c>=size:
                break
            for j in range(pos[1]):
                if self.c>=size:
                    break
                frame=ttkb.Frame(self.root)
                frame.place(anchor='center',x=x*(relx+2*relx*j),y=y*(rely+2*rely*i)+pady)
                tk.Button(
                    frame,
                    image=self.images[self.c],
                    command=lambda x=self.c:self.zoom(x)).pack()
                ttkb.Label(
                    frame,
                    text=self.image_names[self.c]).pack()
                self.c+=1
        
        self.root.mainloop()
    
    def get_images(self):
        image_names=[i for i in os.listdir(images_path) if not i.startswith('.')]
        size=len(image_names)
        images=[]
        images_origin=[]
        for i in image_names:
            image=Image.open(images_path+'/'+i)
            if i=='热力图.jpg':
                image=resize(image,0.3)
                # image=image.resize((750,700),Image.BILINEAR)
            elif i=='多维关系图.jpg':
                image=resize(image,0.25)
                # image=image.resize((350,700),Image.BILINEAR)
            elif i=='前四个数量最多的房型密度图.jpg':
                image=resize(image,0.25)
                # image=image.resize((900,700),Image.BILINEAR)
            images_origin.append(image)
            image=image.resize(image_size,Image.BILINEAR)
            image=ImageTk.PhotoImage(image)
            images.append(image)
        image_names=[i.split('.')[0] for i in image_names]
        return size,image_names,images,images_origin
    
    def zoom(self,x):
        c=x
        root=ttkb.Toplevel(title='详情')
        
        size=list(self.images_origin[c].size)
        size[1]+=40
        set_window_position(root,size)
        
        cv =ttkb.Canvas(root,width=size[0],height=size[1])
        cv.pack()
        
        image=ImageTk.PhotoImage(self.images_origin[c])
        
        pic = cv.create_image(size[0]//2,(size[1]-40)//2,image=image)
        
        ttkb.Button(
            root,
            text='确定',
            command=lambda x=root:self.exit(x)).place(anchor='s',relx=0.5,rely=0.98)
        
        root.mainloop()
    
    def exit(self,x):
        global root
        x.destroy()
        root.destroy()
    
    def quit(self):
        global root
        self.root.destroy()
        root.destroy()
    

class pre_data_page:
    def __init__(self):
        self.root=ttkb.Toplevel(title='测试集预测')
        set_window_position(self.root,pre_data_page_window_size)
        
        try:
            self.data=pd.read_csv(submission_path)
        except FileNotFoundError:
            self.clf=joblib.load(model_path)
            self.data=self.predict()
        
        self.data['Price']=self.data['Price'].map(lambda x:'%.2f美元'%x)
        
        size=len(self.data)
        
        image=Image.open(sub_bg_path)
        image=resize(image,1)
        bg=ImageTk.PhotoImage(image)
        cv =ttkb.Canvas(self.root,width=pre_data_page_window_size[0],height=pre_data_page_window_size[1])
        cv.pack()
        cv.create_image(pre_data_page_window_size[0]//2,pre_data_page_window_size[1]//2,image=bg)
        
        ttkb.Button(
            self.root,
            text='退出',
            bootstyle='primary',
            command=self.exit).place(relx=0.05,rely=0.04)
        
        ttkb.Label(
            self.root,
            text='Id',
            bootstyle='primary').place(relx=0.30,rely=0.05)
        
        self.search_entry=ttkb.Entry(
            self.root,
            width=7,
            bootstyle='primary')
        self.search_entry.place(relx=0.4,rely=0.04)
        
        search_button=ttkb.Button(
            self.root,
            text='搜索',
            bootstyle='primary',
            command=self.search)
        search_button.place(relx=0.75,rely=0.04)
        
        multipleList(
                self.root,
                ['Id','Price'],
                self.data,
                width=pre_data_page_window_size[0]-20,
                width_column=60,
                height=29,
                place_anchor='n',
                relx=0.5)
        
        show_size=ttkb.Label(
            self.root,
            bootstyle='info',
            text='共 '+str(size)+' 个样本')
        show_size.place(relx=0.05,rely=0.93)
        
        self.root.mainloop()
        
    def predict(self):
        test_data=pd.read_csv(test_origin_path)
        test_sub=test_data.pop('Id')
        test_sub=test_sub.astype(int)
        test_data=pd.read_csv(test_modified_path)
        y_pred = self.clf.predict(test_data)
        price = []
        for i in range(len(test_sub)):
            price.append(y_pred[i])
        df_price = pd.DataFrame({'Price':price})
        # 将id列和预测出来的房价列拼接并输出submission文件
        df=pd.concat([test_sub,df_price],axis=1)
        df.to_csv(submission_path,header=['Id','Price'], index=False)
        return df
    
    def search(self):
        feature='Id'
        result=self.data.loc[self.data[feature]==int(self.search_entry.get())]
        if len(result)>0:
            show=ttkb.Toplevel(title='搜索结果  共 '+str(len(result))+' 条结果')
            set_window_position(show,predict_page_search_window_size)
            multipleList(
                show,
                ['Id','Price'],
                result,
                width=pre_data_page_window_size[0]-20,
                width_column=100,
                height=3,
                style='success',
                place_anchor='n',
                relx=0.5,
                rely=0.01)
        else:
            message_box('没有搜索到结果！')
    
    def exit(self):
        global root
        self.root.destroy()
        root.destroy()
            
class pre_single_page:
    def __init__(self):
        self.clf=joblib.load(model_path)
        self.root=ttkb.Toplevel(title='样本预测')
        set_window_position(self.root,pre_single_page_window_size)
        
        self.features_combobox=lists.features_combobox
        
        image=Image.open(pre_single_path)
        image=resize(image,0.5)
        bg=ImageTk.PhotoImage(image)
        cv =ttkb.Canvas(self.root,width=pre_single_page_window_size[0],height=pre_single_page_window_size[1])
        cv.pack()
        cv.create_image(pre_single_page_window_size[0]//2,pre_single_page_window_size[1]//2+7,image=bg)
        
        x=150
        combobox_y=130
        padx=300
        pady=70
        self.Region=self.combobox('Region',load_npy('Region'),'Los Angeles',x,combobox_y)
        self.State=self.combobox('State',load_npy('State'),'CA',x+padx,combobox_y)
        self.seperate(x-100,combobox_y-26,13,1,style='warning')
        
        date_entry_y=combobox_y+pady
        self.Listed_On=self.date_entry('Listed On','2021-01-13',x,date_entry_y)
        self.Last_Sold_On=self.date_entry('Last Sold On','2017-06-30',x+padx,date_entry_y)
        self.seperate(x-100,date_entry_y-26,13,1,style='info')
        
        elements_y=date_entry_y+pady
        self.Type=self.elements('Type','SingleFamily',x,elements_y)
        self.Heating=self.elements('Heating','Central',x+padx,elements_y)
        self.Cooling=self.elements('Cooling','Central Air',x,elements_y+pady)
        self.Parking=self.elements('Parking','Garage, Garage - Attached, Covered',x+padx,elements_y+pady)
        self.Bedrooms=self.elements('Bedrooms','3',x,elements_y+pady*2)
        self.Flooring=self.elements('Flooring','Wood',x+padx,elements_y+pady*2)
        self.Appliances_included=self.elements('Appliances included','Dishwasher, Dryer, Garbage disposal, Microwave, Range / Oven, Refrigerator, Washer',x,elements_y+pady*3)
        self.Laundry_features=self.elements('Laundry features','In Garage',x+padx,elements_y+pady*3)
        self.Parking_features=self.elements('Parking features','Garage, Garage - Attached, Covered',x,elements_y+pady*4)
        self.seperate(x-100,elements_y-26,13,7,style='primary')
        
        entry_y=combobox_y
        x=800
        self.Year_built=self.entry('Year built',2020,x,entry_y)
        self.Lot=self.entry('Lot',6098.0,x+padx,entry_y)
        self.Bathrooms=self.entry('Bathrooms',2.0,x,entry_y+pady)
        self.Full_bathrooms=self.entry('Full bathrooms',2.0,x+padx,entry_y+pady)
        self.Total_interior_livable_area=self.entry('Total interior livable area',1200.0,x,entry_y+pady*2)
        self.Total_spaces=self.entry('Total spaces',2.0,x+padx,entry_y+pady*2)
        self.Garage_spaces=self.entry('Garage spaces',2.0,x,entry_y+pady*3)
        self.Elementary_School_Score=self.entry('Elementary School Score',5.0,x+padx,entry_y+pady*3)
        self.Elementary_School_Distance=self.entry('Elementary School Distance',0.3,x,entry_y+pady*4)
        self.Middle_School_Score=self.entry('Middle School Score',6.0,x+padx,entry_y+pady*4)
        self.Middle_School_Distance=self.entry('Middle School Distance',0.6,x,entry_y+pady*5)
        self.High_School_Score=self.entry('High School Score',7.0,x+padx,entry_y+pady*5)
        self.High_School_Distance=self.entry('High School Distance',0.8,x,entry_y+pady*6)
        self.Tax_assessed_value=self.entry('Tax assessed value',510000.0,x+padx,entry_y+pady*6)
        self.Annual_tax_amount=self.entry('Annual tax amount',1395.0,x,entry_y+pady*7)
        self.Listed_Price=self.entry('Listed Price',799000.0,x+padx,entry_y+pady*7)
        self.Last_Sold_Price=self.entry('Last Sold Price',300000.0,x,entry_y+pady*8)
        self.Zip=self.entry('Zip',95123,x+padx,entry_y+pady*8)
        self.seperate(x-90,entry_y-26,13,13,style='danger')
        
        ttkb.Button(
            self.root,
            text='退出',
            bootstyle='primary',
            command=self.exit).place(anchor='ne',x=x-650,y=combobox_y-70)
        
        ttkb.Button(
            self.root,
            text='预测',
            bootstyle='success',
            command=self.predict).place(anchor='ne',x=x-650,y=elements_y+pady*6-50)
        
        self.labelframe=ttkb.Labelframe(
            self.root,
            text='预测结果',
            bootstyle='success')
        self.labelframe.place(anchor='nw',x=x-630,y=elements_y+pady*6-60)
        
        self.result=ttkb.Label(
            self.labelframe,
            width=16,
            bootstyle='success')
        self.result.pack()
        
        ttkb.Label(
            self.root,
            text='美元',
            bootstyle='success').place(anchor='nw',x=x-476,y=elements_y+pady*6-48)
        
        self.root.mainloop()
        
    def predict(self):
        def devide(data,name):
            data[name]=data[name].fillna('unknown')
            all=load_npy(name+'_devided')
            for i in all:
                data[name+'_'+str(i)]=data[name].map(lambda x:1 if i in x else 0)
            data.drop(columns=[name],inplace=True)
        
        def devide_time(data,name):
            data[name].fillna('0-0-0',inplace=True)
            data[name]=data[name].map(lambda x:x.split('-'))
            data[name+'_year']=data[name].map(lambda x:int(x[0]))
            data[name+'_month']=data[name].map(lambda x:int(x[1]))
            data[name+'_day']=data[name].map(lambda x:int(x[2]))
            data.drop(columns=[name],inplace=True)
        
        def one_hot(data,name):
            temp=load_npy(name+'_onehot')
            for i in temp:
                data[name+'_'+str(i)]=data[name].map(lambda x:1 if x==i else 0)
            data.drop(columns=[name],inplace=True)
        
        data=pd.DataFrame()
        data['Type']=[self.Type.get()]
        data['Year built']=[self.Year_built.get()]
        data['Heating']=[self.Heating.get()]
        data['Cooling']=[self.Cooling.get()]
        data['Parking']=[self.Parking.get()]
        data['Lot']=[self.Lot.get()]
        data['Bedrooms']=[self.Bedrooms.get()]
        data['Bathrooms']=[self.Bathrooms.get()]
        data['Full bathrooms']=[self.Full_bathrooms.get()]
        data['Total interior livable area']=[self.Total_interior_livable_area.get()]
        data['Total spaces']=[self.Total_spaces.get()]
        data['Garage spaces']=[self.Garage_spaces.get()]
        data['Region']=[self.Region.get()]
        data['Elementary School Score']=[self.Elementary_School_Score.get()]
        data['Elementary School Distance']=[self.Elementary_School_Distance.get()]
        data['Middle School Score']=[self.Middle_School_Score.get()]
        data['Middle School Distance']=[self.Middle_School_Distance.get()]
        data['High School Score']=[self.High_School_Score.get()]
        data['High School Distance']=[self.High_School_Distance.get()]
        data['Flooring']=[self.Flooring.get()]
        data['Appliances included']=[self.Appliances_included.get()]
        data['Laundry features']=[self.Laundry_features.get()]
        data['Parking features']=[self.Parking_features.get()]
        data['Tax assessed value']=[self.Tax_assessed_value.get()]
        data['Annual tax amount']=[self.Annual_tax_amount.get()]
        data['Listed On']=[self.Listed_On.entry.get()]
        data['Listed Price']=[self.Listed_Price.get()]
        data['Last Sold On']=[self.Last_Sold_On.entry.get()]
        data['Last Sold Price']=[self.Last_Sold_Price.get()]
        data['Zip']=[self.Zip.get()]
        data['State']=[self.State.get()]
        
        devide(data,'Type')
        devide(data,'Heating')
        devide(data,'Cooling')
        devide(data,'Parking')
        devide(data,'Bedrooms')
        devide(data,'Flooring')
        devide(data,'Appliances included')
        devide(data,'Laundry features')
        devide(data,'Parking features')
        
        devide_time(data,'Listed On')
        devide_time(data,'Last Sold On')
        
        one_hot(data,'Region')
        one_hot(data,'State')
        
        data['Zip_National_Area']=data['Zip'].map(lambda x:int(str(x)[0]))
        data['Zip_Sectional_Center']=data['Zip'].map(lambda x:int(str(x)[1:3]))
        data['Zip_Delivery_Area']=data['Zip'].map(lambda x:int(str(x)[3:]))
        data.drop(columns=['Zip'],inplace=True)
        
        y_pred = self.clf.predict(data)
        print(data)
        data.to_csv('2.csv')
        self.result['text']='%.2f'%y_pred[0]
    
    def devide_name(self,name):
        temp=name.split(' ')
        temp1=temp[0]
        if len(temp)>1:
            for i in temp[1:]:
                temp1+='\n'+i
        return temp1
    
    def seperate(self,x1,y1,sizex,sizey,style):
        pad=50
        for i in range(sizex):
            ttkb.Separator(
                self.root,
                bootstyle=style).place(x=x1+i*pad,y=y1)
            ttkb.Separator(
                self.root,
                bootstyle=style).place(x=x1+i*pad,y=y1+sizey*pad)
            
        for i in range(sizey):
            ttkb.Separator(
                self.root,
                bootstyle=style,
                orient='vertical').place(x=x1,y=y1+5+i*pad)
            ttkb.Separator(
                self.root,
                bootstyle=style,
                orient='vertical').place(x=x1+sizex*pad,y=y1+5+i*pad)
    
    def entry(self,name,value,x,y,padx=20):
        name=self.devide_name(name)
        ttkb.Label(
            self.root,
            text=name,
            justify='right',
            bootstyle='danger').place(anchor='e',x=x,y=y+0.005)
        
        _entry=ttkb.Entry(
            self.root,
            width=20,
            bootstyle='danger')
        _entry.place(anchor='w',x=x+padx,y=y)
        _entry.insert(0,value)
        return _entry
    
    def combobox(self,name,_features,default,x,y,padx=20):
        name=self.devide_name(name)
        ttkb.Label(
            self.root,
            text=name,
            justify='right',
            bootstyle='warning').place(anchor='e',x=x,y=y+0.005)
        
        _combobox=ttkb.Combobox(
            self.root,
            values=_features,
            width=20,
            bootstyle="warning")
        _combobox.current(_features.index(default))
        _combobox.place(anchor='w',x=x+padx,y=y)
        return _combobox
    
    def date_entry(self,name,date,x,y,padx=20):
        name=self.devide_name(name)
        ttkb.Label(
            self.root,
            text=name,
            justify='right',
            bootstyle='info').place(anchor='e',x=x,y=y+0.005)
        
        _date_entry=ttkb.DateEntry(
            self.root,
            firstweekday=1,
            width=18,
            startdate=datetime.datetime.strptime(date,'%Y-%m-%d'),
            bootstyle='info')
        _date_entry.place(anchor='w',x=x+padx,y=y)
        return _date_entry
    
    def elements(self,name,value,x,y,padx=20):
        name1=self.devide_name(name)
        ttkb.Label(
            self.root,
            text=name1,
            justify='right',
            bootstyle='primary').place(anchor='e',x=x,y=y+0.005)
        
        _entry=ttkb.Entry(
            self.root,
            width=15,
            bootstyle='primary')
        _entry.place(anchor='w',x=x+padx,y=y)
        _entry.insert(0,value)
        
        _button=ttkb.Button(
            self.root,
            text='选择',
            bootstyle='primary',
            command=lambda v=value,x=name,y=lists.elements[name],z=_entry:self.select(v,x,y,z))
        _button.place(anchor='w',x=x+padx+155,y=y)
        return _entry
    
    def select(self,value,name,elements,entry):
        root=element_select(value,name,elements)
        entry.delete(0,'end')
        entry.insert(0,root.get())
    
    def exit(self):
        global root
        self.root.destroy()
        root.destroy()
        
class element_select:
    def __init__(self,value,name,elements): #value 默认值
        self.root=ttkb.Toplevel(title='样本预测')
        set_window_position(self.root,element_select_window_size)
        
        self.value=value
        
        self.elements=elements
        
        image=Image.open(sub_bg_path)
        image=resize(image,1)
        bg=ImageTk.PhotoImage(image)
        cv =ttkb.Canvas(self.root,width=element_select_window_size[0],height=element_select_window_size[1])
        cv.pack()
        cv.create_image(element_select_window_size[0]//2,element_select_window_size[1]//2,image=bg)
        
        self.balloon=None
        
        ttkb.Label(
            self.root,
            text='选择 '+name+' 的值',
            bootstyle='primary').place(relx=0.02,rely=0.04)
        
        self.number=[-1 for i in range(len(self.elements))]
        
        x=0.02
        y=0.07
        count=0
        for i in self.elements:
            count+=1
            self.check_button(i,x,y)
            if count%16==0:
                x+=0.08
                y=0.07
            else:
                y+=0.055

        ttkb.Button(self.root,
                    text='完成',
                    command=self.exit).place(relx=0.9,rely=0.95)
        
        self.root.mainloop()
        
    def check_button(self,name,x,y): 
        _check_button=ttkb.Checkbutton(
            self.root,
            text=name,
            width=9,
            bootstyle="primary-outline-toolbutton",
            command=lambda x=name:self.toggle(name))
        _check_button.place(relx=x,rely=y)
        _check_button.bind('<Enter>',lambda event=True,name=name,x=x,y=y+0.04:self.balloon_show(event,name,x,y))
        _check_button.bind('<Leave>',self.balloon_hide)
        return _check_button
    
    def balloon_show(self,event,name,x,y):
        self.balloon=ttkb.Label(
            self.root,
            text=name)
        self.balloon.place(relx=x,rely=y)
            
    def balloon_hide(self,event):
        self.balloon.destroy()
    
    def toggle(self,name):
        self.number[self.elements.index(name)]*=-1
        
    def exit(self):
        global root
        self.root.destroy()
        root.destroy()
        
    def get(self):
        result=''
        temp=[]
        for i in range(len(self.number)):
            if self.number[i]==1:
                temp.append(self.elements[i])
        
        if len(temp)==1:
            result+=temp[0]
        elif len(temp)>1:
            result+=temp[0]
            for i in temp[1:]:
                result+=', '+i
        else:
            result=self.value
        return result

class main_page:
    def __init__(self,root):
        self.root=root
        self.root.title('加州房价预测系统')
        
        image=Image.open(main_page_bg_path)
        image=resize(image,0.73)
        bg=ImageTk.PhotoImage(image)
        cv =ttkb.Canvas(self.root,width=main_page_window_size[0],height=main_page_window_size[1])
        cv.pack()
        cv.create_image(main_page_window_size[0]//2,main_page_window_size[1]//2,image=bg)
        
        ttkb.Button(
            self.root,
            text='浏览训练数据集',
            bootstyle="primary",
            command=self.data_train_browser).place(anchor='center',relx=0.3,rely=0.8)
        
        ttkb.Button(
            self.root,
            text='浏览测试数据集',
            bootstyle="primary",
            command=self.data_test_browser).place(anchor='center',relx=0.3,rely=0.9)
        
        ttkb.Button(
            self.root,
            text='测试集预测',
            width=8,
            bootstyle="info",
            command=self.pre_data_page).place(anchor='center',relx=0.5,rely=0.8)
        
        ttkb.Button(
            self.root,
            text='样本预测',
            width=8,
            bootstyle="info",
            command=self.pre_single_page).place(anchor='center',relx=0.5,rely=0.9)
        
        ttkb.Button(
            self.root,
            text='分析',
            bootstyle="danger",
            command=self.analysis_page).place(anchor='center',relx=0.7,rely=0.8)
        
        ttkb.Button(
            self.root,
            text='退出',
            bootstyle="danger",
            command=self.exit).place(anchor='center',relx=0.7,rely=0.9)
        
        self.root.mainloop()
    
    def data_train_browser(self):
        data_browser(train_origin_path)
    
    def data_test_browser(self):
        data_browser(test_origin_path)
    
    def pre_data_page(self):
        pre_data_page()
    
    def pre_single_page(self):
        pre_single_page()
        
    def analysis_page(self):
        analysis_page()
    
    def exit(self):
        self.root.destroy()
        
# root.geometry('+{}+{}'.format(sw-main_page_window_size[0]//2,sh-main_page_window_size[1]//2))
set_window_position(root,main_page_window_size)
main_page(root)
# element_select('123','Parking',lists.elements['Parking'])
# pre_single_page()
