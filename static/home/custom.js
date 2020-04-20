$(document).ready(function(){
	$(".reply-review").hide();
    $(this).click(function(e) {
        let nameId = e.target.id;
        let numberId = nameId.replace (/[^\d.]/g, '');
        if (nameId.includes('btn-reply')) {
            $(`#reply-review-${numberId}`).toggle()
        }
    });

});
