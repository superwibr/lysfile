// importing
const fs = require("fs");
//const { ipcRenderer } = require("electron");
const path = require('path');

/* IPC test
function pingpong(){
	console.log(ipcRenderer.sendSync('test', 'ping'))
}
*/

// define the main object and add the file manager
const planter = {}

planter.loadContent = async function(filepath, selector){
	let data = await fs.readFileSync(path.resolve(__dirname, filepath), 'utf8')
	document.querySelector(selector).innerHTML = await data
}
