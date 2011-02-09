// Set up the buttons to look like buttons and give them appropriate events
function buttonize() {
	// Set up button style
	$( ".button").button();
}


// Set up stripey table rows
function stripe_tables() {
	$(".stripeMe tr:even").addClass("alt");
	$(".stripeMe tr").mouseover(function() {$(this).addClass("over");	}).mouseout(function() {$(this).removeClass("over");});
}


