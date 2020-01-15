$("input[type='text']").keypress(function (event) {
    if (event.which === 13) {
        //grabbing new todo text from input
        var todoText = $(this).val();
        $(this).val("");
        //create a new li and add to ul
        $(" .msg_card_body ").append(
            "<div class='d-flex justify-content-end mb-4'><div class='msg_cotainer_send'>"+todoText+"<span class='msg_time_send'>8:55 AM, Today</span></div><div class='img_cont_msg'>"
        )
	}
});