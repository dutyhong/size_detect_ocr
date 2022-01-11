# 作者 ：duty
# 创建时间 ：2022/1/11 5:24 下午
# 文件 ：no_chinese_filter.py
#去除特殊字符，只保留汉子，字母、数字
import re
#去除不可见字符
def no_chinese_filter(input_str):
	output_str = re.sub('[^\u4e00-\u9fa5]+','',input_str)
	return output_str

if __name__=="__main__":
	s = "今天下雨了123！@#%@……￥@￥，不开心()/"
	ss = no_chinese_filter(s)
	print(ss)