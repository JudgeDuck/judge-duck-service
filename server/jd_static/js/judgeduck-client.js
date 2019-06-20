// This is the judgeduck js client

var duckclient = function() {
	var conf = {
		server_url: "wss://api.duck-ac.cn",
		token: "anonymous",
		debug: console.log
	};
	
	var debug = function(a) {
		return conf.debug(a);
	};
	
	/*
		List of states:
		"connecting"
		"connected": Right after connected, sending hello.
		"negotiating": Right after hello response, negotiating judge protocol.
		"send-code": Sending user code.
		"send-input": Sending input data.
		"judging": Receiving judge results.
		
		Protocol: "custom-test:20190309"
		
		Submission format:
		"code": "int mian() {}", no more than 100KB
		"language": "C++/C++11/C"
		"input": input data no more than 100KB
	*/
	var do_custom_test = function(submission, callback) {
		if (function(s) {
			if (typeof s != "object") return true;
			if (typeof s.code != "string") return true;
			if (typeof s.language != "string") return true;
			if (typeof s.input != "string") return true;
			return false;
		} (submission)) {
			callback(undefined, "Invalid submission.");
			return;
		}
		
		var ws = new WebSocket(conf.server_url);
		var state = "connecting";
		var terminated = false;
		var terminate = function(res, err) {
			terminated = true;
			ws.close();
			callback(res, err);
		};
		ws.sendJSON = function(data) {this.send(JSON.stringify(data));};
		ws.onopen = function(event) {
			state = "connected";
			ws.sendJSON({"token": conf.token});
			ws.sendJSON({"protocol": "custom-test:20190309"});
			ws.sendJSON({"code": submission.code, "language": submission.language});
			ws.sendJSON({"type": "text", "content": submission.input});
			debug("Connected, sending hello.");
		};
		ws.onmessage = function(event) {
			debug("on message: " + event.data);
			var data = undefined;
			try {
				data = JSON.parse(event.data);
			} catch (e) {}
			
			if (typeof data != "object") {
				return terminate(undefined, "Invalid response.");
			}
			
			if (state == "connected") {
				if (data.status != "ok") {
					return terminate(undefined, "Auth failed: " + data.error);
				}
				state = "negotiating";
				// already sent
				debug("Auth ok, sending protocol.");
			} else if (state == "negotiating") {
				if (data.status != "ok") {
					return terminate(undefined, "Negotiation failed: " + data.error);
				}
				state = "send-code";
				// already sent
				debug("Negotiation done, sending code.");
			} else if (state == "send-code") {
				if (data.status != "ok") {
					return terminate(undefined, "Send code failed: " + data.error);
				}
				state = "send-input";
				// already sent
				debug("Sending input.");
			} else if (state == "send-input") {
				if (data.status != "ok") {
					return terminate(undefined, "Send input failed: " + data.error);
				}
				state = "judging";
				debug("Judging...");
			} else if (state == "judging") {
				if (data.type == "error") {
					return terminate(undefined, "Judge failed: " + data.error);
				}
				if (data.type == "final") {
					return terminate(data.data, undefined);
				} else if (data.type == "partial") {
					callback(data, undefined);
				}
			}
		};
		ws.onclose = function(event) {
			// on close!!
			if (!terminated) {
				terminate(undefined, "Network error.");
			}
		};
	};
	
	return {
		conf: conf,
		do_custom_test: do_custom_test,
		test_wraper: function() {
			do_custom_test(
				{
					"code": '#include <stdio.h>\nint main() {puts("233333\\\n");}',
					"language": "C++",
					"input": "1 2\n"
				},
				function(res, err) {
					if (err) {
						console.log(err);
					} else {
						console.log(res);
					}
				}
			);
		}
	};
}();

