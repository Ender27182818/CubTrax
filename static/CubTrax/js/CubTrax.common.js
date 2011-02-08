function remove_substance_wrapper( event_object )
{
	alert('removing from DB substance with name ' + event_object.currentTarget.id.replace('_', ' '));
	Dajaxice.Squirly.remove_substance( 'remove_from_substance_table', {'name':event_object.currentTarget.id.replace('_', ' ')} );
}

// Set up the buttons to look like buttons and give them appropriate events
function setup_buttons() {

	// Set up button style
	$( ".button").button();

	// Set up the substance delete buttons
	$( ".substance_delete_button" ).unbind().click( remove_substance_wrapper );
}


// Set up stripey table rows
function stripe_tables() {
	$(".stripeMe tr:even").addClass("alt");
	$(".stripeMe tr").mouseover(function() {$(this).addClass("over");	}).mouseout(function() {$(this).removeClass("over");});
}


function add_to_substance_table(data) {
	// Add the new row
	var underscored_name = data.name.replace(' ', '_');
	var new_row = "<tr id=\"substance_row_" + underscored_name + "\"><td>" + data.name + "</td><td>...flavors...</td><td><button class=\"substance_delete_button button\" id=\"" + underscored_name + "\">X</button></td></tr>";
	$( '#substance_table tr:last' ).after( new_row );

	// Highlight the new row
	$( '#substance_table tr:last' ).effect('highlight');

	// Re-color the rows
	stripe_tables();

	// Re-buttonify the buttons
	setup_buttons();
	//<td><button class="substance_delete_button button" id="{{substance.underscored_name}}">X</button></td>
}

function remove_from_substance_table(data) {
	// Find the row we are interested in
	$( '#substance_row_' + data.name.replace(' ', '_') ).remove();
}

