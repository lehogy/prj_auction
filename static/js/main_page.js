$(document).ready(function (){
    feed_box()
});

function feed_box() {
    $.ajax({
        type: 'GET',
        url: '/main/feed',
        date: {},
        success: function (response) {
            let rows = response['feeds']
            for(let i = 0; i < rows.length; i++) {
                let title =rows[i]['title']
                let user_id = rows[i]['user_id']
                let category = rows[i]['category']
                let date = rows[i]['date']
                let content = rows[i]['content']
                let like = rows[i]['like']
                let comment = rows[i]['comment']
                let price = rows[i]['price']
                let current = rows[i]['current']
                let dead = rows[i]['dead']

                let temp_html = `<div class="mainBox" style=" cursor: pointer;" onclick="location.href='#';">
                                    <h2>${title}</h2>
                                    <h5>ID: ${user_id}</h5>
                                    <h6>작성일: ${date}</h6>
                                    <h6>분류: ${category}</h6>
                                    <div class="bodyBox">
                                        <p>${content}
                                        </p>
                                    </div>
                        
                                    <button class="likeBox">
                                        ❤ ${like}
                                    </button>
                        
                                    <button class="commentBox">
                                        댓글(${comment})
                                    </button>
                        
                                    <div class="deadline">
                                        마감: ${dead}
                                    </div>
                        
                                    <div class="currentState">
                                        상태: ${current}
                                    </div>
                        
                                    <div class="price">
                                        현재 입찰가격: ${price}원
                                    </div>
                                </div> </br>`
                $('#allBox').append(temp_html)

            }
        }
    });
}

function new_comment() {
    $('#comment-cards').empty()
    function sort_field(field_name) {
        return (a, b) => a[field_name] > b[field_name] ? -1 : 1;
    }
    let rows = doc.sort(sort_field("time"))}