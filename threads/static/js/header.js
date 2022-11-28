'use strict'
{
//   const $hamburger = document.querySelector('.hamburger');
//   $hamburger.addEventListener('click',()=>{
//     $hamburger.classList.toggle('is-active');
//
//   });
// }
//   const $wrapper = document.getElementById('wrapper');
//   const $navBtn = document.getElementById('nav-btn');
//
//   $navBtn.addEventListener('click',navToggle());
//
//   function navToggle(){
//     console.log('CLICK');
//     if($wrapper.classList.contains('nav-open')){
//         navCloseFunc();
//     }else{
//         navOpenFunc();
//     }
//     function navOpenFunc(){
//       $wrapper.classList.add('nav-open');
//     }
//     function navCloseFunc(){
//       $wrapper.classList.remove('nav-open');
//     }

    $(function () {
        // クリック時の動作
        $('.hamberger_line').on('click', function() {
            // メニューを閉じる
            if($(this).hasClass('open')) {
                $(this).removeClass('open');
                $('.hamberger_list').removeClass('open');
            // メニューを開く
            } else {
                $(this).addClass('open');
                $('.hamberger_list').addClass('open');
            }
        });
    });


















  }
