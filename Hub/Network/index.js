async function connectWifi(){
    const ssid = document.getElementById("ssid").value
    const password = document.getElementById("password").value

    const response = await fetch("/wifi",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({ ssid, password })
    })

    const data = await response.json()

    if(data.success){
        alert("Connected to Wifi")
    } else {
        alert("Wrong SSID or password. Please try again.")
    }
}