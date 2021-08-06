let subpy;
const { app, BrowserWindow } = require('electron')

// input
if (app.isPackaged) {
  // workaround for missing executable argument)
  process.argv.unshift(null)
}
// parameters is now an array containing any files/folders that your OS will pass to your application
const parameters = process.argv.slice(2)

// window
function createWindow () {
  const win = new BrowserWindow({
    width: 1920,
    height: 1080,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  })

  win.loadFile('./www/index.html')
}

app.whenReady().then(()=>{
	subpy = require('child_process').spawn('python3', ['./hello.py']);
	createWindow()
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
	subpy.kill('SIGINT');
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})
