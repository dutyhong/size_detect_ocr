# 作者 ：duty
# 创建时间 ：2022/1/11 11:49 上午
# 文件 ：size_chart_normal.py
## [{"code":125,"name":"全胸围/Bust/Chest(厘米)"},{"code":132,"name":"腰围/Waist(厘米)"}]
from sizechart_detect.utils.no_chinese_filter import no_chinese_filter


def size_chart_normal(col_texts, size_attrs):
	normal_col_texts = []
	for col_text in col_texts:
		rec_col_name = col_text[0]
		normal_col_text = []
		for size_attr in size_attrs:
			col_code = size_attr.get("code", "未知code")
			col_name = size_attr.get("name", "未知name")
			if no_chinese_filter(rec_col_name) in no_chinese_filter(col_name) or no_chinese_filter(col_name) in no_chinese_filter(rec_col_name):
				normal_col_text.append(col_code)
				normal_col_text.append(col_name)
				for text in col_text[1:]:
					normal_col_text.append(text)
		normal_col_texts.append(normal_col_text)
	return normal_col_texts



