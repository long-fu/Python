
# 获取目录下面的所有文件

# 对文件进行重命名

import os
from os.path import isfile
import random

project_path = "/Users/flqy/Documents/pw/MeetingBeauty"

project_pbxproj_path = "/Users/flqy/Documents/pw/MeetingBeauty/MeetingBeauty.xcodeproj/project.pbxproj"

filter_dirs = [
"Main",
"Supporting Files",
".git",
"MeetingBeauty.xcodeproj",
"MeetingBeautyUITests",
"MeetingBeautyTests",
"MeetingBeauty.xcworkspace",
"Pods"
]


filter_files = [
".DS_Store",
"Base.lproj",
"codeObfuscation.h",
"Info.plist",
"Podfile.lock",
"Podfile",
"MeetingBeauty.entitlements",
"AppDelegate.m",
"AppDelegate.h"
]

filter_file_types = ["json"]

def generate_random_str(randomlength=25):
  """
  生成一个指定长度的随机字符串
  """
  random_str = ''
  base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz'
  length = len(base_str) - 1
  for i in range(randomlength):
    random_str += base_str[random.randint(0, length)]
  random_str = random_str[0].upper() + random_str[1:]
  if random_str in old_new_name_dic:
      return generate_random_str(randomlength)

  return random_str

# 读取项目目录

#xcodeproj 项目目录链接



# 老的文件名 (不带后缀) 关联新的 文件名(不带文件后缀)
old_new_name_dic = {}

# 老的文件名 (不带后缀) 关联新的 文件名(不带文件后缀)
new_old_name_dic = {}

def re_file_name(path):
    """
    重命名文件
    """
    #os.path.split（）返回文件的路径和文件名
    dirname,filename = os.path.split(path)
    #os.path.splitext()将文件名和扩展名分开
    fname,fename = os.path.splitext(filename)
    # 不需要进行修改的扩展名文件
    if fename == ".caf":
        return
    old_name = fname
    types = fename
    if old_name in old_new_name_dic:
        new_name = old_new_name_dic[old_name]
        new_path = os.path.join(dirname,new_name + types)
        os.rename(path,new_path)
        pass
    else:
        new_name = generate_random_str()
        old_new_name_dic[old_name] = new_name
        new_old_name_dic[new_name] = old_name
        new_path = os.path.join(dirname,new_name + types)
        os.rename(path,new_path)
        pass
    pass

def re_project_file_name(root_path,filter_dirs=[],filter_files=[]):
    """
    替换项目的文件名
    """
    file_list = os.listdir(root_path)
    for name in file_list:
        if filter_dirs.count(name)>0:
            continue
        if filter_files.count(name)>0:
            continue
        temp_path = os.path.join(root_path,name)
        if os.path.isdir(temp_path):
            re_project_file_name(temp_path,filter_dirs,filter_files)
        else:
            re_file_name(temp_path)
    
    # 替换项目下面的文件链接
    pass



def re_import_text(path):

    r_f = open(path,'r')
    code_text = r_f.read()
    r_f.close()

    # 从最长串开始匹配
    temp_dic = sorted(old_new_name_dic.items(), key = lambda kv :(len(kv[1]), len(kv[0])),reverse=True)
    for old_name in temp_dic:
        new_name = old_new_name_dic[old_name[0]]
        code_text = code_text.replace(old_name[0],new_name)
        pass

    # for key,value in new_old_name_dic.items():
    #     old_name = f"{value}"
    #     new_name = f"{key}"
    #     code_text = code_text.replace(old_name,new_name)
    #     pass
    
    w_f = open(path,'w')
    w_f.write(code_text)
    w_f.close()

    pass

def re_xib_class(path,old,new):

    r_f = open(path,'r')
    code_text = r_f.read()
    r_f.close()

    code_text = code_text.replace(old,new)

    w_f = open(path,'w')
    w_f.write(code_text)
    w_f.close()
    pass

def re_file_text(path):

    dirname,filename = os.path.split(path)

    fname,fename = os.path.splitext(filename)
    if fename == '.xib':
        if fname in new_old_name_dic:
            old_name = new_old_name_dic[fname]
            re_xib_class(path,old_name,fname)
            pass
        pass
    elif fename == '.h' or fename == '.m' or fename == '.mm' or  fename == '.pch':
        re_import_text(path)
        pass
    pass


text_filter_dirs = [
"Resources",
"Assets.xcassets",
".git",
"MeetingBeauty.xcodeproj",
"MeetingBeautyUITests",
"MeetingBeautyTests",
"MeetingBeauty.xcworkspace",
"Pods"
]


text_filter_files = [
".DS_Store",
"Base.lproj",
"codeObfuscation.h",
"Info.plist",
"Podfile.lock",
"Podfile",
"MeetingBeauty.entitlements",
"main.m"
]

def re_project_file_text(root_path,text_filter_dirs,text_filter_files):
    """
    替换所有文件里面的代码
    """

    file_list = os.listdir(root_path)

    

    for name in file_list:
        if text_filter_dirs.count(name)>0:
            continue
        if text_filter_files.count(name)>0:
            continue
        temp_path = os.path.join(root_path,name)
        if os.path.isdir(temp_path):
            re_project_file_text(temp_path,text_filter_dirs,text_filter_files)
        else:
            re_file_text(temp_path)
    
    # 替换项目下面的文件链接
    pass

def re_project_pbxproj(path):
    r_f = open(path,"r")
    pbxproj_text = r_f.read()
    r_f.close()

    w_f = open("/Users/flqy/Documents/pw/MeetingBeauty/file_reanme.md",'a+')

    # 从最长串开始匹配
    temp_dic = sorted(old_new_name_dic.items(), key = lambda kv:(len(kv[1]), len(kv[0])),reverse=True)

    for key in temp_dic:
        new_name = old_new_name_dic[key[0]]
        pbxproj_text = pbxproj_text.replace(key[0],new_name)
        key_line = key[0] + " --- " + new_name + "\r\n"
        w_f.write(key_line)
        pass
    
    w_f.close()

    w_f = open(path,"w")
    if w_f.write(pbxproj_text) == 0:
        print("文件写入失败")
        assert(False)
    w_f.close()

    pass


if __name__ == "__main__":

    re_project_file_name(project_path,filter_dirs,filter_files)

    re_project_pbxproj(project_pbxproj_path)

    re_project_file_text(project_path,text_filter_dirs,text_filter_files)

    # test_dic ={"1":"11","1234":'1231231',"123":"jkkj","12":"1232"}
    
    # tmp = sorted(test_dic.items(), key = lambda kv:(len(kv[1]), len(kv[0])),reverse=True)
    # print(tmp)
    # print(tmp[0][0])
    pass
