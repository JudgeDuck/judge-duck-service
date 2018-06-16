#encoding=utf-8


index_htmldoc = """
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
6月13日更新：计时精度提高，现在计时分度值为 10 ns，误差约为 1‰ + 1 us
<br />
6月9日更新：可以使用全局变量和在函数中定义静态(static)变量了，如果仍有问题请反馈
<br />
<br />
<a href="/old">访问旧版（测测你的排序）</a>
<br />

<br />
<h2>题目列表</h2>

%s

<br />
<br />
你很可能想问，为什么要有这样一个奇怪的OJ呢？如果就是为了比一比谁的排序跑得更快，随便一个OJ都能配置一道这样的题，也能给出一个评测记录的统计呀！
<br />
<br />
也许你知道某些OJ的运行时间总是15.625ms的倍数，也许你知道在某些OJ上多次提交的时间会波动很大，也许你知道评测时滚键盘能对运行时间造成很大影响……
<br />
<br />
所以，我们采用了你从未见过的技术！
<br />
<br />
（未完待续）
<br />
</body>
</html>
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
6月13日更新：计时精度提高，现在计时分度值为 10 ns，误差约为 1‰ + 1 us
<br />
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
6月13日更新：计时精度提高，现在计时分度稳定值为 10 ns，误差约为 1‰ + 1 us
<br />
6月9日更新：可以使用全局变量和在函数中定义静态(static)变量了，如果仍有问题请反馈
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

