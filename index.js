import { ipcRenderer } from "electron";

function pingpong(){
	console.log(ipcRenderer.sendSync('synchronous-message', 'ping'))
}