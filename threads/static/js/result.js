'use strict'
{

   const title = document.getElementById('question');

  //  ans = answer
  //  ras = reans
   const mgz = document.getElementById('mygraphzone');

  class EditList{
    constructor(basisarray){
      // 基準となる配列一つと、それに連動して編集させたい配列計5個まで、
      this.basisarray = basisarray;
      if(arguments[1]){
      this.array1 = arguments[1];
      }
      if(arguments[2]){
      this.array2 = arguments[2];
      }
      if(arguments[3]){
        this.array3 = arguments[3];
      }
    }

    descending_order_based_on_criteria(){
      // basisarrayをもとにそれと渡された他の配列も入れ替える。
      let orderlist =[];
      let basisarray = this.basisarray.concat();
      let array1;
      let array2;
      let array3;
      if(typeof this.array1!== 'undefined'){
        array1 = this.array1.concat();
      }
      if(typeof this.array2 !== 'undefined'){
        array2 = this.array2.concat();
      }
      if(typeof this.array3 != 'undefined'){
        array3 = this.array3.concat();
      }
       for(let outer = 0; outer < basisarray.length -1; outer++){
         for(let i = basisarray.length-1; i > outer; i--){
           if(basisarray[i-1] < basisarray[i]){
             let tmp =basisarray[i-1];
             basisarray[i-1] = basisarray[i];
             basisarray[i] = tmp;
             if(array1){
             let tmp1 = array1[i-1];
             array1[i-1] = array1[i];
             array1[i] = tmp1;
             }
             if(array2){
             let tmp2 = array2[i-1];
             array2[i-1] = array2[i];
             array2[i] = tmp2;
             }
             if(array3){
             let tmp3 = array3[i-1];
             array3[i-1] = array3[i];
             array3[i] = tmp3;
             }
            }
          }
        }
        orderlist.push(basisarray);
        if(array1){
        orderlist.push(array1);
      }
        if(array2){
        orderlist.push(array2);
        }
        if(array3){
        orderlist.push(array3);
      }
      return orderlist;
    }

    cut_until_beyond(until,basisarray,array){
      let cutlist = [];
      let cubbasisarray = basisarray.concat();
      let cubarray = array.concat();
      if(cubbasisarray.length>until){
         let count = 0;
         while(cubbasisarray.length >until){
           count += cubbasisarray.pop();
           cubarray.pop();
         }
         cubbasisarray.push(count);
         cubarray.push('その他');
      }

      return [cubbasisarray,cubarray];
    }

    order_and_cut(until){
      const orderarray = this.descending_order_based_on_criteria();
      const orderbasisarray = orderarray[0];
      const ordertextarray = orderarray[1];
      const cubarray = this.cut_until_beyond(until,orderbasisarray,ordertextarray);
      return cubarray;
    }
  }
  class sepa_array{
    constructor(a_r){
      this.ans_ras = a_r;
    }

    get_property(){
      console.log(this.ans_ras);
    }

    get_labels_dates_reasons(){
      const labels =[];
      const dates = [];
      const reasons = [];

      for(let i=0;i < ans_ras.length; i++){
          const ar = this.ans_ras[i];
          labels.push(ar[0]);
          dates.push(ar[1]);
          reasons.push(ar[2]);

          const rlbs =[];
          const ranss = [];
        }

      // console.log(labels);
      // console.log(dates);
      // console.log(reasons);
      return [labels,dates,reasons];
  }

}

const b = new sepa_array([['タケノコ派',65,[['サクサクしとるで',42],['序盤中盤終盤',23]]],['キノコ派',86,[['なめまわすのがスコ',74],]]])
const ldr = b.get_labels_dates_reasons();


const a = new EditList([38, 31, 21, 10,10,10,10],["A型", "O型", "B型", "AB型","D型","E型","F型"]);
  // console.log(a.descending_order_based_on_criteria())
  // console.log(a.order_and_cut(4))



class ChartRlt{
  constructor(lbs,dts,stts){
    this.bc = ["#252e57", "#428abd", "#00627c", "#25799e", "#327585",
               "#59b5d1", "#009bcc", "#00678e", "#00aad6", "#009ec3",
               "#3b91c4", "#00869f", "#3c8490", "#4f95c5", "#002752",
               "#325e9a", "#5a8cb3", "#389192", "#428abd", "#88b6c9",
               "#006785", "#00375f", "#2d91ae", "#144384", "#00a4c4",
               "#006a9c", "#15485f", "#1289a4", "#004b8b", "#0085af",
               "#20597c", "#3a4789", "#508e9e", "#73aed5",
               "#00929b", "#4387bb", "#348baa", "#98c8e1", "#26747b",
               "#33b5ba", "#002a5a", "#005b8f", "#427596", "#325e9a",
               "#007888", "#7db0d6", "#004264", "#00607d", "#5782a1",
                "#72c5c1", "#4c6d9b", "#00668f", "#67c7d9"];
    this.lbs = lbs;
    this.dts = dts;
    this.stts = stts;

  }
  get_property(){
    console.log(this.lbs);
    console.log(this.dts);
  }
  choose_at_random(cc){
       let c = cc|| 1;
       let arraydate = this.bc;
       let result = [];
       for(var i = 0; i<c;i++){
           let arrayindex = Math.floor(Math.random()*arraydate.length)
           result[i] = arraydate[arrayindex];
           arraydate.splice(arrayindex,1)
       }
       console.log(result);
       return result
   }

  pieChart(){
     this.ctx = document.getElementById("cjsPieChart");
     this.cjsPieChart = new Chart(this.ctx, {
      type: 'pie',
      data: {
      labels: this.lbs,
      datasets: [{
          backgroundColor: this.choose_at_random(5),
          data: this.dts
      }]
    },
    options: {
      title: {
        display: true,
        text: ''
      }
     }
    });
  }

  PieChartdestroy(){
    console.log('削除！');
    if(this.cjsPieChart){
      this.cjsPieChart.destroy(); }
  }

  mygraph(){
    let count =0;
    for(let i=0; i< this.dts.length;i++){
        count += this.dts[i];
    }

    // console.log(count);
    while(mgz.firstChild){
        mgz.removeChild(mgz.firstChild)
       }
    for(let i=0;i<=this.lbs.length-1;i++){
      // 配列に保存されている総合データからデータとテキストを取得し、それらを簡単な棒グラフとして、描写する。
      // ここでは渡された配列の最初から羅列していくだけ。
      const lb= this.lbs[i];
      const dt= this.dts[i];

      const graphbox = document.createElement('div');

      if(this.stts){
        // もし、クラス第3引数を持つかどうかという条件
        // このサイトでは、sepa_arrayによって、返ってきた値を最初はconstructorに渡すので、投票結果の画面では、引数が三つ渡される。
        graphbox.setAttribute('class','graphboxP');
      }else{
        graphbox.setAttribute('class','graphboxC');
      }

      const  lbel = document.createElement('p');
        // lbel = label element
        lbel.textContent= lb;
        lbel.setAttribute('style','text-align:center;');

      const  graph = document.createElement('div');
        graph.classList.add('graph');
        const  bar = document.createElement('span');
        const width = Math.floor(dt/count*100);
        // ここで誤って、lbをしてしまうとNaN
        // console.log(width);
        bar.classList.add('bar');
        bar.setAttribute('style','width'+':'+new String(width)+'%');
        graph.appendChild(bar);
      //  if(choicesresults[i].length != 0){
        //    // もしchoicesresultsのi番目が空っぽなら、ボタンを設置しない。
        //   var choicereasonel = document.createElement('button');
        //      choicereasonel.classList.add('reasonbtn');
        //      choicereasonel.setAttribute('id',`${i}`);
        //      choicereasonel.textContent = '理由';
        //      graphbox.appendChild(choicereasonel);
        //  }

        const dtel = document.createElement('span');
        dtel.setAttribute('class', 'gbspan')
        // date element
           dtel.textContent = dt;
           dtel.setAttribute('style','text-align:center;');

        graphbox.appendChild(lbel);
        graphbox.appendChild(graph);
        graphbox.appendChild(dtel);
      mgz.appendChild(graphbox);
    }
  }

}


  // c.get();
  // pieChart(["A型", "O型", "B型", "AB型","D型","E型","F型"],[38, 31, 21, 10,10,10,10],choose_at_random(gcolor,8))
  // mygraph(["A型", "O型", "B型", "AB型","D型","E型","F型"], [38, 31, 21, 10,10,10,10]);

  function checkansclick(){
    const ans = document.getElementsByClassName('graphboxP');
    for(let i=0;i<ans.length;i++){
        ans[i].addEventListener('click',()=>{
        const answerlabel = ldr[0][i];
        title.textContent = answerlabel;
        const reasons = ldr[2][i];
        const rlabels = [];
        const rdates =[];
        for(let i =0;i<reasons.length;i++){
          rlabels.push(reasons[i][0]);
          rdates.push(reasons[i][1]);
        }
        const rc = new ChartRlt(rlabels,rdates);

        c.PieChartdestroy();
        rc.pieChart();
        rc.mygraph();
        })
    }
}
  const c = new ChartRlt(...ldr);
  c.mygraph();
  c.pieChart();
  checkansclick();












 }
