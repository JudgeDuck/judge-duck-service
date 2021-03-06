#encoding=utf-8

import markdown2
from . import jd_utils as utils

path_htmldocs = "jd_htmldocs/"

header_htmldoc = utils.read_file(path_htmldocs + "header.html")
header_online_htmldoc = utils.read_file(path_htmldocs + "header_online.html")
footer_htmldoc = utils.read_file(path_htmldocs + "footer.html")

empty_page_htmldoc = utils.read_file(path_htmldocs + "empty_page.html")

index_htmldoc = utils.read_file(path_htmldocs + "index.html")
faq_htmldoc = utils.read_file(path_htmldocs + "faq.html")
register_htmldoc = utils.read_file(path_htmldocs + "register.html")
login_htmldoc = utils.read_file(path_htmldocs + "login.html")
profile_htmldoc = utils.read_file(path_htmldocs + "profile.html")
profile_self_htmldoc = utils.read_file(path_htmldocs + "profile_self.html")
edit_profile_htmldoc = utils.read_file(path_htmldocs + "edit_profile.html")

beibishi_htmldoc = utils.read_file(path_htmldocs + "beibishi.html")

custom_test_htmldoc = utils.read_file(path_htmldocs + "custom_test.html")

problems_htmldoc = utils.read_file(path_htmldocs + "problems.html")
problems_problem = """
				<tr>
					<td> %s </td>
					<td> <a href="/problem/%s"> %s </a> </td>
					<td> %s </td>
					<td class="no-decoration" style="text-align:center">
						%s
					</td>
				</tr>
"""


problem_page_cpp_faq = """
#### 关于标准输出的说明（最后更新：2018年10月23日）

标准输出将被重定向到内存中，所以你的内存使用量也包括了你的标准输出的大小（向上取整到 4KB 的倍数）。

如果你的程序要进行大量输出，请考虑这一点。
"""

problem_page_submit_htmldoc = """
				<div class="row">
					<input type="hidden" id="pid" value="%s" />
					<div class="col-xs-3 form-group">
						<label for="language"> 语言 </label>
						<select class="form-control" id="language">
							%s
						</select>
					</div>
					<div class="col-xs-12 form-group">
						""" + markdown2.markdown(problem_page_cpp_faq) + """
					</div>
					<div class="col-xs-12 form-group">
						<label for="code"> 你的代码 </label>
						<textarea id="code" class="form-control" rows="10">%s</textarea>
						<br />
					</div>
					<div class="col-xs-12 form-group">
						<a href="javascript:judgeduck.submit()" id="btn_submit" class="btn btn-md btn-default"> 提交 </a>
					</div>
					<br />
				</div>
"""

problem_board_htmldoc = """
			<table class="table table-hover">
				<tr>
					<th class="col-xs-1"> 排名 </th>
					<th class="col-xs-1"> 提交编号 </th>
					<th class="col-xs-2"> 用户 </th>
					<th class="col-xs-2"> 用时 </th>
					<th class="col-xs-2"> 内存 </th>
					<th class="col-xs-2"> 代码长度 </th>
					<th class="col-xs-2"> 提交时间 </th>
				</tr>
				%s
			</table>
"""

submissions_htmldoc = utils.read_file(path_htmldocs + "submissions.html")
submissions_my_button = """
				<div class="pull-right">
					<a href="/submissions?username=%s" class="btn btn-success"> 我的提交记录 </a>
				</div>
"""

submission_htmldoc = utils.read_file(path_htmldocs + "submission.html")

blogs_htmldoc = utils.read_file(path_htmldocs + "blogs.html")
blog_post_htmldoc = utils.read_file(path_htmldocs + "blog_post.html")
blog_edit_htmldoc = utils.read_file(path_htmldocs + "edit_blog.html")








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

