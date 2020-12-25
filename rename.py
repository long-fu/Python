
# 获取目录下面的所有文件

# 对文件进行重命名

import os
import random

project_path = "/Users/flqy/Documents/pw/MeetingBeauty"

filter_dirs = [
"Main",
"Assets.xcassets",
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
"MeetingBeauty.entitlements"
]

filter_file_types = ["json"]

def generate_random_str(randomlength=25):
  """
  生成一个指定长度的随机字符串
  """
  random_str = ''
  base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
  length = len(base_str) - 1
  for i in range(randomlength):
    random_str += base_str[random.randint(0, length)]

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

def re_file_name(root_path,filter_dirs=[],filter_files=[]):
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
        if not os.pardir.isdir(temp_path):
            pass
        else:
            re_file_name(temp_path,filter_dirs,filter_files)
    
    # 替换项目下面的文件链接
    pass

def re_project_pbxproj(path):
    r_f = open(path,"r")
    pbxproj_text = r_f.read()
    r_f.close()

    for key in old_new_name_dic:
        new_name = old_new_name_dic[key]
        pbxproj_text = pbxproj_text.replace(key,new_name)
        pass
    
    w_f = open(path,"w")
    if w_f.write(pbxproj_text):
        print("文件写入失败")
        assert(False)
    w_f.close()

    pass

# 找到老的项目

# 替换 .h .m  import ".h"

# 直接替换文件

#import "DaShi_TaskController.h" -> #import ".h"

def re_file_text(path,old,new):

    old_name = "#import \"{old}.h\""
    new_name = "#import \"{new}.h\""

    r_f = open(path,'r')
    code_text = r_f.read()
    r_f.close()

    code_text = code_text.replace(old_name,new_name)

    w_f = open(path,'w')
    w_f.write(code_text)
    w_f.close()

    pass

def re_xib_name(path):
    
    pass

def re_import_name(path):
    #os.path.split（）返回文件的路径和文件名
    dirname,filename = os.path.split(path)
    #os.path.splitext()将文件名和扩展名分开
    fname,fename = os.path.splitext(filename)
    

    if fname in new_old_name_dic:
        old_name = new_old_name_dic[fname]

        pass
    else:
        assert(False)
        pass

    pass

# 替换 .h 文件


# 通过新的文件名找到 老的文件名 替换 每一个的 .h 文件

# 替换 .xib
# 通过新的文件名找到 老的文件名 直接替换文件文字就可以


# 先对其所有的文件 进行重命名

# project.pbxproj 链接替换

# 代码文件 import 进行文字替换



if __name__ == "__main__":
    # f = open("/Users/flqy/Documents/pw/MeetingBeauty/MeetingBeauty.xcodeproj/project.pbxproj",'r',encoding="utf-8")
    # text = f.read()
    # print("显示读取的文字", text)
    # f.close()
    # 操作成功
    # traverse(project_path)
    # re_file(pbxproj)
    pass