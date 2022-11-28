'use strict'
{
  const form = document.getElementById('form');

  const totalManageElement = document.getElementById('id_answer-TOTAL_FORMS');
  const moreanswer = document.getElementById('moreanswer');
  const addanszone = document.getElementById('addanszone');
  const max_num_forms = document.getElementById('id_answer-MAX_NUM_FORMS');
  let currentanscount = parseInt(totalManageElement.value);
  const max_num = max_num_forms.value;

  moreanswer.addEventListener('click',()=>{
        const tp = document.querySelectorAll('p');

        const p = document.createElement('p');

        const inputt = document.createElement('input');
        inputt.classList.add('answer_create_form');
        inputt.placeholder =`選択肢${currentanscount+1}`;
        inputt.type = `text`;
        inputt.name = `answer-${currentanscount}-text`;
        inputt.maxLength ='50';
        inputt.id = `id_answer-${currentanscount}-id`;
        p.appendChild(inputt);

        const inputh1 = document.createElement('input');
        inputh1.type = `hidden`
        inputh1.name = `answer-${currentanscount}-id`;
        inputh1.id = `id_answer-${currentanscount}-id`;
        p.appendChild(inputh1);

        const inputh2 = document.createElement(`input`);
        inputh2.type = `hidden`;
        inputh2.name = `answer-${currentanscount}-parent_question`;
        inputh2.id = `id_answer-${currentanscount}-parent_question`;
        p.appendChild(inputh2);

        addanszone.appendChild(p);
        currentanscount += 1;
        totalManageElement.value = currentanscount;
      // さっきまで上手く追加されなかった原因は、TOTAL_FORMSの値が更新されていなかったため
        if(max_num <= currentanscount){
          moreanswer.remove();
            alert('初期選択肢は10個までです。')
        }
    });


  }
