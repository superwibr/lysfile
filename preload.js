

function pingpong(){
	let ipcRenderer = require('electron').ipcRenderer
	console.log(ipcRenderer.sendSync('synchronous-message', 'ping'))
}

global.pingpong = pingpong