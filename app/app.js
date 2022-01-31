function test(){
    document.getElementById("demo").innerHTML = "Hello JavaScript!";
    const shit = document.createElement("p")
    shit.innerText = "Loogdaf fullt"
    let btn = document.createElement("button");
    btn.innerHTML = "Click Me";
    btn.type = "submit"
    btn.name = "nyrtakki"
    btn.onclick = function(){
        shit.remove()
        btn.remove()
    }
    document.body.appendChild(shit)
    document.body.appendChild(btn)
}






