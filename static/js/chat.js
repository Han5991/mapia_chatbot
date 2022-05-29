$(function () {
    $("input[type='text']").keypress(function (e) {
        if (e.keyCode === 13 && $(this).val().length) {
            let _val = $(this).val();
            f(_val).then((value) => {
                extracted('mymsg', _val);
                extracted('yourmsg', value.response);
            });
            $(this).val('');
        }
    });

    function extracted(_class, _val) {
        $(".chat_wrap .inner").append('<div class="item ' + _class + '"><div class="box"><p class="msg">' + _val + '</p><span class="time">' + currentTime() + '</span></div></div>');
        let lastItem = $(".chat_wrap .inner").find(".item:last");
        setTimeout(function () {
            lastItem.addClass("on");
        }, 10);
        let position = lastItem.position().top + $(".chat_wrap .inner").scrollTop();
        $(".chat_wrap .inner").stop().animate({scrollTop: position}, 500);
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