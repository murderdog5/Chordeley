let selectedRoot = null;
let selectedQuality = "maj";
let selectedTensions = []; 

// ルート選択ボタン取得→リスト化
const chord_btns = document.querySelectorAll(".chord-btn");
// 選択時に
// 1. .selectedクラスを追加して見た目を変更
// 2. 変数selectedRootに選択したボタンの文字を代入
chord_btns.forEach(function(btn){
    btn.addEventListener("click",function(){
        chord_btns.forEach(function(i){i.classList.remove("selected")});
        btn.classList.add("selected");
        selectedRoot = btn.textContent;
        console.log(btn.textContent);
    });
});

const quality_btns = document.querySelectorAll(".quality-btn");
quality_btns.forEach(function(btn){
    btn.addEventListener("click",function(){
        quality_btns.forEach(function(i){i.classList.remove("selected")});
        btn.classList.add("selected");
        selectedQuality = btn.textContent;
        console.log(btn.textContent);
    });
});

const tension_btns = document.querySelectorAll(".tension-btn");
tension_btns.forEach(function(btn){
    btn.addEventListener("click",function(){
        if(btn.classList.contains("selected")){
            btn.classList.remove("selected");
            selectedTensions = selectedTensions.filter(item => item!==btn.textContent);
        }
        else{
            btn.classList.add("selected");
            selectedTensions.push(btn.textContent);
            console.log(btn.textContent);
        }
    });
});

let progression = [];

const add_btn = document.querySelector(".add-btn");
add_btn.addEventListener("click",function(){
    if(!selectedRoot){
        return
    }
    else{
        if(selectedTensions.length === 0){
            progression.push(selectedRoot+selectedQuality)
        }
        else{
            progression.push(`${selectedRoot}${selectedQuality}(${selectedTensions.join(",")})`)
        }

    }
        
    let prog_str = progression.join(" → ");
    document.getElementById("progression-display").textContent = prog_str;
});

const save_btn = document.getElementById("save-btn");
save_btn.addEventListener("click",function(){
    fetch("http://localhost:8000/save", {
    method: "POST",                           // 「送る」操作
    headers: {"Content-Type": "application/json"}, // 「JSON形式で送ります」
    body: JSON.stringify({                    // データをJSON文字列に変換
        title: document.getElementById("title-input").value,
        chords: document.getElementById("progression-display").textContent
    })
})
    .then(function() {
        console.log("保存完了！");
        progression = [];
        document.getElementById("progression-display").textContent = "";
    });
});

function loadProgressions(){
    document.getElementById("saved-list").innerHTML = "";
    fetch("http://localhost:8000/progressions")
        .then(function(response) {
            return response.json();  // JSON文字列 → JS オブジェクトに変換
        })
        .then(function(data) {
            data.forEach(function(item){
                document.getElementById("saved-list").innerHTML += 
                `<tr>
                    <td class="table-data">${item.title}</td>
                    <td class="table-data">${item.chords}</td>
                    <td class="table-data">${item.key_root}</td>
                    <td class="table-data">${item.created_at}</td>
                    <td class="table-data"><button class="delete-btn" data-id="${item.id}">🗑️</button></td>
                </tr>`
            });
                document.querySelectorAll(".delete-btn").forEach(function(btn){
                btn.addEventListener("click",function(){
                    const id = btn.dataset.id;
                    fetch(`http://localhost:8000/progressions/${id}`, {
                        method: "DELETE"
                    }).then(function() {
                        loadProgressions();  // 一覧を再読み込み
                    });
                });
            });
        });
}

loadProgressions();



//進行追加ボタンが押されたとき、ページを遷移する
document.getElementById("add").addEventListener("click",function(){
    document.getElementById("home").style.display = "none";
    document.getElementById("edit-page").style.display = "block";
});

