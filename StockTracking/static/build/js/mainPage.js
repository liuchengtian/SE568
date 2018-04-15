$( document ).ready(function() {
	console.log( "ready!" );
	var url = "./backend/get_news";
	var input = {ticker: AMZN};
    $.ajax({type: "post",
        url: url,
        data: input,
        dataType: 'json',
        success: function(data){
            console.log(data)
        },
		fail: function(){
            alert('query fail.');
          }
        });
});