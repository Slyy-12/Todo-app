
// let Reading = msg.payload;
// if (Reading <= 1.26){
//     msg.payload = "PASS";
// }
// else{
//     msg.payload="FAIL";
// }
// return msg;

function voltage_check(reading){
    
    if (reading <= 1.26){
        Node.send = "PASS";
        
    }
    else if (reading > 1.26){
        Node.send = "FAIL";
    }}
    return output;
    