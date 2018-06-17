#encoding=utf-8

from . import jd_utils as utils

path_htmldocs = "jd_htmldocs/"

header_htmldoc = utils.read_file(path_htmldocs + "header.html")
footer_htmldoc = utils.read_file(path_htmldocs + "footer.html")

index_htmldoc = utils.read_file(path_htmldocs + "index.html")
faq_htmldoc = utils.read_file(path_htmldocs + "faq.html")
register_htmldoc = utils.read_file(path_htmldocs + "register.html")

index_problem_list_problem = """
<strong><a target="_blank" href="problem?pid=%s">%s</a></strong> %s
<strong><a target="_blank" href="board?pid=%s">排行榜</a></strong>
<br />
<br />
"""


problem_page_htmldoc = """
<html>
<head>
<meta http-equiv=Content-Type content="text/html;charset=utf-8">
<title>测一测</title>
<style type="text/css">
textarea{
height:50%%;
width:100%%;
display:block;
max-width:100%%;
line-height:1.5;
border-radius:3px;
font:16px Consolas;
transition:box-shadow 0.5s ease;
font-smoothing:subpixel-antialiased;
}
</style>
</head>
<body>

<h1>测一测</h1>
<h2>公告：正在升级中，服务可能不稳定，感谢您的支持！</h2>
6月9日更新：可以使用全局变量和在函数中定义静态(static)变量了，如果仍有问题请反馈

<br />
<br />

%s

</body>
</html>
"""

problem_page_submit_htmldoc = """
<form id="form" method="post" action="submit?pid=%s">
<input type="submit" value="提交" />
你的昵称：<input type="text" name="name" value="咕咕咕" />
<br />
<textarea name="code">
%s</textarea>
</form>
"""











board_htmldoc = """
<html>
<head>
<meta http-equiv=Content-Type content="text/html;charset=utf-8">
<title>测一测</title>
<style type="text/css">
textarea{
height:50%%;
width:100%%;
display:block;
max-width:100%%;
line-height:1.5;
border-radius:3px;
font:16px Consolas;
transition:box-shadow 0.5s ease;
font-smoothing:subpixel-antialiased;
}
</style>
</head>
<body>
<h2>公告：正在升级中，服务可能不稳定，感谢您的支持！</h2>
<h1>测一测</h1>
<h2> %s 排行榜 </h2>
%s
</body>
</html>
"""


detail_htmldoc = """
<html>
<head>
<meta http-equiv=Content-Type content="text/html;charset=utf-8">
<title>测一测</title>
<style type="text/css">
textarea{
height:50%%;
width:100%%;
display:block;
max-width:100%%;
line-height:1.5;
border-radius:3px;
font:16px Consolas;
transition:box-shadow 0.5s ease;
font-smoothing:subpixel-antialiased;
}
</style>
</head>
<body>
<h2>提交记录 %s 的结果（题目： <a href="problem?pid=%s" > %s </a> ，用户： %s）</h2>
<textarea style="height:25%%">
%s</textarea>
<br />
<textarea>
%s</textarea>
</body>
</html>
"""

