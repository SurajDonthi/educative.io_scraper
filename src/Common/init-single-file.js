function initSingleFile() {
	singlefile.init({
		fetch: (url, options) => {
			return new Promise(function (resolve, reject) {
				const xhrRequest = new XMLHttpRequest();
				xhrRequest.withCredentials = true;
				xhrRequest.responseType = "arraybuffer";
				xhrRequest.onerror = event => reject(new Error(event.detail));
				xhrRequest.onabort = () => reject(new Error("aborted"));
				xhrRequest.onreadystatechange = () => {
					if (xhrRequest.readyState == XMLHttpRequest.DONE) {
						resolve({
							arrayBuffer: async () => xhrRequest.response || new ArrayBuffer(),
							headers: { get: headerName => xhrRequest.getResponseHeader(headerName) },
							status: xhrRequest.status
						});
					}
				};
				xhrRequest.open("GET", url, true);
				if (options.headers) {
					for (const entry of Object.entries(options.headers)) {
						xhrRequest.setRequestHeader(entry[0], entry[1]);
					}
				}
				xhrRequest.send();
			});
		}
	});
}