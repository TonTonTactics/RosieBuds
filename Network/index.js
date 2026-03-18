    window.onload = function() {
    const securitySelect = document.getElementById('security');
    const authSelect = document.getElementById('authentication');

    securitySelect.addEventListener('change', handleSecurityChange);
    authSelect.addEventListener('change', handleAuthChange);

    handleSecurityChange();
};

function handleSecurityChange() {
    const sec = document.getElementById('security').value;

    const allDivs = [
        'leapDiv','wpa2personalDiv','wpa2enterpriseDiv','wpa3personalDiv',
        'tlsauthDiv','leapauthDiv','pwdDiv','fastDiv','ttlsauthDiv','peapDiv'
    ];
    allDivs.forEach(id => document.getElementById(id).style.display = 'none');

    if (sec === 'leap') document.getElementById('leapDiv').style.display = 'block';
    else if (sec === 'wpa2personal') document.getElementById('wpa2personalDiv').style.display = 'block';
    else if (sec === 'wpa2enterprise') {
        document.getElementById('wpa2enterpriseDiv').style.display = 'block';
        handleAuthChange(); // show selected auth
    }
    else if (sec === 'wpa3personal') document.getElementById('wpa3personalDiv').style.display = 'block';
}

function handleAuthChange() {
    const auth = document.getElementById('authentication').value;

    const authDivs = ['tlsauthDiv','leapauthDiv','pwdDiv','fastDiv','ttlsauthDiv','peapDiv'];
    authDivs.forEach(id => document.getElementById(id).style.display = 'none');

    if (auth === 'tls') document.getElementById('tlsauthDiv').style.display = 'block';
    else if (auth === 'leap') document.getElementById('leapauthDiv').style.display = 'block';
    else if (auth === 'pwd') document.getElementById('pwdDiv').style.display = 'block';
    else if (auth === 'fast') document.getElementById('fastDiv').style.display = 'block';
    else if (auth === 'ttls') document.getElementById('ttlsauthDiv').style.display = 'block';
    else if (auth === 'peap') document.getElementById('peapDiv').style.display = 'block';
}

async function connectWifi() {
    const ssid = document.getElementById('networkname').value;
    const security = document.getElementById('security').value;

    if (!ssid) {
        document.getElementById('status').innerText = 'Please enter a WiFi name!';
        return;
    }

    let body = { ssid };

    if (security === "none") {
        body.type = "open";
    }

    else if (security === "wpa2personal") {
        body.type = "wpa_personal";
        body.password = document.getElementById('wpapersonalpassword').value;
    }

    else if (security === "wpa3personal") {
        body.type = "wpa3";
        body.password = document.getElementById('wpa3password').value;
    }

    else if (security === "leap") {
        body.type = "leap";
        body.username = document.getElementById('leapusername').value;
        body.password = document.getElementById('leappassword').value;
    }

    else if (security === "enhancedopen") {
        body.type = "eopen";
    }

    else if (security === "wpa2enterprise") {
        const auth = document.getElementById('authentication').value;

        if (auth === "peap") {
            body.type = "wpa_enterprise_peap";
            body.username = document.getElementById('peapusername').value;
            body.password = document.getElementById('peappassword').value;
            body.anonid = document.getElementById('peapanonymousidentity').value;
            body.domain = document.getElementById('peapdomain').value;
            body.cacertpassword = document.getElementById('peapcacertpassword').value;
            body.noncacert = document.getElementById('peapnocacert').checked;
            body.innerauth = document.getElementById('peapinnerauth').value;
        }

        else if (auth === "ttls") {
            body.type = "wpa_enterprise_ttls";
            body.username = document.getElementById('ttlsusername').value;
            body.password = document.getElementById('ttlspassword').value;
            body.anonid = document.getElementById('ttlsanonymousidentity').value;
            body.domain = document.getElementById('ttlsdomain').value;
            body.cacertpassword = document.getElementById('ttlscacertpassword').value;
            body.noncacert = document.getElementById('ttlsnocacert').checked;
            body.innerauth = document.getElementById('ttlsinnerauth').value;
        }

        else if (auth === "pwd") {
            body.type = "wpa_enterprise_pwd";
            body.pwdusername = document.getElementById('pwdusername').value;
            body.pwdpassword = document.getElementById('pwdpassword').value;
        }

        else if (auth === "fast") {
            body.type = "wpa_enterprise_fast";
            body.username = document.getElementById('fastusername').value;
            body.password = document.getElementById('fastpassword').value;
            body.anonid = document.getElementById('anonymousidentity').value;
            body.pacprov = document.getElementById('pacprovisioning').value;
            body.innerauth = document.getElementById('innerauth').value;
        }

        else if (auth === "leap") {
            body.type = "wpa_enterprise_leap";
            body.leapusername = document.getElementById('leapauthusername').value;
            body.leappassword = document.getElementById('leapauthpassword').value;
        }

        else if (auth === "tls") {
            body.type = "wpa_enterprise_tls";
            body.tlsid = document.getElementById('tlsidentity').value;
            body.domain = document.getElementById('tlsdomain').value;
            body.cacertpassword = document.getElementById('tlscacertpassword').value;
            body.nocacert = document.getElementById('tlsnocacert').checked;
            body.usercertpassword = document.getElementById('tlsusercertpassword').value;
            body.userPKpassword = document.getElementById('tlsuserprivatekeypassword').value;
        }
    }

    try {
        const res = await fetch("/wifi", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });

        const data = await res.json();
        document.getElementById('status').innerText = data.status;

    } catch (err) {
        document.getElementById('status').innerText = "Connection failed";
        console.error(err);
    }
}