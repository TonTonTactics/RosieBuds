window.onload = function () {
    const securitySelect = document.getElementById("security");
    const authSelect = document.getElementById("authentication");

    securitySelect.addEventListener("change", handleSecurityChange);
    authSelect.addEventListener("change", handleAuthChange);

    handleSecurityChange();
};

function hideDiv(id) {
    const el = document.getElementById(id);
    if (el) el.style.display = "none";
}

function showDiv(id) {
    const el = document.getElementById(id);
    if (el) el.style.display = "block";
}

function handleSecurityChange() {
    const sec = document.getElementById("security").value;

    const allDivs = [
        "leapDiv",
        "wpa2personalDiv",
        "wpa2enterpriseDiv",
        "wpa3personalDiv",
        "tlsauthDiv",
        "leapauthDiv",
        "pwdDiv",
        "fastDiv",
        "ttlsauthDiv",
        "peapDiv",
    ];

    allDivs.forEach(hideDiv);

    if (sec === "leap") {
        showDiv("leapDiv");
    } else if (sec === "wpa2personal") {
        showDiv("wpa2personalDiv");
    } else if (sec === "wpa2enterprise") {
        showDiv("wpa2enterpriseDiv");
        handleAuthChange();
    } else if (sec === "wpa3personal") {
        showDiv("wpa3personalDiv");
    }
}

function handleAuthChange() {
    const auth = document.getElementById("authentication").value;

    const authDivs = [
        "tlsauthDiv",
        "leapauthDiv",
        "pwdDiv",
        "fastDiv",
        "ttlsauthDiv",
        "peapDiv",
    ];

    authDivs.forEach(hideDiv);

    if (auth === "tls") {
        showDiv("tlsauthDiv");
    } else if (auth === "leap") {
        showDiv("leapauthDiv");
    } else if (auth === "pwd") {
        showDiv("pwdDiv");
    } else if (auth === "fast") {
        showDiv("fastDiv");
    } else if (auth === "ttls") {
        showDiv("ttlsauthDiv");
    } else if (auth === "peap") {
        showDiv("peapDiv");
    }
}

document.getElementById("connectBtn").addEventListener("click", connectWifi);
async function connectWifi() {
    const statusEl = document.getElementById("status");
    const wifiname = document.getElementById("networkname").value.trim();
    const security = document.getElementById("security").value;

    if (!wifiname) {
        statusEl.innerText = "Please enter a WiFi name!";
        return;
    }

    let body = { wifiname };

    if (security === "none") {
        body.type = "open";
    } 
    
    else if (security === "wpa2personal") {
        body.type = "wpa_personal";
        body.password = document.getElementById("wpapersonalpassword").value;
    } 
    
    else if (security === "wpa3personal") {
        body.type = "wpa3personal";
        body.password = document.getElementById("wpa3password").value;
    } 
    
    else if (security === "leap") {
        body.type = "leap";
        body.username = document.getElementById("leapusername").value;
        body.password = document.getElementById("leappassword").value;
    } 
    
    else if (security === "enhancedopen") {
        body.type = "eopen";
    } 
    
    else if (security === "wpa2enterprise") {
        const auth = document.getElementById("authentication").value;

        if (auth === "peap") {
            body.type = "wpa_enterprise_peap";
            body.username = document.getElementById("peapusername").value;
            body.password = document.getElementById("peappassword").value;
            body.anonid = document.getElementById("peapanonymousidentity").value || null;
            body.domain = document.getElementById("peapdomain").value || null;
            body.cacertpassword = document.getElementById("peapcacertpassword").value || null;
            body.noncacert = document.getElementById("peapnocacert").checked;
            body.innerauth = document.getElementById("peapinnerauth").value || null;
        } 
        
        else if (auth === "ttls") {
            body.type = "wpa_enterprise_ttls";
            body.username = document.getElementById("ttlsusername").value;
            body.password = document.getElementById("ttlspassword").value;
            body.anonid = document.getElementById("ttlsanonymousidentity").value || null;
            body.domain = document.getElementById("ttlsdomain").value || null;
            body.cacertpassword = document.getElementById("ttlscacertpassword").value || null;
            body.noncacert = document.getElementById("ttlsnocacert").checked;
            body.innerauth = document.getElementById("ttlsinnerauth").value || null;
        } 
        
        else if (auth === "pwd") {
            body.type = "wpa_enterprise_pwd";
            body.pwdusername = document.getElementById("pwdusername").value;
            body.pwdpassword = document.getElementById("pwdpassword").value;
        } 
        
        else if (auth === "fast") {
            body.type = "wpa_enterprise_fast";
            body.username = document.getElementById("fastusername").value;
            body.password = document.getElementById("fastpassword").value;
            body.anonid = document.getElementById("anonymousidentity").value || null;
            body.pacprov = document.getElementById("pacprovisioning").value || null;
            body.innerauth = document.getElementById("innerauth").value || null;
        } 
        
        else if (auth === "leap") {
            body.type = "wpa_enterprise_leap";
            body.leapusername = document.getElementById("leapauthusername").value;
            body.leappassword = document.getElementById("leapauthpassword").value;
        } 
        
        else if (auth === "tls") {
            body.type = "wpa_enterprise_tls";
            body.tlsid = document.getElementById("tlsidentity").value;
            body.domain = document.getElementById("tlsdomain").value || null;
            body.cacertpassword = document.getElementById("tlscacertpassword").value || null;
            body.nocacert = document.getElementById("tlsnocacert").checked;
            body.usercertpassword = document.getElementById("tlsusercertpassword").value || null;
            body.userPKpassword = document.getElementById("tlsuserprivatekeypassword").value || null;
        }
    }

    statusEl.innerText = "Connecting...";

    try {
        const res = await fetch("/wifi", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        });

        const data = await res.json();

        if (!res.ok) {
            statusEl.innerText = data.detail
                ? JSON.stringify(data.detail)
                : "Connection failed";
            return;
        }

        if (data.connection?.status) {
            statusEl.innerText = `Saved: ${data.connection.status}`;
        } else if (data.status) {
            statusEl.innerText = data.status;
        } else {
            statusEl.innerText = "Done";
        }
    } catch (err) {
        console.error(err);
        statusEl.innerText = "Connection failed";
    }
}