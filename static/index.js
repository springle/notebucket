function push(token) {
    fetch("https://api.notebucket.dev/push?noteid=" + document.getElementById("noteid").value , {
        method: "PUT",
        headers: {
            'reCAPTCHA-Token': token
        },
        body: CryptoJS.AES.encrypt(
            document.getElementById("note").value,
            document.getElementById("notekey").value
        ).toString()
    }).then(response => {
        if (response.status == 200) {
            console.log("success")
        }
    })
}

function pull(token) {
    fetch("https://api.notebucket.dev/pull?noteid=" + document.getElementById("noteid").value, {
        method: "GET",
        headers: {
            'reCAPTCHA-Token': token
        }
    })
    .then(response => response.json())
    .then(data => document.getElementById("note").value =
        CryptoJS.AES.decrypt(
            data["note"],
            document.getElementById("notekey").value
        ).toString(CryptoJS.enc.Utf8)
    )
}