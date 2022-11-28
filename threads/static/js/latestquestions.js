'use strict'

{
    const howManyAgo = document.getElementsByClassName('how');
    const latestquestions_id = document.getElementById('latestquestions-0');
    const latestquestions_class = document.getElementsByClassName('latestquestions');
    const morelink = document.getElementById('morelink');
    window.onload = function () {
        console.log('JS起動');
    }
    morelink.addEventListener('click', () => {
        console.log('more')
        changeclass();
        removelink()
    })
    function changeclass() {
        latestquestions_id.classList.remove('latestquestions');
        latestquestions_id.classList.add('latestquestions-linknone');
    }
    function removelink() {
        morelink.remove();
    }
    function createquestions() {
    }









}
