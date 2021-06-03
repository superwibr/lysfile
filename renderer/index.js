import { ipcRenderer } from "electron";

function pingpong(){
	ipcRenderer.sendSync('test', 'ping')
}