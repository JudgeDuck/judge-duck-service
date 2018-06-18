#encoding=utf-8

from . import jd_utils as utils

path_htmldocs = "jd_htmldocs/"

header_htmldoc = utils.read_file(path_htmldocs + "header.html")
header_online_htmldoc = utils.read_file(path_htmldocs + "header_online.html")
footer_htmldoc = utils.read_file(path_htmldocs + "footer.html")

index_htmldoc = utils.read_file(path_htmldocs + "index.html")
faq_htmldoc = utils.read_file(path_htmldocs + "faq.html")
register_htmldoc = utils.read_file(path_htmldocs + "register.html")
login_htmldoc = utils.read_file(path_htmldocs + "login.html")
profile_htmldoc = utils.read_file(path_htmldocs + "profile.html")
profile_self_htmldoc = utils.read_file(path_htmldocs + "profile_self.html")
edit_profile_htmldoc = utils.read_file(path_htmldocs + "edit_profile.html")

problems_htmldoc = utils.read_file(path_htmldocs + "problems.html")
problems_problem = """
				<tr>
					<td> %s </td>
					<td> <a href="/problem/%s"> %s </a> </td>
					<td> %s </td>
				</tr>
"""


problem_page_submit_htmldoc = """
				<input type="hidden" id="pid" value="%s" />
				<label for="code"> 你的代码 </label>
				<textarea id="code" class="form-control" rows="10">%s</textarea>
				<br />
				<a href="javascript:judgeduck.submit()" id="btn_submit" class="btn btn-md btn-default"> 提交 </a>
				<br />
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

