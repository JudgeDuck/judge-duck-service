// Bei bi shi !!!

var beibishi = function() {
	
	var problem_text;
	var option_texts;
	var option_divs;
	var submit_div;
	
	var init = function() {
		problem_text = $("#problem_text");
		option_texts = [];
		option_divs = [];
		for (var i = 1; i <= 4; i++) {
			option_texts.push($("#option_text_" + i));
			option_divs.push($("#option_div_" + i));
		}
		for (var i = 0; i < 4; i++) {
			option_divs[i].click(function(id_in) {
				var id = id_in;
				return function() {
					option_click(id);
				};
			}(i));
			
			selected[i] = false;
		}
		
		submit_div = $("#submit_div");
		$("#submit_button").click(check_answer);
		
		load_problems();
		show_random_problem();
	};
	
	var selected = {};  // Real id
	
	var option_click = function(id) {
		var real_id = order_map[id];
		if (!selected[real_id]) {
			option_divs[id].addClass("has-checked");
			selected[real_id] = true;
		} else {
			option_divs[id].removeClass("has-checked");
			selected[real_id] = false;
		}
		
		if (!cur_prob.is_multiple) {
			beibishi.check_answer();
		}
	};
	
	var check_answer = function() {
		var WA = false;
		var ans_s = "";
		for (var i = 0; i < 4; i++) {
			var real_i = order_map[i];
			if (selected[real_i] != cur_prob.answer[real_i]) {
				WA = true;
			}
			if (cur_prob.answer[real_i]) {
				ans_s = ans_s + cur_prob["option_" + (real_i + 1)] + "\n";
			}
		}
		if (WA) {
			alert("做错啦！正确答案是：\n\n" + ans_s);
		}
		
		show_random_problem();
	};
	
	var cur_prob;
	
	var order_map = {};
	var order_map_inv = {};
	
	var show_problem = function(p) {
		// description, options[4], is_multiple, answer("1234"), need_reorder
		cur_prob = p;
		for (var i = 0; i < 4; i++) {
			order_map[i] = i;
			order_map_inv[i] = i;
		}
		if (p.need_reorder) {
			for (var i = 0; i < 3; i++) {
				var j = Math.floor(Math.random() * (4 - i));
				if (j < i) j = i;
				if (j > 3) j = 3;
				if (j != i) {
					var tmp = order_map[i];
					order_map[i] = order_map[j];
					order_map[j] = tmp;
				}
			}
			for (var i = 0; i < 4; i++) {
				order_map_inv[order_map[i]] = i;
			}
		}
		for (var i = 0; i < 4; i++) {
			option_texts[i].text(p["option_" + (order_map[i] + 1)]);
			option_divs[i].removeClass("has-checked");
			selected[i] = false;
		}
		
		problem_text[0].innerHTML = (p.description.replace(/\n/g, '<br>'));
		
		if (p.is_multiple) {
			submit_div.css("display", "");
		} else {
			submit_div.css("display", "none");
		}
	};
	
	var show_random_problem = function() {
		pid = Math.floor(Math.random() * all_probs.length);
		if (pid < 0) pid = 0;
		if (pid >= all_probs.length) pid = all_probs.length - 1;
		show_problem(all_probs[pid]);
	};
	
	var all_probs;
	
	var load_problems = function() {
		var convert_problem = function(p) {
			var ret = {
				description: p[0],
				option_1: p[1],
				option_2: p[2],
				option_3: p[3],
				option_4: p[4],
				is_multiple: p[5],
				answer: {},
				need_reorder: p[7]
			};
			if (ret.is_multiple) {
				ret.description = "（多选题）" + ret.description;
			}
			for (var i = 0; i < 4; i++) {
				ret.answer[i] = false;
			}
			for (var i = 0; i < p[6].length; i++) {
				ret.answer[p[6][i] - 1] = true;
			}
			return ret;
		};
		var probs = [
			["NOI 机试使用的操作系统是", "Linux", "Windows", "Mac OS", "JudgeDuck OS", false, "1", true],
			["Linux 中为文件改名使用的命令是", "mv <旧文件名> <新文件名>", "mv <新文件名> <旧文件名>", "rename <旧文件名> <新文件名>", "rename <新文件名> <旧文件名>", false, "1", true],
			["在 Linux 中返回上一级目录使用的命令是", "cd ..", "cd .", "cd /", "cd ~", false, "1", true],
			["在 Linux 中删除当前目录下的 test 目录的命令是", "rm -r test", "rm test", "rm -f test", "rm /test", false, "1", true],
			["当前目录下有一个编译好的可执行文件 a.out，执行它使用的命令是", "./a.out", "/a.out", "a.out", "../a.out", false, "1", true],
			["使用高级语言编写的程序称之为", "源程序", "源代码", "高级程序", "高级代码", false, "1", true],
			["在 NOI Linux 系统中可以用来调试程序的程序是", "gdb", "gcc", "vim", "g++", false, "1", true],
			["在 Linux 系统中，文件夹中的文件可以与该文件夹同名吗", "可以", "不可以", "有时候可以", "有时候不可以", false, "1", true],
			["Linux 系统中杀死名为 test 的后台进程的命令是", "killall test", "kill test", "rm test", "close test", false, "1", true],
			["Linux 系统中可以查看隐藏文件的命令是", "ls -a", "ls -l", "ls -h", "ls -R", false, "1", true],
			["Linux 系统中编译 C 程序的编译器是", "gcc", "g++", "fpc", "gdb", false, "1", true],
			["Linux 系统中编译 Pascal 程序的编译器是", "fpc", "gcc", "g++", "gdb", false, "1", true],
			["Linux 系统中编译 C++ 程序的编译器是", "g++", "gcc", "gdb", "fpc", false, "1", true],
			["Linux 系统中，将当前目录下的文件名打印到 tmp 文件中的命令是", "ls > tmp", "ls < tmp", "ls tmp", "ls -o tmp", false, "1", true],
			["Linux 系统中，测量当前目录下程序 test 运行时间的命令是", "time ./test", "time test", "time ../test", "time test.exe", false, "1", true],
			["vim 编辑器中，强制退出不保存修改应当输入", ":q!", ":wq", ":w!", "q", false, "1", true],
			["vim 编辑器中，强制退出并保存修改可输入以下三种命令之一", ":wq", "ZZ", ":x", ":w!", true, "123", true],
			["vim 编辑器中，定位到文件中第 12 行应当输入", ":12", "12", ":l12", "/12", false, "1", true],
			["vim 编辑器中，在文件中查找字符串“12”应当输入", "/12", ":12", ":l12", "12", false, "1", true],
			["使用 gcc 编译 C 程序时，生成调试信息的命令行选项是", "-g", "-o", "-c", "-d", false, "1", true],
			["使用 gcc 编译 C 程序时，生成所有警告信息的命令行选项是", "-Wall", "-Werror", "-g", "-o", false, "1", true],
			["使用 gcc 编译 C 程序时，只编译生成目标文件的命令行选项是", "-c", "-o", "-g", "-d", false, "1", true],
			["使用 gcc 编译 C 程序时，指定输出文件名的命令行选项是", "-o", "-c", "-g", "-d", false, "1", true],
			["如果 C 程序中使用了 math.h 中的函数，在编译时需要加入选项", "-lm", "-lmath", "-m", "-math", false, "1", true],
			["Linux 系统中具有最高权限的用户是", "root", "sudo", "admin", "friend", false, "1", true],
			["在 Linux 的各个虚拟控制台间切换的快捷键是", "Ctrl+Alt+F[1-6]", "Ctrl+Alt+Del", "Ctrl+Alt+PageDown", "Ctrl+Alt+PageUp", false, "1", true],
			["在 NOI Linux 中，从字符控制台切换回桌面环境使用的快捷键是", "Ctrl+Alt+F7", "Ctrl+Alt+F1", "Ctrl+Alt+Del", "Ctrl+Alt+F12", false, "1", true],
			["在 NOI Linux 中默认使用的 Shell 是", "bash", "sh", "zsh", "shell", false, "1", true],
			["在 Linux 中查看当前系统中的进程使用的命令是", "ps", "ls", "cd", "time", false, "1", true],
			["在 Linux 中查看进程的 CPU 利用率使用的命令是", "ps", "ls", "cd", "time", false, "1", true],
			["如果自己的程序进入死循环，应当如何终止", "Ctrl-C", "Ctrl-A", "Ctrl-X", "Ctrl+Alt+Del", false, "1", true],
			["可执行文件a.out从标准输入读取数据。现有一组输入数据保存在 1.in 中，使用这个测试数据文件测试自己的程序的命令是", "./a.out < 1.in", "./a.out > 1.in", "./a.out 1.in", "./a.out -o 1.in", false, "1", true],
			["可执行文件 prog_1 向标准输出输出运行结果。将输出结果保存到 1.out 文件中使用的命令是", "./prog_1 > 1.out", "./prog_1 < 1.out", "./prog_1 1.out", "./prog_1 -o 1.out", false, "1", true],
			["使用 Reset 键强行重新启动计算机可能会对系统造成的后果是", "文件系统损坏", "硬盘损坏", "CPU 过热", "无法开机", false, "1", true],
			["在 Linux 系统中，用于查看文件的大小的命令是", "ls -l", "ls -a", "ls -h", "ls -R", false, "1", true],
			["当前目录中有如下文件：\n-rw-r--r-- 1 user None 8.7K Jul 2 16:35 foobar\n-rw-r--r-- 1 user None 93 Jul 2 16:35 foobar.c\n-rwx------ 1 user None 144 Jul 2 16:35 foobar.sh\n其中，可以执行的文件是", "foobar.sh", "foobar.c", "foobar", "都不可执行", false, "1", true],
			["评测系统中对程序源文件大小的限制是", "小于 100KB", "小于 50KB", "小于等于 100KB", "小于等于 50KB", false, "1", true],
			["如无另行说明，评测系统中对程序使用内存的限制是", "以硬件资源为限", "2GB", "512MB", "256MB", false, "1", true],
			["Linux 下的换行字符为", "\\n", "\\r", "\\r\\n", "enter", false, "1", true],
			["终止一个失去响应的进程（$pid 代表进程号）的命令是", "kill $pid", "killall $pid", "rm $pid", "stop $pid", false, "1", true],
			["Linux 中是否区分文件和目录名称的大小写", "是", "否", "可能是", "可能不是", false, "1", true],
			["选手在 NOI 机试过程中是否禁止使用网络", "是", "否", "可能是", "可能不是", false, "1", true],
			["为程序my.c创建一个备份myc.bak时，使用的命令是", "cp my.c myc.bak", "cp myc.bak my.c", "mv my.c myc.bak", "mv myc.bak my.c", false, "1", true],
			["在 Anjuta 中调试程序，继续执行的快捷键是", "F4", "F5", "F6", "F7", false, "1", true],
			["在 Lazarus 中开始运行程序的快捷键是", "F9", "F8", "F10", "F11", false, "1", true],
			["在 Anjuta 中调试程序，单步运行(Step over)的快捷键是", "F6", "F5", "F4", "F7", false, "1", true],
			["在 Lazarus 中调试程序，单步运行(Step over)的快捷键是", "F8", "F9", "F10", "F11", false, "1", true],
			["调试程序的方法有", "单步调试", "使用 print 类语句打印中间结果", "读源代码", "使用小黄鸭", true, "123", true],
			["如果需要在 Lazarus 中使用单步调试，则", "在 Environment->Debugger Options 中配置", "按 F9", "在 Environment->Compiler Options 中配置", "按 F8", false, "1", true],
			["在考试过程中，如果出现系统死机或者崩溃现象，选手应当采取的措施是", "举手示意监考人员处理", "自行重启机器", "按下 Ctrl+Alt+Del", "按 Reset 键", false, "1", true],
			["提交的答案程序中如果包含 NOI 考试明确禁止使用的代码，后果是", "本题成绩以 0 分计算", "本场比赛成绩以 0 分计算", "取消比赛资格", "取消获奖资格", false, "1", true],
			["NOI 比赛使用的 Linux 发行版是", "NOI Linux", "Ubuntu", "Arch Linux", "Debian", false, "1", true],
			["对评测结果有疑义，需要申请复评，则", "提出书面申请", "经领队、有关工作人员、科学委员会主席签字确认", "提交至评测人员", "经教练签字", true, "123", true],
			["复评成绩较原始成绩有变化，则", "以复评成绩为准", "以原始成绩为准", "取两者最高分", "由评测人员决定", false, "1", true],
			["Pascal 中 integer 和 long integer 类型的长度和编译选项是否有关系", "有关系", "没关系", "可能有关系", "可能没关系", false, "1", true],
			["NOI 考试对 C++语言模板的使用有限制吗？", "没有", "有", "可能有", "可能没有", false, "1", true],
			["NOI 考试对 PASCAL 语言的使用有限制吗？", "有", "没有", "可能有", "可能没有", false, "1", true],
			["名为 FILE 的文件和名为 File 的文件在 Linux 系统中被认为是", "不同的文件", "相同的文件", "可能是不同的文件", "可能是相同的文件", false, "1", true],
			["目录 DIRECT 和目录 Direct 在 Linux 系统中被认为是", "不同的目录", "相同的目录", "可能是不同的目录", "可能是相同的目录", false, "1", true],
			["在 NOI 正式考试中如何登录自己的比赛用机", "使用考前工作人员下发的账户及密码", "使用 root 账户", "使用 friend 账户", "使用试机时下发的账户及密码", false, "1", true],
			["如果考试分多日进行，那么选手的考试账户和口令", "由工作人员在每场考试开始前下发", "试机之前统一下发", "每次考试一样", "在考试前放在选手的桌上", false, "1", true],
			["考试结束后，应如何处理密码条", "保存好密码条，用于复测", "可以丢弃密码条", "将密码告诉别人", "随便怎么处理", false, "1", true],
			["选手答案文件保存的目录是", "选手目录下和考题名称相同的目录", "选手目录", "/home", "根目录", false, "1", true],
			["选手答案的文件名要求是", "和试卷的题目摘要中所示文件名一致", "answer", "任何文件名都可以", "code", false, "1", true],
			["选手答案的文件名大小写错误，成绩会怎样", "0分", "100分", "不变", "可能不变", false, "1", true],
			["选手提交的源代码文件名是否有特殊要求", "源程序文件名由试题名称缩写加后缀构成", "试题名称缩写及后缀一律使用小写", "试题名称缩写及后缀一律使用大写", "试题名称首字母大写，后缀小写", false, "1", true],
			["在NOI考试中，Pascal 源文件的扩展名规定为", "pas", "cpp", "c", "txt", false, "1", true],
			["在NOI考试中，C源文件的扩展名规定为", "c", "cpp", "pas", "txt", false, "1", true],
			["在NOI考试中，C++源文件的扩展名规定为", "cpp", "c", "pas", "txt", false, "1", true],
			["发现鼠标或其他硬件设备有问题，选手可以", "请工作人员更换", "重启电脑", "重新插入有问题的硬件设备", "关机", false, "1", true],
			["对试题理解有问题，选手可以", "举手向工作人员求助", "和边上选手讨论", "自行处理", "做其他题目", false, "1", true],
			["考试结束后选手需要", "迅速离开", "在原地等待评测", "在考场内讨论题目", "继续答题", false, "1", true],
			["复评结束后是否还能提交复评申请", "不能", "能", "也许能", "也许不能", false, "1", true],
			["测试点时间限制的含义是指", "题目允许程序运行所占用的用户时间总和的上限值", "题目允许程序运行所占用的实际时间总和的上限值", "题目允许程序编译所占用的用户时间总和的上限值", "题目允许程序编译所占用的实际时间总和的上限值", false, "1", true],
			["什么情况下选手可以申请延长考试时间", "机器出现故障，并由工作人员确认和记录", "对试题理解有问题", "忘记保存源程序", "水喝完了", false, "1", true],
			["考试中选手自行重新启动机器，能否获得加时？", "否", "能", "也许能", "也许不能", false, "1", true],
			["草稿纸用完了，如何处理", "举手向监考人员求助", "向边上选手要一张", "使用自己带的草稿纸", "在桌上打草稿", false, "1", true],
			["水喝完了，如何处理", "举手向工作人员再要一瓶", "向边上选手要一瓶", "喝自己带的水", "不能喝更多的水", false, "1", true],
			["考试太简单，能提前离开吗？", "能", "不能", "工作人员说能就能", "工作人员说不能就不能", false, "1", true],
			["离开考场后，发现还有个问题没改，能回去再改吗？", "不能", "能", "工作人员说能就能", "工作人员说不能就不能", false, "1", true],
			["考试中机器突然没响应了，如何处理", "举手向监考人员求助", "重启机器", "关机", "等待机器响应", false, "1", true],
			["考试中发现登录名和密码的单子丢了，如何处理", "请工作人员处理，并需承担总成绩扣分的处罚", "离开考场", "使用 root 账户登录", "无法继续考试", false, "1", true],
			["复评的时候忘记登录名和密码了，如何处理", "请工作人员处理，并需承担总成绩扣分的处罚", "使用 friend 账户登录", "使用 root 账户登录", "无法进行复评", false, "1", true],
			["在监考人员宣布 NOI 机试开始之前，是否允许选手登录系统和翻阅试卷", "是", "否", "可能允许", "可能不允许", false, "2", true],
			["在NOI系列考试中，如果由于文件名不正确导致被判 0 分，提出复评请求，会被接受吗", "不会", "会", "可能会", "可能不会", false, "1", true],
			["在NOI系列考试中，如果由于文件目录名不正确导致被判 0 分，提出复评请求，会被接受吗", "不会", "会", "可能会", "可能不会", false, "1", true],
			["在NOI系列考试中，如果由于文件保存路径不正确导致被判 0 分，提出复评请求，会被接受吗", "不会", "会", "可能会", "可能不会", false, "1", true],
			["Lazarus 是可以支持多窗口编辑的 IDE 吗", "是", "不是", "有时候是", "有时候不是", false, "1", true],
			["Anjuta 是可以支持多窗口编辑的 IDE 吗", "是", "不是", "有时候是", "有时候不是", false, "1", true],
			["选手可以不使用IDE环境编辑程序源代码吗", "可以", "不可以", "可能可以", "可能不可以", false, "1", true],
			["选手回答填空题，提交的答案中可以包含引号吗", "不可以", "可以", "可能可以", "可能不可以", false, "1", true],
			["在NOI上机考试中，允许选手使用的编程语言包括", "C", "C++", "Pascal", "C++11", true, "123", true],
			["NOI比赛的题目类型有", "非交互式程序题", "交互式程序题", "答案提交题", "填空题", true, "123", true],
			["选手比赛中提交的有效文件类型有", "答案文件", "源程序", "输出文件", "输入文件", true, "12", true],
			["选手提交的程序不得进行的操作包括", "试图访问网络", "使用 fork 或其它线程/进程生成函数", "打开或创建题目规定的输入/输出文件之外的其它文件", "运行其它程序", true, "1234", true],
			["以修改过的程序或答案为依据的申诉是否会被受理", "否", "是", "可能是", "可能否", false, "1", true],
			["没有复测结果支持的申诉是否会被受理", "否", "是", "可能是", "可能否", false, "1", true],
			["超过申诉时间的申诉是否会被受理", "否", "是", "可能是", "可能否", false, "1", true],
			["遇到下列哪些情况可以向工作人员申请加时补偿", "计算机硬件故障，并由工作人员确认和记录", "操作系统死机，并由工作人员确认和记录", "题目理解有问题", "上厕所", true, "12", true],
			["考试时若遇到计算机硬件故障或操作系统死机，应如何处理", "举手向工作人员求助", "关机", "重启", "向边上的选手求助", false, "1", true],
			["选手进入考场可以携带的物品是", "笔", "手表", "手机", "纸", true, "12", true],
			["选手进入考场不可以携带的物品是", "纸", "U盘", "手机", "笔记本", true, "1234", true],
			["竞赛组织者将在竞赛场地为选手提供的物品是", "草稿纸", "饮用水", "食品", "笔", true, "123", true],
			["选手在复评过程中，若因丢失密码条而向工作人员索取密码，将", "被扣 5 分", "被扣 10 分", "被取消比赛资格", "什么都不会发生", false, "1", true],
			["选手程序在某测试点上的运行时间仅比时限多 0.005 秒，算不算超时", "算", "不算", "可能算", "可能不算", false, "1", true],
			["NOI 比赛中，选手的哪些行为是禁止的", "在监考人员宣布 NOI 机试开始之前翻看试题", "在监考人员宣布 NOI 机试开始之前登陆系统", "在监考人员宣布 NOI 机试开始之前触摸键盘、鼠标等外设", "使用网络", true, "1234", true],
			["在评测考生答案时，如果某测试点的运行内存超过内存限制，则", "程序不能正常运行，该测试点得0分", "程序能正常运行", "程序不能正常运行，该题目得0分", "程序不能正常运行，该天考试得0分", false, "1", true],
			["考试过程中如果考生之间互相讨论，将", "取消考生的考试资格", "取消当天的考试成绩", "取消讨论的试题的成绩", "什么都不会发生", false, "1", true],
			["一个完整的计算机系统应包括", "硬件系统", "软件系统", "操作系统", "显示器", true, "12", true],
			["目前微型计算机中采用的逻辑组件是", "大规模集成电路", "超大规模集成电路", "电子管", "晶体管", true, "12", true],
			["软件与程序的区别是", "软件是程序以及开发、使用和维护所需要的所有文档的总称", "程序是软件的一部分", "软件就是程序", "程序不是软件的一部分", true, "12", true],
			["IT 表示", "信息技术", "信息学", "信息学竞赛", "全国信息学竞赛", false, "1", true],
			["计算机中央处理器简称为", "CPU", "RAM", "ALU", "HDD", false, "1", true],
			["计算机内存储器的作用是用来存放", "当前 CPU 正在使用的程序", "当前 CPU 正在使用的数据", "计算机硬盘中的程序", "计算机硬盘中的数据", true, "12", true],
			["用来全面管理计算机硬件和软件资源的软件叫", "操作系统", "BIOS", "Linux", "固件", false, "1", true],
			["LAN 是指", "局域网", "广域网", "城域网", "无线网络", false, "1", true],
			["在微机中，bit 的中文含义是", "二进制位", "二进制", "字节", "字", false, "1", true],
			["计算机所能辨认的最小信息单位是", "位", "字节", "int", "字", false, "1", true],
			["ASCII 的含义是", "美国信息交换标准代码", "中国信息交换标准代码", "这个选项是错的", "这个选项也是错的", false, "1", true],
			["在计算机术语中经常用 RAM 表示", "随机存取存储器", "只读存储器", "硬盘", "顺序存取存储器", false, "1", true],
			["RAM 存储器在断电后，其中的数据", "会变化", "不会变化", "可能会变化", "可能不会变化", false, "1", true],
			["ROM 存储器在断电后，其中的数据", "不会变化", "会变化", "可能会变化", "可能不会变化", false, "1", true],
			["现代计算机所应用的存储程序原理是由谁提出的", "冯·诺依曼", "阿兰·图灵", "Dijkstra", "Tarjan", false, "1", true],
			["计算机内所有的信息都是以什么形式表示的", "二进制数码", "十进制数码", "十六进制数码", "八进制数码", false, "1", true],
			["计算机直接识别和执行的语言是", "机器语言", "汇编语言", "二进制", "高级语言", false, "1", true],
			["Linux 是一个开源的操作系统，意思是", "源码可以免费获得", "源码不可以免费获得", "Linux 不是免费的", "Linux 很贵", false, "1", true],
			["NOI 的中文意思是", "全国青少年信息学奥林匹克竞赛", "全国青少年信息学奥林匹克联赛", "国际青少年信息学奥林匹克竞赛", "国际青少年信息学奥林匹克联赛", false, "1", true],
			["字长为 32bit 的计算机,表示它能作为一个整体进行传送的数据长度可为多少个字节", "4", "1", "8", "32", false, "1", true],
			["一个字节由相邻的多少个二进制位组成", "8", "1", "4", "16", false, "1", true],
			["二进制数“10”化为十进制数是", "2", "1", "10", "0", false, "1", true],
			["与十六进制数（AB）等值的二进数是", "10101011", "10101111", "10000000", "10100011", false, "1", true],
			["Linux 中查看当前路径使用的命令是", "pwd", "ls", "cat", "ps", false, "1", true],
			["在 Linux 下建立目录使用的命令是", "mkdir", "ls", "rmdir", "cat", false, "1", true],
			["NOI 比赛中提供的 Pascal IDE 环境有", "GUIDE", "Lazarus", "Anjuta", "vim", true, "12", true],
			["NOI 比赛中提供的 C++ IDE 环境有", "GUIDE", "Lazarus", "Anjuta", "vim", true, "13", true],
			["NOI 比赛中提供的编程工具除了 GUIDE、Lazarus、Anjuta 等IDE环境之外，还可以使用的有", "vi", "gedit", "notepad", "cat", true, "12", true],
			["NOI 比赛每场上机考试的比赛时间是", "5 小时", "3 小时", "10 小时", "4 小时", false, "1", true],
			["首届 NOI 是在哪一年举办的", "1984", "2000", "1985", "2017", false, "1", true],
			["今年是第几届NOI？", "35", "34", "36", "33", false, "1", true],
			["今年是第几届IOI？", "30", "29", "28", "27", false, "1", true],
			["第 12 届IOI是哪一年在北京举办的", "2000", "1984", "1985", "2017", true, "1", true]
		];
		all_probs = [];
		for (var pid in probs) {
			all_probs.push(convert_problem(probs[pid]));
		}
	};
	
	return {
		init: init,
		check_answer: check_answer
	};
}();

beibishi.init();
if (window.screen.width > 1024) {
	document.body.style.zoom = window.screen.height / 640.0 * (360.0 / 980.0);
} else if (window.screen.height / window.screen.width < 16.0 / 9.0) {
	document.body.style.zoom = 1 * (window.screen.height / window.screen.width) / (16.0 / 9.0);
}
