/**
 * Created by huangjia on 17-2-17.
 */


function initPostList() {
    $.getJSON("../../data.json",function (data) {
        alert(data);
    });
}