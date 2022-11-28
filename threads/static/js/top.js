'use strict'

{
const content = document.getElementById('content');

let category_exist = true;

console.log('JSは有効です。')
window.addEventListener('resize',()=>{
       console.log(category_exist);
       change_temp_from_window();
})

window.onload= function() {
    change_temp_from_window();
}


function change_temp_from_window(){
    const category = document.getElementById('category');
    if(window.outerWidth < 1850){
        if(category_exist){
            delete_category();
            category_exist=false;
        }
    }else{
        if(category_exist){
        }else{
            add_category();
            category_exist=true;
        }
    }
}
function delete_category(){
    category.innerHTML='';
    category.remove();


}
function add_category(){
    const category = document.createElement('div');
    category.setAttribute('id','category');
    const list_title = document.createElement('h1');
    list_title.classList.add("list-title");
    list_title.textContent="カテゴリー";
    const ul = document.createElement('ul');
    for(let i=0; i < 4;i++){
        const li = document.createElement('li');
        li.classList.add('category-list');
        li.textContent =`リンク`+`${i+1}`;
        ul.appendChild(li);
    }
    category.appendChild(list_title);
    category.appendChild(ul);

    content.insertBefore(category,content.firstChild);

}

// 1400px
}
