#encoding=utf-8

import markdown2
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


problem_page_cpp_faq = """
#### 关于 C/C++ 语言的说明

你可以使用 C 语言的标准头文件，但不是所有特性都是支持的。

比如我们目前支持 `getchar`, `putchar` 和 `malloc` 系列函数，暂不支持 `scanf`, `printf` 和 `fseek` 系列函数。

#### 关于 C++ 语言的说明

你可以使用 C++ 语言的各种语法特性，也可以使用 C++ 的标准头文件和 STL 库。

但是，至少有下列 C++ 特性是不支持的：`new` 和 `delete`、全局变量动态初始化、`iostream` 头文件、使用默认分配器的标准库容器及其上的适配器。

#### 关于 C/C++ 标准库的说明

当你使用标准库函数的时候，一些额外的内存将会被使用。这是因为标准库要维护它的运行状态。

一般情况下，这些额外的内存使用不会超过 4KB。

#### 关于标准输出的说明

标准输出将被重定向到内存中，所以你的内存使用量也包括了你的标准输出的大小（向上取整到 4KB 的倍数）。

综上，一个包含一行 `puts("");` 的程序至少需要占用 12KB 的内存（标准库、标准输出、栈空间各4KB）。

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

