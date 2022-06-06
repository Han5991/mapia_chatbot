$(function () {
    const item = ['감사', '겸손', '경청', '공감', '공부', '공평', '관심', '관용', '긍정', '나눔',
        '노력', '도전', '믿음', '반성', '발전', '배려', '보람', '보살핌', '부지런함', '사랑',
        '생명존중', '성실', '솔선수범', '실천', '아름다움', '약속', '양보', '양심', '용기', '우정',
        '유머', '인내', '자신감', '자연사랑', '자유', '적극성', '절제', '깔끔', '정성', '존중',
        '질서', '착한마음', '책임', '친절', '평화', '행복', '협동', '희망'];
    // 32강
    let array1 = random(item, 34);
    // 16강
    let array2 = [];
    // 8강
    let array3 = [];
    // 4강
    let array4 = [];
    // 2강
    let array5 = [];
    // 우승
    let result = '';

    function random(item, size) {
        let new_item = [];
        const item_size = item.length;
        while (item.length > (item_size - size)) new_item.push(item.splice(Math.floor(Math.random() * item.length), 1)[0]);
        return new_item;
    }

    f('안녕').then((value) => {
        extracted('mymsg', '안녕');
        extracted('yourms', value.response);
    });

    $("input[type='text']").keypress(function (e) {
        if (e.keyCode === 13 && $(this).val().length) {
            let _val = $(this).val();
            f(_val).then((value) => {
                extracted('mymsg', _val);
                extracted('yourmsg', value.response);

                if (array1.length != 2) {
                    extracted('yourmsg', '32강');
                    extracted('yourmsg', '1.' + array1[0] + ' 2. ' + array1[1]);
                    if (value.response.includes('가치관')) {
                        array1.splice(0, 2)
                    }
                    if (value.entity != undefined) {
                        array1.splice(0, 2)
                        array2.push(value.entity)
                    }
                    console.log(array1)
                    console.log(array2)
                } else if (array2.length != 0) {
                    extracted('yourmsg', '16강');
                    extracted('yourmsg', '1.' + array2[0] + ' 2. ' + array2[1]);

                    if (value.entity != undefined) {
                        array2.splice(0, 2)
                        array3.push(value.entity)
                    }
                    console.log(array3)
                } else if (array3.length != 0) {
                    extracted('yourmsg', '8강');
                    extracted('yourmsg', '1.' + array3[0] + ' 2. ' + array3[1]);

                    if (value.entity != undefined) {
                        array3.splice(0, 2)
                        array4.push(value.entity)
                    }
                    console.log(array4)
                } else if (array4.length != 0) {
                    extracted('yourmsg', '준결승');
                    extracted('yourmsg', '1.' + array4[0] + ' 2. ' + array4[1]);

                    if (value.entity != undefined) {
                        array4.splice(0, 2)
                        array5.push(value.entity)
                    }
                    console.log(array5)
                } else if (array5.length != 0) {
                    extracted('yourmsg', '결승');
                    extracted('yourmsg', '1.' + array5[0] + ' 2. ' + array5[1]);

                    if (value.entity !== undefined) {
                        array5.splice(0, 2)
                        result = value.entity
                        extracted('yourmsg', result);
                    }
                    console.log(result)
                }
            });
            $(this).val('');
        }
    });

    function extracted(_class, _val) {
        if (_val !== '안녕') {
            $(".chat_wrap .inner").append('<div class="item ' + _class + '"><div class="box"><p class="msg">' + _val + '</p><span class="time">' + currentTime() + '</span></div></div>');
            let lastItem = $(".chat_wrap .inner").find(".item:last");
            setTimeout(function () {
                lastItem.addClass("on");
            }, 10);
            let position = lastItem.position().top + $(".chat_wrap .inner").scrollTop();
            $(".chat_wrap .inner").stop().animate({scrollTop: position}, 500);
        }
    }

    let currentTime = function () {
        let date = new Date();
        let hh = date.getHours();
        let mm = date.getMinutes();
        let apm = hh > 12 ? "오후" : "오전";
        return apm + " " + hh + ":" + mm + "";
    }

    async function f(chat) {
        return await fetch("http://127.0.0.1:5000", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                input: chat
            }),
        }).then(response => response.json());
    }

});