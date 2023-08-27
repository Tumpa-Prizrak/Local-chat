function addOption(id_, content_) {
    var pre = document.createElement("option");
    var content = document.getElementById(id_);

    pre.innerHTML = content_

    content.parentNode.insertBefore(pre, content);
    content.appendChild(pre);
}

function getToken() {
    let cookies = getCookies();
    
    if (cookies.has("token")) {
        return cookies.get("token");
    } else {
        window.location.replace("/src/web_client/login/");
    }
}

function getCookies(){
    let cookies = new Map();
    for (let egg of document.cookie.split("; ")){
        let span = egg.split("=");
        cookies.set(span[0], span[1]);
    }
    
    return cookies;
}
