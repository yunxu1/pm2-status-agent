//npm install pm2 -save
//npm install ws -save

var pm2 = require('pm2');
var WebSocket = require("ws");

websocket_host="ws://10.211.55.2:8080/websocket";
local_address=getIPAdress();

function getIPAdress(){  
    var interfaces = require('os').networkInterfaces();  
    for(var devName in interfaces){  
          var iface = interfaces[devName];  
          for(var i=0;i<iface.length;i++){  
               var alias = iface[i];  
               if(alias.family === 'IPv4' && alias.address !== '127.0.0.1' && !alias.internal){  
                     return alias.address;  
               }  
          }  
    }  
} 

function sendMsg(msg_text){
   const ws = new WebSocket(websocket_host);
    ws.on('open', function open() {
      ws.send(msg_text);
    });

    ws.on('error',function(){
      console.log('error');
    });
}

function pm2ProccessStatus(){
  pm2.list(function(err,proccessDesc){
      info={"host":local_address,"proccess":[],"proccessNameItem":[]};
      if (proccessDesc!=[]){
            proccessDesc.forEach(function(procces){
            procInformat={"host":local_address,"pid":procces.pid,"name":procces.name,"status":procces.pm2_env.status};
            console.log(procInformat);
            info['proccessNameItem'].push("'"+procces.name+"'");
            info['proccess'].push(procInformat);
        });
      }
      try{sendMsg(JSON.stringify(info))}catch(err){}
  });
}



setInterval(pm2ProccessStatus,10000);
