// planter
const planter = (()=>{
    // main object
    var planter = {
        readFromFileContent(inputid){
            var input, fr, content;

            input = document.getElementById(inputid);
    
            fr = new FileReader(); 
            fr.onload = function(){ planter.read(fr.result) }
            fr.readAsText(input.files[0]);
        },
        read(filecontent){
            // variables
            var sections, protocol, parameters, content;

            // assigning
            sections = filecontent.split('===$');
            protocol = sections[0];
            parameters = sections[1].split(',');
            content = JSON.parse(sections[2]);

            // sending to correct protocol
            switch(protocol){
                case'BUNDL': return planter.read.bundle(parameters, content);
                case'BOOKM': return planter.read.bookmark(parameters, content);
                case'PLANT': return planter.read.planter(parameters, content);
            }
        },
        writeFromFile(content){
            planter.write
        },
        write(){}
    }

    //
    // Read methods
    //
    planter.read.bundle = (params, content)=>{
        // info line
        document.body.insertAdjacentHTML('beforeend', '<span>Lysent Bundle File. </span><br>')
        if(params.includes('raw')){ document.body.insertAdjacentHTML('beforeend', '<span>Raw parameter set to true. Files will not be decoded. </span><br>') }
        if(params.includes('download')){ 
            document.body.insertAdjacentHTML('beforeend', '<span>Download parameter set to true. Files will auto-download.</span><br>') 
        }else{
            document.body.insertAdjacentHTML('beforeend', '<span>Download parameter set to false. Files will list below.</span><br><br>')
        }

        // looping through bundle entries
        for (let i = 0; i < content.length; i++) {
            const value = content[i];

            // if it's a comment (or missing content)
            if(!value.content) continue

            // decode
            if(params.includes('raw')){
                var ccontent = value.content
            }else{
                var ccontent = ascii85.decode(value.content)
            }

            // if it downloads
            if(params.includes('download')){
                // download
                var element = document.createElement('a');
                element.setAttribute('href', 'data:;charset=utf-8,'+encodeURIComponent(ccontent))
                element.setAttribute('download', value.name);
        
                element.style.display = 'none';
                document.body.appendChild(element);
        
                element.click();
        
                document.body.removeChild(element);
                continue
            }
            // if it displays
            console.log(ccontent)
            var element = document.createElement('a');
            element.setAttribute('href', 'data:application/octet-stream;charset=utf-8,'+encodeURIComponent(ccontent));
            element.setAttribute('download', value.name);
            element.innerText = value.name
            document.body.appendChild(element);
            document.body.appendChild(document.createElement('br'));
        }
    }

    planter.read.bookmark = (params, content)=>{
        var title, list, link, linkLabel;

        // info line
        document.body.insertAdjacentHTML('beforeend', '<span>Lysent Bookmarks File. </span><br>')

        // adding tags & reference
        document.body.insertAdjacentHTML('beforeend', '<h2 id="bookm-title"></h2>')
        document.body.insertAdjacentHTML('beforeend', '<ul id="bookm-list"></ul>')
        title = document.querySelector('#bookm-title')
        list = document.querySelector('#bookm-list')

        // looping through content entries
        for(var i = 0; i < content.length; i++){

            // Document title
            if(i == 0) {
                title.innerText = content[0]
                continue
            }

            // title
            if(content[i].title) list.insertAdjacentHTML('beforeend', `<li><h2>${content[i].title}</h2></li>`);continue

            // link
        }

    }
    planter.read.planter = (params, content)=>{}

    //
    // Write methods
    //
    planter.write.bundle = async (params)=>{
        var file, input, content
        file = 'BUNDL===$'

        // adding params to file
        var parameters = JSON.stringify(params)
        var subpar = parameters.substring(1, parameters.length - 1)
        file = file.concat(subpar+'===$')

        // creating content section
        content = []
        var i = 0
        input = document.getElementById('fileInput');
        for (var i = 0; i < input.files.length; i++) { 
            content[i] = {}
            console.log(content[i])
            content[i].content = await new Promise((resolve) => {
                let fr = new FileReader();
                fr.onload = (e) => {
                    if(params.includes('raw')){
                        resolve(fr.result);
                    }else{
                        resolve(ascii85.encode(fr.result));
                    }
                }
                fr.readAsText(input.files[i]);
            });
            console.log(content[i].content)
            content[i].name = input.files[i].name
        }
        file = file.concat(JSON.stringify(content))
        console.log(file)
        return file
    }
    planter.write.bookmark = (params, content)=>{}
    planter.write.planter = (params, content)=>{}

    // 
    // private methods
    //
    planter._$ = function(query){
        return document.querySelector(query)
    }

    // return public methods
    return planter
})()