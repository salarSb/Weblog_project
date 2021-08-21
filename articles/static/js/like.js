$(document).ready(function () {
    $('.like-btn').click(function (event) {
        let articleId = $(event.target)[0].dataset.articleId;
        $.ajax({
            url: `/like/${articleId}`,
            method: 'POST',
            success: function (response) {
                let likes = response.likes;
                $('#like-count-' + articleId).html(likes);
            }
        });
    });
});