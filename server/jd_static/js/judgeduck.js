// This is the judgeduck js lib

var judgeduck = function() {
	var timeout = 2000;
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
		var pass = md5(pass + pass_salt);
		do_post("/user/do_register", {
			username: user,
			email: email,
			password: pass
		}, function(data) {
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
		});
	};
	
	var register = function() {
		var user = $("#username").val();
		var email = $("#email").val();
		var pass1 = $("#password1").val();
		var pass2 = $("#password2").val();
		$("#btn_register").attr("disabled", true);
		if (do_register(user, email, pass1, pass2)) {
			window.location = "/";
		} else {
			$("#btn_register").attr("disabled", false);
			$("#username").focus();
		}
	};
	
	return {
		register: register
	};
}();
