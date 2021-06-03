// importing
const fs = require("fs");
const { ipcRenderer } = require("electron");

function pingpong(){
	console.log(ipcRenderer.sendSync('test', 'ping'))
}

