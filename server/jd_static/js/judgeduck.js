// This is the judgeduck js lib

var judgeduck = function() {
	var timeout = 10000;
	var user_regex = /^[a-zA-Z0-9_]{3,20}$/;
	var email_regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	var pass_regex = /^.{1,100}$/;
	var pass_salt = "jdo123456789";
	
	var do_post = function(url, contents, callback) {
		$.ajax({
			method: "POST",
			url: url,
			data: contents,
			timeout: timeout,
			success: function(data) {
				callback(data);
			},
			error: function() {
				callback(null);
			}
		});
	};
	
	var do_register = function(user, email, pass1, pass2) {
		if (user.match(user_regex) == null) {
			return alert("用户名必须由 3 ~ 20 个字母、数字或下划线组成！");
		}
		if (email.match(email_regex) == null) {
			return alert("电子邮件地址不合法！");
		}
		if (pass1 != pass2) {
			return alert("两次输入的密码不一致！");
		}
		if (pass1.match(pass_regex) == null) {
			return alert("密码太短或太长！");
		}
		var pass = md5(pass1 + pass_salt);
		do_post("/user/do_register", {
			username: user,
			email: email,
			password: pass
		}, function(data) {
			var ret = function(data) {
				if (!data) {
					return alert("注册失败：网络错误");
				}
				if (data["status"] == "success") {
					alert("注册成功");
					return true;
				}
				if (data["status"] == "failed") {
					return alert("注册失败：" + data["error"]);
				}
				return alert("注册失败：未知错误");
			}(data);
			if (ret) {
				window.location = "/";
			} else {
				$("#btn_register").attr("disabled", false);
				$("#username").focus();
			}
		});
		return true;
	};
	
	var do_login = function(user, pass) {
		pass = md5(pass + pass_salt);
		do_post("/user/do_login", {
			username: user,
			password: pass
		}, function(data) {
			var ret = function(data) {
				if (!data) {
					return alert("登录失败：网络错误");
				}
				if (data["status"] == "success") {
					return true;
				}
				if (data["status"] == "failed") {
					return alert("登录失败：" + data["error"]);
				}
				return alert("登录失败：未知错误");
			}(data);
			if (ret) {
				window.location = "/index";
			} else {
				$("#btn_login").attr("disabled", false);
				$("#password").focus();
			}
		});
	};
	
	var do_edit_profile = function(pass, email, pass1, pass2, signature) {
		pass = md5(pass + pass_salt);
		if (email.match(email_regex) == null) {
			return alert("电子邮件地址不合法！");
		}
		if (pass1 != pass2) {
			return alert("两次输入的密码不一致！");
		}
		if (pass1 != "" && pass1.match(pass_regex) == null) {
			return alert("密码太短或太长！");
		}
		if (pass1 != "") {
			pass1 = md5(pass1 + pass_salt);
		}
		do_post("/user/do_edit_profile", {
			password: pass,
			email: email,
			new_password: pass1,
			signature: signature
		}, function(data) {
			var ret = function(data) {
				if (!data) {
					return alert("更改失败：网络错误");
				}
				if (data["status"] == "success") {
					return true;
				}
				if (data["status"] == "failed") {
					return alert("更改失败：" + data["error"]);
				}
				return alert("更改失败：未知错误");
			}(data);
			if (ret) {
				window.location = "/user/profile/" + data["username"];
			} else {
				$("#btn_edit_profile").attr("disabled", false);
				$("#password").focus();
			}
		});
		return true;
	};
	
	var do_submit = function(pid, language, code) {
		do_post("/do_submit", {
			pid: pid,
			language: language,
			code: code
		}, function(data) {
			var ret = function(data) {
				if (!data) {
					return alert("提交失败：网络错误");
				}
				if (data["status"] == "success") {
					return true;
				}
				if (data["status"] == "failed") {
					return alert("提交失败：" + data["error"]);
				}
				return alert("提交失败：未知错误");
			}(data);
			if (ret) {
				window.location = "/submissions";
			} else {
				$("#btn_submit").attr("disabled", false);
				$("#code").focus();
			}
		});
	};
	
	var do_post_blog = function(title, content) {
		if (title == "") {
			return alert("发表失败：标题为空");
		}
		if (title.length > 50) {
			return alert("发表失败：标题太长");
		}
		do_post("/blog/do_post", {
			title: title,
			content: content
		}, function(data) {
			var ret = function(data) {
				if (!data) {
					return alert("发表失败：网络错误");
				}
				if (data["status"] == "success") {
					return true;
				}
				if (data["status"] == "failed") {
					return alert("发表失败：" + data["error"]);
				}
				return alert("发表失败：未知错误");
			}(data);
			if (ret) {
				window.location = "/blog/" + data["bid"];
			} else {
				$("#btn_post_blog").attr("disabled", false);
				$("#title").focus();
			}
		});
	};
	
	var do_edit_blog = function(bid, title, content) {
		if (title == "") {
			return alert("修改失败：标题为空");
		}
		if (title.length > 50) {
			return alert("修改失败：标题太长");
		}
		do_post("/blog/do_edit", {
			bid: bid,
			title: title,
			content: content
		}, function(data) {
			var ret = function(data) {
				if (!data) {
					return alert("修改失败：网络错误");
				}
				if (data["status"] == "success") {
					return true;
				}
				if (data["status"] == "failed") {
					return alert("修改失败：" + data["error"]);
				}
				return alert("修改失败：未知错误");
			}(data);
			if (ret) {
				window.location = "/blog/" + bid;
			} else {
				$("#btn_edit_blog").attr("disabled", false);
				$("#title").focus();
			}
		});
	};
	
	var register = function() {
		var user = $("#username").val();
		var email = $("#email").val();
		var pass1 = $("#password1").val();
		var pass2 = $("#password2").val();
		$("#btn_register").attr("disabled", true);
		if (!do_register(user, email, pass1, pass2)) {
			$("#btn_register").attr("disabled", false);
			$("#username").focus();
		}
	};
	
	var login = function() {
		var user = $("#username").val();
		var pass = $("#password").val();
		$("#btn_login").attr("disabled", true);
		do_login(user, pass);
	};
	
	var edit_profile = function() {
		var pass = $("#password").val();
		var email = $("#email").val();
		var pass1 = $("#password1").val();
		var pass2 = $("#password2").val();
		var signature = $("#signature").val();
		$("#btn_edit_profile").attr("disabled", true);
		if (!do_edit_profile(pass, email, pass1, pass2, signature)) {
			$("#btn_edit_profile").attr("disabled", false);
			$("#password").focus();
		}
	};
	
	var vote_problem = function(pid, val, prev_val) {
		var up = $("#vote_up_" + pid);
		var down = $("#vote_down_" + pid);
		var value = $("#vote_value_" + pid);
		up.css("color", "#ccc");
		up.css("font-weight", "normal");
		down.css("color", "#ccc");
		down.css("font-weight", "normal");
		up.attr("href", "javascript:judgeduck.vote_problem('" + pid + "', 1, " + val + ")");
		down.attr("href", "javascript:judgeduck.vote_problem('" + pid + "', -1, " + val + ")");
		
		if (val == 1) {
			up.css("color", "green");
			up.css("font-weight", "bold");
			up.attr("href", "javascript:judgeduck.vote_problem('" + pid + "', 0, " + val + ")");
			down.attr("href", "javascript:judgeduck.vote_problem('" + pid + "', 0, " + val + ")");
		} else if (val == -1) {
			down.css("color", "red");
			down.css("font-weight", "bold");
			up.attr("href", "javascript:judgeduck.vote_problem('" + pid + "', 0, " + val + ")");
			down.attr("href", "javascript:judgeduck.vote_problem('" + pid + "', 0, " + val + ")");
		}
		
		var org_val = val;
		val += parseInt(value.text()) - prev_val;
		value.css("color", val > 0 ? "green" : val == 0 ? "#ccc" : "red");
		value.text(val > 0 ? "+" + val : "" + val);
		
		do_post("/problems/do_vote", {
			pid: pid,
			value: org_val
		}, function(data) {
			if (!data) {
				return alert("网络错误");
			}
			if (data["status"] == "failed") {
				return alert(data["error"]);
			}
			if (data["status"] == "success") {
				return;
			}
			return alert("未知错误");
		});
	};
	
	var submit = function() {
		var pid = $("#pid").val();
		var language = $("#language").val();
		var code = $("#code").val();
		$("#btn_submit").attr("disabled", true);
		do_submit(pid, language, code);
	};
	
	var post_blog = function() {
		var title = $("#title").val();
		var content = simplemde.value();
		$("#btn_post_blog").attr("disabled", true);
		if (!do_post_blog(title, content)) {
			$("#btn_post_blog").attr("disabled", false);
			$("#title").focus();
		}
	};
	
	var edit_blog = function() {
		var bid = $("#bid").val();
		var title = $("#title").val();
		var content = simplemde.value();
		$("#btn_edit_blog").attr("disabled", true);
		if (!do_edit_blog(bid, title, content)) {
			$("#btn_edit_blog").attr("disabled", false);
			$("#title").focus();
		}
	};
	
	return {
		register: register,
		login: login,
		edit_profile: edit_profile,
		vote_problem: vote_problem,
		submit: submit,
		post_blog: post_blog,
		edit_blog: edit_blog
	};
}();
