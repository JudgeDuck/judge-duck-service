#encoding=utf-8

from . import jd_utils as utils

header_htmldoc = utils.read_file("jd_htmldocs/header.html")
footer_htmldoc = utils.read_file("jd_htmldocs/footer.html")

index_htmldoc = """
	<div class="row" style="margin-top: 0px">
		<div class="col-xs-8">
			<table class="table table-hover table-align-left">
				<tr>
					<th class="col-xs-6"> 公告 </th>
					<th class="col-xs-2"> </th>
				</tr>
				<tr>
					<td> <a href="/blog/2"> 评测鸭上线啦 </a> </td>
					<td> 2019-01-01 23:33:33 </td>
				</tr>
				<tr>
					<td> <a href="/blog/1"> 什么是评测鸭 </a> </td>
					<td> 2019-01-01 00:00:00 </td>
				</tr>
				<tr>
					<td> <a href="/blog/1"> test 3 </a> </td>
					<td> 2018-01-01 23:33:33 </td>
				</tr>
				<tr>
					<td> <a href="/blog/1"> test 4 </a> </td>
					<td> 2018-01-01 23:33:33 </td>
				</tr>
				<tr>
					<td> <a href="/blog/1"> test 5 </a> </td>
					<td> 2018-01-01 23:33:33 </td>
				</tr>
			</table>
		</div>
		<div class="col-xs-4" style="text-align: center">
			<img src="/images/wys.png" width="250px" height="250px" style="border: 1px solid #ccc" />
		</div>
	</div>

	<hr />

	<div class="row jumbotron">
		<p style="font-size: 18px">
			“奋战三星期，造台……” 计算机？评测机？不，评测鸭！ <br />
			【评测鸭在线】是你见过的第一个能够精确计时的 OJ！ <br />
			在这里，你可以知道 register int 和 int 哪个快，或者尝试时间限制 10 us 的题，或者围观跑得最快的代码。 <br />
			你也可以加入QQ群，评测鸭用户群，群号是 781384211 。
		</p>
		<a href="/blog/1" class="btn btn-primary btn-lg"> 了解更多 </a>
	</div>
"""

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

