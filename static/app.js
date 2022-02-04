function test(){
    document.getElementById("demo")
    let btn = document.createElement("button")
    btn.innerHTML = "Click Me"
    btn.type = "submit"
    btn.name = "nyrtakki"
    btn.onclick = function(){
        shit.remove()
        btn.remove()
    }
    document.body.appendChild(btn)
}






